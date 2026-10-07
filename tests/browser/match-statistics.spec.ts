import { test, expect, type Page } from '@playwright/test';
const key = { up: 'KeyW', right: 'KeyD', down: 'KeyS', left: 'KeyA' };
async function queue(page: Page) {
  return page.evaluate(async () => {
    const db = await new Promise<IDBDatabase>((resolve, reject) => { const r = indexedDB.open('mindbattle-results-v1', 1); r.onsuccess = () => resolve(r.result); r.onerror = () => reject(r.error); });
    return await new Promise<{ eventId: string; kind: string; mode: string; correct: number }[]>((resolve, reject) => { const r = db.transaction('outbox').objectStore('outbox').getAll(); r.onsuccess = () => { resolve(r.result); db.close(); }; r.onerror = () => reject(r.error); });
  });
}
async function start(page: Page) {
  await page.goto('/?muted=1');
  await page.getByRole('button', { name: 'Настройки', exact: true }).click();
  await page.getByRole('button', { name: 'Звук включён', exact: true }).click();
  await page.getByRole('button', { name: 'Назад', exact: true }).click();
  await page.getByRole('button', { name: 'Одиночная игра' }).click();
  await page.keyboard.press('Enter');
}
async function answer(page: Page) {
  await expect(page.locator('.question-stage')).toBeVisible();
  const position = await page.evaluate(() => JSON.parse(localStorage.getItem('mindbattle:data:v1')!).lastSolo.state.phase.round.correctPosition as keyof typeof key);
  await page.keyboard.press(key[position]);
  await expect(page.locator('.question-stage--reveal')).toBeVisible();
}
test('persistent queue survives offline reload and sends on online without a statistics window', async ({ page, context }) => {
  await start(page);
  await page.evaluate(async () => { await navigator.serviceWorker.ready; });
  await page.reload(); // ensure service worker controls the document before offline reload
  await page.getByRole('button', { name: 'Продолжить одиночную игру' }).click();
  await page.keyboard.press('Escape'); // restored snapshot pauses the run
  await context.setOffline(true);
  await answer(page);
  await expect.poll(async () => (await queue(page)).filter(e => e.kind === 'question').length).toBe(1);
  const id = (await queue(page)).find(e => e.kind === 'question')!.eventId;
  await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { name: 'Выберите тему' })).toBeVisible();
  await page.reload();
  expect((await queue(page)).some(e => e.eventId === id)).toBe(true);
  await context.setOffline(false);
  await page.evaluate(() => window.dispatchEvent(new Event('online')));
  await expect.poll(async () => (await queue(page)).length).toBe(0);
});
test('unavailable endpoint do not delay continue; duplicate ACK clears reload replay', async ({ page }) => {
  let delivered = false;
  await page.route('**/api/match-results', route => route.fulfill({ status: 503, body: '{}' }));
  await start(page); await answer(page);
  await expect.poll(async () => (await queue(page)).filter(e => e.kind === 'question').length).toBe(1);
  const e = (await queue(page)).find(e => e.kind === 'question')!;
  const at = Date.now(); await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { name: 'Выберите тему' })).toBeVisible();
  expect(Date.now() - at).toBeLessThan(1500);
  await page.reload(); expect((await queue(page)).some(q => q.eventId === e.eventId)).toBe(true);
  await page.unroute('**/api/match-results');
  await page.route('**/api/match-results', async route => { const event = route.request().postDataJSON(); delivered = true; await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'duplicate', eventId: event.eventId }) }); });
  await page.evaluate(() => window.dispatchEvent(new Event('online')));
  await expect.poll(async () => (await queue(page)).length).toBe(0); expect(delivered).toBe(true);
});
test('finished solo retains all three revealed questions and the anonymous terminal result', async ({ page }) => {
  await page.route('**/api/match-results', route => route.fulfill({ status: 503, body: '{}' }));
  await start(page);
  for (let i = 0; i < 3; i++) {
    if (i) await page.keyboard.press('Enter');
    const pos = await page.evaluate(() => JSON.parse(localStorage.getItem('mindbattle:data:v1')!).lastSolo.state.phase.round.correctPosition as keyof typeof key);
    const wrong = pos === 'up' ? 'right' : 'up';
    await page.keyboard.press(key[wrong]);
    await expect(page.locator('.question-stage--reveal')).toBeVisible();
    await page.keyboard.press('Enter');
  }
  await expect(page.getByRole('heading', { name: 'Результат: 0', exact: true })).toBeVisible();
  await expect.poll(async () => (await queue(page)).filter(e => e.kind === 'question').length).toBe(3);
  await expect.poll(async () => page.evaluate(async () => {
    const r = indexedDB.open('mindbattle-results-v1'); const db = await new Promise<IDBDatabase>(resolve => r.onsuccess = () => resolve(r.result));
    const req = db.transaction('outbox').objectStore('outbox').getAll(); const events = await new Promise<{ kind: string; status: string; lives: number }[]>(resolve => req.onsuccess = () => resolve(req.result)); db.close();
    return events.some(e => e.kind === 'match' && e.status === 'completed' && e.lives === 0);
  })).toBe(true);
});
test('complete local two-team match persists nine questions, bonuses, tie-break and terminal score', async ({ page }) => {
  test.setTimeout(60_000);
  await page.route('**/api/match-results', route => route.fulfill({ status: 503, body: '{}' }));
  await page.goto('/?muted=1');
  await page.getByRole('button', { name: 'Настройки', exact: true }).click();
  await page.getByRole('button', { name: 'Звук включён', exact: true }).click();
  await page.getByRole('button', { name: 'Назад', exact: true }).click();
  await page.getByRole('button', { name: 'На одном устройстве (2–4)', exact: true }).click();
  await page.getByRole('button', { name: '9', exact: true }).click();
  await page.getByRole('button', { name: 'Начать игру', exact: true }).click();
  const state = () => page.evaluate(() => JSON.parse(localStorage.getItem('mindbattle:data:v1')!).lastMatch.state);
  const keys = { green: { up: 'w', right: 'd', down: 's', left: 'a' }, blue: { up: 'ArrowUp', right: 'ArrowRight', down: 'ArrowDown', left: 'ArrowLeft' } };
  for (let round = 0; round < 10; round++) {
    await page.waitForTimeout(100);
    let s = await state();
    if (s.phase.kind === 'standings') { await page.keyboard.press('w'); await page.waitForTimeout(100); s = await state(); }
    if (s.phase.kind === 'normal-topic') await page.keyboard.press(s.phase.chooser === 'green' ? 'Space' : 'ShiftRight');
    else {
      expect(['bonus-veto', 'final-veto']).toContain(s.phase.kind);
      await page.keyboard.press('Space'); await page.keyboard.press('ArrowRight'); await page.keyboard.press('ShiftRight');
    }
    await expect(page.locator('.topic-confirmation-stage')).toBeVisible();
    await page.waitForTimeout(100); await page.keyboard.press('w');
    await expect(page.locator('.question-stage')).toBeVisible();
    await page.waitForTimeout(100); s = await state();
    const correct = s.phase.round.correctPosition as keyof typeof key;
    await page.keyboard.press(keys.green[correct]);
    await page.keyboard.press(keys.blue[round === 9 ? correct === 'up' ? 'right' : 'up' : correct]);
    await expect(page.locator('.question-stage--reveal')).toBeVisible();
    await page.waitForTimeout(100); await page.keyboard.press('w');
  }
  await expect(page.getByRole('button', { name: 'Начать заново', exact: true })).toBeVisible();
  expect((await state()).phase.kind).toBe('finished');
  await expect.poll(async () => (await queue(page)).filter(e => e.kind === 'question').length).toBe(10);
  const events = await page.evaluate(async () => {
    const r = indexedDB.open('mindbattle-results-v1'); const db = await new Promise<IDBDatabase>(resolve => r.onsuccess = () => resolve(r.result));
    const req = db.transaction('outbox').objectStore('outbox').getAll(); const data = await new Promise<import('../../src/statistics/events').ResultEvent[]>(resolve => req.onsuccess = () => resolve(req.result)); db.close(); return data;
  });
  expect(events.filter(e => e.kind === 'question').every(e => e.eligible === 2)).toBe(true);
  expect(events.filter(e => e.kind === 'question' && e.roundKind === 'bonus')).toHaveLength(3);
  expect(events.find(e => e.roundKind === 'tie-break')).toMatchObject({ correct: 1, wrong: 1 });
  expect(events.find(e => e.status === 'completed')).toMatchObject({ winnerId: 'green' });
});
test('denied statistics storage does not interrupt answering or continuing', async ({ page }) => {
  const errors: string[] = []; page.on('pageerror', error => errors.push(error.message));
  await page.addInitScript(() => Object.defineProperty(window, 'indexedDB', { configurable: true, value: { open() { throw new DOMException('Storage denied', 'SecurityError'); } } }));
  await start(page); await answer(page); await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { name: 'Выберите тему' })).toBeVisible();
  expect(errors).toEqual([]);
});
