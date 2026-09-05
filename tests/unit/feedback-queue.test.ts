import { describe, expect, it } from "vitest";
import { QueuedDifficultyFeedbackSink, type DifficultyFeedbackEvent, type DifficultyFeedbackSink } from "../../src/feedback";
import type { StorageLike } from "../../src/adapters/storage";

class Store implements StorageLike { values = new Map<string, string>(); getItem(key: string) { return this.values.get(key) ?? null; } setItem(key: string, value: string) { this.values.set(key, value); } removeItem(key: string) { this.values.delete(key); } }
class Sink implements DifficultyFeedbackSink { fail = true; events: DifficultyFeedbackEvent[] = []; async submit(event: DifficultyFeedbackEvent) { this.events.push(event); if (this.fail) throw new Error("offline"); } }
const event: DifficultyFeedbackEvent = { schemaVersion: 3, eventId: "event-1", matchId: "run-1", catalogRevision: "catalog", questionId: "question", assignedDifficulty: "easy", hasComplaint: false, complaintReasons: [] };

describe("queued feedback", () => {
  it("queues one minimal event offline and flushes the same id later", async () => {
    const storage = new Store(); const sink = new Sink(); const queued = new QueuedDifficultyFeedbackSink(sink, storage);
    await queued.submit(event); await queued.submit(event);
    expect(JSON.parse(storage.getItem("mindbattle:feedback-queue:v1") ?? "[]")).toEqual([event]);
    sink.fail = false; await queued.flush();
    expect(storage.getItem("mindbattle:feedback-queue:v1")).toBeNull();
    expect(sink.events.at(-1)?.eventId).toBe("event-1");
  });

  it("drops corrupted queue safely", async () => {
    const storage = new Store(); storage.setItem("mindbattle:feedback-queue:v1", "broken"); const sink = new Sink(); sink.fail = false;
    await new QueuedDifficultyFeedbackSink(sink, storage).flush();
    expect(storage.getItem("mindbattle:feedback-queue:v1")).toBeNull();
  });
});
