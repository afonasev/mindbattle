import { expect, type Page } from '@playwright/test';
export async function openComplaint(page: Page) {
  await page.getByRole('button', { name: 'Меню', exact: true }).click();
  await page.getByRole('button', { name: 'Пожаловаться на вопрос', exact: true }).click();
  await expect(page.getByRole('dialog', { name: 'Пожаловаться на вопрос' })).toBeVisible();
}
export async function pendingComplaints(page: Page): Promise<any[]> {
  return page.evaluate(async () => {
    const db = await new Promise<IDBDatabase>((resolve,reject) => { const request = indexedDB.open('mindbattle-feedback-v1'); request.onsuccess = () => resolve(request.result); request.onerror = () => reject(request.error); });
    try { return await new Promise<any[]>((resolve,reject) => { const tx=db.transaction('outbox'); const req=tx.objectStore('outbox').getAll(); tx.oncomplete=() => resolve(req.result);tx.onabort=tx.onerror=() => reject(tx.error); }); }
    finally { db.close(); }
  });
}
