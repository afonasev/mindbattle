import { readdir, readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const topicsDir = resolve(root, "src/content/topics");
const outputPath = resolve(process.argv[2] ?? "/private/tmp/mindbattle-wikidata-answer-descriptions.json");
const files = (await readdir(topicsDir)).filter((name) => name.endsWith(".json")).sort();
const topics = await Promise.all(files.map(async (name) => JSON.parse(await readFile(resolve(topicsDir, name), "utf8"))));
const labels = [...new Set(topics.flatMap((topic) => topic.questions.flatMap((question) => question.answers.map((answer) => typeof answer === "string" ? answer : answer.text))))]
  .filter((label) => label.length <= 80 && !/^\d+(?:[.,–-]\d+)?(?:\s*(?:год|года|лет|%|°C|км|м|см|кг|г|ч|мин|сек))?$/iu.test(label))
  .sort((left, right) => left.localeCompare(right, "ru"));
const descriptions = {};
const batchSize = 80;

function sparqlString(value) {
  return `"${value.replaceAll("\\", "\\\\").replaceAll('"', '\\"').replaceAll("\n", " ")}"@ru`;
}

for (let offset = 0; offset < labels.length; offset += batchSize) {
  const batch = labels.slice(offset, offset + batchSize);
  const query = `SELECT ?label (SAMPLE(?description) AS ?description) WHERE {
    VALUES ?label { ${batch.map(sparqlString).join(" ")} }
    ?item <http://www.w3.org/2000/01/rdf-schema#label> ?label.
    OPTIONAL { ?item <http://schema.org/description> ?description. FILTER(LANG(?description) = "ru") }
  } GROUP BY ?label`;
  const response = await fetch("https://query.wikidata.org/sparql", {
    method: "POST",
    headers: {
      accept: "application/sparql-results+json",
      "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
      "user-agent": "MindbattleContentAudit/1.0 (local editorial tool)"
    },
    body: new URLSearchParams({ query }).toString()
  });
  if (!response.ok) throw new Error(`Wikidata ${response.status} at batch ${offset / batchSize + 1}`);
  const data = await response.json();
  for (const binding of data.results.bindings) {
    if (binding.description?.value) descriptions[binding.label.value] = binding.description.value;
  }
  console.log(`${Math.min(offset + batchSize, labels.length)}/${labels.length}: ${Object.keys(descriptions).length} descriptions`);
}

await writeFile(outputPath, `${JSON.stringify({ fetchedAt: new Date().toISOString(), labels: labels.length, descriptions }, null, 2)}\n`, "utf8");
console.log(`Wrote ${outputPath}`);
