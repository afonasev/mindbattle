import { createNetworkGame, selectNetworkGame } from "./network-lobby-helpers";
import { openComplaint, pendingComplaints } from './complaintHelpers';
import { test, expect, type Page, type BrowserContext } from "@playwright/test";
import { readdirSync, readFileSync } from "node:fs";
const catalogQuestions = readdirSync("src/content/topics").filter(name => name.endsWith(".json")).flatMap(name => JSON.parse(readFileSync(`src/content/topics/${name}`, "utf8")).questions) as Array<{ prompt: string; explanation: string }>;

test("network optional complaint returns to reveal and continuation needs no server write", async ({ browser, page }, testInfo) => {
  test.setTimeout(90000);
  await page.goto("/network?muted=1");
  const code = await createNetworkGame(page);
  const contexts: BrowserContext[] = [];
  const phones: Page[] = [];
  try {
    for (let i = 0; i < 2; i++) {
      const context = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, baseURL: testInfo.project.use.baseURL });
      contexts.push(context);
      const phone = await context.newPage();
      phones.push(phone);
      await phone.goto("/network?muted=1");
      await selectNetworkGame(phone, code);
      await phone.getByLabel("Ваше имя").fill(`Участник ${i + 1}`);
      await phone.getByRole("button", { name: "Подключиться", exact: true }).click();
    }
    await page.getByRole("button", { name: "Начать игру", exact: true }).click();
    await expect.poll(async () => (await Promise.all(phones.map(phone => phone.getByRole("heading", { name: "Выберите тему", exact: true }).isVisible()))).some(Boolean)).toBe(true);
    const chooser = await phones[0].getByRole("heading", { name: "Выберите тему", exact: true }).isVisible() ? phones[0] : phones[1];
    await chooser.locator(".network-topics button").first().click();
    await phones[0].locator(".network-header").click();
    await expect(phones[0].locator(".network-answers button").first()).toBeVisible();
    await phones[0].locator(".network-answers button").first().click();
    await phones[1].locator(".network-answers button").first().click();
    const sharedPause: string[] = [];
    for (const phone of phones) {
      phone.on('request', request => { if (new URL(request.url()).pathname === '/api/network/command' && ['pause','resume'].includes(request.postDataJSON()?.action?.type)) sharedPause.push(request.postDataJSON().action.type); });
      await phone.route('**/api/difficulty-feedback',route => route.abort('failed'));
    }
    await openComplaint(phones[1]);
    await phones[1].getByRole('button',{name:'Неоднозначный ответ',exact:true}).click();
    await phones[1].getByRole('button',{name:'Сохранить жалобу',exact:true}).click();
    await expect.poll(async () => (await pendingComplaints(phones[1])).length).toBe(1);
    const other = (await pendingComplaints(phones[1]))[0];
    await phones[0].route('**/api/difficulty-feedback',route => route.abort('failed'));
    await openComplaint(phones[0]);await phones[0].getByRole('button',{name:'Фактическая ошибка',exact:true}).click();
    await phones[0].getByRole('button',{name:'Сохранить жалобу',exact:true}).click();
    await expect(phones[0].getByRole('button',{name:'Дальше',exact:true})).toBeVisible();
    await expect.poll(async () => (await pendingComplaints(phones[0])).length).toBe(1);
    const leader = (await pendingComplaints(phones[0]))[0];
    expect(leader.eventId).not.toBe(other.eventId);
    expect(other.complaintReasons).toEqual(['ambiguous-answer']);
    expect(leader.complaintReasons).toEqual(['suspected-error']);
    expect(Object.keys(other).sort()).toEqual(Object.keys(leader).sort());
    expect(sharedPause).toEqual([]);
    await phones[1].getByRole('button',{name:'Меню',exact:true}).click();
    await phones[1].getByRole('button',{name:'Пожаловаться на вопрос',exact:true}).click();
    await expect(phones[1].getByRole('dialog',{name:'Жалоба сохранена',exact:true})).toBeVisible();
    await phones[0].getByRole('button',{name:'Дальше',exact:true}).click();
    await expect(phones[1].getByRole('dialog')).toHaveCount(0);
    await expect(phones[0].getByRole("dialog", { name: "Отправка фидбэка временно недоступна" })).toHaveCount(0);
    await expect(page.getByRole("heading", { name: /Выбирает Участник/ })).toBeVisible();
  } finally {
    await Promise.all(contexts.map((context) => context.close()));
  }
});

test("network: 12 phones, private answers, bonus, display restore and departure", async ({
  browser,
  page,
}, testInfo) => {
  test.setTimeout(180000);
  page.setDefaultTimeout(15000);
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("/network?muted=1");
  const code = await createNetworkGame(page);
  expect(code).toMatch(/^Тестовая игра /);
  const contexts: BrowserContext[] = [];
  const phones: Page[] = [];
  const phoneAudio: string[] = [];
  try {
    for (let i = 0; i < 12; i++) {
      const context = await browser.newContext({
        viewport: { width: 390, height: 844 },
        isMobile: true,
        hasTouch: true,
        baseURL: testInfo.project.use.baseURL,
      });
      contexts.push(context);
      const phone = await context.newPage();
      phone.setDefaultTimeout(15000);
      phones.push(phone);
      phone.on("pageerror", (e) => errors.push(e.message));
      phone.on("request", request => {
        if (new URL(request.url()).pathname.startsWith("/audio/")) phoneAudio.push(request.url());
      });
      await phone.goto("/network");
      await selectNetworkGame(phone, code);
      await phone.getByLabel("Ваше имя").fill(`Участник ${i + 1}`);
      await phone
        .getByRole("button", { name: "Подключиться", exact: true })
        .click();
      await expect(
        phone.getByText("Вы в комнате. Ждём начала игры."),
      ).toBeVisible();
    }
    await expect(
      page.getByRole("heading", { name: "Игроки · 12/12" }),
    ).toBeVisible();
    await page.getByLabel("Вопросов", { exact: true }).selectOption("9");
    await page.screenshot({
      path: testInfo.outputPath("network-lobby-12.png"),
      fullPage: true,
    });
    await page
      .getByRole("button", { name: "Начать игру", exact: true })
      .click();
    for (let round = 0; round < 3; round++) {
      if (round < 2) {
        await expect
          .poll(async () => {
            for (let i = 0; i < 12; i++)
              if (
                await phones[i]
                  .getByRole("heading", { name: "Выберите тему", exact: true })
                  .isVisible()
              )
                return i;
            return -1;
          })
          .toBeGreaterThanOrEqual(0);
        const chooser = (
          await Promise.all(
            phones.map((p) =>
              p
                .getByRole("heading", { name: "Выберите тему", exact: true })
                .isVisible(),
            ),
          )
        ).indexOf(true);
        await expect(
          phones[(chooser + 1) % phones.length].getByRole("heading", {
            name: `Выбирает Участник ${chooser + 1}`,
          }),
        ).toBeVisible();
        await phones[chooser].locator(".network-topics button").first().click();
      } else {
        await expect(
          page.getByRole("heading", { name: "Бонусный вопрос · ×2" }),
        ).toBeVisible();
        await expect.poll(async () => {
          const statuses = await Promise.all(
            phones.map((phone) =>
              phone
                .getByRole("status").filter({ hasText: "Выберите тему, которую хотите исключить" })
                .isVisible(),
            ),
          );
          return statuses.filter(Boolean).length;
        }).toBe(4);
        const vetoReady = await Promise.all(
          phones.map((phone) =>
            phone
              .getByRole("status").filter({ hasText: "Выберите тему, которую хотите исключить" })
              .isVisible(),
          ),
        );
        const voters = phones.filter((_, index) => vetoReady[index]);
        expect(voters).toHaveLength(4);
        await voters[0].locator(".network-topics button").first().click();
        await expect(
          voters[1].locator(".network-topics button").first(),
        ).toBeDisabled();
        await expect(
          voters[1].getByText(
            `Исключил: Участник ${phones.indexOf(voters[0]) + 1}`,
          ),
        ).toBeVisible();
        await voters[1].screenshot({
          path: testInfo.outputPath("network-phone-bonus-veto.png"),
          fullPage: true,
        });
        for (let i = 1; i < 4; i++)
          await voters[i].locator(".network-topics button").nth(i).click();
      }
      await expect(phones[0].locator(".network-confirmation")).toBeVisible();
      await phones[0].locator(".network-header").click();
      await expect(
        phones[0].locator(".network-answers button").first(),
      ).toBeEnabled({ timeout: 10000 });
      const mobileAnswerWidths = await phones[0]
        .locator(".network-answers button")
        .evaluateAll((buttons) =>
          buttons.map((button) => ({
            width: Math.round(button.getBoundingClientRect().width),
            viewportWidth: innerWidth,
          })),
        );
      expect(mobileAnswerWidths).toHaveLength(4);
      expect(
        mobileAnswerWidths.every(
          ({ width, viewportWidth }) => width >= viewportWidth - 24,
        ),
      ).toBe(true);
      await expect(page.locator(".network-player-card")).toHaveCount(12);
      for (const phone of phones)
        await expect(phone.locator(".network-player-card")).toHaveCount(1);
      if (round === 0) {
        await page.screenshot({
          path: testInfo.outputPath("network-question-12.png"),
          fullPage: true,
        });
        await phones[0].locator(".network-player-card").click();
        const scoreboard = phones[0].getByRole("dialog", {
          name: "Текущий счёт",
        });
        await expect(scoreboard).toBeVisible();
        await expect(scoreboard.locator(".network-scoreboard-list > div")).toHaveCount(12);
        await phones[0].screenshot({
          path: testInfo.outputPath("network-phone-scoreboard.png"),
          fullPage: true,
        });
        await scoreboard.click({ position: { x: 4, y: 4 } });
        await expect(scoreboard).toBeHidden();
        await phones[0].locator(".network-player-card").evaluate((card) =>
          (card as HTMLElement).blur(),
        );
        await phones[0].screenshot({
          path: testInfo.outputPath("network-phone-question.png"),
          fullPage: true,
        });
      }
      await phones[0].locator(".network-answers button").first().click();
      await expect(
        phones[0].getByText("Ответ принят. Ждём остальных. Его можно изменить до раскрытия"),
      ).toBeVisible();
      await expect(page.locator(".network-answers .correct")).toHaveCount(0);
      for (let i = 1; i < 12; i++)
        await phones[i]
          .locator(".network-answers button")
          .nth(i % 4)
          .click();
      await expect(page.locator(".network-answers .correct")).toHaveCount(1);
      const prompt = await page.locator(".network-question").innerText();
      const question = catalogQuestions.find(question => question.prompt === prompt);
      expect(question, "revealed question must exist in the actual catalog").toBeDefined();
      expect(question!.explanation.length).toBeGreaterThan(0);
      await expect.poll(async () => (await page.locator(".network-explanation > p").allTextContents()).join(" ").replace(/\s+/g, " ").trim()).toBe(question!.explanation.replace(/\s+/g, " ").trim());
      for (const phone of phones) {
        await expect.poll(async () => (await phone.locator(".network-explanation > p").allTextContents()).join(" ").replace(/\s+/g, " ").trim()).toBe(question!.explanation.replace(/\s+/g, " ").trim());
        await expect(phone.locator(".network-explanation .wrong-answer-notes article")).toHaveCount(3);
        await expect(phone.locator(".network-explanation .wrong-answer-notes article b")).toHaveCount(3);
        await expect(phone.locator(".network-answers small")).toContainText(["Участник 1", "Участник 2", "Участник 3", "Участник 4"]);
      }
      if (round === 0) {
        await page.screenshot({
          path: testInfo.outputPath("network-reveal-12.png"),
          fullPage: true,
        });
        expect(await page.evaluate(() => document.documentElement.scrollHeight)).toBeLessThanOrEqual(testInfo.project.use.viewport!.height);
        await phones[0].screenshot({
          path: testInfo.outputPath("network-phone-reveal.png"),
          fullPage: true,
        });
      }
      await phones[0]
        .locator(".network-round-heading")
        .getByRole("button", { name: "Дальше", exact: true })
        .click();
    }
    await expect(
      page.getByRole("heading", { name: "Результаты этапа" }),
    ).toBeVisible();
    await expect(page.locator(".network-standings tbody > tr")).toHaveCount(12);
    for (const phone of phones) {
      await expect(phone.locator(".network-standings tbody > tr")).toHaveCount(12);
      await expect(phone.locator(".network-standing--self")).toHaveCount(1);
    }
    await phones[0].screenshot({ path: testInfo.outputPath("network-phone-standings-12.png"), fullPage: true });
    expect(
      new Set(
        await page
          .locator(".network-standings tbody > tr")
          .evaluateAll((rows) => rows.map((row) => row.getBoundingClientRect().x)),
      ).size,
    ).toBe(1);
    await page.screenshot({ path: testInfo.outputPath("network-standings-12.png"), fullPage: true });
    await page.reload();
    await expect(
      page.getByRole("heading", { name: "Игра на паузе" }),
    ).toBeVisible();
    await phones[0]
      .getByRole("button", { name: "Продолжить", exact: true })
      .click();
    await expect(
      page.getByRole("heading", { name: "Игра на паузе" }),
    ).toHaveCount(0);
    await contexts[1].setOffline(true);
    await expect(
      page.getByRole("button", {
        name: "Продолжить без Участник 2",
        exact: true,
      }),
    ).toBeVisible({ timeout: 15000 });
    await contexts[1].setOffline(false);
    await expect(
      phones[1].getByText("Связь потеряна. Восстанавливаем подключение…"),
    ).toHaveCount(0, { timeout: 15000 });
    await expect(
      page.getByRole("button", {
        name: "Продолжить без Участник 2",
        exact: true,
      }),
    ).toHaveCount(0, { timeout: 15000 });
    await phones[0]
      .getByRole("button", { name: "Продолжить", exact: true })
      .click();
    await contexts[1].setOffline(true);
    await expect(
      page.getByRole("button", {
        name: "Продолжить без Участник 2",
        exact: true,
      }),
    ).toBeVisible({ timeout: 15000 });
    await page
      .getByRole("button", { name: "Продолжить без Участник 2", exact: true })
      .click();
    await expect(page.locator(".network-standings tbody tr").filter({hasText:"Участник 2"}).getByText("Выбыл", {exact:true})).toBeVisible();
    await phones[0].getByRole("button", { name: "Меню", exact: true }).click();
    await phones[0].getByRole("button", { name: "Настройки", exact: true }).click();
    await expect(phones[0].getByRole("heading", { name: "Настройки", exact: true })).toBeVisible();
    await phones[0].getByRole("button", { name: "Назад", exact: true }).click();
    await phones[0]
      .getByRole("button", { name: "Вернуться в лобби", exact: true })
      .click();
    await expect(
      page.getByRole("heading", { name: "Игроки · 11/12" }),
    ).toBeVisible();
    await expect(page.locator(".network-room-title")).toHaveText(code);
    expect(phoneAudio).toEqual([]);
    expect(errors).toEqual([]);
  } finally {
    for (const context of contexts) await context.close().catch(() => {});
  }
});

test("network display starts the arena sound after create gesture", async ({ page }, testInfo) => {
  const audioRequests: string[] = [];
  page.on("request", request => {
    const path = new URL(request.url()).pathname;
    if (path.startsWith("/audio/quiz-v1/")) audioRequests.push(path);
  });
  await page.goto("/network");
  await expect(page.getByRole("heading", { name: "Соберите свою игру." })).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath("network-entry.png"), fullPage: true });
  await createNetworkGame(page);
  await expect(page.locator(".network-room-title")).toBeVisible();
  await expect.poll(() => audioRequests.includes("/audio/quiz-v1/menu.mp3")).toBe(true);
});

test("network entry keeps the menu music playing", async ({ page }) => {
  await page.addInitScript(() => {
    const events: string[] = [];
    (window as Window & { __musicEvents?: string[] }).__musicEvents = events;
    const originalPlay = HTMLMediaElement.prototype.play;
    const originalPause = HTMLMediaElement.prototype.pause;
    HTMLMediaElement.prototype.play = function () {
      if (new URL(this.currentSrc || this.src).pathname.endsWith("/quiz-v1/menu.mp3")) events.push("play");
      return originalPlay.call(this);
    };
    HTMLMediaElement.prototype.pause = function () {
      if (new URL(this.currentSrc || this.src).pathname.endsWith("/quiz-v1/menu.mp3")) events.push("pause");
      return originalPause.call(this);
    };
  });
  await page.goto("/");
  await page.getByRole("button", { name: "Сетевая игра (2–12)", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Соберите свою игру." })).toBeVisible();
  await expect.poll(() => page.evaluate(() => (window as Window & { __musicEvents?: string[] }).__musicEvents ?? [])).toEqual(["play"]);
});

test("network entry has no sound toggle in its header", async ({ page }, testInfo) => {
  await page.goto("/network?muted=1");
  await expect(page.getByRole("heading", { name: "Соберите свою игру." })).toBeVisible();
  await expect(page.getByRole("button", { name: /Звук (включён|выключен)/ })).toHaveCount(0);
  await page.screenshot({ path: testInfo.outputPath("network-entry-no-sound-toggle.png"), fullPage: true });
});
