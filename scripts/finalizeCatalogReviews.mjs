import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const manifest = JSON.parse(await readFile(resolve(root, "src/content/taxonomy-manifest.json"), "utf8"));
const ledger = JSON.parse(await readFile(resolve(root, "src/content/expansion-ledger.json"), "utf8"));
let verified = 0;
const topicEvidence = [];

for (const topic of manifest.topics) {
  const packages = ledger.packages.filter(({ topicId }) => topicId === topic.id);
  const authors = new Set(packages.map(({ author }) => author));
  const reviewers = new Set(packages.map(({ reviewer }) => reviewer));
  if (packages.length === 0 || authors.size !== 1 || reviewers.size !== 1) {
    throw new Error(`${topic.id}: ledger должен назначать единственного автора и reviewer`);
  }
  const [author] = authors;
  const [reviewer] = reviewers;
  if (author === reviewer) throw new Error(`${topic.id}: self-review запрещён`);
  const bytes = await readFile(resolve(root, `src/content/topics/${topic.id}.json`));
  const pack = JSON.parse(bytes);
  if (pack.questions.length !== topic.targetSize) {
    throw new Error(`${topic.id}: ожидалось ${topic.targetSize} вопросов, получено ${pack.questions.length}`);
  }
  const review = JSON.parse(await readFile(resolve(root, `src/content/reviews/${topic.id}.json`), "utf8"));
  const expectedPackageIds = packages.map(({ packageId }) => packageId).sort();
  const reviewedPackageIds = [...(review.evidence?.reviewedPackageIds ?? [])].sort();
  const expectedQuestionIdsSha256 = createHash("sha256")
    .update(pack.questions.map(({ id }) => id).join("\n"))
    .digest("hex");
  const checks = Object.values(review.evidence?.checks ?? {});
  if (
    review.status !== "approved" ||
    review.author !== `codex-${author}` ||
    review.reviewer !== `codex-independent-${reviewer}` ||
    review.contentSha256 !== createHash("sha256").update(bytes).digest("hex") ||
    review.checkedQuestions !== pack.questions.length ||
    review.criticalFindingsOpen !== 0 ||
    review.evidence?.questionIdsSha256 !== expectedQuestionIdsSha256 ||
    checks.length !== 9 ||
    checks.some((count) => count !== pack.questions.length) ||
    JSON.stringify(reviewedPackageIds) !== JSON.stringify(expectedPackageIds) ||
    !Array.isArray(review.evidence?.resolvedFindings) ||
    review.evidence.resolvedFindings.some(
      ({ questionId, issue, resolution }) => !questionId?.trim() || !issue?.trim() || !resolution?.trim()
    )
  ) {
    throw new Error(`${topic.id}: независимое review не имеет полного актуального evidence`);
  }
  verified += 1;
  topicEvidence.push({
    topicId: topic.id,
    author: review.author,
    reviewer: review.reviewer,
    checkedQuestions: review.checkedQuestions,
    reviewedPackageIds,
    checks: review.evidence.checks,
    resolvedFindings: review.evidence.resolvedFindings
  });
}

await writeFile(
  resolve(root, "docs/content-audits/independent-review-summary-2026-09-04.json"),
  `${JSON.stringify({
    schemaVersion: 1,
    verifiedOn: "2026-09-04",
    totals: {
      topics: topicEvidence.length,
      questions: topicEvidence.reduce((sum, entry) => sum + entry.checkedQuestions, 0),
      packages: topicEvidence.reduce((sum, entry) => sum + entry.reviewedPackageIds.length, 0),
      resolvedFindings: topicEvidence.reduce((sum, entry) => sum + entry.resolvedFindings.length, 0)
    },
    topics: topicEvidence
  }, null, 2)}\n`,
  "utf8"
);
console.log(`Verified ${verified} catalog cross-reviews with per-check evidence`);
