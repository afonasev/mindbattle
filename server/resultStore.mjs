import { mkdir, open, readFile, truncate, readdir, rename, unlink } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { createHash, randomUUID } from 'node:crypto';

function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (value && typeof value === 'object') return Object.fromEntries(Object.keys(value).sort().map(k => [k, canonical(value[k])]));
  return value;
}
const encode = e => JSON.stringify(canonical(e));
const common = ['schemaVersion', 'eventId', 'matchId', 'mode', 'catalogRevision', 'kind', 'ordinal'];
const questionKeys = ['questionId', 'questionVersion', 'assignedDifficulty', 'roundKind', 'eligible', 'correct', 'wrong', 'noAnswer', 'timeout', 'choices'];
const matchKeys = ['status', 'reason', 'units', 'score', 'lives', 'winnerId'];
const count = n => Number.isSafeInteger(n) && n >= 0;
const text = s => typeof s === 'string' && s.length > 0 && s.length <= 256;
export function validateResult(e, allowNetwork = true) {
  if (!e || typeof e !== 'object' || Array.isArray(e) || e.schemaVersion !== 1 || !['solo-endless-v1', 'classic-v1', 'network-v1'].includes(e.mode) || (!allowNetwork && e.mode === 'network-v1') || !['question', 'match'].includes(e.kind) || !count(e.ordinal)) return false;
  if (!['eventId', 'matchId', 'catalogRevision'].every(k => text(e[k]))) return false;
  const keys = [...common, ...(e.kind === 'question' ? questionKeys : matchKeys)];
  if (Object.keys(e).some(k => !keys.includes(k))) return false;
  if (e.kind === 'question') {
    if (!text(e.questionId) || !/^domain-v1-fnv64:[0-9a-f]{16}$/.test(e.questionVersion) || !['easy', 'medium', 'hard'].includes(e.assignedDifficulty) || !['normal', 'bonus', 'tie-break'].includes(e.roundKind)) return false;
    if (!['eligible', 'correct', 'wrong', 'noAnswer', 'timeout'].every(k => count(e[k])) || e.eligible > 12 || (e.mode === 'classic-v1' && e.eligible > 4) || (e.mode === 'solo-endless-v1' && e.eligible !== 1)) return false;
    if (e.correct + e.wrong + e.noAnswer !== e.eligible || e.timeout > e.noAnswer) return false;
    if (!e.choices || Array.isArray(e.choices) || Object.keys(e.choices).length !== 4 || !Object.entries(e.choices).every(([k, v]) => /^answer-[0-3]$/.test(k) && count(v)) || Object.values(e.choices).reduce((a, b) => a + b, 0) !== e.correct + e.wrong) return false;
    return true;
  }
  if (!['in-progress', 'completed', 'interrupted'].includes(e.status) || !text(e.reason)) return false;
  if (e.mode === 'solo-endless-v1') return Number.isSafeInteger(e.score) && count(e.lives) && e.lives <= 3 && e.units === undefined && e.winnerId === undefined;
  const validId = id => e.mode === 'classic-v1' ? ['green', 'blue', 'yellow', 'red'].includes(id) : /^player-([1-9]|1[0-2])$/.test(id);
  return e.score === undefined && e.lives === undefined && Array.isArray(e.units) && e.units.length >= 2 && e.units.length <= (e.mode === 'classic-v1' ? 4 : 12) && new Set(e.units.map(u => u.id)).size === e.units.length && e.units.every(u => u && validId(u.id) && Object.keys(u).length === 5 && ['score', 'correct', 'incorrect', 'noAnswer'].every(k => count(u[k])) && u.noAnswer <= u.incorrect) && (e.winnerId === undefined || validId(e.winnerId));
}
export async function createResultStore(filePath) {
  await mkdir(dirname(filePath), { recursive: true });
  let source = '';
  try { source = await readFile(filePath, 'utf8'); } catch (e) { if (e.code !== 'ENOENT') throw e; }
  // A crash may leave a torn final write: it was never ACKed and will be replayed.
  if (source && !source.endsWith('\n')) {
    source = source.slice(0, source.lastIndexOf('\n') + 1);
    await truncate(filePath, Buffer.byteLength(source));
  }
  const events = new Map();
  for (const line of source.split('\n').filter(Boolean)) {
    const e = JSON.parse(line);
    if (!validateResult(e)) throw new Error('Corrupt result journal');
    if (events.has(e.eventId) && encode(events.get(e.eventId)) !== encode(e)) throw new Error('Conflicting result journal');
    events.set(e.eventId, e);
  }
  let chain = Promise.resolve();
  return {
    append(e) {
      const work = chain.then(async () => {
        if (!validateResult(e)) return { status: 'invalid', eventId: e?.eventId };
        const previous = events.get(e.eventId);
        if (previous) return { status: encode(previous) === encode(e) ? 'duplicate' : 'conflict', eventId: e.eventId };
        const file = await open(filePath, 'a');
        try { await file.writeFile(JSON.stringify(e) + '\n'); await file.sync(); } finally { await file.close(); }
        events.set(e.eventId, e);
        return { status: 'created', eventId: e.eventId };
      });
      chain = work.catch(() => {});
      return work;
    }
  };
}
// Spool writes and result writes run outside the room reducer. Durable files survive restarts.
export function createServerResultQueue(directory, append) {
  const pending = new Map();
  let writing = Promise.resolve(), running = false;
  async function persist(e) {
    await mkdir(directory, { recursive: true });
    const name = createHash('sha256').update(e.eventId).digest('hex') + '.json';
    const path = join(directory, name), temp = path + '.' + randomUUID() + '.tmp';
    const file = await open(temp, 'wx');
    try { await file.writeFile(JSON.stringify(e)); await file.sync(); } finally { await file.close(); }
    await rename(temp, path);
    const dir = await open(directory, 'r');
    try { await dir.sync(); } finally { await dir.close(); }
  }
  async function flush() {
    if (running) return;
    running = true;
    try {
      await writing;
      for (const e of pending.values()) { await persist(e); pending.delete(e.eventId); }
      await mkdir(directory, { recursive: true });
      for (const name of await readdir(directory)) {
        if (!/^[0-9a-f]{64}\.json$/.test(name)) continue;
        const path = join(directory, name), e = JSON.parse(await readFile(path, 'utf8'));
        const ack = await append(e);
        if (['created', 'duplicate'].includes(ack.status) && ack.eventId === e.eventId) await unlink(path);
      }
    } catch (error) { console.error('Result outbox retry:', error.message); }
    finally { running = false; }
  }
  const timer = setInterval(() => void flush(), 5000); timer.unref();
  void flush();
  return {
    enqueue(e) {
      pending.set(e.eventId, e);
      writing = writing.then(async () => { try { await persist(e); pending.delete(e.eventId); } catch { /* next flush retries memory */ } });
      void writing.then(flush);
    },
    flush,
    stop() { clearInterval(timer); }
  };
}
