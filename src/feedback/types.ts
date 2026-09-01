import type { Difficulty } from "../domain/types";

export interface DifficultyFeedbackEvent {
  readonly schemaVersion: 1;
  readonly eventId: string;
  readonly matchId: string;
  readonly catalogRevision: string;
  readonly questionId: string;
  readonly assignedDifficulty: Difficulty;
  readonly perceivedDifficulty: Difficulty;
}

export interface StoredDifficultyFeedbackEvent extends DifficultyFeedbackEvent {
  readonly recordedAt: string;
}

export interface DifficultyFeedbackSink {
  submit(event: DifficultyFeedbackEvent): Promise<void>;
}

export type FeedbackSubmissionStatus = "idle" | "pending" | "error";
