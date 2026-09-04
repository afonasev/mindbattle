import { mkdir, open, readFile, stat } from "node:fs/promises";
import { dirname } from "node:path";

const LEVELS = ["easy", "medium", "hard"];
const levelIndex = new Map(LEVELS.map((level, index) => [level, index]));

function isHistoricalFeedbackEvent(value, catalogRevision) {
  return value &&
    typeof value === "object" &&
    !Array.isArray(value) &&
    value.schemaVersion === 1 &&
    typeof value.eventId === "string" && value.eventId.length > 0 &&
    typeof value.matchId === "string" && value.matchId.length > 0 &&
    typeof value.questionId === "string" && value.questionId.length > 0 &&
    typeof value.catalogRevision === "string" &&
    value.catalogRevision.length > 0 &&
    value.catalogRevision !== catalogRevision &&
    LEVELS.includes(value.assignedDifficulty) &&
    LEVELS.includes(value.perceivedDifficulty) &&
    typeof value.recordedAt === "string";
}

function canonicalEvent(event) {
  const base = {
    schemaVersion: event.schemaVersion,
    eventId: event.eventId,
    matchId: event.matchId,
    catalogRevision: event.catalogRevision,
    questionId: event.questionId,
    assignedDifficulty: event.assignedDifficulty,
  };
  return JSON.stringify(event.schemaVersion === 1 ? { ...base, perceivedDifficulty: event.perceivedDifficulty } : { ...base, responses: event.responses });
}

export function validateFeedbackEvent(value, questions, catalogRevision) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return "Ожидался JSON-объект";
  const strings = ["eventId", "matchId", "catalogRevision", "questionId"];
  if (![1, 2].includes(value.schemaVersion) || strings.some((key) => typeof value[key] !== "string" || value[key].length === 0)) {
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

export async function createFeedbackStore({ filePath, questions, catalogRevision }) {
  await mkdir(dirname(filePath), { recursive: true });
  let source = "";
  try { source = await readFile(filePath, "utf8"); } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }
  const events = new Map();
  let corruptedLines = 0;
  let historicalLines = 0;
  for (const line of source.split("\n")) {
    if (!line.trim()) continue;
    try {
      const stored = JSON.parse(line);
      if (isHistoricalFeedbackEvent(stored, catalogRevision)) {
        historicalLines += 1;
        continue;
      }
      const error = validateFeedbackEvent(stored, questions, catalogRevision);
      if (error || typeof stored.recordedAt !== "string") corruptedLines += 1;
      else events.set(stored.eventId, stored);
    } catch { corruptedLines += 1; }
  }
  let needsLeadingNewline = source.length > 0 && !source.endsWith("\n");
  let queue = Promise.resolve();

  async function append(event) {
    const validationError = validateFeedbackEvent(event, questions, catalogRevision);
    if (validationError) return { status: "invalid", error: validationError };
    const existing = events.get(event.eventId);
    if (existing) {
      return canonicalEvent(existing) === canonicalEvent(event)
        ? { status: "duplicate" }
        : { status: "conflict", error: "eventId уже записан с другим содержимым" };
    }
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
    for (const event of events.values()) {
      if (event.schemaVersion === 2) {
        v2Events += 1;
        v2ByQuestion[event.questionId] ??= emptyV2Aggregate();
        for (const response of event.responses) { addV2(v2ByQuestion[event.questionId], response); addV2(v2ByAssignedDifficulty[event.assignedDifficulty], response); }
        continue;
      }
      byQuestion[event.questionId] ??= emptyAggregate();
      addToAggregate(byQuestion[event.questionId], event);
      addToAggregate(byAssignedDifficulty[event.assignedDifficulty], event);
    }
    return {
      schemaVersion: 1,
      total: events.size,
      corruptedLines,
      historicalLines,
      byQuestion: Object.fromEntries(Object.entries(byQuestion).map(([id, value]) => [id, withRates(value)])),
      byAssignedDifficulty: Object.fromEntries(Object.entries(byAssignedDifficulty).map(([id, value]) => [id, withRates(value)]))
      , v2: { events: v2Events, byQuestion: v2ByQuestion, byAssignedDifficulty: v2ByAssignedDifficulty }
    };
  }

  // Fail fast when the configured path is not writable.
  const probe = await open(filePath, "a");
  await probe.close();
  await stat(filePath);
  return { append, summary, filePath };
}
