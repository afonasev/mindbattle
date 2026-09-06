import {
  addSoloRecord,
  loadSoloRecords,
  loadPersistedData,
  saveSoloRecords,
  savePersistedData,
  soloLeaderboard,
  type PersistedData,
  type SoloRecord,
  type StorageLike
} from "../adapters/storage";
import { EMPTY_QUESTION_HISTORY, migrateQuestionHistory, type ContentCatalog } from "../content";
import { createSoloRun, reduceSoloFrame, type SoloCommand, type SoloConfig, type SoloState } from "../domain/solo";
import { CatalogDomainContext } from "./contentContext";
import type { GameControllerClock, GameSeedSource } from "./gameController";
import type { ComplaintReason } from "../domain/types";
import type { DifficultyFeedbackEvent, DifficultyFeedbackSink, FeedbackSubmissionStatus } from "../feedback";

function validSoloState(value: unknown, revision: string): value is SoloState {
  if (!value || typeof value !== "object") return false;
  const state = value as Partial<SoloState>;
  return state.schemaVersion === 1 && state.catalogRevision === revision && state.config?.profile === "solo-endless-v1" && typeof state.slotIndex === "number" && typeof state.score === "number" && typeof state.lives === "number" && typeof state.reserveMs === "number" && typeof state.lastFrameAtMs === "number" && !!state.phase;
}

export class SoloController {
  private readonly catalog: ContentCatalog;
  private readonly storage: StorageLike;
  private readonly clock: GameControllerClock;
  private readonly seeds: GameSeedSource;
  private persisted: PersistedData;
  private soloRecords: readonly SoloRecord[];
  private context: CatalogDomainContext;
  private currentState: SoloState | null = null;
  private restorableState: SoloState | null = null;
  private readonly feedback?: DifficultyFeedbackSink;
  private feedbackStatus: FeedbackSubmissionStatus = "idle";
  private feedbackError: string | null = null;

  constructor({ catalog, storage, clock, seeds, feedback }: { catalog: ContentCatalog; storage: StorageLike; clock: GameControllerClock; seeds: GameSeedSource; feedback?: DifficultyFeedbackSink }) {
    this.catalog = catalog;
    this.storage = storage;
    this.clock = clock;
    this.seeds = seeds;
    this.feedback = feedback;
    this.persisted = loadPersistedData(storage, catalog.revision, (history) => migrateQuestionHistory(catalog.topics, history));
    this.soloRecords = loadSoloRecords(storage);
    this.context = new CatalogDomainContext(catalog, this.persisted.history);
    this.restorableState = this.persisted.lastSolo && this.persisted.lastSolo.status === "in-progress" && validSoloState(this.persisted.lastSolo.state, catalog.revision) ? this.persisted.lastSolo.state : null;
  }

  get state(): SoloState | null { return this.currentState; }
  get records(): readonly SoloRecord[] { return soloLeaderboard(this.soloRecords); }
  get canRestore(): boolean { return this.restorableState !== null; }
  get difficultyFeedbackStatus(): FeedbackSubmissionStatus { return this.feedbackStatus; }
  get difficultyFeedbackError(): string | null { return this.feedbackError; }

  start(config: SoloConfig = { profile: "solo-endless-v1" }): SoloState {
    this.context = new CatalogDomainContext(this.catalog, this.persisted.history);
    const seed = this.seeds.nextSeed();
    this.currentState = createSoloRun(config, seed, this.clock.now(), this.context);
    this.persistCurrent();
    return this.currentState;
  }

  dispatch(commands: readonly SoloCommand[]): SoloState | null {
    if (!this.currentState) return null;
    const next = reduceSoloFrame(this.currentState, { atMs: this.clock.now(), commands }, this.context);
    if (next !== this.currentState) {
      this.currentState = next;
      this.persistCurrent();
    }
    return this.currentState;
  }

  tick(): SoloState | null { return this.dispatch([]); }

  setFeedbackChoice(hasComplaint: boolean): SoloState | null {
    return this.dispatch([{ type: "set-feedback-choice", hasComplaint }]);
  }

  toggleFeedbackReason(reason: ComplaintReason): SoloState | null {
    return this.dispatch([{ type: "toggle-feedback-reason", reason }]);
  }

  setFeedbackNote(note: string): SoloState | null {
    return this.dispatch([{ type: "set-feedback-note", note }]);
  }

  async submitFeedback(): Promise<boolean> {
    const state = this.currentState;
    if (!state || state.phase.kind !== "feedback" || !this.feedback || this.feedbackStatus === "pending") return false;
    const phase = state.phase;
    if (phase.hasComplaint === null || (phase.hasComplaint && phase.complaintReasons.length === 0 && !phase.complaintNote.trim())) return false;
    const event: DifficultyFeedbackEvent = {
      schemaVersion: 3,
      eventId: phase.eventId,
      matchId: state.runId,
      catalogRevision: state.catalogRevision,
      questionId: phase.round.questionId,
      assignedDifficulty: phase.round.difficulty,
      hasComplaint: phase.hasComplaint,
      complaintReasons: [...phase.complaintReasons],
      ...(phase.complaintNote.trim() ? { complaintNote: phase.complaintNote.trim() } : {})
    };
    this.feedbackStatus = "pending";
    this.feedbackError = null;
    try {
      await this.feedback.submit(event);
      this.feedbackStatus = "idle";
      this.dispatch([{ type: "confirm-feedback", eventId: phase.eventId }]);
      return true;
    } catch (error) {
      this.feedbackStatus = "error";
      this.feedbackError = error instanceof Error ? error.message : "Не удалось сохранить фидбэк";
      return false;
    }
  }

  restore(): SoloState | null {
    if (!this.restorableState) return null;
    this.context = new CatalogDomainContext(this.catalog, this.persisted.history);
    this.currentState = { ...this.restorableState, paused: true, lastFrameAtMs: this.clock.now() };
    this.persistCurrent();
    return this.currentState;
  }

  saveResult(name: string): SoloRecord | null {
    if (!this.currentState || this.currentState.phase.kind !== "finished") return null;
    const normalized = name.trim();
    if (!normalized) return null;
    const record: SoloRecord = {
      id: `${this.currentState.runId}:${this.clock.wallTime()}`,
      name: normalized,
      score: this.currentState.score,
      savedAt: this.clock.wallTime()
    };
    this.soloRecords = addSoloRecord(this.persisted, record).soloRecords;
    saveSoloRecords(this.storage, this.soloRecords);
    return record;
  }

  private persistHistory(): void {
    this.persisted = { ...this.persisted, history: this.context.history };
    savePersistedData(this.storage, this.persisted);
  }

  private persistCurrent(): void {
    if (!this.currentState) return;
    this.persisted = { ...this.persisted, history: this.context.history, lastSolo: { status: this.currentState.phase.kind === "finished" ? "completed" : "in-progress", savedAt: this.clock.wallTime(), state: this.currentState } };
    this.restorableState = this.currentState.phase.kind === "finished" ? null : this.currentState;
    savePersistedData(this.storage, this.persisted);
  }
}
