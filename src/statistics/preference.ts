import type { StorageLike } from '../adapters/storage';
export const STATISTICS_KEY = 'mindbattle:statistics-preference:v1';
export interface StatisticsPreference { version: 1; enabled: boolean; revokedRooms: string[]; generation?: number; revision?: number }
export function readStatisticsPreference(storage: StorageLike): StatisticsPreference {
  try {
    const raw = storage.getItem(STATISTICS_KEY);
    if (raw === null) return { version: 1, enabled: true, revokedRooms: [] };
    const value = JSON.parse(raw);
    if (value?.version !== 1 || typeof value.enabled !== 'boolean') throw Error('Invalid statistics preference');
    if ([value.generation, value.revision].some(number => number !== undefined && (!Number.isSafeInteger(number) || number < 0))) throw Error('Invalid statistics revision');
    return { version: 1, enabled: value.enabled, ...(value.generation !== undefined ? { generation: value.generation } : {}), ...(value.revision !== undefined ? { revision: value.revision } : {}), revokedRooms: Array.isArray(value.revokedRooms) ? value.revokedRooms.filter((code: unknown) => typeof code === 'string') : [] };
  } catch { return { version: 1, enabled: false, revokedRooms: [] }; }
}
export function statisticsGeneration(): number { return readStatisticsPreference(localStorage).generation ?? 0; }
let volatileOff = false;
export function statisticsEnabled(): boolean { return !volatileOff && readStatisticsPreference(localStorage).enabled; }
export function writeStatisticsPreference(value: StatisticsPreference): void {
  if (!value.enabled) volatileOff = true;
  try { localStorage.setItem(STATISTICS_KEY, JSON.stringify(value)); volatileOff = false; }
  finally { window.dispatchEvent(new Event('mindbattle-statistics')); }
}
export function disableStoredStatistics(storage: StorageLike): void {
  const raw = storage.getItem('mindbattle:data:v1');
  if (!raw) return;
  let data: any;
  try { data = JSON.parse(raw); } catch { return; }
  if (!data || typeof data !== 'object') return;
  let changed = false;
  for (const key of ['lastMatch', 'lastSolo']) {
    const state = data[key]?.state;
    if (state?.config && state.config.collectStatistics !== false) { state.config.collectStatistics = false; changed = true; }
  }
  if (changed) storage.setItem('mindbattle:data:v1', JSON.stringify(data));
}
