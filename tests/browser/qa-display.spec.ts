import { expect, test } from '@playwright/test';
import { snapshot } from './qa-phoneSnapshot';
for (const highContrast of [false, true]) test(`display reveal snapshot / contrast=${highContrast}`, async ({ page }, info) => {
  const phone = snapshot(12);
  const display = { ...phone, role: 'display', selfId: undefined, isLeader: false,
    view: { ...phone.view!, teams: phone.revealedChoices! } };
  await page.addInitScript(({ highContrast }) => {
    localStorage.setItem('mindbattle-network-credentials-v1', JSON.stringify([{ code: '1234', token: 'qa-display', role: 'display' }]));
    localStorage.setItem('mindbattle-network-preferences-v1', JSON.stringify({ volume: 0, muted: true, textSize: 'normal', highContrast, reducedMotion: true }));
  }, { highContrast });
  await page.route('**/api/network/stream?*', route => route.fulfill({ contentType: 'text/event-stream', body: `event: connected\ndata: {"generation":1}\n\ndata: ${JSON.stringify(display)}\n\n` }));
  await page.route('**/api/network/heartbeat?*', route => route.fulfill({ json: { ok: true } }));
  await page.goto('/network?muted=1');
  await expect(page.locator('.network-display .network-player-card')).toHaveCount(12);
  await expect(page.locator('.network-explanation > p')).toHaveCount(1);
  await expect(page.locator('.wrong-answer-notes article')).toHaveCount(3);
  await expect(page.locator('.network-turn-status')).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Дальше', exact: true })).toHaveCount(0);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await page.screenshot({ path: info.outputPath(`display-reveal-${highContrast}.png`), fullPage: true });
});
test('mobile menu and solo touch surface', async ({ page }, info) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/?muted=1');
  await expect(page.getByRole('button', { name: 'Одиночная игра', exact: true })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Рекорды', exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Одиночная игра', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Выберите тему' })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await page.screenshot({ path: info.outputPath('mobile-solo-smoke.png'), fullPage: true });
});
