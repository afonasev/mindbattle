import { describe, expect, it } from "vitest";
import {
  addSoloRecord,
  DEFAULT_PREFERENCES,
  STORAGE_KEY,
  decodePersistedData,
  emptyPersistedData,
  loadPersistedData,
  replaceLastMatch,
  resetQuestionHistory,
  savePersistedData,
  soloLeaderboard,
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

  it("uses the catalog migration callback when a revision changes", () => {
    const data = {
      ...emptyPersistedData("mindbattle-questions-2026-09-01-r2"),
      history: {
        version: 1 as const,
        serial: 9,
        bags: {
          "history-russia:hard": {
            cycle: 1,
            remaining: ["history-russia-rurik-first-prince"],
            previousOrder: ["history-russia-rurik-first-prince"],
            lastShownId: "history-russia-rurik-first-prince",
            shownCount: { "history-russia-rurik-first-prince": 2 },
            lastShownSerial: { "history-russia-rurik-first-prince": 8 }
          }
        }
      },
      lastMatch: {
        status: "in-progress" as const,
        savedAt: "2026-09-01",
        state: { phase: "answering" }
      }
    };
    const migratedHistory = { version: 1 as const, serial: 9, bags: {} };
    const decoded = decodePersistedData(
      JSON.stringify(data),
      "mindbattle-questions-2026-09-02-r3",
      (history) => {
        expect(history.serial).toBe(9);
        return migratedHistory;
      }
    );
    expect(decoded).toMatchObject({
      catalogRevision: "mindbattle-questions-2026-09-02-r3",
      history: migratedHistory,
      lastMatch: null
    });
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

  it("keeps history and snapshots when only the solo table is corrupt", () => {
    const source = {
      ...emptyPersistedData("r1"),
      history: { version: 1 as const, serial: 7, bags: {} },
      lastMatch: { status: "in-progress" as const, savedAt: "2026-09-05", state: { phase: "answering" } },
      soloRecords: [{ id: "broken", name: "Игрок", score: "not-a-number", savedAt: "2026-09-05" }]
    };
    const decoded = decodePersistedData(JSON.stringify(source), "r1");
    expect(decoded.history.serial).toBe(7);
    expect(decoded.lastMatch).toEqual(source.lastMatch);
    expect(decoded.soloRecords).toEqual([]);
  });

  it("sorts local solo records without discarding negative results", () => {
    let data = emptyPersistedData("r1");
    data = addSoloRecord(data, { id: "low", name: "Низ", score: -100, savedAt: "2026-09-05T10:00:00.000Z" });
    data = addSoloRecord(data, { id: "high", name: "Верх", score: 600, savedAt: "2026-09-05T11:00:00.000Z" });
    data = addSoloRecord(data, { id: "middle", name: "Середина", score: 100, savedAt: "2026-09-05T12:00:00.000Z" });
    expect(soloLeaderboard(data.soloRecords).map((record) => record.id)).toEqual(["high", "middle", "low"]);
  });
});
