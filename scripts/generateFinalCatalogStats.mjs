import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const manifest = JSON.parse(await readFile(resolve(root, "src/content/taxonomy-manifest.json"), "utf8"));
const ledger = JSON.parse(await readFile(resolve(root, "src/content/expansion-ledger.json"), "utf8"));
const legacyAudit = JSON.parse(await readFile(resolve(root, "docs/content-audits/existing-catalog-audit-2026-09-02.json"), "utf8"));
const feedback = JSON.parse(await readFile(resolve(root, "docs/content-audits/feedback-analysis-2026-09-02.json"), "utf8"));
const sourceCheck = JSON.parse(await readFile(resolve(root, "docs/content-audits/source-url-check-2026-09-02.json"), "utf8"));
const findings = JSON.parse(await readFile(resolve(root, "docs/content-audits/content-findings-final-2026-09-02.json"), "utf8"));
const caseCheck = JSON.parse(await readFile(resolve(root, "docs/content-audits/russian-case-findings-final-2026-09-02.json"), "utf8"));
const caseManualReview = JSON.parse(await readFile(resolve(root, "docs/content-audits/russian-case-manual-review-2026-09-02.json"), "utf8"));
const difficulties = ["easy", "medium", "hard"];
const legacyChanges = legacyAudit.entries.flatMap(({ changes }) => changes);
const totals = {
  topics: 0,
  questions: 0,
  easy: 0,
  medium: 0,
  hard: 0,
  answerNotes: 0,
  independentlyReviewedQuestions: 0,
  resolvedReviewFindings: 0
};
const allIds = new Set();
const sourceUrls = new Set();
const sourceDomains = new Set();
const topics = [];

for (const target of manifest.topics) {
  const pack = JSON.parse(await readFile(resolve(root, `src/content/topics/${target.id}.json`), "utf8"));
  const review = JSON.parse(await readFile(resolve(root, `src/content/reviews/${target.id}.json`), "utf8"));
  const counts = Object.fromEntries(difficulties.map((difficulty) => [
    difficulty,
    pack.questions.filter((question) => question.difficulty === difficulty).length
  ]));
  if (pack.questions.length !== target.targetSize || difficulties.some((difficulty) => counts[difficulty] !== target.quota[difficulty])) {
    throw new Error(`${target.id}: pack не совпадает с target/quota manifest`);
  }
  const reviewChecks = Object.values(review.evidence?.checks ?? {});
  if (
    review.status !== "approved" ||
    review.checkedQuestions !== pack.questions.length ||
    review.criticalFindingsOpen !== 0 ||
    reviewChecks.length !== 9 ||
    reviewChecks.some((count) => count !== pack.questions.length)
  ) {
    throw new Error(`${target.id}: отсутствует полный независимый review evidence`);
  }
  const urls = new Set();
  for (const question of pack.questions) {
    if (allIds.has(question.id)) throw new Error(`Duplicate question id: ${question.id}`);
    allIds.add(question.id);
    sourceUrls.add(question.source.url);
    urls.add(question.source.url);
    sourceDomains.add(new URL(question.source.url).hostname);
    totals.answerNotes += question.answers.filter((answer) => typeof answer !== "string" && answer.note.trim()).length;
  }
  totals.topics += 1;
  totals.questions += pack.questions.length;
  totals.independentlyReviewedQuestions += review.checkedQuestions;
  totals.resolvedReviewFindings += review.evidence.resolvedFindings.length;
  for (const difficulty of difficulties) totals[difficulty] += counts[difficulty];
  topics.push({
    topicId: target.id,
    title: target.title,
    targetSize: target.targetSize,
    ...counts,
    uniqueSourceUrls: urls.size,
    resolvedReviewFindings: review.evidence.resolvedFindings.length
  });
}

const reviewedPackages = ledger.packages.filter(({ status }) => status === "reviewed").length;
if (reviewedPackages !== ledger.packages.length) {
  throw new Error(`Ledger review incomplete: ${reviewedPackages}/${ledger.packages.length}`);
}

const report = {
  schemaVersion: 1,
  generatedOn: "2026-09-04",
  catalogRevision: "mindbattle-questions-2026-09-02-r3",
  totals: {
    ...totals,
    uniqueQuestionIds: allIds.size,
    uniqueSourceUrls: sourceUrls.size,
    sourceDomains: sourceDomains.size,
    legacyQuestionsMoved: legacyAudit.stats.moved,
    legacyGrammarFixes: legacyAudit.stats.grammarFixes,
    legacyDistractorFixes: legacyChanges.filter((change) => change.startsWith("distractor:")).length,
    legacyAnswerNotesAdded: legacyAudit.stats.answerNotes,
    feedbackEventsAnalyzed: feedback.totals.uniqueEvents,
    feedbackRatedQuestions: feedback.totals.ratedQuestions,
    feedbackCorrectnessRateAvailable: feedback.totals.correctnessRateAvailable,
    feedbackStrengths: feedback.totals.strengths,
    feedbackComparisonBeforeAudit: feedback.totals.comparisons,
    feedbackComparisonAfterAudit: legacyAudit.stats.feedbackComparisonAfter,
    sourceUrlsChecked: sourceCheck.totals.uniqueUrls,
    sourceUrlsReachable: sourceCheck.totals.reachable,
    sourceUrlsContentInspectable: sourceCheck.totals.contentInspectable,
    sourceUrlsUnreachable: sourceCheck.totals.unreachable,
    sourceUrlsDefiniteDead: sourceCheck.totals.definiteDead,
    sourceUrlsNetworkOrServerLimited: sourceCheck.totals.networkOrServerLimited,
    sourceQuestionsCovered: sourceCheck.totals.questionsCovered,
    grammarWarnings: findings.grammar.questionsWithWarnings,
    russianCaseFramesChecked: caseCheck.questionsWithRecognizedCaseFrame,
    russianCaseCandidatesForManualReview: caseCheck.candidateQuestions,
    russianCaseCandidatesManuallyReviewed: caseManualReview.totals.candidates,
    russianCaseCandidatesOpen: caseManualReview.totals.open,
    editorialWarnings: findings.editorial.questionsWithWarnings,
    correctIndexCandidatesForManualReview: findings.correctIndexCandidates.total,
    semanticDuplicateCandidates: findings.semanticDuplicates.total,
    factReuseCandidatesForManualReview: findings.factReuseCandidates.total,
    expansionPackagesReviewed: reviewedPackages
  },
  targetSizes: Object.fromEntries([100, 200, 300].map((size) => [
    size,
    manifest.topics.filter(({ targetSize }) => targetSize === size).length
  ])),
  topics
};

await writeFile(
  resolve(root, "docs/content-audits/final-catalog-stats-2026-09-02.json"),
  `${JSON.stringify(report, null, 2)}\n`,
  "utf8"
);
console.log(`Catalog stats: ${totals.topics} topics, ${totals.questions} questions, ${sourceUrls.size} unique source URLs`);
