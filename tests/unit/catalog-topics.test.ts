import { describe, expect, it } from "vitest";
import { catalog, validateCatalog, validateTopicPack } from "../../src/content";

describe("integrated topic packages", () => {
  it("keeps every present package valid and globally unique", () => {
    const ids = new Set<string>();
    for (const topic of catalog.topics) {
      expect(validateTopicPack(topic), topic.id).toEqual([]);
      for (const question of topic.questions) {
        expect(ids.has(question.id), question.id).toBe(false);
        ids.add(question.id);
      }
    }
    expect(ids.size).toBe(catalog.topics.length * 50);
    if (catalog.topics.length === 30) {
      expect(validateCatalog(catalog)).toBe(catalog);
    }
  });
});
