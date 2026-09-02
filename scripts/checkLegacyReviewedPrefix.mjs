import { createHash } from "node:crypto";
import { access, readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const baseline = JSON.parse(await readFile(resolve(root, "docs/content-audits/catalog-baseline-2026-09-02.json"), "utf8"));
const reportPath = resolve(root, "docs/content-audits/legacy-reviewed-prefix-2026-09-02.json");
let expected = null;
try {
  await access(reportPath);
  expected = JSON.parse(await readFile(reportPath, "utf8"));
} catch {}

const rows = [];
for (const { id } of baseline.topics) {
  const topic = JSON.parse(await readFile(resolve(root, `src/content/topics/${id}.json`), "utf8"));
  const prefixBytes = `${JSON.stringify({ ...topic, questions: topic.questions.slice(0, 50) }, null, 2)}\n`;
  const actualSha256 = createHash("sha256").update(prefixBytes).digest("hex");
  const expectedSha256 = expected
    ? expected.topics.find(({ topicId }) => topicId === id)?.contentSha256
    : JSON.parse(await readFile(resolve(root, `src/content/reviews/${id}.json`), "utf8")).contentSha256;
  rows.push({ topicId: id, contentSha256: actualSha256, matchesReviewedPrefix: actualSha256 === expectedSha256 });
}

const failures = rows.filter(({ matchesReviewedPrefix }) => !matchesReviewedPrefix);
if (failures.length > 0) {
  throw new Error(`Legacy reviewed prefix changed: ${failures.map(({ topicId }) => topicId).join(", ")}`);
}
if (!expected) {
  await writeFile(reportPath, `${JSON.stringify({
    schemaVersion: 1,
    capturedOn: "2026-09-02",
    policy: "SHA-256 каждого независимо одобренного 50-вопросного пакета до добавления новых вопросов; authoring расширения не может менять этот prefix.",
    topics: rows.map(({ topicId, contentSha256 }) => ({ topicId, contentSha256 }))
  }, null, 2)}\n`, "utf8");
}
console.log(`Legacy reviewed prefix passed: ${rows.length}/30`);
