import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const topicIds = new Set(process.argv.slice(2));
if (topicIds.size === 0) throw new Error("Укажите хотя бы один topicId");

const ledgerPath = resolve(root, "src/content/expansion-ledger.json");
const ledger = JSON.parse(await readFile(ledgerPath, "utf8"));

for (const topicId of topicIds) {
  const topicPath = resolve(root, `src/content/topics/${topicId}.json`);
  const bytes = await readFile(topicPath);
  const topic = JSON.parse(bytes);
  const review = JSON.parse(
    await readFile(resolve(root, `src/content/reviews/${topicId}.json`), "utf8")
  );
  const packages = ledger.packages.filter((entry) => entry.topicId === topicId);
  const packageIds = packages.map(({ packageId }) => packageId).sort();
  const reviewedPackageIds = [...(review.evidence?.reviewedPackageIds ?? [])].sort();
  const questionIdsSha256 = createHash("sha256")
    .update(topic.questions.map(({ id }) => id).join("\n"))
    .digest("hex");
  const checks = Object.values(review.evidence?.checks ?? {});
  const assignedReviewers = new Set(packages.map(({ reviewer }) => `codex-independent-${reviewer}`));
  if (
    packages.length === 0 ||
    review.status !== "approved" ||
    !assignedReviewers.has(review.reviewer) ||
    review.contentSha256 !== createHash("sha256").update(bytes).digest("hex") ||
    review.evidence?.questionIdsSha256 !== questionIdsSha256 ||
    checks.length !== 9 ||
    checks.some((count) => count !== topic.questions.length) ||
    JSON.stringify(packageIds) !== JSON.stringify(reviewedPackageIds) ||
    review.criticalFindingsOpen !== 0
  ) {
    throw new Error(`${topicId}: review evidence не позволяет закрыть ledger packages`);
  }
  for (const entry of packages) {
    entry.status = "reviewed";
    entry.reviewedAt = review.reviewedAt;
    entry.reviewContentSha256 = review.contentSha256;
  }
}

ledger.totals = {
  ...ledger.totals,
  assigned: ledger.packages.filter(({ status }) => status === "assigned").length,
  reviewed: ledger.packages.filter(({ status }) => status === "reviewed").length
};
await writeFile(ledgerPath, `${JSON.stringify(ledger, null, 2)}\n`, "utf8");
console.log(`Marked reviewed packages for ${topicIds.size} topics`);
