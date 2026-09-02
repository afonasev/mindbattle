import { readdir, readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const topicsDir = resolve(root, "src/content/topics");
const args = process.argv.slice(2);
const outputArgument = args.find((value) => !value.startsWith("--"));
const legacyOnly = args.includes("--legacy-only");
const topicFilter = new Set(args.filter((value) => value.startsWith("--topic=")).map((value) => value.slice("--topic=".length)));
const manifest = JSON.parse(await readFile(resolve(root, "src/content/taxonomy-manifest.json"), "utf8"));
const legacyTopicIds = new Set(manifest.topics.slice(0, 30).map(({ id }) => id));
const outputPath = resolve(root, outputArgument ?? "docs/content-audits/content-findings-final-2026-09-02.json");
const files = (await readdir(topicsDir))
  .filter((name) => name.endsWith(".json"))
  .filter((name) => !legacyOnly || legacyTopicIds.has(name.slice(0, -5)))
  .filter((name) => topicFilter.size === 0 || topicFilter.has(name.slice(0, -5)))
  .sort();
const topics = await Promise.all(files.map(async (name) => JSON.parse(await readFile(resolve(topicsDir, name), "utf8"))));
const questions = topics.flatMap((topic) => {
  const selected = legacyOnly ? topic.questions.slice(0, 50) : topic.questions;
  return selected.map((question) => ({ ...question, topicId: topic.id }));
});

function answerText(answer) {
  return typeof answer === "string" ? answer.trim() : answer.text.trim();
}

function grammarWarnings(question) {
  const warnings = [];
  if (/\s{2,}/u.test(question.prompt)) warnings.push("double-space");
  if (/(?:^|[^\p{L}])кого(?:$|[^\p{L}])[^?]{0,50}(?:^|[^\p{L}])является(?:$|[^\p{L}])/iu.test(question.prompt)) warnings.push("case-whom-is");
  if (/(?:^|[^\p{L}])какой(?:$|[^\p{L}])[^?]{0,50}(?:^|[^\p{L}])являются(?:$|[^\p{L}])/iu.test(question.prompt)) warnings.push("agreement-singular-plural");
  if (/(?:^|[^\p{L}])какие(?:$|[^\p{L}])[^?]{0,50}(?:^|[^\p{L}])является(?:$|[^\p{L}])/iu.test(question.prompt)) warnings.push("agreement-plural-singular");
  const answers = question.answers.map(answerText);
  const isStylizedDottedBrand = (text) => /^(?:[A-Za-z]\.){2,}[A-Za-z]?\.?$/u.test(text);
  const punctuation = answers.map((text) => !isStylizedDottedBrand(text) && /[.!?]$/u.test(text));
  if (punctuation.some(Boolean) && !punctuation.every(Boolean)) warnings.push("mixed-final-punctuation");
  const lowercase = answers.map((text) => !isStylizedDottedBrand(text) && /^\p{Ll}/u.test(text));
  if (lowercase.some(Boolean) && !lowercase.every(Boolean)) warnings.push("mixed-initial-case");
  return warnings;
}

function normalize(prompt) {
  return prompt.toLocaleLowerCase("ru").replace(/ё/gu, "е").replace(/[^a-zа-я0-9]+/gu, " ").trim();
}

const CORRECT_INDEX_STOP_WORDS = new Set(
  "как какой какая какое какие кто кого кем где когда что это этот эта эти был была были является стали стало стала назвать называют называли называется в на к с со из от для по при над под и или а но не его ее их он она они оно".split(" ")
);

function lexicalRoots(value) {
  return [...new Set(normalize(value).split(" ")
    .filter((token) => token.length >= 4 && !CORRECT_INDEX_STOP_WORDS.has(token))
    .map((token) => token.slice(0, Math.min(6, token.length))))];
}

function correctIndexWarning(question) {
  const firstExplanationSentence = question.explanation.split(/[.!?](?:\s|$)/u)[0];
  const explanationRoots = new Set(lexicalRoots(firstExplanationSentence));
  const scores = question.answers.map((answer) => {
    const roots = lexicalRoots(answerText(answer));
    return roots.length === 0 ? 0 : roots.filter((root) => explanationRoots.has(root)).length / roots.length;
  });
  const bestScore = Math.max(...scores);
  const bestIndexes = scores.flatMap((score, index) => score === bestScore ? [index] : []);
  if (
    bestScore >= 0.75 &&
    bestIndexes.length === 1 &&
    bestIndexes[0] !== question.correctIndex &&
    bestScore - scores[question.correctIndex] >= 0.5
  ) {
    const suggestedIndex = bestIndexes[0];
    return {
      questionId: question.id,
      topicId: question.topicId,
      selectedIndex: question.correctIndex,
      selectedAnswer: answerText(question.answers[question.correctIndex]),
      suggestedIndex,
      suggestedAnswer: answerText(question.answers[suggestedIndex]),
      scores
    };
  }
  return null;
}

function difficultyWarnings(question) {
  const warnings = [];
  if (question.difficulty === "easy" && /(?:в каком|каком) году|какого года/iu.test(question.prompt)) {
    warnings.push("easy-exact-year-manual-review");
  }
  if (
    question.difficulty === "hard" &&
    /^(?:кто|какой человек|какая личность)/iu.test(question.prompt.trim()) &&
    question.answers.every((answer) => {
      const text = answerText(answer);
      return /^[А-ЯЁA-Z][\p{L}.'’-]+(?:\s+[А-ЯЁA-Z][\p{L}.'’-]+){1,3}$/u.test(text);
    })
  ) {
    warnings.push("hard-four-proper-names-inference-review");
  }
  return warnings;
}

const GENERIC_SOURCE_TITLES = new Set([
  "just a moment...",
  "access denied"
]);

function editorialWarnings(question) {
  const warnings = [];
  const questionMarks = (question.prompt.match(/\?/gu) ?? []).length;
  if (questionMarks !== 1) warnings.push("prompt-must-be-one-natural-question");
  const correct = normalize(answerText(question.answers[question.correctIndex]));
  const prompt = normalize(question.prompt);
  if (correct.length >= 5 && new RegExp(`(?:^| )${correct.replace(/[.*+?^${}()|[\]\\]/gu, "\\$&")}(?: |$)`, "u").test(prompt)) {
    warnings.push("literal-correct-answer-in-prompt");
  }
  if (question.explanation.includes("Формулировка вопроса указывает именно на этот признак.")) {
    warnings.push("generic-explanation-filler");
  }
  if (/^(?:Какой|Какая|Какое|Какие) .+ соответствует описанию:|^О каком .+ идёт речь:|^Назовите .+ по описанию:|^Что означает следующее описание:|^Что это за .+: «/u.test(question.prompt)) {
    warnings.push("machine-definition-template");
  }
  if (/В структурированных данных объект связан/u.test(question.explanation)) {
    warnings.push("structured-data-explanation-filler");
  }
  if (/(?:листа ного|з[её]рен йного|напиток с на основе)/iu.test(`${question.prompt} ${question.explanation} ${question.answers.map(answerText).join(" ")}`)) {
    warnings.push("damaged-imported-description");
  }
  if (/^Wikidata:/iu.test(question.source.title) || /wikidata\.org\/wiki\/Special:EntityData\//iu.test(question.source.url)) {
    warnings.push("raw-wikidata-source-needs-editorial-review");
  }
  if (GENERIC_SOURCE_TITLES.has(question.source.title.trim().toLocaleLowerCase("ru"))) {
    warnings.push("generic-or-antibot-source-title");
  }
  if (/&(?:#\d+|#x[0-9a-f]+|[a-z]+);/iu.test(question.source.title)) {
    warnings.push("html-entity-in-source-title");
  }
  return warnings;
}

function jaccard(left, right) {
  const intersection = [...left].filter((token) => right.has(token)).length;
  const union = new Set([...left, ...right]).size;
  return union === 0 ? 0 : intersection / union;
}

const normalized = questions.map((question) => ({
  id: question.id,
  topicId: question.topicId,
  prompt: normalize(question.prompt),
  tokens: new Set(normalize(question.prompt).split(" ").filter(Boolean))
}));
const duplicates = [];
for (let leftIndex = 0; leftIndex < normalized.length; leftIndex += 1) {
  for (let rightIndex = leftIndex + 1; rightIndex < normalized.length; rightIndex += 1) {
    const left = normalized[leftIndex];
    const right = normalized[rightIndex];
    if (left.prompt === right.prompt) {
      duplicates.push({ leftQuestionId: left.id, rightQuestionId: right.id, withinTopic: left.topicId === right.topicId, similarity: 1, kind: "exact" });
      continue;
    }
    if (Math.min(left.tokens.size, right.tokens.size) < 4) continue;
    const similarity = jaccard(left.tokens, right.tokens);
    if (similarity >= 0.82) duplicates.push({ leftQuestionId: left.id, rightQuestionId: right.id, withinTopic: left.topicId === right.topicId, similarity, kind: "near" });
  }
}

const factReuseGroups = new Map();
for (const question of questions) {
  const correctAnswer = normalize(answerText(question.answers[question.correctIndex]));
  const key = `${question.topicId}\u0000${question.source.url}\u0000${correctAnswer}`;
  const group = factReuseGroups.get(key) ?? [];
  group.push(question.id);
  factReuseGroups.set(key, group);
}
const factReuseCandidates = [...factReuseGroups.entries()]
  .filter(([, questionIds]) => questionIds.length > 1)
  .map(([key, questionIds]) => {
    const [topicId, sourceUrl, correctAnswer] = key.split("\u0000");
    return { topicId, sourceUrl, correctAnswer, questionIds };
  });

const grammar = questions.flatMap((question) => {
  const findings = grammarWarnings(question);
  return findings.length ? [{ questionId: question.id, topicId: question.topicId, findings }] : [];
});
const difficulty = questions.flatMap((question) => {
  const findings = difficultyWarnings(question);
  return findings.length ? [{ questionId: question.id, topicId: question.topicId, findings }] : [];
});
const editorial = questions.flatMap((question) => {
  const findings = editorialWarnings(question);
  return findings.length ? [{ questionId: question.id, topicId: question.topicId, findings }] : [];
});
const correctIndexCandidates = questions.map(correctIndexWarning).filter(Boolean);
const report = {
  schemaVersion: 1,
  generatedOn: "2026-09-02",
  catalog: { topics: topics.length, questions: questions.length },
  grammar: { questionsWithWarnings: grammar.length, findings: grammar },
  difficulty: { questionsWithWarnings: difficulty.length, findings: difficulty },
  editorial: { questionsWithWarnings: editorial.length, findings: editorial },
  correctIndexCandidates: {
    policy: "Консервативный lexical scan первой фразы explanation; каждый кандидат требует ручной сверки с source, автоматическая смена correctIndex запрещена.",
    total: correctIndexCandidates.length,
    candidates: correctIndexCandidates
  },
  semanticDuplicates: {
    threshold: 0.82,
    total: duplicates.length,
    withinTopic: duplicates.filter(({ withinTopic }) => withinTopic).length,
    crossTopic: duplicates.filter(({ withinTopic }) => !withinTopic).length,
    candidates: duplicates
  },
  factReuseCandidates: {
    policy: "Одинаковые тема, правильный ответ и source URL требуют ручной проверки независимости фактов.",
    total: factReuseCandidates.length,
    candidates: factReuseCandidates
  }
};
await writeFile(outputPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(`Wrote ${outputPath}: ${grammar.length} grammar warnings, ${duplicates.length} duplicate candidates`);
