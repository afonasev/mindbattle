import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createServer, type Server } from 'node:http';
import { once } from 'node:events';
import type { Credential, NetworkSnapshot } from '../../src/network/protocol';
const hashGate = vi.hoisted(() => ({ blocked: false, jobs: [] as Array<() => void> }));
vi.mock('node:crypto', async (original) => {
  const crypto = await original<typeof import('node:crypto')>();
  return { ...crypto, scrypt: (password: string, salt: Buffer, _length: number, callback: (error: Error | null, key: Buffer) => void) => {
    const finish = () => callback(null, crypto.createHash('sha256').update(password).update(salt).digest());
    if (hashGate.blocked) hashGate.jobs.push(finish); else queueMicrotask(finish);
  } };
});
import { createNetworkApi } from '../../server/network';
let server: Server, origin: string;
const streams: AbortController[] = [];
async function request(path: string, body: unknown = {}, credential?: Credential) {
  const response = await fetch(`${origin}/api/network/${path}${credential ? `?code=${credential.code}` : ''}`, { method: 'POST', headers: { 'content-type': 'application/json', ...(credential ? { authorization: `Bearer ${credential.token}` } : {}) }, body: JSON.stringify(body) });
  return { status: response.status, value: await response.json() };
}
async function create(title = 'Одинаковое название', password = '') {
  const result = await request('create', { title, password });
  expect(result.status).toBe(201);
  return result.value as Credential;
}
async function join(display: Credential, name: string, password = '') {
  const result = await request('join', { code: display.code, name, password });
  expect(result.status).toBe(201);
  return result.value as Credential;
}
async function connect(credential: Credential) {
  const abort = new AbortController(); streams.push(abort);
  const response = await fetch(`${origin}/api/network/stream?code=${credential.code}`, { headers: { authorization: `Bearer ${credential.token}` }, signal: abort.signal });
  expect(response.status).toBe(200);
  const reader = response.body!.getReader();
  const chunk = await reader.read();
  const events = new TextDecoder().decode(chunk.value).split('\n\n');
  const snapshot = events.find(e => e.startsWith('data: '));
  expect(snapshot).toBeTruthy();
  return JSON.parse(snapshot!.slice(6)) as NetworkSnapshot;
}
async function command(credential: Credential, action: unknown) {
  const snap = await connect(credential);
  return request('command', { commandId: crypto.randomUUID(), epoch: snap.epoch, phaseRevision: snap.phaseRevision, action }, credential);
}
beforeEach(async () => {
  hashGate.blocked = false; hashGate.jobs.length = 0;
  const api = createNetworkApi(async () => {});
  server = createServer((req, res) => { void api(req, res); });
  server.listen(0, '127.0.0.1'); await once(server, 'listening');
  const address = server.address(); if (!address || typeof address === 'string') throw new Error('No address');
  origin = `http://127.0.0.1:${address.port}`;
});
afterEach(async () => { hashGate.blocked = false; hashGate.jobs.splice(0).forEach(f => f()); streams.splice(0).forEach(s => s.abort()); server.closeAllConnections(); await new Promise<void>(resolve => server.close(() => resolve())); });
describe('named network lobby API', () => {
  it('projects waiting rooms without secrets; verifies password and existing membership independently', async () => {
    expect((await request('create', {})).status).toBe(400);
    expect((await request('create', { title: '\u0000' })).status).toBe(400);
    const display = await create('Защищённая', 'пароль');
    const other = await create('Защищённая');
    const publicList = await request('catalog');
    expect(publicList.value.rooms.map((r: { code: string }) => r.code)).toEqual([display.code, other.code]);
    expect(publicList.value.rooms[0]).toEqual({ code: display.code, title: 'Защищённая', playerCount: 0, passwordProtected: true, phase: 'lobby' });
    expect(JSON.stringify(publicList.value)).not.toMatch(/token|salt|hash|players|leaderName/);
    expect((await request('join', { code: display.code, name: 'Анна', password: 'неверный' })).status).toBe(403);
    const player = await join(display, 'Анна', 'пароль');
    const list = await request('catalog', { credentials: [{ ...player, role: 'display' }, { ...display, token: 'forged' }] });
    expect(list.value.ownRooms[0]).toMatchObject({ role: 'player', selfName: 'Анна', leaderName: 'Анна' });
    expect(list.value.invalidIndexes).toEqual([1]);
    expect(JSON.stringify(list.value)).not.toContain(player.token);
    const detail = await fetch(`${origin}/api/network/room?code=${display.code}`);
    expect(await detail.json()).toMatchObject({ leaderName: 'Анна' });
    expect((await request('catalog', { credentials: Array(21).fill(player) })).status).toBe(400);
  });
  it('hides started rooms server-side, preserves own return and reopens the same protection on replay', async () => {
    const display = await create('Партия', 'pw');
    const first = await join(display, 'Анна', 'pw'); const second = await join(display, 'Борис', 'pw');
    await connect(first); await connect(second);
    expect((await command(display, { type: 'start' })).status).toBe(200);
    expect((await request('catalog')).value.rooms).toEqual([]);
    expect((await fetch(`${origin}/api/network/room?code=${display.code}`)).status).toBe(404);
    const own = await request('catalog', { credentials: [display, first, { ...first, token: 'forged' }] });
    expect(own.value.ownRooms).toHaveLength(2); expect(own.value.invalidIndexes).toEqual([2]);
    expect(own.value.ownRooms[1]).toMatchObject({ phase: 'playing', leaderName: 'Анна' });
    expect((await request('join', { code: display.code, name: 'Новый', password: 'pw' })).status).toBe(404);
    expect((await command(first, { type: 'replay' })).status).toBe(200);
    expect((await request('catalog')).value.rooms[0]).toMatchObject({ title: 'Партия', passwordProtected: true, playerCount: 2 });
    expect((await request('join', { code: display.code, name: 'Новый', password: 'wrong' })).status).toBe(403);
    expect((await command(display, { type: 'remove', playerId: 'player-1' })).status).toBe(200);
    const revoked = await request('catalog', { credentials: [first, second] });
    expect(revoked.value.invalidIndexes).toEqual([0]); expect(revoked.value.ownRooms[0].leaderName).toBe('Борис');
    expect((await command(display, { type: 'close' })).status).toBe(200);
    expect((await request('catalog')).value.rooms).toEqual([]);
  });
  it('does not admit a password verification that finishes after start or close', async () => {
    const display = await create('Гонка', 'pw');
    const first = await join(display, 'А', 'pw'); const second = await join(display, 'Б', 'pw');
    await connect(first); await connect(second); await connect(display);
    hashGate.blocked = true;
    const pending = request('join', { code: display.code, name: 'Поздний', password: 'pw' });
    await vi.waitFor(() => expect(hashGate.jobs).toHaveLength(1));
    expect((await command(display, { type: 'start' })).status).toBe(200);
    hashGate.jobs.splice(0).forEach(f => f());
    expect((await pending).status).toBe(409);
    expect((await request('catalog', { credentials: [display] })).value.ownRooms[0].playerCount).toBe(2);
    hashGate.blocked = false;
    const closing = await create('Закрытие', 'pw');
    hashGate.blocked = true;
    const afterClose = request('join', { code: closing.code, name: 'Поздний', password: 'pw' });
    await vi.waitFor(() => expect(hashGate.jobs).toHaveLength(1));
    expect((await command(closing, { type: 'close' })).status).toBe(200);
    hashGate.jobs.splice(0).forEach(f => f());
    expect([404,410]).toContain((await afterClose).status);
  });
  it('serializes final-seat joins and rechecks the room cap after async hashing', async () => {
    const display = await create('Места', 'pw');
    for (let i = 0; i < 11; i++) await join(display, `Игрок ${i}`, 'pw');
    hashGate.blocked = true;
    const a = request('join', { code: display.code, name: 'А', password: 'pw' });
    const b = request('join', { code: display.code, name: 'Б', password: 'pw' });
    await vi.waitFor(() => expect(hashGate.jobs).toHaveLength(2)); hashGate.jobs.splice(0).forEach(f => f());
    expect([(await a).status, (await b).status].sort()).toEqual([201,409]);
    hashGate.blocked = false;
    for (let i = 0; i < 30; i++) await create(`Комната ${i}`);
    hashGate.blocked = true;
    const first = request('create', { title: '32', password: 'pw' }); const last = request('create', { title: '33', password: 'pw' });
    await vi.waitFor(() => expect(hashGate.jobs).toHaveLength(2)); hashGate.jobs.splice(0).forEach(f => f());
    expect([(await first).status, (await last).status].sort()).toEqual([201,503]);
    expect((await request('catalog')).value.rooms).toHaveLength(32);
  });
  it('bounds pending password work while allowing a twelve-player admission burst', async () => {
    hashGate.blocked = true;
    const pending = Array.from({ length: 16 }, (_, i) => request('create', { title: `В очереди ${i}`, password: 'pw' }));
    await vi.waitFor(() => expect(hashGate.jobs).toHaveLength(16));
    expect((await request('create', { title: 'Перегрузка', password: 'pw' })).status).toBe(503);
    hashGate.jobs.splice(0).forEach(f => f());
    expect((await Promise.all(pending)).map(r => r.status)).toEqual(Array(16).fill(201));
  });

});
