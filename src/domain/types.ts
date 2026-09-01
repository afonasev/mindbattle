import type { RandomState } from "./prng";

export type TeamId = "green" | "blue" | "yellow" | "red";
export type Difficulty = "easy" | "medium" | "hard";
export type AnswerPosition = "up" | "right" | "down" | "left";
export type TopicId = string;
export type QuestionId = string;
export type AnswerId = string;

export const ANSWER_POSITIONS = ["up", "right", "down", "left"] as const satisfies readonly AnswerPosition[];

export interface MatchConfig {
  readonly profile: "classic-v1";
  readonly questionCount: 9 | 15 | 21;
  readonly answerTimeMs: 10_000 | 20_000 | 30_000;
  readonly teams: readonly TeamId[];
}

export interface AnswerDefinition {
  readonly id: AnswerId;
  readonly text: string;
}

export interface QuestionDefinition {
  readonly id: QuestionId;
  readonly topicId: TopicId;
  readonly difficulty: Difficulty;
  readonly prompt: string;
  readonly answers: readonly [AnswerDefinition, AnswerDefinition, AnswerDefinition, AnswerDefinition];
  readonly correctAnswerId: AnswerId;
  readonly explanation: readonly string[];
}

export interface TopicSelectionRequest {
  readonly count: number;
  readonly difficulty: Difficulty;
  readonly excludedTopicIds: readonly TopicId[];
  readonly shownTopicCounts: Readonly<Record<TopicId, number>>;
  readonly random: RandomState;
}

export interface TopicSelection {
  readonly topicIds: readonly TopicId[];
  readonly random: RandomState;
}

export interface QuestionSelectionRequest {
  readonly topicId: TopicId | null;
  readonly difficulty: Difficulty;
  readonly starterOnly?: boolean;
  readonly excludedQuestionIds: readonly QuestionId[];
  readonly allowRecycleWhenExhausted?: boolean;
  readonly random: RandomState;
}

export interface QuestionSelection {
  readonly question: QuestionDefinition;
  readonly random: RandomState;
  readonly recycledAfterExhaustion?: boolean;
}

export interface DomainContext {
  readonly catalogRevision: string;
  selectTopics(request: TopicSelectionRequest): TopicSelection;
  selectQuestion(request: QuestionSelectionRequest): QuestionSelection;
  getQuestion(questionId: QuestionId): QuestionDefinition | undefined;
}

export interface TeamState {
  readonly id: TeamId;
  readonly score: number;
  readonly correct: number;
  readonly incorrect: number;
  readonly noAnswer: number;
  readonly reserveMs: number;
}

export interface TeamAttempt {
  readonly teamId: TeamId;
  readonly status: "open" | "answered" | "timed-out" | "spectator";
  readonly answer: AnswerPosition | null;
}

export interface RoundState {
  readonly mode: "main" | "tie-break";
  readonly questionId: QuestionId;
  readonly topicId: TopicId;
  readonly difficulty: Difficulty;
  readonly answerOrder: readonly [AnswerId, AnswerId, AnswerId, AnswerId];
  readonly correctPosition: AnswerPosition;
  readonly points: number;
  readonly attempts: readonly TeamAttempt[];
}

export interface NormalTopicPhase {
  readonly kind: "normal-topic";
  readonly chooser: TeamId;
  readonly candidates: readonly [TopicId, TopicId, TopicId];
}

export interface TopicConfirmationPhase {
  readonly kind: "topic-confirmation";
  readonly topicId: TopicId;
  readonly remainingMs: number;
}

export interface BonusVetoPhase {
  readonly kind: "bonus-veto";
  readonly candidates: readonly TopicId[];
  readonly cursors: Readonly<Partial<Record<TeamId, number>>>;
  readonly vetoes: Readonly<Partial<Record<TeamId, TopicId>>>;
}

export interface AnsweringPhase {
  readonly kind: "answering";
  readonly round: RoundState;
  readonly baseRemainingMs: number;
}

export interface TeamResolution {
  readonly teamId: TeamId;
  readonly answer: AnswerPosition | null;
  readonly result: "correct" | "wrong" | "no-answer" | "spectator";
}

export type RevealContinuation =
  | { readonly kind: "next-main" }
  | {
      readonly kind: "standings";
      readonly completedStage: 1 | 2 | 3;
      readonly tieBreakContenders?: readonly TeamId[];
    }
  | { readonly kind: "tie-break"; readonly contenders: readonly TeamId[] }
  | { readonly kind: "finished"; readonly winnerId: TeamId };

export interface RevealPhase {
  readonly kind: "reveal";
  readonly round: RoundState;
  readonly resolutions: readonly TeamResolution[];
  readonly continuation: RevealContinuation;
}

export interface StandingsPhase {
  readonly kind: "standings";
  readonly completedStage: 1 | 2 | 3;
  readonly tieBreakContenders?: readonly TeamId[];
}

export interface FinishedPhase {
  readonly kind: "finished";
  readonly winnerId: TeamId;
}

export type MatchPhase =
  | NormalTopicPhase
  | TopicConfirmationPhase
  | BonusVetoPhase
  | AnsweringPhase
  | RevealPhase
  | StandingsPhase
  | FinishedPhase;

export type PauseReason =
  | { readonly kind: "manual" }
  | { readonly kind: "focus-lost" }
  | { readonly kind: "controller-disconnected"; readonly teamId: TeamId }
  | { readonly kind: "restored-snapshot" };

export interface PauseState {
  readonly reasons: readonly PauseReason[];
}

export interface TieBreakState {
  readonly originalLeaders: readonly TeamId[];
  readonly contenders: readonly TeamId[];
  readonly questionNumber: number;
}

export interface MatchState {
  readonly schemaVersion: 1;
  readonly catalogRevision: string;
  readonly seed: string;
  readonly random: RandomState;
  readonly config: MatchConfig;
  readonly teams: readonly TeamState[];
  readonly mainQuestionIndex: number;
  readonly firstChooserOffset: number;
  readonly normalChoiceOrdinal: number;
  readonly selectedTopicIds: readonly TopicId[];
  readonly usedQuestionIds: readonly QuestionId[];
  readonly shownTopicCounts: Readonly<Record<TopicId, number>>;
  readonly tieBreak: TieBreakState | null;
  readonly phase: MatchPhase;
  readonly pause: PauseState | null;
  readonly lastFrameAtMs: number;
}

export type DomainCommand =
  | { readonly type: "choose-topic"; readonly teamId: TeamId; readonly topicId: TopicId }
  | { readonly type: "move-veto"; readonly teamId: TeamId; readonly delta: -1 | 1 }
  | { readonly type: "set-veto"; readonly teamId: TeamId; readonly topicId?: TopicId }
  | { readonly type: "clear-veto"; readonly teamId: TeamId }
  | { readonly type: "answer"; readonly teamId: TeamId; readonly position: AnswerPosition }
  | { readonly type: "continue"; readonly teamId: TeamId }
  | { readonly type: "pause"; readonly reason: PauseReason }
  | { readonly type: "resume" };

export interface InputFrame {
  readonly atMs: number;
  readonly sequence: number;
  readonly commands: readonly DomainCommand[];
}
