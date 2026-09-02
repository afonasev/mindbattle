import { readdir, readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const topicsDir = resolve(root, "src/content/topics");
const args = process.argv.slice(2);
const outputArgument = args.find((value) => !value.startsWith("--"));
const topicFilter = new Set(args.filter((value) => value.startsWith("--topic=")).map((value) => value.slice("--topic=".length)));
const outputPath = resolve(root, outputArgument ?? "docs/content-audits/source-url-check-2026-09-02.json");
const timeoutMs = Number(process.env.MINDBATTLE_SOURCE_TIMEOUT_MS ?? 15_000);
const concurrency = Number(process.env.MINDBATTLE_SOURCE_CONCURRENCY ?? 12);
const cacheArgument = process.env.MINDBATTLE_SOURCE_CACHE_PATH;
const cachePath = cacheArgument ? resolve(root, cacheArgument) : null;
const files = (await readdir(topicsDir))
  .filter((name) => name.endsWith(".json"))
  .filter((name) => topicFilter.size === 0 || topicFilter.has(name.slice(0, -5)))
  .sort();
const topics = await Promise.all(files.map(async (name) => JSON.parse(await readFile(resolve(topicsDir, name), "utf8"))));
const references = new Map();
for (const topic of topics) {
  for (const question of topic.questions) {
    const list = references.get(question.source.url) ?? [];
    list.push(question.id);
    references.set(question.source.url, list);
  }
}
const urls = [...references.keys()].sort();
const results = new Array(urls.length);
let cachedReachable = 0;
if (cachePath) {
  try {
    const cachedReport = JSON.parse(await readFile(cachePath, "utf8"));
    const cachedByUrl = new Map(
      cachedReport.results
        .filter(({ reachable }) => reachable)
        .map((result) => [result.url, result])
    );
    for (const [index, url] of urls.entries()) {
      const cached = cachedByUrl.get(url);
      if (!cached) continue;
      results[index] = {
        ...cached,
        questionCount: references.get(url).length,
        questionIds: references.get(url)
      };
      cachedReachable += 1;
    }
  } catch (error) {
    console.warn(`Source cache was not used: ${error instanceof Error ? error.message : "unknown error"}`);
  }
}
let cursor = 0;

async function check(url, attempt = 1) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, {
      redirect: "follow",
      signal: controller.signal,
      headers: {
        range: "bytes=0-1023",
        "user-agent": "Mozilla/5.0 MindbattleContentAudit/1.0"
      }
    });
    await response.body?.cancel();
    const genericRedirect = /\/stories\/story\/spotlighting-the-world-factbook-as-we-bid-a-fond-farewell\/?$/u.test(new URL(response.url).pathname);
    return {
      url,
      questionCount: references.get(url).length,
      questionIds: references.get(url),
      status: response.status,
      reachable: (response.ok || [401, 403, 405, 429].includes(response.status)) && !genericRedirect,
      finalUrl: response.url,
      error: genericRedirect ? "GenericRedirect" : null
    };
  } catch (error) {
    if (attempt < 2) return check(url, attempt + 1);
    return {
      url,
      questionCount: references.get(url).length,
      questionIds: references.get(url),
      status: null,
      reachable: false,
      finalUrl: null,
      error: error instanceof Error ? error.name : "UnknownError"
    };
  } finally {
    clearTimeout(timeout);
  }
}

async function worker() {
  while (cursor < urls.length) {
    const index = cursor;
    cursor += 1;
    if (!results[index]) results[index] = await check(urls[index]);
    if ((index + 1) % 100 === 0) console.log(`${index + 1}/${urls.length}`);
  }
}

await Promise.all(Array.from({ length: concurrency }, () => worker()));
const report = {
  schemaVersion: 1,
  checkedOn: "2026-09-02",
  policy: "2xx, 401, 403, 405 and 429 prove a responding endpoint unless it redirects to a known generic retirement page; failures require editorial follow-up and do not rewrite content automatically.",
  execution: {
    timeoutMs,
    concurrency,
    cachedReachable,
    rechecked: results.length - cachedReachable
  },
  totals: {
    uniqueUrls: results.length,
    reachable: results.filter(({ reachable }) => reachable).length,
    unreachable: results.filter(({ reachable }) => !reachable).length,
    definiteDead: results.filter(({ status }) => [404, 410].includes(status)).length,
    networkOrServerLimited: results.filter(({ reachable, status }) => !reachable && ![404, 410].includes(status)).length,
    questionsCovered: [...references.values()].reduce((sum, ids) => sum + ids.length, 0)
  },
  failures: results.filter(({ reachable }) => !reachable),
  results
};
await writeFile(outputPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(`Wrote ${outputPath}: ${report.totals.reachable}/${report.totals.uniqueUrls} reachable`);
