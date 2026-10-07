import { expect, test } from '@playwright/test';
import { snapshot } from './qa-phoneSnapshot';

for (const count of [2, 12]) for (const accessible of [false, true]) {
  test(`network classic layout: ${count} players / accessible=${accessible}`, async ({ page }, info) => {
    const reveal = snapshot(count);
    const display = { ...reveal, role: 'display', selfId: undefined, isLeader: false,
      view: { ...reveal.view!, teams: reveal.revealedChoices! } };
    let payload: unknown = display;
    await page.addInitScript(({ accessible }) => {
      localStorage.setItem('mindbattle-network-credentials-v1', JSON.stringify([{ code: '1234', token: 'layout-display', role: 'display' }]));
      localStorage.setItem('mindbattle-network-preferences-v1', JSON.stringify({ volume: 0, muted: true, textSize: accessible ? 'large' : 'normal', highContrast: accessible, reducedMotion: true }));
    }, { accessible });
    await page.route('**/api/network/stream?*', route => route.fulfill({ contentType: 'text/event-stream', body: `event: connected\ndata: {"generation":1}\n\ndata: ${JSON.stringify(payload)}\n\n` }));
    await page.route('**/api/network/heartbeat?*', route => route.fulfill({ json: { ok: true } }));
    await page.goto('/network?muted=1');
    await expect(page.locator('.network-player-card')).toHaveCount(count);
    await expect(page.locator('.network-player-card--correct')).toHaveCount(count === 2 ? 1 : 3);
    await expect(page.locator('.network-explanation .wrong-answer-notes article')).toHaveCount(3);
    await expect(page.locator('.network-player-card strong')).toHaveText(display.view.teams.map(p => p.name));
    const geometry = await page.evaluate(() => {
      const area = document.querySelector('.network-question-area')!.getBoundingClientRect();
      const cards = [...document.querySelectorAll('.network-player-card')].map(card => {
        const rect = card.getBoundingClientRect();
        return { top: rect.top, width: rect.width, scroll: card.scrollWidth, client: card.clientWidth };
      });
      const options = [...document.querySelectorAll('.network-answers button')].map(el => { const r = el.getBoundingClientRect(); return { x: r.x, y: r.y }; });
      return { bottom: area.bottom, cards, options, scrollWidth: document.documentElement.scrollWidth, width: innerWidth };
    });
    expect(geometry.scrollWidth).toBeLessThanOrEqual(geometry.width);
    for (const card of geometry.cards) {
      expect(card.top).toBeGreaterThanOrEqual(geometry.bottom);
      expect(card.scroll).toBeLessThanOrEqual(card.client + 1);
    }
    expect(geometry.options[0].x).toBe(geometry.options[2].x);
    expect(geometry.options[1].y).toBe(geometry.options[3].y);
    expect(geometry.options[3].x).toBeLessThan(geometry.options[0].x);
    expect(geometry.options[1].x).toBeGreaterThan(geometry.options[0].x);
    await page.screenshot({ path: info.outputPath(`reveal-${count}-${accessible}.png`), fullPage: true });
    const { correctPosition: _correct, explanation: _explanation, answerNotes: _notes, ...question } = display.view.question!;
    payload = { ...display, phase: 'answering', revealedChoices: undefined, view: { ...display.view, phase: 'answering', question,
      teams: display.view.teams.map(({ result: _result, answerPosition: _answer, ...card }) => ({ ...card, remainingMs: 15_000 })) } };
    await page.reload();
    await expect(page.locator('.network-question-area:not(.revealed)')).toBeVisible();
    await expect(page.locator('.network-player-card')).toHaveCount(count);
    await expect(page.locator('.network-player-card[class*="network-player-card--"]')).toHaveCount(0);
    await expect(page.locator('.network-answers .correct, .network-answers .wrong')).toHaveCount(0);
    await expect(page.locator('.network-answers small, .network-explanation')).toHaveCount(0);
    await expect(page.locator('.network-player-card small')).toHaveText(display.view.teams.map(card => card.departed ? 'Выбыл' : 'Время: 15 с'));
    await page.screenshot({ path: info.outputPath(`answering-${count}-${accessible}.png`), fullPage: true });
  });
}
