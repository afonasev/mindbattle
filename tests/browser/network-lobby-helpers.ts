import { expect, type Page } from '@playwright/test';
export async function createNetworkGame(page: Page) {
  const title = `Тестовая игра ${crypto.randomUUID().slice(0, 8)}`;
  await page.getByLabel('Название игры', { exact: true }).fill(title);
  await page.getByRole('button', { name: 'Создать сетевую игру', exact: true }).click();
  await expect(page.locator('.network-room-title')).toHaveText(title);
  return title;
}
export async function selectNetworkGame(page: Page, title: string) {
  const row = page.locator('.network-room-row').filter({ has: page.getByText(title, { exact: true }) });
  // Prior tests may have left waiting rooms; paginate rather than assuming first page.
  await expect(page.locator(".network-room-list")).toBeVisible();
  for (let attempt = 0; attempt < 32; attempt++) {
    if (await row.count()) { await row.click(); return; }
    const next = page.getByRole('button', { name: 'Следующая страница', exact: true });
    if (await next.isEnabled().catch(() => false)) await next.click();
    else { await page.getByRole('button', { name: 'Обновить список', exact: true }).click(); await expect.poll(() => row.count(), { timeout: 5000 }).toBeGreaterThan(0); await row.click(); return; }
  }
  throw new Error(`Room not found: ${title}`);
}
