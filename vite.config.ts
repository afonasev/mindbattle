import { defineConfig, type Plugin } from "vite";
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

const packageVersion = JSON.parse(readFileSync(new URL("./package.json", import.meta.url), "utf8")).version;
const publicationInput = process.env.MINDBATTLE_PUBLISHED_AT;
if (publicationInput && (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/.test(publicationInput) || !Number.isFinite(Date.parse(publicationInput)))) {
  throw new Error("MINDBATTLE_PUBLISHED_AT must be a UTC ISO timestamp");
}
const publishedAt = publicationInput ? new Date(publicationInput).toISOString() : null;
let releaseVersion = "";
const updateVersionPlugin: Plugin = {
  name: "game-update-version",
  generateBundle(_options, bundle) {
    const hash = createHash("sha256").update(publishedAt ?? "unpublished");
    for (const [name, output] of Object.entries(bundle).sort(([a], [b]) => a.localeCompare(b))) {
      hash.update(name).update(output.type === "chunk" ? output.code : output.source);
    }
    const version = `${packageVersion}+${hash.digest("hex").slice(0, 8)}`;
    releaseVersion = version;
    this.emitFile({ type: "asset", fileName: "game-version.json", source: JSON.stringify({ version, publishedAt }) });
    this.emitFile({ type: "asset", fileName: "update-version.js", source: `self.addEventListener("message", event => { if (event.data === "mindbattle:update-version") event.ports[0]?.postMessage(${JSON.stringify(version)}); });` });
  },
  writeBundle(options) {
    // Stamp the loaded document before Workbox precaches it. No latest-version fetch.
    const file = resolve(options.dir!, "index.html");
    const html = readFileSync(file, "utf8");
    writeFileSync(file, html.replace("</head>", `<meta name="mindbattle:version" content="${releaseVersion}"><meta name="mindbattle:published-at" content="${publishedAt ?? ""}"></head>`));
  }
};

const appIcons = [
  { src: "/icons/mindbattle-192.png", sizes: "192x192", type: "image/png", purpose: "any" },
  { src: "/icons/mindbattle-512.png", sizes: "512x512", type: "image/png", purpose: "any maskable" }
];

export default defineConfig({
  plugins: [react(), updateVersionPlugin, VitePWA({ registerType: "prompt", injectRegister: false, manifest: { name: "Mindbattle — интеллектуальная битва", short_name: "Mindbattle", lang: "ru", theme_color: "#07101f", background_color: "#07101f", display: "standalone", icons: appIcons }, workbox: { importScripts: ["update-version.js"], navigateFallback: "/index.html", navigateFallbackDenylist: [/^\/desktop\//], globPatterns: ["**/*.{js,css,html,ico,png,svg,json,wav,mp3,woff2}"], maximumFileSizeToCacheInBytes: 20 * 1024 * 1024 } })],
  server: {
    host: "127.0.0.1",
    port: 4173,
    strictPort: true
  },
  preview: {
    host: "127.0.0.1",
    port: 4173,
    strictPort: true
  }
});
