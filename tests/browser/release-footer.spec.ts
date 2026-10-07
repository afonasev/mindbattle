import { expect, test } from "@playwright/test";

// Published-document fixture: the separate real-worker test covers offline precache.
test.use({ serviceWorkers: "block" });

for (const desktop of [false, true]) {
  test(`current published release footer on ${desktop ? "desktop" : "web/mobile"}`, async ({ page }, info) => {
    await page.addInitScript((desktop) => {
      HTMLMediaElement.prototype.play = async () => {};
      if (desktop) (window as any).mindbattleDesktop = {
        version: 1, status: async () => ({ ready: false, shellVersion: "1.0.2" }),
        onUpdate: () => () => {}, ready: async () => {}, safeToUpdate: () => {},
      };
    }, desktop);
    // Simulate a published document; keep the actual running JS/CSS intact.
    await page.route("**/*", async route => {
      if (!route.request().isNavigationRequest()) return route.continue();
      const response = await route.fetch();
      const body = (await response.text())
        .replace(/(<meta name="mindbattle:version" content=")[^"]*/, "$1" + "0.1.0+published")
        .replace(/(<meta name="mindbattle:published-at" content=")[^"]*/, "$1" + "2026-10-04T07:00:00.000Z");
      await route.fulfill({ response, body });
    });
    await page.goto("/");
    // Wait for the actual lazy-loaded application, then verify the footer contract.
    await expect(page.getByText("Загружаем Mindbattle…", { exact: true })).toBeHidden({ timeout: 30_000 });
    const footer = page.getByRole("contentinfo", { name: "Версия приложения" });
    await expect(footer).toContainText("Версия 0.1.0");
    await expect(footer).not.toContainText("+published");
    expect(await page.locator('meta[name="mindbattle:version"]').getAttribute("content")).toBe("0.1.0+published");
    await expect(footer).toContainText("Опубликована");
    await expect.poll(() => page.evaluate(() => Math.abs(parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--app-footer-height")) - document.querySelector("footer")!.getBoundingClientRect().height))).toBeLessThanOrEqual(1);
    await expect(footer.locator("time")).toHaveAttribute("datetime", "2026-10-04T07:00:00.000Z");
    await expect(footer).toContainText("04.10.2026");
    await page.screenshot({ path: info.outputPath(`footer-${desktop ? "desktop" : "web"}.png`), fullPage: true });
    if (!desktop) {
      await page.setViewportSize({ width: 390, height: 844 });
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
      await page.screenshot({ path: info.outputPath("footer-mobile.png"), fullPage: true });
      await page.goto("/network");
      await expect(footer).toContainText("Версия 0.1.0");
      await expect(footer.locator("time")).toHaveAttribute("datetime", "2026-10-04T07:00:00.000Z");
    }
  });
}
