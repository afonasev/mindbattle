import { readFile, readdir } from "node:fs/promises";
import { join, resolve } from "node:path";
import { analyzeProductionFeedback } from "../server/feedbackReport.mjs";

const [journalPath] = process.argv.slice(2);
if (!journalPath) {
  console.error("Usage: npm run feedback:production-report -- /var/lib/mindbattle/difficulty-feedback.ndjson");
  process.exitCode = 64;
} else {
  const root = resolve(import.meta.dirname, "..");
  const catalogRevision = "mindbattle-questions-2026-09-02-r3";
  const questions = new Map();
  for (const name of await readdir(join(root, "src/content/topics"))) {
    if (!name.endsWith(".json")) continue;
    const topic = JSON.parse(await readFile(join(root, "src/content/topics", name), "utf8"));
    for (const question of topic.questions) questions.set(question.id, question.difficulty);
  }
  const report = analyzeProductionFeedback(await readFile(resolve(journalPath), "utf8"), { questions, catalogRevision });
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
}
