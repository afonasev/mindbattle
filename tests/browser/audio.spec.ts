import { expect, test } from "@playwright/test";

type Team = "green" | "blue";

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
  page.on("request", (request) => {
    const url = new URL(request.url());
    if (url.pathname.startsWith("/audio/arena-v1/")) requestedAudio.add(url.pathname);
  });
  page.on("pageerror", (error) => errors.push(error.message));

  await page.goto("/");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await page.getByRole("button", { name: "9", exact: true }).click();
  await page.getByRole("button", { name: "10 c", exact: true }).click();
  await page.getByRole("button", { name: "Начать игру" }).click();
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
  await expect.poll(() => requestedAudio.has("/audio/arena-v1/reveal.wav")).toBe(true);
  expect([...requestedAudio]).toEqual(expect.arrayContaining([
    "/audio/arena-v1/neon-arena.wav",
    "/audio/arena-v1/topic-countdown.wav",
    "/audio/arena-v1/question-start.wav",
    "/audio/arena-v1/timer-last-second.wav",
    "/audio/arena-v1/reserve-start.wav",
    "/audio/arena-v1/reveal.wav"
  ]));
  expect(errors).toEqual([]);
});
