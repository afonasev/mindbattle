import { describe, expect, it } from "vitest";
import {
  InvalidMatchConfigError,
  pointsFor,
  reserveFor,
  validateMatchConfig
} from "../../src/domain/classic";
import { createMatch, reduceFrame } from "../../src/domain/match";
import { nextUint32, seedRandom, shuffle } from "../../src/domain/prng";
import { deserializeMatch, serializeMatch } from "../../src/domain/serialization";
import { selectPublicView, selectStandings } from "../../src/domain/selectors";
import type {
  DomainCommand,
  DomainContext,
  MatchConfig,
  MatchState,
  QuestionDefinition,
  TeamId
} from "../../src/domain/types";

const TWO_TEAMS: MatchConfig = {
  profile: "classic-v1",
  questionCount: 9,
  answerTimeMs: 10_000,
  teams: ["green", "blue"]
};

function makeContext(topicCount = 40): DomainContext {
  const topics = Array.from({ length: topicCount }, (_, index) => `topic-${index}`);
  const questions: QuestionDefinition[] = topics.flatMap((topicId) =>
    (["easy", "medium", "hard"] as const).flatMap((difficulty) =>
      Array.from({ length: 12 }, (_, index): QuestionDefinition => ({
        id: `${topicId}.${difficulty}.${index}`,
        topicId,
        difficulty,
        prompt: `Вопрос ${topicId} ${difficulty} ${index}`,
        answers: [
          { id: "a", text: "Верный" },
          { id: "b", text: "Второй" },
          { id: "c", text: "Третий" },
          { id: "d", text: "Четвёртый" }
        ],
        correctAnswerId: "a",
        explanation: ["Верный ответ подтверждён.", "Это тестовая справка."],
        source: { title: "Тестовый источник", url: "https://example.com/question" }
      }))
    )
  );
  const byId = new Map(questions.map((question) => [question.id, question]));
  return {
    catalogRevision: "fixture-r1",
    selectTopics(request) {
      const eligible = topics.filter((topicId) => !request.excludedTopicIds.includes(topicId));
      const [ordered, random] = shuffle(eligible, request.random);
      return { topicIds: ordered.slice(0, request.count), random };
    },
    selectQuestion(request) {
      const eligible = questions.filter(
        (question) =>
          question.difficulty === request.difficulty &&
          (request.topicId === null || question.topicId === request.topicId) &&
          !request.excludedQuestionIds.includes(question.id)
      );
      if (eligible.length === 0) throw new Error("fixture catalog exhausted");
      const [ordered, random] = shuffle(eligible, request.random);
      return { question: ordered[0], random };
    },
    getQuestion(questionId) {
      return byId.get(questionId);
    }
  };
}

function frame(
  state: MatchState,
  context: DomainContext,
  commands: readonly DomainCommand[],
  elapsedMs = 0
): MatchState {
  return reduceFrame(
    state,
    { atMs: state.lastFrameAtMs + elapsedMs, sequence: 1, commands },
    context
  );
}

function startQuestion(state: MatchState, context: DomainContext): MatchState {
  if (state.phase.kind === "normal-topic") {
    const confirmation = frame(state, context, [
      {
        type: "choose-topic",
        teamId: state.phase.chooser,
        topicId: state.phase.candidates[0]
      }
    ]);
    return frame(confirmation, context, [{ type: "continue", teamId: "green" }]);
  }
  if (state.phase.kind === "bonus-veto") {
    const confirmation = frame(
      state,
      context,
      state.config.teams.map((teamId, index) => ({
        type: "set-veto" as const,
        teamId,
        topicId: state.phase.kind === "bonus-veto" ? state.phase.candidates[index] : ""
      }))
    );
    if (confirmation.phase.kind !== "topic-confirmation") {
      throw new Error("Expected bonus topic confirmation");
    }
    return frame(confirmation, context, [{ type: "continue", teamId: "green" }]);
  }
  throw new Error(`Expected a topic phase, received ${state.phase.kind}`);
}

function answerAllCorrect(state: MatchState, context: DomainContext): MatchState {
  if (state.phase.kind !== "answering") throw new Error("Expected answering phase");
  const correct = state.phase.round.correctPosition;
  return frame(
    state,
    context,
    state.phase.round.attempts
      .filter(({ status }) => status !== "spectator")
      .map(({ teamId }) => ({ type: "answer" as const, teamId, position: correct }))
  );
}

function continueByGreen(state: MatchState, context: DomainContext): MatchState {
  let next = frame(state, context, [{ type: "continue", teamId: "green" }]);
  if (next.phase.kind === "difficulty-feedback") {
    next = frame(next, context, [{ type: "rate-difficulty", teamId: "green", difficulty: "easy" }]);
    if (next.phase.kind !== "difficulty-feedback") throw new Error("Expected feedback phase");
    next = frame(next, context, [{ type: "confirm-difficulty-feedback", eventId: next.phase.eventId }]);
  }
  return next;
}

describe("classic-v1 and seeded PRNG", () => {
  it("validates profile boundaries and derives reserve and points", () => {
    expect(validateMatchConfig(TWO_TEAMS)).toBe(TWO_TEAMS);
    expect(reserveFor(9)).toBe(60_000);
    expect(reserveFor(15)).toBe(90_000);
    expect(reserveFor(21)).toBe(120_000);
    expect([0, 2, 3, 5, 6, 8].map((index) => pointsFor(TWO_TEAMS, index))).toEqual([
      100,
      200,
      200,
      400,
      300,
      600
    ]);
    expect(() =>
      validateMatchConfig({ ...TWO_TEAMS, teams: ["green"] } as MatchConfig)
    ).toThrow(InvalidMatchConfigError);
    expect(() =>
      validateMatchConfig({ ...TWO_TEAMS, teams: ["green", "green"] } as MatchConfig)
    ).toThrow(InvalidMatchConfigError);
    expect(() =>
      validateMatchConfig({ ...TWO_TEAMS, questionCount: 12 } as unknown as MatchConfig)
    ).toThrow(InvalidMatchConfigError);
  });

  it("replays equal seeds and separates different seeds", () => {
    let first = seedRandom("same-seed");
    let repeated = seedRandom("same-seed");
    let different = seedRandom("different-seed");
    const firstValues: number[] = [];
    const repeatedValues: number[] = [];
    const differentValues: number[] = [];
    for (let index = 0; index < 8; index += 1) {
      let value: number;
      [value, first] = nextUint32(first);
      firstValues.push(value);
      [value, repeated] = nextUint32(repeated);
      repeatedValues.push(value);
      [value, different] = nextUint32(different);
      differentValues.push(value);
    }
    expect(repeatedValues).toEqual(firstValues);
    expect(differentValues).not.toEqual(firstValues);
    expect(JSON.parse(JSON.stringify(first))).toEqual(first);
  });

  it("rejects structurally corrupted nested snapshots", () => {
    const context = makeContext();
    const state = createMatch(TWO_TEAMS, "snapshot", 0, context);
    const broken = {
      ...state,
      phase: { kind: "answering", round: {}, baseRemainingMs: 10_000 }
    };
    expect(deserializeMatch(JSON.stringify(broken), context.catalogRevision)).toBeNull();
  });
});

describe("topic phases", () => {
  it("holds a chosen normal topic for three seconds before creating its question", () => {
    const context = makeContext();
    const initial = createMatch(TWO_TEAMS, "topic-confirmation", 0, context);
    if (initial.phase.kind !== "normal-topic") throw new Error("Expected topic choice");
    const confirmation = frame(initial, context, [{
      type: "choose-topic",
      teamId: initial.phase.chooser,
      topicId: initial.phase.candidates[0]
    }]);
    expect(confirmation.phase).toEqual({
      kind: "topic-confirmation",
      topicId: initial.phase.candidates[0],
      remainingMs: 3_000
    });
    expect(confirmation.usedQuestionIds).toEqual([]);
    expect(selectPublicView(confirmation, context).confirmationBonus).toBe(false);
    const waiting = frame(confirmation, context, [], 2_999);
    expect(waiting.phase.kind).toBe("topic-confirmation");
    const answering = frame(waiting, context, [], 1);
    expect(answering.phase.kind).toBe("answering");
    expect(answering.phase.kind === "answering" && answering.phase.baseRemainingMs).toBe(10_000);
  });

  it("allows a new continue press to start the question without accepting an answer in that frame", () => {
    const context = makeContext();
    const initial = createMatch(TWO_TEAMS, "topic-manual", 0, context);
    if (initial.phase.kind !== "normal-topic") throw new Error("Expected topic choice");
    const confirmation = frame(initial, context, [{
      type: "choose-topic",
      teamId: initial.phase.chooser,
      topicId: initial.phase.candidates[0]
    }]);
    const answering = frame(confirmation, context, [
      { type: "continue", teamId: "green" },
      { type: "answer", teamId: "green", position: "up" }
    ]);
    expect(answering.phase.kind).toBe("answering");
    expect(answering.phase.kind === "answering" && answering.phase.round.attempts[0]).toMatchObject({
      status: "open",
      answer: null
    });
  });

  it("freezes topic confirmation while paused", () => {
    const context = makeContext();
    const initial = createMatch(TWO_TEAMS, "topic-pause", 0, context);
    if (initial.phase.kind !== "normal-topic") throw new Error("Expected topic choice");
    const confirmation = frame(initial, context, [{
      type: "choose-topic",
      teamId: initial.phase.chooser,
      topicId: initial.phase.candidates[0]
    }]);
    const paused = frame(confirmation, context, [{ type: "pause", reason: { kind: "manual" } }], 1_000);
    expect(paused.phase.kind === "topic-confirmation" && paused.phase.remainingMs).toBe(2_000);
    const stillPaused = frame(paused, context, [], 20_000);
    expect(stillPaused.phase.kind === "topic-confirmation" && stillPaused.phase.remainingMs).toBe(2_000);
    const resumed = frame(stillPaused, context, [{ type: "resume" }]);
    const answering = frame(resumed, context, [], 2_000);
    expect(answering.phase.kind).toBe("answering");
  });

  it("uses a seeded cyclic chooser and rejects another team", () => {
    const context = makeContext();
    const first = createMatch(TWO_TEAMS, "chooser-seed", 0, context);
    const repeated = createMatch(TWO_TEAMS, "chooser-seed", 0, context);
    expect(repeated.phase).toEqual(first.phase);
    expect(first.phase.kind).toBe("normal-topic");
    if (first.phase.kind !== "normal-topic") return;
    const chooser = first.phase.chooser;
    const other = TWO_TEAMS.teams.find((teamId) => teamId !== chooser) as TeamId;
    const rejected = frame(first, context, [
      { type: "choose-topic", teamId: other, topicId: first.phase.candidates[0] }
    ]);
    expect(rejected.phase).toEqual(first.phase);

    let state = startQuestion(first, context);
    state = answerAllCorrect(state, context);
    state = continueByGreen(state, context);
    expect(state.phase.kind).toBe("normal-topic");
    if (state.phase.kind === "normal-topic") expect(state.phase.chooser).toBe(other);
  });

  it("holds the sole bonus remainder for confirmation before starting with full time", () => {
    const context = makeContext();
    let state = createMatch(TWO_TEAMS, "bonus-seed", 0, context);
    for (let questionIndex = 0; questionIndex < 2; questionIndex += 1) {
      state = startQuestion(state, context);
      state = answerAllCorrect(state, context);
      state = continueByGreen(state, context);
    }
    expect(state.phase.kind).toBe("bonus-veto");
    if (state.phase.kind !== "bonus-veto") return;
    expect(state.phase.candidates).toHaveLength(3);
    const [first, second] = state.phase.candidates;
    state = frame(state, context, [
      { type: "set-veto", teamId: "green", topicId: first },
      { type: "set-veto", teamId: "blue", topicId: first }
    ]);
    expect(state.phase.kind).toBe("bonus-veto");
    if (state.phase.kind !== "bonus-veto") return;
    expect(state.phase.vetoes).toEqual({ green: first, blue: first });
    const randomBeforeConfirmation = state.random;
    const usedBeforeConfirmation = state.usedQuestionIds;
    state = frame(state, context, [{ type: "set-veto", teamId: "blue", topicId: second }]);
    expect(state.phase.kind).toBe("topic-confirmation");
    if (state.phase.kind !== "topic-confirmation") return;
    expect(state.phase.remainingMs).toBe(3_000);
    expect([first, second]).not.toContain(state.phase.topicId);
    expect(state.random).toEqual(randomBeforeConfirmation);
    expect(state.usedQuestionIds).toEqual(usedBeforeConfirmation);
    expect(selectPublicView(state, context)).toMatchObject({
      topicId: state.phase.topicId,
      confirmationRemainingMs: 3_000,
      confirmationBonus: true
    });
    expect(deserializeMatch(serializeMatch(state), context.catalogRevision)).toEqual(state);

    const manual = frame(state, context, [
      { type: "continue", teamId: "green" },
      { type: "answer", teamId: "green", position: "up" }
    ]);
    expect(manual.phase.kind).toBe("answering");
    if (manual.phase.kind === "answering") {
      expect(manual.phase.baseRemainingMs).toBe(10_000);
      expect(manual.phase.round.points).toBe(200);
      expect(manual.phase.round.topicId).toBe(state.phase.topicId);
      expect(manual.phase.round.attempts[0]).toMatchObject({ status: "open", answer: null });
    }

    const paused = frame(state, context, [{ type: "pause", reason: { kind: "manual" } }], 1_000);
    expect(paused.phase.kind === "topic-confirmation" && paused.phase.remainingMs).toBe(2_000);
    const stillPaused = frame(paused, context, [], 20_000);
    expect(stillPaused.phase.kind === "topic-confirmation" && stillPaused.phase.remainingMs).toBe(2_000);
    const resumed = frame(stillPaused, context, [{ type: "resume" }]);
    const automatic = frame(resumed, context, [], 2_000);
    expect(automatic.phase.kind).toBe("answering");
    if (automatic.phase.kind === "answering") {
      expect(automatic.phase.baseRemainingMs).toBe(10_000);
      expect(automatic.phase.round.points).toBe(200);
      expect(automatic.phase.round.topicId).toBe(state.phase.topicId);
    }
  });
});

describe("answer clock, reserve and atomic frames", () => {
  it("accepts deadline-1 and times out zero reserve exactly at the deadline", () => {
    const context = makeContext();
    let state = startQuestion(createMatch(TWO_TEAMS, "deadline", 0, context), context);
    state = {
      ...state,
      teams: state.teams.map((team) => (team.id === "green" ? { ...team, reserveMs: 0 } : team))
    };
    state = frame(state, context, [{ type: "answer", teamId: "blue", position: "up" }], 9_999);
    expect(state.phase.kind).toBe("answering");
    state = frame(state, context, [{ type: "answer", teamId: "green", position: "up" }], 1);
    expect(state.phase.kind).toBe("reveal");
    if (state.phase.kind === "reveal") {
      expect(state.phase.resolutions.find(({ teamId }) => teamId === "green")?.result).toBe(
        "no-answer"
      );
    }
  });

  it("spends reserve only for open teams and freezes it after the first answer", () => {
    const context = makeContext();
    let state = startQuestion(createMatch(TWO_TEAMS, "reserve", 0, context), context);
    state = frame(state, context, [{ type: "answer", teamId: "green", position: "left" }], 5_000);
    state = frame(state, context, [], 10_000);
    expect(state.teams.find(({ id }) => id === "green")?.reserveMs).toBe(60_000);
    expect(state.teams.find(({ id }) => id === "blue")?.reserveMs).toBe(55_000);
    expect(state.phase.kind).toBe("answering");
  });

  it("freezes both clocks while paused", () => {
    const context = makeContext();
    let state = startQuestion(createMatch(TWO_TEAMS, "pause", 0, context), context);
    state = frame(state, context, [{ type: "pause", reason: { kind: "manual" } }], 4_000);
    expect(state.phase.kind === "answering" && state.phase.baseRemainingMs).toBe(6_000);
    state = frame(state, context, [], 30_000);
    expect(state.phase.kind === "answering" && state.phase.baseRemainingMs).toBe(6_000);
    expect(state.teams.map(({ reserveMs }) => reserveMs)).toEqual([60_000, 60_000]);
    state = frame(state, context, [{ type: "resume" }], 1_000);
    state = frame(state, context, [], 1_000);
    expect(state.phase.kind === "answering" && state.phase.baseRemainingMs).toBe(5_000);
  });

  it("applies every answer in one frame before reveal and keeps the last team answer", () => {
    const context = makeContext();
    let state = startQuestion(createMatch(TWO_TEAMS, "atomic", 0, context), context);
    if (state.phase.kind !== "answering") return;
    const correct = state.phase.round.correctPosition;
    const replacement = correct === "left" ? "right" : "left";
    state = frame(state, context, [
      { type: "answer", teamId: "green", position: correct },
      { type: "answer", teamId: "blue", position: correct },
      { type: "answer", teamId: "green", position: replacement }
    ]);
    expect(state.phase.kind).toBe("reveal");
    if (state.phase.kind === "reveal") {
      expect(state.phase.resolutions.find(({ teamId }) => teamId === "green")).toMatchObject({
        answer: replacement,
        result: "wrong"
      });
      expect(state.phase.resolutions.find(({ teamId }) => teamId === "blue")?.result).toBe(
        "correct"
      );
    }
  });
});

describe("reveal, stages and sudden death", () => {
  it("collects one difficulty rating and waits for the matching acknowledgement", () => {
    const context = makeContext();
    let state = startQuestion(createMatch(TWO_TEAMS, "feedback", 0, context), context);
    state = answerAllCorrect(state, context);
    expect(state.phase.kind).toBe("reveal");
    state = frame(state, context, [{ type: "continue", teamId: "green" }]);
    expect(state.phase.kind).toBe("difficulty-feedback");
    if (state.phase.kind !== "difficulty-feedback") throw new Error("Expected feedback");
    const eventId = state.phase.eventId;
    state = frame(state, context, [
      { type: "rate-difficulty", teamId: "blue", difficulty: "hard" },
      { type: "rate-difficulty", teamId: "green", difficulty: "easy" }
    ]);
    expect(state.phase.kind === "difficulty-feedback" && state.phase.selectedDifficulty).toBe("hard");
    expect(deserializeMatch(serializeMatch(state), context.catalogRevision)?.phase).toEqual(state.phase);
    state = frame(state, context, [{ type: "confirm-difficulty-feedback", eventId: "wrong" }]);
    expect(state.phase.kind).toBe("difficulty-feedback");
    state = frame(state, context, [{ type: "confirm-difficulty-feedback", eventId }]);
    expect(state.phase.kind).toBe("normal-topic");
  });

  it("scores correct, wrong and no-answer exactly once", () => {
    const context = makeContext();
    let state = startQuestion(createMatch(TWO_TEAMS, "score", 0, context), context);
    if (state.phase.kind !== "answering") return;
    const correct = state.phase.round.correctPosition;
    state = {
      ...state,
      teams: state.teams.map((team) => (team.id === "blue" ? { ...team, reserveMs: 0 } : team))
    };
    state = frame(state, context, [{ type: "answer", teamId: "green", position: correct }], 10_000);
    expect(state.phase.kind).toBe("reveal");
    expect(state.teams.find(({ id }) => id === "green")).toMatchObject({ score: 100, correct: 1 });
    expect(state.teams.find(({ id }) => id === "blue")).toMatchObject({
      score: 0,
      incorrect: 1,
      noAnswer: 1
    });
    const repeated = frame(state, context, [], 1_000);
    expect(repeated.teams).toEqual(state.teams);
  });

  it("routes a stage-ending bonus through standings", () => {
    const context = makeContext();
    let state = createMatch(TWO_TEAMS, "stage", 0, context);
    // Use a selected topic to exercise the stage/scoring branch without rebuilding catalog state.
    state = { ...state, mainQuestionIndex: 2 };
    state = startQuestion(state, context);
    state = answerAllCorrect(state, context);
    expect(state.phase.kind === "reveal" && state.phase.round.points).toBe(200);
    state = continueByGreen(state, context);
    expect(state.phase).toEqual({ kind: "standings", completedStage: 1 });
    state = continueByGreen(state, context);
    expect(state.mainQuestionIndex).toBe(3);
    expect(state.phase.kind).toBe("normal-topic");
  });

  it("uses hard no-score questions and picks a single winner without changing scores", () => {
    const context = makeContext();
    let state = createMatch(TWO_TEAMS, "tie", 0, context);
    state = {
      ...state,
      mainQuestionIndex: 8,
      teams: state.teams.map((team) => ({ ...team, score: 500 }))
    };
    state = startQuestion(state, context);
    state = answerAllCorrect(state, context);
    state = continueByGreen(state, context);
    expect(state.phase).toEqual({
      kind: "standings",
      completedStage: 3,
      tieBreakContenders: ["green", "blue"]
    });
    state = continueByGreen(state, context);
    expect(state.phase.kind).toBe("answering");
    if (state.phase.kind !== "answering") return;
    expect(state.phase.round).toMatchObject({ mode: "tie-break", difficulty: "hard", points: 0 });
    const scoreBeforeTie = state.teams.map(({ score }) => score);
    const correct = state.phase.round.correctPosition;
    const wrong = correct === "left" ? "right" : "left";
    state = frame(state, context, [
      { type: "answer", teamId: "green", position: correct },
      { type: "answer", teamId: "blue", position: wrong }
    ]);
    expect(state.phase.kind === "reveal" && state.phase.continuation).toEqual({
      kind: "finished",
      winnerId: "green"
    });
    expect(state.teams.map(({ score }) => score)).toEqual(scoreBeforeTie);
    state = continueByGreen(state, context);
    expect(state.phase).toEqual({ kind: "finished", winnerId: "green" });
  });

  it("narrows several correct contenders and keeps eliminated leaders as spectators", () => {
    const context = makeContext();
    const config: MatchConfig = { ...TWO_TEAMS, teams: ["green", "blue", "yellow"] };
    let state = createMatch(config, "tie-three", 0, context);
    state = {
      ...state,
      mainQuestionIndex: 8,
      teams: state.teams.map((team) => ({ ...team, score: 900 }))
    };
    state = startQuestion(state, context);
    state = answerAllCorrect(state, context);
    state = continueByGreen(state, context);
    expect(state.phase).toEqual({
      kind: "standings",
      completedStage: 3,
      tieBreakContenders: ["green", "blue", "yellow"]
    });
    state = continueByGreen(state, context);
    if (state.phase.kind !== "answering") return;
    const correct = state.phase.round.correctPosition;
    const wrong = correct === "up" ? "down" : "up";
    state = frame(state, context, [
      { type: "answer", teamId: "green", position: correct },
      { type: "answer", teamId: "blue", position: correct },
      { type: "answer", teamId: "yellow", position: wrong }
    ]);
    expect(state.phase.kind === "reveal" && state.phase.continuation).toEqual({
      kind: "tie-break",
      contenders: ["green", "blue"]
    });
    state = continueByGreen(state, context);
    expect(state.tieBreak?.contenders).toEqual(["green", "blue"]);
    expect(
      state.phase.kind === "answering" &&
        state.phase.round.attempts.find(({ teamId }) => teamId === "yellow")?.status
    ).toBe("spectator");
  });
});

describe("public selectors and serialization", () => {
  it("round-trips a topic confirmation and rejects an invalid remaining time", () => {
    const context = makeContext();
    const initial = createMatch(TWO_TEAMS, "confirmation-snapshot", 0, context);
    if (initial.phase.kind !== "normal-topic") throw new Error("Expected topic choice");
    const confirmation = frame(initial, context, [{
      type: "choose-topic",
      teamId: initial.phase.chooser,
      topicId: initial.phase.candidates[0]
    }]);
    expect(deserializeMatch(serializeMatch(confirmation), context.catalogRevision)).toEqual(confirmation);
    const damaged = JSON.parse(serializeMatch(confirmation));
    damaged.phase.remainingMs = 3_001;
    expect(deserializeMatch(JSON.stringify(damaged), context.catalogRevision)).toBeNull();
  });

  it("exposes only answer registration before reveal and full choices after it", () => {
    const context = makeContext();
    let state = startQuestion(createMatch(TWO_TEAMS, "hidden", 0, context), context);
    state = frame(state, context, [{ type: "answer", teamId: "green", position: "left" }]);
    const hidden = selectPublicView(state, context);
    const green = hidden.teams.find(({ id }) => id === "green");
    expect(green?.hasAnswered).toBe(true);
    expect(green).not.toHaveProperty("answerPosition");
    expect(hidden.question).not.toHaveProperty("correctPosition");
    expect(hidden.question).not.toHaveProperty("explanation");
    expect(hidden.question).not.toHaveProperty("source");

    state = frame(state, context, [{ type: "answer", teamId: "blue", position: "right" }]);
    const revealed = selectPublicView(state, context);
    expect(revealed.teams.find(({ id }) => id === "green")?.answerPosition).toBe("left");
    expect(revealed.question).toHaveProperty("correctPosition");
    expect(revealed.question?.explanation).toHaveLength(2);
    expect(revealed.question?.source).toEqual({
      title: "Тестовый источник",
      url: "https://example.com/question"
    });
  });

  it("round-trips JSON and rejects corrupt or incompatible snapshots", () => {
    const context = makeContext();
    const state = startQuestion(createMatch(TWO_TEAMS, "snapshot", 123, context), context);
    const serialized = serializeMatch(state);
    expect(deserializeMatch(serialized, context.catalogRevision)).toEqual(state);
    expect(deserializeMatch(serialized, "other-revision")).toBeNull();
    expect(deserializeMatch("not-json", context.catalogRevision)).toBeNull();
    const missingMatchId = JSON.parse(serialized);
    delete missingMatchId.matchId;
    expect(deserializeMatch(JSON.stringify(missingMatchId), context.catalogRevision)).toBeNull();
  });

  it("uses competition ranking for equal scores", () => {
    const context = makeContext();
    const config: MatchConfig = { ...TWO_TEAMS, teams: ["green", "blue", "yellow", "red"] };
    const state = createMatch(config, "ranking", 0, context);
    const ranked: MatchState = {
      ...state,
      teams: state.teams.map((team, index) => ({ ...team, score: [500, 300, 300, 100][index] }))
    };
    expect(selectStandings(ranked).map(({ rank }) => rank)).toEqual([1, 2, 2, 4]);
  });

  it("gives the tie-break winner sole first place without changing lower ties", () => {
    const context = makeContext();
    const config: MatchConfig = { ...TWO_TEAMS, teams: ["green", "blue", "yellow", "red"] };
    const state = createMatch(config, "finished-ranking", 0, context);
    const finished: MatchState = {
      ...state,
      teams: state.teams.map((team, index) => ({ ...team, score: [500, 500, 500, 100][index] })),
      phase: { kind: "finished", winnerId: "blue" }
    };
    expect(selectStandings(finished).map(({ teamId, rank }) => [teamId, rank])).toEqual([
      ["blue", 1],
      ["green", 2],
      ["yellow", 2],
      ["red", 4]
    ]);
  });
});
