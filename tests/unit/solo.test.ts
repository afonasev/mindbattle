import { describe, expect, it } from "vitest";
import { createSoloRun, reduceSoloFrame, soloSlotAt, type SoloState } from "../../src/domain/solo";
import { shuffle } from "../../src/domain/prng";
import type { DomainContext, QuestionDefinition } from "../../src/domain/types";

function context(): DomainContext {
  const topics = Array.from({ length: 8 }, (_, index) => `topic-${index}`);
  const questions = topics.flatMap((topicId) => (["easy", "medium", "hard"] as const).map((difficulty): QuestionDefinition => ({
    id: `${topicId}-${difficulty}`,
    topicId,
    difficulty,
    prompt: topicId,
    answers: [
      { id: "a", text: "a", note: "a" }, { id: "b", text: "b", note: "b" },
      { id: "c", text: "c", note: "c" }, { id: "d", text: "d", note: "d" }
    ],
    correctAnswerId: "a",
    explanation: ["ok"],
    source: { title: "test", url: "https://example.com" }
  })));
  return {
    catalogRevision: "solo-fixture",
    selectTopics(request) {
      const [ordered, random] = shuffle(topics.filter((id) => !request.excludedTopicIds.includes(id)), request.random);
      return { topicIds: ordered.slice(0, request.count), random };
    },
    selectQuestion(request) {
      const candidates = questions.filter((question) => question.difficulty === request.difficulty && (request.topicId === null || request.topicId === question.topicId) && !request.excludedQuestionIds.includes(question.id));
      const pool = candidates.length > 0 ? candidates : questions.filter((question) => question.difficulty === request.difficulty && (request.topicId === null || request.topicId === question.topicId));
      const [ordered, random] = shuffle(pool, request.random);
      return { question: ordered[0], random, recycledAfterExhaustion: candidates.length === 0 };
    },
    getQuestion(id) { return questions.find((question) => question.id === id); }
  };
}

function frame(state: SoloState, commands: Parameters<typeof reduceSoloFrame>[1]["commands"], elapsed = 0) {
  return reduceSoloFrame(state, { atMs: state.lastFrameAtMs + elapsed, commands }, context());
}

function finishCorrectQuestion(state: SoloState): SoloState {
  if (state.phase.kind === "topic") state = frame(state, [{ type: "confirm-topic" }]);
  else if (state.phase.kind === "risk") state = frame(state, [{ type: "accept-risk" }]);
  if (state.phase.kind !== "answering") throw new Error("Expected an answering solo phase");
  state = frame(state, [{ type: "answer", position: state.phase.round.correctPosition }]);
  if (state.phase.kind !== "reveal") throw new Error("Expected a solo reveal");
  return frame(state, [{ type: "continue" }]);
}

describe("solo-endless-v1", () => {
  it("plans the approved opening and endless hard-risk loop", () => {
    expect(Array.from({ length: 25 }, (_, index) => soloSlotAt(index))).toEqual([
      ...Array.from({ length: 4 }, () => ({ kind: "normal", difficulty: "easy" })),
      { kind: "risk", difficulty: "easy" },
      ...Array.from({ length: 3 }, () => ({ kind: "normal", difficulty: "medium" })),
      { kind: "normal", difficulty: "hard" }, { kind: "risk", difficulty: "medium" },
      ...Array.from({ length: 3 }, () => ({ kind: "normal", difficulty: "medium" })),
      { kind: "normal", difficulty: "hard" }, { kind: "risk", difficulty: "medium" },
      ...Array.from({ length: 3 }, () => ({ kind: "normal", difficulty: "medium" })),
      { kind: "normal", difficulty: "hard" }, { kind: "risk", difficulty: "hard" },
      ...Array.from({ length: 3 }, () => ({ kind: "normal", difficulty: "medium" })),
      { kind: "normal", difficulty: "hard" }, { kind: "risk", difficulty: "hard" }
    ]);
  });

  it("starts with three easy topics and makes risk acceptance seeded", () => {
    const first = createSoloRun({ profile: "solo-endless-v1" }, "same", 0, context());
    const second = createSoloRun({ profile: "solo-endless-v1" }, "same", 0, context());
    expect(first.phase).toEqual(second.phase);
    expect(first.phase.kind).toBe("topic");
    if (first.phase.kind !== "topic") throw new Error("Expected topic");
    let risk: SoloState = { ...first, slotIndex: 4, phase: { kind: "risk", difficulty: "easy" } };
    risk = frame(risk, [{ type: "accept-risk" }]);
    expect(risk.phase.kind).toBe("answering");
    expect(risk.phase.kind === "answering" && risk.phase.round.points).toBe(300);
    const firstAccepted = frame({ ...first, slotIndex: 4, phase: { kind: "risk", difficulty: "easy" } }, [{ type: "accept-risk" }]);
    const secondAccepted = frame({ ...second, slotIndex: 4, phase: { kind: "risk", difficulty: "easy" } }, [{ type: "accept-risk" }]);
    expect(firstAccepted).toEqual(secondAccepted);
  });

  it("uses catalog exclusions without repeats and reproduces the same seed/history", () => {
    let first = createSoloRun({ profile: "solo-endless-v1", collectQuestionFeedback: false }, "catalog-history", 0, context());
    let second = createSoloRun({ profile: "solo-endless-v1", collectQuestionFeedback: false }, "catalog-history", 0, context());
    for (let index = 0; index < 5; index += 1) {
      first = finishCorrectQuestion(first);
      second = finishCorrectQuestion(second);
    }
    expect(first.usedQuestionIds).toHaveLength(5);
    expect(new Set(first.usedQuestionIds).size).toBe(5);
    expect(second.usedQuestionIds).toEqual(first.usedQuestionIds);
    expect(second.random).toEqual(first.random);
    expect(second.phase).toEqual(first.phase);
  });

  it("applies refusal penalties without exposing a question", () => {
    const initial = createSoloRun({ profile: "solo-endless-v1" }, "decline", 0, context());
    const risk = { ...initial, slotIndex: 4, phase: { kind: "risk", difficulty: "easy" } as const };
    const next = frame(risk, [{ type: "decline-risk" }]);
    expect(next.score).toBe(-100);
    expect(next.lives).toBe(3);
    expect(next.usedQuestionIds).toEqual([]);
    expect(next.slotIndex).toBe(5);
  });

  it("confirms the risk option selected by the same horizontal cursor as menus", () => {
    const initial = createSoloRun({ profile: "solo-endless-v1" }, "risk-cursor", 0, context());
    const risk = { ...initial, slotIndex: 4, phase: { kind: "risk", difficulty: "easy", cursor: 0 } as const };
    const declined = frame(frame(risk, [{ type: "move-risk", delta: 1 }]), [{ type: "confirm-risk" }]);
    expect(declined).toMatchObject({ score: -100, slotIndex: 5, phase: { kind: "topic" } });
    const accepted = frame(frame(risk, [{ type: "move-risk", delta: -1 }]), [{ type: "confirm-risk" }]);
    expect(accepted.phase).toMatchObject({ kind: "answering", round: { risk: true, points: 300 } });
  });

  it("keeps bonus topic hidden and ignores commands from another phase", () => {
    const initial = createSoloRun({ profile: "solo-endless-v1" }, "risk-gate", 0, context());
    const risk = { ...initial, slotIndex: 9, score: -100, phase: { kind: "risk", difficulty: "medium" } as const };
    const ignored = frame(risk, [{ type: "answer", position: "up" }, { type: "select-topic", index: 0 }, { type: "continue" }]);
    expect(ignored).toEqual(risk);
    const declined = frame(risk, [{ type: "decline-risk" }]);
    expect(declined.score).toBe(-300);
    const hardRisk = { ...risk, slotIndex: 19, phase: { kind: "risk", difficulty: "hard" } as const };
    expect(frame(hardRisk, [{ type: "decline-risk" }]).score).toBe(-400);
    const accepted = frame(risk, [{ type: "accept-risk" }]);
    expect(accepted.phase.kind).toBe("answering");
    expect(accepted.phase.kind === "answering" && accepted.phase.round.topicId).toBeTruthy();
    expect(accepted.phase.kind === "answering" && accepted.phase.round.points).toBe(600);
  });

  it("keeps a wrong selected position for reveal presentation", () => {
    let state = createSoloRun({ profile: "solo-endless-v1", collectQuestionFeedback: false }, "wrong-reveal", 0, context());
    state = frame(state, [{ type: "confirm-topic" }]);
    if (state.phase.kind !== "answering") throw new Error("Expected an answering solo phase");
    const selected = state.phase.round.correctPosition === "up" ? "right" : "up";
    state = frame(state, [{ type: "answer", position: selected }]);
    expect(state.phase).toMatchObject({ kind: "reveal", result: "wrong", answer: selected });
  });

  it("freezes both clocks while paused and moves correct runs through feedback only when enabled", () => {
    let state = createSoloRun({ profile: "solo-endless-v1" }, "pause-feedback", 0, context());
    state = frame(state, [{ type: "confirm-topic" }]);
    state = frame(state, [], 10_100);
    expect(state.phase.kind).toBe("answering");
    expect(state.reserveMs).toBe(59_900);
    state = frame(state, [{ type: "pause" }]);
    state = frame(state, [], 30_000);
    expect(state.reserveMs).toBe(59_900);
    state = frame(state, [{ type: "resume" }]);
    if (state.phase.kind !== "answering") throw new Error("Expected active answer");
    state = frame(state, [{ type: "answer", position: state.phase.round.correctPosition }]);
    expect(state.phase.kind).toBe("reveal");
    state = frame(state, [{ type: "continue" }]);
    expect(state.phase.kind).toBe("feedback");
    if (state.phase.kind !== "feedback") throw new Error("Expected feedback");
    const eventId = state.phase.eventId;
    state = frame(state, [{ type: "set-feedback-choice", hasComplaint: false }]);
    state = frame(state, [{ type: "confirm-feedback", eventId: "wrong" }]);
    expect(state.phase.kind).toBe("feedback");
    state = frame(state, [{ type: "confirm-feedback", eventId }]);
    expect(state.phase.kind).toBe("topic");
  });

  it("keeps the final reserve error revealed until continuation", () => {
    let state = createSoloRun({ profile: "solo-endless-v1", collectQuestionFeedback: false }, "timer", 0, context());
    for (let index = 0; index < 3; index += 1) {
      if (state.phase.kind !== "topic") throw new Error("Expected topic");
      state = frame(state, [{ type: "confirm-topic" }]);
      state = frame(state, [], 70_000);
      if (index < 2) {
        expect(state.phase.kind).toBe("reveal");
        state = frame(state, [{ type: "continue" }]);
      }
    }
    expect(state.phase.kind).toBe("reveal");
    if (state.phase.kind !== "reveal") throw new Error("Expected final reveal");
    expect(state.phase.final).toBe(true);
    state = frame(state, [{ type: "continue" }]);
    expect(state.phase.kind).toBe("finished");
    expect(state.lives).toBe(0);
    expect(state.reserveMs).toBe(0);
  });
});
