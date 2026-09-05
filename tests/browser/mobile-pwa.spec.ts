import { expect, test } from "@playwright/test";

test.use({ viewport: { width: 390, height: 844 } });

test("mobile menu exposes solo only and has an install manifest", async ({ page }, testInfo) => {
  await page.goto("/");
  await expect(page.getByRole("button", { name: "Соло-забег" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Начать игру" })).toBeHidden();
  await expect(page.locator('link[rel="manifest"]')).toHaveCount(1);
  expect(await page.locator("body").evaluate((body) => document.documentElement.scrollWidth <= window.innerWidth && body.scrollWidth <= window.innerWidth)).toBe(true);
  await page.getByRole("button", { name: "Соло-забег" }).click();
  await expect(page.getByRole("heading", { name: "Выберите тему" })).toBeVisible();
  expect(await page.locator("body").evaluate((body) => document.documentElement.scrollWidth <= window.innerWidth && body.scrollWidth <= window.innerWidth)).toBe(true);
  await page.screenshot({ path: testInfo.outputPath("mindbattle-mobile-solo-topic.png"), fullPage: true });
});
