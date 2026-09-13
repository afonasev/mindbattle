import { describe, it, expect } from "vitest";
import {
  createMatch,
  reduceFrame,
  activeTeams,
  choiceQueue,
  bonusParticipants,
  excludeNetworkPlayer,
} from "../../src/domain/match";
import { validateMatchConfig } from "../../src/domain/classic";
import { shuffle } from "../../src/domain/prng";
import type {
  DomainContext,
  QuestionDefinition,
  MatchState,
  DomainCommand,
  TeamId,
} from "../../src/domain/types";
import {
  deserializeMatch,
  serializeMatch,
} from "../../src/domain/serialization";
import { game, ids, send } from "./network-fixture";
function question(state: MatchState, context: DomainContext) {
  if (state.phase.kind === "normal-topic")
    state = send(state, context, [
      { type: "confirm-topic", teamId: state.phase.chooser },
    ]);
  if (state.phase.kind === "bonus-veto") {
    const topics = state.phase.candidates;
    state = send(
      state,
      context,
      bonusParticipants(state).map((teamId, i) => ({
        type: "set-veto",
        teamId,
        topicId: topics[i],
      })),
    );
  }
  return state.phase.kind === "topic-confirmation"
    ? send(state, context, [], 3000)
    : state;
}
function resolve(state: MatchState, context: DomainContext) {
  state = question(state, context);
  if (state.phase.kind !== "answering") throw Error(state.phase.kind);
  const position = state.phase.round.correctPosition;
  return send(
    state,
    context,
    activeTeams(state).map((teamId) => ({ type: "answer", teamId, position })),
  );
}
describe("network rules", () => {
  it("validates distinct independent IDs and keeps classic limited", () => {
    expect(() => game()).not.toThrow();
    expect(() => game(1)).toThrow();
    expect(() =>
      validateMatchConfig({
        ...game().state.config,
        teams: [...ids, "player-13"],
      }),
    ).toThrow();
    expect(() =>
      validateMatchConfig({ ...game().state.config, profile: "classic-v1" }),
    ).toThrow();
  });
  it("cycles bonus participants without consuming ordinary choices", () => {
    let { state, context } = game();
    for (let i = 0; i < 2; i++) {
      state = resolve(state, context);
      state = send(state, context, [{ type: "continue", teamId: ids[0] }]);
    }
    expect(state.phase.kind).toBe("bonus-veto");
    const queue = choiceQueue(state);
    const ordinal = state.normalChoiceOrdinal;
    expect(bonusParticipants(state)).toEqual(queue.slice(0, 4));
    if (state.phase.kind !== "bonus-veto") throw Error();
    expect(state.phase.candidates).toHaveLength(5);
    const ignored = send(state, context, [
      { type: "set-veto", teamId: queue[4] },
    ]);
    expect(ignored.phase).toEqual(state.phase);
    state = resolve(state, context);
    state = send(state, context, [{ type: "continue", teamId: ids[0] }]);
    state = send(state, context, [{ type: "continue", teamId: ids[0] }]);
    expect(state.normalChoiceOrdinal).toBe(ordinal);
    expect(state.phase).toMatchObject({
      kind: "normal-topic",
      chooser: queue[0],
    });
  });
  it("round-trips network snapshots including reduced bonus ballots", () => {
    let { state, context } = game(4);
    for (let i = 0; i < 2; i++) {
      state = resolve(state, context);
      state = send(state, context, [{ type: "continue", teamId: ids[0] }]);
    }
    state = excludeNetworkPlayer(state, bonusParticipants(state)[0], context);
    expect(
      deserializeMatch(serializeMatch(state), context.catalogRevision),
    ).toEqual(state);
    const bad = { ...state, departedTeamIds: ["player-99"] };
    expect(
      deserializeMatch(JSON.stringify(bad), context.catalogRevision),
    ).toBeNull();
  });
  it("preserves next player when a predecessor departs", () => {
    let { state, context } = game();
    const queue = choiceQueue(state);
    state = excludeNetworkPlayer(state, queue[11], context);
    expect(choiceQueue(state)[0]).toBe(queue[0]);
    state = excludeNetworkPlayer(state, queue[0], context);
    expect(state.phase).toMatchObject({ chooser: queue[1] });
    state = question(state, context);
    expect(choiceQueue(state)[0]).toBe(queue[2]);
  });
  it("freezes every timer and preserves a submitted answer", () => {
    let { state, context } = game();
    state = question(state, context);
    state = send(
      state,
      context,
      [{ type: "answer", teamId: ids[0], position: "up" }],
      11000,
    );
    state = send(state, context, [
      { type: "pause", reason: { kind: "manual" } },
    ]);
    const phase = state.phase;
    const teams = state.teams;
    state = send(state, context, [], 30000);
    expect(state.phase).toEqual(phase);
    expect(state.teams).toEqual(teams);
  });
  it("restarts only affected bonus ballots and reduces candidates below four", () => {
    let { state, context } = game(4);
    for (let i = 0; i < 2; i++) {
      state = resolve(state, context);
      state = send(state, context, [{ type: "continue", teamId: ids[0] }]);
    }
    const voter = bonusParticipants(state)[0];
    state = send(state, context, [{ type: "set-veto", teamId: voter }]);
    state = excludeNetworkPlayer(state, voter, context);
    expect(state.phase).toMatchObject({ kind: "bonus-veto", vetoes: {} });
    if (state.phase.kind !== "bonus-veto") throw Error();
    expect(state.phase.candidates).toHaveLength(4);
  });
  it("retains departed score but ends at one active player", () => {
    let { state, context } = game(2);
    state = resolve(state, context);
    const score = state.teams[0].score;
    state = excludeNetworkPlayer(state, ids[0], context);
    expect(state.teams[0].score).toBe(score);
    expect(state.endReason).toBe("insufficient-players");
    expect(state.phase).toMatchObject({ kind: "finished", winnerId: ids[1] });
  });
  it("plays nine questions with twelve then a direct final question", () => {
    let { state, context } = game();
    for (let i = 0; i < 9; i++) {
      state = resolve(state, context);
      state = send(state, context, [{ type: "continue", teamId: ids[0] }]);
      if (state.phase.kind === "standings" && i < 8)
        state = send(state, context, [{ type: "continue", teamId: ids[0] }]);
    }
    state = send(state, context, [{ type: "continue", teamId: ids[0] }]);
    expect(state.phase.kind).toBe("answering");
    if (state.phase.kind !== "answering") throw Error();
    expect(state.phase.round.mode).toBe("tie-break");
    expect(state.phase.round.points).toBe(0);
  });
  it("keeps the decided tie-break winner when a loser departs during reveal", () => {
    let { state, context } = game(3);
    state = {
      ...state,
      teams: state.teams.map((t) => ({ ...t, score: 100 })),
      phase: {
        kind: "standings",
        completedStage: 3,
        tieBreakContenders: ids.slice(0, 3),
      },
    };
    state = send(state, context, [{ type: "continue", teamId: ids[0] }]);
    if (state.phase.kind !== "answering") throw Error();
    const correct = state.phase.round.correctPosition;
    const wrong = correct === "up" ? "right" : "up";
    state = send(
      state,
      context,
      ids
        .slice(0, 3)
        .map((teamId, i) => ({
          type: "answer",
          teamId,
          position: i === 0 ? correct : wrong,
        })),
    );
    state = excludeNetworkPlayer(state, ids[2], context);
    expect(state.phase).toMatchObject({
      kind: "reveal",
      continuation: { kind: "finished", winnerId: ids[0] },
    });
  });
});
