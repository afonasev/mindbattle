import { describe, expect, it } from "vitest";
import {
  QUOTA_BY_TARGET_SIZE,
  EMPTY_QUESTION_HISTORY,
  TaxonomyValidationError,
  catalog,
  drawQuestion,
  migrateQuestionHistory,
  quotaForTopicSize,
  seedRandom,
  validateTaxonomyManifest,
  validateTopicPack,
  type Difficulty,
  type TaxonomyManifest,
  type TopicPack,
  type TopicTargetSize
} from "../../src/content";
import productionManifest from "../../src/content/taxonomy-manifest.json";
import expansionLedger from "../../src/content/expansion-ledger.json";

const difficulties: readonly Difficulty[] = ["easy", "medium", "hard"];

function manifest(size: TopicTargetSize = 100): TaxonomyManifest {
  return {
    revision: "taxonomy-test-r1",
    topics: Array.from({ length: 110 }, (_, index) => ({
      id: `topic-${index}`,
      title: `Тема ${index}`,
      scope: `Область темы ${index}`,
      antiOverlap: `Не пересекается с соседними темами ${index}`,
      sourceStrategy: `Авторитетные источники для темы ${index}`,
      sourceInventory: ["https://example.com/reference-a", "https://example.com/reference-b"],
      capacityEvidence: { independentFacts: size, easyCandidates: Math.max(40, QUOTA_BY_TARGET_SIZE[size].easy) },
      targetSize: size,
      quota: QUOTA_BY_TARGET_SIZE[size]
    }))
  };
}

function pack(index: number, size: TopicTargetSize): TopicPack {
  const id = `topic-${index}`;
  const quota = QUOTA_BY_TARGET_SIZE[size];
  return {
    id,
    title: `Тема ${index}`,
    questions: difficulties.flatMap((difficulty) =>
      Array.from({ length: quota[difficulty] }, (_, questionIndex) => ({
        id: `${id}-${difficulty}-${questionIndex}`,
        difficulty,
        prompt: `Какой ответ верен: ${index}/${difficulty}/${questionIndex}?`,
        answers: [
          { text: "Первый", note: "Первый — правильный тестовый вариант." },
          { text: "Второй", note: "Второй — неправильный тестовый вариант." },
          { text: "Третий", note: "Третий — неправильный тестовый вариант." },
          { text: "Четвёртый", note: "Четвёртый — неправильный тестовый вариант." }
        ] as const,
        correctIndex: (questionIndex % 4) as 0 | 1 | 2 | 3,
        explanation: "Первый ответ верен по условию. Это проверяемая тестовая справка.",
        source: {
          title: "Проверяемый источник",
          url: "https://example.com/reference",
          verifiedAt: "2026-09-02"
        }
      }))
    )
  };
}

describe("taxonomy manifest", () => {
  it("keeps the production taxonomy at exactly 110 independently viable topics", () => {
    expect(validateTaxonomyManifest(productionManifest as TaxonomyManifest)).toBe(productionManifest);
    expect(productionManifest.topics.slice(0, 30).map(({ id }) => id)).toEqual([
      "history-russia", "world-history", "geography-russia", "world-geography", "russian-literature",
      "world-literature", "russian-language", "soviet-russian-cinema", "world-cinema", "tv-series",
      "russian-music", "world-pop-music", "classical-music", "russian-culture", "visual-art",
      "architecture", "physics", "chemistry", "biology", "human-medicine", "astronomy-space",
      "math-logic", "inventions-technology", "computers-internet", "economics-money",
      "mythology-religions", "world-cuisine", "sports", "modern-video-games", "video-game-history"
    ]);
  });

  it("assigns all 9,500 base-expansion questions in independent 25-question packages", () => {
    expect(expansionLedger.totals).toEqual({
      packages: 380,
      questions: 9500,
      existingTopicExtensionPackages: 60,
      newTopicBasePackages: 320
    });
    expect(expansionLedger.packages).toHaveLength(380);
    expect(expansionLedger.packages.every(({ questionCount, author, reviewer }) =>
      questionCount === 25 && author !== reviewer
    )).toBe(true);
    expect(expansionLedger.packages.every(({ quota, correctIndexQuota }) =>
      difficulties.every((difficulty) =>
        correctIndexQuota[difficulty].length === 4 &&
        correctIndexQuota[difficulty].reduce((sum, count) => sum + count, 0) === quota[difficulty]
      )
    )).toBe(true);
    for (const topic of productionManifest.topics) {
      const assigned = expansionLedger.packages.filter(({ topicId }) => topicId === topic.id);
      expect(new Set(assigned.map(({ author }) => author)).size).toBe(1);
      expect(new Set(assigned.map(({ reviewer }) => reviewer)).size).toBe(1);
    }
    for (const topic of productionManifest.topics.slice(0, 30)) {
      const assigned = expansionLedger.packages.filter(({ topicId }) => topicId === topic.id);
      const current = catalog.topics.find(({ id }) => id === topic.id)!;
      for (const difficulty of difficulties) {
        const currentCount = current.questions.filter((question) => question.difficulty === difficulty).length;
        const assignedCount = assigned.reduce((sum, { quota }) => sum + quota[difficulty], 0);
        expect(
          current.questions.length === topic.targetSize ? currentCount : currentCount + assignedCount
        ).toBe(topic.quota[difficulty]);
        const targetPerPosition = difficulty === "hard" ? 5 : 10;
        for (const position of [0, 1, 2, 3]) {
          const currentAtPosition = current.questions.filter((question) =>
            question.difficulty === difficulty && question.correctIndex === position
          ).length;
          const assignedAtPosition = assigned.reduce((sum, { correctIndexQuota }) =>
            sum + correctIndexQuota[difficulty][position], 0
          );
          expect(
            current.questions.length === topic.targetSize
              ? currentAtPosition
              : currentAtPosition + assignedAtPosition
          ).toBe(targetPerPosition);
        }
      }
    }
    for (const topic of productionManifest.topics.slice(30)) {
      const assigned = expansionLedger.packages.filter(({ topicId }) => topicId === topic.id);
      expect(assigned).toHaveLength(4);
      expect(assigned.reduce((sum, { quota }) => sum + quota.easy, 0)).toBe(40);
      expect(assigned.reduce((sum, { quota }) => sum + quota.medium, 0)).toBe(40);
      expect(assigned.reduce((sum, { quota }) => sum + quota.hard, 0)).toBe(20);
      for (const difficulty of difficulties) {
        const targetPerPosition = difficulty === "hard" ? 5 : 10;
        for (const position of [0, 1, 2, 3]) {
          expect(assigned.reduce((sum, { correctIndexQuota }) =>
            sum + correctIndexQuota[difficulty][position], 0
          )).toBe(targetPerPosition);
        }
      }
    }
  });
  it("accepts 100 entries with the exact 100/200/300 profiles", () => {
    for (const size of [100, 200, 300] as const) {
      expect(quotaForTopicSize(size)).toEqual(QUOTA_BY_TARGET_SIZE[size]);
      expect(validateTaxonomyManifest(manifest(size))).toEqual(manifest(size));
      expect(validateTopicPack(pack(0, size))).toEqual([]);
    }
  });

  it("rejects unknown sizes, bad quotas and duplicate ids", () => {
    const base = manifest();
    const broken = {
      ...base,
      topics: base.topics.map((entry, index) =>
        index === 0
          ? { ...entry, targetSize: 150 as TopicTargetSize, quota: { easy: 50, medium: 50, hard: 50 } }
          : index === 1
            ? { ...entry, id: base.topics[2].id }
            : entry
      )
    };
    expect(() => validateTaxonomyManifest(broken)).toThrow(TaxonomyValidationError);
    expect(() => validateTaxonomyManifest(broken)).toThrow(/недопустимый targetSize|повтор topic id/);
  });

  it("rejects packs that do not match taxonomy", () => {
    const base = manifest();
    const packs = base.topics.map((_, index) => pack(index, 100));
    packs[0] = { ...packs[0], title: "Другое название" };
    expect(() => validateTaxonomyManifest(base, packs)).toThrow(/название pack не совпадает/);
  });

  it("draws complete deterministic bags for every supported size", () => {
    for (const size of [100, 200, 300] as const) {
      const topic = pack(0, size);
      for (const difficulty of difficulties) {
        let history = EMPTY_QUESTION_HISTORY;
        let random = seedRandom(`taxonomy-${size}-${difficulty}`);
        const ids: string[] = [];
        for (let index = 0; index < QUOTA_BY_TARGET_SIZE[size][difficulty]; index += 1) {
          const draw = drawQuestion(topic, difficulty, history, random);
          ids.push(draw.questionId);
          history = draw.history;
          random = draw.random;
        }
        expect(new Set(ids).size).toBe(QUOTA_BY_TARGET_SIZE[size][difficulty]);
        const next = drawQuestion(topic, difficulty, history, random);
        expect(next.questionId).not.toBe(ids.at(-1));
      }
    }
  });

  it("migrates compact history by stable question id across levels and bag sizes", () => {
    const expanded = pack(0, 100);
    const movedId = expanded.questions.find(({ difficulty }) => difficulty === "medium")!.id;
    const removedId = "topic-0-removed";
    const history = {
      version: 1 as const,
      serial: 17,
      bags: {
        "topic-0:easy": {
          cycle: 2,
          remaining: [movedId, removedId],
          previousOrder: [removedId, movedId],
          lastShownId: movedId,
          shownCount: { [movedId]: 3, [removedId]: 4 },
          lastShownSerial: { [movedId]: 16, [removedId]: 17 }
        }
      }
    };
    const migrated = migrateQuestionHistory([expanded], history);
    expect(migrated.serial).toBe(17);
    expect(migrated.bags["topic-0:medium"]).toMatchObject({
      cycle: 0,
      remaining: [],
      previousOrder: [],
      lastShownId: movedId,
      shownCount: { [movedId]: 3 },
      lastShownSerial: { [movedId]: 16 }
    });
    expect(JSON.stringify(migrated)).not.toContain(removedId);
    expect(migrated.bags["topic-0:easy"]).toBeUndefined();
  });
});
