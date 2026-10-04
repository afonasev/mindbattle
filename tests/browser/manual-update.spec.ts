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
  test.beforeAll(async ({}, info) => {
    test.skip(info.project.name !== "chromium-1280", "Shared worker fixture runs once");
    original = await readFile("dist/sw.js", "utf8");
    server = createServer((request, response) => {
      if (request.url === "/sw.js") {
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
  test("web/mobile button checks, keeps data, applies A→B and reports offline", async ({ page, context }, info) => {
    tag = "A";
    await page.addInitScript(() => {
      // Mute browser QA at the media boundary irrespective of settings schema.
      HTMLMediaElement.prototype.play = async () => {};
      localStorage.setItem("manual-update-loads", String(Number(localStorage.getItem("manual-update-loads") ?? 0) + 1));
    });
    await page.goto(origin);
    await page.evaluate(async () => { await navigator.serviceWorker.ready; });
    await page.reload();
    const update = page.getByRole("button", { name: "Обновить", exact: true });
    await expect(update).toBeVisible();
    await update.click();
    await expect(page.getByRole("status")).toHaveText("Обновлений нет.");
    await page.screenshot({ path: info.outputPath("update-web.png"), fullPage: true });
    await page.setViewportSize({ width: 390, height: 844 });
    await expect(update).toBeVisible();
    expect(await update.evaluate(element => element.getBoundingClientRect().height)).toBeGreaterThanOrEqual(44);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await page.screenshot({ path: info.outputPath("update-mobile.png"), fullPage: true });
    await page.evaluate(() => localStorage.setItem("manual-update-preserved", "saved-data"));
    const loads = await page.evaluate(() => localStorage.getItem("manual-update-loads"));
    tag = "B";
    const reloaded = page.waitForEvent("load");
    await update.click();
    await reloaded;
    await expect(update).toBeVisible();
    expect(await page.evaluate(() => localStorage.getItem("manual-update-loads"))).not.toBe(loads);
    expect(await page.evaluate(() => localStorage.getItem("manual-update-preserved"))).toBe("saved-data");
    expect(await page.evaluate(() => new Promise(resolve => {
      const channel = new MessageChannel();
      channel.port1.onmessage = event => resolve(event.data);
      navigator.serviceWorker.controller!.postMessage("update-test-tag", [channel.port2]);
    }))).toBe("B");
    await context.setOffline(true);
    await update.click();
    await expect(page.getByRole("alert")).toContainText("Не удалось обновить");
    await expect(update).toBeEnabled();
  });
});

for (const legacy of [false, true]) {
  test(`desktop bridge ${legacy ? "legacy" : "manual"} reports an honest result`, async ({ page }) => {
    await page.addInitScript((legacy) => {
      HTMLMediaElement.prototype.play = async () => {};
      let calls = 0;
      (window as any).updateCalls = () => calls;
      (window as any).mindbattleDesktop = {
        version: 1, status: async () => ({ ready: false, shellVersion: "1.0.0" }),
        ...(legacy ? {} : { checkUpdate: async () => { calls++; return { ready: false }; } }),
        onUpdate: () => () => {}, applyUpdate: async () => { throw Error("must not apply current"); },
        safeToUpdate: () => {}, ready: async () => {}, quit: async () => {},
      };
    }, legacy);
    await page.goto("/");
    await page.getByRole("button", { name: "Обновить", exact: true }).click();
    if (legacy) await expect(page.getByRole("alert")).toContainText("проверяются автоматически");
    else {
      await expect(page.getByRole("status")).toHaveText("Обновлений нет.");
      expect(await page.evaluate(() => (window as any).updateCalls())).toBe(1);
    }
  });
}

test("leaving the menu cancels apply after a delayed desktop check", async ({ page }) => {
  await page.addInitScript(() => {
    HTMLMediaElement.prototype.play = async () => {};
    (window as any).applied = 0;
    (window as any).mindbattleDesktop = {
      version: 1, status: async () => ({ ready: false, shellVersion: "1.0.1" }),
      checkUpdate: () => new Promise(resolve => { (window as any).finishCheck = () => resolve({ ready: true }); }),
      onUpdate: () => () => {}, applyUpdate: async () => { (window as any).applied++; return true; },
      safeToUpdate: () => {}, ready: async () => {}, quit: async () => {},
    };
  });
  await page.goto("/");
  await page.getByRole("button", { name: "Обновить", exact: true }).click();
  await expect(page.getByRole("button", { name: "Проверяем…" })).toBeDisabled();
  await page.getByRole("button", { name: "Одиночная игра", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Выберите тему" })).toBeVisible();
  await page.evaluate(() => (window as any).finishCheck());
  expect(await page.evaluate(() => (window as any).applied)).toBe(0);
});
