import { describe, expect, it } from "vitest";
import {
  DEFAULT_PREFERENCES,
  STORAGE_KEY,
  decodePersistedData,
  emptyPersistedData,
  loadPersistedData,
  replaceLastMatch,
  resetQuestionHistory,
  savePersistedData,
  updatePreferences,
  updateControls,
  type StorageLike
} from "../../src/adapters/storage";

class MemoryStorage implements StorageLike {
  value: string | null = null;
  getItem(key: string) {
    expect(key).toBe(STORAGE_KEY);
    return this.value;
  }
  setItem(key: string, value: string) {
    expect(key).toBe(STORAGE_KEY);
    this.value = value;
  }
  removeItem() {
    this.value = null;
  }
}

describe("versioned persistence", () => {
  it("round-trips one last match, history and preferences", () => {
    const storage = new MemoryStorage();
    let data = emptyPersistedData("catalog-r1");
    data = {
      ...data,
      history: { version: 1, serial: 4, bags: {} }
    };
    data = replaceLastMatch(data, {
      status: "in-progress",
      savedAt: "2026-09-01T10:00:00.000Z",
      state: { phase: "answering" }
    });
    data = updatePreferences(data, { ...DEFAULT_PREFERENCES, muted: true });
    data = updateControls(data, [
      { teamId: "green", source: { kind: "keyboard", layout: "wasd" } },
      { teamId: "blue", source: { kind: "keyboard", layout: "arrows" } }
    ]);
    expect(savePersistedData(storage, data)).toBe(true);
    expect(loadPersistedData(storage, "catalog-r1")).toEqual(data);
  });

  it("fails safe on corruption and unsupported versions", () => {
    expect(decodePersistedData("{broken", "r1")).toEqual(emptyPersistedData("r1"));
    expect(decodePersistedData('{"version":2}', "r1")).toEqual(emptyPersistedData("r1"));
    const nested = {
      ...emptyPersistedData("r1"),
      history: {
        version: 1,
        serial: 1,
        bags: { "topic:easy": { cycle: "broken" } }
      }
    };
    expect(decodePersistedData(JSON.stringify(nested), "r1")).toEqual(
      emptyPersistedData("r1")
    );
  });

  it("drops an incompatible snapshot but keeps compact history", () => {
    const data = {
      ...emptyPersistedData("old"),
      history: { version: 1 as const, serial: 7, bags: {} },
      lastMatch: {
        status: "completed" as const,
        savedAt: "2026-09-01",
        state: { winner: "green" }
      }
    };
    const decoded = decodePersistedData(JSON.stringify(data), "new");
    expect(decoded.lastMatch).toBeNull();
    expect(decoded.history.serial).toBe(7);
  });

  it("resets only question history", () => {
    const data = replaceLastMatch(emptyPersistedData("r1"), {
      status: "completed",
      savedAt: "2026-09-01",
      state: { winner: "blue" }
    });
    const reset = resetQuestionHistory({
      ...data,
      history: { version: 1, serial: 99, bags: {} }
    });
    expect(reset.history.serial).toBe(0);
    expect(reset.lastMatch).toEqual(data.lastMatch);
  });
});
