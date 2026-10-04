import { expect, test } from "@playwright/test";
import { readFile } from "node:fs/promises";
import { createServer, type Server } from "node:http";
import { resolve } from "node:path";
import { serveStatic } from "../../server/static.mjs";

// The real generated worker participates; the small tag identifies A/B workers.
test.describe("real PWA update", () => {
  let original: string;
  let server: Server;
  let origin: string;
  let tag = "A";
  let offline = false;
  test.beforeAll(async ({}, info) => {
    test.skip(info.project.name !== "chromium-1280", "Shared worker fixture runs once");
    original = await readFile("dist/sw.js", "utf8");
    server = createServer((request, response) => {
      if (offline) { response.writeHead(503); response.end(); return; }
      if (request.url === "/update-version.js") {
        response.writeHead(200, { "content-type": "text/javascript", "cache-control": "no-store" });
        response.end(`self.addEventListener('message', event => { if (event.data === 'mindbattle:update-version') event.ports[0].postMessage('2.0.0-${tag}'); });`);
      } else if (request.url === "/sw.js") {
        response.writeHead(200, { "content-type": "text/javascript", "cache-control": "no-store" });
        response.end(`${original}\nself.addEventListener('message', event => { if (event.data === 'update-test-tag') event.ports[0].postMessage('${tag}'); });\n`);
      } else void serveStatic(request, response, resolve("dist")).catch(() => { response.writeHead(500); response.end(); });
    });
    await new Promise<void>(done => server.listen(0, "127.0.0.1", done));
    origin = `http://127.0.0.1:${(server.address() as { port: number }).port}`;
  });
  test.afterAll(async ({}, info) => {
    if (info.project.name === "chromium-1280" && server) {
      server.closeAllConnections();
      await new Promise<void>(done => server.close(() => done()));
    }
  });
  test("web/mobile hides current, offers a ready update and applies A→B offline", async ({ page, context }, info) => {
    tag = "A";
    offline = false;
    await page.addInitScript(() => {
      // Mute browser QA at the media boundary irrespective of settings schema.
      HTMLMediaElement.prototype.play = async () => {};
      localStorage.setItem("manual-update-loads", String(Number(localStorage.getItem("manual-update-loads") ?? 0) + 1));
    });
    await page.goto(origin);
    await page.evaluate(async () => { await navigator.serviceWorker.ready; });
    await page.reload();
    await expect(page.getByRole("button", { name: "Одиночная игра", exact: true })).toBeVisible();
    const update = page.getByRole("button", { name: "Появилось новое обновление", exact: true });
    await expect(update).toBeHidden();
    const footer = page.getByRole("contentinfo", { name: "Версия приложения" });
    const currentVersion = await footer.innerText();
    await expect(footer).toContainText("Ещё не опубликована");
    await page.screenshot({ path: info.outputPath("update-web-hidden.png"), fullPage: true });
    tag = "B";
    await page.evaluate(async () => { await (await navigator.serviceWorker.getRegistration())!.update(); });
    await expect(update).toBeVisible();
    await expect(update).toContainText("Версия 2.0.0-B");
    expect(await footer.innerText()).toBe(currentVersion);
    await page.screenshot({ path: info.outputPath("update-web.png"), fullPage: true });
    await page.setViewportSize({ width: 390, height: 844 });
    expect(await update.evaluate(element => element.getBoundingClientRect().height)).toBeGreaterThanOrEqual(44);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await page.screenshot({ path: info.outputPath("update-mobile.png"), fullPage: true });
    await page.evaluate(() => localStorage.setItem("manual-update-preserved", "saved-data"));
    const loads = await page.evaluate(() => localStorage.getItem("manual-update-loads"));
    offline = true; // Service-worker requests bypass Playwright page offline emulation.
    tag = "C"; // The server advanced, but the button must still describe waiting B.
    await context.setOffline(true);
    await expect(update).toContainText("Версия 2.0.0-B");
    const reloaded = page.waitForEvent("load");
    await update.click();
    await reloaded;
    await expect(page.getByRole("button", { name: "Одиночная игра", exact: true })).toBeVisible();
    await expect(update).toBeHidden();
    expect(await footer.innerText()).toBe(currentVersion);
    expect(await page.evaluate(() => localStorage.getItem("manual-update-loads"))).not.toBe(loads);
    expect(await page.evaluate(() => localStorage.getItem("manual-update-preserved"))).toBe("saved-data");
    expect(await page.evaluate(() => new Promise(resolve => {
      const channel = new MessageChannel();
      channel.port1.onmessage = event => resolve(event.data);
      navigator.serviceWorker.controller!.postMessage("update-test-tag", [channel.port2]);
    }))).toBe("B");
    await page.screenshot({ path: info.outputPath("update-mobile-hidden.png"), fullPage: true });
  });
});

for (const legacy of [false, true]) {
  test(`desktop ${legacy ? "legacy" : "manual"} hides until discovery and retains retry after apply error`, async ({ page }) => {
    await page.addInitScript((legacy) => {
      HTMLMediaElement.prototype.play = async () => {};
      (window as any).mindbattleDesktop = {
        version: 1, status: async () => ({ ready: false, shellVersion: "1.0.1" }),
        ...(legacy ? {} : { checkUpdate: async () => ({ ready: false }) }),
        onUpdate: (notify: (ready: boolean) => void) => { (window as any).notifyUpdate = notify; return () => {}; },
        applyUpdate: async () => false, safeToUpdate: () => {}, ready: async () => {}, quit: async () => {},
      };
    }, legacy);
    await page.goto("/");
    const update = page.getByRole("button", { name: "Появилось новое обновление", exact: true });
    await expect(page.getByRole("button", { name: "Одиночная игра", exact: true })).toBeVisible();
    await expect(update).toBeHidden();
    await page.evaluate(() => (window as any).notifyUpdate(true, "1.2.3+abcdef12"));
    await expect(update).toBeVisible();
    await expect(update).toContainText("Версия 1.2.3");
    await expect(update).not.toContainText("abcdef12");
    await update.click();
    await expect(page.getByRole("alert")).toContainText("Не удалось обновить");
    await expect(update).toBeEnabled();
    await page.evaluate(() => (window as any).notifyUpdate(false));
    await expect(update).toBeHidden();
  });
}
