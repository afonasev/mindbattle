import { expect, test, type Page } from "@playwright/test";

type Team = "green" | "blue";
type Position = "up" | "right" | "down" | "left";

const keys: Record<Team, Record<Position, string>> = {
  green: { up: "w", right: "d", down: "s", left: "a" },
  blue: { up: "ArrowUp", right: "ArrowRight", down: "ArrowDown", left: "ArrowLeft" }
};

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

async function chooseCurrentTopic(page: Page) {
  const state = await storedState(page);
  if (state.phase.kind === "normal-topic") {
    await page.keyboard.press(state.phase.chooser === "green" ? "a" : "ArrowLeft");
    await expect(page.locator(".question-stage")).toBeVisible();
    return;
  }
  expect(state.phase.kind).toBe("bonus-veto");
  await expect(page.locator(".topic-veto")).toHaveCount(state.config.teams.length + 1);
  await page.keyboard.press("d");
  let vetoState = await storedState(page);
  expect(vetoState.phase.cursors.green).toBe(1);
  await page.keyboard.press("a");
  vetoState = await storedState(page);
  expect(vetoState.phase.cursors.green).toBe(0);
  await page.keyboard.press("s");
  vetoState = await storedState(page);
  expect(vetoState.phase.vetoes.green).toBe(vetoState.phase.candidates[0]);
  await page.keyboard.press("ArrowRight");
  vetoState = await storedState(page);
  expect(vetoState.phase.cursors.blue).toBe(1);
  await page.keyboard.press("ArrowDown");
  await expect(page.locator(".question-stage")).toBeVisible();
}

async function answer(page: Page, team: Team, position: Position) {
  await page.keyboard.press(keys[team][position]);
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

  await page.getByText("Звук и доступность").click();
  await page.getByLabel("Крупный текст").check();
  await page.getByLabel("Высокий контраст").check();
  await page.getByLabel("Без анимации").check();
  await page.reload();
  await page.getByText("Звук и доступность").click();
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
  await page.getByText("Звук и доступность").click();
  await captureSettled(page, testInfo.outputPath("menu-accessible.png"));

  await context.setOffline(true);
  await page.getByRole("button", { name: "Начать игру" }).click();
  await expect(page.getByRole("heading", { name: /команда выбирает/ })).toBeVisible();
  await captureSettled(page, testInfo.outputPath("topic-selection.png"));
  expect(errors).toEqual([]);
  expect(externalRequests).toEqual([]);
});

test("plays a complete keyboard match through bonus veto, restore and sudden death", async ({ page }, testInfo) => {
  await page.getByRole("button", { name: "9", exact: true }).click();
  await page.getByRole("button", { name: "10 c", exact: true }).click();
  await page.getByRole("button", { name: "Начать игру" }).click();
  await waitForInputGate(page);

  for (let round = 0; round < 9; round += 1) {
    if (round === 2) {
      await expect(page.locator(".bonus-stage")).toBeVisible();
      await expect(page.locator(".bonus-stage .control-help")).toHaveText(
        "←/→ курсор · ↓ запретить или заменить · ↑ снять запрет · D-pad / WASD / стрелки"
      );
      const bonusFits = await page.locator(".bonus-stage").evaluate((stage) => ({
        pageFits: document.documentElement.scrollWidth <= innerWidth,
        stageFits: stage.scrollWidth <= stage.clientWidth
      }));
      expect(bonusFits).toEqual({ pageFits: true, stageFits: true });
      await captureSettled(page, testInfo.outputPath("bonus-veto.png"));
    }
    await chooseCurrentTopic(page);
    await waitForInputGate(page);

    if (round === 0) {
      await captureSettled(page, testInfo.outputPath("question.png"));
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
    await expect(page.getByText("Почему так?")).toBeVisible();
    if (round === 0) {
      await captureSettled(page, testInfo.outputPath("reveal.png"));
    }
    await waitForInputGate(page);
    await page.keyboard.press("w");

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
  await waitForInputGate(page);
  const tieQuestion = await storedState(page);
  expect(tieQuestion.phase.kind).toBe("answering");
  expect(tieQuestion.phase.round.mode).toBe("tie-break");
  const correct = tieQuestion.phase.round.correctPosition as Position;
  await answer(page, "green", correct);
  await answer(page, "blue", another(correct));
  await expect(page.locator(".question-stage--reveal")).toBeVisible();
  await waitForInputGate(page);
  await page.keyboard.press("w");

  await expect(page.getByText("Зелёная команда")).toBeVisible();
  await expect(page.locator(".standings-table li").nth(0).locator(".standing-rank")).toHaveText("1");
  await expect(page.locator(".standings-table li").nth(1).locator(".standing-rank")).toHaveText("2");
  await expect(page.getByRole("button", { name: "Начать заново" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Выйти в меню" })).toBeVisible();
  await captureSettled(page, testInfo.outputPath("winner.png"));
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
      await page.locator(".topic-cards--three button").first().click();
      await waitForInputGate(page);
      const state = await storedState(page);
      const correct = state.phase.round.correctPosition as Position;
      await answer(page, "green", correct);
      await answer(page, "blue", correct);
      await pressVirtualPad(page, 0, faceButton[correct]);
      if (teamCount === 4) await pressVirtualPad(page, 1, faceButton[correct]);
      await expect(page.locator(".question-stage--reveal")).toBeVisible();
      await waitForInputGate(page);
      await page.keyboard.press("w");
      await waitForInputGate(page);
    }

    await expect(page.locator(".topic-veto")).toHaveCount(teamCount + 1);
    await page.keyboard.press("d");
    await page.keyboard.press("a");
    let vetoState = await storedState(page);
    expect(vetoState.phase.cursors.green).toBe(0);
    await page.keyboard.press("s");
    await page.keyboard.press("ArrowRight");
    vetoState = await storedState(page);
    expect(vetoState.phase.cursors.blue).toBe(1);
    await page.keyboard.press("ArrowDown");
    await pressVirtualPad(page, 0, 15);
    await pressVirtualPad(page, 0, 15);
    vetoState = await storedState(page);
    expect(vetoState.phase.cursors.yellow).toBe(2);
    await pressVirtualPad(page, 0, 13);
    if (teamCount === 4) {
      await pressVirtualPad(page, 1, 15);
      await pressVirtualPad(page, 1, 15);
      await pressVirtualPad(page, 1, 15);
      vetoState = await storedState(page);
      expect(vetoState.phase.cursors.red).toBe(3);
      await pressVirtualPad(page, 1, 13);
    }
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
