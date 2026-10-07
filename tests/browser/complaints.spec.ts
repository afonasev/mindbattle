import { expect, test, type Page } from '@playwright/test';
import { openComplaint, pendingComplaints } from './complaintHelpers';
async function reveal(page: Page) {
  await page.goto('/?muted=1');
  await page.getByRole('button',{name:'Одиночная игра',exact:true}).click();
  await page.keyboard.press('Enter');
  const correct=await page.evaluate(() => JSON.parse(localStorage.getItem('mindbattle:data:v1')!).lastSolo.state.phase.round.correctPosition);
  await page.keyboard.press(({up:'w',right:'d',down:'s',left:'a'} as Record<string,string>)[correct]);
  await expect(page.locator('.question-stage--reveal')).toBeVisible();
}
test('phone complaint menu returns to the same reveal and fits the viewport',async ({page},testInfo) => {
  await page.setViewportSize({width:390,height:844});await reveal(page);
  const before=await page.evaluate(() => JSON.parse(localStorage.getItem('mindbattle:data:v1')!).lastSolo.state.phase);
  await openComplaint(page);await page.getByRole('button',{name:'Фактическая ошибка',exact:true}).click();
  await expect(page.getByRole('button',{name:'Сохранить жалобу',exact:true})).toBeInViewport();
  expect(await page.evaluate(() => document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  await page.screenshot({path:testInfo.outputPath('phone-complaint.png'),fullPage:true});
  await page.getByRole('button',{name:'Отмена',exact:true}).click();await expect(page.locator('.question-stage--reveal')).toBeVisible();
  expect(await page.evaluate(() => JSON.parse(localStorage.getItem('mindbattle:data:v1')!).lastSolo.state.phase)).toEqual(before);
  expect(await pendingComplaints(page)).toEqual([]);
});
test('local storage failure retains the complaint form and never claims successful saving',async ({page}) => {
  await reveal(page);await openComplaint(page);await page.locator('textarea').fill('Сохранить эту заметку');
  await page.evaluate(() => {
    const original=IDBObjectStore.prototype.add;
    IDBObjectStore.prototype.add=function(...args: Parameters<typeof original>) {
      if(this.name==='outbox'){this.transaction.abort();return original.apply(this,args);}
      return original.apply(this,args);
    };
  });
  await page.getByRole('button',{name:'Сохранить жалобу',exact:true}).click();
  await expect(page.getByRole('alert')).toContainText('Не удалось сохранить');
  await expect(page.locator('textarea')).toHaveValue('Сохранить эту заметку');expect(await pendingComplaints(page)).toEqual([]);
  await page.getByRole('button',{name:'Отмена',exact:true}).click();await expect(page.locator('.question-stage--reveal')).toBeVisible();
});

test('lost server acknowledgement retries the same complaint without another stored event',async ({page}) => {
  let lost=true;
  await page.route('**/api/difficulty-feedback',async route => {
    if(lost){await route.fetch();await route.abort('failed');}
    else await route.continue();
  });
  await reveal(page);await openComplaint(page);
  await page.getByRole('button',{name:'Фактическая ошибка',exact:true}).click();
  await page.getByRole('button',{name:'Сохранить жалобу',exact:true}).click();
  await expect.poll(async () => (await pendingComplaints(page)).length).toBe(1);
  const event=(await pendingComplaints(page))[0];
  await expect.poll(async () => {const response=await page.request.post('/api/difficulty-feedback',{data:event});return (await response.json()).status;}).toBe('duplicate');
  lost=false;await page.evaluate(() => window.dispatchEvent(new Event('online')));
  await expect.poll(async () => (await pendingComplaints(page)).length,{timeout:10000}).toBe(0);
  const replay=await page.request.post('/api/difficulty-feedback',{data:event});
  expect(await replay.json()).toEqual({status:'duplicate',eventId:event.eventId});
});
