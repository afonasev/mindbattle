import { expect, test } from "@playwright/test";

test("loads and operates the Mindbattle shell without page errors", async ({ context, page }) => {
  const errors: string[] = [];
  const externalRequests: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("request", (request) => {
    const url = new URL(request.url());
    if (url.hostname !== "127.0.0.1") externalRequests.push(request.url());
  });

  await page.goto("/");

  await expect(page).toHaveTitle(/Mindbattle/);
  await expect(page.getByRole("heading", { level: 1, name: "Mindbattle" })).toBeVisible();
  const metrics = await page.evaluate(() => ({
    innerHeight,
    innerWidth,
    scrollHeight: document.documentElement.scrollHeight,
    scrollWidth: document.documentElement.scrollWidth
  }));
  expect(metrics.scrollWidth).toBeLessThanOrEqual(metrics.innerWidth);
  expect(metrics.scrollHeight).toBeLessThanOrEqual(metrics.innerHeight);

  await context.setOffline(true);
  await page.getByRole("button", { name: "Начать игру" }).click();
  await expect(page.getByRole("status")).toHaveText(
    "Игровой цикл будет подключён следующим OpenSpec change."
  );
  expect(errors).toEqual([]);
  expect(externalRequests).toEqual([]);
});
