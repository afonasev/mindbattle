// Only for positive assertions immediately after navigation to a lazy-rendered UI.
// Browser-side RAF polling avoids the locator retry backoff while the DOM mounts.
// Mount and the unchanged assertion share the original 5s assertion budget.
export async function expectAfterMount(page, selector, assertion, timeout = 5000) {
  if (!Number.isFinite(timeout) || timeout <= 0) throw new Error('Expected a finite positive assertion timeout');
  const started = performance.now();
  const handle = await page.waitForFunction(css => document.querySelector(css) !== null, selector, { polling: 'raf', timeout });
  await handle.dispose();
  const remaining = timeout - (performance.now() - started);
  // Playwright interprets zero as unlimited. Never turn an exhausted budget into that.
  if (remaining <= 0) throw new Error(`UI did not mount within the ${timeout}ms assertion budget: ${selector}`);
  await assertion({ timeout: remaining });
}
