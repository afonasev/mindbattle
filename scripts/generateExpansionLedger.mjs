import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const manifest = JSON.parse(await readFile(resolve(root, "src/content/taxonomy-manifest.json"), "utf8"));
const agents = ["content-a", "content-b", "content-c"];
const assignmentOverrides = new Map([
  ["countries-flags", { author: "root", reviewer: "content-a" }],
  ["baking-desserts", { author: "content-b", reviewer: "content-c" }],
  ["agriculture", { author: "content-b", reviewer: "content-c" }],
  ["football", { author: "content-b", reviewer: "content-c" }],
  ["racket-sports", { author: "content-b", reviewer: "content-c" }],
  ["olympic-games", { author: "content-c", reviewer: "content-a" }],
  ["motorsport", { author: "content-b", reviewer: "content-c" }],
  ["combat-sports", { author: "content-c", reviewer: "content-a" }]
]);
const packages = [];

function splitIntoTwoPackages(quota) {
  const first = Object.fromEntries(Object.entries(quota).map(([difficulty, count]) => [difficulty, Math.floor(count / 2)]));
  for (const difficulty of ["easy", "medium", "hard"]) {
    if (Object.values(first).reduce((sum, count) => sum + count, 0) === 25) break;
    if (quota[difficulty] % 2 === 1) first[difficulty] += 1;
  }
  const second = Object.fromEntries(Object.entries(quota).map(([difficulty, count]) => [difficulty, count - first[difficulty]]));
  if ([first, second].some((entry) => Object.values(entry).reduce((sum, count) => sum + count, 0) !== 25)) {
    throw new Error(`Cannot split legacy deficit ${JSON.stringify(quota)} into two 25-question packages`);
  }
  return [first, second];
}

function splitPositionDeficit(deficit, firstCount) {
  const first = deficit.map((count) => Math.floor(count / 2));
  for (let position = 0; first.reduce((sum, count) => sum + count, 0) < firstCount; position += 1) {
    const index = position % 4;
    if (deficit[index] % 2 === 1 && first[index] < Math.ceil(deficit[index] / 2)) first[index] += 1;
  }
  const second = deficit.map((count, position) => count - first[position]);
  return [first, second];
}

function rotatingPositionQuota(questionCount, packageIndex) {
  const base = Math.floor(questionCount / 4);
  const result = Array(4).fill(base);
  for (let offset = 0; offset < questionCount % 4; offset += 1) {
    result[(packageIndex + offset) % 4] += 1;
  }
  return result;
}

for (const [topicIndex, topic] of manifest.topics.entries()) {
  const existingExtension = topicIndex < 30;
  let profiles;
  let positionProfiles;
  if (existingExtension) {
    const current = JSON.parse(await readFile(resolve(root, `src/content/topics/${topic.id}.json`), "utf8"));
    const legacyQuestions = current.questions.slice(0, 50);
    const counts = Object.fromEntries(["easy", "medium", "hard"].map((difficulty) => [
      difficulty,
      legacyQuestions.filter((question) => question.difficulty === difficulty).length
    ]));
    const deficit = Object.fromEntries(["easy", "medium", "hard"].map((difficulty) => [
      difficulty,
      topic.quota[difficulty] - counts[difficulty]
    ]));
    if (Object.values(deficit).some((count) => count < 0) || Object.values(deficit).reduce((sum, count) => sum + count, 0) !== 50) {
      throw new Error(`${topic.id}: invalid absolute-ranking deficit ${JSON.stringify(deficit)}`);
    }
    profiles = splitIntoTwoPackages(deficit);
    const finalPerPosition = { easy: 10, medium: 10, hard: 5 };
    positionProfiles = [{}, {}];
    for (const difficulty of ["easy", "medium", "hard"]) {
      const currentPositions = [0, 1, 2, 3].map((position) =>
        legacyQuestions.filter((question) => question.difficulty === difficulty && question.correctIndex === position).length
      );
      const positionDeficit = currentPositions.map((count) => finalPerPosition[difficulty] - count);
      if (positionDeficit.some((count) => count < 0)) {
        throw new Error(`${topic.id}/${difficulty}: invalid correctIndex deficit ${JSON.stringify(positionDeficit)}`);
      }
      const split = splitPositionDeficit(positionDeficit, profiles[0][difficulty]);
      positionProfiles[0][difficulty] = split[0];
      positionProfiles[1][difficulty] = split[1];
    }
  } else {
    profiles = Array.from({ length: 4 }, () => ({ easy: 10, medium: 10, hard: 5 }));
    positionProfiles = profiles.map((quota, packageIndex) => Object.fromEntries(
      Object.entries(quota).map(([difficulty, count]) => [difficulty, rotatingPositionQuota(count, packageIndex)])
    ));
  }
  const assignment = assignmentOverrides.get(topic.id);
  const author = assignment?.author ?? agents[topicIndex % agents.length];
  const reviewer = assignment?.reviewer ?? agents[(topicIndex + 1) % agents.length];
  for (const [packageIndex, quota] of profiles.entries()) {
    packages.push({
      packageId: `${topic.id}-batch-${String(packageIndex + 1).padStart(2, "0")}`,
      topicId: topic.id,
      topicIndex: topicIndex + 1,
      kind: existingExtension ? "existing-topic-extension" : "new-topic-base",
      questionCount: 25,
      quota,
      correctIndexQuota: positionProfiles[packageIndex],
      author,
      reviewer,
      status: "assigned"
    });
  }
}
const ledger = {
  revision: "mindbattle-expansion-ledger-2026-09-02-r3",
  packageSize: 25,
  policy: "Для прежней темы квоты двух пакетов вычисляются из абсолютного распределения исходных 50 вопросов до финальных 40/40/20. Все пакеты темы закреплены за одним автором, reviewer всегда другой агент; интеграция требует независимой проверки вопросов, источников, сложности, грамматики и дубликатов.",
  totals: {
    packages: packages.length,
    questions: packages.reduce((sum, entry) => sum + entry.questionCount, 0),
    existingTopicExtensionPackages: packages.filter(({ kind }) => kind === "existing-topic-extension").length,
    newTopicBasePackages: packages.filter(({ kind }) => kind === "new-topic-base").length
  },
  packages
};
if (ledger.totals.packages !== 380 || ledger.totals.questions !== 9500) throw new Error("Expansion ledger totals are invalid");
if (packages.some(({ author, reviewer }) => author === reviewer)) throw new Error("Self-review assignment found");
await writeFile(resolve(root, "src/content/expansion-ledger.json"), `${JSON.stringify(ledger, null, 2)}\n`, "utf8");
console.log(`Wrote ${ledger.totals.packages} packages for ${ledger.totals.questions} questions`);
