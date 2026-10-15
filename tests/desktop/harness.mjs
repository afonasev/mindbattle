// Test entry point only; never included in installers.
import { app } from "electron";
import { readFile } from "node:fs/promises";
import path from "node:path";
if (!process.env.MINDBATTLE_DESKTOP_TEST_DIR)
  throw new Error("Isolated test directory required");
app.setPath("userData", process.env.MINDBATTLE_DESKTOP_TEST_DIR);
app.commandLine.appendSwitch("mute-audio");
globalThis.testNetwork = { online: false, events: [], duplicate: false, discoveries: 0 };
try {
  await readFile(
    path.join(process.env.MINDBATTLE_DESKTOP_TEST_DIR, "fixture-online"),
  );
  globalThis.testNetwork.online = true;
} catch {}
const originalFetch = globalThis.fetch;
globalThis.fetch = async (url, options = {}) => {
  if (String(url).startsWith("https://api.github.com/repos/afonasev/mindbattle/releases")) {
    const state = globalThis.testNetwork;
    state.discoveries++;
    if (!state.online) throw new Error("Fixture offline");
    const envelope = JSON.parse(await readFile(path.join(process.env.MINDBATTLE_DESKTOP_TEST_CONTENT, "latest.json")));
    const manifest = JSON.parse(envelope.payload);
    const base = manifest.objectBaseUrl;
    return Response.json([{ tag_name: `content-${manifest.sequence}`, draft: false, prerelease: false,
      published_at: manifest.publishedAt, body: "## Русский\nТестовое обновление\n\n## English\nTest update",
      assets: [{name:"latest.json",state:"uploaded",browser_download_url:`${base}/latest.json`},
        ...manifest.files.map(f => ({name:f.sha256,state:"uploaded",size:f.size,browser_download_url:`${base}/${f.sha256}`}))] }]);
  }
  if (String(url).startsWith("https://mindbattle.afonasev.tech/") || String(url).startsWith("https://afonasev.github.io/mindbattle/") || String(url).startsWith("https://github.com/afonasev/mindbattle/releases/download/")) {
    const state = globalThis.testNetwork;
    if (!state.online) throw new Error("Fixture offline");
    const u = new URL(url);
    if (u.hostname === "afonasev.github.io") u.pathname = u.pathname.slice("/mindbattle".length);
    if (u.hostname === "github.com") u.pathname = u.pathname.endsWith("/latest.json") ? "/desktop/content/latest.json" : `/desktop/content/objects/${u.pathname.split("/").at(-1)}`;
    if (
      u.pathname.startsWith("/api/network/") &&
      process.env.MINDBATTLE_DESKTOP_TEST_API
    )
      return originalFetch(
        `${process.env.MINDBATTLE_DESKTOP_TEST_API}${u.pathname}${u.search}`,
        options,
      );
    if (u.pathname === "/api/match-results") {
      const body = JSON.parse(Buffer.from(options.body).toString());
      state.events.push(body.eventId);
      return Response.json({
        status: state.duplicate ? "duplicate" : "created",
        eventId: body.eventId,
      });
    }
    if (u.pathname.startsWith("/desktop/content/")) {
      const relative = u.pathname.slice("/desktop/content/".length);
      try {
        return new Response(
          await readFile(
            path.join(process.env.MINDBATTLE_DESKTOP_TEST_CONTENT, relative),
          ),
        );
      } catch {
        return new Response("", { status: 404 });
      }
    }
    return new Response("", { status: 503 });
  }
  return originalFetch(url, options);
};
await import("../../desktop/main.mjs");
