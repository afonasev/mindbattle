import { describe, expect, it, vi, afterEach } from 'vitest';
import { mkdtemp, readFile, writeFile, rm, readdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { ResultObserver, metrics, questionVersion, type ResultEvent } from '../../src/statistics/events';
import { ResultUploader, type ResultQueue } from '../../src/statistics/outbox';
import { createMatch, excludeNetworkPlayer } from '../../src/domain/match';
import { createSoloRun, reduceSoloFrame } from '../../src/domain/solo';
import { ANSWER_POSITIONS, type DomainContext, type MatchState, type QuestionDefinition } from '../../src/domain/types';
import { makeContext, send } from './network-fixture';
import { createResultStore, createServerResultQueue, validateResult } from '../../server/resultStore.mjs';
import { resultReport, interruptedNetworkCheckpoints } from '../../server/resultReport.mjs';
import { NetworkRoom } from '../../src/network/room';
const context = (): DomainContext => {
  const c = makeContext();
  const convert = (q: QuestionDefinition): QuestionDefinition => ({ ...q, correctAnswerId: 'answer-0', answers: q.answers.map((a, i) => ({ ...a, id: `answer-${i}` })) as unknown as QuestionDefinition['answers'] });
  return { ...c, getQuestion: id => { const q = c.getQuestion(id); return q && convert(q); }, selectQuestion: r => { const s = c.selectQuestion(r); return { ...s, question: convert(s.question) }; } };
};
function answering(mode: 'classic-v1' | 'network-v1' = 'classic-v1', count = 4) {
  const ctx = context();
  let s = createMatch({ profile: mode, questionCount: 9, answerTimeMs: 10000, teams: mode === 'classic-v1' ? ['green', 'blue', 'yellow', 'red'].slice(0, count) as MatchState['config']['teams'] : Array.from({ length: count }, (_, i) => `player-${i + 1}` as const), collectQuestionFeedback: false }, 'stats-seed', 0, ctx, `${mode}:stats-seed`);
  if (s.phase.kind !== 'normal-topic') throw Error();
  s = send(s, ctx, [{ type: 'confirm-topic', teamId: s.phase.chooser }]);
  s = send(s, ctx, [], 3000);
  if (s.phase.kind !== 'answering') throw Error('not answering');
  return { ctx, s };
}
function revealed(mode: 'classic-v1' | 'network-v1', results: ('correct' | 'wrong' | 'timeout')[]) {
  const { ctx, s } = answering(mode, results.length);
  if (s.phase.kind !== 'answering') throw Error();
  const correct = s.phase.round.correctPosition, wrong = ANSWER_POSITIONS.find(p => p !== correct)!;
  let next = send(s, ctx, results.flatMap((r, i) => r === 'timeout' ? [] : [{ type: 'answer' as const, teamId: s.teams[i].id, position: r === 'correct' ? correct : wrong }]));
  next = send(next, ctx, [], 100_000);
  const events: ResultEvent[] = [];
  const observer = new ResultObserver({ enqueue: e => events.push(e) }, ctx);
  observer.match(next); observer.match(next); observer.match({ ...next, phase: next.phase });
  return { events, observer, ctx, state: next };
}
function sample(): ResultEvent { return revealed('classic-v1', ['correct', 'wrong']).events[0]; }
afterEach(() => vi.useRealTimers());
describe('authoritative result observations', () => {
  it.each(['classic-v1', 'network-v1'] as const)('counts correct/wrong/no-answer/partial separately in %s', mode => {
    for (const [answers, expected] of [
      [['correct', 'correct'], { correct: 2, wrong: 0, noAnswer: 0, timeout: 0, allCorrect: true, noneCorrect: false, noSelection: false, correctRate: 1 }],
      [['wrong', 'wrong'], { correct: 0, wrong: 2, noAnswer: 0, timeout: 0, allCorrect: false, noneCorrect: true, noSelection: false, correctRate: 0 }],
      [['timeout', 'timeout'], { correct: 0, wrong: 0, noAnswer: 2, timeout: 2, allCorrect: false, noneCorrect: true, noSelection: true, correctRate: 0 }],
      [['correct', 'wrong', 'timeout'], { correct: 1, wrong: 1, noAnswer: 1, timeout: 1, allCorrect: false, noneCorrect: false, noSelection: false, correctRate: 1 / 3 }]
    ] as const) {
      const { events } = revealed(mode, [...answers]);
      expect(events.filter(e => e.kind === 'question')).toHaveLength(1);
      expect({ ...events[0], ...metrics(events[0]) }).toMatchObject({ eligible: answers.length, ...expected });
      expect(validateResult(events[0])).toBe(true);
      expect(Object.values(events[0].choices!).reduce((a, b) => a + b)).toBe(expected.correct + expected.wrong);
    }
  });
  it('excludes spectators before reveal, keeps bonus/tie observations distinct and null denominator safe', () => {
    const { ctx, s } = answering('network-v1', 3);
    if (s.phase.kind !== 'answering') throw Error();
    let next = excludeNetworkPlayer(s, s.teams[0].id, ctx);
    next = send(next, ctx, [], 100_000);
    const events: ResultEvent[] = [], observer = new ResultObserver({ enqueue: e => events.push(e) }, ctx);
    observer.match(next);
    expect(events[0]).toMatchObject({ eligible: 2, noAnswer: 2 });
    if (next.phase.kind !== 'reveal') throw Error();
    const tie: MatchState = { ...next, tieBreak: { originalLeaders: [s.teams[1].id, s.teams[2].id], contenders: [s.teams[1].id, s.teams[2].id], questionNumber: 1 }, phase: { ...next.phase, round: { ...next.phase.round, mode: 'tie-break', points: 0 } } };
    observer.match(tie); observer.match({ ...tie, tieBreak: { ...tie.tieBreak!, questionNumber: 2 } });
    expect(events.filter(e => e.kind === 'question').map(e => e.eventId)).toHaveLength(3);
    expect(events.filter(e => e.kind === 'question').slice(1).every(e => e.roundKind === 'tie-break')).toBe(true);
    expect(metrics({ ...events[0], eligible: 0, noAnswer: 0 })).toEqual({ allCorrect: false, noneCorrect: false, noSelection: false, correctRate: null });
    observer.match({ ...next, mainQuestionIndex: 3, phase: { ...next.phase, round: { ...next.phase.round, points: 200 } } });
    expect(events.find(e => e.kind === 'question' && e.ordinal === 3)?.roundKind).toBe('bonus');
  });
  it('records every endless solo reveal, final exhausted run and explicit interruption without names', () => {
    const ctx = context(), events: ResultEvent[] = [], observer = new ResultObserver({ enqueue: e => events.push(e) }, ctx);
    let state = createSoloRun({ profile: 'solo-endless-v1', collectQuestionFeedback: false }, 'solo-stats', 0, ctx);
    for (let i = 0; i < 3; i++) {
      state = reduceSoloFrame(state, { atMs: state.lastFrameAtMs, commands: [{ type: 'confirm-topic' }] }, ctx);
      state = reduceSoloFrame(state, { atMs: state.lastFrameAtMs + 100_000, commands: [] }, ctx);
      observer.solo(state); observer.solo(state);
      state = reduceSoloFrame(state, { atMs: state.lastFrameAtMs, commands: [{ type: 'continue' }] }, ctx);
      observer.solo(state);
    }
    expect(events.filter(e => e.kind === 'question')).toHaveLength(3);
    expect(events.filter(e => e.kind === 'question').every(e => e.timeout === 1)).toBe(true);
    expect(events.at(-1)).toMatchObject({ kind: 'match', status: 'completed', lives: 0 });
    observer.solo({ ...state, runId: 'unfinished', phase: { kind: 'topic', candidates: ['a', 'b', 'c'], cursor: 0 } }, 'replaced');
    expect(events.at(-1)?.status).toBe('interrupted');
    expect(validateResult({ ...events.at(-1), score: -200 })).toBe(true);
    expect(JSON.stringify(events)).not.toMatch(/name|token/);
  });
  it('fingerprints question content and leaves rules intact even when the sink throws', () => {
    const { events, ctx, state } = revealed('classic-v1', ['correct', 'wrong']);
    const modified = { ...ctx, getQuestion: (id: string) => ({ ...ctx.getQuestion(id)!, prompt: 'Edited' }) };
    expect(questionVersion(ctx, events[0].questionId!)).not.toBe(questionVersion(modified, events[0].questionId!));
    expect(() => new ResultObserver({ enqueue: () => { throw Error('disk'); } }, ctx).match(state)).not.toThrow();
  });
  it('network snapshots/reconnect do not multiply observations and room close records interruption', () => {
    const events: ResultEvent[] = []; let id = 0;
    const room = new NetworkRoom('0001', 'display', context(), {}, () => `secret-${++id}`, async () => {}, () => {}, { enqueue: e => events.push(e) });
    room.connect('display', 0); const a = room.join('PRIVATE NAME A', 0), b = room.join('PRIVATE NAME B', 0); room.connect(a.token, 0); room.connect(b.token, 0);
    const command = (token: string, action: Parameters<NetworkRoom['command']>[1]['action']) => room.command(token, { commandId: `cmd-${++id}`, epoch: room.epoch, phaseRevision: room.phaseRevision, action }, 0);
    command('display', { type: 'start' });
    if (room.state!.phase.kind !== 'normal-topic') throw Error();
    command(room.state!.phase.chooser === a.id ? a.token : b.token, { type: 'topic', topicId: room.state!.phase.candidates[0] });
    command(a.token, { type: 'continue' });
    const active = room.state as MatchState;
    if (active.phase.kind !== 'answering') throw Error();
    const pos = active.phase.round.correctPosition;
    command(a.token, { type: 'answer', position: pos }); command(b.token, { type: 'answer', position: pos });
    for (let i = 0; i < 10; i++) { room.snapshot(a.token, 0); room.snapshot('display', 0); }
    const g = room.connect(a.token, 0); room.disconnect(a.token, g, 0); room.connect(a.token, 0);
    expect(events.filter(e => e.kind === 'question')).toHaveLength(1);
    command(a.token, { type: 'close' });
    expect(events.at(-1)).toMatchObject({ kind: 'match', status: 'interrupted', reason: 'closed' });
    expect(JSON.stringify(events)).not.toContain('PRIVATE');
  });
});
class Queue implements ResultQueue {
  events = new Map<string, ResultEvent>(); fail = false;
  async put(e: ResultEvent) { if (this.fail) throw Error('quota'); this.events.set(e.eventId, e); }
  async list() { return [...this.events.values()]; }
  async remove(id: string) { this.events.delete(id); }
}
describe('independent delivery and read-only aggregation', () => {
  it('offline → restart → online retries retained events and requires matching ACK', async () => {
    vi.useFakeTimers(); const q = new Queue(), e = sample();
    const first = new ResultUploader(q, async () => { throw Error('offline'); }); first.enqueue(e); await first.flush(); first.stop();
    expect(q.events.size).toBe(1);
    const wrongAck = new ResultUploader(q, async () => 'wrong-id'); await wrongAck.flush(); wrongAck.stop(); expect(q.events.size).toBe(1);
    const next = new ResultUploader(q, async event => event.eventId); await next.flush(); next.stop(); expect(q.events.size).toBe(0);
  });
  it('does not await a hung server during enqueue and retries local quota failure', async () => {
    vi.useFakeTimers(); const q = new Queue(); q.fail = true; const e = sample();
    const uploader = new ResultUploader(q, async event => event.eventId);
    expect(uploader.enqueue(e)).toBeUndefined(); await uploader.flush(); expect(q.events.size).toBe(0);
    q.fail = false; await uploader.flush(); uploader.stop(); expect(q.events.size).toBe(0);
    let release!: (id: string) => void;
    const hung = new ResultUploader(q, () => new Promise(resolve => { release = resolve; })); hung.enqueue(e);
    const flight = hung.flush(); await vi.waitFor(() => expect(release).toBeTypeOf('function'));
    expect(q.events.size).toBe(1); release(e.eventId); await flight; hung.stop();
  });
  it('online arriving during an in-flight failure retries immediately afterward', async () => {
    vi.useFakeTimers(); const q = new Queue(); await q.put(sample());
    let reject!: (error: Error) => void; let attempt = 0;
    const uploader = new ResultUploader(q, event => ++attempt === 1 ? new Promise((_resolve, fail) => { reject = fail; }) : Promise.resolve(event.eventId));
    const flight = uploader.flush(); await vi.waitFor(() => expect(reject).toBeTypeOf('function'));
    uploader.wake(); reject(Error('old offline request')); await flight;
    await vi.advanceTimersByTimeAsync(1); expect(attempt).toBe(2); expect(q.events.size).toBe(0); uploader.stop();
  });
  it('fsync journal deduplicates concurrently/reordered payloads/restarts, rejects conflicts and recovers torn tail', async () => {
    const dir = await mkdtemp(join(tmpdir(), 'mindbattle-results-'));
    try {
      const path = join(dir, 'events.ndjson'), e = sample(), store = await createResultStore(path);
      const acks = await Promise.all([store.append(e), store.append(e)]);
      expect(acks.map(a => a.status)).toEqual(['created', 'duplicate']);
      expect((await store.append(Object.fromEntries(Object.entries(e).reverse()) as unknown as ResultEvent)).status).toBe('duplicate');
      expect((await store.append({ ...e, questionVersion: 'domain-v1-fnv64:1111111111111111' })).status).toBe('conflict');
      expect(validateResult({ ...e, name: 'private' })).toBe(false); expect(validateResult({ ...e, mode: 'network-v1' }, false)).toBe(false);
      expect(validateResult({ ...e, noAnswer: 10 })).toBe(false);
      await writeFile(path, (await readFile(path, 'utf8')) + '{torn');
      const reopened = await createResultStore(path); expect((await reopened.append(e)).status).toBe('duplicate');
      expect((await readFile(path, 'utf8')).trim().split('\n')).toHaveLength(1);
    } finally { await rm(dir, { recursive: true }); }
  });
  it('server persistent spool survives unavailable storage and restart until ACK', async () => {
    const dir = await mkdtemp(join(tmpdir(), 'mindbattle-spool-'));
    const e = sample(); let fail = true;
    const first = createServerResultQueue(dir, async event => { if (fail) throw Error('disk unavailable'); return { status: 'created', eventId: event.eventId }; });
    try {
      first.enqueue(e); await new Promise(resolve => setTimeout(resolve, 30)); await first.flush(); first.stop();
      expect((await readdir(dir)).filter(n => n.endsWith('.json'))).toHaveLength(1);
      fail = false; const second = createServerResultQueue(dir, async event => ({ status: 'duplicate', eventId: event.eventId }));
      await new Promise(resolve => setTimeout(resolve, 30)); await second.flush(); second.stop(); expect(await readdir(dir)).toEqual([]);
    } finally { first.stop(); await rm(dir, { recursive: true }); }
  });
  it('recovers network start/reveal checkpoints after restart with valid terminal payloads', () => {
    const { ctx, s } = answering('network-v1', 2), events: ResultEvent[] = [];
    const o = new ResultObserver({ enqueue: e => events.push(e) }, ctx); o.match(s, undefined, true);
    const recovered = interruptedNetworkCheckpoints(events);
    expect(recovered).toHaveLength(1); expect(validateResult(recovered[0])).toBe(true);
    expect(recovered[0]).toMatchObject({ status: 'interrupted', reason: 'server-restart' });
    expect(interruptedNetworkCheckpoints([...events, recovered[0]])).toEqual([]);
  });
  it('groups modes/versions, excludes duplicate observations and separates 0% selection absence', () => {
    const correct = revealed('classic-v1', ['correct', 'correct']).events[0], none = revealed('network-v1', ['timeout', 'timeout']).events[0];
    const report = resultReport([correct, correct, none, { ...correct, eventId: 'edited', questionVersion: 'domain-v1-fnv64:1111111111111111' }]);
    expect(report.questions).toHaveLength(3); expect(report.hundredPercent).toHaveLength(2); expect(report.zeroPercent).toHaveLength(1);
    expect(report.noSelection).toHaveLength(1); expect(report.questions.every(g => g.observations === 1)).toBe(true);
  });
});
