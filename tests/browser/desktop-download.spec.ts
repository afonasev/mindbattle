import { expect, test } from "@playwright/test";
import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";

// Serve small installer fixtures through the real production static server so
// the active service worker participates (page.route would bypass that path).
const fixtureRoot = path.resolve("dist/desktop");
const installer = Buffer.from("MZ Mindbattle download regression fixture");
const installerUrl = "/desktop/installers/Mindbattle-test-win-x64.exe";

// The fixtures share one production server. Run once rather than concurrently
// for both viewport projects; download handling does not depend on viewport.
test.beforeAll(async ({}, testInfo) => {
  test.skip(testInfo.project.name !== "chromium-1280", "Covered by chromium-1280");
  await mkdir(path.join(fixtureRoot, "installers"), { recursive: true });
  await writeFile(path.join(fixtureRoot, "installers/Mindbattle-test-win-x64.exe"), installer);
  await writeFile(path.join(fixtureRoot, "downloads.json"), JSON.stringify({
    windows: { url: installerUrl },
  }));
  await writeFile(path.join(fixtureRoot, "download-check.html"),
    `<a href="${installerUrl}">Installer</a>`);
});

test.afterAll(async ({}, testInfo) => {
  if (testInfo.project.name !== "chromium-1280") return;
  await rm(fixtureRoot, { recursive: true, force: true });
});

test("Windows installer downloads with an active PWA without replacing the game", async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(navigator, "platform", { get: () => "Win32" });
  });
  await page.goto("/");
  await page.evaluate(async () => { await navigator.serviceWorker.ready; });
  await page.reload();
  await expect.poll(() => page.evaluate(() => !!navigator.serviceWorker.controller)).toBe(true);
  const link = page.getByRole("link", { name: "Скачать игру" });
  await expect(link).toHaveAttribute("href", installerUrl);
  const downloaded = page.waitForEvent("download", { timeout: 5000 });
  await link.click();
  const download = await downloaded;
  expect(download.suggestedFilename()).toBe("Mindbattle-test-win-x64.exe");
  expect(await readFile((await download.path())!)).toEqual(installer);
  await expect(page).toHaveURL(/\/$/);
  await expect(page.getByRole("button", { name: "Одиночная игра" })).toBeVisible();

  // A plain navigation must also reach the installer, without the download
  // attribute: verify the service worker exclusion independently of the button.
  await page.goto("/desktop/download-check.html");
  const directDownload = page.waitForEvent("download", { timeout: 5000 });
  await page.getByRole("link", { name: "Installer", exact: true }).click();
  expect(await readFile((await (await directDownload).path())!)).toEqual(installer);
});
