import { createHash } from "node:crypto";
import { readdir, readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const topicsDir = resolve(root, "src/content/topics");
const files = (await readdir(topicsDir)).filter((name) => name.endsWith(".json")).sort();
const topicFiles = await Promise.all(files.map(async (name) => {
  const bytes = await readFile(resolve(topicsDir, name));
  return { name, bytes, topic: JSON.parse(bytes) };
}));
const topics = topicFiles.map(({ topic }) => topic);
const baseline = JSON.parse(await readFile(resolve(root, "docs/content-audits/catalog-baseline-2026-09-02.json"), "utf8"));
const audit = JSON.parse(await readFile(resolve(root, "docs/content-audits/existing-catalog-audit-2026-09-02.json"), "utf8"));
const feedback = JSON.parse(await readFile(resolve(root, "docs/content-audits/feedback-analysis-2026-09-02.json"), "utf8"));
const expectedIds = new Set(baseline.topics.flatMap((topic) => topic.questions.map(({ id }) => id)));
const actualQuestions = topics.flatMap((topic) => topic.questions);
const actualIds = new Set(actualQuestions.map(({ id }) => id));
const auditIds = new Set(audit.entries.map(({ questionId }) => questionId));
const notes = actualQuestions.flatMap(({ answers }) => answers.map((answer) => typeof answer === "string" ? "" : answer.note));
const duplicateNoteQuestions = actualQuestions.filter(({ answers }) => {
  const values = answers.map((answer) => typeof answer === "string" ? "" : answer.note.trim().toLocaleLowerCase("ru"));
  return new Set(values).size !== 4;
}).map(({ id }) => id);
const difficultyCoverageIssues = topics.flatMap((topic) => {
  const counts = Object.fromEntries(["easy", "medium", "hard"].map((difficulty) => [difficulty, topic.questions.filter((question) => question.difficulty === difficulty).length]));
  return topic.questions.length === 50 && counts.easy + counts.medium + counts.hard === 50
    ? []
    : [{ topicId: topic.id, counts }];
});
const reviews = await Promise.all(topicFiles.map(async ({ topic }) =>
  JSON.parse(await readFile(resolve(root, `src/content/reviews/${topic.id}.json`), "utf8"))
));
const reviewIssues = topicFiles.flatMap(({ bytes, topic }) => {
  const review = reviews.find(({ topicId }) => topicId === topic.id);
  const digest = createHash("sha256").update(bytes).digest("hex");
  return review &&
    review.status === "approved" &&
    review.author !== review.reviewer &&
    review.contentSha256 === digest &&
    review.checkedQuestions === 50 &&
    review.criticalFindingsOpen === 0
    ? []
    : [{ topicId: topic.id, expectedSha256: digest, review }];
});
const checks = {
  topics: topics.length === 30,
  questions: actualQuestions.length === 1500,
  baselineIdsPreserved: expectedIds.size === 1500 && [...expectedIds].every((id) => actualIds.has(id)),
  auditCoverage: audit.entries.length === 1500 && auditIds.size === 1500 && [...expectedIds].every((id) => auditIds.has(id)),
  notes: notes.length === 6000 && notes.every((note) => note.trim().length > 0),
  distinctNotesWithinQuestion: duplicateNoteQuestions.length === 0,
  absoluteLegacyDifficultyCoverage: difficultyCoverageIssues.length === 0,
  independentReviews: reviewIssues.length === 0,
  feedbackReport: feedback.totals.uniqueEvents === 80 && feedback.totals.correctnessRateAvailable === false
};
const report = {
  schemaVersion: 1,
  checkedOn: "2026-09-02",
  passed: Object.values(checks).every(Boolean),
  checks,
  details: {
    duplicateNoteQuestions,
    difficultyCoverageIssues,
    reviewIssues,
    movedQuestions: audit.stats.moved,
    sourceUrlsRequiringReplacementOrBrowserVerification: JSON.parse(await readFile(resolve(root, "docs/content-audits/source-url-check-2026-09-02.json"), "utf8")).totals.unreachable
  }
};
await writeFile(resolve(root, "docs/content-audits/pre-agent-gate-2026-09-02.json"), `${JSON.stringify(report, null, 2)}\n`, "utf8");
if (!report.passed) throw new Error("Pre-agent gate failed");
console.log(`Pre-agent gate passed: ${actualQuestions.length} questions, ${notes.length} notes, ${audit.entries.length} audit decisions`);
