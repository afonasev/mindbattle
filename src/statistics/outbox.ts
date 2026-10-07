import { statisticsEnabled, statisticsGeneration } from './preference';
import type { ResultEvent, ResultSink } from './events';
type QueuedResult = ResultEvent & { _statisticsGeneration?: number };
export interface ResultQueue {
  put(event: ResultEvent): Promise<void>;
  list(): Promise<ResultEvent[]>;
  remove(id: string): Promise<void>;
  clear?(): Promise<void>;
}
export class IndexedResultQueue implements ResultQueue {
  private db?: Promise<IDBDatabase>;
  private open(): Promise<IDBDatabase> {
    if (!this.db) this.db = new Promise<IDBDatabase>((resolve, reject) => {
      const req = indexedDB.open('mindbattle-results-v1', 1);
      req.onupgradeneeded = () => req.result.createObjectStore('outbox', { keyPath: 'eventId' });
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
      req.onblocked = () => reject(new Error('Statistics database blocked'));
    }).catch(error => { this.db = undefined; throw error; });
    return this.db;
  }
  private async transaction<T>(mode: IDBTransactionMode, operation: (store: IDBObjectStore) => IDBRequest<T>): Promise<T> {
    const db = await this.open();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('outbox', mode);
      const req = operation(tx.objectStore('outbox'));
      tx.oncomplete = () => resolve(req.result);
      tx.onerror = tx.onabort = () => reject(tx.error ?? new Error('Statistics transaction failed'));
    });
  }
  async put(e: ResultEvent) { await this.transaction('readwrite', store => store.put(e)); }
  list() { return this.transaction<ResultEvent[]>('readonly', store => store.getAll()); }
  async remove(id: string) { await this.transaction('readwrite', store => store.delete(id)); }
  async clear() { await this.transaction('readwrite', store => store.clear()); }
}
export class ResultUploader implements ResultSink {
  private pending = new Map<string, ResultEvent>();
  private writing: Promise<void> = Promise.resolve();
  private flushing?: Promise<void>;
  private disabling?: Promise<void>;
  private timer?: ReturnType<typeof setTimeout>;
  private failures = 0;
  private stopped = false;
  private blocked = false;
  private generation = 0;
  private request?: AbortController;
  private wakeRequested = false;
  constructor(private queue: ResultQueue, private send: (event: ResultEvent, signal?: AbortSignal) => Promise<string>, private permitted: () => boolean = () => true, private epoch: () => number = () => 0) {}
  private allowed() { return !this.blocked && this.permitted(); }
  enqueue(e: ResultEvent): void {
    if (!this.allowed()) return;
    e = { ...e, _statisticsGeneration: this.epoch() } as QueuedResult;
    const epoch = this.epoch();
    const generation = this.generation;
    this.pending.set(e.eventId, e);
    this.wakeRequested = true;
    this.writing = this.writing.then(async () => {
      if (!this.allowed() || generation !== this.generation || epoch !== this.epoch()) return;
      try { await this.queue.put(e); this.pending.delete(e.eventId); } catch { /* retry from memory */ }
    });
    this.schedule(0);
  }
  wake = () => { if (!this.allowed()) return; this.stopped = false; this.failures = 0; this.wakeRequested = true; this.schedule(0); };
  stop() { this.stopped = true; if (this.timer) clearTimeout(this.timer); }
  disable(): Promise<void> {
    this.blocked = true; this.generation++; this.stop(); this.request?.abort();
    if (!this.disabling) this.disabling = this.purge().finally(() => { this.disabling = undefined; });
    return this.disabling;
  }
  private async purge(): Promise<void> {
    await this.writing; await this.flushing;
    this.pending.clear();
    if (this.queue.clear) await this.queue.clear();
    else for (const event of await this.queue.list()) await this.queue.remove(event.eventId);
  }
  async enable() { await this.disabling; if (!this.permitted()) return; this.blocked = false; this.wake(); }
  private schedule(ms: number) {
    if (this.stopped || !this.allowed()) return;
    if (this.timer) clearTimeout(this.timer);
    this.timer = setTimeout(() => { this.timer = undefined; void this.flush(); }, ms);
  }
  flush(): Promise<void> {
    if (this.flushing) return this.flushing;
    this.flushing = this.deliver().finally(() => { this.flushing = undefined; });
    return this.flushing;
  }
  private async deliver(): Promise<void> {
    if (!this.allowed()) return;
    const generation = this.generation;
    this.wakeRequested = false;
    try {
      await this.writing;
      if (!this.allowed() || generation !== this.generation) return;
      for (const e of this.pending.values()) { await this.queue.put(e); this.pending.delete(e.eventId); }
      let deliveryFailed = false;
      for (const e of await this.queue.list()) {
        if (!this.allowed() || generation !== this.generation) return;
        if (((e as QueuedResult)._statisticsGeneration ?? 0) !== this.epoch()) { await this.queue.remove(e.eventId); continue; }
        const { _statisticsGeneration: _generation, ...payload } = e as QueuedResult;
        this.request = new AbortController();
        try {
          if (await this.send(payload, this.request.signal) !== e.eventId) throw new Error('Statistics acknowledgement mismatch');
          if (!this.allowed() || generation !== this.generation) return;
          await this.queue.remove(e.eventId);
        } catch { deliveryFailed = true; }
      }
      this.failures = deliveryFailed ? this.failures + 1 : 0;
    } catch { this.failures++; }
    finally {
      this.request = undefined;
      this.schedule(this.wakeRequested ? 0 : this.failures ? Math.min(300_000, 5000 * 2 ** Math.min(this.failures - 1, 6)) + Math.random() * 1000 : 30_000);
    }
  }
}
let singleton: ResultUploader | undefined;
export function browserResults(): ResultUploader {
  if (!singleton) {
    singleton = new ResultUploader(new IndexedResultQueue(), async (event, signal) => {
      const response = await fetch('/api/match-results', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(event), signal: signal ? AbortSignal.any([signal, AbortSignal.timeout(5000)]) : AbortSignal.timeout(5000) });
      if (!response.ok) throw new Error('Statistics delivery unavailable');
      const ack = await response.json();
      if (!['created', 'duplicate'].includes(ack.status)) throw new Error('Statistics not committed');
      return ack.eventId;
    }, statisticsEnabled, statisticsGeneration);
    window.addEventListener('online', singleton.wake);
    window.addEventListener('pageshow', singleton.wake);
    singleton.wake();
  }
  return singleton;
}
