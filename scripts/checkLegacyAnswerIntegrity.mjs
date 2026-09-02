import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readdir, readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const topicsDir = resolve(root, "src/content/topics");
const baselinePath = resolve(root, "docs/content-audits/legacy-answer-key-2026-09-02.json");
const mode = process.argv[2] ?? "verify";
const revision = process.argv[3] ?? "3d4a2f47fd9bc964ac9384769233b23cada2c5ee";
const answerText = (answer) => typeof answer === "string" ? answer : answer.text;
const approvedGrammarMigrations = new Map([
  ["history-russia-patriotic-war-enemy", ["Германии", "Германия"]],
  ["history-russia-war-1812-opponent", ["Французской империи", "Французская империя"]],
  ["world-literature-anne-frank-format", ["Дневника", "Дневник"]],
  ["sports-swimming-individual-medley-order", [
    "Баттерфляй, на спине, брасс, вольный стиль",
    "Баттерфляй, плавание на спине, брасс, вольный стиль"
  ]],
  ["sports-medley-relay-order", [
    "На спине, брасс, баттерфляй, вольный стиль",
    "Плавание на спине, брасс, баттерфляй, вольный стиль"
  ]]
]);
const normalize = (value) => value
  .toLocaleLowerCase("ru")
  .replace(/ё/gu, "е")
  .replace(/[«»„“”"'`]/gu, "")
  .replace(/[^a-zа-я0-9]+/gu, " ")
  .trim();

if (mode === "generate") {
  const names = execFileSync("git", ["ls-tree", "-r", "--name-only", revision, "src/content/topics"], {
    cwd: root,
    encoding: "utf8"
  }).split("\n").filter((name) => name.endsWith(".json")).sort();
  const questions = [];
  for (const name of names) {
    const topic = JSON.parse(execFileSync("git", ["show", `${revision}:${name}`], { cwd: root, encoding: "utf8" }));
    for (const question of topic.questions) {
      questions.push({
        questionId: question.id,
        topicId: topic.id,
        correctAnswerText: answerText(question.answers[question.correctIndex]),
        sourceQuestionSha256: createHash("sha256").update(JSON.stringify(question)).digest("hex")
      });
    }
  }
  const report = {
    schemaVersion: 1,
    generatedOn: "2026-09-02",
    sourceRevision: revision,
    questionCount: questions.length,
    questions
  };
  if (questions.length !== 1500) throw new Error(`Expected 1500 legacy questions, got ${questions.length}`);
  await writeFile(baselinePath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
  console.log(`Wrote ${baselinePath}: ${questions.length} correct answers`);
  process.exit(0);
}

const baseline = JSON.parse(await readFile(baselinePath, "utf8"));
const expected = new Map(baseline.questions.map((entry) => [entry.questionId, entry]));
const files = (await readdir(topicsDir)).filter((name) => name.endsWith(".json")).sort();
const current = new Map();
for (const name of files) {
  const topic = JSON.parse(await readFile(resolve(topicsDir, name), "utf8"));
  for (const question of topic.questions) {
    if (!expected.has(question.id)) continue;
    current.set(question.id, {
      topicId: topic.id,
      correctAnswerText: answerText(question.answers[question.correctIndex])
    });
  }
}

const issues = [];
for (const [questionId, entry] of expected) {
  const found = current.get(questionId);
  if (!found) {
    issues.push(`${questionId}: legacy question missing`);
    continue;
  }
  if (found.topicId !== entry.topicId) issues.push(`${questionId}: moved from ${entry.topicId} to ${found.topicId}`);
  const approved = approvedGrammarMigrations.get(questionId);
  const preservesMeaning = normalize(found.correctAnswerText) === normalize(entry.correctAnswerText) ||
    (approved && normalize(entry.correctAnswerText) === normalize(approved[0]) && normalize(found.correctAnswerText) === normalize(approved[1]));
  if (!preservesMeaning) {
    issues.push(`${questionId}: correct answer changed from «${entry.correctAnswerText}» to «${found.correctAnswerText}»`);
  }
}
if (issues.length > 0) {
  console.error(issues.join("\n"));
  process.exitCode = 1;
} else {
  console.log(`Legacy answer integrity passed: ${expected.size}/${expected.size}`);
}
