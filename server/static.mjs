import { createHash } from "node:crypto";
import { createReadStream } from "node:fs";
import { readFile, stat } from "node:fs/promises";
import { extname, join, normalize, relative, resolve, sep } from "node:path";

const mime = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".woff2": "font/woff2", ".svg": "image/svg+xml", ".png": "image/png", ".webmanifest": "application/manifest+json" };
const immutableCache = "public, max-age=31536000, immutable";
const revalidateCache = "no-cache";

function versionedAsset(dist, target) {
  return /^assets\/[^/]+-[A-Za-z0-9_-]{8,}\.[a-z0-9]+$/.test(relative(dist, target).split(sep).join("/"));
}

function matchesEtag(header, etag) {
  if (!header) return false;
  const value = Array.isArray(header) ? header.join(",") : header;
  return value.split(",").some((candidate) => {
    const trimmed = candidate.trim();
    return trimmed === "*" || trimmed.replace(/^W\//, "") === etag.replace(/^W\//, "");
  });
}

export async function serveStatic(request, response, distRoot) {
  const dist = resolve(distRoot);
  const pathname = decodeURIComponent(new URL(request.url, "http://local").pathname);
  const relativePath = normalize(pathname).replace(/^[/\\]+/, "");
  let target = resolve(dist, relativePath || "index.html");
  if (!target.startsWith(`${dist}${sep}`)) {
    response.writeHead(404, { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" });
    response.end(JSON.stringify({ error: "Not found" }));
    return;
  }
  try {
    if ((await stat(target)).isDirectory()) target = join(target, "index.html");
  } catch {
    target = join(dist, "index.html");
  }

  const headers = {
    "content-type": `${mime[extname(target)] ?? "application/octet-stream"}; charset=utf-8`,
    "cache-control": versionedAsset(dist, target) ? immutableCache : revalidateCache
  };
  if (headers["cache-control"] === revalidateCache) {
    const digest = createHash("sha256").update(await readFile(target)).digest("hex");
    headers.etag = `W/"${digest}"`;
    if ((request.method === "GET" || request.method === "HEAD") && matchesEtag(request.headers["if-none-match"], headers.etag)) {
      response.writeHead(304, headers);
      response.end();
      return;
    }
  }
  response.writeHead(200, headers);
  if (request.method === "HEAD") response.end();
  else createReadStream(target).pipe(response);
}
