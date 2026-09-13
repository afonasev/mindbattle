import { expect, test } from "@playwright/test";

type Team = "green" | "blue";
type Position = "up" | "right" | "down" | "left";

const confirmKey = (team: Team) => team === "green" ? "Space" : "ShiftRight";

async function waitForInputGate(page: import("@playwright/test").Page) {
  await page.waitForTimeout(120);
}

async function storedState(page: import("@playwright/test").Page) {
  return page.evaluate(() => {
    const source = localStorage.getItem("mindbattle:data:v1");
    if (!source) throw new Error("No persisted match");
    return JSON.parse(source).lastMatch.state;
  });
}

test("loads the local arena palette across topic confirmation, timer, reserve and reveal", async ({ page }, testInfo) => {
  const requestedAudio = new Set<string>();
  const errors: string[] = [];
  await page.addInitScript(() => {
    const originalPlay = HTMLMediaElement.prototype.play;
    HTMLMediaElement.prototype.play = function () {
      const played = (window as Window & { __playedAudio?: string[] }).__playedAudio ?? [];
      played.push(new URL(this.currentSrc || this.src).pathname);
      (window as Window & { __playedAudio?: string[] }).__playedAudio = played;
      return originalPlay.call(this);
    };
  });
  page.on("request", (request) => {
    const url = new URL(request.url());
    if (url.pathname.startsWith("/audio/arena-v1/")) requestedAudio.add(url.pathname);
  });
  page.on("pageerror", (error) => errors.push(error.message));

  await page.goto("/");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await expect(page.getByRole("button", { name: "Одиночная игра", exact: true })).toBeVisible();
  expect(await page.locator(".menu-actions > *").allTextContents()).toEqual([
    "Одиночная игра",
    "На одном устройстве (2–4)",
    "Сетевая игра (2–12)",
    "Сетевая игра (2–12)",
    "Настройки",
    "Рекорды"
  ]);
  await page.getByRole("button", { name: "На одном устройстве (2–4)" }).click();
  await page.getByRole("button", { name: "9", exact: true }).click();
  await page.getByRole("button", { name: "10 c", exact: true }).click();
  await page.getByRole("button", { name: "На одном устройстве (2–4)" }).click();
  await waitForInputGate(page);

  const choosing = await storedState(page);
  expect(choosing.phase.kind).toBe("normal-topic");
  const chooser = choosing.phase.chooser as Team;
  await page.keyboard.press(confirmKey(chooser));
  await expect(page.locator(".topic-confirmation-stage")).toBeVisible();
  await expect.poll(() => requestedAudio.has("/audio/arena-v1/topic-countdown.wav")).toBe(true);
  await page.waitForTimeout(3_100);
  await expect(page.locator(".question-stage")).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath("audio-answering.png") });

  await page.waitForTimeout(10_300);
  await expect.poll(() => requestedAudio.has("/audio/arena-v1/timer-last-second.wav")).toBe(true);
  await expect.poll(() => requestedAudio.has("/audio/arena-v1/reserve-start.wav")).toBe(true);

  await page.keyboard.press("w");
  await page.keyboard.press("ArrowUp");
  await expect(page.locator(".question-stage--reveal")).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath("audio-reveal.png") });
  await expect.poll(async () => page.evaluate(() => (window as Window & { __playedAudio?: string[] }).__playedAudio ?? [])).toContainEqual(
    expect.stringMatching(/\/audio\/arena-v2\/reveal-(all|some|none)\.wav$/)
  );
  const playedAudio = await page.evaluate(() => (window as Window & { __playedAudio?: string[] }).__playedAudio ?? []);
  expect(playedAudio).toEqual(expect.arrayContaining([
    "/audio/arena-v2/menu-theme.wav",
    "/audio/arena-v2/game-theme.wav",
    "/audio/arena-v2/screen-transition.wav",
    "/audio/arena-v1/topic-countdown.wav",
    "/audio/arena-v1/question-start.wav",
    "/audio/arena-v1/timer-last-second.wav",
    "/audio/arena-v1/reserve-start.wav"
  ]));
  expect(errors).toEqual([]);
});

test("plays the arena palette in mobile solo", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.addInitScript(() => {
    const originalPlay = HTMLMediaElement.prototype.play;
    HTMLMediaElement.prototype.play = function () {
      const played = (window as Window & { __playedAudio?: string[] }).__playedAudio ?? [];
      played.push(new URL(this.currentSrc || this.src).pathname);
      (window as Window & { __playedAudio?: string[] }).__playedAudio = played;
      return originalPlay.call(this);
    };
  });
  await page.goto("/");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await page.getByRole("button", { name: "Одиночная игра" }).click();
  await expect(page.getByRole("heading", { name: "Выберите тему" })).toBeVisible();
  await page.locator(".topic-choice").first().click();
  await expect(page.locator(".solo-question")).toBeVisible();
  const correctPosition = await page.evaluate(() => {
    const source = localStorage.getItem("mindbattle:data:v1");
    if (!source) throw new Error("No persisted solo run");
    return JSON.parse(source).lastSolo.state.phase.round.correctPosition as Position;
  });
  const key: Record<Position, string> = { up: "KeyW", right: "KeyD", down: "KeyS", left: "KeyA" };
  await page.keyboard.press(key[correctPosition]);
  await expect(page.locator(".question-stage--reveal")).toBeVisible();
  const played = await page.evaluate(() => (window as Window & { __playedAudio?: string[] }).__playedAudio ?? []);
  expect(played).toEqual(expect.arrayContaining([
    "/audio/arena-v2/game-theme.wav",
    "/audio/arena-v1/question-start.wav",
    "/audio/arena-v2/reveal-all.wav"
  ]));
});

test("shows an immediate sound toggle in the main menu", async ({ page }, testInfo) => {
  await page.goto("/");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  const toggle = page.getByRole("button", { name: "Выключить звук", exact: true });
  await expect(toggle).toHaveAttribute("aria-pressed", "true");
  await page.screenshot({ path: testInfo.outputPath("menu-sound-toggle.png"), fullPage: true });
  await toggle.click();
  await expect(page.getByRole("button", { name: "Включить звук", exact: true })).toHaveAttribute("aria-pressed", "false");
  const actions = page.locator(".menu-actions");
  await expect(actions.getByRole("button", { name: "Настройки", exact: true })).toBeVisible();
  await expect(actions.getByRole("button", { name: "Рекорды", exact: true })).toBeVisible();
  const actionLabels = await actions.getByRole("button").allTextContents();
  expect(actionLabels.indexOf("Настройки")).toBeLessThan(actionLabels.indexOf("Рекорды"));
  await actions.getByRole("button", { name: "Настройки", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Настройки", exact: true })).toBeVisible();
  await expect(page.locator("details.preferences-panel")).toHaveCount(0);
  await page.screenshot({ path: testInfo.outputPath("menu-settings-submenu.png"), fullPage: true });
  await page.getByRole("button", { name: "Назад", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Настройки", exact: true })).toHaveCount(0);
});
