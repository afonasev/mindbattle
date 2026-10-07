import { browserResults } from './outbox';
import { disableStoredStatistics, readStatisticsPreference, statisticsEnabled, writeStatisticsPreference } from './preference';
import { networkRequest, savedCredentials } from '../network/client';
import type { Credential } from '../network/protocol';
async function editPreference(edit: () => void): Promise<void> {
  if (navigator.locks) await navigator.locks.request('mindbattle-statistics-preference', edit);
  else edit();
}
let syncing: Promise<void> | undefined;
export function syncStatisticsRooms(): Promise<void> {
  if (syncing) return syncing;
  syncing = (async () => {
    let failure: unknown;
    let before: string;
    do {
    before = JSON.stringify([readStatisticsPreference(localStorage), savedCredentials()]);
    for (const credential of savedCredentials().filter(c => c.role === 'display')) {
      const current = readStatisticsPreference(localStorage);
      const revoke = current.revokedRooms.includes(credential.code);
      try {
        await networkRequest('statistics', { enabled: statisticsEnabled(), revision: current.revision ?? 0, generation: current.generation ?? 0 }, credential, AbortSignal.timeout(5000));
      } catch (error) {
        if (![403, 404].includes((error as { status?: number }).status ?? 0)) { failure = error; continue; }
      }
      await editPreference(() => {
        const next = readStatisticsPreference(localStorage);
        if (revoke && next.revision === current.revision) writeStatisticsPreference({ ...next, revokedRooms: next.revokedRooms.filter(code => code !== credential.code) });
      });
    }
    } while (before !== JSON.stringify([readStatisticsPreference(localStorage), savedCredentials()]));
    if (failure) throw failure;
  })().finally(() => { syncing = undefined; });
  return syncing;
}
export async function registerStatisticsRoom(credential: Credential, creationGeneration: number): Promise<void> {
  await editPreference(() => {
  const next = readStatisticsPreference(localStorage);
  if (!statisticsEnabled() || creationGeneration !== (next.generation ?? 0)) {
    writeStatisticsPreference({ ...next, revokedRooms: [...new Set([...next.revokedRooms, credential.code])] });
  }
  });
  // A room created across an off/on transition must revoke the old generation even if now enabled.
  await syncStatisticsRooms().catch(() => {});
}
export async function setStatisticsEnabled(enabled: boolean): Promise<void> {
  try { await editPreference(() => {
  const previous = readStatisticsPreference(localStorage);
  const revision = Math.max(Date.now(), (previous.revision ?? 0) + 1);
  const revokedRooms = enabled ? previous.revokedRooms : [...new Set([...previous.revokedRooms, ...savedCredentials().filter(c => c.role === 'display').map(c => c.code)])];
  const generation = (previous.generation ?? 0) + (enabled ? 0 : 1);
  writeStatisticsPreference({ ...previous, enabled, revision, generation, revokedRooms });
  }); }
  catch { await browserResults().disable(); throw new Error('Статистика выключена до закрытия страницы, но настройку не удалось сохранить на устройстве.'); }
  disableStoredStatistics(localStorage);
  await browserResults().disable();
  if (statisticsEnabled()) await browserResults().enable();
  try { await syncStatisticsRooms(); }
  catch { throw new Error('Настройка сохранена на устройстве. Сервер применит её после восстановления подключения.'); }
}
let initialized = false;
export function initializeStatistics(): void {
  if (initialized) return;
  initialized = true;
  const refresh = () => {
    if (!statisticsEnabled()) {
      try { disableStoredStatistics(localStorage); } catch { /* permission still blocks collection */ }
      void browserResults().disable().catch(() => {});
    } else void browserResults().enable();
    void syncStatisticsRooms().catch(() => {});
  };
  window.addEventListener('online', refresh);
  window.addEventListener('pageshow', refresh);
  window.addEventListener('focus', refresh);
  window.addEventListener('storage', refresh);
  window.addEventListener('mindbattle-statistics', refresh);
  setInterval(() => { void syncStatisticsRooms().catch(() => {}); }, 30_000);
  refresh();
}
