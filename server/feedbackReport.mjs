const REASONS = ["too-easy", "too-hard", "weak-answer-options", "unclear-wording", "suspected-error", "ambiguous-answer", "uninteresting-for-quiz"];

function isV3Event(value) {
  return value && typeof value === "object" && !Array.isArray(value) &&
    value.schemaVersion === 3 &&
    ["eventId", "matchId", "catalogRevision", "questionId", "assignedDifficulty"].every((key) => typeof value[key] === "string" && value[key].length > 0) &&
    ["easy", "medium", "hard"].includes(value.assignedDifficulty) &&
    typeof value.hasComplaint === "boolean" &&
    Array.isArray(value.complaintReasons) &&
    new Set(value.complaintReasons).size === value.complaintReasons.length &&
    value.complaintReasons.every((reason) => REASONS.includes(reason)) &&
    !((value.complaintReasons.includes("too-easy")) && value.complaintReasons.includes("too-hard"));
}

function emptyAggregate() {
  return { total: 0, complaints: 0, noComplaints: 0, complaintRate: 0, reasons: {} };
}

function addEvent(target, event) {
  target.total += 1;
  if (event.hasComplaint) {
    target.complaints += 1;
    for (const reason of event.complaintReasons) target.reasons[reason] = (target.reasons[reason] ?? 0) + 1;
  } else target.noComplaints += 1;
}

function withRate(aggregate) {
  return { ...aggregate, complaintRate: aggregate.total === 0 ? 0 : aggregate.complaints / aggregate.total };
}

/** Produces an aggregate safe to print in an SSH terminal: complaintNote is never returned. */
export function analyzeProductionFeedback(source, { questions, catalogRevision }) {
  const byQuestion = new Map();
  const byDifficulty = new Map(["easy", "medium", "hard"].map((difficulty) => [difficulty, emptyAggregate()]));
  const catalogRevisions = new Map();
  const seenEventIds = new Set();
  const duplicateEventIds = new Set();
  const unknownQuestionIds = new Set();
  let invalidLines = 0;
  let historicalEvents = 0;

  for (const line of source.split("\n")) {
    if (!line.trim()) continue;
    let event;
    try { event = JSON.parse(line); } catch { invalidLines += 1; continue; }
    if (!isV3Event(event)) { invalidLines += 1; continue; }
    catalogRevisions.set(event.catalogRevision, (catalogRevisions.get(event.catalogRevision) ?? 0) + 1);
    if (seenEventIds.has(event.eventId)) { duplicateEventIds.add(event.eventId); continue; }
    seenEventIds.add(event.eventId);
    if (event.catalogRevision !== catalogRevision) { historicalEvents += 1; continue; }
    if (questions && !questions.has(event.questionId)) { unknownQuestionIds.add(event.questionId); continue; }
    const questionAggregate = byQuestion.get(event.questionId) ?? emptyAggregate();
    addEvent(questionAggregate, event);
    byQuestion.set(event.questionId, questionAggregate);
    addEvent(byDifficulty.get(event.assignedDifficulty), event);
  }

  const total = emptyAggregate();
  for (const aggregate of byQuestion.values()) {
    total.total += aggregate.total;
    total.complaints += aggregate.complaints;
    total.noComplaints += aggregate.noComplaints;
    for (const [reason, count] of Object.entries(aggregate.reasons)) total.reasons[reason] = (total.reasons[reason] ?? 0) + count;
  }
  return {
    schemaVersion: 1,
    catalogRevision,
    totals: withRate(total),
    byQuestion: Object.fromEntries([...byQuestion.entries()].sort(([left], [right]) => left.localeCompare(right)).map(([id, aggregate]) => [id, withRate(aggregate)])),
    byAssignedDifficulty: Object.fromEntries([...byDifficulty.entries()].map(([difficulty, aggregate]) => [difficulty, withRate(aggregate)])),
    diagnostics: {
      invalidLines,
      historicalEvents,
      duplicateEventIds: [...duplicateEventIds].sort(),
      unknownQuestionIds: [...unknownQuestionIds].sort(),
      catalogRevisions: Object.fromEntries([...catalogRevisions.entries()].sort(([left], [right]) => left.localeCompare(right)))
    }
  };
}
