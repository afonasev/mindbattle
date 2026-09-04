import type { Difficulty, Question, TopicPack } from "./types";

export type AuditScore = 0 | 1 | 2;
export type AuditStatus = "pending" | "final";

export interface QuestionAuditEntry {
  readonly questionId: string;
  readonly topicId: string;
  readonly previousDifficulty: Difficulty;
  readonly difficulty: Difficulty;
  readonly status: AuditStatus;
  readonly rubric: {
    readonly audienceBreadth: AuditScore;
    readonly topicSpecialization: AuditScore;
    readonly inferencePotential: AuditScore;
    readonly distractorQuality: AuditScore;
  };
  readonly reasons: readonly string[];
  readonly checks: {
    readonly grammar: boolean;
    readonly distractors: boolean;
    readonly answerNotes: boolean;
    readonly source: boolean;
  };
  readonly changes: readonly string[];
}

export interface DifficultyFeedbackInput {
  readonly eventId: string;
  readonly questionId: string;
  readonly assignedDifficulty: Difficulty;
  readonly perceivedDifficulty: Difficulty;
}

export interface DifficultySignal {
  readonly questionId: string;
  readonly assignedDifficulty: Difficulty;
  readonly total: number;
  readonly perceived: Readonly<Record<Difficulty, number>>;
  readonly median: Difficulty;
  readonly strength: "weak" | "indicative" | "sustained";
  readonly suggestedDifficulty: Difficulty | null;
}

export interface ComplaintFeedbackInput {
  readonly eventId: string;
  readonly questionId: string;
  readonly assignedDifficulty: Difficulty;
  readonly hasComplaint: boolean;
  readonly complaintReasons: readonly string[];
}

export function analyzeComplaintFeedback(events: readonly ComplaintFeedbackInput[], knownQuestionIds: ReadonlySet<string>) {
  const seen = new Set<string>(); const duplicateEventIds = new Set<string>(); const unknownQuestionIds = new Set<string>();
  const grouped = new Map<string, ComplaintFeedbackInput[]>();
  for (const event of events) { if (seen.has(event.eventId)) { duplicateEventIds.add(event.eventId); continue; } seen.add(event.eventId); if (!knownQuestionIds.has(event.questionId)) { unknownQuestionIds.add(event.questionId); continue; } grouped.set(event.questionId, [...(grouped.get(event.questionId) ?? []), event]); }
  const signals = [...grouped.entries()].map(([questionId, rows]) => {
    const reasons: Record<string, number> = {}; const complaints = rows.filter(({ hasComplaint }) => hasComplaint);
    for (const row of complaints) for (const reason of row.complaintReasons) reasons[reason] = (reasons[reason] ?? 0) + 1;
    return { questionId, assignedDifficulty: rows[0].assignedDifficulty, total: rows.length, complaints: complaints.length, noComplaints: rows.length - complaints.length, complaintRate: complaints.length / rows.length, reasons };
  }).sort((left, right) => right.total - left.total || left.questionId.localeCompare(right.questionId));
  return { signals, duplicateEventIds: [...duplicateEventIds].sort(), unknownQuestionIds: [...unknownQuestionIds].sort(), correctnessRateAvailable: false as const };
}

export interface DuplicateCandidate {
  readonly leftQuestionId: string;
  readonly rightQuestionId: string;
  readonly similarity: number;
  readonly kind: "exact" | "near";
}

const order: Readonly<Record<Difficulty, number>> = { easy: 0, medium: 1, hard: 2 };
const difficulties: readonly Difficulty[] = ["easy", "medium", "hard"];

export function validateAuditCoverage(
  entries: readonly QuestionAuditEntry[],
  expectedQuestionIds: readonly string[],
  requireFinal = true
): readonly string[] {
  const issues: string[] = [];
  const expected = new Set(expectedQuestionIds);
  const seen = new Set<string>();
  for (const entry of entries) {
    if (seen.has(entry.questionId)) issues.push(`${entry.questionId}: повтор audit entry`);
    seen.add(entry.questionId);
    if (!expected.has(entry.questionId)) issues.push(`${entry.questionId}: отсутствует в baseline`);
    if (requireFinal && entry.status !== "final") issues.push(`${entry.questionId}: audit не завершён`);
    if (entry.reasons.length === 0) issues.push(`${entry.questionId}: отсутствует причина решения`);
    if (requireFinal && Object.values(entry.checks).some((value) => !value)) {
      issues.push(`${entry.questionId}: checklist не завершён`);
    }
  }
  for (const id of expected) if (!seen.has(id)) issues.push(`${id}: отсутствует audit entry`);
  return issues;
}

export function lintQuestionGrammar(question: Question): readonly string[] {
  const warnings: string[] = [];
  const at = `${question.id}:`;
  if (/\s{2,}/u.test(question.prompt)) warnings.push(`${at} двойной пробел в вопросе`);
  if (/(?:^|[^\p{L}])кого(?:$|[^\p{L}])[^?]{0,50}(?:^|[^\p{L}])является(?:$|[^\p{L}])/iu.test(question.prompt)) {
    warnings.push(`${at} возможно неверное управление «кого … является»`);
  }
  if (/(?:^|[^\p{L}])какой(?:$|[^\p{L}])[^?]{0,50}(?:^|[^\p{L}])являются(?:$|[^\p{L}])/iu.test(question.prompt)) {
    warnings.push(`${at} возможно несогласованы единственное и множественное число`);
  }
  if (/(?:^|[^\p{L}])какие(?:$|[^\p{L}])[^?]{0,50}(?:^|[^\p{L}])является(?:$|[^\p{L}])/iu.test(question.prompt)) {
    warnings.push(`${at} возможно несогласованы множественное и единственное число`);
  }
  if (/^Что означает следующее описание:/u.test(question.prompt)) {
    warnings.push(`${at} машинный шаблон вопроса требует естественной формулировки`);
  }
  const texts = question.answers.map((answer) =>
    typeof answer === "string" ? answer.trim() : answer.text.trim()
  );
  const punctuation = texts.map((text) => /[.!?]$/u.test(text));
  if (punctuation.some(Boolean) && !punctuation.every(Boolean)) {
    warnings.push(`${at} варианты неодинаково используют конечную пунктуацию`);
  }
  const lowercase = texts.map((text) => /^\p{Ll}/u.test(text));
  if (lowercase.some(Boolean) && !lowercase.every(Boolean)) {
    warnings.push(`${at} варианты неодинаково начинаются с прописной/строчной буквы`);
  }
  return warnings;
}

export function analyzeDifficultyFeedback(
  events: readonly DifficultyFeedbackInput[],
  knownQuestionIds: ReadonlySet<string>
): {
  readonly signals: readonly DifficultySignal[];
  readonly duplicateEventIds: readonly string[];
  readonly unknownQuestionIds: readonly string[];
  readonly correctnessRateAvailable: false;
} {
  const unique = new Map<string, DifficultyFeedbackInput>();
  const duplicateEventIds = new Set<string>();
  const unknownQuestionIds = new Set<string>();
  for (const event of events) {
    if (unique.has(event.eventId)) {
      duplicateEventIds.add(event.eventId);
      continue;
    }
    unique.set(event.eventId, event);
    if (!knownQuestionIds.has(event.questionId)) unknownQuestionIds.add(event.questionId);
  }
  const grouped = new Map<string, DifficultyFeedbackInput[]>();
  for (const event of unique.values()) {
    if (!knownQuestionIds.has(event.questionId)) continue;
    grouped.set(event.questionId, [...(grouped.get(event.questionId) ?? []), event]);
  }
  const signals = [...grouped.entries()].map(([questionId, rows]): DifficultySignal => {
    const perceived = { easy: 0, medium: 0, hard: 0 };
    for (const row of rows) perceived[row.perceivedDifficulty] += 1;
    const values = rows.map((row) => row.perceivedDifficulty).sort((a, b) => order[a] - order[b]);
    const median = values[Math.floor((values.length - 1) / 2)];
    const [plurality, pluralityCount] = difficulties
      .map((difficulty) => [difficulty, perceived[difficulty]] as const)
      .sort((left, right) => right[1] - left[1] || order[left[0]] - order[right[0]])[0];
    const sustained = rows.length >= 5 && pluralityCount / rows.length >= 2 / 3;
    return {
      questionId,
      assignedDifficulty: rows[0].assignedDifficulty,
      total: rows.length,
      perceived,
      median,
      strength: rows.length < 3 ? "weak" : sustained ? "sustained" : "indicative",
      suggestedDifficulty: sustained && plurality !== rows[0].assignedDifficulty ? plurality : null
    };
  });
  signals.sort((left, right) => right.total - left.total || left.questionId.localeCompare(right.questionId));
  return {
    signals,
    duplicateEventIds: [...duplicateEventIds].sort(),
    unknownQuestionIds: [...unknownQuestionIds].sort(),
    correctnessRateAvailable: false
  };
}

export function normalizeQuestionPrompt(prompt: string): string {
  return prompt
    .toLocaleLowerCase("ru")
    .replace(/ё/gu, "е")
    .replace(/[^a-zа-я0-9]+/gu, " ")
    .trim();
}

function jaccard(left: ReadonlySet<string>, right: ReadonlySet<string>): number {
  const intersection = [...left].filter((token) => right.has(token)).length;
  const union = new Set([...left, ...right]).size;
  return union === 0 ? 0 : intersection / union;
}

export function findSemanticDuplicateCandidates(
  topics: readonly TopicPack[],
  threshold = 0.82
): readonly DuplicateCandidate[] {
  const questions = topics.flatMap((topic) => topic.questions);
  const normalized = questions.map((question) => ({
    id: question.id,
    prompt: normalizeQuestionPrompt(question.prompt),
    tokens: new Set(normalizeQuestionPrompt(question.prompt).split(" ").filter(Boolean))
  }));
  const candidates: DuplicateCandidate[] = [];
  for (let leftIndex = 0; leftIndex < normalized.length; leftIndex += 1) {
    for (let rightIndex = leftIndex + 1; rightIndex < normalized.length; rightIndex += 1) {
      const left = normalized[leftIndex];
      const right = normalized[rightIndex];
      if (left.prompt === right.prompt) {
        candidates.push({
          leftQuestionId: left.id,
          rightQuestionId: right.id,
          similarity: 1,
          kind: "exact"
        });
        continue;
      }
      if (Math.min(left.tokens.size, right.tokens.size) < 4) continue;
      const similarity = jaccard(left.tokens, right.tokens);
      if (similarity >= threshold) {
        candidates.push({
          leftQuestionId: left.id,
          rightQuestionId: right.id,
          similarity,
          kind: "near"
        });
      }
    }
  }
  return candidates.sort(
    (left, right) =>
      right.similarity - left.similarity ||
      left.leftQuestionId.localeCompare(right.leftQuestionId) ||
      left.rightQuestionId.localeCompare(right.rightQuestionId)
  );
}
