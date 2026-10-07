import { mkdir, open, readFile, stat, writeFile, rename } from "node:fs/promises";
import { dirname } from "node:path";

const LEVELS = ["easy", "medium", "hard"];
const levelIndex = new Map(LEVELS.map((level, index) => [level, index]));

function canonicalEvent(event) {
  const base = {
    schemaVersion: event.schemaVersion,
    eventId: event.eventId,
    matchId: event.matchId,
    catalogRevision: event.catalogRevision,
    questionId: event.questionId,
    assignedDifficulty: event.assignedDifficulty,
  };
  return JSON.stringify(event.schemaVersion === 1 ? { ...base, perceivedDifficulty: event.perceivedDifficulty } : event.schemaVersion === 2 ? { ...base, responses: event.responses } : { ...base, hasComplaint: event.hasComplaint, complaintReasons: event.complaintReasons, ...(event.complaintNote ? { complaintNote: event.complaintNote } : {}) });
}

export function validateFeedbackEvent(value, questions, catalogRevision) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return "Ожидался JSON-объект";
  const strings = ["eventId", "matchId", "catalogRevision", "questionId"];
  if (![1, 2, 3].includes(value.schemaVersion) || strings.some((key) => typeof value[key] !== "string" || value[key].length === 0)) {
    return "Некорректная схема события";
  }
  if (!LEVELS.includes(value.assignedDifficulty)) {
    return "Некорректный уровень сложности";
  }
  if (value.catalogRevision !== catalogRevision) return "Ревизия каталога не поддерживается";
  const assigned = questions.get(value.questionId);
  if (!assigned) return "Неизвестный questionId";
  if (assigned !== value.assignedDifficulty) return "assignedDifficulty не соответствует каталогу";
  if (value.schemaVersion === 1) return LEVELS.includes(value.perceivedDifficulty) ? null : "Некорректный уровень сложности";
  if (value.schemaVersion === 3) {
    const reasons = ["too-easy", "too-hard", "weak-answer-options", "unclear-wording", "suspected-error", "ambiguous-answer", "uninteresting-for-quiz"];
    if (typeof value.hasComplaint !== "boolean" || !Array.isArray(value.complaintReasons) || new Set(value.complaintReasons).size !== value.complaintReasons.length || !value.complaintReasons.every((reason) => reasons.includes(reason)) || (value.complaintReasons.includes("too-easy") && value.complaintReasons.includes("too-hard")) || (value.complaintNote !== undefined && (typeof value.complaintNote !== "string" || [...value.complaintNote].length > 500))) return "Некорректная жалоба";
    const hasSignal = value.complaintReasons.length > 0 || (typeof value.complaintNote === "string" && value.complaintNote.trim().length > 0);
    return value.hasComplaint === hasSignal && (!value.hasComplaint ? value.complaintNote === undefined : true) ? null : "Причины или заметка не согласованы с жалобой";
  }
  const flags = ["unfamiliar-topic", "unclear-wording", "suspected-error", "ambiguous-answer", "too-niche-or-uninteresting", "weak-answer-options"];
  if (!Array.isArray(value.responses) || value.responses.length === 0 || !value.responses.every((response) => response && typeof response === "object" && ["trivial", "easy", "medium", "hard"].includes(response.perceivedDifficulty) && ["like", "abstain", "dislike"].includes(response.similarityPreference) && Array.isArray(response.diagnosticFlags) && new Set(response.diagnosticFlags).size === response.diagnosticFlags.length && response.diagnosticFlags.every((flag) => flags.includes(flag)))) return "Некорректные ответы фидбэка";
  return null;
}

function emptyAggregate() {
  return { total: 0, perceived: { easy: 0, medium: 0, hard: 0 }, exact: 0, lower: 0, higher: 0 };
}

function addToAggregate(target, event) {
  target.total += 1;
  target.perceived[event.perceivedDifficulty] += 1;
  const assigned = levelIndex.get(event.assignedDifficulty);
  const perceived = levelIndex.get(event.perceivedDifficulty);
  if (assigned === perceived) target.exact += 1;
  else if (perceived < assigned) target.lower += 1;
  else target.higher += 1;
}

function withRates(aggregate) {
  const total = aggregate.total || 1;
  return {
    ...aggregate,
    rates: {
      exact: aggregate.exact / total,
      lower: aggregate.lower / total,
      higher: aggregate.higher / total
    }
  };
}

function emptyV2Aggregate() { return { total: 0, perceived: { trivial: 0, easy: 0, medium: 0, hard: 0 }, similarity: { like: 0, abstain: 0, dislike: 0 }, flags: { "unfamiliar-topic": 0, "unclear-wording": 0, "suspected-error": 0, "ambiguous-answer": 0, "too-niche-or-uninteresting": 0, "weak-answer-options": 0 }, unfamiliar: { total: 0, perceived: { trivial: 0, easy: 0, medium: 0, hard: 0 } } }; }
function addV2(target, response) { target.total += 1; target.perceived[response.perceivedDifficulty] += 1; target.similarity[response.similarityPreference] += 1; for (const flag of response.diagnosticFlags) target.flags[flag] += 1; if (response.diagnosticFlags.includes("unfamiliar-topic")) { target.unfamiliar.total += 1; target.unfamiliar.perceived[response.perceivedDifficulty] += 1; } }

export async function createFeedbackStore({ filePath, questions, catalogRevision, historicalCatalogs = {} }) {
  await mkdir(dirname(filePath), { recursive: true });
  let source = "";
  try { source = await readFile(filePath, "utf8"); } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }
  // Trusted manifests live beside the journal, outside web-root, across releases.
  const registryPath = `${filePath}.catalogs.json`;
  let registry = {};
  try { registry = JSON.parse(await readFile(registryPath, 'utf8')); }
  catch (error) { if (error?.code !== 'ENOENT') throw error; }
  const incoming = { ...historicalCatalogs, [catalogRevision]: Object.fromEntries(questions) };
  const canonical = map => JSON.stringify(Object.entries(map).sort(([a], [b]) => a.localeCompare(b)));
  for (const [revision, manifest] of Object.entries(incoming)) {
    if (registry[revision] && canonical(registry[revision]) !== canonical(manifest)) throw new Error(`Conflicting feedback catalog manifest: ${revision}`);
    registry[revision] = manifest;
  }
  const temporary = `${registryPath}.${process.pid}.tmp`;
  await writeFile(temporary, JSON.stringify(registry));
  await rename(temporary, registryPath);
  const validate = event => {
    const manifest = registry[event?.catalogRevision];
    return manifest ? validateFeedbackEvent(event, new Map(Object.entries(manifest)), event.catalogRevision) : 'Ревизия каталога не поддерживается';
  };
  const events = new Map();
  let corruptedLines = 0;
  let historicalLines = 0;
  for (const line of source.split("\n")) {
    if (!line.trim()) continue;
    try {
      const stored = JSON.parse(line);
      const error = validate(stored);
      if (typeof stored.recordedAt !== 'string') corruptedLines += 1;
      else if (!error) { events.set(stored.eventId, stored); if (stored.catalogRevision !== catalogRevision) historicalLines += 1; }
      else if (stored.catalogRevision !== catalogRevision && !validateFeedbackEvent(stored, new Map([[stored.questionId, stored.assignedDifficulty]]), stored.catalogRevision)) { historicalLines += 1; events.set(stored.eventId, stored); }
      else corruptedLines += 1;
    } catch { corruptedLines += 1; }
  }
  let needsLeadingNewline = source.length > 0 && !source.endsWith("\n");
  let queue = Promise.resolve();

  async function append(event) {
    const existing = event && events.get(event.eventId);
    if (existing) {
      return canonicalEvent(existing) === canonicalEvent(event)
        ? { status: 'duplicate' }
        : { status: 'conflict', error: 'eventId уже записан с другим содержимым' };
    }
    const validationError = validate(event);
    if (validationError) return { status: 'invalid', error: validationError };
    const stored = { ...event, recordedAt: new Date().toISOString() };
    const job = queue.then(async () => {
      const afterWait = events.get(event.eventId);
      if (afterWait) {
        return canonicalEvent(afterWait) === canonicalEvent(event)
          ? { status: "duplicate" }
          : { status: "conflict", error: "eventId уже записан с другим содержимым" };
      }
      const handle = await open(filePath, "a");
      try {
        await handle.write(`${needsLeadingNewline ? "\n" : ""}${JSON.stringify(stored)}\n`);
        await handle.sync();
        needsLeadingNewline = false;
      } finally {
        await handle.close();
      }
      events.set(event.eventId, stored);
      return { status: "created" };
    });
    queue = job.then(() => undefined, () => undefined);
    return job;
  }

  function summary() {
    const byQuestion = {};
    const byAssignedDifficulty = Object.fromEntries(LEVELS.map((level) => [level, emptyAggregate()]));
    const v2ByQuestion = {};
    const v2ByAssignedDifficulty = Object.fromEntries(LEVELS.map((level) => [level, emptyV2Aggregate()]));
    let v2Events = 0;
    const v3ByQuestion = {}; const v3ByAssignedDifficulty = Object.fromEntries(LEVELS.map((level) => [level, { total: 0, complaints: 0, noComplaints: 0, reasons: {} }])); let v3Events = 0;
    for (const event of events.values()) {
      if (event.catalogRevision !== catalogRevision) continue;
      if (event.schemaVersion === 2) {
        v2Events += 1;
        v2ByQuestion[event.questionId] ??= emptyV2Aggregate();
        for (const response of event.responses) { addV2(v2ByQuestion[event.questionId], response); addV2(v2ByAssignedDifficulty[event.assignedDifficulty], response); }
        continue;
      }
      if (event.schemaVersion === 3) { v3Events += 1; const add = (target) => { target.total += 1; if (event.hasComplaint) { target.complaints += 1; for (const reason of event.complaintReasons) target.reasons[reason] = (target.reasons[reason] ?? 0) + 1; } else target.noComplaints += 1; }; v3ByQuestion[event.questionId] ??= { total: 0, complaints: 0, noComplaints: 0, reasons: {} }; add(v3ByQuestion[event.questionId]); add(v3ByAssignedDifficulty[event.assignedDifficulty]); continue; }
      byQuestion[event.questionId] ??= emptyAggregate();
      addToAggregate(byQuestion[event.questionId], event);
      addToAggregate(byAssignedDifficulty[event.assignedDifficulty], event);
    }
    return {
      schemaVersion: 1,
      total: [...events.values()].filter(event => event.catalogRevision === catalogRevision).length,
      corruptedLines,
      historicalLines,
      byQuestion: Object.fromEntries(Object.entries(byQuestion).map(([id, value]) => [id, withRates(value)])),
      byAssignedDifficulty: Object.fromEntries(Object.entries(byAssignedDifficulty).map(([id, value]) => [id, withRates(value)]))
      , v2: { events: v2Events, byQuestion: v2ByQuestion, byAssignedDifficulty: v2ByAssignedDifficulty }, v3: { events: v3Events, byQuestion: v3ByQuestion, byAssignedDifficulty: v3ByAssignedDifficulty }
    };
  }

  // Fail fast when the configured path is not writable.
  const probe = await open(filePath, "a");
  await probe.close();
  await stat(filePath);
  return { append, summary, filePath };
}
