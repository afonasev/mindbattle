import { describe, expect, it } from "vitest";
import {
  CatalogValidationError,
  EMPTY_QUESTION_HISTORY,
  TOPIC_DEFINITIONS,
  chooseTopicCandidates,
  drawQuestion,
  seedRandom,
  validateCatalog,
  validateTopicPack,
  type Difficulty,
  type QuestionHistory,
  type TopicPack
} from "../../src/content";

const difficulties: readonly Difficulty[] = ["easy", "medium", "hard"];

function makeTopic(index: number): TopicPack {
  const id = `topic-${index}`;
  return {
    id,
    title: `Тема ${index}`,
    questions: difficulties.flatMap((difficulty) =>
      Array.from({ length: 10 }, (_, questionIndex) => ({
        id: `${id}-${difficulty}-${questionIndex}`,
        difficulty,
        prompt: `Какой ответ верен для вопроса ${questionIndex}?`,
        answers: ["Первый", "Второй", "Третий", "Четвёртый"] as const,
        correctIndex: 0 as const,
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
  it("accepts the exact 30 × 30 catalog", () => {
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
  });

  it("reports a path for invalid answers and quotas", () => {
    const topic = makeTopic(0);
    const broken = {
      ...topic,
      questions: topic.questions.slice(0, 1).map((question) => ({
        ...question,
        answers: ["Один", "Один", "Три", "Четыре"] as const
      }))
    };
    const issues = validateTopicPack(broken);
    expect(issues.some((issue) => issue.includes("ожидалось 30"))).toBe(true);
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
  it("draws a complete unique cycle and changes the next cycle boundary", () => {
    const topic = makeTopic(0);
    let history: QuestionHistory = EMPTY_QUESTION_HISTORY;
    let random = seedRandom("match-a");
    const firstCycle: string[] = [];
    for (let index = 0; index < 10; index += 1) {
      const draw = drawQuestion(topic, "easy", history, random);
      firstCycle.push(draw.questionId);
      history = draw.history;
      random = draw.random;
    }
    expect(new Set(firstCycle).size).toBe(10);
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
});
