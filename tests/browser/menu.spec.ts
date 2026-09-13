import { expect, test } from "@playwright/test";

test("main menu uses one tagline on every viewport", async ({ page }, testInfo) => {
  await page.goto("/?muted=1");
  await expect(page.getByText("Все решит эрудиция", { exact: true })).toBeVisible();
  await expect(page.getByText("Соберите команды. Остальное решит эрудиция.", { exact: true })).toHaveCount(0);
  await page.screenshot({ path: testInfo.outputPath("main-menu-unified-tagline.png"), fullPage: true });
});

test("local mode uses the same secondary action and opens classic setup", async ({ page }) => {
  await page.goto("/?muted=1");
  const localMode = page.getByRole("button", { name: "На одном устройстве (2–4)", exact: true });
  await expect(localMode).toHaveClass(/secondary-action/);
  await expect(localMode).not.toHaveClass(/primary-action/);
  await localMode.click();
  await expect(page.getByRole("button", { name: "Начать игру", exact: true })).toBeVisible();
});

test("persists presentation volume in the browser", async ({ page }) => {
  await page.goto("/");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await page.getByRole("button", { name: "Настройки", exact: true }).click();
  await page.getByLabel("Громкость").fill("0.4");
  await page.reload();
  await page.getByRole("button", { name: "Настройки", exact: true }).click();
  await expect(page.getByLabel("Громкость")).toHaveValue("0.4");
});
