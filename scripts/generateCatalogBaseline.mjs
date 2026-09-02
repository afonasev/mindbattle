import { createHash } from "node:crypto";
import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";

const topicsDirectory = resolve(process.argv[2] ?? "src/content/topics");
const outputPath = resolve(
  process.argv[3] ?? "docs/content-audits/catalog-baseline-2026-09-02.json"
);
const catalogRevision = process.argv[4] ?? "mindbattle-questions-2026-09-01-r2";

const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const files = (await readdir(topicsDirectory))
  .filter((file) => file.endsWith(".json"))
  .sort();

const topics = [];
const questionIds = new Set();

for (const file of files) {
  const raw = await readFile(join(topicsDirectory, file), "utf8");
  const topic = JSON.parse(raw);
  const questions = topic.questions.map((question) => {
    if (questionIds.has(question.id)) {
      throw new Error(`Duplicate question id: ${question.id}`);
    }
    questionIds.add(question.id);
    return {
      id: question.id,
      difficulty: question.difficulty,
      prompt: question.prompt,
      semanticSha256: sha256(JSON.stringify(question))
    };
  });
  topics.push({
    id: topic.id,
    title: topic.title,
    file,
    contentSha256: sha256(raw),
    questions
  });
}

const baseline = {
  schemaVersion: 1,
  capturedOn: "2026-09-02",
  catalogRevision,
  totals: {
    topics: topics.length,
    questions: questionIds.size
  },
  topics
};

if (baseline.totals.topics !== 30 || baseline.totals.questions !== 1500) {
  throw new Error(
    `Expected 30 topics / 1500 questions, got ${baseline.totals.topics} / ${baseline.totals.questions}`
  );
}

await mkdir(dirname(outputPath), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(baseline, null, 2)}\n`, "utf8");
console.log(`Wrote ${outputPath}: ${baseline.totals.topics} topics / ${baseline.totals.questions} questions`);
