import type { DifficultyFeedbackEvent, DifficultyFeedbackSink } from "./types";
import type { StorageLike } from "../adapters/storage";
import { sendFeedbackWithinDeadline } from "./deadline";

const QUEUE_KEY = "mindbattle:feedback-queue:v1";
function queue(storage: StorageLike): DifficultyFeedbackEvent[] { try { const value: unknown = JSON.parse(storage.getItem(QUEUE_KEY) ?? "[]"); return Array.isArray(value) ? value.filter((item): item is DifficultyFeedbackEvent => typeof item === "object" && item !== null && typeof (item as { eventId?: unknown }).eventId === "string") : []; } catch { return []; } }
function saveQueue(storage: StorageLike, events: readonly DifficultyFeedbackEvent[]) { if (events.length) storage.setItem(QUEUE_KEY, JSON.stringify(events)); else storage.removeItem(QUEUE_KEY); }

export class QueuedDifficultyFeedbackSink implements DifficultyFeedbackSink {
  constructor(private readonly sink: DifficultyFeedbackSink, private readonly storage: StorageLike) {}
  private flushing?: Promise<void>;
  async submit(event: DifficultyFeedbackEvent) {
    const events = queue(this.storage);
    if (!events.some(item => item.eventId === event.eventId)) saveQueue(this.storage, [...events, event]);
  }
  flush() {
    if (this.flushing) return this.flushing;
    this.flushing = (async () => {
      for (const event of queue(this.storage)) {
        try { await this.sink.submit(event); saveQueue(this.storage, queue(this.storage).filter(item => item.eventId !== event.eventId)); }
        catch { /* Retain this event until acknowledgement. */ }
      }
    })().finally(() => { this.flushing = undefined; });
    return this.flushing;
  }
}

export class HttpDifficultyFeedbackSink implements DifficultyFeedbackSink {
  constructor(private readonly endpoint = "/api/difficulty-feedback") {}

  async submit(event: DifficultyFeedbackEvent): Promise<void> {
    await sendFeedbackWithinDeadline(async (signal) => {
      let response: Response;
      try {
        response = await fetch(this.endpoint, {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify(event),
          signal
        });
      } catch {
        throw new Error("Не удалось связаться с локальным сервером");
      }
      if (!response.ok) {
        const body = await response.json().catch(() => null) as { readonly error?: string } | null;
        throw new Error(body?.error ?? `Сервер отклонил оценку (${response.status})`);
      }
      const ack = await response.json() as { status?: string; eventId?: string };
      if (!['created', 'duplicate'].includes(ack.status ?? '') || ack.eventId !== event.eventId) throw new Error('Сервер не подтвердил сохранение жалобы');
    });
  }
}
