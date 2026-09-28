import type { ResultEvent, ResultSink } from './events';
export interface ResultQueue {
  put(event: ResultEvent): Promise<void>;
  list(): Promise<ResultEvent[]>;
  remove(id: string): Promise<void>;
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
}
export class ResultUploader implements ResultSink {
  private pending = new Map<string, ResultEvent>();
  private writing: Promise<void> = Promise.resolve();
  private running = false;
  private timer?: ReturnType<typeof setTimeout>;
  private failures = 0;
  private stopped = false;
  private wakeRequested = false;
  constructor(private queue: ResultQueue, private send: (event: ResultEvent) => Promise<string>) {}
  enqueue(e: ResultEvent): void {
    this.pending.set(e.eventId, e);
    this.wakeRequested = true;
    this.writing = this.writing.then(async () => {
      try { await this.queue.put(e); this.pending.delete(e.eventId); } catch { /* retry from memory */ }
    });
    this.schedule(0);
  }
  wake = () => { this.stopped = false; this.failures = 0; this.wakeRequested = true; this.schedule(0); };
  stop() { this.stopped = true; if (this.timer) clearTimeout(this.timer); }
  private schedule(ms: number) {
    if (this.stopped) return;
    if (this.timer) clearTimeout(this.timer);
    this.timer = setTimeout(() => { this.timer = undefined; void this.flush(); }, ms);
  }
  async flush(): Promise<void> {
    if (this.running) return;
    this.running = true;
    this.wakeRequested = false;
    try {
      await this.writing;
      for (const e of this.pending.values()) { await this.queue.put(e); this.pending.delete(e.eventId); }
      let deliveryFailed = false;
      for (const e of await this.queue.list()) {
        try {
          if (await this.send(e) !== e.eventId) throw new Error('Statistics acknowledgement mismatch');
          await this.queue.remove(e.eventId);
        } catch { deliveryFailed = true; }
      }
      this.failures = deliveryFailed ? this.failures + 1 : 0;
    } catch {
      this.failures++;
    } finally {
      this.running = false;
      this.schedule(this.wakeRequested ? 0 : this.failures ? Math.min(300_000, 5000 * 2 ** Math.min(this.failures - 1, 6)) + Math.random() * 1000 : 30_000);
    }
  }
}
let singleton: ResultUploader | undefined;
export function browserResults(): ResultUploader {
  if (!singleton) {
    singleton = new ResultUploader(new IndexedResultQueue(), async event => {
      const response = await fetch('/api/match-results', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(event), signal: AbortSignal.timeout(5000) });
      if (!response.ok) throw new Error('Statistics delivery unavailable');
      const ack = await response.json();
      if (!['created', 'duplicate'].includes(ack.status)) throw new Error('Statistics not committed');
      return ack.eventId;
    });
    window.addEventListener('online', singleton.wake);
    window.addEventListener('pageshow', singleton.wake);
    singleton.wake();
  }
  return singleton;
}
