import type { Difficulty, MatchConfig, TeamId } from "./types";

export const TEAM_IDS = ["green", "blue", "yellow", "red"] as const satisfies readonly TeamId[];
export const QUESTION_COUNTS = [9, 15, 21] as const;
export const ANSWER_TIMES_MS = [10_000, 20_000, 30_000] as const;

export const CLASSIC_V1 = Object.freeze({
  id: "classic-v1" as const,
  stages: 3 as const,
  difficulties: ["easy", "medium", "hard"] as const satisfies readonly Difficulty[],
  basePoints: [100, 200, 300] as const,
  bonusMultiplier: 2 as const,
  reserveByQuestionCount: Object.freeze({
    9: 60_000,
    15: 90_000,
    21: 120_000
  })
});

export class InvalidMatchConfigError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "InvalidMatchConfigError";
  }
}

export function validateMatchConfig(config: MatchConfig): MatchConfig {
  if (config.profile !== CLASSIC_V1.id) {
    throw new InvalidMatchConfigError(`Unknown profile: ${config.profile}`);
  }
  if (!(QUESTION_COUNTS as readonly number[]).includes(config.questionCount)) {
    throw new InvalidMatchConfigError(`Unsupported question count: ${config.questionCount}`);
  }
  if (!(ANSWER_TIMES_MS as readonly number[]).includes(config.answerTimeMs)) {
    throw new InvalidMatchConfigError(`Unsupported answer time: ${config.answerTimeMs}`);
  }
  if (config.teams.length < 2 || config.teams.length > 4) {
    throw new InvalidMatchConfigError("A match requires two to four teams");
  }
  if (new Set(config.teams).size !== config.teams.length) {
    throw new InvalidMatchConfigError("Team identifiers must be unique");
  }
  if (config.teams.some((teamId) => !(TEAM_IDS as readonly string[]).includes(teamId))) {
    throw new InvalidMatchConfigError("Unknown team identifier");
  }
  return config;
}

export function reserveFor(questionCount: MatchConfig["questionCount"]): number {
  return CLASSIC_V1.reserveByQuestionCount[questionCount];
}

export function stageSize(config: MatchConfig): number {
  return config.questionCount / CLASSIC_V1.stages;
}

export function stageFor(config: MatchConfig, questionIndex: number): 0 | 1 | 2 {
  return Math.floor(questionIndex / stageSize(config)) as 0 | 1 | 2;
}

export function isBonusQuestion(config: MatchConfig, questionIndex: number): boolean {
  return questionIndex % stageSize(config) === stageSize(config) - 1;
}

export function pointsFor(config: MatchConfig, questionIndex: number): number {
  const stage = stageFor(config, questionIndex);
  return CLASSIC_V1.basePoints[stage] * (isBonusQuestion(config, questionIndex) ? 2 : 1);
}
