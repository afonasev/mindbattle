import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const manifest = JSON.parse(await readFile(resolve(root, "src/content/taxonomy-manifest.json"), "utf8"));
const findings = JSON.parse(await readFile(resolve(root, "docs/content-audits/content-findings-final-2026-09-02.json"), "utf8"));
const decisions = [];

for (const target of manifest.topics) {
  const bytes = await readFile(resolve(root, `src/content/topics/${target.id}.json`));
  const pack = JSON.parse(bytes);
  const review = JSON.parse(await readFile(resolve(root, `src/content/reviews/${target.id}.json`), "utf8"));
  const urls = new Set(pack.questions.map(({ source }) => source.url));
  const domains = new Set(pack.questions.map(({ source }) => new URL(source.url).hostname));
  const prompts = new Set(pack.questions.map(({ prompt }) =>
    prompt.toLocaleLowerCase("ru").replace(/[^a-zа-яё0-9]+/gu, " ").trim()
  ));
  const reuseCandidates = findings.factReuseCandidates.candidates.filter(
    ({ topicId }) => topicId === target.id
  );
  const counts = Object.fromEntries(["easy", "medium", "hard"].map((difficulty) => [
    difficulty,
    pack.questions.filter((question) => question.difficulty === difficulty).length
  ]));
  const evidenceComplete = Object.values(review.evidence?.checks ?? {}).length === 9 &&
    Object.values(review.evidence.checks).every((count) => count === pack.questions.length);
  decisions.push({
    topicId: target.id,
    evaluatedSize: pack.questions.length,
    packBytes: bytes.length,
    uniqueSourceUrls: urls.size,
    sourceDomains: domains.size,
    sourceInventory: [...urls].sort(),
    independentFactsReviewed: evidenceComplete ? pack.questions.length : 0,
    easyCandidatesReviewed: evidenceComplete ? counts.easy : 0,
    difficultyProfile: counts,
    duplicateRisk: {
      exactPromptDuplicates: pack.questions.length - prompts.size,
      automaticFactReuseCandidateGroups: reuseCandidates.length,
      independentDuplicateReviewComplete: review.evidence?.checks?.duplicates === pack.questions.length
    },
    reviewContentSha256: review.contentSha256,
    decision: 100,
    eligibleFor200: false,
    eligibleFor300: false,
    reasons: [
      "Базовый пакет 40/40/20 имеет приоритет перед расширением отдельных тем.",
      "Независимый inventory дополнительных 100 неповторяющихся фактов сверх базового пакета не проводился.",
      "Остановка на 100 уменьшает риск семантических дублей и ослабления источников."
    ]
  });
}

await writeFile(
  resolve(root, "docs/content-audits/topic-expansion-eligibility-2026-09-02.json"),
  `${JSON.stringify({
    schemaVersion: 2,
    evaluatedOn: "2026-09-04",
    policy: "Для базовых 100 учитываются фактические source inventory, байты pack, профиль сложности и независимый duplicate review. Расширение до 200/300 требует отдельного inventory дополнительных фактов и повторного performance gate; отсутствие доказательства означает 100.",
    totals: { evaluated: decisions.length, target100: decisions.length, target200: 0, target300: 0 },
    decisions
  }, null, 2)}\n`,
  "utf8"
);
console.log(`Eligibility: ${decisions.length} topics remain at 100`);
