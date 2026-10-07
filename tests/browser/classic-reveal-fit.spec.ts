import { test, expect } from "@playwright/test";
import { readFileSync } from "node:fs";
import fixture from "./classic-reveal-fixture.json" with { type: "json" };

// These actual catalog questions triggered overflowing reveals in the release gate.
const cases = [
  ["law-rights", "law-rights-negotiation"],
  ["rivers-lakes", "rivers-lakes-seasonal-flood-high-water"],
  ["video-game-history", "video-game-history-playstation-japan-year"],
  ["folklore-fairy-tales", "folklore-fairy-tales-leprechaun-ireland"]
];
test("classic long reveal retains full content and intrinsic cross geometry", async ({ page }, info) => {
  for (const [topicId, id] of cases) for (const accessible of [false, true]) {
    const question = JSON.parse(readFileSync(`src/content/topics/${topicId}.json`, "utf8")).questions.find((q: { id: string }) => q.id === id);
    const data = structuredClone(fixture);
    data.preferences = { ...data.preferences, textSize: accessible ? "large" : "normal", highContrast: accessible, muted: true, reducedMotion: true };
    const round = data.lastMatch.state.phase.round;
    Object.assign(round, { questionId: id, topicId, difficulty: question.difficulty, answerOrder: ["answer-0", "answer-1", "answer-2", "answer-3"], correctPosition: ["up", "right", "down", "left"][question.correctIndex] });
    await page.goto("/?muted=1");
    await page.evaluate(data => localStorage.setItem("mindbattle:data:v1", JSON.stringify(data)), data);
    await page.reload();
    await page.getByRole("button", { name: "Продолжить игру на одном устройстве" }).click();
    await page.getByRole("button", { name: "Продолжить", exact: true }).click();
    const stage = page.locator(".question-stage--reveal");
    await expect(stage).toBeVisible();
    await expect(stage.locator("h2")).toHaveText(question.prompt);
    await expect(stage.locator(".wrong-answer-notes article")).toHaveCount(3);
    await expect(stage.locator(".explanation > p")).toHaveText(question.explanation);
    await page.evaluate(() => document.fonts.ready);
    expect(await stage.evaluate(el => ({
      stageFits: el.scrollHeight <= el.clientHeight && el.scrollWidth <= el.clientWidth,
      pageFits: document.documentElement.scrollWidth <= innerWidth && document.documentElement.scrollHeight <= innerHeight,
      targetHeight: Math.min(...Array.from(el.querySelectorAll(".answer-option"), option => option.getBoundingClientRect().height))
    }))).toEqual({ stageFits: true, pageFits: true, targetHeight: expect.any(Number) });
    expect(await stage.locator(".answer-option").first().evaluate(el => el.getBoundingClientRect().height)).toBeGreaterThanOrEqual(52);
    await page.screenshot({ path: info.outputPath(`${id}-${accessible}.png`), fullPage: true });
  }
});
