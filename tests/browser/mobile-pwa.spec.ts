import { expect, test } from "@playwright/test";

test.use({ viewport: { width: 390, height: 844 } });

test("mobile menu exposes solo only and has an install manifest", async ({ page }, testInfo) => {
  await page.goto("/");
  await expect(page.getByRole("button", { name: "Соло-забег" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Начать игру" })).toBeHidden();
  await expect(page.getByText("Все решит эрудиция")).toBeVisible();
  await expect(page.getByText("Соберите команды. Остальное решит эрудиция.")).toBeHidden();
  await expect(page.getByText("Локально · Offline-first · один общий экран")).toBeHidden();
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
  const soloButton = page.getByRole("button", { name: "Соло-забег" });
  const recordsButton = page.getByRole("button", { name: "Рекорды" });
  const soloBox = await soloButton.boundingBox();
  const recordsBox = await recordsButton.boundingBox();
  expect(recordsBox?.y).toBeGreaterThan((soloBox?.y ?? 0) + (soloBox?.height ?? 0));
  expect(await page.locator("body").evaluate((body) => document.documentElement.scrollWidth <= window.innerWidth && body.scrollWidth <= window.innerWidth)).toBe(true);
  await page.screenshot({ path: testInfo.outputPath("mindbattle-mobile-menu-actions.png"), fullPage: true });
  await recordsButton.click();
  await expect(page.getByRole("heading", { name: "Рекорды" })).toBeVisible();
  await expect(page.getByText("Пока нет сохранённых результатов.")).toBeVisible();
  expect(await page.locator("body").evaluate((body) => document.documentElement.scrollWidth <= window.innerWidth && body.scrollWidth <= window.innerWidth)).toBe(true);
  await page.waitForTimeout(300);
  await page.screenshot({ path: testInfo.outputPath("mindbattle-mobile-records.png"), fullPage: true });
  await page.getByRole("button", { name: "Назад" }).click();
  await soloButton.click();
  await expect(page.getByRole("heading", { name: "Выберите тему" })).toBeVisible();
  await page.waitForTimeout(300);
  expect(await page.locator("body").evaluate((body) => document.documentElement.scrollWidth <= window.innerWidth && body.scrollWidth <= window.innerWidth)).toBe(true);
  await page.screenshot({ path: testInfo.outputPath("mindbattle-mobile-solo-topic.png"), fullPage: true });
});
