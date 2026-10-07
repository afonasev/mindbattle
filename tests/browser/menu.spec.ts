import { createNetworkGame, selectNetworkGame } from "./network-lobby-helpers";
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
  await page.getByLabel("Громкость музыки").fill("0.4");
  await page.reload();
  await page.getByRole("button", { name: "Настройки", exact: true }).click();
  await expect(page.getByLabel("Громкость музыки")).toHaveValue("0.4");
});

for (const width of [1280, 390]) {
  test(`menu navigation is consistent at ${width}px`, async ({ page }, testInfo) => {
    await page.setViewportSize({ width, height: 844 });
    await page.goto("/?muted=1");
    await page.getByRole("button", { name: "Настройки", exact: true }).click();
    await expect(page.getByLabel("Громкость музыки")).toBeVisible();
    await page.keyboard.press("Escape");
    await page.getByRole("button", { name: "Рекорды", exact: true }).click();
    await page.getByRole("button", { name: "Назад", exact: true }).click();
    await page.getByRole("button", { name: width <= 760 ? "Подключиться к игре" : "Сетевая игра (2–12)", exact: true }).click();
    await expect(page).toHaveURL(/\/network$/);
    await page.getByRole("button", { name: "Назад", exact: true }).click();
    await page.getByRole("button", { name: "Одиночная игра", exact: true }).click();
    await page.getByRole("button", { name: "Меню", exact: true }).click();
    await expect(page.getByRole("dialog", { name: "Игра на паузе", exact: true })).toBeVisible();
    await page.getByRole("button", { name: "Настройки", exact: true }).click();
    await page.getByLabel("Громкость музыки").fill("0.3");
    await page.keyboard.press("Escape");
    await expect(page.getByRole("dialog", { name: "Игра на паузе", exact: true })).toBeVisible();
    await page.screenshot({ path: testInfo.outputPath(`shared-pause-${width}.png`), fullPage: true });
    await page.getByRole("button", { name: "Продолжить", exact: true }).click();
    await expect(page.getByRole("heading", { name: "Выберите тему", exact: true })).toBeVisible();
    await page.getByRole("button", { name: "Меню", exact: true }).click();
    await page.getByRole("button", { name: "Выйти в меню", exact: true }).click();
    await expect(page.getByRole("button", { name: "Одиночная игра", exact: true })).toBeVisible();
  });
}

test("network menu preserves leader authority and pause through settings", async ({ browser, page }, testInfo) => {
  await page.goto("/network?muted=1");
  const code = await createNetworkGame(page);
  const contexts = [];
  const phones = [];
  try {
    for (const name of ["Ведущий", "Игрок"]) {
      const context = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, baseURL: testInfo.project.use.baseURL });
      contexts.push(context);
      const phone = await context.newPage(); phones.push(phone);
      await phone.goto("/network?muted=1");
      await selectNetworkGame(phone, code);
      await phone.getByLabel("Ваше имя").fill(name);
      await phone.getByRole("button", { name: "Подключиться", exact: true }).click();
      await expect(phone.getByText("Вы в комнате. Ждём начала игры.")).toBeVisible();
    }
    await page.getByRole("button", { name: "Начать игру", exact: true }).click();
    await phones[1].getByRole("button", { name: "Меню", exact: true }).click();
    await expect(phones[1].getByRole("button", { name: "Продолжить", exact: true })).toHaveCount(0);
    await expect(phones[1].getByRole("button", { name: "Завершить игру", exact: true })).toHaveCount(0);
    await phones[1].getByRole("button", { name: "Назад", exact: true }).click();
    await phones[0].getByRole("button", { name: "Меню", exact: true }).click();
    await expect(page.getByRole("dialog", { name: "Игра на паузе", exact: true })).toBeVisible();
    await phones[0].getByRole("button", { name: "Настройки", exact: true }).click();
    await phones[0].keyboard.press("Escape");
    await expect(phones[0].getByRole("dialog", { name: "Игра на паузе", exact: true })).toBeVisible();
    await phones[0].screenshot({ path: testInfo.outputPath("network-shared-pause-phone.png"), fullPage: true });
    await page.screenshot({ path: testInfo.outputPath("network-shared-pause-display.png"), fullPage: true });
    await phones[0].getByRole("button", { name: "Продолжить", exact: true }).click();
    await expect(page.getByRole("dialog")).toHaveCount(0);
  } finally { await Promise.all(contexts.map(context => context.close())); }
});

test("classic menu can pause twice and settings never resume its clock", async ({ page }) => {
  await page.goto("/?muted=1");
  await page.getByRole("button", { name: "На одном устройстве (2–4)", exact: true }).click();
  await page.getByRole("button", { name: "Начать игру", exact: true }).click();
  await page.waitForTimeout(100);
  for (let cycle = 0; cycle < 2; cycle++) {
    await page.keyboard.press("Escape");
    const dialog = page.getByRole("dialog");
    await expect(dialog).toBeVisible();
    await dialog.getByRole("button", { name: "Настройки", exact: true }).click();
    await page.getByLabel("Громкость музыки").fill("0.3");
    await page.keyboard.press("Escape");
    await expect(page.getByRole("button", { name: "Продолжить", exact: true })).toBeVisible();
    const state = await page.evaluate(() => JSON.parse(localStorage.getItem("mindbattle:data:v1")!).lastMatch.state);
    expect(state.pause).toBeTruthy();
    await page.getByRole("button", { name: "Продолжить", exact: true }).click();
    await page.waitForTimeout(100);
    await expect(page.getByRole("dialog")).toHaveCount(0);
  }
  await page.getByRole("button", { name: "Меню", exact: true }).click();
  await page.getByRole("button", { name: "Выйти в меню", exact: true }).click();
  await expect(page.getByRole("button", { name: "На одном устройстве (2–4)", exact: true })).toBeVisible();
});
