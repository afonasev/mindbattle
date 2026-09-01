import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import {
  TOPIC_DEFINITIONS,
  assertFullCatalog,
  contentReviews
} from "../../src/content";

describe("full production question catalog", () => {
  it("contains 30 approved topics, 1500 questions and reviews of the current bytes", () => {
    const catalog = assertFullCatalog();
    expect(catalog.topics).toHaveLength(30);
    expect(catalog.topics.flatMap(({ questions }) => questions)).toHaveLength(1500);

    for (const [topicId] of TOPIC_DEFINITIONS) {
      const path = fileURLToPath(
        new URL(`../../src/content/topics/${topicId}.json`, import.meta.url)
      );
      const digest = createHash("sha256").update(readFileSync(path)).digest("hex");
      const review = contentReviews.find((entry) => entry.topicId === topicId);
      expect(review?.contentSha256, `${topicId}: review должен соответствовать файлу`).toBe(
        digest
      );
    }
  });
});
