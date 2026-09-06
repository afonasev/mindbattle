import { expect, test } from "@playwright/test";

test.use({ viewport: { width: 390, height: 844 } });

test("mobile menu exposes solo only and has an install manifest", async ({ page }, testInfo) => {
  await page.goto("/");
  await expect(page.getByRole("button", { name: "Соло-забег" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Начать игру" })).toBeHidden();
  await expect(page.locator('link[rel="manifest"]')).toHaveCount(1);
  await expect(page.locator('link[rel="apple-touch-icon"]')).toHaveAttribute("href", "/icons/apple-touch-icon.png");
  await expect(page.locator('link[rel="apple-touch-icon"]')).toHaveAttribute("sizes", "180x180");
  const manifest = await (await page.request.get("/manifest.webmanifest")).json();
  expect(manifest.lang).toBe("ru");
  expect(manifest.icons).toEqual([
    { src: "/icons/mindbattle-192.png", sizes: "192x192", type: "image/png", purpose: "any" },
    { src: "/icons/mindbattle-512.png", sizes: "512x512", type: "image/png", purpose: "any maskable" }
  ]);
  expect((await page.request.get("/icons/apple-touch-icon.png")).ok()).toBe(true);
  expect(await page.locator("body").evaluate((body) => document.documentElement.scrollWidth <= window.innerWidth && body.scrollWidth <= window.innerWidth)).toBe(true);
  await page.getByRole("button", { name: "Соло-забег" }).click();
  await expect(page.getByRole("heading", { name: "Выберите тему" })).toBeVisible();
  await page.waitForTimeout(300);
  expect(await page.locator("body").evaluate((body) => document.documentElement.scrollWidth <= window.innerWidth && body.scrollWidth <= window.innerWidth)).toBe(true);
  await page.screenshot({ path: testInfo.outputPath("mindbattle-mobile-solo-topic.png"), fullPage: true });
});
