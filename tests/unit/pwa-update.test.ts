import { describe, expect, it, vi } from "vitest";
import { canApplyPwaUpdate, checkForPwaUpdate, waitingUpdateInfo, waitingUpdateVersion } from "../../src/pwaUpdate";

describe("PWA update safety", () => {
  it("waits for menu or finished solo run", () => {
    expect(canApplyPwaUpdate(false, null)).toBe(true);
    expect(canApplyPwaUpdate(false, "finished")).toBe(true);
    expect(canApplyPwaUpdate(false, "answering")).toBe(false);
    expect(canApplyPwaUpdate(true, null)).toBe(false);
  });

  it("checks the registered worker immediately when the application starts", async () => {
    const update = vi.fn().mockResolvedValue(undefined);
    await checkForPwaUpdate({ update });
    expect(update).toHaveBeenCalledOnce();
  });

  it("does nothing when service workers are unavailable", async () => {
    await expect(checkForPwaUpdate(undefined)).resolves.toBeUndefined();
  });
});

describe('waiting update metadata', () => {
  it('reads publication metadata from the waiting worker and preserves legacy string requests', async () => {
    const worker = { postMessage: (message: string, ports: MessagePort[]) => ports[0].postMessage(message === 'mindbattle:update-info' ? { version: '2.0.0+B', publishedAt: '2026-10-10T07:15:00.000Z' } : '2.0.0+B') } as unknown as ServiceWorker;
    expect(await waitingUpdateVersion(worker)).toBe('2.0.0+B');
    expect(await waitingUpdateInfo(worker)).toEqual({ version: '2.0.0+B', publishedAt: '2026-10-10T07:15:00.000Z' });
  });
  it('handles older workers with no publication response without fabricating a date', async () => {
    const worker = { postMessage: (message: string, ports: MessagePort[]) => { if (message === 'mindbattle:update-version') ports[0].postMessage('1.0.0'); } } as unknown as ServiceWorker;
    expect(await waitingUpdateVersion(worker)).toBe('1.0.0');
    expect(await waitingUpdateInfo(worker, 10)).toBeUndefined();
  });
  it('discards malformed dates and versions', async () => {
    const worker = { postMessage: (_message: string, ports: MessagePort[]) => ports[0].postMessage({ version: '2.0.0', publishedAt: 'not-a-date' }) } as unknown as ServiceWorker;
    expect(await waitingUpdateInfo(worker)).toEqual({ version: '2.0.0', publishedAt: undefined });
    const invalid = { postMessage: (_message: string, ports: MessagePort[]) => ports[0].postMessage({ version: '<invalid>', publishedAt: '2026-10-10T07:15:00.000Z' }) } as unknown as ServiceWorker;
    expect(await waitingUpdateInfo(invalid)).toBeUndefined();
  });
});
