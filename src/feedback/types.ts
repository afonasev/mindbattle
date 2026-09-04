import type { ComplaintReason, DiagnosticFlag, Difficulty, PerceivedDifficulty, SimilarityPreference } from "../domain/types";

export interface DifficultyFeedbackEventV1 {
  readonly schemaVersion: 1;
  readonly eventId: string;
  readonly matchId: string;
  readonly catalogRevision: string;
  readonly questionId: string;
  readonly assignedDifficulty: Difficulty;
  readonly perceivedDifficulty: Difficulty;
}

export interface AnonymousFeedbackResponse {
  readonly perceivedDifficulty: PerceivedDifficulty;
  readonly similarityPreference: SimilarityPreference;
  readonly diagnosticFlags: readonly DiagnosticFlag[];
}

export interface DifficultyFeedbackEventV2 {
  readonly schemaVersion: 2;
  readonly eventId: string;
  readonly matchId: string;
  readonly catalogRevision: string;
  readonly questionId: string;
  readonly assignedDifficulty: Difficulty;
  readonly responses: readonly AnonymousFeedbackResponse[];
}

export interface DifficultyFeedbackEventV3 {
  readonly schemaVersion: 3;
  readonly eventId: string;
  readonly matchId: string;
  readonly catalogRevision: string;
  readonly questionId: string;
  readonly assignedDifficulty: Difficulty;
  readonly hasComplaint: boolean;
  readonly complaintReasons: readonly ComplaintReason[];
  readonly complaintNote?: string;
}

export type DifficultyFeedbackEvent = DifficultyFeedbackEventV1 | DifficultyFeedbackEventV2 | DifficultyFeedbackEventV3;

export type StoredDifficultyFeedbackEvent = DifficultyFeedbackEvent & {
  readonly recordedAt: string;
};

export interface DifficultyFeedbackSink {
  submit(event: DifficultyFeedbackEvent): Promise<void>;
}

export type FeedbackSubmissionStatus = "idle" | "pending" | "error";
