import { emptyPersistedData, savePersistedData } from '../../src/adapters/storage';
import { describe, expect, it } from 'vitest';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { readStatisticsPreference, disableStoredStatistics, STATISTICS_KEY } from '../../src/statistics/preference';
import { ResultObserver, type ResultEvent } from '../../src/statistics/events';
import { ResultUploader, type ResultQueue } from '../../src/statistics/outbox';
import { createSoloRun } from '../../src/domain/solo';
import { createServerResultQueue } from '../../server/resultStore.mjs';
import { makeContext } from './network-fixture';
import { NetworkRoom } from '../../src/network/room';
const event: ResultEvent = { schemaVersion: 1, eventId:'old', matchId:'match', mode:'solo-endless-v1', catalogRevision:'fixture-r1', kind:'match', ordinal:0, status:'in-progress',reason:'checkpoint',score:0,lives:3 };
class Queue implements ResultQueue {
  events = new Map<string,ResultEvent>();
  async put(e: ResultEvent) { this.events.set(e.eventId,e); }
  async list() { return [...this.events.values()]; }
  async remove(id: string) { this.events.delete(id); }
  async clear() { this.events.clear(); }
}
function storage() {
  const values=new Map<string,string>();
  return {values,getItem:(key:string)=>values.get(key)??null,setItem:(key:string,value:string)=>{values.set(key,value);},removeItem:(key:string)=>{values.delete(key);}};
}
describe('statistics permission', () => {
  it('defaults independently of legacy feedback and disables snapshots without touching records', () => {
    const s=storage();s.setItem('mindbattle:data:v1',JSON.stringify({lastSolo:{state:{config:{collectQuestionFeedback:false}}},lastMatch:{state:{config:{}}},soloRecords:[{name:'record',score:100}]}));
    expect(readStatisticsPreference(s).enabled).toBe(true);
    s.setItem(STATISTICS_KEY,JSON.stringify({version:1,enabled:false,revokedRooms:['room']}));
    disableStoredStatistics(s);
    const data=JSON.parse(s.getItem('mindbattle:data:v1')!);
    expect(data.lastSolo.state.config).toEqual({collectQuestionFeedback:false,collectStatistics:false});
    expect(data.lastMatch.state.config.collectStatistics).toBe(false);
    expect(data.soloRecords).toEqual([{name:'record',score:100}]);
    expect(readStatisticsPreference(s)).toEqual({version:1,enabled:false,revokedRooms:['room']});
  });
  it('older controller snapshots cannot overwrite a revoked permission for the same run', () => {
    const s=storage();const data={...emptyPersistedData('fixture-r1'),lastSolo:{status:'in-progress' as const,savedAt:'now',state:{runId:'same',config:{collectStatistics:true}}}};
    expect(savePersistedData(s,data)).toBe(true);disableStoredStatistics(s);expect(savePersistedData(s,data)).toBe(true);
    expect(JSON.parse(s.getItem('mindbattle:data:v1')!).lastSolo.state.config.collectStatistics).toBe(false);
    const fresh={...data,lastSolo:{...data.lastSolo,state:{runId:'new',config:{collectStatistics:true}}}};savePersistedData(s,fresh);
    expect(JSON.parse(s.getItem('mindbattle:data:v1')!).lastSolo.state.config.collectStatistics).toBe(true);
  });
  it('never constructs an observation without permission and does not revive an opted-out run', () => {
    const ctx=makeContext(),events:ResultEvent[]=[];
    let allowed=false;
    const observer=new ResultObserver({enqueue:e=>events.push(e)},ctx,()=>allowed);
    const run=createSoloRun({profile:'solo-endless-v1'},'permission',0,ctx);
    observer.solo(run,undefined,true);expect(events).toEqual([]);
    allowed=true;observer.solo({...run,config:{...run.config,collectStatistics:false}},undefined,true);expect(events).toEqual([]);
    observer.solo({...run,runId:'new-run'},undefined,true);expect(events).toHaveLength(1);
  });
  it('purges a queued IDB write before enable and online wake cannot restart disabled delivery', async () => {
    const q=new Queue();let release!:()=>void;
    const normal=q.put.bind(q);q.put=async e=>{await new Promise<void>(resolve=>{release=resolve;});await normal(e);};
    let calls=0;const uploader=new ResultUploader(q,async e=>{calls++;return e.eventId;});
    try {
      uploader.enqueue(event);await Promise.resolve();
      const off=uploader.disable();uploader.wake();release();await off;
      await uploader.flush();expect(calls).toBe(0);expect(await q.list()).toEqual([]);
      q.put=normal;await uploader.enable();uploader.enqueue({...event,eventId:'new'});await uploader.flush();expect(calls).toBe(1);
    } finally {uploader.stop();}
  });
  it('cancel prevents the remainder of an active batch from sending after disable', async () => {
    const q=new Queue();await q.put(event);await q.put({...event,eventId:'later'});
    let entered!:()=>void;const start=new Promise<void>(resolve=>{entered=resolve;});let calls=0;
    const uploader=new ResultUploader(q,async (_e,signal)=>{calls++;entered();await new Promise<void>((_resolve,reject)=>signal!.addEventListener('abort',()=>reject(Error('cancel')),{once:true}));return 'old';});
    try {const flushing=uploader.flush();await start;await uploader.disable();await flushing;expect(calls).toBe(1);expect(await q.list()).toEqual([]);}
    finally {uploader.stop();}
  });
  it('server revoke waits for preceding append and survives restart, excluding recovered checkpoints', async () => {
    const dir=await mkdtemp(join(tmpdir(),'mindbattle-permission-'));let release!:()=>void;let entered!:()=>void;
    const started=new Promise<void>(resolve=>{entered=resolve;});const delivered:string[]=[];
    const q=createServerResultQueue(dir,async e=>{entered();await new Promise<void>(resolve=>{release=resolve;});delivered.push(e.eventId);return {status:'created',eventId:e.eventId};});
    try {
      q.enqueue(event);await started;q.enqueue({...event,eventId:"not-yet-sent"});
      let revoked=false;const off=q.disableMatch(event.matchId).then(()=>{revoked=true;});await Promise.resolve();expect(revoked).toBe(false);
      release();await off;
      q.enqueue({...event,eventId:'after-revoke'});await q.flush();expect(delivered).toEqual(['old']);q.stop();
      const restarted=createServerResultQueue(dir,async e=>{delivered.push(e.eventId);return {status:'created',eventId:e.eventId};});
      try {restarted.enqueue({...event,eventId:'restart-checkpoint'});restarted.enqueue({...event,eventId:'new-match',matchId:'new-match'});await restarted.flush();expect(delivered).toEqual(['old','new-match']);}
      finally {restarted.stop();}
    } finally {q.stop();await rm(dir,{recursive:true,force:true});}
  });
  it('only the creator can disable a room; reenable permits new matches without reviving the current match', async () => {
    const events:ResultEvent[]=[];const denied:string[]=[];let serial=0;
    const room=new NetworkRoom('room','creator',makeContext(),{},()=>`key-${++serial}`,async()=>{},()=>{},{enqueue:e=>events.push(e),disableMatch:async id=>{denied.push(id);}});
    room.connect('creator',0);const players=[room.join('one',0),room.join('two',0)];for(const p of players)room.connect(p.token,0);
    let command=0;const start=()=>room.command('creator',{commandId:`cmd-${++command}`,epoch:room.epoch,phaseRevision:room.phaseRevision,action:{type:'start'}},0);
    start();expect(events.length).toBeGreaterThan(0);const id=room.state!.matchId;
    await expect(room.setStatistics(players[0].token,false)).rejects.toThrow('устройству-создателю');
    await room.setStatistics('creator',false);expect(denied).toEqual([id]);const before=events.length;
    await room.setStatistics('creator',true);room.interruptResults('test');expect(events.length).toBe(before);expect(room.state!.config.collectStatistics).toBe(false);
    room.command(players[0].token,{commandId:`cmd-${++command}`,epoch:room.epoch,phaseRevision:room.phaseRevision,action:{type:'replay'}},0);start();expect(room.state!.config.collectStatistics).toBe(true);expect(events.length).toBeGreaterThan(before);
  });
  it('a stale enabled tab cannot observe an old-generation match or deliver its backlog', async () => {
    const ctx=makeContext(), events:ResultEvent[]=[];let generation=0;
    const run=createSoloRun({profile:'solo-endless-v1',statisticsGeneration:0},'generation',0,ctx);
    const observer=new ResultObserver({enqueue:e=>events.push(e)},ctx,g=>(g??0)===generation);
    generation=1;observer.solo(run,undefined,true);expect(events).toEqual([]);
    observer.solo(createSoloRun({profile:'solo-endless-v1',statisticsGeneration:1},'new',0,ctx),undefined,true);expect(events).toHaveLength(1);
    const q=new Queue();await q.put(event);const sent:ResultEvent[]=[];
    const uploader=new ResultUploader(q,async e=>{sent.push(e);return e.eventId;},()=>true,()=>generation);
    try {await uploader.flush();expect(sent).toEqual([]);uploader.enqueue({...event,eventId:'new'});await uploader.flush();expect(sent).toHaveLength(1);expect(sent[0]).not.toHaveProperty('_statisticsGeneration');}finally{uploader.stop();}
  });
  it('revokes backlog after replay and rejects a delayed older enable', async () => {
    const denied:string[]=[];let serial=0;
    const room=new NetworkRoom('room','creator',makeContext(),{},()=>`s-${++serial}`,async()=>{},()=>{},{enqueue:()=>{},disableMatch:async id=>{denied.push(id);}});
    room.connect('creator',0);const players=[room.join('one',0),room.join('two',0)];for(const p of players)room.connect(p.token,0);
    room.command('creator',{commandId:'start',epoch:room.epoch,phaseRevision:room.phaseRevision,action:{type:'start'}},0);const id=room.state!.matchId;
    room.command(players[0].token,{commandId:'replay',epoch:room.epoch,phaseRevision:room.phaseRevision,action:{type:'replay'}},0);
    await room.setStatistics('creator',false,20,1);expect(denied).toEqual([id]);
    await room.setStatistics('creator',true,10,0);expect(room.statisticsEnabled).toBe(false);
    await room.setStatistics('creator',true,21,1);expect(room.statisticsEnabled).toBe(true);
  });

  it('retries a failed durable revoke before acknowledging a newer enabled generation', async () => {
    let attempts=0,serial=0;
    const room=new NetworkRoom('room','creator',makeContext(),{},()=>`s-${++serial}`,async()=>{},()=>{},{enqueue:()=>{},disableMatch:async()=>{if(++attempts===1)throw Error('disk');}});
    room.connect('creator',0);for(const name of ['one','two']){const p=room.join(name,0);room.connect(p.token,0);}
    room.command('creator',{commandId:'start',epoch:room.epoch,phaseRevision:room.phaseRevision,action:{type:'start'}},0);
    await expect(room.setStatistics('creator',true,20,1)).rejects.toThrow('disk');expect(room.statisticsEnabled).toBe(false);
    await room.setStatistics('creator',true,20,1);expect(attempts).toBe(2);expect(room.statisticsEnabled).toBe(true);expect(room.state!.config.collectStatistics).toBe(false);
  });

});
