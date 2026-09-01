import { EMPTY_QUESTION_HISTORY, type QuestionHistory } from "../content";
import type { TeamControlAssignment } from "./input";

export const STORAGE_KEY = "mindbattle:data:v1";

export interface AccessibilityPreferences {
  readonly volume: number;
  readonly muted: boolean;
  readonly textSize: "normal" | "large";
  readonly highContrast: boolean;
  readonly reducedMotion: boolean;
}

export const DEFAULT_PREFERENCES: AccessibilityPreferences = {
  volume: 0.7,
  muted: false,
  textSize: "normal",
  highContrast: false,
  reducedMotion: false
};

export interface LastMatchSnapshot<TState = unknown> {
  readonly status: "in-progress" | "completed";
  readonly savedAt: string;
  readonly state: TState;
}

export interface PersistedData<TState = unknown> {
  readonly version: 1;
  readonly catalogRevision: string;
  readonly history: QuestionHistory;
  readonly lastMatch: LastMatchSnapshot<TState> | null;
  readonly preferences: AccessibilityPreferences;
  readonly controls: readonly TeamControlAssignment[];
}

export interface StorageLike {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
  removeItem(key: string): void;
}

export function emptyPersistedData(catalogRevision: string): PersistedData {
  return {
    version: 1,
    catalogRevision,
    history: EMPTY_QUESTION_HISTORY,
    lastMatch: null,
    preferences: DEFAULT_PREFERENCES,
    controls: []
  };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function decodePreferences(value: unknown): AccessibilityPreferences | null {
  if (!isRecord(value)) return null;
  if (
    typeof value.volume !== "number" ||
    value.volume < 0 ||
    value.volume > 1 ||
    typeof value.muted !== "boolean" ||
    (value.textSize !== "normal" && value.textSize !== "large") ||
    typeof value.highContrast !== "boolean" ||
    typeof value.reducedMotion !== "boolean"
  ) {
    return null;
  }
  return {
    volume: value.volume,
    muted: value.muted,
    textSize: value.textSize,
    highContrast: value.highContrast,
    reducedMotion: value.reducedMotion
  };
}

function decodeHistory(value: unknown): QuestionHistory | null {
  if (
    !isRecord(value) ||
    value.version !== 1 ||
    typeof value.serial !== "number" ||
    !Number.isSafeInteger(value.serial) ||
    value.serial < 0 ||
    !isRecord(value.bags)
  ) {
    return null;
  }
  for (const bag of Object.values(value.bags)) {
    if (
      !isRecord(bag) ||
      typeof bag.cycle !== "number" ||
      !Number.isSafeInteger(bag.cycle) ||
      bag.cycle < 0 ||
      !Array.isArray(bag.remaining) ||
      !bag.remaining.every((id) => typeof id === "string") ||
      !Array.isArray(bag.previousOrder) ||
      !bag.previousOrder.every((id) => typeof id === "string") ||
      (bag.lastShownId !== null && typeof bag.lastShownId !== "string") ||
      !isRecord(bag.shownCount) ||
      !Object.values(bag.shownCount).every(
        (count) => typeof count === "number" && Number.isSafeInteger(count) && count >= 0
      ) ||
      !isRecord(bag.lastShownSerial) ||
      !Object.values(bag.lastShownSerial).every(
        (serial) => typeof serial === "number" && Number.isSafeInteger(serial) && serial >= 0
      )
    ) {
      return null;
    }
  }
  return value as unknown as QuestionHistory;
}

function decodeLastMatch(value: unknown): LastMatchSnapshot | null | undefined {
  if (value === null) return null;
  if (
    !isRecord(value) ||
    (value.status !== "in-progress" && value.status !== "completed") ||
    typeof value.savedAt !== "string" ||
    !("state" in value)
  ) {
    return undefined;
  }
  return value as unknown as LastMatchSnapshot;
}

function decodeControls(value: unknown): readonly TeamControlAssignment[] | null {
  if (!Array.isArray(value)) return null;
  const result: TeamControlAssignment[] = [];
  for (const item of value) {
    if (!isRecord(item) || typeof item.teamId !== "string" || !isRecord(item.source)) {
      return null;
    }
    const source = item.source;
    if (source.kind === "keyboard") {
      if (source.layout !== "wasd" && source.layout !== "arrows") return null;
      result.push({ teamId: item.teamId, source: { kind: "keyboard", layout: source.layout } });
      continue;
    }
    if (
      source.kind !== "gamepad" ||
      typeof source.index !== "number" ||
      !Number.isSafeInteger(source.index) ||
      source.index < 0 ||
      typeof source.id !== "string" ||
      !["xbox", "playstation", "nintendo", "universal"].includes(String(source.profile))
    ) {
      return null;
    }
    result.push({
      teamId: item.teamId,
      source: {
        kind: "gamepad",
        index: source.index,
        id: source.id,
        profile: source.profile as "xbox" | "playstation" | "nintendo" | "universal"
      }
    });
  }
  const teamIds = result.map(({ teamId }) => teamId);
  const sourceKeys = result.map(({ source }) =>
    source.kind === "keyboard" ? `keyboard:${source.layout}` : `gamepad:${source.index}`
  );
  return new Set(teamIds).size === teamIds.length && new Set(sourceKeys).size === sourceKeys.length
    ? result
    : null;
}

export function decodePersistedData(
  source: string | null,
  catalogRevision: string
): PersistedData {
  if (!source) return emptyPersistedData(catalogRevision);
  try {
    const parsed: unknown = JSON.parse(source);
    if (!isRecord(parsed) || parsed.version !== 1) return emptyPersistedData(catalogRevision);
    const history = decodeHistory(parsed.history);
    const preferences = decodePreferences(parsed.preferences);
    const lastMatch = decodeLastMatch(parsed.lastMatch);
    const controls = decodeControls(parsed.controls ?? []);
    if (
      !history ||
      !preferences ||
      lastMatch === undefined ||
      !controls ||
      typeof parsed.catalogRevision !== "string"
    ) {
      return emptyPersistedData(catalogRevision);
    }
    return {
      version: 1,
      catalogRevision,
      history,
      lastMatch: parsed.catalogRevision === catalogRevision ? lastMatch : null,
      preferences,
      controls
    };
  } catch {
    return emptyPersistedData(catalogRevision);
  }
}

export function loadPersistedData(
  storage: StorageLike,
  catalogRevision: string
): PersistedData {
  return decodePersistedData(storage.getItem(STORAGE_KEY), catalogRevision);
}

export function savePersistedData(storage: StorageLike, data: PersistedData): boolean {
  try {
    storage.setItem(STORAGE_KEY, JSON.stringify(data));
    return true;
  } catch {
    return false;
  }
}

export function resetQuestionHistory<TState>(
  data: PersistedData<TState>
): PersistedData<TState> {
  return { ...data, history: EMPTY_QUESTION_HISTORY };
}

export function replaceLastMatch<TState>(
  data: PersistedData<TState>,
  lastMatch: LastMatchSnapshot<TState> | null
): PersistedData<TState> {
  return { ...data, lastMatch };
}

export function updatePreferences<TState>(
  data: PersistedData<TState>,
  preferences: AccessibilityPreferences
): PersistedData<TState> {
  return { ...data, preferences };
}

export function updateControls<TState>(
  data: PersistedData<TState>,
  controls: readonly TeamControlAssignment[]
): PersistedData<TState> {
  return { ...data, controls: [...controls] };
}
