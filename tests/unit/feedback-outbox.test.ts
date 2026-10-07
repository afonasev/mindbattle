import { legacySnapshotFeedback } from '../../src/feedback/legacy';
import { emptyPersistedData, savePersistedData, STORAGE_KEY } from '../../src/adapters/storage';
import { describe, expect, it } from 'vitest';
import { FeedbackUploader, type FeedbackQueue } from '../../src/feedback/outbox';
import type { DifficultyFeedbackEvent, DifficultyFeedbackSink } from '../../src/feedback/types';
const event: DifficultyFeedbackEvent = { schemaVersion: 3, eventId: 'complaint-1', matchId: 'match', catalogRevision: 'old', questionId: 'q', assignedDifficulty: 'easy', hasComplaint: true, complaintReasons: ['suspected-error'] };
class Queue implements FeedbackQueue {
  events = new Map<string, DifficultyFeedbackEvent>(); fail = false;
  async put(e: DifficultyFeedbackEvent) { if (this.fail) throw Error('quota'); this.events.set(e.eventId, e); }
  async list() { return [...this.events.values()]; }
  async remove(id: string) { this.events.delete(id); }
}
describe('durable complaint delivery', () => {
  it('commits locally before any HTTP and retains failures across uploader restarts', async () => {
    const q = new Queue(); let calls = 0;
    const sink: DifficultyFeedbackSink = { submit: async () => { calls++; throw Error('offline'); } };
    const uploader = new FeedbackUploader(q, sink);
    try {
      await uploader.submit(event); expect(calls).toBe(0); expect(q.events.get(event.eventId)).toEqual(event);
      await uploader.flush(); expect(q.events.get(event.eventId)).toEqual(event);
    } finally { uploader.stop(); }
    const sent: DifficultyFeedbackEvent[] = [];
    const restarted = new FeedbackUploader(q, { submit: async e => { sent.push(e); } });
    try { await restarted.flush(); expect(sent).toEqual([event]); expect(q.events.size).toBe(0); }
    finally { restarted.stop(); }
  });
  it('never calls HTTP while offline and delivers after internet returns', async () => {
    const q=new Queue();let online=false;let calls=0;
    const uploader=new FeedbackUploader(q,{submit:async () => {calls++;}},() => online);
    try {await uploader.submit(event);await uploader.flush();expect(calls).toBe(0);expect(q.events.size).toBe(1);online=true;await uploader.flush();expect(calls).toBe(1);expect(q.events.size).toBe(0);}
    finally {uploader.stop();}
  });
  it('propagates local commit failure and never sends an unsaved complaint', async () => {
    const q = new Queue(); q.fail = true; let calls = 0;
    const uploader = new FeedbackUploader(q, { submit: async () => { calls++; } });
    try { await expect(uploader.submit(event)).rejects.toThrow('quota'); expect(calls).toBe(0); }
    finally { uploader.stop(); }
  });
  it('does not lose append during flush and coalesces concurrent flushes', async () => {
    const q = new Queue(); await q.put(event);
    let complete!: () => void; let entered!: () => void;
    const started = new Promise<void>(resolve => { entered = resolve; });
    const uploader = new FeedbackUploader(q, { submit: async () => { entered(); await new Promise<void>(resolve => { complete = resolve; }); } });
    try {
      const flushing = uploader.flush(); await started;
      expect(uploader.flush()).toBe(flushing);
      await uploader.submit({ ...event, eventId: 'complaint-2' }); complete(); await flushing;
      expect([...q.events.keys()]).toEqual(['complaint-2']);
    } finally { uploader.stop(); }
  });
  it('copies a confirmed legacy complaint before catalog mismatch discards the match snapshot', () => {
    const values = new Map<string,string>();
    const storage = { getItem: (key: string) => values.get(key) ?? null, setItem: (key: string,value: string) => { values.set(key,value); }, removeItem: (key: string) => { values.delete(key); } };
    storage.setItem('mindbattle:data:v1', JSON.stringify({ lastMatch: { state: { matchId: event.matchId, catalogRevision: event.catalogRevision, phase: { kind: 'difficulty-feedback', stage: 'done', eventId: event.eventId, hasComplaint: true, complaintReasons: ['suspected-error'], complaintNote: '', round: { questionId:'q', difficulty:'easy' } } } } }));
    storage.setItem('mindbattle:feedback-queue:v1', '{broken');
    expect(legacySnapshotFeedback(storage.getItem(STORAGE_KEY))).toEqual([event]);
    expect(savePersistedData(storage, emptyPersistedData('new-catalog'))).toBe(true);
    expect(legacySnapshotFeedback(storage.getItem(STORAGE_KEY))).toEqual([event]);
    const failedStorage = { ...storage, setItem: () => { throw Error('quota'); } };
    expect(savePersistedData(failedStorage, emptyPersistedData('newer-catalog'))).toBe(false);
    expect(legacySnapshotFeedback(storage.getItem(STORAGE_KEY))).toEqual([event]);
  });
  it('preserves the exact old note after a lost acknowledgement', () => {
    const source = JSON.stringify({lastMatch:{state:{matchId:'match',catalogRevision:'old',phase:{kind:'difficulty-feedback',stage:'done',eventId:'complaint-1',hasComplaint:true,complaintReasons:['suspected-error'],complaintNote:' text ',round:{questionId:'q',difficulty:'easy'}}}}});
    expect(legacySnapshotFeedback(source)).toEqual([{...event,complaintNote:' text '}]);
  });

});
