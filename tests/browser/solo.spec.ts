import { expect, test } from "@playwright/test";

type Position = "up" | "right" | "down" | "left";
type SoloPersistedState = {
  readonly slotIndex: number;
  readonly phase: {
    readonly kind: string;
    readonly round?: { readonly correctPosition: Position; readonly risk: boolean; readonly points: number };
  };
};

const answerKey: Record<Position, string> = {
  up: "KeyW",
  right: "KeyD",
  down: "KeyS",
  left: "KeyA"
};

async function muteAudio(page: import("@playwright/test").Page) {
  await page.locator(".preferences-panel summary").click();
  const muted = page.getByLabel("Без звука");
  if (!(await muted.isChecked())) await muted.check();
  await page.locator(".preferences-panel summary").click();
}

async function soloState(page: import("@playwright/test").Page): Promise<SoloPersistedState> {
  return page.evaluate(() => {
    const source = localStorage.getItem("mindbattle:data:v1");
    if (!source) throw new Error("No persisted solo run");
    return JSON.parse(source).lastSolo.state as SoloPersistedState;
  });
}

async function startSoloWithoutFeedback(page: import("@playwright/test").Page) {
  await page.locator(".preferences-panel summary").click();
  await page.getByLabel("Собирать обратную связь по вопросам").uncheck();
  await page.locator(".preferences-panel summary").click();
  await page.getByRole("button", { name: "Соло-забег" }).click();
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

test("shows the appropriate solo controls without overflowing the topic stage", async ({ page }, testInfo) => {
  await page.goto("/?muted=1");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await muteAudio(page);
  await page.getByRole("button", { name: "Соло-забег" }).click();

  await expect(page.getByRole("heading", { name: "Выберите тему" })).toBeVisible();
  await page.keyboard.press("KeyD");
  await expect(page.locator(".control-help")).toHaveText("A/D · S");
  await expect(page.locator(".topic-choice--current")).toHaveCount(1);
  await captureSettled(page, testInfo.outputPath("solo-wasd-topic.png"));

  await page.keyboard.press("ArrowRight");
  await expect(page.locator(".control-help")).toHaveText("←/→ · Enter");
  const metrics = await page.locator(".solo-topic-stage").evaluate((stage) => ({
    stageFits: stage.scrollWidth <= stage.clientWidth,
    pageFits: document.documentElement.scrollWidth <= innerWidth,
    cardBelowStage: document.querySelector(".solo-team-strip")!.getBoundingClientRect().top > stage.getBoundingClientRect().bottom
  }));
  expect(metrics).toEqual({ stageFits: true, pageFits: true, cardBelowStage: true });
  await captureSettled(page, testInfo.outputPath("solo-arrows-topic.png"));
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
  await page.locator(".preferences-panel summary").click();
  await page.getByLabel("Крупный текст").check();
  await page.getByLabel("Высокий контраст").check();
  await page.getByLabel("Без анимации").check();
  await page.locator(".preferences-panel summary").click();
  await page.getByRole("button", { name: "Соло-забег" }).click();
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

test("uses the team feedback layout with no selected by default", async ({ page }, testInfo) => {
  await page.goto("/?muted=1");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await muteAudio(page);
  await page.getByRole("button", { name: "Соло-забег" }).click();
  await page.keyboard.press("Enter");
  const answering = await soloState(page);
  const correctPosition = answering.phase.round?.correctPosition;
  if (!correctPosition) throw new Error("Expected solo question");
  await page.keyboard.press(answerKey[correctPosition]);
  await expect(page.locator(".question-stage--reveal")).toBeVisible();
  await expect(page.locator(".solo-team-strip .game-team-card")).toHaveClass(/game-team-card--correct/);
  await page.locator(".question-stage--reveal .explanation").click();

  await expect(page.getByRole("heading", { name: "Хотите пожаловаться на вопрос?" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Нет" })).toHaveClass(/feedback-tag--cursor/);
  await expect(page.getByRole("button", { name: "Да" })).not.toHaveClass(/feedback-tag--cursor/);
  await expect(page.locator(".feedback-status")).toContainText("«Нет» выбрано по умолчанию");
  await captureSettled(page, testInfo.outputPath("solo-feedback-default-no.png"));
  await page.keyboard.press("KeyA");
  await expect(page.getByRole("button", { name: "Да" })).toHaveClass(/feedback-tag--cursor/);
  await page.keyboard.press("Enter");
  await expect(page.getByRole("heading", { name: "Что не так с вопросом?" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Слишком лёгкий" })).toHaveClass(/feedback-tag--cursor/);
  await page.keyboard.press("KeyD");
  await expect(page.getByRole("button", { name: "Слишком сложный" })).toHaveClass(/feedback-tag--cursor/);
  await page.keyboard.press("Enter");
  await expect(page.getByRole("button", { name: "Слишком сложный" })).toContainText("✓");
  await page.keyboard.press("KeyS");
  await expect(page.getByRole("button", { name: "Фактическая ошибка" })).toHaveClass(/feedback-tag--cursor/);
});

test("matches the team reveal for a wrong solo answer", async ({ page }, testInfo) => {
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
  await expect(page.locator(".game-brand span")).toHaveText("Соло-забег");
  await expect(page.locator(".question-header strong")).toHaveText("Вопрос 1");
  await expect(page.locator(".solo-team-strip .game-team-card")).toHaveClass(/game-team-card--wrong/);
  await expect(page.locator(".wrong-answer-notes")).toBeVisible();
  await expect(page.locator(".wrong-answer-notes")).toContainText("А что означал выбранный вариант?");
  await captureSettled(page, testInfo.outputPath("solo-wrong-answer-reveal.png"));
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
    if (index < 2) {
      await expect(page.locator(".question-stage--reveal")).toBeVisible();
      await page.keyboard.press("Enter");
    }
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
  await expect(page.getByRole("button", { name: "Соло-забег" })).toBeVisible();
});

test("uses the team pause dialog and resumes the solo run", async ({ page }, testInfo) => {
  await page.goto("/?muted=1");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await muteAudio(page);
  await startSoloWithoutFeedback(page);

  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Соло-забег восстановлен" })).toBeVisible();
  await expect(page.locator(".game-brand")).toBeVisible();
  await captureSettled(page, testInfo.outputPath("solo-pause.png"));
  await page.keyboard.press("Enter");
  await expect(page.getByRole("heading", { name: "Выберите тему" })).toBeVisible();
});

test("accepts a neutral virtual gamepad and updates the control hint", async ({ page }, testInfo) => {
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
  await expect(page.locator(".control-help")).toHaveText("Кликните карточку");
  await setVirtualGamepadButton(page, 0, false);
  await setVirtualGamepadButton(page, 15, true);
  await expect(page.locator(".control-help")).toHaveText("D-pad · A");
  await setVirtualGamepadButton(page, 15, false);
  await setVirtualGamepadButton(page, 0, true);
  await expect(page.locator(".question-stage")).toBeVisible();
});
