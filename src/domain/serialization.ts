import { validateMatchConfig } from "./classic";
import type { MatchConfig, MatchState, TeamId } from "./types";

function record(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function finite(value: unknown): value is number {
  return typeof value === "number" && Number.isFinite(value);
}

function validConfig(value: unknown): value is MatchConfig {
  if (!record(value) || !Array.isArray(value.teams)) return false;
  try {
    validateMatchConfig(value as unknown as MatchConfig);
    return true;
  } catch {
    return false;
  }
}

function stringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((item) => typeof item === "string");
}

const positions = ["up", "right", "down", "left"];

function validRound(value: unknown, config: MatchConfig): boolean {
  if (!record(value) || !stringArray(value.answerOrder) || value.answerOrder.length !== 4) {
    return false;
  }
  if (
    (value.mode !== "main" && value.mode !== "tie-break") ||
    typeof value.questionId !== "string" ||
    typeof value.topicId !== "string" ||
    !["easy", "medium", "hard"].includes(String(value.difficulty)) ||
    new Set(value.answerOrder).size !== 4 ||
    !positions.includes(String(value.correctPosition)) ||
    !finite(value.points) ||
    !Array.isArray(value.attempts) ||
    value.attempts.length !== config.teams.length
  ) {
    return false;
  }
  const attemptTeams = new Set<string>();
  for (const attempt of value.attempts) {
    if (
      !record(attempt) ||
      !config.teams.includes(attempt.teamId as TeamId) ||
      !["open", "answered", "timed-out", "spectator"].includes(String(attempt.status)) ||
      (attempt.answer !== null && !positions.includes(String(attempt.answer)))
    ) {
      return false;
    }
    attemptTeams.add(String(attempt.teamId));
  }
  return attemptTeams.size === config.teams.length;
}

function validStandingsFields(value: Record<string, unknown>, config: MatchConfig): boolean {
  if (![1, 2, 3].includes(Number(value.completedStage))) return false;
  if (value.tieBreakContenders === undefined) return value.completedStage !== 3;
  return value.completedStage === 3 &&
    stringArray(value.tieBreakContenders) &&
    value.tieBreakContenders.length >= 2 &&
    value.tieBreakContenders.every((teamId) => config.teams.includes(teamId as TeamId));
}

function validContinuation(value: unknown, config: MatchConfig): boolean {
  if (!record(value) || typeof value.kind !== "string") return false;
  if (value.kind === "next-main") return true;
  if (value.kind === "standings") return validStandingsFields(value, config);
  if (value.kind === "finished") return config.teams.includes(value.winnerId as TeamId);
  return value.kind === "tie-break" &&
    stringArray(value.contenders) &&
    value.contenders.length >= 2 &&
    value.contenders.every((teamId) => config.teams.includes(teamId as TeamId));
}

function validPhase(value: unknown, config: MatchConfig): boolean {
  if (!record(value) || typeof value.kind !== "string") return false;
  if (value.kind === "normal-topic") {
    return config.teams.includes(value.chooser as TeamId) &&
      stringArray(value.candidates) &&
      value.candidates.length === 3 &&
      new Set(value.candidates).size === 3;
  }
  if (value.kind === "topic-confirmation") {
    return typeof value.topicId === "string" &&
      value.topicId.length > 0 &&
      finite(value.remainingMs) &&
      value.remainingMs >= 0 &&
      value.remainingMs <= 3_000;
  }
  if (value.kind === "bonus-veto") {
    if (!(stringArray(value.candidates) &&
      value.candidates.length === config.teams.length + 1 &&
      new Set(value.candidates).size === value.candidates.length &&
      record(value.cursors) &&
      record(value.vetoes))) return false;
    const candidates = value.candidates as string[];
    return Object.entries(value.cursors).every(
      ([teamId, cursor]) =>
        config.teams.includes(teamId as TeamId) &&
        finite(cursor) &&
        Number.isSafeInteger(cursor) &&
        cursor >= 0 &&
        cursor < candidates.length
    ) && Object.entries(value.vetoes).every(
      ([teamId, topicId]) =>
        config.teams.includes(teamId as TeamId) &&
        typeof topicId === "string" &&
        candidates.includes(topicId)
    );
  }
  if (value.kind === "answering") {
    return validRound(value.round, config) && finite(value.baseRemainingMs) && value.baseRemainingMs >= 0;
  }
  if (value.kind === "reveal") {
    if (!(validRound(value.round, config) &&
      Array.isArray(value.resolutions) &&
      value.resolutions.length === config.teams.length &&
      validContinuation(value.continuation, config))) return false;
    const resolvedTeams = new Set<string>();
    for (const resolution of value.resolutions) {
      if (
        !record(resolution) ||
        !config.teams.includes(resolution.teamId as TeamId) ||
        !["correct", "wrong", "no-answer", "spectator"].includes(String(resolution.result)) ||
        (resolution.answer !== null && !positions.includes(String(resolution.answer)))
      ) return false;
      resolvedTeams.add(String(resolution.teamId));
    }
    return resolvedTeams.size === config.teams.length;
  }
  if (value.kind === "standings") return validStandingsFields(value, config);
  return value.kind === "finished" && config.teams.includes(value.winnerId as TeamId);
}

function validPause(value: unknown, config: MatchConfig): boolean {
  if (value === null) return true;
  if (!record(value) || !Array.isArray(value.reasons)) return false;
  return value.reasons.every((reason) => {
    if (!record(reason) || typeof reason.kind !== "string") return false;
    if (["manual", "focus-lost", "restored-snapshot"].includes(reason.kind)) return true;
    return reason.kind === "controller-disconnected" &&
      config.teams.includes(reason.teamId as TeamId);
  });
}

function validTieBreak(value: unknown, config: MatchConfig): boolean {
  if (value === null) return true;
  if (
    !record(value) ||
    !stringArray(value.originalLeaders) ||
    !stringArray(value.contenders) ||
    value.originalLeaders.length < 2 ||
    value.contenders.length < 2 ||
    !value.originalLeaders.every((teamId) => config.teams.includes(teamId as TeamId)) ||
    !value.contenders.every((teamId) => (value.originalLeaders as string[]).includes(teamId)) ||
    !finite(value.questionNumber) ||
    !Number.isSafeInteger(value.questionNumber) ||
    value.questionNumber < 1
  ) {
    return false;
  }
  const originalLeaders = value.originalLeaders as string[];
  const contenders = value.contenders as string[];
  return new Set(originalLeaders).size === originalLeaders.length &&
    new Set(contenders).size === contenders.length;
}

export function serializeMatch(state: MatchState): string {
  return JSON.stringify(state);
}

export function deserializeMatch(
  serialized: string,
  expectedCatalogRevision: string
): MatchState | null {
  let value: unknown;
  try {
    value = JSON.parse(serialized);
  } catch {
    return null;
  }
  if (!record(value) || !validConfig(value.config)) return null;
  const config = value.config;
  if (
    value.schemaVersion !== 1 ||
    value.catalogRevision !== expectedCatalogRevision ||
    typeof value.seed !== "string" ||
    !record(value.random) ||
    !finite(value.random.value) ||
    !Number.isSafeInteger(value.random.value) ||
    value.random.value < 1 ||
    value.random.value > 0xffff_ffff ||
    !Array.isArray(value.teams) ||
    value.teams.length !== config.teams.length ||
    !value.teams.every(
      (team) =>
        record(team) &&
        config.teams.includes(team.id as TeamId) &&
        finite(team.score) && team.score >= 0 &&
        finite(team.correct) && team.correct >= 0 &&
        finite(team.incorrect) && team.incorrect >= 0 &&
        finite(team.noAnswer) && team.noAnswer >= 0 &&
        finite(team.reserveMs) && team.reserveMs >= 0
    ) ||
    new Set(value.teams.map((team) => record(team) ? String(team.id) : "")).size !==
      config.teams.length ||
    !finite(value.mainQuestionIndex) ||
    !Number.isSafeInteger(value.mainQuestionIndex) ||
    value.mainQuestionIndex < 0 ||
    value.mainQuestionIndex >= config.questionCount ||
    !finite(value.firstChooserOffset) ||
    !Number.isSafeInteger(value.firstChooserOffset) ||
    value.firstChooserOffset < 0 ||
    value.firstChooserOffset >= config.teams.length ||
    !finite(value.normalChoiceOrdinal) ||
    !Number.isSafeInteger(value.normalChoiceOrdinal) ||
    value.normalChoiceOrdinal < 0 ||
    !stringArray(value.selectedTopicIds) ||
    new Set(value.selectedTopicIds).size !== value.selectedTopicIds.length ||
    !stringArray(value.usedQuestionIds) ||
    !record(value.shownTopicCounts) ||
    !Object.values(value.shownTopicCounts).every(
      (count) => finite(count) && Number.isSafeInteger(count) && count >= 0
    ) ||
    !validTieBreak(value.tieBreak, config) ||
    !validPhase(value.phase, config) ||
    !validPause(value.pause, config) ||
    !finite(value.lastFrameAtMs)
  ) {
    return null;
  }
  return value as unknown as MatchState;
}
