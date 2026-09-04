import { expect, test, type Page } from "@playwright/test";

type Team = "green" | "blue";
type Position = "up" | "right" | "down" | "left";

const keys: Record<Team, Record<Position, string>> = {
  green: { up: "w", right: "d", down: "s", left: "a" },
  blue: { up: "ArrowUp", right: "ArrowRight", down: "ArrowDown", left: "ArrowLeft" }
};
const confirmKey = (team: Team) => team === "green" ? "Space" : "ShiftRight";

async function storedState(page: Page) {
  return page.evaluate(() => {
    const source = localStorage.getItem("mindbattle:data:v1");
    if (!source) throw new Error("No persisted match");
    return JSON.parse(source).lastMatch.state;
  });
}

async function waitForInputGate(page: Page) {
  await page.waitForTimeout(80);
}

async function captureSettled(page: Page, path: string) {
  await page.waitForTimeout(320);
  await page.screenshot({ path, fullPage: true });
}

async function muteAudio(page: Page) {
  const preferences = page.locator(".preferences-panel");
  await preferences.locator("summary").click();
  const muted = page.getByLabel("Без звука");
  if (!(await muted.isChecked())) await muted.check();
  await preferences.locator("summary").click();
}

async function chooseCurrentTopic(
  page: Page,
  inspectBonusConfirmation?: () => Promise<void>
) {
  const state = await storedState(page);
  if (state.phase.kind === "normal-topic") {
    const chooser = state.phase.chooser as Team;
    await page.keyboard.press(keys[chooser].right);
    const moved = await storedState(page);
    expect(moved.phase).toMatchObject({ kind: "normal-topic", cursor: 1 });
    await page.keyboard.press(confirmKey(chooser));
    await expect(page.locator(".topic-confirmation-stage")).toBeVisible();
    await waitForInputGate(page);
    await page.keyboard.press("w");
    await expect(page.locator(".question-stage")).toBeVisible();
    return;
  }
  expect(["bonus-veto", "final-veto"]).toContain(state.phase.kind);
  const participants = state.phase.kind === "final-veto" ? state.tieBreak.contenders : state.config.teams;
  await expect(page.locator(".topic-veto")).toHaveCount(participants.length + 1);
  await page.keyboard.press("d");
  let vetoState = await storedState(page);
  expect(vetoState.phase.cursors.green).toBe(1);
  await page.keyboard.press("a");
  vetoState = await storedState(page);
  expect(vetoState.phase.cursors.green).toBe(0);
  await page.keyboard.press("Space");
  vetoState = await storedState(page);
  expect(vetoState.phase.vetoes.green).toBe(vetoState.phase.candidates[0]);
  await page.keyboard.press("ArrowRight");
  vetoState = await storedState(page);
  expect(vetoState.phase.cursors.blue).toBe(1);
  await page.keyboard.down("ShiftRight");
  await expect(page.locator(".topic-confirmation-stage")).toBeVisible();
  await expect(page.locator(".topic-confirmation-stage .stage-label")).toHaveText(
    state.phase.kind === "final-veto" ? "Финальная тема" : "Бонусный вопрос · x2"
  );
  await expect(page.locator(".topic-confirmation-stage")).not.toContainText("начнётся через");
  await page.waitForTimeout(120);
  const held = await storedState(page);
  expect(held.phase.kind).toBe("topic-confirmation");
  if (inspectBonusConfirmation) await inspectBonusConfirmation();
  await page.keyboard.up("ShiftRight");
  await waitForInputGate(page);
  await page.keyboard.press("w");
  await expect(page.locator(".question-stage")).toBeVisible();
  const answering = await storedState(page);
  expect(answering.phase.kind).toBe("answering");
  expect(answering.phase.baseRemainingMs).toBeGreaterThan(9_800);
  if (state.phase.kind === "final-veto") {
    expect(answering.phase.round).toMatchObject({ mode: "tie-break", difficulty: "hard", points: 0 });
  } else {
    const stageLength = answering.config.questionCount / 3;
    const basePoints = [100, 200, 300][Math.floor(answering.mainQuestionIndex / stageLength)];
    expect(answering.phase.round.points).toBe(basePoints * 2);
  }
}

async function answer(page: Page, team: Team, position: Position) {
  await page.keyboard.press(keys[team][position]);
}

async function rateDifficulty(page: Page, key = "a", expectDismissed = true) {
  await waitForInputGate(page);
  await page.keyboard.press("KeyQ");
  await page.keyboard.press("w");
  await page.waitForTimeout(120);
  await page.keyboard.press("w");
  await page.waitForTimeout(120);
  await page.keyboard.press("ArrowUp");
  await page.waitForTimeout(120);
  await page.keyboard.press("ArrowUp");
  await expect(page.getByRole("heading", { name: "Отметьте впечатление от вопроса" })).toBeVisible();
  await expect(page.locator(".difficulty-feedback-stage")).toBeVisible();
  await waitForInputGate(page);
  for (const team of ["green", "blue"] as const) {
    for (let attempt = 0; attempt < 4; attempt += 1) {
      const state = await storedState(page);
      if (state.phase.kind !== "difficulty-feedback" || state.phase.responses[team].similarityPreference) break;
      await page.keyboard.press(confirmKey(team));
      await page.waitForTimeout(120);
    }
    for (let attempt = 0; attempt < 6; attempt += 1) {
      const state = await storedState(page);
      if (state.phase.kind !== "difficulty-feedback" || state.phase.responses[team].tagCursor === 9) break;
      await page.keyboard.press(team === "green" ? "s" : "ArrowDown");
      await page.waitForTimeout(120);
    }
    for (let attempt = 0; attempt < 4; attempt += 1) {
      const state = await storedState(page);
      if (state.phase.kind !== "difficulty-feedback" || state.phase.responses[team].completed) break;
      await page.keyboard.press(confirmKey(team));
      await page.waitForTimeout(120);
    }
  }
  if (expectDismissed) {
    await expect(page.locator(".difficulty-feedback-stage")).toHaveCount(0);
  }
}

async function pressVirtualPad(page: Page, padIndex: number, buttonIndex: number) {
  await page.evaluate(
    ({ padIndex, buttonIndex }) => {
      const pads = (globalThis as typeof globalThis & { __mindbattlePads: Gamepad[] })
        .__mindbattlePads;
      (pads[padIndex].buttons[buttonIndex] as GamepadButton & { pressed: boolean; value: number }).pressed = true;
      (pads[padIndex].buttons[buttonIndex] as GamepadButton & { pressed: boolean; value: number }).value = 1;
    },
    { padIndex, buttonIndex }
  );
  await page.waitForTimeout(40);
  await page.evaluate(
    ({ padIndex, buttonIndex }) => {
      const pads = (globalThis as typeof globalThis & { __mindbattlePads: Gamepad[] })
        .__mindbattlePads;
      (pads[padIndex].buttons[buttonIndex] as GamepadButton & { pressed: boolean; value: number }).pressed = false;
      (pads[padIndex].buttons[buttonIndex] as GamepadButton & { pressed: boolean; value: number }).value = 0;
    },
    { padIndex, buttonIndex }
  );
  await page.waitForTimeout(40);
}

const faceButton: Record<Position, number> = { up: 3, right: 1, down: 0, left: 2 };

function another(position: Position): Position {
  return position === "up" ? "right" : "up";
}

test.beforeEach(async ({ page }) => {
  await page.goto("/");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await muteAudio(page);
});

test("confirms a normal topic for three seconds or a new press before the question", async ({ page }, testInfo) => {
  const consoleErrors: string[] = [];
  page.on("pageerror", (error) => consoleErrors.push(error.message));
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });
  await page.getByRole("button", { name: "9", exact: true }).click();
  await page.getByRole("button", { name: "Начать игру" }).click();
  await waitForInputGate(page);
  const before = await storedState(page);
  expect(before.phase.kind).toBe("normal-topic");
  if (before.phase.kind !== "normal-topic") return;
  const chooser = before.phase.chooser as Team;
  const other = chooser === "green" ? "blue" : "green";
  await page.keyboard.press(keys[other].right);
  expect((await storedState(page)).phase).toMatchObject({ kind: "normal-topic", cursor: 0 });
  await page.keyboard.press(keys[chooser].right);
  const moved = await storedState(page);
  expect(moved.phase).toMatchObject({ kind: "normal-topic", cursor: 1 });
  await expect(page.locator(".topic-choice--current")).toHaveCount(1);
  await captureSettled(page, testInfo.outputPath("normal-topic-selection.png"));
  await expect(page.locator(".topic-confirmation-stage")).toHaveCount(0);
  await page.keyboard.down(confirmKey(chooser));
  await expect(page.locator(".topic-confirmation-stage")).toBeVisible();
  await expect(page.locator(".question-stage")).toHaveCount(0);
  const confirmation = await storedState(page);
  expect(confirmation.phase).toMatchObject({
    kind: "topic-confirmation",
    topicId: before.phase.candidates[1]
  });
  await page.waitForTimeout(120);
  expect((await storedState(page)).phase.kind).toBe("topic-confirmation");
  await page.keyboard.up(confirmKey(chooser));
  await captureSettled(page, testInfo.outputPath("topic-confirmation.png"));
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toBeVisible();
  const paused = await storedState(page);
  await page.waitForTimeout(300);
  const stillPaused = await storedState(page);
  expect(stillPaused.phase.remainingMs).toBe(paused.phase.remainingMs);
  await page.getByRole("button", { name: "Продолжить" }).click();
  await waitForInputGate(page);
  await page.waitForTimeout(3_100);
  await expect(page.locator(".question-stage")).toBeVisible();
  const answering = await storedState(page);
  expect(answering.phase.kind).toBe("answering");
  if (answering.phase.kind === "answering") expect(answering.phase.baseRemainingMs).toBeGreaterThan(9_800);

  await page.keyboard.press("Escape");
  await page.getByRole("button", { name: "Выйти в меню" }).click();
  await page.getByRole("button", { name: "Начать игру" }).click();
  await waitForInputGate(page);
  const second = await storedState(page);
  if (second.phase.kind !== "normal-topic") throw new Error("Expected topic choice");
  const secondChooser = second.phase.chooser as Team;
  await page.keyboard.press(confirmKey(secondChooser));
  await expect(page.locator(".topic-confirmation-stage")).toBeVisible();
  await waitForInputGate(page);
  await page.keyboard.press("w");
  await expect(page.locator(".question-stage")).toBeVisible();
  expect(consoleErrors).toEqual([]);
});

test("menu defaults, offline startup and responsive shell", async ({ context, page }, testInfo) => {
  const errors: string[] = [];
  const externalRequests: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("request", (request) => {
    const url = new URL(request.url());
    if (url.hostname !== "127.0.0.1") externalRequests.push(request.url());
  });

  await expect(page).toHaveTitle(/Mindbattle/);
  await expect(page.getByRole("heading", { level: 1, name: "Mindbattle" })).toBeVisible();
  await expect(page.getByRole("button", { name: "15", exact: true })).toHaveClass(/is-selected/);
  await expect(page.getByRole("button", { name: "2", exact: true })).toHaveClass(/is-selected/);
  await expect(page.getByRole("button", { name: "20 c", exact: true })).toHaveClass(/is-selected/);
  await expect(page.getByLabel("Собирать обратную связь по вопросам")).toBeChecked();
  await expect(page.getByText("90 c", { exact: true })).toBeVisible();
  await expect(
    page.getByLabel("Контроллер команды Зелёная").locator("option:checked")
  ).toHaveText("WASD");
  await expect(
    page.getByLabel("Контроллер команды Синяя").locator("option:checked")
  ).toHaveText("Стрелки");
  for (const team of ["Зелёная", "Синяя"]) {
    const fits = await page
      .getByLabel(`Контроллер команды ${team}`)
      .evaluate((select) => select.scrollWidth <= select.clientWidth);
    expect(fits).toBe(true);
  }

  const metrics = await page.evaluate(() => ({
    innerHeight,
    innerWidth,
    scrollHeight: document.documentElement.scrollHeight,
    scrollWidth: document.documentElement.scrollWidth
  }));
  expect(metrics.scrollWidth).toBeLessThanOrEqual(metrics.innerWidth);
  expect(metrics.scrollHeight).toBeLessThanOrEqual(metrics.innerHeight);
  await captureSettled(page, testInfo.outputPath("menu.png"));

  await page.getByText("Настройки").click();
  await captureSettled(page, testInfo.outputPath("menu-settings.png"));
  await page.getByLabel("Крупный текст").check();
  await page.getByLabel("Высокий контраст").check();
  await page.getByLabel("Без анимации").check();
  await page.reload();
  await page.getByText("Настройки").click();
  await expect(page.getByLabel("Крупный текст")).toBeChecked();
  await expect(page.getByLabel("Высокий контраст")).toBeChecked();
  await expect(page.getByLabel("Без анимации")).toBeChecked();
  await expect(page.locator("#root > div")).toHaveClass(/text-large/);
  await expect(page.locator("#root > div")).toHaveClass(/high-contrast/);
  await expect(page.locator("#root > div")).toHaveClass(/reduced-motion/);
  const accessibleMetrics = await page.evaluate(() => ({
    innerWidth,
    scrollWidth: document.documentElement.scrollWidth
  }));
  expect(accessibleMetrics.scrollWidth).toBeLessThanOrEqual(accessibleMetrics.innerWidth);
  await page.getByText("Настройки").click();
  await captureSettled(page, testInfo.outputPath("menu-accessible.png"));

  await context.setOffline(true);
  await page.getByRole("button", { name: "Начать игру" }).click();
  await expect(page.getByRole("heading", { name: /команда выбирает/ })).toBeVisible();
  await captureSettled(page, testInfo.outputPath("topic-selection.png"));
  await waitForInputGate(page);
  await chooseCurrentTopic(page);
  await expect(page.locator(".team-question-timer")).toHaveCount(2);
  await expect(page.locator(".team-question-timer--reserve")).toHaveCount(0);
  const accessibleRound = await storedState(page);
  const accessibleCorrect = accessibleRound.phase.round.correctPosition as Position;
  await answer(page, "green", accessibleCorrect);
  await answer(page, "blue", accessibleCorrect);
  await expect(page.locator(".question-stage--reveal")).toBeVisible();
  await waitForInputGate(page);
  await page.keyboard.press("w");
  await expect(page.getByRole("heading", { name: "Насколько вопрос был сложен для вашей команды?" })).toBeVisible();
  const feedbackMetrics = await page.locator(".difficulty-feedback-stage").evaluate((stage) => ({
    pageFits: document.documentElement.scrollWidth <= innerWidth,
    stageFits: stage.scrollWidth <= stage.clientWidth,
    pageHeightFits: document.documentElement.scrollHeight <= innerHeight
  }));
  expect(feedbackMetrics).toEqual({ pageFits: true, stageFits: true, pageHeightFits: true });
  await captureSettled(page, testInfo.outputPath("difficulty-feedback-accessible.png"));
  await waitForInputGate(page);
  await page.keyboard.press("a");
  await page.waitForTimeout(120);
  await page.keyboard.press("ArrowLeft");
  await waitForInputGate(page);
  await page.keyboard.press("Space");
  await page.waitForTimeout(120);
  await page.keyboard.press("ShiftRight");
  for (let index = 0; index < 3; index += 1) {
    await page.keyboard.press("s");
    await page.waitForTimeout(80);
    await page.keyboard.press("ArrowDown");
    await page.waitForTimeout(80);
  }
  await page.keyboard.press("Space");
  await page.waitForTimeout(120);
  await page.keyboard.press("ShiftRight");
  await expect(page.locator(".feedback-status--error")).toBeVisible();
  await captureSettled(page, testInfo.outputPath("difficulty-feedback-accessible-error.png"));
  expect(errors).toEqual([]);
  expect(externalRequests).toEqual([]);
});

test("skips question feedback without calling its API when the match setting is disabled", async ({ page }) => {
  let feedbackRequests = 0;
  page.on("request", (request) => {
    if (new URL(request.url()).pathname === "/api/difficulty-feedback") feedbackRequests += 1;
  });

  await page.locator(".preferences-panel summary").click();
  await page.getByLabel("Собирать обратную связь по вопросам").uncheck();
  await page.getByRole("button", { name: "9", exact: true }).click();
  await page.getByRole("button", { name: "Начать игру" }).click();
  expect((await storedState(page)).config.collectQuestionFeedback).toBe(false);
  await chooseCurrentTopic(page);
  const answering = await storedState(page);
  if (answering.phase.kind !== "answering") throw new Error("Expected answering phase");
  const correct = answering.phase.round.correctPosition as Position;
  await answer(page, "green", correct);
  await answer(page, "blue", correct);
  await expect(page.locator(".question-stage--reveal")).toBeVisible();
  await waitForInputGate(page);
  await page.keyboard.press("w");
  await expect(page.locator(".difficulty-feedback-stage")).toHaveCount(0);
  expect((await storedState(page)).phase.kind).toBe("normal-topic");
  expect(feedbackRequests).toBe(0);
});

test("plays a complete keyboard match through bonus veto, restore and sudden death", async ({ page }, testInfo) => {
  test.setTimeout(60_000);
  await page.getByRole("button", { name: "9", exact: true }).click();
  await page.getByRole("button", { name: "10 c", exact: true }).click();
  await page.getByRole("button", { name: "Начать игру" }).click();
  await waitForInputGate(page);

  for (let round = 0; round < 9; round += 1) {
    if (round === 2) {
      await expect(page.locator(".bonus-stage")).toBeVisible();
      await expect(page.locator(".bonus-stage .control-help")).toHaveText(
        "←/→ курсор · подтвердить запрет ЗSpaceСRight Shift · ↑ снять запрет"
      );
      const bonusFits = await page.locator(".bonus-stage").evaluate((stage) => ({
        pageFits: document.documentElement.scrollWidth <= innerWidth,
        stageFits: stage.scrollWidth <= stage.clientWidth
      }));
      expect(bonusFits).toEqual({ pageFits: true, stageFits: true });
      await captureSettled(page, testInfo.outputPath("bonus-veto.png"));
    }
    await chooseCurrentTopic(
      page,
      round === 2
        ? () => captureSettled(page, testInfo.outputPath("bonus-topic-confirmation.png"))
        : undefined
    );
    await waitForInputGate(page);

    if (round === 0) {
      await captureSettled(page, testInfo.outputPath("question.png"));
      await expect(page.getByRole("link", { name: /^Источник:/ })).toHaveCount(0);
    }

    if (round === 0) {
      await page.keyboard.press("Escape");
      await expect(page.getByRole("dialog")).toBeVisible();
      const atPause = await storedState(page);
      await page.waitForTimeout(350);
      const whilePaused = await storedState(page);
      expect(whilePaused.phase.baseRemainingMs).toBe(atPause.phase.baseRemainingMs);
      await page.getByRole("button", { name: "Продолжить" }).click();
      await waitForInputGate(page);

      await page.reload();
      await page.getByRole("button", { name: "Продолжить партию" }).click();
      await expect(page.getByRole("dialog")).toContainText("Партия восстановлена");
      await page.getByRole("button", { name: "Продолжить" }).click();
      await waitForInputGate(page);
    }

    const answering = await storedState(page);
    expect(answering.phase.kind).toBe("answering");
    const correct = answering.phase.round.correctPosition as Position;

    if (round === 0) {
      await answer(page, "green", another(correct));
      await expect(page.locator(".game-team-card--correct, .game-team-card--wrong")).toHaveCount(0);
      await expect(page.locator(".answer-option--correct, .answer-option--wrong")).toHaveCount(0);
      await answer(page, "green", correct);
    } else {
      await answer(page, "green", correct);
    }
    await answer(page, "blue", correct);

    await expect(page.locator(".question-stage--reveal")).toBeVisible();
    if (round === 0) {
      const sourceLink = page.getByRole("link", { name: /^Источник:/ });
      await expect(sourceLink).toHaveAttribute("href", /^https:\/\//);
      await expect(sourceLink).toHaveAttribute("target", "_blank");
      await expect(sourceLink).toHaveAttribute("rel", /noopener/);
      await expect(sourceLink).toHaveAttribute("rel", /noreferrer/);
    }
    await expect(page.getByText("Почему так?")).toBeVisible();
    if (round === 0) {
      await captureSettled(page, testInfo.outputPath("reveal.png"));
    }
    if (round === 0) {
      await rateDifficulty(page);
      await captureSettled(page, testInfo.outputPath("difficulty-feedback.png"));
    } else {
      await rateDifficulty(page);
    }

    if (round === 2 || round === 5) {
      await expect(page.locator(".standings-stage")).toBeVisible();
      if (round === 2) {
        await captureSettled(page, testInfo.outputPath("standings.png"));
      }
      await waitForInputGate(page);
      await page.keyboard.press("w");
    }
    await waitForInputGate(page);
  }

  await expect(page.locator(".standings-stage")).toContainText("Ничья за первое место");
  await captureSettled(page, testInfo.outputPath("tie-standings.png"));
  await waitForInputGate(page);
  await page.keyboard.press("w");
  await expect(page.locator(".final-veto-stage")).toBeVisible();
  await captureSettled(page, testInfo.outputPath("final-veto.png"));
  await chooseCurrentTopic(page, () => captureSettled(page, testInfo.outputPath("final-topic-confirmation.png")));
  const tieQuestion = await storedState(page);
  expect(tieQuestion.phase.kind).toBe("answering");
  expect(tieQuestion.phase.round.mode).toBe("tie-break");
  const correct = tieQuestion.phase.round.correctPosition as Position;
  await answer(page, "green", correct);
  await answer(page, "blue", another(correct));
  await expect(page.locator(".question-stage--reveal")).toBeVisible();
  await rateDifficulty(page);

  await expect(page.getByText("Зелёная команда")).toBeVisible();
  await expect(page.locator(".standings-table li").nth(0).locator(".standing-rank")).toHaveText("1");
  await expect(page.locator(".standings-table li").nth(1).locator(".standing-rank")).toHaveText("2");
  await expect(page.getByRole("button", { name: "Начать заново" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Выйти в меню" })).toBeVisible();
  await captureSettled(page, testInfo.outputPath("winner.png"));
  await page.getByRole("button", { name: "Выйти в меню" }).click();
  await expect(page.getByRole("button", { name: "Последние результаты" })).toHaveCount(0);
  await captureSettled(page, testInfo.outputPath("completed-menu.png"));
});

test("renders zero through three selected wrong-answer notes without overflow", async ({ page }, testInfo) => {
  await page.getByRole("button", { name: "9", exact: true }).click();
  await page.getByRole("button", { name: "Начать игру" }).click();
  await waitForInputGate(page);
  await chooseCurrentTopic(page);
  const answering = await storedState(page);
  if (answering.phase.kind !== "answering") throw new Error("Expected answering phase");
  const correct = answering.phase.round.correctPosition as Position;
  await answer(page, "green", correct);
  await answer(page, "blue", correct);
  await expect(page.locator(".question-stage--reveal")).toBeVisible();
  const revealSnapshot = await page.evaluate(() => {
    const source = localStorage.getItem("mindbattle:data:v1");
    if (!source) throw new Error("No persisted match");
    return JSON.parse(source);
  });

  for (const wrongCount of [0, 1, 2, 3]) {
    await page.evaluate(({ snapshot, wrongCount: count }) => {
      const data = structuredClone(snapshot);
      const state = data.lastMatch.state;
      const teamIds = ["green", "blue", "yellow", "red"];
      const positions = ["up", "right", "down", "left"];
      if (count === 3) {
        state.phase.round.questionId = "folklore-fairy-tales-leprechaun-ireland";
        state.phase.round.topicId = "folklore-fairy-tales";
        state.phase.round.difficulty = "easy";
        state.phase.round.answerOrder = ["answer-1", "answer-2", "answer-0", "answer-3"];
        state.phase.round.correctPosition = "right";
      }
      const correctPosition = state.phase.round.correctPosition;
      const wrongPositions = positions.filter((position) => position !== correctPosition);
      const teamTemplate = state.teams[0];
      state.config.teams = teamIds;
      state.teams = teamIds.map((id, index) =>
        state.teams[index] ?? { ...teamTemplate, id, score: 0, correct: 0, incorrect: 0, noAnswer: 0 }
      );
      state.phase.round.attempts = teamIds.map((teamId, index) => ({
        teamId,
        status: "answered",
        answer: index < count ? wrongPositions[index] : correctPosition
      }));
      state.phase.resolutions = teamIds.map((teamId, index) => ({
        teamId,
        answer: index < count ? wrongPositions[index] : correctPosition,
        result: index < count ? "wrong" : "correct"
      }));
      if (count === 3) {
        data.preferences = {
          ...data.preferences,
          muted: true,
          textSize: "large",
          highContrast: true,
          reducedMotion: true
        };
      }
      localStorage.setItem("mindbattle:data:v1", JSON.stringify(data));
    }, { snapshot: revealSnapshot, wrongCount });
    await page.reload();
    await page.getByRole("button", { name: "Продолжить партию" }).click();
    await page.getByRole("button", { name: "Продолжить" }).click();
    await expect(page.locator(".question-stage--reveal")).toBeVisible();
    await expect(page.locator(".wrong-answer-notes article")).toHaveCount(wrongCount);
    const answerAlignment = await page.locator(".answer-cross").evaluate((cross) => {
      const crossRect = cross.getBoundingClientRect();
      const textOffsets = [...cross.querySelectorAll<HTMLElement>(".answer-option")].map((option) => {
        const optionRect = option.getBoundingClientRect();
        const textRect = option.querySelector<HTMLElement>(".answer-text")!.getBoundingClientRect();
        return Math.abs(
          (optionRect.left + optionRect.right) / 2 - (textRect.left + textRect.right) / 2
        );
      });
      return {
        crossCenterOffset: Math.abs((crossRect.left + crossRect.right) / 2 - innerWidth / 2),
        maximumTextCenterOffset: Math.max(...textOffsets),
        minimumOptionHeight: Math.min(
          ...[...cross.querySelectorAll<HTMLElement>(".answer-option")].map(
            (option) => option.getBoundingClientRect().height
          )
        )
      };
    });
    expect(answerAlignment.crossCenterOffset).toBeLessThanOrEqual(1);
    expect(answerAlignment.maximumTextCenterOffset).toBeLessThanOrEqual(1);
    expect(answerAlignment.minimumOptionHeight).toBeGreaterThanOrEqual(52);
    if (wrongCount > 0) {
      const notesAlignment = await page.locator(".wrong-answer-notes").evaluate((notes) => {
        const notesRect = notes.getBoundingClientRect();
        const articleRects = [...notes.querySelectorAll("article")].map((article) =>
          article.getBoundingClientRect()
        );
        const widths = articleRects.map(({ width }) => width);
        return {
          leftGap: Math.abs(articleRects[0].left - notesRect.left),
          rightGap: Math.abs(notesRect.right - articleRects.at(-1)!.right),
          widthSpread: Math.max(...widths) - Math.min(...widths)
        };
      });
      expect(notesAlignment.leftGap).toBeLessThanOrEqual(1);
      expect(notesAlignment.rightGap).toBeLessThanOrEqual(1);
      expect(notesAlignment.widthSpread).toBeLessThanOrEqual(1);
    }
    if (wrongCount === 3) {
      await captureSettled(page, testInfo.outputPath("reveal-three-wrong-notes.png"));
    }
    const metrics = await page.locator(".question-stage--reveal").evaluate((stage) => ({
      pageWidthFits: document.documentElement.scrollWidth <= innerWidth,
      pageHeightFits: document.documentElement.scrollHeight <= innerHeight,
      stageWidthFits: stage.scrollWidth <= stage.clientWidth,
      stageHeightFits: stage.scrollHeight <= stage.clientHeight
    }));
    expect(metrics).toEqual({
      pageWidthFits: true,
      pageHeightFits: true,
      stageWidthFits: true,
      stageHeightFits: true
    });
  }
});

test("supports N+1 public bonus veto for three and four assigned teams", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "chromium-1280", "One viewport is enough for virtual-pad coverage");
  await page.addInitScript(() => {
    const makePad = (index: number) => ({
      index,
      id: `Virtual Xbox ${index}`,
      mapping: "standard",
      connected: true,
      timestamp: 0,
      axes: [],
      vibrationActuator: null,
      buttons: Array.from({ length: 16 }, () => ({ pressed: false, touched: false, value: 0 }))
    });
    const target = globalThis as typeof globalThis & { __mindbattlePads: Gamepad[] };
    target.__mindbattlePads = [makePad(0), makePad(1)] as unknown as Gamepad[];
    Object.defineProperty(navigator, "getGamepads", {
      configurable: true,
      value: () => target.__mindbattlePads
    });
  });

  for (const teamCount of [3, 4] as const) {
    await page.evaluate(() => localStorage.clear());
    await page.reload();
    await muteAudio(page);
    await page.locator(".preferences-panel summary").click();
    await page.getByLabel("Собирать обратную связь по вопросам").uncheck();
    await page.locator(".preferences-panel summary").click();
    await page.getByRole("button", { name: String(teamCount), exact: true }).click();
    await expect(page.getByRole("button", { name: "Начать игру" })).toBeDisabled();
    await page.getByLabel("Контроллер команды Жёлтая").selectOption("gamepad:0");
    if (teamCount === 4) {
      await page.getByLabel("Контроллер команды Красная").selectOption("gamepad:1");
    }
    await page.getByRole("button", { name: "9", exact: true }).click();
    await page.getByRole("button", { name: "Начать игру" }).click();
    await waitForInputGate(page);

    for (let round = 0; round < 2; round += 1) {
      const topicState = await storedState(page);
      expect(topicState.phase.kind).toBe("normal-topic");
      const chooser = topicState.phase.chooser as "green" | "blue" | "yellow" | "red";
      if (chooser === "green" || chooser === "blue") {
        await page.keyboard.press(confirmKey(chooser));
      } else {
        await pressVirtualPad(page, chooser === "yellow" ? 0 : 1, 0);
      }
      await expect(page.locator(".topic-confirmation-stage")).toBeVisible();
      await waitForInputGate(page);
      await pressVirtualPad(page, 0, 0);
      await expect(page.locator(".question-stage")).toBeVisible();
      const state = await storedState(page);
      const correct = state.phase.round.correctPosition as Position;
      await answer(page, "green", correct);
      await answer(page, "blue", correct);
      await pressVirtualPad(page, 0, faceButton[correct]);
      if (teamCount === 4) await pressVirtualPad(page, 1, faceButton[correct]);
      await expect(page.locator(".question-stage--reveal")).toBeVisible();
      await waitForInputGate(page);
      await page.keyboard.press("w");
      await expect(page.locator(".difficulty-feedback-stage")).toHaveCount(0);
      await waitForInputGate(page);
    }

    await expect(page.locator(".topic-veto")).toHaveCount(teamCount + 1);
    await page.keyboard.press("d");
    await page.keyboard.press("a");
    let vetoState = await storedState(page);
    expect(vetoState.phase.cursors.green).toBe(0);
    await page.keyboard.press("Space");
    await page.keyboard.press("ArrowRight");
    vetoState = await storedState(page);
    expect(vetoState.phase.cursors.blue).toBe(1);
    await page.keyboard.press("ShiftRight");
    await pressVirtualPad(page, 0, 15);
    await pressVirtualPad(page, 0, 15);
    vetoState = await storedState(page);
    expect(vetoState.phase.cursors.yellow).toBe(2);
    await pressVirtualPad(page, 0, 0);
    if (teamCount === 4) {
      await pressVirtualPad(page, 1, 15);
      await pressVirtualPad(page, 1, 15);
      await pressVirtualPad(page, 1, 15);
      vetoState = await storedState(page);
      expect(vetoState.phase.cursors.red).toBe(3);
      await pressVirtualPad(page, 1, 0);
    }
    await expect(page.locator(".topic-confirmation-stage")).toBeVisible();
    await expect(page.locator(".topic-confirmation-stage .stage-label")).toHaveText(
      "Бонусный вопрос · x2"
    );
    await waitForInputGate(page);
    await page.keyboard.press("w");
    await expect(page.locator(".question-stage")).toBeVisible();
  }
});

test("marks a zero-reserve team as no-answer at the base deadline", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "chromium-1280", "The real-time deadline is checked once");
  await page.getByRole("button", { name: "9", exact: true }).click();
  await page.getByRole("button", { name: "10 c", exact: true }).click();
  await page.getByRole("button", { name: "Начать игру" }).click();
  await waitForInputGate(page);
  await chooseCurrentTopic(page);
  await page.evaluate(() => {
    const key = "mindbattle:data:v1";
    const data = JSON.parse(localStorage.getItem(key)!);
    data.lastMatch.state.teams = data.lastMatch.state.teams.map((team: { id: string }) =>
      team.id === "blue" ? { ...team, reserveMs: 0 } : team
    );
    localStorage.setItem(key, JSON.stringify(data));
  });
  await page.reload();
  await page.getByRole("button", { name: "Продолжить партию" }).click();
  await page.getByRole("button", { name: "Продолжить" }).click();
  await waitForInputGate(page);
  await page.keyboard.press("w");

  await expect(page.locator(".question-stage--reveal")).toBeVisible({ timeout: 12_000 });
  await expect(page.locator(".game-team-card--no-answer")).toHaveCount(1);
  await expect(page.locator(".game-team-card--no-answer")).toContainText("Синяя");
});

test("shows each unanswered team its timer and switches to red reserve time", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "chromium-1280", "The real-time reserve transition is checked once");
  await page.getByRole("button", { name: "9", exact: true }).click();
  await page.getByRole("button", { name: "10 c", exact: true }).click();
  await page.getByRole("button", { name: "Начать игру" }).click();
  await waitForInputGate(page);
  await chooseCurrentTopic(page);

  await expect(page.locator(".team-question-timer")).toHaveCount(2);
  await expect(page.locator(".question-header .timer")).toHaveCount(0);
  await captureSettled(page, testInfo.outputPath("team-timers-base.png"));
  await answer(page, "green", "up");
  await expect(page.locator(".game-team-card", { hasText: "Зелёная" }).locator(".team-question-timer")).toHaveCount(0);

  await page.evaluate(() => {
    const key = "mindbattle:data:v1";
    const data = JSON.parse(localStorage.getItem(key)!);
    data.lastMatch.state.phase.baseRemainingMs = 0;
    localStorage.setItem(key, JSON.stringify(data));
  });
  await page.reload();
  await page.getByRole("button", { name: "Продолжить партию" }).click();
  await page.getByRole("button", { name: "Продолжить" }).click();

  const blueCard = page.locator(".game-team-card", { hasText: "Синяя" });
  await expect(blueCard.locator(".team-question-timer--reserve")).toBeVisible();
  await expect(blueCard.locator(".team-question-timer--reserve")).toHaveAttribute(
    "aria-label",
    "Расходуется запас времени"
  );
  await expect(page.locator(".game-team-card", { hasText: "Зелёная" }).locator(".team-question-timer")).toHaveCount(0);
  await captureSettled(page, testInfo.outputPath("team-timers-reserve.png"));
});

test("keeps a shared feedback result on screen until the server accepts an idempotent retry", async ({ page }, testInfo) => {
  let failed = false;
  let delayed = false;
  await page.route("**/api/difficulty-feedback", async (route) => {
    if (!failed) {
      failed = true;
      await route.abort("failed");
      return;
    }
    if (!delayed) {
      delayed = true;
      await new Promise((resolve) => setTimeout(resolve, 300));
    }
    await route.continue();
  });
  await page.getByRole("button", { name: "9", exact: true }).click();
  await page.getByRole("button", { name: "Начать игру" }).click();
  await waitForInputGate(page);
  await chooseCurrentTopic(page);
  const state = await storedState(page);
  const correct = state.phase.round.correctPosition as Position;
  await answer(page, "green", correct);
  await answer(page, "blue", correct);
  await expect(page.locator(".question-stage--reveal")).toBeVisible();
  await waitForInputGate(page);
  await page.keyboard.press("w");
  await expect(page.locator(".difficulty-feedback-stage")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Хотите пожаловаться на вопрос?" })).toBeVisible();
  await page.keyboard.press("Space");
  await expect(page.locator(".feedback-status--error")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Продолжаем игру" })).toBeVisible();
  await expect(page.locator(".feedback-tag-board")).toHaveCount(0);
  await captureSettled(page, testInfo.outputPath("difficulty-feedback-error.png"));
  const pending = await storedState(page);
  expect(pending.phase.kind).toBe("difficulty-feedback");
  expect(pending.phase).toMatchObject({ stage: "done", hasComplaint: false, complaintReasons: [] });
  await page.reload();
  await page.getByRole("button", { name: "Продолжить партию" }).click();
  await page.getByRole("button", { name: "Продолжить" }).click();
  await expect(page.locator(".difficulty-feedback-stage")).toBeVisible();
  await waitForInputGate(page);
  await page.keyboard.press("Space");
  await expect(page.locator(".feedback-status")).toContainText("Сохраняем фидбэк");
  await expect(page.locator(".difficulty-feedback-stage")).toHaveCount(0);
});
