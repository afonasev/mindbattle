import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import {
  TOPIC_DEFINITIONS,
  assertFullCatalog,
  contentReviews
} from "../../src/content";
import taxonomyManifest from "../../src/content/taxonomy-manifest.json";

describe("full production question catalog", () => {
  it("contains every approved topic, its target question count and a review of the current bytes", () => {
    const catalog = assertFullCatalog();
    expect(catalog.topics).toHaveLength(taxonomyManifest.topics.length);
    expect(catalog.topics.flatMap(({ questions }) => questions)).toHaveLength(
      taxonomyManifest.topics.reduce((total, topic) => total + topic.targetSize, 0)
    );

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
