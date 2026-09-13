import { describe, expect, it } from "vitest";
import {
  CatalogValidationError,
  EMPTY_QUESTION_HISTORY,
  TOPIC_DEFINITIONS,
  chooseTopicCandidates,
  drawQuestion,
  migrateQuestionHistory,
  seedRandom,
  validateCatalog,
  validateTopicPack,
  type Difficulty,
  type QuestionHistory,
  type ReviewEntry,
  type TopicPack
} from "../../src/content";

const difficulties: readonly Difficulty[] = ["easy", "medium", "hard"];

function makeTopic(index: number): TopicPack {
  const id = `topic-${index}`;
  return {
    id,
    title: `Тема ${index}`,
    questions: difficulties.flatMap((difficulty) =>
      Array.from({ length: difficulty === "hard" ? 20 : 40 }, (_, questionIndex) => ({
        id: `${id}-${difficulty}-${questionIndex}`,
        difficulty,
        prompt: `Какой ответ верен для вопроса ${questionIndex}?`,
        answers: [
          { text: "Первый", note: "Первый тестовый вариант с самостоятельной краткой справкой." },
          { text: "Второй", note: "Второй тестовый вариант с самостоятельной краткой справкой." },
          { text: "Третий", note: "Третий тестовый вариант с самостоятельной краткой справкой." },
          { text: "Четвёртый", note: "Четвёртый тестовый вариант с самостоятельной краткой справкой." }
        ] as const,
        correctIndex: (questionIndex % 4) as 0 | 1 | 2 | 3,
        explanation: "Первый ответ является правильным по условию. Это пояснение даёт краткую проверяемую справку.",
        source: {
          title: "Проверяемый источник",
          url: "https://example.com/reference",
          verifiedAt: "2026-09-01"
        }
      }))
    )
  };
}

describe("content validation", () => {
  it("accepts the exact manifest catalog", () => {
    const catalog = {
      revision: "test-r1",
      topics: TOPIC_DEFINITIONS.map(([id, title], index) => {
        const topic = makeTopic(index);
        return {
          ...topic,
          id,
          title,
          questions: topic.questions.map((question) => ({
          ...question,
            id: question.id.replace(`topic-${index}`, id),
            prompt: `${question.prompt} Тема ${index} ${question.difficulty}`
          }))
        };
      })
    };
    expect(validateCatalog(catalog)).toBe(catalog);
    const reviews: readonly ReviewEntry[] = catalog.topics.map((topic) => ({
      topicId: topic.id,
      author: "author",
      reviewer: "independent-reviewer",
      status: "approved",
      contentSha256: "a".repeat(64),
      reviewedAt: "2026-09-01",
      checkedQuestions: 100,
      criticalFindingsOpen: 0,
      evidence: {
        questionIdsSha256: "b".repeat(64),
        checks: {
          factualCorrectness: 100,
          correctIndex: 100,
          difficulty: 100,
          distractors: 100,
          answerNotes: 100,
          grammar: 100,
          explanation: 100,
          sourceRelevance: 100,
          duplicates: 100
        },
        reviewedPackageIds: [`${topic.id}-batch-01`],
        resolvedFindings: []
      }
    }));
    expect(validateCatalog(catalog, reviews)).toBe(catalog);
    const incomplete = reviews.map((review, index) =>
      index === 0 ? { ...review, checkedQuestions: 99 } : review
    ) as unknown as readonly ReviewEntry[];
    expect(() => validateCatalog(catalog, incomplete)).toThrow(/review не завершено/);
    const unsupportedApproval = reviews.map((review, index) =>
      index === 0
        ? {
            ...review,
            evidence: {
              ...review.evidence,
              checks: { ...review.evidence.checks, sourceRelevance: 99 }
            }
          }
        : review
    ) as unknown as readonly ReviewEntry[];
    expect(() => validateCatalog(catalog, unsupportedApproval)).toThrow(/review не завершено/);
  });

  it("reports a path for invalid answers and quotas", () => {
    const topic = makeTopic(0);
    const broken = {
      ...topic,
      questions: topic.questions.slice(0, 1).map((question) => ({
        ...question,
        answers: [
          { text: "Один", note: "Первая самостоятельная тестовая справка для варианта." },
          { text: "Один", note: "Вторая самостоятельная тестовая справка для варианта." },
          { text: "Три", note: "Третья самостоятельная тестовая справка для варианта." },
          { text: "Четыре", note: "Четвёртая самостоятельная тестовая справка для варианта." }
        ] as const
      }))
    };
    const issues = validateTopicPack(broken);
    expect(issues.some((issue) => issue.includes("ожидался допустимый размер"))).toBe(true);
    expect(issues.some((issue) => issue.includes("ответы должны различаться"))).toBe(true);
    expect(() => validateCatalog({ revision: "x", topics: [broken] })).toThrow(
      CatalogValidationError
    );
  });

  it("rejects duplicate prompt text across different topics", () => {
    const topics = TOPIC_DEFINITIONS.map(([id, title], index) => {
      const topic = makeTopic(index);
      return {
        ...topic,
        id,
        title,
        questions: topic.questions.map((question) => ({
          ...question,
          id: question.id.replace(`topic-${index}`, id),
          prompt: `${question.prompt} Тема ${index}`
        }))
      };
    });
    topics[1].questions[0] = {
      ...topics[1].questions[0],
      prompt: topics[0].questions[0].prompt
    };
    expect(() => validateCatalog({ revision: "duplicate-prompt", topics })).toThrow(
      /глобальный повтор текста вопроса/
    );
  });
});

describe("question shuffle bags", () => {
  it("moves compact history with a question when its difficulty changes", () => {
    const topic = makeTopic(0);
    const movedId = topic.questions.find((question) => question.difficulty === "easy")!.id;
    const migratedTopic = {
      ...topic,
      questions: topic.questions.map((question) =>
        question.id === movedId ? { ...question, difficulty: "medium" as const } : question
      )
    };
    const history: QuestionHistory = {
      version: 1,
      serial: 7,
      bags: {
        "topic-0:easy": {
          cycle: 0,
          remaining: [],
          previousOrder: [movedId],
          lastShownId: movedId,
          shownCount: { [movedId]: 2 },
          lastShownSerial: { [movedId]: 7 }
        }
      }
    };
    const migrated = migrateQuestionHistory([migratedTopic], history);
    expect(migrated.bags["topic-0:medium"]).toMatchObject({
      remaining: [],
      previousOrder: [],
      lastShownId: movedId,
      shownCount: { [movedId]: 2 }
    });
    expect(migrated.bags["topic-0:easy"]).toBeUndefined();
  });

  it("draws a complete unique cycle and changes the next cycle boundary", () => {
    const topic = makeTopic(0);
    let history: QuestionHistory = EMPTY_QUESTION_HISTORY;
    let random = seedRandom("match-a");
    const firstCycle: string[] = [];
    for (let index = 0; index < 20; index += 1) {
      const draw = drawQuestion(topic, "easy", history, random);
      firstCycle.push(draw.questionId);
      history = draw.history;
      random = draw.random;
    }
    expect(new Set(firstCycle).size).toBe(20);
    const next = drawQuestion(topic, "easy", history, random);
    expect(next.questionId).not.toBe(firstCycle.at(-1));
    const nextOrder = next.history.bags["topic-0:easy"].previousOrder;
    expect(nextOrder).not.toEqual(firstCycle);
  });

  it("keeps excluded questions in the remaining bag", () => {
    const topic = makeTopic(0);
    const first = drawQuestion(topic, "easy", EMPTY_QUESTION_HISTORY, seedRandom("match-b"));
    const remainingBefore = first.history.bags["topic-0:easy"].remaining;
    const excluded = new Set([remainingBefore[0]]);
    const second = drawQuestion(topic, "easy", first.history, first.random, excluded);
    expect(second.questionId).not.toBe(remainingBefore[0]);
    expect(second.history.bags["topic-0:easy"].remaining).toContain(remainingBefore[0]);
  });
});

describe("topic candidates", () => {
  const topics = Array.from({ length: 8 }, (_, index) => makeTopic(index));
  const domainForTopic = (topicId: string) => {
    const index = Number(topicId.replace("topic-", ""));
    return ["history", "history", "science", "culture", "sport", "geography", "technology", "nature"][index] ?? "other";
  };

  it("is reproducible for the same seed and avoids a fixed order for another seed", () => {
    const match = { selected: ["topic-7"], shownCounts: { "topic-0": 2 } };
    const first = chooseTopicCandidates(topics, 3, match, seedRandom("same"));
    const repeated = chooseTopicCandidates(topics, 3, match, seedRandom("same"));
    const different = chooseTopicCandidates(topics, 3, match, seedRandom("different"));
    expect(repeated.topicIds).toEqual(first.topicIds);
    expect(different.topicIds).not.toEqual(first.topicIds);
    expect(first.topicIds).not.toContain("topic-7");
    expect(first.topicIds).not.toContain("topic-0");
  });

  it("maximizes distinct domains for normal, bonus, and final topic sets", () => {
    for (const count of [3, 4, 5]) {
      const selection = chooseTopicCandidates(topics, count, { selected: [], shownCounts: {} }, seedRandom(`domains-${count}`), domainForTopic);
      expect(new Set(selection.topicIds.map(domainForTopic)).size).toBe(count);
    }
  });

  it("uses the minimum necessary domain repeat and stays reproducible", () => {
    const limitedTopics = topics.slice(0, 4);
    const limitedDomain = (topicId: string) => topicId === "topic-0" || topicId === "topic-1" ? "history" : "science";
    const input = { selected: [], shownCounts: {} };
    const first = chooseTopicCandidates(limitedTopics, 3, input, seedRandom("domain-fallback"), limitedDomain);
    const repeated = chooseTopicCandidates(limitedTopics, 3, input, seedRandom("domain-fallback"), limitedDomain);
    expect(new Set(first.topicIds).size).toBe(3);
    expect(new Set(first.topicIds.map(limitedDomain))).toEqual(new Set(["history", "science"]));
    expect(repeated).toEqual(first);
  });
});
