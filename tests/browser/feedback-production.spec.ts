import { expect, test } from "@playwright/test";

const event = (suffix: string) => ({
  schemaVersion: 3,
  eventId: `production-browser-${suffix}-${Date.now()}`,
  matchId: `production-match-${suffix}`,
  catalogRevision: "mindbattle-questions-2026-09-02-r3",
  questionId: "agriculture-01-1",
  assignedDifficulty: "easy",
  hasComplaint: false,
  complaintReasons: []
});

test("accepts anonymous feedback from two isolated browser contexts while public read stays closed", async ({ browser, page }) => {
  const secondContext = await browser.newContext();
  const secondPage = await secondContext.newPage();
  try {
    await Promise.all([page.goto("/?muted=1"), secondPage.goto("/?muted=1")]);
    const [first, second] = await Promise.all([
      page.evaluate(async (body) => (await fetch("/api/difficulty-feedback", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) })).status, event("first")),
      secondPage.evaluate(async (body) => (await fetch("/api/difficulty-feedback", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) })).status, event("second"))
    ]);
    expect([first, second]).toEqual([201, 201]);
    expect(await page.evaluate(async () => (await fetch("/api/difficulty-feedback/summary")).status)).toBe(404);
  } finally {
    await secondContext.close();
  }
});
