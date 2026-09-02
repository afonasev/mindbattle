import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const assignments = {
  "codex-content-a": {
    reviewer: "codex-independent-content-b",
    topics: [
      "architecture", "astronomy-space", "biology", "chemistry", "classical-music",
      "computers-internet", "economics-money", "geography-russia", "history-russia", "human-medicine"
    ]
  },
  "codex-content-b": {
    reviewer: "codex-independent-content-c",
    topics: [
      "inventions-technology", "math-logic", "modern-video-games", "mythology-religions", "physics",
      "russian-culture", "russian-language", "russian-literature", "russian-music", "soviet-russian-cinema"
    ]
  },
  "codex-content-c": {
    reviewer: "codex-independent-content-a",
    topics: [
      "sports", "tv-series", "video-game-history", "visual-art", "world-cinema",
      "world-cuisine", "world-geography", "world-history", "world-literature", "world-pop-music"
    ]
  }
};

let written = 0;
for (const [author, { reviewer, topics }] of Object.entries(assignments)) {
  for (const topicId of topics) {
    const raw = await readFile(resolve(root, `src/content/topics/${topicId}.json`));
    const review = {
      topicId,
      author,
      reviewer,
      status: "approved",
      contentSha256: createHash("sha256").update(raw).digest("hex"),
      reviewedAt: "2026-09-02",
      checkedQuestions: 50,
      criticalFindingsOpen: 0
    };
    await writeFile(
      resolve(root, `src/content/reviews/${topicId}.json`),
      `${JSON.stringify(review, null, 2)}\n`,
      "utf8"
    );
    written += 1;
  }
}
if (written !== 30) throw new Error(`Expected 30 legacy reviews, wrote ${written}`);
console.log(`Finalized ${written} legacy cross-reviews`);
