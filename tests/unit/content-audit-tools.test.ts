import { describe, expect, it } from "vitest";
import {
  analyzeDifficultyFeedback,
  analyzeComplaintFeedback,
  findSemanticDuplicateCandidates,
  lintQuestionGrammar,
  validateAuditCoverage,
  type Question,
  type QuestionAuditEntry,
  type TopicPack
} from "../../src/content";

function question(id: string, prompt: string): Question {
  return {
    id,
    difficulty: "easy",
    prompt,
    answers: [
      { text: "Первый", note: "Справка о первом варианте." },
      { text: "Второй", note: "Справка о втором варианте." },
      { text: "Третий", note: "Справка о третьем варианте." },
      { text: "Четвёртый", note: "Справка о четвёртом варианте." }
    ],
    correctIndex: 0,
    explanation: "Первый вариант является правильным. Это тестовая справка.",
    source: { title: "Источник", url: "https://example.com", verifiedAt: "2026-09-02" }
  };
}

function finalAudit(questionId: string): QuestionAuditEntry {
  return {
    questionId,
    topicId: "topic",
    previousDifficulty: "easy",
    difficulty: "easy",
    status: "final",
    rubric: {
      audienceBreadth: 2,
      topicSpecialization: 0,
      inferencePotential: 1,
      distractorQuality: 2
    },
    reasons: ["widely-known"],
    checks: { grammar: true, distractors: true, answerNotes: true, source: true },
    changes: []
  };
}

describe("catalog audit tools", () => {
  it("requires exactly one final checked entry for every baseline id", () => {
    const ids = Array.from({ length: 1500 }, (_, index) => `question-${index}`);
    const entries = ids.map(finalAudit);
    expect(validateAuditCoverage(entries, ids)).toEqual([]);
    expect(validateAuditCoverage([...entries, entries[0]], ids)).toContain(
      "question-0: повтор audit entry"
    );
    expect(validateAuditCoverage(entries.slice(1), ids)).toContain(
      "question-0: отсутствует audit entry"
    );
    expect(validateAuditCoverage([{ ...entries[0], status: "pending" }, ...entries.slice(1)], ids)).toContain(
      "question-0: audit не завершён"
    );
  });

  it("emits grammar warnings without changing question text", () => {
    const source = question("grammar", "Что означает следующее описание: кого из перечисленных является автором  книги?");
    const broken: Question = {
      ...source,
      answers: [
        { text: "Первый.", note: "Справка." },
        { text: "второй", note: "Справка." },
        { text: "Третий", note: "Справка." },
        { text: "Четвёртый", note: "Справка." }
      ]
    };
    expect(lintQuestionGrammar(broken)).toEqual(expect.arrayContaining([
      expect.stringContaining("двойной пробел"),
      expect.stringContaining("кого … является"),
      expect.stringContaining("машинный шаблон"),
      expect.stringContaining("конечную пунктуацию"),
      expect.stringContaining("прописной/строчной")
    ]));
    expect(broken.prompt).toBe(source.prompt);
  });

  it("weights feedback by sample size and never exposes correctness", () => {
    const events = [
      { eventId: "weak", questionId: "q-weak", assignedDifficulty: "medium" as const, perceivedDifficulty: "easy" as const },
      ...Array.from({ length: 3 }, (_, index) => ({
        eventId: `indicative-${index}`,
        questionId: "q-indicative",
        assignedDifficulty: "medium" as const,
        perceivedDifficulty: index < 2 ? "easy" as const : "medium" as const
      })),
      ...Array.from({ length: 6 }, (_, index) => ({
        eventId: `sustained-${index}`,
        questionId: "q-sustained",
        assignedDifficulty: "hard" as const,
        perceivedDifficulty: index < 5 ? "medium" as const : "hard" as const
      })),
      { eventId: "unknown", questionId: "q-unknown", assignedDifficulty: "easy" as const, perceivedDifficulty: "easy" as const },
      { eventId: "weak", questionId: "q-weak", assignedDifficulty: "medium" as const, perceivedDifficulty: "easy" as const }
    ];
    const report = analyzeDifficultyFeedback(events, new Set(["q-weak", "q-indicative", "q-sustained"]));
    expect(report.signals.find(({ questionId }) => questionId === "q-weak")).toMatchObject({
      total: 1,
      strength: "weak",
      suggestedDifficulty: null
    });
    expect(report.signals.find(({ questionId }) => questionId === "q-indicative")).toMatchObject({
      total: 3,
      strength: "indicative",
      suggestedDifficulty: null
    });
    expect(report.signals.find(({ questionId }) => questionId === "q-sustained")).toMatchObject({
      total: 6,
      strength: "sustained",
      suggestedDifficulty: "medium"
    });
    expect(report.duplicateEventIds).toEqual(["weak"]);
    expect(report.unknownQuestionIds).toEqual(["q-unknown"]);
    expect(report.correctnessRateAvailable).toBe(false);
  });

  it("counts v3 complaints against all shown questions without exposing notes", () => {
    const report = analyzeComplaintFeedback([
      { eventId: "no", questionId: "q", assignedDifficulty: "easy", hasComplaint: false, complaintReasons: [] },
      { eventId: "yes", questionId: "q", assignedDifficulty: "easy", hasComplaint: true, complaintReasons: ["too-easy", "unclear-wording"] }
    ], new Set(["q"]));
    expect(report.signals[0]).toMatchObject({ total: 2, complaints: 1, noComplaints: 1, complaintRate: 0.5, reasons: { "too-easy": 1 } });
  });

  it("finds exact and near prompts while leaving distinct facts alone", () => {
    const topic: TopicPack = {
      id: "topic",
      title: "Тема",
      questions: [
        question("q-1", "В каком городе находится Московский Кремль?"),
        question("q-2", "В каком городе расположен Московский Кремль?"),
        question("q-3", "В каком городе находится Московский Кремль?"),
        question("q-4", "Какая планета ближе всего к Солнцу?")
      ]
    };
    const candidates = findSemanticDuplicateCandidates([topic], 0.7);
    expect(candidates).toEqual(expect.arrayContaining([
      expect.objectContaining({ leftQuestionId: "q-1", rightQuestionId: "q-3", kind: "exact" }),
      expect.objectContaining({ leftQuestionId: "q-1", rightQuestionId: "q-2", kind: "near" })
    ]));
    expect(candidates.some(({ leftQuestionId, rightQuestionId }) =>
      leftQuestionId === "q-4" || rightQuestionId === "q-4"
    )).toBe(false);
  });
});
