import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const [topicId, ...argumentsAfterTopic] = process.argv.slice(2);
const draftPaths = argumentsAfterTopic.filter((value) => !value.startsWith("--relevel="));
const relevels = new Map(argumentsAfterTopic.filter((value) => value.startsWith("--relevel=")).map((value) => {
  const [questionId, difficulty] = value.slice("--relevel=".length).split(":");
  if (!questionId || !["easy", "medium", "hard"].includes(difficulty)) throw new Error(`Invalid relevel: ${value}`);
  return [questionId, difficulty];
}));
if (!topicId || draftPaths.length === 0) {
  throw new Error("Usage: node scripts/assembleTopicDrafts.mjs <topicId> <draft.json>...");
}

const manifest = JSON.parse(await readFile(resolve(root, "src/content/taxonomy-manifest.json"), "utf8"));
const target = manifest.topics.find(({ id }) => id === topicId);
if (!target) throw new Error(`Unknown topic: ${topicId}`);

const drafts = await Promise.all(draftPaths.map(async (draftPath) => {
  const draft = JSON.parse(await readFile(resolve(root, draftPath), "utf8"));
  if (draft.topicId !== topicId) throw new Error(`${draftPath}: expected topicId ${topicId}`);
  if (!Array.isArray(draft.questions)) throw new Error(`${draftPath}: questions must be an array`);
  return draft.questions;
}));
const questions = drafts.flat();
for (const [questionId, difficulty] of relevels) {
  const question = questions.find(({ id }) => id === questionId);
  if (!question) throw new Error(`Unknown relevel question: ${questionId}`);
  question.difficulty = difficulty;
}
const ids = new Set(questions.map(({ id }) => id));
if (ids.size !== questions.length) throw new Error(`${topicId}: duplicate question ids across drafts`);
if (questions.length !== target.targetSize) {
  throw new Error(`${topicId}: expected ${target.targetSize} questions, received ${questions.length}`);
}
for (const [difficulty, expected] of Object.entries(target.quota)) {
  const actual = questions.filter((question) => question.difficulty === difficulty).length;
  if (actual !== expected) throw new Error(`${topicId}: expected ${expected} ${difficulty}, received ${actual}`);
}

for (const difficulty of Object.keys(target.quota)) {
  const scoped = questions.filter((question) => question.difficulty === difficulty);
  scoped.forEach((question, index) => {
    const desiredIndex = index % 4;
    if (question.correctIndex === desiredIndex) return;
    const answers = [...question.answers];
    [answers[question.correctIndex], answers[desiredIndex]] = [answers[desiredIndex], answers[question.correctIndex]];
    question.answers = answers;
    question.correctIndex = desiredIndex;
  });
}

const output = { id: topicId, title: target.title, questions };
const outputPath = resolve(root, `src/content/topics/${topicId}.json`);
await writeFile(outputPath, `${JSON.stringify(output, null, 2)}\n`, "utf8");
console.log(`Assembled ${topicId}: ${questions.length} questions from ${draftPaths.length} drafts`);
