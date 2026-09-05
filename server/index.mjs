import { createReadStream } from "node:fs";
import { readFile, readdir, stat } from "node:fs/promises";
import { createServer } from "node:http";
import { extname, join, normalize, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createFeedbackStore } from "./feedbackStore.mjs";

const projectRoot = resolve(fileURLToPath(new URL("..", import.meta.url)));
const dev = process.argv.includes("--dev");
const host = process.env.MINDBATTLE_HOST ?? "127.0.0.1";
const port = Number(process.env.MINDBATTLE_PORT ?? 4173);
const dataPath = resolve(projectRoot, process.env.MINDBATTLE_FEEDBACK_PATH ?? "data/difficulty-feedback.ndjson");
const catalogRevision = "mindbattle-questions-2026-09-02-r3";

async function loadQuestions() {
  const dir = join(projectRoot, "src/content/topics");
  const map = new Map();
  for (const name of await readdir(dir)) {
    if (!name.endsWith(".json")) continue;
    const topic = JSON.parse(await readFile(join(dir, name), "utf8"));
    for (const question of topic.questions) map.set(question.id, question.difficulty);
  }
  return map;
}

const store = await createFeedbackStore({ filePath: dataPath, questions: await loadQuestions(), catalogRevision });
let vite = null;
if (dev) {
  const { createServer: createViteServer } = await import("vite");
  vite = await createViteServer({ root: projectRoot, server: { middlewareMode: true }, appType: "spa" });
}

function json(response, status, body) {
  response.writeHead(status, { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" });
  response.end(JSON.stringify(body));
}

async function readJson(request) {
  const chunks = [];
  let size = 0;
  for await (const chunk of request) {
    size += chunk.length;
    if (size > 16_384) throw Object.assign(new Error("Payload слишком велик"), { status: 413 });
    chunks.push(chunk);
  }
  try { return JSON.parse(Buffer.concat(chunks).toString("utf8")); }
  catch { throw Object.assign(new Error("Некорректный JSON"), { status: 400 }); }
}

const mime = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".woff2": "font/woff2", ".svg": "image/svg+xml", ".png": "image/png", ".webmanifest": "application/manifest+json" };
async function serveStatic(request, response) {
  const dist = join(projectRoot, "dist");
  const pathname = decodeURIComponent(new URL(request.url, "http://local").pathname);
  const relative = normalize(pathname).replace(/^[/\\]+/, "");
  let target = resolve(dist, relative || "index.html");
  if (!target.startsWith(`${dist}/`)) return json(response, 404, { error: "Not found" });
  try {
    if ((await stat(target)).isDirectory()) target = join(target, "index.html");
  } catch { target = join(dist, "index.html"); }
  response.writeHead(200, { "content-type": `${mime[extname(target)] ?? "application/octet-stream"}; charset=utf-8` });
  createReadStream(target).pipe(response);
}

const server = createServer(async (request, response) => {
  try {
    const url = new URL(request.url, "http://local");
    if (url.pathname === "/api/difficulty-feedback" && request.method === "POST") {
      const result = await store.append(await readJson(request));
      if (result.status === "invalid") return json(response, 400, result);
      if (result.status === "conflict") return json(response, 409, result);
      return json(response, result.status === "created" ? 201 : 200, result);
    }
    if (url.pathname.startsWith("/api/")) return json(response, 404, { error: "Not found" });
    if (vite) return vite.middlewares(request, response, () => json(response, 404, { error: "Not found" }));
    return serveStatic(request, response);
  } catch (error) {
    return json(response, error?.status ?? 500, { error: error instanceof Error ? error.message : "Server error" });
  }
});

server.listen(port, host, () => {
  console.log(`Mindbattle: http://${host}:${port}`);
  console.log(`Difficulty feedback: ${store.filePath}`);
});
