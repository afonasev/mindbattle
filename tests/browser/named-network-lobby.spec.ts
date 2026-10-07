import { test, expect, type BrowserContext } from '@playwright/test';
import { selectNetworkGame } from './network-lobby-helpers';

test('named lobby: protected admission, server privacy, own return, leader and replay', async ({ browser, page }, info) => {
  const title = `Лобби ${crypto.randomUUID().slice(0, 8)}`;
  const contexts: BrowserContext[] = [];
  await page.goto('/network?muted=1');
  await page.getByLabel('Название игры', { exact: true }).fill(title);
  await page.getByLabel('Пароль игры (необязательно)', { exact: true }).fill('секрет');
  await page.getByRole('button', { name: 'Создать сетевую игру', exact: true }).click();
  await expect(page.locator('.network-room-title')).toHaveText(title);
  const credential = await page.evaluate(() => JSON.parse(localStorage.getItem('mindbattle-network-credentials-v1')!)[0]);
  try {
    const phones = [];
    for (let i = 0; i < 2; i++) {
      const context = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, baseURL: info.project.use.baseURL }); contexts.push(context);
      const phone = await context.newPage(); phones.push(phone); await phone.goto('/network?muted=1'); await selectNetworkGame(phone, title);
      await phone.getByLabel('Ваше имя', { exact: true }).fill(i === 0 ? 'Анна' : 'Борис');
      if (i === 0) {
        await phone.getByLabel('Пароль игры', { exact: true }).fill('wrong'); await phone.getByRole('button', { name: 'Подключиться', exact: true }).click();
        await expect(phone.getByRole('alert')).toHaveText('Неверный пароль игры');
        expect(await phone.evaluate(() => localStorage.getItem('mindbattle-network-credentials-v1'))).toBeNull();
      } else await expect(phone.locator('.network-current-leader')).toHaveText('Ведущий: Анна');
      await phone.getByLabel('Пароль игры', { exact: true }).fill('секрет'); await phone.getByRole('button', { name: 'Подключиться', exact: true }).click();
      await expect(phone.getByText('Вы в комнате. Ждём начала игры.')).toBeVisible();
    }
    await expect(page.locator('.network-heading-leader')).toHaveText('Ведущий: Анна');
    await page.locator('.network-roster li').filter({ hasText: 'Борис' }).getByRole('button', { name: 'Ведущий', exact: true }).click();
    await expect(phones[0].locator('.network-heading-leader')).toHaveText('Ведущий: Борис');
    await page.getByRole('button', { name: 'Начать игру', exact: true }).click();
    const stranger = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, baseURL: info.project.use.baseURL }); contexts.push(stranger);
    const outside = await stranger.newPage(); await outside.goto('/network?muted=1');
    await expect(outside.locator('.network-catalog-layout h1')).toHaveText('Выберите игру');
    const publicCatalog = await outside.request.post('/api/network/catalog', { data: {} });
    expect((await publicCatalog.json()).rooms.some((r: { code: string }) => r.code === credential.code)).toBe(false);
    expect((await outside.request.get(`/api/network/room?code=${credential.code}`)).status()).toBe(404);
    await phones[0].getByRole('button', { name: 'Меню', exact: true }).click();
    await phones[0].getByRole('button', { name: 'Каталог игр', exact: true }).click();
    const mine = phones[0].locator('.network-room-own').filter({ hasText: title });
    await expect(mine).toBeVisible(); await mine.click();
    await expect(phones[0].locator('.network-heading-leader')).toHaveText('Ведущий: Борис');
    await expect(phones[1].getByRole('dialog')).toBeVisible();
    await phones[1].getByRole('button', { name: 'Вернуться в лобби', exact: true }).click();
    await expect(page.locator('.network-room-title')).toHaveText(title);
    const reopened = await outside.request.post('/api/network/catalog', { data: {} });
    expect((await reopened.json()).rooms.find((r: { code: string }) => r.code === credential.code)).toMatchObject({ title, passwordProtected: true });
    await page.getByRole('button', { name: 'Закрыть комнату', exact: true }).click();
    expect((await (await outside.request.post('/api/network/catalog', { data: {} })).json()).rooms.some((r: { code: string }) => r.code === credential.code)).toBe(false);
  } finally { await Promise.all(contexts.map(c => c.close())); }
});

for (const [width, height, minimum] of [[390,844,6], [360,720,5]]) {
  test(`compact catalog ${width}x${height}: all pages accessible, no overflow`, async ({ page }, info) => {
    await page.setViewportSize({ width, height });
    const rooms = Array.from({ length: 12 }, (_, i) => ({ code: `layout-${i}`, title: `Вечер эрудитов ${i + 1}`, playerCount: i % 11, passwordProtected: i % 2 === 0, phase: 'lobby' }));
    await page.route('**/api/network/catalog', route => route.fulfill({ json: { rooms, ownRooms: [{ code: "own-layout", title: "Битва умов", playerCount: 4, passwordProtected: false, phase: "playing", role: "player", selfName: "Анна" }], invalidIndexes: [] } }));
    await page.goto('/network?muted=1');
    await expect(page.locator('.network-room-list')).toBeVisible();
    await expect.poll(() => page.locator('.network-room-list .network-room-row').count()).toBeGreaterThanOrEqual(minimum);
    const geometry = await page.evaluate(() => ({ width: innerWidth, documentWidth: document.documentElement.scrollWidth, height: innerHeight, documentHeight: document.documentElement.scrollHeight, bottom: document.querySelector('.network-list-pages')!.getBoundingClientRect().bottom, targets: [...document.querySelectorAll('.network-room-row')].map(r => r.getBoundingClientRect().height), scrollbar: getComputedStyle(document.documentElement).scrollbarWidth }));
    expect(geometry.documentWidth).toBe(geometry.width); expect(geometry.documentHeight).toBeLessThanOrEqual(geometry.height); expect(geometry.bottom).toBeLessThanOrEqual(geometry.height);
    expect(Math.min(...geometry.targets)).toBeGreaterThanOrEqual(44); expect(geometry.scrollbar).toBe('none');
    await page.screenshot({ path: info.outputPath(`catalog-${width}.png`), fullPage: true });
    for (let i = 0; i < 12; i++) {
      const next = page.getByRole('button', { name: 'Следующая страница', exact: true }); if (!await next.isEnabled()) break; await next.click();
    }
    await expect(page.locator('.network-room-list').getByText('Вечер эрудитов 12', { exact: true })).toBeVisible();
  });
}
