import {
  loadPersistedData,
  resetQuestionHistory as resetStoredQuestionHistory,
  savePersistedData,
  updatePreferences as replacePreferences,
  updateControls as replaceControls,
  type AccessibilityPreferences,
  type LastMatchSnapshot,
  type PersistedData,
  type StorageLike
} from "../adapters/storage";
import type { TeamControlAssignment } from "../adapters/input";
import { EMPTY_QUESTION_HISTORY, migrateQuestionHistory, type ContentCatalog } from "../content";
import { createMatch, reduceFrame } from "../domain/match";
import { selectPublicView, type PublicMatchView } from "../domain/selectors";
import { deserializeMatch } from "../domain/serialization";
import type {
  DomainCommand,
  InputFrame,
  MatchConfig,
  MatchState,
  PauseReason
} from "../domain/types";
import type {
  DifficultyFeedbackEvent,
  DifficultyFeedbackSink,
  FeedbackSubmissionStatus
} from "../feedback";
import { CatalogDomainContext } from "./contentContext";

export interface GameControllerClock {
  now(): number;
  wallTime(): string;
}

export interface GameSeedSource {
  nextSeed(): string;
}

export interface GameControllerDependencies {
  readonly catalog: ContentCatalog;
  readonly storage: StorageLike;
  readonly clock: GameControllerClock;
  readonly seeds: GameSeedSource;
  readonly feedback?: DifficultyFeedbackSink;
}

export type SavedMatchStatus = "in-progress" | "completed" | null;

function appendRestorePause(state: MatchState, atMs: number): MatchState {
  const reason: PauseReason = { kind: "restored-snapshot" };
  const reasons = state.pause?.reasons ?? [];
  const hasReason = reasons.some((candidate) => candidate.kind === reason.kind);
  return {
    ...state,
    lastFrameAtMs: atMs,
    pause: { reasons: hasReason ? reasons : [...reasons, reason] }
  };
}

function snapshotStatus(state: MatchState): LastMatchSnapshot<MatchState>["status"] {
  return state.phase.kind === "finished" ? "completed" : "in-progress";
}

function validSavedState(
  snapshot: LastMatchSnapshot<unknown> | null,
  catalogRevision: string
): MatchState | null {
  if (!snapshot) return null;
  const state = deserializeMatch(JSON.stringify(snapshot.state), catalogRevision);
  if (!state) return null;
  if (snapshot.status === "completed" && state.phase.kind !== "finished") return null;
  if (snapshot.status === "in-progress" && state.phase.kind === "finished") return null;
  return state;
}

export class GameController {
  private readonly catalog: ContentCatalog;
  private readonly storage: StorageLike;
  private readonly clock: GameControllerClock;
  private readonly seeds: GameSeedSource;
  private readonly feedback?: DifficultyFeedbackSink;
  private context: CatalogDomainContext;
  private persisted: PersistedData<MatchState>;
  private restorableState: MatchState | null;
  private currentState: MatchState | null = null;
  private sequence = 0;
  private saveSucceeded = true;
  private feedbackStatus: FeedbackSubmissionStatus = "idle";
  private feedbackError: string | null = null;

  constructor(dependencies: GameControllerDependencies) {
    this.catalog = dependencies.catalog;
    this.storage = dependencies.storage;
    this.clock = dependencies.clock;
    this.seeds = dependencies.seeds;
    this.feedback = dependencies.feedback;
    this.persisted = loadPersistedData(
      this.storage,
      this.catalog.revision,
      (history) => migrateQuestionHistory(this.catalog.topics, history)
    ) as PersistedData<MatchState>;
    this.context = new CatalogDomainContext(this.catalog, this.persisted.history);
    this.restorableState = validSavedState(this.persisted.lastMatch, this.catalog.revision);
    if (!this.restorableState && this.persisted.lastMatch) {
      this.persisted = { ...this.persisted, lastMatch: null };
      this.saveSucceeded = savePersistedData(this.storage, this.persisted);
    }
  }

  get state(): MatchState | null {
    return this.currentState;
  }

  get view(): PublicMatchView | null {
    return this.currentState ? selectPublicView(this.currentState, this.context) : null;
  }

  get preferences(): AccessibilityPreferences {
    return this.persisted.preferences;
  }

  get questionHistory() {
    return this.persisted.history;
  }

  get controlAssignments(): readonly TeamControlAssignment[] {
    return this.persisted.controls;
  }

  get lastSaveSucceeded(): boolean {
    return this.saveSucceeded;
  }

  get savedMatchStatus(): SavedMatchStatus {
    if (!this.restorableState || !this.persisted.lastMatch) return null;
    return this.persisted.lastMatch.status;
  }

  get difficultyFeedbackStatus(): FeedbackSubmissionStatus {
    return this.feedbackStatus;
  }

  get difficultyFeedbackError(): string | null {
    return this.feedbackError;
  }

  start(config: MatchConfig): MatchState {
    this.context = new CatalogDomainContext(this.catalog, this.persisted.history);
    const seed = this.seeds.nextSeed();
    this.currentState = createMatch(
      config,
      seed,
      this.clock.now(),
      this.context,
      `match-v1:${seed}`
    );
    this.sequence = 0;
    this.restorableState = this.currentState;
    this.persistCurrent();
    return this.currentState;
  }

  restart(): MatchState {
    if (!this.currentState) throw new Error("Cannot restart without a current match");
    return this.start(this.currentState.config);
  }

  restoreLastMatch(): MatchState | null {
    if (!this.restorableState || !this.persisted.lastMatch) return null;
    this.context = new CatalogDomainContext(this.catalog, this.persisted.history);
    this.currentState =
      this.persisted.lastMatch.status === "in-progress"
        ? appendRestorePause(this.restorableState, this.clock.now())
        : this.restorableState;
    this.restorableState = this.currentState;
    this.sequence = 0;
    if (this.persisted.lastMatch.status === "in-progress") this.persistCurrent();
    return this.currentState;
  }

  dispatch(commands: readonly DomainCommand[]): MatchState | null {
    return this.dispatchFrame({
      atMs: this.clock.now(),
      sequence: this.sequence + 1,
      commands
    });
  }

  tick(): MatchState | null {
    return this.dispatch([]);
  }

  dispatchFrame(frame: InputFrame): MatchState | null {
    if (!this.currentState) return null;
    const next = reduceFrame(this.currentState, frame, this.context);
    this.sequence = Math.max(this.sequence, frame.sequence);
    if (next !== this.currentState) {
      this.currentState = next;
      this.restorableState = next;
      this.persistCurrent();
    }
    return this.currentState;
  }

  async handleFeedbackDirection(
    teamId: MatchState["config"]["teams"][number],
    direction: "north" | "east" | "south" | "west"
  ): Promise<boolean> {
    if (!this.currentState || !this.feedback || this.feedbackStatus === "pending") return false;
    this.dispatch([{ type: "feedback-direction", teamId, direction }]);
    return this.submitCompletedFeedback();
  }

  async handleFeedbackConfirmation(
    teamId: MatchState["config"]["teams"][number]
  ): Promise<boolean> {
    if (!this.currentState || !this.feedback || this.feedbackStatus === "pending") return false;
    this.dispatch([{ type: "feedback-confirm", teamId }]);
    return this.submitCompletedFeedback();
  }

  private async submitCompletedFeedback(): Promise<boolean> {
    if (
      !this.currentState ||
      this.currentState.phase.kind !== "difficulty-feedback" ||
      !Object.values(this.currentState.phase.responses).every((response) => response.completed)
    ) return false;

    const feedback = this.feedback;
    if (!feedback) return false;
    const phase = this.currentState.phase;
    const event: DifficultyFeedbackEvent = {
      schemaVersion: 2,
      eventId: phase.eventId,
      matchId: this.currentState.matchId,
      catalogRevision: this.currentState.catalogRevision,
      questionId: phase.round.questionId,
      assignedDifficulty: phase.round.difficulty,
      responses: Object.values(phase.responses).map((response) => ({
        perceivedDifficulty: response.perceivedDifficulty!,
        similarityPreference: response.similarityPreference!,
        diagnosticFlags: [...response.diagnosticFlags]
      })).sort((left, right) => JSON.stringify(left).localeCompare(JSON.stringify(right)))
    };
    this.feedbackStatus = "pending";
    this.feedbackError = null;
    try {
      await feedback.submit(event);
      this.feedbackStatus = "idle";
      this.dispatch([{ type: "confirm-difficulty-feedback", eventId: phase.eventId }]);
      return true;
    } catch (error) {
      this.feedbackStatus = "error";
      this.feedbackError = error instanceof Error ? error.message : "Не удалось сохранить фидбэк";
      return false;
    }
  }

  /** Compatibility path for a v1 snapshot and legacy local callers. */
  async rateDifficulty(teamId: MatchState["config"]["teams"][number], perceivedDifficulty: "easy" | "medium" | "hard"): Promise<boolean> {
    if (!this.currentState || !this.feedback || this.feedbackStatus === "pending") return false;
    this.dispatch([{ type: "rate-difficulty", teamId, difficulty: perceivedDifficulty }]);
    if (!this.currentState || this.currentState.phase.kind !== "difficulty-feedback" || !this.currentState.phase.selectedDifficulty) return false;
    const phase = this.currentState.phase;
    const selectedDifficulty = phase.selectedDifficulty;
    if (!selectedDifficulty) return false;
    const event: DifficultyFeedbackEvent = { schemaVersion: 1, eventId: phase.eventId, matchId: this.currentState.matchId, catalogRevision: this.currentState.catalogRevision, questionId: phase.round.questionId, assignedDifficulty: phase.round.difficulty, perceivedDifficulty: selectedDifficulty };
    this.feedbackStatus = "pending"; this.feedbackError = null;
    try { await this.feedback.submit(event); this.feedbackStatus = "idle"; this.dispatch([{ type: "confirm-difficulty-feedback", eventId: phase.eventId }]); return true; }
    catch (error) { this.feedbackStatus = "error"; this.feedbackError = error instanceof Error ? error.message : "Не удалось сохранить фидбэк"; return false; }
  }

  resetQuestionHistory(): void {
    this.persisted = resetStoredQuestionHistory(this.persisted);
    this.context = new CatalogDomainContext(this.catalog, EMPTY_QUESTION_HISTORY);
    this.saveSucceeded = savePersistedData(this.storage, this.persisted);
  }

  updatePreferences(patch: Partial<AccessibilityPreferences>): AccessibilityPreferences {
    const preferences = { ...this.persisted.preferences, ...patch };
    if (!Number.isFinite(preferences.volume) || preferences.volume < 0 || preferences.volume > 1) {
      throw new RangeError("Volume must be between 0 and 1");
    }
    this.persisted = replacePreferences(this.persisted, preferences);
    this.saveSucceeded = savePersistedData(this.storage, this.persisted);
    return preferences;
  }

  updateControlAssignments(assignments: readonly TeamControlAssignment[]): void {
    this.persisted = replaceControls(this.persisted, assignments);
    this.saveSucceeded = savePersistedData(this.storage, this.persisted);
  }

  private persistCurrent(): void {
    if (!this.currentState) return;
    const lastMatch: LastMatchSnapshot<MatchState> = {
      status: snapshotStatus(this.currentState),
      savedAt: this.clock.wallTime(),
      state: this.currentState
    };
    this.persisted = {
      ...this.persisted,
      history: this.context.history,
      lastMatch
    };
    this.restorableState = this.currentState;
    this.saveSucceeded = savePersistedData(this.storage, this.persisted);
  }
}
