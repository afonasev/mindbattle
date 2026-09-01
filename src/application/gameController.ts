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
import { EMPTY_QUESTION_HISTORY, type ContentCatalog } from "../content";
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
  private context: CatalogDomainContext;
  private persisted: PersistedData<MatchState>;
  private restorableState: MatchState | null;
  private currentState: MatchState | null = null;
  private sequence = 0;
  private saveSucceeded = true;

  constructor(dependencies: GameControllerDependencies) {
    this.catalog = dependencies.catalog;
    this.storage = dependencies.storage;
    this.clock = dependencies.clock;
    this.seeds = dependencies.seeds;
    this.persisted = loadPersistedData(
      this.storage,
      this.catalog.revision
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

  start(config: MatchConfig): MatchState {
    this.context = new CatalogDomainContext(this.catalog, this.persisted.history);
    this.currentState = createMatch(
      config,
      this.seeds.nextSeed(),
      this.clock.now(),
      this.context
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
