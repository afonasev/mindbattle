import { describe, expect, it } from "vitest";
import { analyzeProductionFeedback } from "../../server/feedbackReport.mjs";

const revision = "catalog-r2";
const questions = new Map([["q-easy", "easy"], ["q-hard", "hard"]]);
const base = {
  schemaVersion: 3,
  matchId: "match-1",
  catalogRevision: revision,
  questionId: "q-easy",
  assignedDifficulty: "easy",
  hasComplaint: false,
  complaintReasons: []
};

describe("production feedback report", () => {
  it("aggregates two independent events without revealing complaint notes", () => {
    const source = [
      JSON.stringify({ ...base, eventId: "device-a" }),
      JSON.stringify({ ...base, eventId: "device-b", hasComplaint: true, complaintReasons: ["too-hard"], complaintNote: "Не печатать" }),
      JSON.stringify({ ...base, eventId: "device-b", hasComplaint: true, complaintReasons: ["too-hard"], complaintNote: "Не печатать" }),
      JSON.stringify({ ...base, eventId: "old", catalogRevision: "catalog-r1" }),
      "not-json"
    ].join("\n");
    const report = analyzeProductionFeedback(source, { questions, catalogRevision: revision });
    expect(report.totals).toMatchObject({ total: 2, complaints: 1, noComplaints: 1, complaintRate: 0.5, reasons: { "too-hard": 1 } });
    expect(report.byQuestion["q-easy"]).toMatchObject({ total: 2, complaints: 1 });
    expect(report.diagnostics).toMatchObject({ historicalEvents: 1, invalidLines: 1, duplicateEventIds: ["device-b"], catalogRevisions: { "catalog-r1": 1, "catalog-r2": 3 } });
    expect(JSON.stringify(report)).not.toContain("Не печатать");
  });

  it("reports unknown current question without including it in editor signals", () => {
    const report = analyzeProductionFeedback(JSON.stringify({ ...base, eventId: "unknown", questionId: "missing" }), { questions, catalogRevision: revision });
    expect(report.totals.total).toBe(0);
    expect(report.diagnostics.unknownQuestionIds).toEqual(["missing"]);
  });
});
