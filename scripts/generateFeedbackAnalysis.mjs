import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const snapshotPath = resolve(process.argv[2] ?? "/private/tmp/mindbattle-feedback-snapshot-2026-09-02.ndjson");
const outputPath = resolve(root, process.argv[3] ?? "docs/content-audits/feedback-analysis-2026-09-02.json");
const baselinePath = resolve(root, "docs/content-audits/catalog-baseline-2026-09-02.json");
const difficulties = ["easy", "medium", "hard"];
const rank = new Map(difficulties.map((difficulty, index) => [difficulty, index]));

const baseline = JSON.parse(await readFile(baselinePath, "utf8"));
const questions = new Map(
  baseline.topics.flatMap((topic) => topic.questions.map((question) => [question.id, question]))
);
const rawLines = (await readFile(snapshotPath, "utf8")).split("\n").filter((line) => line.trim());
const unique = new Map();
const duplicateEventIds = new Set();
const invalidLines = [];
const unknownQuestionIds = new Set();

for (const [index, line] of rawLines.entries()) {
  try {
    const event = JSON.parse(line);
    if (
      event.schemaVersion !== 1 ||
      typeof event.eventId !== "string" ||
      typeof event.questionId !== "string" ||
      !difficulties.includes(event.assignedDifficulty) ||
      !difficulties.includes(event.perceivedDifficulty)
    ) {
      invalidLines.push(index + 1);
      continue;
    }
    if (unique.has(event.eventId)) {
      duplicateEventIds.add(event.eventId);
      continue;
    }
    unique.set(event.eventId, event);
    if (!questions.has(event.questionId)) unknownQuestionIds.add(event.questionId);
  } catch {
    invalidLines.push(index + 1);
  }
}

const grouped = new Map();
for (const event of unique.values()) {
  if (!questions.has(event.questionId)) continue;
  grouped.set(event.questionId, [...(grouped.get(event.questionId) ?? []), event]);
}

const signals = [...grouped.entries()].map(([questionId, events]) => {
  const perceived = { easy: 0, medium: 0, hard: 0 };
  for (const event of events) perceived[event.perceivedDifficulty] += 1;
  const ordered = events.map((event) => event.perceivedDifficulty).sort((left, right) => rank.get(left) - rank.get(right));
  const plurality = difficulties
    .map((difficulty) => [difficulty, perceived[difficulty]])
    .sort((left, right) => right[1] - left[1] || rank.get(left[0]) - rank.get(right[0]))[0];
  const sustained = events.length >= 5 && plurality[1] / events.length >= 2 / 3;
  const assignedDifficulty = questions.get(questionId).difficulty;
  const direction = rank.get(ordered[Math.floor((ordered.length - 1) / 2)]) - rank.get(assignedDifficulty);
  return {
    questionId,
    assignedDifficulty,
    total: events.length,
    perceived,
    median: ordered[Math.floor((ordered.length - 1) / 2)],
    comparison: direction === 0 ? "exact" : direction < 0 ? "lower" : "higher",
    strength: events.length < 3 ? "weak" : sustained ? "sustained" : "indicative",
    suggestedDifficulty: sustained && plurality[0] !== assignedDifficulty ? plurality[0] : null
  };
}).sort((left, right) => right.total - left.total || left.questionId.localeCompare(right.questionId));

const byAssignedDifficulty = Object.fromEntries(difficulties.map((difficulty) => {
  const subset = signals.filter(({ assignedDifficulty }) => assignedDifficulty === difficulty);
  return [difficulty, {
    total: subset.length,
    exact: subset.filter(({ comparison }) => comparison === "exact").length,
    lower: subset.filter(({ comparison }) => comparison === "lower").length,
    higher: subset.filter(({ comparison }) => comparison === "higher").length
  }];
}));
const comparisonTotals = {
  exact: signals.filter(({ comparison }) => comparison === "exact").length,
  lower: signals.filter(({ comparison }) => comparison === "lower").length,
  higher: signals.filter(({ comparison }) => comparison === "higher").length
};

const report = {
  schemaVersion: 1,
  generatedOn: "2026-09-02",
  rawSnapshot: { fileName: snapshotPath.split("/").at(-1), committed: false },
  policy: {
    weak: "n < 3: только приоритет ручной проверки",
    indicative: "n = 3–4: заметный сигнал без автоматического переноса",
    sustained: "n >= 5 и не менее 2/3 голосов за один уровень: кандидат на перенос с ручной проверкой"
  },
  totals: {
    rawLines: rawLines.length,
    uniqueEvents: unique.size,
    ratedQuestions: signals.length,
    invalidLines,
    duplicateEventIds: [...duplicateEventIds].sort(),
    unknownQuestionIds: [...unknownQuestionIds].sort(),
    strengths: {
      weak: signals.filter(({ strength }) => strength === "weak").length,
      indicative: signals.filter(({ strength }) => strength === "indicative").length,
      sustained: signals.filter(({ strength }) => strength === "sustained").length
    },
    comparisons: comparisonTotals,
    byAssignedDifficulty,
    correctnessRateAvailable: false
  },
  patterns: [
    `${comparisonTotals.exact} из ${signals.length} оценок совпали с исходным уровнем; игроки чаще считали вопрос легче (${comparisonTotals.lower}), чем сложнее (${comparisonTotals.higher}).`,
    `Среди исходных medium ниже уровня оценены ${byAssignedDifficulty.medium.lower} из ${byAssignedDifficulty.medium.total}, среди hard — ${byAssignedDifficulty.hard.lower} из ${byAssignedDifficulty.hard.total}.`,
    "Каждый вопрос получил только один групповой голос, поэтому закономерность используется как направление ручной проверки, а не как основание автоматического переноса."
  ],
  signals
};

await writeFile(outputPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(`Wrote ${outputPath}: ${signals.length} question signals`);
