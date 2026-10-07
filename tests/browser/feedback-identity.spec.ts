import { expect, test } from "@playwright/test";
import { readFileSync } from "node:fs";
import { randomUUID } from "node:crypto";
import identity from "../../src/content/revision.json" with { type: "json" };

const question = JSON.parse(readFileSync("src/content/topics/animals.json", "utf8")).questions[0];

test("real feedback endpoint accepts the current catalog and rejects another revision", async ({ request }) => {
  const event = {
    schemaVersion: 3, eventId: randomUUID(), matchId: randomUUID(),
    catalogRevision: identity.revision, questionId: question.id,
    assignedDifficulty: question.difficulty, hasComplaint: false, complaintReasons: [],
  };
  const accepted = await request.post("/api/difficulty-feedback", { data: event });
  expect(accepted.status()).toBe(201);
  expect(await accepted.json()).toEqual({ status: "created" });
  const replay = await request.post("/api/difficulty-feedback", { data: event });
  expect(replay.status()).toBe(200);
  expect(await replay.json()).toEqual({ status: "duplicate" });
  const rejected = await request.post("/api/difficulty-feedback", {
    data: { ...event, eventId: randomUUID(), catalogRevision: "unrelated-catalog" },
  });
  expect(rejected.status()).toBe(400);
  expect(await rejected.json()).toMatchObject({ status: "invalid" });
});
