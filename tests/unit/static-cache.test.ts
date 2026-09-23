import { mkdtemp, mkdir, rm, writeFile } from "node:fs/promises";
import { createServer } from "node:http";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import { serveStatic } from "../../server/static.mjs";

const cleanup: Array<() => Promise<void>> = [];
afterEach(async () => {
  await Promise.all(cleanup.splice(0).map((dispose) => dispose()));
});

async function fixture() {
  const dist = await mkdtemp(join(tmpdir(), "mindbattle-static-cache-"));
  await mkdir(join(dist, "assets"));
  await writeFile(join(dist, "index.html"), "<html>first</html>");
  await writeFile(join(dist, "sw.js"), "self.version = 1;");
  await writeFile(join(dist, "assets", "App-AAAA1234.js"), "const version = 1;");
  const server = createServer((request, response) => {
    void serveStatic(request, response, dist).catch((error: unknown) => {
      response.writeHead(500);
      response.end(String(error));
    });
  });
  await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
  cleanup.push(async () => {
    await new Promise<void>((resolve) => server.close(() => resolve()));
    await rm(dist, { recursive: true, force: true });
  });
  const address = server.address();
  if (!address || typeof address === "string") throw new Error("Unexpected server address");
  return { dist, base: `http://127.0.0.1:${address.port}` };
}

describe("production static cache", () => {
  it("keeps versioned assets immutable while revalidating HTML and fallback routes", async () => {
    const { base } = await fixture();
    const asset = await fetch(`${base}/assets/App-AAAA1234.js`);
    expect(asset.status).toBe(200);
    expect(asset.headers.get("cache-control")).toBe("public, max-age=31536000, immutable");
    expect(await asset.text()).toBe("const version = 1;");

    const html = await fetch(base);
    const etag = html.headers.get("etag");
    expect(html.headers.get("cache-control")).toBe("no-cache");
    expect(etag).toMatch(/^W\//);
    if (!etag) throw new Error("Missing ETag");
    expect((await fetch(base, { headers: { "If-None-Match": etag } })).status).toBe(304);
    expect(await (await fetch(base, { headers: { "If-None-Match": etag } })).text()).toBe("");

    for (const path of ["/network", "/assets/missing-AAAA1234.js"]) {
      const fallback = await fetch(`${base}${path}`);
      expect(fallback.headers.get("cache-control")).toBe("no-cache");
      expect(fallback.headers.get("etag")).toBe(etag);
    }
  });

  it("sends changed stable resources while leaving new hashed URLs independent", async () => {
    const { base, dist } = await fixture();
    const oldHtml = await fetch(base);
    const oldEtag = oldHtml.headers.get("etag");
    if (!oldEtag) throw new Error("Missing ETag");
    await writeFile(join(dist, "index.html"), "<html>other</html>");
    const changedHtml = await fetch(base, { headers: { "If-None-Match": oldEtag } });
    expect(changedHtml.status).toBe(200);
    expect(changedHtml.headers.get("etag")).not.toBe(oldEtag);
    expect(await changedHtml.text()).toBe("<html>other</html>");

    const worker = await fetch(`${base}/sw.js`);
    const workerEtag = worker.headers.get("etag");
    if (!workerEtag) throw new Error("Missing ETag");
    expect(worker.headers.get("cache-control")).toBe("no-cache");
    expect((await fetch(`${base}/sw.js`, { headers: { "If-None-Match": workerEtag } })).status).toBe(304);
    await writeFile(join(dist, "sw.js"), "self.version = 2;");
    expect((await fetch(`${base}/sw.js`, { headers: { "If-None-Match": workerEtag } })).status).toBe(200);

    await writeFile(join(dist, "assets", "App-BBBB1234.js"), "const version = 2;");
    const newAsset = await fetch(`${base}/assets/App-BBBB1234.js`);
    expect(newAsset.status).toBe(200);
    expect(newAsset.headers.get("cache-control")).toContain("immutable");
    expect(await newAsset.text()).toBe("const version = 2;");
  });
});
