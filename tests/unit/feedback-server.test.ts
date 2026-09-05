import { mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { createFeedbackStore, validateFeedbackEvent } from "../../server/feedbackStore.mjs";

const questions = new Map([
  ["q-easy", "easy"],
  ["q-hard", "hard"]
]);
const revision = "catalog-r2";
const event = {
  schemaVersion: 1,
  eventId: "event-1",
  matchId: "match-1",
  catalogRevision: revision,
  questionId: "q-easy",
  assignedDifficulty: "easy",
  perceivedDifficulty: "hard"
};

describe("difficulty feedback server store", () => {
  it("stores a v3 positive signal and a complaint without team data", async () => {
    const directory = await mkdtemp(join(tmpdir(), "mindbattle-feedback-"));
    const store = await createFeedbackStore({ filePath: join(directory, "feedback.ndjson"), questions, catalogRevision: revision });
    const positive = { schemaVersion: 3, eventId: "v3-no", matchId: "match-v3", catalogRevision: revision, questionId: "q-easy", assignedDifficulty: "easy", hasComplaint: false, complaintReasons: [] };
    const complaint = { ...positive, eventId: "v3-yes", hasComplaint: true, complaintReasons: ["too-hard", "unclear-wording"], complaintNote: "Нужна редакторская проверка" };
    const noteOnly = { ...positive, eventId: "v3-note", hasComplaint: true, complaintReasons: [], complaintNote: "Проверить формулировку" };
    expect(await store.append(positive)).toEqual({ status: "created" });
    expect(await store.append(complaint)).toEqual({ status: "created" });
    expect(await store.append(noteOnly)).toEqual({ status: "created" });
    expect(store.summary().v3.byQuestion["q-easy"]).toMatchObject({ total: 3, complaints: 2, noComplaints: 1, reasons: { "too-hard": 1 } });
    expect(await store.append({ ...complaint, eventId: "v3-invalid", complaintReasons: ["too-hard", "too-easy"] })).toMatchObject({ status: "invalid" });
    expect(await store.append({ ...noteOnly, eventId: "v3-whitespace", complaintNote: "   " })).toMatchObject({ status: "invalid" });
  });
  it("validates catalog identity and levels", () => {
    expect(validateFeedbackEvent(event, questions, revision)).toBeNull();
    expect(validateFeedbackEvent({ ...event, eventId: "" }, questions, revision)).toMatch(/схема/);
    expect(validateFeedbackEvent({ ...event, questionId: "missing" }, questions, revision)).toMatch(/questionId/);
    expect(validateFeedbackEvent({ ...event, assignedDifficulty: "hard" }, questions, revision)).toMatch(/каталогу/);
  });

  it("appends once, deduplicates and reports higher perceived difficulty", async () => {
    const directory = await mkdtemp(join(tmpdir(), "mindbattle-feedback-"));
    const filePath = join(directory, "feedback.ndjson");
    const store = await createFeedbackStore({ filePath, questions, catalogRevision: revision });
    expect(await store.append(event)).toEqual({ status: "created" });
    expect(await store.append(event)).toEqual({ status: "duplicate" });
    expect((await store.append({ ...event, perceivedDifficulty: "easy" })).status).toBe("conflict");
    const lines = (await readFile(filePath, "utf8")).trim().split("\n");
    expect(lines).toHaveLength(1);
    expect(store.summary().byQuestion["q-easy"]).toMatchObject({ total: 1, higher: 1, exact: 0 });
  });

  it("aggregates exact, lower and higher without storing gameplay data", async () => {
    const directory = await mkdtemp(join(tmpdir(), "mindbattle-feedback-"));
    const filePath = join(directory, "feedback.ndjson");
    const store = await createFeedbackStore({ filePath, questions, catalogRevision: revision });
    await store.append({ ...event, eventId: "higher" });
    await store.append({ ...event, eventId: "exact", perceivedDifficulty: "easy" });
    await store.append({
      ...event,
      eventId: "lower",
      questionId: "q-hard",
      assignedDifficulty: "hard",
      perceivedDifficulty: "easy"
    });
    expect(store.summary()).toMatchObject({
      total: 3,
      byAssignedDifficulty: {
        easy: { total: 2, exact: 1, lower: 0, higher: 1 },
        hard: { total: 1, exact: 0, lower: 1, higher: 0 }
      }
    });
    const stored = await readFile(filePath, "utf8");
    expect(stored).not.toMatch(/teamId|answer|device|score/);
  });

  it("serializes concurrent writes and diagnoses a corrupt line after restart", async () => {
    const directory = await mkdtemp(join(tmpdir(), "mindbattle-feedback-"));
    const filePath = join(directory, "feedback.ndjson");
    await writeFile(filePath, "not-json\n", "utf8");
    const store = await createFeedbackStore({ filePath, questions, catalogRevision: revision });
    await Promise.all(Array.from({ length: 5 }, (_, index) => store.append({ ...event, eventId: `event-${index + 2}` })));
    expect(store.summary()).toMatchObject({ total: 5, corruptedLines: 1 });
    const restarted = await createFeedbackStore({ filePath, questions, catalogRevision: revision });
    expect(restarted.summary()).toMatchObject({ total: 5, corruptedLines: 1 });
  });

  it("preserves events from an older catalog revision without treating them as corrupt", async () => {
    const directory = await mkdtemp(join(tmpdir(), "mindbattle-feedback-"));
    const filePath = join(directory, "feedback.ndjson");
    await writeFile(filePath, `${JSON.stringify({
      ...event,
      catalogRevision: "catalog-r1",
      recordedAt: "2026-09-01T00:00:00.000Z"
    })}\n`, "utf8");
    const store = await createFeedbackStore({ filePath, questions, catalogRevision: revision });
    expect(store.summary()).toMatchObject({ total: 0, historicalLines: 1, corruptedLines: 0 });
    expect(await store.append(event)).toEqual({ status: "created" });
    expect((await readFile(filePath, "utf8")).trim().split("\n")).toHaveLength(2);
  });

  it("fails fast when the configured path cannot be created", async () => {
    const directory = await mkdtemp(join(tmpdir(), "mindbattle-feedback-"));
    const blocker = join(directory, "not-a-directory");
    await writeFile(blocker, "blocked", "utf8");
    await expect(
      createFeedbackStore({
        filePath: join(blocker, "feedback.ndjson"),
        questions,
        catalogRevision: revision
      })
    ).rejects.toBeDefined();
  });
});
