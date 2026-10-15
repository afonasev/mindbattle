import test from 'node:test';
import assert from 'node:assert/strict';
import { createUpdateCoordinator } from '../../desktop/updateCheck.mjs';
import { createDisplayController } from '../../desktop/display.mjs';
import { localizedNotes } from '../../desktop/releases.mjs';
import { isMutedLaunch } from '../../desktop/launch.mjs';

const fixture = () => {
  let discoveries = 0, downloads = 0;
  const shell = { root: '/tmp', state: {}, check: async () => false };
  const content = { root: '/tmp', state: {}, check: async (_emit, {signal}) => { downloads++; signal.throwIfAborted(); content.state.pending = 'yes'; return true; }, directory: () => '', manifestAt: async () => ({ version: '1.0.1' }) };
  const catalog = { candidate: async () => { discoveries++; return {kind:'content',raw:Buffer.from('signed'),manifest:{version:'1.0.1',files:[{size:1}]}}; } };
  const coordinator = createUpdateCoordinator({ shellStore:shell,contentStore:content,catalog });
  return { coordinator, content, catalog, counts:()=>({discoveries,downloads}) };
};
test('one discovery per session, no bytes before consent; ready from selected download', async () => {
  const f = fixture();
  const a = f.coordinator.start(), b = f.coordinator.start(); assert.equal(a,b);
  await a; assert.deepEqual(f.counts(), {discoveries:1,downloads:0}); assert.equal(f.coordinator.status().phase,'available');
  await f.coordinator.setSafe(true); await f.coordinator.download();
  await new Promise(resolve=>setTimeout(resolve,40));
  assert.equal(f.coordinator.status().phase,'ready'); assert.deepEqual(f.counts(),{discoveries:1,downloads:1});
  await f.coordinator.start(); assert.equal(f.counts().discoveries,1);
});
test('failed discovery never retries after reconnect/menu calls', async () => {
  const f=fixture(); let calls=0; f.catalog.candidate=async()=>{calls++;throw Error('offline');};
  await f.coordinator.start(); await f.coordinator.start(); await f.coordinator.setSafe(true); await f.coordinator.download();
  assert.equal(calls,1); assert.equal(f.coordinator.status().phase,'error');
});
test('pause waits for selected download to stop, resumes without discovery, cancellation removes consent', async () => {
  const f=fixture(); let started;
  const active = new Promise(resolve=>{started=resolve;});
  f.content.check = async (_emit,{signal,raw})=>{assert.equal(raw.toString(),'signed');started();await new Promise((_resolve,reject)=>signal.addEventListener('abort',()=>reject(signal.reason),{once:true}));};
  await f.coordinator.setSafe(true); await f.coordinator.download(); await active;
  await f.coordinator.setSafe(false); assert.equal(f.coordinator.status().phase,'paused');
  await f.coordinator.cancel(); await f.coordinator.setSafe(true); assert.equal(f.coordinator.status().phase,'available');
  assert.equal(f.counts().discoveries,1);
});
test('display timeout and cancellation never persist an unsafe preview', async () => {
  let callback; const applied=[],saved=[];
  const initial={width:1280,height:720,fullscreen:false};
  const control=createDisplayController({initial,apply:async v=>applied.push(v),persist:async v=>saved.push(v),timers:{setTimeout:cb=>{callback=cb;return 1;},clearTimeout:()=>{}}});
  await control.preview({...initial,fullscreen:true});callback();await new Promise(resolve=>setImmediate(resolve));
  assert.deepEqual(control.value(),initial);assert.equal(saved.length,0);assert.deepEqual(applied.at(-1),initial);
  await control.preview({...initial,width:1024});await control.confirm();assert.equal(saved.length,1);assert.equal(control.value().width,1024);
});
test('failed display write restores last confirmed mode',async()=>{
  const applied=[];const initial={width:1280,height:720,fullscreen:false};
  const control=createDisplayController({initial,apply:async v=>applied.push(v),persist:async()=>{throw Error('disk full');}});
  await control.preview({...initial,fullscreen:true});await assert.rejects(control.confirm(),/disk full/);assert.deepEqual(applied.at(-1),initial);assert.deepEqual(control.value(),initial);
});
test('notes select only the menu language and absent translations are honest',()=>{
  const body='## Русский\n### Новое\n- Справка.\n\n## English\n### Added\n- Help.';
  assert.match(localizedNotes(body),/Справка/);assert.doesNotMatch(localizedNotes(body),/Help/);
  assert.match(localizedNotes(body,'en'),/Help/);assert.match(localizedNotes('legacy'),/отсутствует/);
});
test('single-dash contract and old double-dash alias both work',()=>{
  assert.equal(isMutedLaunch(['-muted']),true);assert.equal(isMutedLaunch(['--muted']),true);assert.equal(isMutedLaunch(['muted']),false);
});
