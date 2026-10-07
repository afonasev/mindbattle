import { createNetworkGame, selectNetworkGame } from "./network-lobby-helpers";
import { expect, test, type Page } from "@playwright/test";

async function instrument(page: Page) {
  await page.addInitScript(() => {
    const events: { action: string; path: string; volume: number }[] = [];
    const sources: HTMLMediaElement[] = [];
    Object.assign(window, { __sfxEvents: events, __sfxSources: sources });
    const play = HTMLMediaElement.prototype.play;
    const pause = HTMLMediaElement.prototype.pause;
    HTMLMediaElement.prototype.play = function () {
      events.push({ action: "play", path: new URL(this.src).pathname, volume: this.volume });
      sources.push(this);
      this.muted = true; // Technical routing and real browser decode, not audible acceptance.
      return play.call(this);
    };
    HTMLMediaElement.prototype.pause = function () {
      events.push({ action: "pause", path: new URL(this.src).pathname, volume: this.volume });
      return pause.call(this);
    };
  });
}
async function count(page: Page, cue: string, action = "play") {
  return page.evaluate(({ cue, action }) => (window as any).__sfxEvents.filter((event: any) =>
    event.path === `/audio/quiz-sfx-v1/${cue}.wav` && event.action === action).length, { cue, action });
}
async function solo(page: Page) {
  await instrument(page);
  await page.goto("/");
  await page.getByRole("button", { name: "Настройки", exact: true }).click();
  await page.getByLabel("Собирать обратную связь по вопросам").uncheck();
  await page.getByRole("button", { name: "Назад", exact: true }).click();
  await page.getByRole("button", { name: "Одиночная игра", exact: true }).click();
  await page.locator(".topic-choice").first().click();
  await expect(page.locator(".solo-question")).toBeVisible();
}
async function position(page: Page, correct: boolean) {
  const answer = await page.evaluate(() => JSON.parse(localStorage.getItem("mindbattle:data:v1")!).lastSolo.state.phase.round.correctPosition);
  return correct ? answer : ["up", "right", "down", "left"].find(item => item !== answer)!;
}

test("all selected SFX decode with exact manifest duration in the real browser", async ({ page }) => {
  await page.goto("/?muted=1");
  const results = await page.evaluate(async () => {
    const manifest = await (await fetch("/audio/quiz-sfx-v1/manifest.json")).json();
    const context = new AudioContext();
    try {
      const decoded = [];
      for (const track of manifest.tracks) {
        const response = await fetch(`/audio/quiz-sfx-v1/${track.asset}`);
        if (!response.ok) throw new Error(track.asset);
        const audio = await context.decodeAudioData(await response.arrayBuffer());
        decoded.push({ cue: track.cue, channels: audio.numberOfChannels, durationMs: audio.duration * 1000, expected: track.duration_ms });
      }
      return decoded;
    } finally { await context.close(); }
  });
  expect(results).toHaveLength(13);
  for (const result of results) {
    expect(result.channels).toBe(2);
    expect(result.durationMs).toBeCloseTo(result.expected, 0);
  }
});

for (const correct of [true, false]) {
  test(`solo accepted ${correct ? "correct" : "wrong"} answer confirms before its distinct result and pause does not replay it`, async ({ page }) => {
    await solo(page);
    await page.locator(`.solo-answer-button.answer-option--${await position(page, correct)}`).click();
    await expect(page.locator(".question-stage--reveal")).toBeVisible();
    const cue = correct ? "reveal-all" : "reveal-none";
    expect(await count(page, "answer-locked")).toBe(1);
    expect(await count(page, cue)).toBe(1);
    expect(await count(page, correct ? "reveal-none" : "reveal-all")).toBe(0);
    const paths = await page.evaluate(() => (window as any).__sfxEvents.filter((item: any) => item.action === "play").map((item: any) => item.path));
    expect(paths.indexOf("/audio/quiz-sfx-v1/answer-locked.wav")).toBeLessThan(paths.indexOf(`/audio/quiz-sfx-v1/${cue}.wav`));
    await expect.poll(() => page.evaluate(cue => (window as any).__sfxSources.some((source: HTMLMediaElement) =>
      new URL(source.src).pathname === `/audio/quiz-sfx-v1/${cue}.wav` && source.readyState >= 2), cue)).toBe(true);
    await page.keyboard.press("Escape");
    await expect.poll(() => count(page, cue, "pause")).toBeGreaterThan(0);
    await page.getByRole("button", { name: "Продолжить", exact: true }).click();
    expect(await count(page, cue)).toBe(1);
    expect(await count(page, "answer-locked")).toBe(1);
  });
}

test("solo timeout uses its own result and no answer confirmation after restore", async ({ page }) => {
  await solo(page);
  // Explicit short-timer restore fixture; no claim of waiting a full natural timer.
  await page.keyboard.press("Escape");
  await page.evaluate(() => {
    const data = JSON.parse(localStorage.getItem("mindbattle:data:v1")!);
    data.lastSolo.state.phase.baseRemainingMs = 150;
    data.lastSolo.state.reserveMs = 0;
    localStorage.setItem("mindbattle:data:v1", JSON.stringify(data));
  });
  await page.reload();
  await page.getByRole("button", { name: "Продолжить одиночную игру", exact: true }).click();
  await page.getByRole("button", { name: "Продолжить", exact: true }).click();
  await expect(page.locator(".question-stage--reveal")).toBeVisible();
  expect(await count(page, "timeout")).toBe(1);
  expect(await count(page, "reveal-none")).toBe(0);
  expect(await count(page, "answer-locked")).toBe(0);
  await page.reload();
  await page.getByRole("button", { name: "Продолжить одиночную игру", exact: true }).click();
  await page.getByRole("button", { name: "Продолжить", exact: true }).click();
  await expect(page.locator(".question-stage--reveal")).toBeVisible();
  expect(await count(page, "timeout")).toBe(0);
});

test("network display owns timer/reserve/answer effects while both player browsers stay silent", async ({ page, browser }, testInfo) => {
  test.setTimeout(60000);
  await instrument(page);
  await page.goto("/network");
  const code = await createNetworkGame(page);
  const contexts = [];
  const phones: Page[] = [];
  try {
    for (let index = 0; index < 2; index++) {
      const context = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, baseURL: testInfo.project.use.baseURL });
      contexts.push(context);
      const phone = await context.newPage();
      phones.push(phone);
      await instrument(phone);
      await phone.goto("/network");
      await selectNetworkGame(phone, code);
      await phone.getByLabel("Ваше имя").fill(`Аудио ${index+1}`);
      await phone.getByRole("button", { name: "Подключиться", exact: true }).click();
    }
    await page.getByLabel("Время на ответ", { exact: true }).selectOption("10000");
    await page.getByRole("button", { name: "Начать игру", exact: true }).click();
    await expect.poll(async () => (await Promise.all(phones.map(phone => phone.getByRole("heading", { name: "Выберите тему", exact: true }).isVisible()))).indexOf(true)).toBeGreaterThanOrEqual(0);
    const chooser = await phones[0].getByRole("heading", { name: "Выберите тему", exact: true }).isVisible() ? phones[0] : phones[1];
    await chooser.locator(".network-topics button").first().click();
    await expect(phones[0].locator(".network-answers button").first()).toBeVisible();
    await expect.poll(() => count(page, "reserve-start"), { timeout: 16000 }).toBe(1);
    expect(await count(page, "timer-last-second")).toBe(5);
    await phones[0].locator(".network-answers button").first().click();
    await expect.poll(() => count(page, "answer-locked")).toBe(1);
    await phones[1].locator(".network-answers button").first().click();
    await expect.poll(() => count(page, "answer-locked")).toBe(2);
    await expect.poll(() => page.evaluate(() => (window as any).__sfxEvents.filter((event: any) => event.action === "play" && /quiz-sfx-v1\/reveal-(all|some|none)\.wav$/.test(event.path)).length)).toBe(1);
    for (const phone of phones) expect(await phone.evaluate(() => (window as any).__sfxEvents)).toEqual([]);
  } finally { await Promise.all(contexts.map(context => context.close())); }
});

test("natural solo finish plays victory through effects volume even with music at zero", async ({ page }) => {
  await solo(page);
  await page.keyboard.press("Escape");
  await page.getByRole("button", { name: "Настройки", exact: true }).click();
  await page.getByRole("slider", { name: "Громкость музыки" }).fill("0");
  await page.getByRole("slider", { name: "Громкость эффектов" }).fill("0.8");
  await page.getByRole("button", { name: "Назад", exact: true }).click();
  await page.getByRole("button", { name: "Продолжить", exact: true }).click();
  for (let round = 0; round < 3; round++) {
    if (round > 0) await page.locator(".topic-choice").first().click();
    await page.locator(`.solo-answer-button.answer-option--${await position(page, false)}`).click();
    await expect(page.locator(".question-stage--reveal")).toBeVisible();
    await page.locator(".question-stage--reveal .explanation").click();
  }
  await expect.poll(() => count(page, "winner")).toBe(1);
  const victory = await page.evaluate(() => (window as any).__sfxEvents.find((event: any) => event.action === "play" && event.path === "/audio/quiz-sfx-v1/winner.wav"));
  expect(victory.volume).toBeCloseTo(.8);
  await expect.poll(() => page.evaluate(() => (window as any).__sfxSources.some((source: HTMLMediaElement) =>
    new URL(source.src).pathname === "/audio/quiz-sfx-v1/winner.wav" && source.readyState >= 2))).toBe(true);
  expect(await count(page, "winner")).toBe(1);
});
