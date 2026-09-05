import { nextInt, seedRandom, shuffle, type RandomState } from "./prng";
import {
  ANSWER_POSITIONS,
  type AnswerId,
  type AnswerPosition,
  type ComplaintReason,
  type Difficulty,
  type DomainContext,
  type QuestionDefinition,
  type QuestionId,
  type TopicId
} from "./types";

export const SOLO_ENDLESS_V1 = Object.freeze({
  id: "solo-endless-v1" as const,
  baseAnswerTimeMs: 10_000,
  reserveMs: 60_000,
  lives: 3,
  bonusMultiplier: 3,
  basePoints: { easy: 100, medium: 200, hard: 300 } as const
});

export interface SoloConfig {
  readonly profile: "solo-endless-v1";
  readonly collectQuestionFeedback?: boolean;
}

export interface SoloSlot {
  readonly kind: "normal" | "risk";
  readonly difficulty: Difficulty;
}

export interface SoloRound {
  readonly questionId: QuestionId;
  readonly topicId: TopicId;
  readonly difficulty: Difficulty;
  readonly risk: boolean;
  readonly points: number;
  readonly answerOrder: readonly [AnswerId, AnswerId, AnswerId, AnswerId];
  readonly correctPosition: AnswerPosition;
}

export type SoloPhase =
  | { readonly kind: "topic"; readonly candidates: readonly [TopicId, TopicId, TopicId]; readonly cursor: number }
  | { readonly kind: "risk"; readonly difficulty: Difficulty; readonly cursor?: 0 | 1 }
  | { readonly kind: "answering"; readonly round: SoloRound; readonly baseRemainingMs: number; readonly answer: AnswerPosition | null }
  | { readonly kind: "reveal"; readonly round: SoloRound; readonly result: "correct" | "wrong" | "no-answer"; readonly answer: AnswerPosition | null }
  | { readonly kind: "feedback"; readonly round: SoloRound; readonly result: "correct" | "wrong" | "no-answer"; readonly eventId: string; readonly hasComplaint: boolean | null; readonly feedbackCursor: number; readonly complaintReasons: readonly ComplaintReason[]; readonly complaintNote: string }
  | { readonly kind: "finished" };

export interface SoloState {
  readonly schemaVersion: 1;
  readonly catalogRevision: string;
  readonly runId: string;
  readonly seed: string;
  readonly random: RandomState;
  readonly config: Required<SoloConfig>;
  readonly slotIndex: number;
  readonly score: number;
  readonly lives: number;
  readonly reserveMs: number;
  readonly usedQuestionIds: readonly QuestionId[];
  readonly shownTopicCounts: Readonly<Record<TopicId, number>>;
  readonly recentTopicIds: readonly TopicId[];
  readonly phase: SoloPhase;
  readonly paused: boolean;
  readonly lastFrameAtMs: number;
}

export type SoloCommand =
  | { readonly type: "move-topic"; readonly delta: -1 | 1 }
  | { readonly type: "select-topic"; readonly index: 0 | 1 | 2 }
  | { readonly type: "confirm-topic" }
  | { readonly type: "move-risk"; readonly delta: -1 | 1 }
  | { readonly type: "confirm-risk" }
  | { readonly type: "accept-risk" }
  | { readonly type: "decline-risk" }
  | { readonly type: "answer"; readonly position: AnswerPosition }
  | { readonly type: "continue" }
  | { readonly type: "set-feedback-choice"; readonly hasComplaint: boolean }
  | { readonly type: "set-feedback-cursor"; readonly cursor: number }
  | { readonly type: "toggle-feedback-reason"; readonly reason: ComplaintReason }
  | { readonly type: "set-feedback-note"; readonly note: string }
  | { readonly type: "confirm-feedback"; readonly eventId: string }
  | { readonly type: "pause" }
  | { readonly type: "resume" };

export interface SoloFrame {
  readonly atMs: number;
  readonly commands: readonly SoloCommand[];
}

export function soloSlotAt(index: number): SoloSlot {
  if (!Number.isSafeInteger(index) || index < 0) throw new RangeError("Solo slot index must be non-negative");
  if (index < 4) return { kind: "normal", difficulty: "easy" };
  if (index === 4) return { kind: "risk", difficulty: "easy" };
  const afterEasy = index - 5;
  const earlyBlock = Math.floor(afterEasy / 5);
  const withinBlock = afterEasy % 5;
  const difficulty: Difficulty = withinBlock < 3 ? "medium" : withinBlock === 3 ? "hard" : earlyBlock < 2 ? "medium" : "hard";
  return { kind: withinBlock === 4 ? "risk" : "normal", difficulty };
}

function asTriple(values: readonly TopicId[]): readonly [TopicId, TopicId, TopicId] {
  if (values.length !== 3 || new Set(values).size !== 3) throw new Error("Solo requires three unique topic candidates");
  return [values[0], values[1], values[2]];
}

function addShownTopics(counts: Readonly<Record<TopicId, number>>, topics: readonly TopicId[]) {
  const next = { ...counts };
  for (const topicId of topics) next[topicId] = (next[topicId] ?? 0) + 1;
  return next;
}

function prepareSlot(state: SoloState, context: DomainContext): SoloState {
  const slot = soloSlotAt(state.slotIndex);
  if (slot.kind === "risk") return { ...state, phase: { kind: "risk", difficulty: slot.difficulty, cursor: 0 } };
  const selection = context.selectTopics({
    count: 3,
    difficulty: slot.difficulty,
    excludedTopicIds: state.recentTopicIds,
    shownTopicCounts: state.shownTopicCounts,
    random: state.random
  });
  const candidates = asTriple(selection.topicIds);
  return {
    ...state,
    random: selection.random,
    shownTopicCounts: addShownTopics(state.shownTopicCounts, candidates),
    phase: { kind: "topic", candidates, cursor: 0 }
  };
}

function correctPosition(answerOrder: readonly AnswerId[], correctId: AnswerId): AnswerPosition {
  const index = answerOrder.indexOf(correctId);
  if (index < 0) throw new Error("Correct answer is absent from solo answer order");
  return ANSWER_POSITIONS[index];
}

function startQuestion(state: SoloState, context: DomainContext, topicId: TopicId | null, risk: boolean): SoloState {
  const difficulty = soloSlotAt(state.slotIndex).difficulty;
  const selection = context.selectQuestion({
    topicId,
    difficulty,
    excludedQuestionIds: state.usedQuestionIds,
    allowRecycleWhenExhausted: true,
    random: state.random
  });
  const question: QuestionDefinition = selection.question;
  if (question.difficulty !== difficulty || (topicId !== null && question.topicId !== topicId)) throw new Error("Solo question selection mismatch");
  const [answerIds, random] = shuffle(question.answers.map(({ id }) => id), selection.random);
  const answerOrder = answerIds as readonly [AnswerId, AnswerId, AnswerId, AnswerId];
  const points = SOLO_ENDLESS_V1.basePoints[difficulty] * (risk ? SOLO_ENDLESS_V1.bonusMultiplier : 1);
  return {
    ...state,
    random,
    usedQuestionIds: selection.recycledAfterExhaustion ? [question.id] : [...state.usedQuestionIds, question.id],
    recentTopicIds: [question.topicId, ...state.recentTopicIds].slice(0, 2),
    phase: {
      kind: "answering",
      round: { questionId: question.id, topicId: question.topicId, difficulty, risk, points, answerOrder, correctPosition: correctPosition(answerOrder, question.correctAnswerId) },
      baseRemainingMs: SOLO_ENDLESS_V1.baseAnswerTimeMs,
      answer: null
    }
  };
}

export function createSoloRun(config: SoloConfig, seed: string, atMs: number, context: DomainContext, runId = `solo-v1:${seed}`): SoloState {
  if (config.profile !== SOLO_ENDLESS_V1.id) throw new Error("Unknown solo profile");
  if (!Number.isFinite(atMs) || !runId) throw new RangeError("Solo run requires a finite time and id");
  return prepareSlot({
    schemaVersion: 1,
    catalogRevision: context.catalogRevision,
    runId,
    seed,
    random: seedRandom(seed),
    config: { profile: config.profile, collectQuestionFeedback: config.collectQuestionFeedback ?? true },
    slotIndex: 0,
    score: 0,
    lives: SOLO_ENDLESS_V1.lives,
    reserveMs: SOLO_ENDLESS_V1.reserveMs,
    usedQuestionIds: [],
    shownTopicCounts: {},
    recentTopicIds: [],
    phase: { kind: "risk", difficulty: "easy" },
    paused: false,
    lastFrameAtMs: atMs
  }, context);
}

function settle(state: SoloState, result: "correct" | "wrong" | "no-answer"): SoloState {
  if (state.phase.kind !== "answering") return state;
  const score = result === "correct" ? state.score + state.phase.round.points : state.score;
  const lives = result === "correct" ? state.lives : state.lives - 1;
  return { ...state, score, lives, phase: lives === 0 ? { kind: "finished" } : { kind: "reveal", round: state.phase.round, result, answer: state.phase.answer } };
}

function advance(state: SoloState, atMs: number): SoloState {
  if (state.paused || atMs <= state.lastFrameAtMs) return { ...state, lastFrameAtMs: atMs };
  if (state.phase.kind !== "answering") return { ...state, lastFrameAtMs: atMs };
  const elapsed = atMs - state.lastFrameAtMs;
  const baseSpent = Math.min(elapsed, state.phase.baseRemainingMs);
  const baseRemainingMs = state.phase.baseRemainingMs - baseSpent;
  const reserveMs = state.phase.answer === null && baseRemainingMs === 0 ? Math.max(0, state.reserveMs - (elapsed - baseSpent)) : state.reserveMs;
  const advanced = { ...state, reserveMs, lastFrameAtMs: atMs, phase: { ...state.phase, baseRemainingMs } };
  return advanced.phase.answer === null && reserveMs === 0 ? settle(advanced, "no-answer") : advanced;
}

function nextSlot(state: SoloState, context: DomainContext) {
  return prepareSlot({ ...state, slotIndex: state.slotIndex + 1 }, context);
}

export function reduceSoloFrame(state: SoloState, frame: SoloFrame, context: DomainContext): SoloState {
  if (!Number.isFinite(frame.atMs) || frame.atMs < state.lastFrameAtMs) return state;
  const wasAnswering = state.phase.kind === "answering";
  let next = advance(state, frame.atMs);
  if (wasAnswering && (next.phase.kind === "reveal" || next.phase.kind === "finished")) return next;
  for (const command of frame.commands) {
    if (command.type === "pause") return { ...next, paused: true };
    if (next.paused) { if (command.type === "resume") next = { ...next, paused: false }; continue; }
    if (command.type === "resume") continue;
    if (next.phase.kind === "topic") {
      if (command.type === "move-topic") {
        const cursor = (next.phase.cursor + command.delta + 3) % 3;
        next = { ...next, phase: { ...next.phase, cursor } };
      } else if (command.type === "confirm-topic" || command.type === "select-topic") {
        const index = command.type === "select-topic" ? command.index : next.phase.cursor;
        return startQuestion(next, context, next.phase.candidates[index], false);
      }
    } else if (next.phase.kind === "risk") {
      if (command.type === "move-risk") return { ...next, phase: { ...next.phase, cursor: command.delta < 0 ? 0 : 1 } };
      const accepted = command.type === "accept-risk" || (command.type === "confirm-risk" && (next.phase.cursor ?? 0) === 0);
      const declined = command.type === "decline-risk" || (command.type === "confirm-risk" && (next.phase.cursor ?? 0) === 1);
      if (accepted) return startQuestion(next, context, null, true);
      if (declined) return nextSlot({ ...next, score: next.score - SOLO_ENDLESS_V1.basePoints[next.phase.difficulty] }, context);
    } else if (next.phase.kind === "answering" && command.type === "answer" && next.phase.answer === null) {
      const answered = { ...next, phase: { ...next.phase, answer: command.position } };
      return settle(answered, command.position === answered.phase.round.correctPosition ? "correct" : "wrong");
    } else if (next.phase.kind === "reveal" && command.type === "continue") {
      if (!next.config.collectQuestionFeedback) return nextSlot(next, context);
      return {
        ...next,
        phase: {
          kind: "feedback",
          round: next.phase.round,
          result: next.phase.result,
          eventId: `feedback-v3:${next.runId}:solo-${next.slotIndex + 1}:${next.phase.round.questionId}`,
          hasComplaint: null,
          feedbackCursor: 1,
          complaintReasons: [],
          complaintNote: ""
        }
      };
    } else if (next.phase.kind === "feedback") {
      if (command.type === "set-feedback-choice") {
        return { ...next, phase: { ...next.phase, hasComplaint: command.hasComplaint, feedbackCursor: command.hasComplaint ? 0 : 1, complaintReasons: command.hasComplaint ? next.phase.complaintReasons : [], complaintNote: command.hasComplaint ? next.phase.complaintNote : "" } };
      }
      if (command.type === "set-feedback-cursor") {
        const maximum = next.phase.hasComplaint === true ? 7 : 1;
        return { ...next, phase: { ...next.phase, feedbackCursor: Math.max(0, Math.min(maximum, command.cursor)) } };
      }
      if (command.type === "toggle-feedback-reason" && next.phase.hasComplaint) {
        const complaintReasons = next.phase.complaintReasons.includes(command.reason)
          ? next.phase.complaintReasons.filter((reason) => reason !== command.reason)
          : [...next.phase.complaintReasons, command.reason];
        return { ...next, phase: { ...next.phase, complaintReasons } };
      }
      if (command.type === "set-feedback-note" && next.phase.hasComplaint) {
        return { ...next, phase: { ...next.phase, complaintNote: command.note.slice(0, 500) } };
      }
      if (command.type === "confirm-feedback" && command.eventId === next.phase.eventId) return nextSlot(next, context);
    }
  }
  return next;
}
