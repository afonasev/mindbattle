import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { forgetCredential, savedCredential, savedCredentials, saveCredential } from '../../src/network/client';
const key = 'mindbattle-network-credentials-v1';
let entries: Map<string,string>;
beforeEach(() => { entries = new Map(); vi.stubGlobal('localStorage', { getItem: (k: string) => entries.get(k) ?? null, setItem: (k: string, v: string) => entries.set(k,v) }); });
afterEach(() => vi.unstubAllGlobals());
it('accepts legacy same-browser credentials and ignores malformed storage', () => {
  const legacy = { code: '0001', token: 'existing-secret', role: 'player' as const };
  entries.set(key, JSON.stringify([legacy, null, { code: 'a', token: 4, role: 'player' }, { code: 'b', token: 'x', role: 'administrator' }]));
  expect(savedCredentials()).toEqual([legacy]); expect(savedCredential('0001','player')).toEqual(legacy);
  entries.set(key, '{}'); expect(savedCredentials()).toEqual([]);
  entries.set(key, 'broken'); expect(savedCredentials()).toEqual([]);
});
it('late invalidation cannot delete a newer credential for the same room', () => {
  const old = { code: 'same-room', token: 'old', role: 'player' as const };
  saveCredential(old); const current = { ...old, token: 'new' }; saveCredential(current);
  forgetCredential(old); expect(savedCredential('same-room')).toEqual(current);
  forgetCredential(current); expect(savedCredentials()).toEqual([]);
});
it('storage failure does not prevent entering a room', () => {
  vi.stubGlobal('localStorage', { getItem: () => { throw new Error('disabled'); }, setItem: () => { throw new Error('disabled'); } });
  expect(() => saveCredential({ code:'room',token:'secret',role:'player' })).not.toThrow(); expect(savedCredentials()).toEqual([]);
});
