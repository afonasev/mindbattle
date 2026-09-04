import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const auditsDir = resolve(root, "docs/content-audits");
const baseline = JSON.parse(await readFile(resolve(auditsDir, "catalog-baseline-2026-09-02.json"), "utf8"));
const ranges = [[1, 10], [11, 20], [21, 30]];
const checkNames = [
  "factualCorrectness",
  "optionQuestionRelevance",
  "educationalValue",
  "neutrality",
  "noCorrectAnswerLeak",
  "russianGrammar",
  "sourceVerifiability"
];
const summarySegments = [];

for (const [start, end] of ranges) {
  const label = `${String(start).padStart(2, "0")}-${String(end).padStart(2, "0")}`;
  const reportPath = resolve(auditsDir, `baseline-wrong-answer-notes-audit-${label}-2026-09-04.json`);
  const reportBytes = await readFile(reportPath);
  const report = JSON.parse(reportBytes);
  const baselineTopics = baseline.topics.slice(start - 1, end);
  const expected = new Map();

  for (const baselineTopic of baselineTopics) {
    const topic = JSON.parse(await readFile(resolve(root, `src/content/topics/${baselineTopic.id}.json`), "utf8"));
    const currentById = new Map(topic.questions.map((question) => [question.id, question]));
    for (const baselineQuestion of baselineTopic.questions) {
      const question = currentById.get(baselineQuestion.id);
      if (!question) throw new Error(`${label}: отсутствует baseline question ${baselineQuestion.id}`);
      question.answers.forEach((answer, answerIndex) => {
        if (answerIndex === question.correctIndex) return;
        expected.set(`${question.id}:${answerIndex}`, {
          topicId: topic.id,
          questionId: question.id,
          answerIndex,
          answerText: answer.text,
          note: answer.note
        });
      });
    }
  }

  if (report.schemaVersion !== 1 || JSON.stringify(report.manifestRange) !== JSON.stringify([start, end])) {
    throw new Error(`${label}: неверная схема или manifestRange`);
  }
  if (!Array.isArray(report.records) || report.records.length !== expected.size) {
    throw new Error(`${label}: ожидалось ${expected.size} item records, получено ${report.records?.length ?? 0}`);
  }
  const seen = new Set();
  let correctedNotes = 0;
  for (const record of report.records) {
    const key = `${record.questionId}:${record.answerIndex}`;
    const current = expected.get(key);
    if (!current || seen.has(key)) throw new Error(`${label}: лишняя или повторная запись ${key}`);
    seen.add(key);
    for (const field of ["topicId", "questionId", "answerIndex", "answerText", "note"]) {
      if (record[field] !== current[field]) throw new Error(`${label}: ${key} не совпадает по ${field}`);
    }
    if (record.status !== "approved") throw new Error(`${label}: ${key} не approved`);
    if (Object.keys(record.checks ?? {}).sort().join("|") !== [...checkNames].sort().join("|") ||
        checkNames.some((name) => record.checks[name] !== true)) {
      throw new Error(`${label}: ${key} не прошёл семь проверок`);
    }
    if (record.finding !== null) {
      if (!record.finding || !record.finding.issue?.trim() || !record.finding.resolution?.trim()) {
        throw new Error(`${label}: ${key} содержит неполный finding`);
      }
      correctedNotes += 1;
    }
  }
  if (seen.size !== expected.size) throw new Error(`${label}: неполное покрытие baseline notes`);
  const expectedTotals = {
    topics: 10,
    questions: 500,
    wrongAnswerNotes: 1500,
    correctedNotes,
    openFindings: 0
  };
  if (JSON.stringify(report.totals) !== JSON.stringify(expectedTotals)) {
    throw new Error(`${label}: totals не совпадают с фактическими ${JSON.stringify(expectedTotals)}`);
  }
  summarySegments.push({
    manifestRange: [start, end],
    report: reportPath.slice(root.length + 1),
    reportSha256: createHash("sha256").update(reportBytes).digest("hex"),
    ...expectedTotals
  });
}

const summary = {
  schemaVersion: 1,
  verifiedOn: new Date().toISOString().slice(0, 10),
  criteria: checkNames,
  totals: {
    topics: summarySegments.reduce((sum, segment) => sum + segment.topics, 0),
    questions: summarySegments.reduce((sum, segment) => sum + segment.questions, 0),
    wrongAnswerNotes: summarySegments.reduce((sum, segment) => sum + segment.wrongAnswerNotes, 0),
    correctedNotes: summarySegments.reduce((sum, segment) => sum + segment.correctedNotes, 0),
    openFindings: summarySegments.reduce((sum, segment) => sum + segment.openFindings, 0)
  },
  segments: summarySegments
};
await writeFile(
  resolve(auditsDir, "baseline-wrong-answer-notes-audit-summary-2026-09-04.json"),
  `${JSON.stringify(summary, null, 2)}\n`,
  "utf8"
);
console.log(`Baseline wrong-answer notes verified: ${summary.totals.wrongAnswerNotes}/4500, corrected ${summary.totals.correctedNotes}`);
