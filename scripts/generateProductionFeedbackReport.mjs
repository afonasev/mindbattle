import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { readFeedbackCatalog } from "../server/feedbackCatalog.mjs";
import { analyzeProductionFeedback } from "../server/feedbackReport.mjs";

const [journalPath] = process.argv.slice(2);
if (!journalPath) {
  console.error("Usage: npm run feedback:production-report -- /var/lib/mindbattle/difficulty-feedback.ndjson");
  process.exitCode = 64;
} else {
  const catalog = await readFeedbackCatalog();
  const report = analyzeProductionFeedback(await readFile(resolve(journalPath), "utf8"), catalog);
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
}
