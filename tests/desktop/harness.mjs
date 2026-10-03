// Test entry point only; never included in installers.
import { app } from "electron";
import { readFile } from "node:fs/promises";
import path from "node:path";
if (!process.env.MINDBATTLE_DESKTOP_TEST_DIR)
  throw new Error("Isolated test directory required");
app.setPath("userData", process.env.MINDBATTLE_DESKTOP_TEST_DIR);
globalThis.testNetwork = { online: false, events: [], duplicate: false };
try {
  await readFile(
    path.join(process.env.MINDBATTLE_DESKTOP_TEST_DIR, "fixture-online"),
  );
  globalThis.testNetwork.online = true;
} catch {}
const originalFetch = globalThis.fetch;
globalThis.fetch = async (url, options = {}) => {
  if (String(url).startsWith("https://mindbattle.afonasev.tech/")) {
    const state = globalThis.testNetwork;
    if (!state.online) throw new Error("Fixture offline");
    const u = new URL(url);
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
