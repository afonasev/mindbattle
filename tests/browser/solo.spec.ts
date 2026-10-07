import { openComplaint, pendingComplaints } from './complaintHelpers';
import { expect, test } from "@playwright/test";

type Position = "up" | "right" | "down" | "left";
type SoloPersistedState = {
  readonly slotIndex: number;
  readonly phase: {
    readonly kind: string;
    readonly cursor?: number;
    readonly round?: { readonly correctPosition: Position; readonly risk: boolean; readonly points: number };
  };
};

async function revealSolo(page: import('@playwright/test').Page) {
  await page.goto('/?muted=1'); await page.evaluate(() => localStorage.clear()); await page.reload(); await muteAudio(page);
  await page.getByRole('button', { name:'Одиночная игра' }).click(); await page.keyboard.press('Enter');
  const state=await soloState(page); if (!state.phase.round) throw Error('Expected question');
  await page.keyboard.press(answerKey[state.phase.round.correctPosition]); await expect(page.locator('.question-stage--reveal')).toBeVisible();
}
const answerKey: Record<Position, string> = {
  up: "KeyW",
  right: "KeyD",
  down: "KeyS",
  left: "KeyA"
};

async function muteAudio(page: import("@playwright/test").Page) {
  await page.getByRole("button", { name: "Настройки", exact: true }).click();
  const toggle = page.getByRole("button", { name: "Звук включён", exact: true });
  if (await toggle.count()) await toggle.click();
  await page.getByRole("button", { name: "Назад", exact: true }).click();
}

async function soloState(page: import("@playwright/test").Page): Promise<SoloPersistedState> {
  return page.evaluate(() => {
    const source = localStorage.getItem("mindbattle:data:v1");
    if (!source) throw new Error("No persisted solo run");
    return JSON.parse(source).lastSolo.state as SoloPersistedState;
  });
}

async function startSoloWithoutFeedback(page: import("@playwright/test").Page) {
  await page.getByRole("button", { name: "Настройки", exact: true }).click();
  await page.getByRole("button", { name: "Назад", exact: true }).click();
  await page.getByRole("button", { name: "Одиночная игра" }).click();
}

async function captureSettled(page: import("@playwright/test").Page, path: string) {
  await page.waitForTimeout(350);
  await page.screenshot({ path, fullPage: true });
}

async function setVirtualGamepadButton(
  page: import("@playwright/test").Page,
  buttonIndex: number,
  pressed: boolean
) {
  await page.evaluate(({ buttonIndex, pressed }) => {
    const pad = (globalThis as typeof globalThis & { __soloPad: Gamepad }).__soloPad;
    (pad.buttons[buttonIndex] as GamepadButton & { pressed: boolean; value: number }).pressed = pressed;
    (pad.buttons[buttonIndex] as GamepadButton & { pressed: boolean; value: number }).value = pressed ? 1 : 0;
  }, { buttonIndex, pressed });
  await page.waitForTimeout(80);
}

test("shows touch-only solo controls without overflowing the topic stage", async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/?muted=1");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await muteAudio(page);
  await page.getByRole("button", { name: "Одиночная игра" }).click();

  await expect(page.getByRole("heading", { name: "Выберите тему" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Меню" })).toBeVisible();
  await expect(page.locator(".solo-shell")).not.toContainText(/ESC|Enter|WASD|стрелки/i);
  await expect(page.locator(".topic-choice--current")).toHaveCount(1);
  const metrics = await page.locator(".solo-topic-stage").evaluate((stage) => ({
    stageFits: stage.scrollWidth <= stage.clientWidth,
    pageFits: document.documentElement.scrollWidth <= innerWidth,
    cardBelowStage: document.querySelector(".solo-team-strip")!.getBoundingClientRect().top > stage.getBoundingClientRect().bottom
  }));
  expect(metrics).toEqual({ stageFits: true, pageFits: true, cardBelowStage: true });
  await captureSettled(page, testInfo.outputPath("solo-touch-topic.png"));
  await page.locator(".topic-choice").nth(1).click();
  await expect(page.locator(".question-stage")).toBeVisible();
  const answerWidths = await page.locator(".solo-answer-button").evaluateAll((buttons) =>
    buttons.map((button) => ({
      width: Math.round(button.getBoundingClientRect().width),
      viewportWidth: innerWidth
    }))
  );
  expect(answerWidths).toHaveLength(4);
  expect(answerWidths.every(({ width, viewportWidth }) => width >= viewportWidth - 24)).toBe(true);
  await captureSettled(page, testInfo.outputPath("solo-touch-answers.png"));
  await page.locator(".solo-answer-button").first().click();
  await expect(page.locator(".question-stage--reveal")).toBeVisible();
  await captureSettled(page, testInfo.outputPath("solo-touch-answer-reveal.png"));
  await page.getByRole("button", { name: "Меню" }).click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await page.getByRole("button", { name: "Настройки", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Настройки", exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Назад", exact: true }).click();
  await expect(page.getByRole("button", { name: "Продолжить", exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Продолжить" }).click();
  await expect(page.locator(".question-stage--reveal")).toBeVisible();
  await page.locator(".solo-team-strip").click();
  await expect(page.locator(".solo-topic-stage")).toBeVisible();
});

test("boots when the browser does not implement the Gamepad API", async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(navigator, "getGamepads", { configurable: true, value: undefined });
  });
  await page.goto("/?muted=1");
  await expect(page.getByRole("button", { name: "Одиночная игра" })).toBeVisible();
});

test("explains the easy risk before declining it without creating a question", async ({ page }, testInfo) => {
  await page.goto("/?muted=1");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await muteAudio(page);
  await startSoloWithoutFeedback(page);

  for (let index = 0; index < 4; index += 1) {
    await page.keyboard.press("Enter");
    await expect(page.locator(".question-stage")).toBeVisible();
    const answering = await soloState(page);
    const correctPosition = answering.phase.round?.correctPosition;
    if (!correctPosition) throw new Error("Expected solo question");
    await page.keyboard.press(answerKey[correctPosition]);
    await expect(page.locator(".question-stage--reveal")).toBeVisible();
    if (index === 0) {
      await captureSettled(page, testInfo.outputPath("solo-reveal-no-continue-button.png"));
      await page.locator(".question-stage--reveal .explanation").click();
    }
    else await page.keyboard.press("Enter");
  }

  await expect(page.locator(".solo-risk")).toBeVisible();
  await expect(page.locator(".solo-risk")).toContainText("Тема будет выбрана случайно");
  await expect(page.locator(".solo-risk")).toContainText("+300");
  await expect(page.locator(".solo-risk")).toContainText("−100");
  await captureSettled(page, testInfo.outputPath("solo-easy-risk.png"));
  await page.getByRole("button", { name: "Отказаться" }).click();
  await expect(page.getByRole("heading", { name: "Выберите тему" })).toBeVisible();
  expect((await soloState(page)).slotIndex).toBe(5);
});

test("starts the random easy risk question with the x3 reward", async ({ page }, testInfo) => {
  await page.goto("/?muted=1");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await muteAudio(page);
  await startSoloWithoutFeedback(page);

  for (let index = 0; index < 4; index += 1) {
    await page.keyboard.press("Enter");
    const answering = await soloState(page);
    const correctPosition = answering.phase.round?.correctPosition;
    if (!correctPosition) throw new Error("Expected solo question");
    await page.keyboard.press(answerKey[correctPosition]);
    await expect(page.locator(".question-stage--reveal")).toBeVisible();
    await page.keyboard.press("Enter");
  }

  await expect(page.locator(".solo-risk")).toBeVisible();
  await expect(page.getByRole("button", { name: "Принять риск" })).toHaveClass(/topic-choice--current/);
  await page.keyboard.press("KeyD");
  await expect(page.getByRole("button", { name: "Отказаться" })).toHaveClass(/topic-choice--current/);
  await page.keyboard.press("KeyA");
  await page.keyboard.press("Enter");
  await expect(page.locator(".question-stage")).toBeVisible();
  const riskQuestion = await soloState(page);
  expect(riskQuestion.phase.round).toMatchObject({ risk: true, points: 300 });
  await captureSettled(page, testInfo.outputPath("solo-easy-risk-accepted.png"));
});

test("keeps the solo card and question readable with accessibility preferences", async ({ page }, testInfo) => {
  await page.goto("/?muted=1");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await muteAudio(page);
  await page.getByRole("button", { name: "Настройки", exact: true }).click();
  await page.getByLabel("Крупный текст").check();
  await page.getByLabel("Высокий контраст").check();
  await page.getByLabel("Без анимации").check();
  await page.getByRole("button", { name: "Назад", exact: true }).click();
  await page.getByRole("button", { name: "Одиночная игра" }).click();
  await page.keyboard.press("Enter");

  await expect(page.locator(".question-stage")).toBeVisible();
  await expect(page.locator(".solo-lives")).toHaveAttribute("aria-label", "Жизни: 3 из 3");
  await expect(page.locator(".team-question-timer")).toBeVisible();
  const metrics = await page.locator(".question-stage").evaluate((stage) => ({
    questionFits: stage.scrollWidth <= stage.clientWidth,
    pageFits: document.documentElement.scrollWidth <= innerWidth,
    pageHeightFits: document.documentElement.scrollHeight <= innerHeight
  }));
  expect(metrics).toEqual({ questionFits: true, pageFits: true, pageHeightFits: true });
  await captureSettled(page, testInfo.outputPath("solo-accessible-question.png"));
});

test("shows the shared reserve on the solo player card after the base timer", async ({ page }, testInfo) => {
  await page.goto("/?muted=1");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await muteAudio(page);
  await startSoloWithoutFeedback(page);
  await page.keyboard.press("Enter");
  await expect(page.locator(".team-question-timer")).toHaveText("10");

  await page.waitForTimeout(10_150);
  await expect(page.locator(".team-question-timer--reserve")).toBeVisible();
  await expect(page.locator(".team-question-timer--reserve")).not.toHaveText("60");
  await captureSettled(page, testInfo.outputPath("solo-reserve-timer.png"));
});

test("offers an optional complaint only in the reveal pause menu", async ({ page }, testInfo) => {
  await revealSolo(page); expect(await page.getByRole('button',{name:'Пожаловаться на вопрос',exact:true}).count()).toBe(0); await openComplaint(page);
  await expect(page.getByText('Сложность: Лёгкий',{exact:true})).toBeVisible(); await expect(page.getByRole('button',{name:'Сохранить жалобу',exact:true})).toBeDisabled();
  await captureSettled(page,testInfo.outputPath('solo-complaint-menu.png'));await page.getByRole('button',{name:'Отмена',exact:true}).click();
  await expect(page.locator('.question-stage--reveal')).toBeVisible();expect((await soloState(page)).slotIndex).toBe(0);
});

test("continues solo reveal with no feedback step or HTTP request", async ({ page }) => {
  let calls=0;await page.route('**/api/difficulty-feedback',route => {calls++;return route.abort('failed');});
  await revealSolo(page); await page.locator('.question-stage--reveal .explanation').click();
  await expect(page.locator('.solo-topic-stage')).toBeVisible();expect((await soloState(page)).slotIndex).toBe(1);expect(calls).toBe(0);
});

test("saves solo complaints offline without retry or skip dialogs", async ({ page }, testInfo) => {
  await page.route('**/api/difficulty-feedback',route => route.abort('failed'));await revealSolo(page);const before=await soloState(page);await openComplaint(page);
  await page.getByRole('button',{name:'Неинтересный для викторины',exact:true}).click();await captureSettled(page,testInfo.outputPath('solo-offline-complaint.png'));
  await page.getByRole('button',{name:'Сохранить жалобу',exact:true}).click();await expect(page.locator('.question-stage--reveal')).toBeVisible();expect((await soloState(page)).phase).toEqual(before.phase);
  await expect.poll(async () => (await pendingComplaints(page)).length).toBe(1);
  await page.locator('.question-stage--reveal .explanation').click();await expect(page.locator('.solo-topic-stage')).toBeVisible();
});

for (const width of [null, 360, 760]) test(`matches the team reveal for a wrong solo answer (${width ?? "desktop"})`, async ({ page }, testInfo) => {
  if (width) await page.setViewportSize({width, height:800});
  await page.goto("/?muted=1");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await muteAudio(page);
  await startSoloWithoutFeedback(page);
  await page.keyboard.press("Enter");
  const answering = await soloState(page);
  const correctPosition = answering.phase.round?.correctPosition;
  if (!correctPosition) throw new Error("Expected solo question");
  const wrongPosition = (["up", "right", "down", "left"] as const).find((position) => position !== correctPosition);
  if (!wrongPosition) throw new Error("Expected a wrong position");
  await page.keyboard.press(answerKey[wrongPosition]);

  await expect(page.locator(".question-stage--reveal .answer-option--wrong")).toHaveCount(1);
  await expect(page.locator(".solo-shell .game-brand strong")).toHaveText("Mindbattle");
  await expect(page.locator(".question-header strong")).toHaveText("Вопрос 1 (Лёгкий)");
  await expect(page.locator(".solo-team-strip .game-team-card")).toHaveClass(/game-team-card--wrong/);
  await expect(page.locator(".wrong-answer-notes")).toBeVisible();
  await expect(page.locator(".wrong-answer-notes article")).toHaveCount(3);
  await expect(page.locator(".explanation > p")).toHaveCount(1);
  await expect(page.locator(".wrong-answer-notes > strong")).toHaveCount(0);
  if (!width) {
    const rows = await page.locator(".wrong-answer-notes article").evaluateAll(cards => cards.map(card => Math.round(card.getBoundingClientRect().top)));
    expect(new Set(rows).size).toBe(1);
  }
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  if (width) {
    const fits = await page.evaluate(() => {
      const notes = document.querySelector(".wrong-answer-notes")!.getBoundingClientRect();
      const player = document.querySelector(".solo-team-strip")!.getBoundingClientRect();
      return notes.bottom <= player.top;
    });
    expect(fits).toBe(true);
  }
  await captureSettled(page, testInfo.outputPath(`solo-wrong-answer-reveal-${width ?? "desktop"}.png`));
});

test("uses the team final-stage framing for solo results and leaderboard rank", async ({ page }, testInfo) => {
  await page.goto("/?muted=1");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await muteAudio(page);
  await startSoloWithoutFeedback(page);

  for (let index = 0; index < 3; index += 1) {
    await page.keyboard.press("Enter");
    const answering = await soloState(page);
    const correctPosition = answering.phase.round?.correctPosition;
    if (!correctPosition) throw new Error("Expected solo question");
    const wrongPosition = (["up", "right", "down", "left"] as const).find((position) => position !== correctPosition);
    if (!wrongPosition) throw new Error("Expected a wrong position");
    await page.keyboard.press(answerKey[wrongPosition]);
    await expect(page.locator(".question-stage--reveal")).toBeVisible();
    await page.keyboard.press("Enter");
  }

  await expect(page.getByRole("heading", { name: "Результат: 0" })).toBeVisible();
  await expect(page.locator(".winner-stage.solo-results")).toBeVisible();
  await captureSettled(page, testInfo.outputPath("solo-name-entry.png"));
  await page.getByLabel("Ваше имя").fill("Проверка");
  await page.keyboard.press("Enter");
  await expect(page.getByRole("heading", { name: "Ваш результат: 0" })).toBeVisible();
  await expect(page.locator(".game-brand")).toBeVisible();
  await expect(page.locator(".solo-rank")).toContainText("Ваше место: 1 из 1");
  await page.evaluate(() => window.scrollTo(0, 0));
  await captureSettled(page, testInfo.outputPath("solo-leaderboard.png"));
  await page.keyboard.press("Enter");
  await expect(page.getByRole("button", { name: "Одиночная игра" })).toBeVisible();
});

test("uses the team pause dialog and resumes the solo run", async ({ page }, testInfo) => {
  await page.goto("/?muted=1");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await muteAudio(page);
  await startSoloWithoutFeedback(page);

  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Игра на паузе" })).toBeVisible();
  await expect(page.locator(".game-brand")).toBeVisible();
  await captureSettled(page, testInfo.outputPath("solo-pause.png"));
  await page.getByRole("button", { name: "Настройки", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Настройки", exact: true })).toBeVisible();
  await page.getByLabel("Громкость музыки").fill("0.4");
  await page.getByRole("button", { name: "Назад", exact: true }).click();
  await expect(page.getByRole("button", { name: "Продолжить", exact: true })).toBeVisible();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("heading", { name: "Выберите тему" })).toBeVisible();
});

test("accepts a neutral virtual gamepad before moving and confirming", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "chromium-1280", "One viewport is enough for gamepad input coverage");
  await page.addInitScript(() => {
    const pad = {
      index: 0,
      id: "Virtual Xbox Solo",
      mapping: "standard",
      connected: true,
      timestamp: 0,
      axes: [],
      vibrationActuator: null,
      buttons: Array.from({ length: 16 }, (_, index) => ({ pressed: index === 0, touched: false, value: index === 0 ? 1 : 0 }))
    } as unknown as Gamepad;
    (globalThis as typeof globalThis & { __soloPad: Gamepad }).__soloPad = pad;
    Object.defineProperty(navigator, "getGamepads", { configurable: true, value: () => [pad] });
  });
  await page.goto("/?muted=1");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await muteAudio(page);
  await startSoloWithoutFeedback(page);

  await page.waitForTimeout(180);
  await expect(page.getByRole("heading", { name: "Выберите тему" })).toBeVisible();
  expect((await soloState(page)).phase).toMatchObject({ kind: "topic", cursor: 0 });
  await setVirtualGamepadButton(page, 0, false);
  await setVirtualGamepadButton(page, 15, true);
  await expect.poll(async () => {
    const phase = (await soloState(page)).phase;
    return phase.kind === "topic" ? phase.cursor : null;
  }).toBe(1);
  await setVirtualGamepadButton(page, 15, false);
  await setVirtualGamepadButton(page, 0, true);
  await expect(page.locator(".question-stage")).toBeVisible();
});

test("uses D-pad navigation in the optional solo complaint menu", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "chromium-1280", "One viewport is enough for gamepad input coverage");
  await page.addInitScript(() => {
    const pad = {
      index: 0,
      id: "Virtual Xbox Solo",
      mapping: "standard",
      connected: true,
      timestamp: 0,
      axes: [],
      vibrationActuator: null,
      buttons: Array.from({ length: 16 }, () => ({ pressed: false, touched: false, value: 0 }))
    } as unknown as Gamepad;
    (globalThis as typeof globalThis & { __soloPad: Gamepad }).__soloPad = pad;
    Object.defineProperty(navigator, "getGamepads", { configurable: true, value: () => [pad] });
  });
  await page.goto("/?muted=1");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await muteAudio(page);
  await page.getByRole("button", { name: "Одиночная игра" }).click();
  await expect(page.getByRole("heading", { name: "Выберите тему" })).toBeVisible();

  await setVirtualGamepadButton(page, 15, true);
  await setVirtualGamepadButton(page, 15, false);
  await setVirtualGamepadButton(page, 0, true);
  await setVirtualGamepadButton(page, 0, false);
  await expect(page.locator(".question-stage")).toBeVisible();
  const state = await soloState(page);
  const correctPosition = state.phase.round?.correctPosition;
  if (!correctPosition) throw new Error("Expected solo question");
  const buttonForPosition: Record<Position, number> = { up: 3, right: 1, down: 0, left: 2 };
  await setVirtualGamepadButton(page, buttonForPosition[correctPosition], true);
  await setVirtualGamepadButton(page, buttonForPosition[correctPosition], false);
  await expect(page.locator(".question-stage--reveal")).toBeVisible();
  await openComplaint(page);await page.waitForTimeout(80);
  const press=async (button:number) => {await setVirtualGamepadButton(page,button,true);await setVirtualGamepadButton(page,button,false);};
  const easy=page.getByRole('button',{name:'Слишком лёгкий',exact:true});const hard=page.getByRole('button',{name:'Слишком сложный',exact:true});
  await expect(easy).toBeFocused();await press(13);await expect(hard).toBeFocused();await press(0);await expect(hard).toHaveAttribute('aria-pressed','true');
  await press(12);await expect(easy).toBeFocused();await press(0);await expect(easy).toHaveAttribute('aria-pressed','true');await expect(hard).toHaveAttribute('aria-pressed','false');
  await press(1);await expect(page.locator('.question-stage--reveal')).toBeVisible();
});
