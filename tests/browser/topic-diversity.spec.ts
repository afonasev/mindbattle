import { createNetworkGame, selectNetworkGame } from "./network-lobby-helpers";
import { test, expect, type Page, type BrowserContext } from '@playwright/test';
import taxonomy from '../../src/content/taxonomy-manifest.json' with { type: 'json' };
const groups = Object.fromEntries(taxonomy.topics.map(t => [t.id, t.domain]));
const answerKeys = { green: { up: 'w', right: 'd', down: 's', left: 'a' }, blue: { up: 'ArrowUp', right: 'ArrowRight', down: 'ArrowDown', left: 'ArrowLeft' } };
async function settings(page: Page) {
  await page.goto('/?muted=1');
  await page.getByRole('button', { name: 'Настройки', exact: true }).click();
  const sound = page.getByRole('button', { name: 'Звук включён', exact: true });
  if (await sound.count()) await sound.click();
  await page.getByRole('button', { name: 'Назад', exact: true }).click();
}
function distinct(ids: string[]) { expect(ids.every(id => groups[id])).toBe(true); expect(new Set(ids.map(id => groups[id])).size).toBe(ids.length); }

test('solo ordinary choices have distinct groups and survive reload', async ({ page }, info) => {
  const errors: string[] = []; page.on('pageerror', e => errors.push(e.message));
  await settings(page); await page.getByRole('button', { name: 'Одиночная игра' }).click();
  const state = () => page.evaluate(() => JSON.parse(localStorage.getItem('mindbattle:data:v1')!).lastSolo.state);
  const first = await state(); distinct(first.phase.candidates);
  await page.screenshot({ path: info.outputPath('solo-topic-groups.png') });
  await page.reload(); await page.getByRole('button', { name: 'Продолжить одиночную игру', exact: true }).click();
  expect((await state()).phase.candidates).toEqual(first.phase.candidates);
  await page.getByRole('button', { name: 'Продолжить', exact: true }).click();
  await page.locator('.solo-topic-stage .topic-choice').first().click();
  await expect(page.locator('.question-stage')).toBeVisible(); await page.waitForTimeout(100);
  const question = await state(); const position = question.phase.round.correctPosition as keyof typeof answerKeys.green;
  await page.keyboard.press(answerKeys.green[position]); await expect(page.locator('.question-stage--reveal')).toBeVisible();
  await page.keyboard.press('Enter'); distinct((await state()).phase.candidates);
  expect(errors).toEqual([]); console.log('solo seed', first.seed);
});

test('classic ordinary, bonus and final groups remain distinct through a complete match', async ({ page }, info) => {
  test.setTimeout(60_000);
  const errors: string[] = []; page.on('pageerror', e => errors.push(e.message));
  await settings(page); await page.getByRole('button', { name: 'На одном устройстве (2–4)', exact: true }).click();
  await page.getByRole('button', { name: '9', exact: true }).click(); await page.getByRole('button', { name: 'Начать игру', exact: true }).click();
  const state = () => page.evaluate(() => JSON.parse(localStorage.getItem('mindbattle:data:v1')!).lastMatch.state);
  const observed: string[] = []; const seed = (await state()).seed;
  for (let round = 0; round < 10; round++) {
    await page.waitForTimeout(100); let s = await state();
    if (s.phase.kind === 'standings') { await page.keyboard.press('w'); await page.waitForTimeout(100); s = await state(); }
    distinct(s.phase.candidates);
    if (round === 0 || round === 2 || round === 9) await page.screenshot({ path: info.outputPath(`classic-groups-round-${round}.png`) });
    if (s.phase.kind === 'normal-topic') await page.keyboard.press(s.phase.chooser === 'green' ? 'Space' : 'ShiftRight');
    else { expect(['bonus-veto','final-veto']).toContain(s.phase.kind); await page.keyboard.press('Space'); await page.keyboard.press('ArrowRight'); await page.keyboard.press('ShiftRight'); }
    await expect(page.locator('.topic-confirmation-stage')).toBeVisible(); await page.waitForTimeout(100); await page.keyboard.press('w');
    await expect(page.locator('.question-stage')).toBeVisible(); await page.waitForTimeout(100); s = await state();
    observed.push(s.phase.round.questionId); const correct = s.phase.round.correctPosition as keyof typeof answerKeys.green;
    await page.keyboard.press(answerKeys.green[correct]);
    await page.keyboard.press(answerKeys.blue[round === 9 ? correct === 'up' ? 'right' : 'up' : correct]);
    await expect(page.locator('.question-stage--reveal')).toBeVisible(); await page.waitForTimeout(100); await page.keyboard.press('w');
  }
  expect((await state()).phase.kind).toBe('finished'); expect(new Set(observed).size).toBe(10); expect(errors).toEqual([]); console.log('classic seed', seed);
});

test('network authoritative three and five topic lists agree on display and phones', async ({ browser, page }, info) => {
  test.setTimeout(90_000); const errors: string[] = []; page.on('pageerror', e => errors.push(e.message));
  await page.goto('/network?muted=1'); const code = await createNetworkGame(page); const contexts: BrowserContext[] = []; const phones: Page[] = [];
  async function titles(p: Page) { return (await p.locator('.network-topics button').allTextContents()).map(text => {
    const t = taxonomy.topics.find(t => text.trim().startsWith(t.title)); expect(t).toBeTruthy(); return t!.id;
  }); }
  try {
    for (let i = 0; i < 4; i++) {
      const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, baseURL: info.project.use.baseURL }); contexts.push(ctx);
      const phone = await ctx.newPage(); phones.push(phone); phone.on('pageerror', e => errors.push(e.message));
      await phone.goto('/network?muted=1'); await selectNetworkGame(phone, code); await phone.getByLabel('Ваше имя').fill(`Тест ${i+1}`); await phone.getByRole('button', { name: 'Подключиться', exact: true }).click();
    }
    await page.getByLabel('Вопросов', { exact: true }).selectOption('9'); await page.getByRole('button', { name: 'Начать игру', exact: true }).click();
    for (let round = 0; round < 3; round++) {
      await expect(page.locator('.network-topics button')).toHaveCount(round === 2 ? 5 : 3);
      const ids = await titles(page); distinct(ids);
      for (const phone of phones) { await expect(phone.locator('.network-topics button')).toHaveCount(ids.length); expect(await titles(phone)).toEqual(ids); }
      if (round === 2) {
        await page.screenshot({ path: info.outputPath('network-five-topic-groups.png') });
        for (let i = 0; i < 4; i++) await phones[i].locator('.network-topics button').nth(i).click();
      } else {
        const chooser = await Promise.all(phones.map(p => p.getByRole('heading', { name: 'Выберите тему', exact: true }).isVisible()));
        await phones[chooser.indexOf(true)].locator('.network-topics button').first().click();
      }
      await expect(phones[0].locator('.network-confirmation')).toBeVisible(); await phones[0].locator('.network-header').click();
      for (let i = 0; i < 4; i++) await phones[i].locator('.network-answers button').nth(i).click();
      await expect(page.locator('.network-answers .correct')).toHaveCount(1);
      await phones[0].locator('.network-round-heading').getByRole('button', { name: 'Дальше', exact: true }).click();
    }
    expect(errors).toEqual([]); console.log('network QA room', code);
  } finally { for (const ctx of contexts) await ctx.close(); }
});
