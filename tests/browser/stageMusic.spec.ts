import { expect, test, type Page } from "@playwright/test";

async function observeAudio(page: Page) {
  await page.addInitScript(() => {
    const events: { action: string; path: string }[] = [];
    const sources: HTMLMediaElement[] = [];
    (window as Window & { __musicEvents?: typeof events }).__musicEvents = events;
    (window as Window & { __musicSources?: HTMLMediaElement[] }).__musicSources = sources;
    const play = HTMLMediaElement.prototype.play;
    const pause = HTMLMediaElement.prototype.pause;
    HTMLMediaElement.prototype.play = function () {
      events.push({ action: "play", path: new URL(this.src).pathname });
      if (this.src.includes("/quiz-v1/")) sources.push(this);
      this.muted = true; // Instrumented routing/decoding test, not human listening.
      return play.call(this);
    };
    HTMLMediaElement.prototype.pause = function () {
      events.push({ action: "pause", path: new URL(this.src).pathname });
      return pause.call(this);
    };
  });
}

async function events(page: Page, action: string, path: string) {
  return page.evaluate(({ action, path }) =>
    ((window as Window & { __musicEvents?: { action: string; path: string }[] }).__musicEvents ?? [])
      .filter(event => event.action === action && event.path === path).length, { action, path });
}

test("selected menu decodes, survives volume changes and resumes after mute", async ({ page }) => {
  await observeAudio(page);
  const response = await page.request.get("/audio/quiz-v1/menu.mp3");
  expect(response.ok()).toBe(true);
  expect(response.headers()["content-type"]).toContain("audio/mpeg");
  await page.goto("/");
  await page.getByRole("button", { name: "Настройки", exact: true }).click();
  await expect.poll(() => events(page, "play", "/audio/quiz-v1/menu.mp3")).toBeGreaterThan(0);
  const prior = await events(page, "play", "/audio/quiz-v1/menu.mp3");
  await page.getByRole("slider", { name: "Громкость музыки" }).fill("0.4");
  await page.getByRole("slider", { name: "Громкость эффектов" }).fill("0.8");
  expect(await events(page, "play", "/audio/quiz-v1/menu.mp3")).toBe(prior);
  expect(await page.evaluate(() => JSON.parse(localStorage.getItem("mindbattle:data:v1")!).preferences)).toMatchObject({ musicVolume: 0.4, effectsVolume: 0.8 });
  await page.getByRole("button", { name: "Звук включён", exact: true }).click();
  await expect.poll(() => events(page, "pause", "/audio/quiz-v1/menu.mp3")).toBeGreaterThan(0);
  await page.getByRole("button", { name: "Звук выключен", exact: true }).click();
  await expect.poll(() => events(page, "play", "/audio/quiz-v1/menu.mp3")).toBe(prior + 1);
});

for (const [index, theme] of [[0, "stage-one"], [5, "stage-two"], [10, "stage-three"]] as const) {
  test(`restores stage ${theme} and resumes its theme after pause`, async ({ page }) => {
    await observeAudio(page);
    await page.goto("/");
    await page.getByRole("button", { name: "На одном устройстве (2–4)", exact: true }).click();
    await page.getByRole("button", { name: "Начать игру", exact: true }).click();
    await expect(page.locator(".topic-cards--three")).toBeVisible();
    // Use an explicitly recorded restore fixture; not a claim of naturally played rounds.
    await page.evaluate(index => {
      const data = JSON.parse(localStorage.getItem("mindbattle:data:v1")!);
      data.lastMatch.state.mainQuestionIndex = index;
      localStorage.setItem("mindbattle:data:v1", JSON.stringify(data));
    }, index);
    await page.reload();
    await page.getByRole("button", { name: "Продолжить игру на одном устройстве", exact: true }).click();
    await page.getByRole("button", { name: "Продолжить", exact: true }).click();
    const path = `/audio/quiz-v1/${theme}.mp3`;
    await expect.poll(() => events(page, "play", path)).toBeGreaterThan(0);
    await expect.poll(() => page.evaluate(path =>
      ((window as Window & { __musicSources?: HTMLMediaElement[] }).__musicSources ?? [])
        .some(source => new URL(source.src).pathname === path && source.readyState >= 2 && source.duration > 89), path)).toBe(true);
    await page.waitForTimeout(800);
    const prior = await events(page, "play", path);
    await page.keyboard.press("Escape");
    await expect.poll(() => events(page, "pause", path)).toBeGreaterThan(0);
    await page.getByRole("button", { name: "Продолжить", exact: true }).click();
    await expect.poll(() => events(page, "play", path)).toBe(prior + 1);
  });
}

test("solo uses the calm selected theme and retains question cues", async ({ page }) => {
  await observeAudio(page);
  await page.goto("/");
  await page.getByRole("button", { name: "Одиночная игра", exact: true }).click();
  await expect.poll(() => events(page, "play", "/audio/quiz-v1/stage-one.mp3")).toBeGreaterThan(0);
  await page.locator(".topic-choice").first().click();
  await expect.poll(() => events(page, "play", "/audio/arena-v1/question-start.wav")).toBe(1);
  expect(await events(page, "play", "/audio/quiz-v1/stage-one.mp3")).toBe(1);
});

test("solo advances after the first completed bonus and restores the saved music stage", async ({ page }) => {
  await observeAudio(page);
  await page.goto("/");
  await page.getByRole("button", { name: "Настройки", exact: true }).click();
  await page.getByLabel("Собирать обратную связь по вопросам").uncheck();
  await page.getByRole("button", { name: "Назад", exact: true }).click();
  await page.getByRole("button", { name: "Одиночная игра", exact: true }).click();
  const answerCurrentQuestion = async (continueAfterReveal = true) => {
    const state = await page.evaluate(() => JSON.parse(localStorage.getItem("mindbattle:data:v1")!).lastSolo.state);
    await page.locator(`.solo-answer-button.answer-option--${state.phase.round.correctPosition}`).click();
    await expect(page.locator(".question-stage--reveal")).toBeVisible();
    if (continueAfterReveal) await page.locator(".question-stage--reveal .explanation").click();
  };
  for (let slot = 0; slot < 4; slot += 1) {
    await page.locator(".topic-choice").first().click();
    await answerCurrentQuestion();
  }
  expect(await events(page, "play", "/audio/quiz-v1/stage-two.mp3")).toBe(0);
  await page.getByRole("button", { name: "Принять риск" }).click();
  await answerCurrentQuestion(false);
  expect(await events(page, "play", "/audio/quiz-v1/stage-two.mp3")).toBe(0);
  await page.locator(".question-stage--reveal .explanation").click();
  expect(await page.evaluate(() => JSON.parse(localStorage.getItem("mindbattle:data:v1")!).lastSolo.state)).toMatchObject({ slotIndex: 5, musicStage: 1 });
  await expect.poll(() => events(page, "play", "/audio/quiz-v1/stage-two.mp3")).toBe(1);
  await page.reload();
  await page.getByRole("button", { name: "Продолжить одиночную игру", exact: true }).click();
  await page.getByRole("button", { name: "Продолжить", exact: true }).click();
  await expect.poll(() => events(page, "play", "/audio/quiz-v1/stage-two.mp3")).toBe(1);
});
