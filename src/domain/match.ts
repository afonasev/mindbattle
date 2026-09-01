import {
  CLASSIC_V1,
  isBonusQuestion,
  pointsFor,
  reserveFor,
  stageFor,
  validateMatchConfig
} from "./classic";
import { nextInt, seedRandom, shuffle } from "./prng";
import {
  ANSWER_POSITIONS,
  type AnswerId,
  type AnsweringPhase,
  type AnswerPosition,
  type BonusVetoPhase,
  type DomainCommand,
  type DomainContext,
  type InputFrame,
  type MatchConfig,
  type MatchPhase,
  type MatchState,
  type PauseReason,
  type QuestionDefinition,
  type RevealContinuation,
  type RoundState,
  type TeamAttempt,
  type TeamId,
  type TeamResolution,
  type TopicId
} from "./types";

function asTriple(values: readonly TopicId[]): readonly [TopicId, TopicId, TopicId] {
  if (values.length !== 3) throw new Error("The normal topic selector must return three topics");
  return [values[0], values[1], values[2]];
}

function validateTopicSelection(
  topics: readonly TopicId[],
  expectedCount: number,
  excluded: readonly TopicId[]
): void {
  if (topics.length !== expectedCount || new Set(topics).size !== expectedCount) {
    throw new Error(`Expected ${expectedCount} unique topic candidates`);
  }
  const blocked = new Set(excluded);
  if (topics.some((topicId) => blocked.has(topicId))) {
    throw new Error("The topic selector returned a topic already selected in this match");
  }
}

function addShownTopics(
  counts: Readonly<Record<TopicId, number>>,
  topics: readonly TopicId[]
): Readonly<Record<TopicId, number>> {
  const next = { ...counts };
  for (const topicId of topics) next[topicId] = (next[topicId] ?? 0) + 1;
  return next;
}

function prepareMainSelection(state: MatchState, context: DomainContext): MatchState {
  const stage = stageFor(state.config, state.mainQuestionIndex);
  const difficulty = CLASSIC_V1.difficulties[stage];
  const bonus = isBonusQuestion(state.config, state.mainQuestionIndex);
  const count = bonus ? state.config.teams.length + 1 : 3;
  const selection = context.selectTopics({
    count,
    difficulty,
    excludedTopicIds: state.selectedTopicIds,
    shownTopicCounts: state.shownTopicCounts,
    random: state.random
  });
  validateTopicSelection(selection.topicIds, count, state.selectedTopicIds);
  const shownTopicCounts = addShownTopics(state.shownTopicCounts, selection.topicIds);

  if (bonus) {
    const cursors = Object.fromEntries(state.config.teams.map((teamId) => [teamId, 0]));
    return {
      ...state,
      random: selection.random,
      shownTopicCounts,
      phase: {
        kind: "bonus-veto",
        candidates: selection.topicIds,
        cursors,
        vetoes: {}
      }
    };
  }

  const chooserIndex =
    (state.firstChooserOffset + state.normalChoiceOrdinal) % state.config.teams.length;
  return {
    ...state,
    random: selection.random,
    shownTopicCounts,
    phase: {
      kind: "normal-topic",
      chooser: state.config.teams[chooserIndex],
      candidates: asTriple(selection.topicIds)
    }
  };
}

function validateQuestion(
  question: QuestionDefinition,
  difficulty: RoundState["difficulty"],
  requestedTopicId: TopicId | null,
  usedQuestionIds: readonly string[],
  recycledAfterExhaustion: boolean
): void {
  if (question.difficulty !== difficulty) throw new Error("Question difficulty mismatch");
  if (requestedTopicId !== null && question.topicId !== requestedTopicId) {
    throw new Error("Question topic mismatch");
  }
  if (usedQuestionIds.includes(question.id) && !recycledAfterExhaustion) {
    throw new Error("Question repeated inside a match");
  }
  const answerIds = question.answers.map(({ id }) => id);
  if (new Set(answerIds).size !== 4 || !answerIds.includes(question.correctAnswerId)) {
    throw new Error("Question must have four unique answers and one valid correct answer");
  }
}

function positionOf(answerOrder: readonly AnswerId[], correctAnswerId: AnswerId): AnswerPosition {
  const index = answerOrder.indexOf(correctAnswerId);
  if (index < 0) throw new Error("Correct answer is absent from the shuffled order");
  return ANSWER_POSITIONS[index];
}

function startQuestion(
  state: MatchState,
  context: DomainContext,
  topicId: TopicId | null,
  mode: "main" | "tie-break"
): MatchState {
  const difficulty =
    mode === "tie-break"
      ? "hard"
      : CLASSIC_V1.difficulties[stageFor(state.config, state.mainQuestionIndex)];
  const selection = context.selectQuestion({
    topicId,
    difficulty,
    excludedQuestionIds: state.usedQuestionIds,
    allowRecycleWhenExhausted: mode === "tie-break",
    random: state.random
  });
  validateQuestion(
    selection.question,
    difficulty,
    topicId,
    state.usedQuestionIds,
    selection.recycledAfterExhaustion === true
  );
  const [answerOrder, random] = shuffle(
    selection.question.answers.map(({ id }) => id),
    selection.random
  );
  const orderedAnswers = answerOrder as readonly [AnswerId, AnswerId, AnswerId, AnswerId];
  const contenders = new Set(state.tieBreak?.contenders ?? []);
  const attempts: readonly TeamAttempt[] = state.config.teams.map((teamId) => ({
    teamId,
    status: mode === "main" || contenders.has(teamId) ? "open" : "spectator",
    answer: null
  }));
  const round: RoundState = {
    mode,
    questionId: selection.question.id,
    topicId: selection.question.topicId,
    difficulty,
    answerOrder: orderedAnswers,
    correctPosition: positionOf(orderedAnswers, selection.question.correctAnswerId),
    points: mode === "main" ? pointsFor(state.config, state.mainQuestionIndex) : 0,
    attempts
  };
  return {
    ...state,
    random,
    usedQuestionIds: [...state.usedQuestionIds, selection.question.id],
    phase: {
      kind: "answering",
      round,
      baseRemainingMs: state.config.answerTimeMs
    }
  };
}

function startTieBreak(
  state: MatchState,
  context: DomainContext,
  contenders: readonly TeamId[]
): MatchState {
  const tieBreak = state.tieBreak
    ? {
        ...state.tieBreak,
        contenders: [...contenders],
        questionNumber: state.tieBreak.questionNumber + 1
      }
    : {
        originalLeaders: [...contenders],
        contenders: [...contenders],
        questionNumber: 1
      };
  return startQuestion({ ...state, tieBreak }, context, null, "tie-break");
}

export function createMatch(
  config: MatchConfig,
  seed: string,
  atMs: number,
  context: DomainContext,
  matchId = `match-v1:${seed}`
): MatchState {
  validateMatchConfig(config);
  if (!Number.isFinite(atMs)) throw new RangeError("atMs must be finite");
  if (!matchId) throw new RangeError("matchId must not be empty");
  const initialRandom = seedRandom(seed);
  const [firstChooserOffset, random] = nextInt(initialRandom, config.teams.length);
  const reserveMs = reserveFor(config.questionCount);
  const initial: MatchState = {
    schemaVersion: 1,
    catalogRevision: context.catalogRevision,
    matchId,
    seed,
    random,
    config: { ...config, teams: [...config.teams] },
    teams: config.teams.map((id) => ({
      id,
      score: 0,
      correct: 0,
      incorrect: 0,
      noAnswer: 0,
      reserveMs
    })),
    mainQuestionIndex: 0,
    firstChooserOffset,
    normalChoiceOrdinal: 0,
    selectedTopicIds: [],
    usedQuestionIds: [],
    shownTopicCounts: {},
    tieBreak: null,
    phase: {
      kind: "normal-topic",
      chooser: config.teams[0],
      candidates: ["", "", ""]
    },
    pause: null,
    lastFrameAtMs: atMs
  };
  return prepareMainSelection(initial, context);
}

function activeTeam(state: MatchState, teamId: TeamId): boolean {
  return state.config.teams.includes(teamId);
}

function withAttempt(
  phase: AnsweringPhase,
  teamId: TeamId,
  update: (attempt: TeamAttempt) => TeamAttempt
): AnsweringPhase {
  return {
    ...phase,
    round: {
      ...phase.round,
      attempts: phase.round.attempts.map((attempt) =>
        attempt.teamId === teamId ? update(attempt) : attempt
      )
    }
  };
}

function allResolved(round: RoundState): boolean {
  return round.attempts.every(
    ({ status }) => status === "answered" || status === "timed-out" || status === "spectator"
  );
}

function winnersByScore(teams: MatchState["teams"]): readonly TeamId[] {
  const topScore = Math.max(...teams.map(({ score }) => score));
  return teams.filter(({ score }) => score === topScore).map(({ id }) => id);
}

function settleRound(state: MatchState): MatchState {
  if (state.phase.kind !== "answering" || !allResolved(state.phase.round)) return state;
  const round = state.phase.round;
  const resolutions: readonly TeamResolution[] = round.attempts.map((attempt) => {
    if (attempt.status === "spectator") {
      return { teamId: attempt.teamId, answer: null, result: "spectator" };
    }
    if (attempt.status === "timed-out" || attempt.answer === null) {
      return { teamId: attempt.teamId, answer: null, result: "no-answer" };
    }
    return {
      teamId: attempt.teamId,
      answer: attempt.answer,
      result: attempt.answer === round.correctPosition ? "correct" : "wrong"
    };
  });

  const teams =
    round.mode === "main"
      ? state.teams.map((team) => {
          const resolution = resolutions.find(({ teamId }) => teamId === team.id);
          if (!resolution || resolution.result === "spectator") return team;
          if (resolution.result === "correct") {
            return { ...team, correct: team.correct + 1, score: team.score + round.points };
          }
          return {
            ...team,
            incorrect: team.incorrect + 1,
            noAnswer: team.noAnswer + (resolution.result === "no-answer" ? 1 : 0)
          };
        })
      : state.teams;

  let continuation: RevealContinuation;
  if (round.mode === "tie-break") {
    const correct = resolutions
      .filter(({ result }) => result === "correct")
      .map(({ teamId }) => teamId);
    const contenders = correct.length === 0 ? state.tieBreak?.contenders ?? [] : correct;
    continuation =
      correct.length === 1
        ? { kind: "finished", winnerId: correct[0] }
        : { kind: "tie-break", contenders };
  } else if (state.mainQuestionIndex === state.config.questionCount - 1) {
    const leaders = winnersByScore(teams);
    continuation =
      leaders.length === 1
        ? { kind: "finished", winnerId: leaders[0] }
        : { kind: "standings", completedStage: 3, tieBreakContenders: leaders };
  } else if (isBonusQuestion(state.config, state.mainQuestionIndex)) {
    continuation = {
      kind: "standings",
      completedStage: (stageFor(state.config, state.mainQuestionIndex) + 1) as 1 | 2
    };
  } else {
    continuation = { kind: "next-main" };
  }

  return {
    ...state,
    teams,
    phase: { kind: "reveal", round, resolutions, continuation }
  };
}

const TOPIC_CONFIRMATION_MS = 3_000;

function advanceClock(state: MatchState, atMs: number, context: DomainContext): MatchState {
  if (state.pause) {
    return { ...state, lastFrameAtMs: atMs };
  }
  const elapsed = atMs - state.lastFrameAtMs;
  if (elapsed <= 0) return { ...state, lastFrameAtMs: atMs };
  if (state.phase.kind === "topic-confirmation") {
    const remainingMs = Math.max(0, state.phase.remainingMs - elapsed);
    const prepared = {
      ...state,
      lastFrameAtMs: atMs,
      phase: { ...state.phase, remainingMs }
    };
    return remainingMs === 0
      ? startQuestion(prepared, context, state.phase.topicId, "main")
      : prepared;
  }
  if (state.phase.kind !== "answering") return { ...state, lastFrameAtMs: atMs };
  const baseSpent = Math.min(state.phase.baseRemainingMs, elapsed);
  const baseRemainingMs = state.phase.baseRemainingMs - baseSpent;
  const reserveElapsed = elapsed - baseSpent;
  let attempts = state.phase.round.attempts;
  let teams = state.teams;

  if (baseRemainingMs === 0) {
    attempts = attempts.map((attempt) => {
      if (attempt.status !== "open") return attempt;
      const team = teams.find(({ id }) => id === attempt.teamId);
      if (!team) return attempt;
      const reserveMs = Math.max(0, team.reserveMs - reserveElapsed);
      teams = teams.map((candidate) =>
        candidate.id === team.id ? { ...candidate, reserveMs } : candidate
      );
      return reserveMs === 0 ? { ...attempt, status: "timed-out" } : attempt;
    });
  }

  return settleRound({
    ...state,
    teams,
    lastFrameAtMs: atMs,
    phase: {
      ...state.phase,
      baseRemainingMs,
      round: { ...state.phase.round, attempts }
    }
  });
}

function addPauseReason(state: MatchState, reason: PauseReason): MatchState {
  const reasons = state.pause?.reasons ?? [];
  const key = JSON.stringify(reason);
  if (reasons.some((candidate) => JSON.stringify(candidate) === key)) return state;
  return { ...state, pause: { reasons: [...reasons, reason] } };
}

function applyNormalTopic(
  state: MatchState,
  command: Extract<DomainCommand, { type: "choose-topic" }>
): MatchState {
  if (
    state.phase.kind !== "normal-topic" ||
    command.teamId !== state.phase.chooser ||
    !state.phase.candidates.includes(command.topicId)
  ) {
    return state;
  }
  const selected = {
    ...state,
    selectedTopicIds: [...state.selectedTopicIds, command.topicId],
    normalChoiceOrdinal: state.normalChoiceOrdinal + 1
  };
  return {
    ...selected,
    phase: { kind: "topic-confirmation", topicId: command.topicId, remainingMs: TOPIC_CONFIRMATION_MS }
  };
}

function applyBonusCommand(
  state: MatchState,
  command: DomainCommand
): MatchState {
  if (state.phase.kind !== "bonus-veto" || !("teamId" in command) || !activeTeam(state, command.teamId)) {
    return state;
  }
  let phase: BonusVetoPhase = state.phase;
  if (command.type === "move-veto") {
    const previous = phase.cursors[command.teamId] ?? 0;
    const cursor = (previous + command.delta + phase.candidates.length) % phase.candidates.length;
    phase = { ...phase, cursors: { ...phase.cursors, [command.teamId]: cursor } };
  } else if (command.type === "clear-veto") {
    const vetoes = { ...phase.vetoes };
    delete vetoes[command.teamId];
    phase = { ...phase, vetoes };
  } else if (command.type === "set-veto") {
    const cursorTopic = phase.candidates[phase.cursors[command.teamId] ?? 0];
    const topicId = command.topicId ?? cursorTopic;
    if (!phase.candidates.includes(topicId)) return state;
    phase = { ...phase, vetoes: { ...phase.vetoes, [command.teamId]: topicId } };
  } else {
    return state;
  }

  const vetoed = state.config.teams.map((teamId) => phase.vetoes[teamId]);
  if (vetoed.every((topicId): topicId is string => topicId !== undefined) && new Set(vetoed).size === state.config.teams.length) {
    const remaining = phase.candidates.filter((topicId) => !vetoed.includes(topicId));
    if (remaining.length !== 1) throw new Error("Distinct bonus vetoes must leave exactly one topic");
    return {
      ...state,
      selectedTopicIds: [...state.selectedTopicIds, remaining[0]],
      phase: {
        kind: "topic-confirmation",
        topicId: remaining[0],
        remainingMs: TOPIC_CONFIRMATION_MS
      }
    };
  }
  return { ...state, phase };
}

function applyAnswer(state: MatchState, teamId: TeamId, position: AnswerPosition): MatchState {
  if (state.phase.kind !== "answering" || !activeTeam(state, teamId)) return state;
  const attempt = state.phase.round.attempts.find((candidate) => candidate.teamId === teamId);
  if (!attempt || (attempt.status !== "open" && attempt.status !== "answered")) return state;
  return {
    ...state,
    phase: withAttempt(state.phase, teamId, (current) => ({
      ...current,
      status: "answered",
      answer: position
    }))
  };
}

function applyContinue(state: MatchState, teamId: TeamId, context: DomainContext): MatchState {
  if (!activeTeam(state, teamId)) return state;
  if (state.phase.kind === "topic-confirmation") {
    return startQuestion(state, context, state.phase.topicId, "main");
  }
  if (state.phase.kind === "standings") {
    if (state.phase.completedStage === 3 && state.phase.tieBreakContenders) {
      return startTieBreak(state, context, state.phase.tieBreakContenders);
    }
    return prepareMainSelection(
      { ...state, mainQuestionIndex: state.mainQuestionIndex + 1 },
      context
    );
  }
  if (state.phase.kind !== "reveal") return state;
  const sequence =
    state.phase.round.mode === "tie-break"
      ? `tie-break-${state.tieBreak?.questionNumber ?? 1}`
      : `main-${state.mainQuestionIndex + 1}`;
  return {
    ...state,
    phase: {
      kind: "difficulty-feedback",
      round: state.phase.round,
      resolutions: state.phase.resolutions,
      continuation: state.phase.continuation,
      eventId: `feedback-v1:${state.matchId}:${sequence}:${state.phase.round.questionId}`,
      selectedDifficulty: null
    }
  };
}

function applyFeedbackSelection(
  state: MatchState,
  teamId: TeamId,
  difficulty: "easy" | "medium" | "hard"
): MatchState {
  if (
    state.phase.kind !== "difficulty-feedback" ||
    state.phase.selectedDifficulty !== null ||
    !activeTeam(state, teamId)
  ) return state;
  return { ...state, phase: { ...state.phase, selectedDifficulty: difficulty } };
}

function applyFeedbackConfirmation(
  state: MatchState,
  eventId: string,
  context: DomainContext
): MatchState {
  if (
    state.phase.kind !== "difficulty-feedback" ||
    state.phase.selectedDifficulty === null ||
    state.phase.eventId !== eventId
  ) return state;
  const continuation = state.phase.continuation;
  if (continuation.kind === "finished") {
    return { ...state, phase: { kind: "finished", winnerId: continuation.winnerId } };
  }
  if (continuation.kind === "tie-break") {
    return startTieBreak(state, context, continuation.contenders);
  }
  if (continuation.kind === "standings") {
    return {
      ...state,
      phase: {
        kind: "standings",
        completedStage: continuation.completedStage,
        ...(continuation.tieBreakContenders
          ? { tieBreakContenders: continuation.tieBreakContenders }
          : {})
      }
    };
  }
  return prepareMainSelection(
    { ...state, mainQuestionIndex: state.mainQuestionIndex + 1 },
    context
  );
}

function processCommands(
  state: MatchState,
  commands: readonly DomainCommand[],
  context: DomainContext
): MatchState {
  let next = state;
  const startedKind = state.phase.kind;
  for (const command of commands) {
    if (command.type === "pause") {
      next = addPauseReason(next, command.reason);
      break;
    }
    if (next.pause) {
      if (command.type === "resume") next = { ...next, pause: null };
      break;
    }
    if (command.type === "resume") continue;

    if (startedKind === "answering" && command.type === "answer") {
      next = applyAnswer(next, command.teamId, command.position);
      continue;
    }
    if (next.phase.kind === "normal-topic" && command.type === "choose-topic") {
      const changed = applyNormalTopic(next, command);
      if (changed !== next) return changed;
    } else if (next.phase.kind === "bonus-veto") {
      const previousKind = next.phase.kind;
      next = applyBonusCommand(next, command);
      if (previousKind !== next.phase.kind) return next;
    } else if (
      (next.phase.kind === "topic-confirmation" ||
        next.phase.kind === "reveal" ||
        next.phase.kind === "standings") &&
      command.type === "continue"
    ) {
      const changed = applyContinue(next, command.teamId, context);
      if (changed !== next) return changed;
    } else if (command.type === "rate-difficulty") {
      const changed = applyFeedbackSelection(next, command.teamId, command.difficulty);
      if (changed !== next) return changed;
    } else if (command.type === "confirm-difficulty-feedback") {
      const changed = applyFeedbackConfirmation(next, command.eventId, context);
      if (changed !== next) return changed;
    }
  }
  return startedKind === "answering" ? settleRound(next) : next;
}

export function reduceFrame(
  state: MatchState,
  frame: InputFrame,
  context: DomainContext
): MatchState {
  if (!Number.isFinite(frame.atMs) || frame.atMs < state.lastFrameAtMs) return state;
  if (!Number.isSafeInteger(frame.sequence) || frame.sequence < 0) return state;
  const wasAnswering = state.phase.kind === "answering";
  const advanced = advanceClock(state, frame.atMs, context);
  if (wasAnswering && advanced.phase.kind === "reveal") return advanced;
  return processCommands(advanced, frame.commands, context);
}
