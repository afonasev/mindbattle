import { expect, test } from "@playwright/test";

for (const width of [360, 390, 760, 1280, 1920]) {
  test(`arena menu has direct accessible actions at ${width}px`, async ({ page }, info) => {
    await page.setViewportSize({ width, height: width <= 760 ? 844 : 1080 });
    await page.goto("/?muted=1");
    await expect(page.getByRole("heading", { name: "Mindbattle", exact: true })).toHaveCount(1);
    await expect(page.locator(".menu-home footer")).toHaveCount(0);
    await expect(page.getByRole("button", { name: "Выход из игры", exact: true })).toHaveCount(0);
    const records = page.getByRole("button", { name: "Рекорды", exact: true });
    await expect(records).toHaveAccessibleDescription("Лучшие результаты одиночной игры");
    if (width <= 760) {
      await expect(page.getByRole("button", { name: "На одном устройстве (2–4)", exact: true })).toBeHidden();
      await expect(page.getByRole("button", { name: "Подключиться к игре", exact: true })).toBeVisible();
      const metrics = await page.locator(".main-menu-actions .menu-action, .menu-utilities .menu-action").evaluateAll(buttons =>
        buttons.filter(button => button.getBoundingClientRect().height > 0).map(button => ({
          width: button.getBoundingClientRect().width,
          height: button.getBoundingClientRect().height
        }))
      );
      expect(metrics).toHaveLength(4);
      expect(metrics.every(metric => metric.height >= 44 && metric.height <= 80)).toBe(true);
      expect(new Set(metrics.map(metric => metric.width)).size).toBe(1);
    }
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await page.screenshot({ path: info.outputPath(`arena-menu-${width}.png`), fullPage: true, animations: "disabled" });
    await records.click();
    await expect(page.getByRole("heading", { name: "Рекорды", exact: true })).toBeVisible();
    await page.screenshot({ path: info.outputPath(`arena-records-${width}.png`), fullPage: true, animations: "disabled" });
    await page.getByRole("button", { name: "Назад", exact: true }).click();
    await page.getByRole("button", { name: "Настройки", exact: true }).click();
    await expect(page.getByLabel("Громкость музыки")).toBeVisible();
    await page.screenshot({ path: info.outputPath(`arena-settings-${width}.png`), fullPage: true, animations: "disabled" });
    await page.getByLabel("Высокий контраст").check();
    await page.keyboard.press("Escape");
    await expect(page.locator(".menu-home")).toBeVisible();
    await page.screenshot({ path: info.outputPath(`arena-menu-high-contrast-${width}.png`), fullPage: true, animations: "disabled" });
    await page.getByRole("button", { name: width <= 760 ? "Подключиться к игре" : "Сетевая игра (2–12)", exact: true }).click();
    await expect(page).toHaveURL(/\/network$/);
    await page.screenshot({ path: info.outputPath(`arena-network-entry-${width}.png`), fullPage: true, animations: "disabled" });
  });
}

test("installed desktop retains its native exit action", async ({ page }, info) => {
  await page.addInitScript(() => {
    Object.assign(window, { mindbattleDesktop: {
      version: 1,
      status: async () => ({ ready: false, shellVersion: "ui-test" }),
      onUpdate: () => () => {},
      safeToUpdate: () => {},
      ready: async () => {},
      quit: async () => { document.documentElement.dataset.quitRequested = "true"; }
    } });
  });
  await page.goto("/?muted=1");
  const exit = page.getByRole("button", { name: "Выход из игры", exact: true });
  await expect(exit).toBeVisible();
  await page.screenshot({ path: info.outputPath("arena-menu-installed.png"), fullPage: true, animations: "disabled" });
  await exit.click();
  await expect(page.locator("html")).toHaveAttribute("data-quit-requested", "true");
});

test("solo result remains reachable after its final answer reveal", async ({ page }, info) => {
  await page.goto("/?muted=1");
  await page.getByRole("button", { name: "Настройки", exact: true }).click();
  await page.getByLabel("Собирать обратную связь по вопросам").uncheck();
  await page.getByRole("button", { name: "Назад", exact: true }).click();
  await page.getByRole("button", { name: "Одиночная игра", exact: true }).click();
  for (let round = 0; round < 3; round++) {
    await page.locator(".topic-choice").first().click();
    await expect(page.locator(".solo-answer-button")).toHaveCount(4);
    const wrongPosition = await page.evaluate(() => {
      const state = JSON.parse(localStorage.getItem("mindbattle:data:v1")!).lastSolo.state;
      return state.phase.round.correctPosition === "up" ? "right" : "up";
    });
    await page.locator(`.solo-answer-button.answer-option--${wrongPosition}`).click();
    await expect(page.locator(".question-stage--reveal")).toBeVisible();
    if (round === 2) await page.screenshot({ path: info.outputPath("arena-solo-final-reveal.png"), fullPage: true, animations: "disabled" });
    await page.locator(".solo-team-strip").click();
  }
  await expect(page.getByRole("heading", { name: "Результат: 0", exact: true })).toBeVisible();
  await page.getByLabel("Ваше имя").fill("Проверка оформления");
  await page.getByRole("button", { name: "Сохранить результат", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Ваш результат: 0", exact: true })).toBeVisible();
  await page.screenshot({ path: info.outputPath("arena-solo-results.png"), fullPage: true, animations: "disabled" });
});

test("arena network surfaces support twelve connected phones", async ({ browser, page }, info) => {
  test.setTimeout(90_000);
  await page.goto("/network?muted=1");
  await page.getByRole("button", { name: "Создать сетевую игру", exact: true }).click();
  const code = await page.locator(".network-code").innerText();
  const contexts = [];
  const phones = [];
  try {
    for (let index = 0; index < 12; index++) {
      const context = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, baseURL: info.project.use.baseURL });
      contexts.push(context);
      const phone = await context.newPage();
      phones.push(phone);
      await phone.goto("/network?muted=1");
      await phone.getByLabel("Код комнаты").fill(code);
      await phone.getByLabel("Ваше имя").fill(`Участник ${index + 1}`);
      await phone.getByRole("button", { name: "Подключиться", exact: true }).click();
      await expect(phone.getByText("Вы в комнате. Ждём начала игры.")).toBeVisible();
    }
    await expect(page.getByRole("heading", { name: "Игроки · 12/12" })).toBeVisible();
    await page.screenshot({ path: info.outputPath("arena-network-lobby-12.png"), fullPage: true, animations: "disabled" });
    await page.getByRole("button", { name: "Начать игру", exact: true }).click();
    await expect.poll(async () => {
      for (const phone of phones) if (await phone.getByRole("heading", { name: "Выберите тему", exact: true }).isVisible()) return true;
      return false;
    }).toBe(true);
    for (const phone of phones) {
      if (await phone.getByRole("heading", { name: "Выберите тему", exact: true }).isVisible()) {
        await phone.locator(".network-topics button").first().click();
        break;
      }
    }
    await expect(phones[0].locator(".network-answers button")).toHaveCount(4);
    await page.screenshot({ path: info.outputPath("arena-network-question-12.png"), fullPage: true, animations: "disabled" });
    await phones[0].screenshot({ path: info.outputPath("arena-network-question-phone.png"), fullPage: true, animations: "disabled" });
    for (const phone of phones) await phone.locator(".network-answers button").first().click();
    await expect(page.locator(".network-explanation")).toBeVisible();
    await expect(page.locator(".network-explanation .wrong-answer-notes article")).toHaveCount(3);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    expect(await phones[0].evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await page.screenshot({ path: info.outputPath("arena-network-reveal-12.png"), fullPage: true, animations: "disabled" });
  } finally {
    await Promise.all(contexts.map(context => context.close()));
  }
});
