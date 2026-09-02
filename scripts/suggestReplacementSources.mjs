import { readdir, readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const topicsDir = resolve(root, "src/content/topics");
const sourceReport = JSON.parse(await readFile(resolve(root, "docs/content-audits/source-url-check-2026-09-02.json"), "utf8"));
const failedUrls = new Set(sourceReport.failures.map(({ url }) => url));
const files = (await readdir(topicsDir)).filter((name) => name.endsWith(".json")).sort();
const topics = await Promise.all(files.map(async (name) => JSON.parse(await readFile(resolve(topicsDir, name), "utf8"))));
const questions = topics.flatMap((topic) => topic.questions.filter((question) => failedUrls.has(question.source.url)).map((question) => ({ ...question, topicId: topic.id })));
const outputPath = resolve(process.argv[2] ?? "/private/tmp/mindbattle-source-replacement-suggestions.json");
const labels = [...new Set(questions.map((question) => {
  const correct = question.answers[question.correctIndex];
  return typeof correct === "string" ? correct : correct.text;
}))];
const articlesByLabel = new Map();

function sparqlString(value) {
  return `"${value.replaceAll("\\", "\\\\").replaceAll('"', '\\"').replaceAll("\n", " ")}"@ru`;
}

for (let offset = 0; offset < labels.length; offset += 70) {
  const batch = labels.slice(offset, offset + 70);
  const query = `SELECT ?label ?item ?article WHERE {
    VALUES ?label { ${batch.map(sparqlString).join(" ")} }
    ?item <http://www.w3.org/2000/01/rdf-schema#label> ?label.
    OPTIONAL { ?article <http://schema.org/about> ?item; <http://schema.org/isPartOf> <https://ru.wikipedia.org/>. }
  }`;
  const response = await fetch("https://query.wikidata.org/sparql", {
    method: "POST",
    headers: {
      accept: "application/sparql-results+json",
      "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
      "user-agent": "MindbattleContentAudit/1.0 (local editorial tool)"
    },
    body: new URLSearchParams({ query }).toString()
  });
  if (!response.ok) throw new Error(`Wikidata ${response.status}`);
  const data = await response.json();
  for (const binding of data.results.bindings) {
    const label = binding.label.value;
    const candidate = {
      title: binding.article?.value ? decodeURIComponent(binding.article.value.split("/").at(-1)).replaceAll("_", " ") : label,
      url: binding.article?.value ?? binding.item.value
    };
    const list = articlesByLabel.get(label) ?? [];
    if (!list.some(({ url }) => url === candidate.url)) list.push(candidate);
    articlesByLabel.set(label, list);
  }
}

const suggestions = questions.map((question) => {
  const correct = question.answers[question.correctIndex];
  const answer = typeof correct === "string" ? correct : correct.text;
  return {
    questionId: question.id,
    topicId: question.topicId,
    prompt: question.prompt,
    correctAnswer: answer,
    previousUrl: question.source.url,
    candidates: articlesByLabel.get(answer) ?? []
  };
});
await writeFile(outputPath, `${JSON.stringify({ generatedOn: "2026-09-02", questions: suggestions.length, suggestions }, null, 2)}\n`, "utf8");
console.log(`Wrote ${outputPath}: ${suggestions.length} questions, ${suggestions.filter(({ candidates }) => candidates.length).length} with candidates`);
