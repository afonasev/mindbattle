import { readFile, realpath } from "node:fs/promises";
import path from "node:path";
import { validPath } from "./content.mjs";
export const APP_ORIGIN = "mindbattle://game";
const mime = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript",
  ".css": "text/css",
  ".json": "application/json",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".ico": "image/x-icon",
  ".wav": "audio/wav",
  ".mp3": "audio/mpeg",
  ".woff2": "font/woff2",
};
const CSP =
  "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; media-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-src 'none'";
export function createHandler({ directory, origin, fetcher }) {
  return async (request) => {
    try {
      const url = new URL(request.url);
      if (url.protocol !== "mindbattle:" || url.host !== "game")
        return new Response("Forbidden", { status: 403 });
      const pathname = decodeURIComponent(url.pathname);
      if (pathname.startsWith("/api/")) {
        if (
          !/^\/api\/(?:match-results|difficulty-feedback|network\/[a-z-]+)$/.test(
            pathname,
          ) ||
          !["GET", "POST"].includes(request.method)
        )
          return new Response("Not found", { status: 404 });
        const headers = new Headers();
        for (const key of ["authorization", "content-type", "accept"])
          if (request.headers.has(key))
            headers.set(key, request.headers.get(key));
        // Only this fixed upstream may receive game credentials. Renderer Origin is not forwarded.
        const upstream = await fetcher(`${origin}${pathname}${url.search}`, {
          method: request.method,
          headers,
          body:
            request.method === "POST" ? await request.arrayBuffer() : undefined,
          signal: request.signal,
          redirect: "error",
          credentials: "omit",
        });
        return new Response(upstream.body, {
          status: upstream.status,
          headers: {
            "content-type":
              upstream.headers.get("content-type") || "application/json",
            "cache-control": "no-store",
          },
        });
      }
      if (request.method !== "GET")
        return new Response("Method not allowed", { status: 405 });
      let relative =
        pathname === "/" || pathname === "/network"
          ? "index.html"
          : pathname.slice(1);
      if (!validPath(relative) || relative === "release.json")
        return new Response("Not found", { status: 404 });
      const root = await realpath(directory());
      const file = await realpath(path.join(root, relative));
      if (!file.startsWith(`${root}${path.sep}`))
        return new Response("Forbidden", { status: 403 });
      return new Response(await readFile(file), {
        headers: {
          "content-type":
            mime[path.extname(file)] || "application/octet-stream",
          "content-security-policy": CSP,
          "cache-control": "no-store",
        },
      });
    } catch {
      return new Response("Unavailable", { status: 503 });
    }
  };
}
