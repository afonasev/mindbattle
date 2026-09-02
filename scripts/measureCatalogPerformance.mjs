import { spawn } from "node:child_process";
import { gzipSync } from "node:zlib";
import { readFile, stat, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { chromium } from "@playwright/test";

const root = resolve(import.meta.dirname, "..");
const port = Number(process.env.MINDBATTLE_PERFORMANCE_PORT ?? 4191);
const outputPath = resolve(root, "docs/content-audits/performance-gate-2026-09-02.json");
const feedbackPath = `/private/tmp/mindbattle-performance-feedback-${process.pid}.ndjson`;
const startedAt = performance.now();
const server = spawn(process.execPath, ["server/index.mjs"], {
  cwd: root,
  env: {
    ...process.env,
    MINDBATTLE_PORT: String(port),
    MINDBATTLE_FEEDBACK_PATH: feedbackPath
  },
  stdio: ["ignore", "pipe", "pipe"]
});

let stdout = "";
let stderr = "";
server.stdout.on("data", (chunk) => { stdout += chunk; });
server.stderr.on("data", (chunk) => { stderr += chunk; });

try {
  const deadline = Date.now() + 30_000;
  while (!stdout.includes("Mindbattle:")) {
    if (server.exitCode !== null) throw new Error(`Server exited ${server.exitCode}: ${stderr}`);
    if (Date.now() > deadline) throw new Error(`Server startup timeout: ${stdout}\n${stderr}`);
    await new Promise((resolveWait) => setTimeout(resolveWait, 10));
  }
  const serverReadyMs = Math.round((performance.now() - startedAt) * 10) / 10;
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
    const navigationStartedAt = performance.now();
    await page.goto(`http://127.0.0.1:${port}`, { waitUntil: "networkidle" });
    const pageReadyMs = Math.round((performance.now() - navigationStartedAt) * 10) / 10;
    const cdp = await page.context().newCDPSession(page);
    await cdp.send("Performance.enable");
    const { metrics } = await cdp.send("Performance.getMetrics");
    const metric = Object.fromEntries(metrics.map(({ name, value }) => [name, value]));
    const html = await readFile(resolve(root, "dist/index.html"), "utf8");
    const jsFile = html.match(/<script[^>]+src="\/([^"]+\.js)"/u)?.[1];
    const cssFiles = [...html.matchAll(/<link[^>]+href="\/([^"]+\.css)"/gu)].map((match) => match[1]);
    if (!jsFile) throw new Error("Production JS asset not found in dist/index.html");
    const assetPaths = [jsFile, ...cssFiles];
    const assets = [];
    for (const file of assetPaths) {
      const path = resolve(root, "dist", file);
      const bytes = await readFile(path);
      assets.push({ file, bytes: (await stat(path)).size, gzipBytes: gzipSync(bytes).length });
    }
    const report = {
      schemaVersion: 1,
      measuredOn: "2026-09-02",
      serverReadyMs,
      pageReadyMs,
      chromium: {
        viewport: "1920x1080",
        jsHeapUsedBytes: metric.JSHeapUsedSize,
        jsHeapTotalBytes: metric.JSHeapTotalSize,
        documents: metric.Documents,
        nodes: metric.Nodes,
        layoutObjects: metric.LayoutObjects
      },
      productionAssets: assets
    };
    await writeFile(outputPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
    console.log(JSON.stringify(report, null, 2));
  } finally {
    await browser.close();
  }
} finally {
  server.kill("SIGTERM");
}
