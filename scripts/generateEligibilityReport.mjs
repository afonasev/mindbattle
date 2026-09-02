import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const manifest = JSON.parse(await readFile(resolve(root, "src/content/taxonomy-manifest.json"), "utf8"));
const decisions = [];

for (const target of manifest.topics) {
  const pack = JSON.parse(await readFile(resolve(root, `src/content/topics/${target.id}.json`), "utf8"));
  const urls = new Set(pack.questions.map(({ source }) => source.url));
  const domains = new Set(pack.questions.map(({ source }) => new URL(source.url).hostname));
  decisions.push({
    topicId: target.id,
    evaluatedSize: pack.questions.length,
    uniqueSourceUrls: urls.size,
    sourceDomains: domains.size,
    decision: 100,
    eligibleFor200: false,
    eligibleFor300: false,
    reasons: [
      "Базовый пакет 40/40/20 имеет приоритет перед расширением отдельных тем.",
      "Независимый inventory ещё 100 неповторяющихся фактов и повторный performance gate не проводились.",
      "Остановка на 100 уменьшает риск семантических дублей и ослабления источников."
    ]
  });
}

await writeFile(
  resolve(root, "docs/content-audits/topic-expansion-eligibility-2026-09-02.json"),
  `${JSON.stringify({
    schemaVersion: 1,
    evaluatedOn: "2026-09-02",
    policy: "Расширение до 200/300 выполняется только после отдельного подтверждения source inventory, duplicate audit и performance gate; отсутствие доказательства означает 100.",
    totals: { evaluated: decisions.length, target100: decisions.length, target200: 0, target300: 0 },
    decisions
  }, null, 2)}\n`,
  "utf8"
);
console.log(`Eligibility: ${decisions.length} topics remain at 100`);
