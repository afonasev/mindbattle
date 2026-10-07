import { legacySnapshotFeedback } from './legacy';
import type { ComplaintContext, DifficultyFeedbackEvent, DifficultyFeedbackSink } from './types';
import { HttpDifficultyFeedbackSink } from './client';

export interface FeedbackQueue {
  put(event: DifficultyFeedbackEvent): Promise<void>;
  list(): Promise<DifficultyFeedbackEvent[]>;
  remove(id: string): Promise<void>;
  has?(id: string): Promise<boolean>;
}

function canonical(value: unknown): string {
  return JSON.stringify(value, (_key, item) => item && typeof item === 'object' && !Array.isArray(item) ? Object.fromEntries(Object.entries(item).sort(([a], [b]) => a.localeCompare(b))) : item);
}
export class IndexedFeedbackQueue implements FeedbackQueue {
  private db?: Promise<IDBDatabase>;
  private open(): Promise<IDBDatabase> {
    if (!this.db) this.db = new Promise<IDBDatabase>((resolve, reject) => {
      const request = indexedDB.open('mindbattle-feedback-v1', 1);
      request.onupgradeneeded = () => { request.result.createObjectStore('outbox', { keyPath: 'eventId' }); request.result.createObjectStore('saved', { keyPath: 'eventId' }); };
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
      request.onblocked = () => reject(new Error('Локальное хранилище жалоб заблокировано'));
    }).catch(error => { this.db = undefined; throw error; });
    return this.db;
  }
  private async transaction<T>(mode: IDBTransactionMode, operation: (store: IDBObjectStore) => IDBRequest<T>): Promise<T> {
    const db = await this.open();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('outbox', mode);
      const request = operation(tx.objectStore('outbox'));
      tx.oncomplete = () => resolve(request.result);
      tx.onabort = tx.onerror = () => reject(tx.error ?? new Error('Не удалось сохранить жалобу на устройстве'));
    });
  }
  async put(event: DifficultyFeedbackEvent) {
    const db = await this.open();
    await new Promise<void>((resolve, reject) => {
      const tx = db.transaction(['outbox', 'saved'], 'readwrite');
      const saved = tx.objectStore('saved');
      const request = saved.get(event.eventId);
      let conflict = false;
      request.onsuccess = () => {
        if (request.result) {
          if (canonical(request.result) !== canonical(event)) { conflict = true; tx.abort(); }
          return;
        }
        saved.add(event); tx.objectStore('outbox').add(event);
      };
      tx.oncomplete = () => resolve();
      tx.onerror = tx.onabort = () => reject(new Error(conflict ? 'Жалоба на этот вопрос уже сохранена' : 'Не удалось сохранить жалобу на устройстве'));
    });
  }
  async has(id: string): Promise<boolean> {
    const db = await this.open();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('saved'); const req = tx.objectStore('saved').getKey(id);
      tx.oncomplete = () => resolve(req.result !== undefined);
      tx.onerror = tx.onabort = () => reject(tx.error);
    });
  }
  list() { return this.transaction<DifficultyFeedbackEvent[]>('readonly', store => store.getAll()); }
  async remove(id: string) { await this.transaction('readwrite', store => store.delete(id)); }
}

/** submit resolves on durable local commit, independently of delivery. */
export class FeedbackUploader implements DifficultyFeedbackSink {
  private running?: Promise<void>;
  private timer?: ReturnType<typeof setTimeout>;
  private failures = 0;
  private stopped = false;
  private wakeRequested = false;
  constructor(private readonly queue: FeedbackQueue, private readonly sink: DifficultyFeedbackSink, private readonly canSend: () => boolean = () => true) {}
  has(id: string) { return this.queue.has?.(id) ?? Promise.resolve(false); }
  async submit(event: DifficultyFeedbackEvent): Promise<void> {
    await this.queue.put(event);
    this.wake();
  }
  wake = () => { this.stopped = false; this.wakeRequested = true; this.schedule(0); };
  stop() { this.stopped = true; if (this.timer) clearTimeout(this.timer); }
  private schedule(delay: number) {
    if (this.stopped) return;
    if (this.timer) clearTimeout(this.timer);
    this.timer = setTimeout(() => { this.timer = undefined; void this.flush(); }, delay);
  }
  flush(): Promise<void> {
    if (this.running) return this.running;
    this.running = this.deliver().finally(() => { this.running = undefined; });
    return this.running;
  }
  private async deliver() {
    this.wakeRequested = false;
    if (!this.canSend()) { this.schedule(30_000); return; }
    let failed = false;
    try {
      for (const event of await this.queue.list()) {
        try { await this.sink.submit(event); await this.queue.remove(event.eventId); }
        catch { failed = true; }
      }
    } catch { failed = true; }
    this.failures = failed ? this.failures + 1 : 0;
    this.schedule(this.wakeRequested ? 0 : failed ? Math.min(300_000, 5_000 * 2 ** Math.min(this.failures - 1, 6)) : 30_000);
  }
}
let singleton: FeedbackUploader | undefined;
export function browserFeedback(): FeedbackUploader {
  if (!singleton) {
    const queue = new IndexedFeedbackQueue();
    singleton = new FeedbackUploader(queue, new HttpDifficultyFeedbackSink(), () => navigator.onLine);
    const uploader = singleton;
    // Await durable writes before removing the legacy queue. Failure preserves it.
    const migrate = async () => {
      // The snapshot backup survives catalog changes and controller writes until IDB recovers.
      for (const event of legacySnapshotFeedback(localStorage.getItem('mindbattle:data:v1'))) await queue.put(event);
      const raw = localStorage.getItem('mindbattle:feedback-queue:v1');
      if (raw) {
        const events: unknown = JSON.parse(raw);
        if (!Array.isArray(events)) throw new Error('Некорректная локальная очередь жалоб');
        for (const event of events) {
          if (!event || typeof event.eventId !== 'string') throw new Error('Некорректное событие жалобы');
          await queue.put(event as DifficultyFeedbackEvent);
        }
        if (localStorage.getItem('mindbattle:feedback-queue:v1') === raw) localStorage.removeItem('mindbattle:feedback-queue:v1');
      }
      uploader.wake();
    };
    const wake = () => { void migrate().catch(() => uploader.wake()); };
    window.addEventListener('online', wake);
    window.addEventListener('focus', wake);
    window.addEventListener('pageshow', wake);
    wake();
  }
  return singleton;
}
export function complaintEvent(context: ComplaintContext, reasons: readonly import('../domain/types').ComplaintReason[], note: string): import('./types').DifficultyFeedbackEventV3 {
  return { schemaVersion: 3, ...context, hasComplaint: true, complaintReasons: [...reasons], ...(note.trim() ? { complaintNote: note.trim() } : {}) };
}
