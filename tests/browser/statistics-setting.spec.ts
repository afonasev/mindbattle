import { expect, test, type Page } from '@playwright/test';
import { openComplaint, pendingComplaints } from './complaintHelpers';
const key='mindbattle:statistics-preference:v1';
async function resultQueue(page:Page) {
  return page.evaluate(async()=>{
    const r=indexedDB.open('mindbattle-results-v1',1);const db=await new Promise<IDBDatabase>((resolve,reject)=>{r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);});
    try {const tx=db.transaction('outbox');const req=tx.objectStore('outbox').getAll();return await new Promise<any[]>((resolve,reject)=>{tx.oncomplete=()=>resolve(req.result);tx.onabort=()=>reject(tx.error);});}
    finally {db.close();}
  });
}
async function settings(page:Page) {await page.getByRole('button',{name:'Настройки',exact:true}).click();}
async function solo(page:Page) {await page.getByRole('button',{name:'Одиночная игра',exact:true}).click();await page.keyboard.press('Enter');await expect(page.locator('.question-stage:not(.question-stage--reveal)')).toBeVisible();}
async function answer(page:Page) {
 const position=await page.evaluate(()=>JSON.parse(localStorage.getItem('mindbattle:data:v1')!).lastSolo.state.phase.round.correctPosition);
 await page.keyboard.press(({up:'w',right:'d',down:'s',left:'a'} as Record<string,string>)[position]);await expect(page.locator('.question-stage--reveal')).toBeVisible();
}
test('statistics default, durable off, complaints and new-match-only enable',async({page},testInfo)=>{
 let requests=0;page.on('request',request=>{if(new URL(request.url()).pathname==='/api/match-results')requests++;});
 await page.route('**/api/difficulty-feedback',route=>route.abort('failed'));
 await page.goto('/?muted=1');await settings(page);
 const checkbox=page.getByLabel('Отправлять анонимную статистику',{exact:true});await expect(checkbox).toBeChecked();
 await checkbox.uncheck();await expect(checkbox).toBeEnabled();
 await expect(page.getByText('Помогает улучшать вопросы и баланс игры. Без имён и данных устройства.')).toBeVisible();
 await page.screenshot({path:testInfo.outputPath('statistics-settings-desktop.png'),fullPage:true});
 await page.getByRole('button',{name:'Назад',exact:true}).click();await page.reload();
 await settings(page);await expect(checkbox).not.toBeChecked();await page.getByRole('button',{name:'Назад',exact:true}).click();
 await solo(page);await answer(page);expect(requests).toBe(0);expect(await resultQueue(page)).toEqual([]);
 await openComplaint(page);await page.getByRole('button',{name:'Фактическая ошибка',exact:true}).click();await page.getByRole('button',{name:'Сохранить жалобу',exact:true}).click();
 await expect.poll(async()=>(await pendingComplaints(page)).length).toBe(1);
 await page.getByRole('button',{name:'Меню',exact:true}).click();await settings(page);await checkbox.check();await expect(checkbox).toBeEnabled();
 await page.getByRole('button',{name:'Назад',exact:true}).click();await page.getByRole('button',{name:'Продолжить',exact:true}).click();
 expect(await page.evaluate(()=>JSON.parse(localStorage.getItem('mindbattle:data:v1')!).lastSolo.state.config.collectStatistics)).toBe(false);
 await page.keyboard.press('Enter');await page.keyboard.press('Enter');await answer(page);expect(requests).toBe(0);
 await page.getByRole('button',{name:'Меню',exact:true}).click();await page.getByRole('button',{name:'Выйти в меню',exact:true}).click();await solo(page);
 await expect.poll(()=>requests).toBeGreaterThan(0);
});
test('off purges old backlog and startup online cannot deliver it',async({page})=>{
 await page.route('**/api/match-results',route=>route.fulfill({status:503,body:'{}'}));
 await page.goto('/?muted=1');await solo(page);await answer(page);await expect.poll(async()=>(await resultQueue(page)).length).toBeGreaterThan(0);
 await page.getByRole('button',{name:'Меню',exact:true}).click();await settings(page);
 await page.getByLabel('Отправлять анонимную статистику',{exact:true}).uncheck();await expect(page.getByLabel('Отправлять анонимную статистику',{exact:true})).toBeEnabled();
 expect(await resultQueue(page)).toEqual([]);await page.reload();
 let sent=0;await page.unroute('**/api/match-results');page.on('request',request=>{if(new URL(request.url()).pathname==='/api/match-results')sent++;});
 await page.evaluate(()=>window.dispatchEvent(new Event('online')));await settings(page);
 await expect(page.getByLabel('Отправлять анонимную статистику',{exact:true})).not.toBeChecked();expect(await resultQueue(page)).toEqual([]);expect(sent).toBe(0);
});
test('phone statistics setting remains readable and storage failure is explicit',async({page},testInfo)=>{
 await page.setViewportSize({width:390,height:844});await page.goto('/?muted=1');await settings(page);
 await expect(page.getByLabel('Отправлять анонимную статистику',{exact:true})).toBeInViewport();
 await page.screenshot({path:testInfo.outputPath('statistics-settings-phone.png'),fullPage:true});
 await page.evaluate(()=>{const original=Storage.prototype.setItem;Storage.prototype.setItem=function(name,value){if(name==='mindbattle:statistics-preference:v1')throw Error('quota');return original.call(this,name,value);};});
 await page.getByLabel('Отправлять анонимную статистику',{exact:true}).uncheck();
 await expect(page.getByRole('alert')).toContainText('не удалось сохранить');
 expect(await page.evaluate(key=>localStorage.getItem(key),key)).toBeNull();
});
test('cross-tab decisions retain revocation and room creation applies the latest creator permission',async({page,context})=>{
 const other=await context.newPage();await page.goto('/network?muted=1');await other.goto('/?muted=1');await settings(other);
 let release!:()=>void;let created!:()=>void;const ready=new Promise<void>(resolve=>{created=resolve;});const hold=new Promise<void>(resolve=>{release=resolve;});
 const applied:any[]=[];page.on('request',request=>{if(new URL(request.url()).pathname==='/api/network/statistics')applied.push(request.postDataJSON());});
 await page.route('**/api/network/create',async route=>{const response=await route.fetch();created();await hold;await route.fulfill({response});});
 await page.getByLabel('Название игры',{exact:true}).fill('Creation permission race');await page.getByRole('button',{name:'Создать сетевую игру',exact:true}).click();await ready;
 const checkbox=other.getByLabel('Отправлять анонимную статистику',{exact:true});await checkbox.uncheck();await expect(checkbox).toBeEnabled();
 await checkbox.check();await expect(checkbox).toBeEnabled();release();
 await expect(page.locator('.network-room-title')).toHaveText('Creation permission race');
 await expect.poll(()=>applied.some(value=>value.enabled===true&&value.generation===1)).toBe(true);
 const permission=await other.evaluate(key=>JSON.parse(localStorage.getItem(key)!),key);expect(permission.generation).toBe(1);
 await page.goto('/?muted=1');await settings(page);
 await page.evaluate(()=>{(window as any).held=false;void navigator.locks.request('mindbattle-statistics-preference',async()=>{(window as any).held=true;await new Promise<void>(resolve=>{(window as any).releasePreference=resolve;});});});
 await expect.poll(()=>page.evaluate(()=>(window as any).held)).toBe(true);
 await Promise.all([page.getByLabel('Отправлять анонимную статистику',{exact:true}).uncheck(),checkbox.uncheck()]);
 await page.evaluate(()=>(window as any).releasePreference());
 await expect(page.getByLabel('Отправлять анонимную статистику',{exact:true})).toBeEnabled();await expect(checkbox).toBeEnabled();
 expect(await page.evaluate(key=>JSON.parse(localStorage.getItem(key)!).generation,key)).toBe(3);
});
