import { describe, expect, it } from "vitest";
import {
  STORAGE_KEY,
  emptyPersistedData,
  loadPersistedData,
  savePersistedData,
  type StorageLike
} from "../../src/adapters/storage";
import {
  GameController,
  type GameControllerClock,
  type GameSeedSource
} from "../../src/application/gameController";
import { createMatch } from "../../src/domain/match";
import { CatalogDomainContext } from "../../src/application/contentContext";
import type { ContentCatalog, TopicPack } from "../../src/content/types";
import { EMPTY_QUESTION_HISTORY, seedRandom } from "../../src/content";
import type { MatchConfig, MatchState } from "../../src/domain/types";

class MemoryStorage implements StorageLike {
  value: string | null = null;
  writes = 0;

  getItem(key: string): string | null {
    expect(key).toBe(STORAGE_KEY);
    return this.value;
  }

  setItem(key: string, value: string): void {
    expect(key).toBe(STORAGE_KEY);
    this.value = value;
    this.writes += 1;
  }

  removeItem(): void {
    this.value = null;
  }
}

class FakeClock implements GameControllerClock {
  value = 1_000;

  now(): number {
    return this.value;
  }

  wallTime(): string {
    return new Date(1_700_000_000_000 + this.value).toISOString();
  }

  advance(milliseconds: number): void {
    this.value += milliseconds;
  }
}

class FakeSeeds implements GameSeedSource {
  private index = 0;

  constructor(private readonly values: readonly string[]) {}

  nextSeed(): string {
    const value = this.values[this.index];
    if (!value) throw new Error("No fixture seed available");
    this.index += 1;
    return value;
  }
}

const CONFIG: MatchConfig = {
  profile: "classic-v1",
  questionCount: 9,
  answerTimeMs: 10_000,
  teams: ["green", "blue"]
};

function makeTopic(index: number): TopicPack {
  const id = `topic-${index}`;
  return {
    id,
    title: `Тема ${index}`,
    questions: (["easy", "medium", "hard"] as const).flatMap((difficulty) =>
      Array.from({ length: 10 }, (_, questionIndex) => ({
        id: `${id}-${difficulty}-${questionIndex}`,
        difficulty,
        prompt: `Вопрос ${questionIndex}`,
        answers: ["Верный", "Второй", "Третий", "Четвёртый"] as const,
        correctIndex: 0 as const,
        explanation: "Верный ответ подтверждён источником. Это краткая справка для игроков.",
        source: {
          title: "Источник",
          url: "https://example.com/reference",
          verifiedAt: "2026-09-01"
        }
      }))
    )
  };
}

function makeCatalog(): ContentCatalog {
  return {
    revision: "controller-fixture-r1",
    topics: Array.from({ length: 30 }, (_, index) => makeTopic(index))
  };
}

function makeController(
  storage: MemoryStorage,
  clock = new FakeClock(),
  seeds = new FakeSeeds(["seed-a", "seed-b"])
): GameController {
  return new GameController({ catalog: makeCatalog(), storage, clock, seeds });
}

function chooseFirstTopic(controller: GameController): MatchState {
  const state = controller.state;
  if (!state || state.phase.kind !== "normal-topic") throw new Error("Expected topic choice");
  const next = controller.dispatch([
    {
      type: "choose-topic",
      teamId: state.phase.chooser,
      topicId: state.phase.candidates[0]
    }
  ]);
  if (!next) throw new Error("Expected active match");
  if (next.phase.kind !== "topic-confirmation") throw new Error("Expected topic confirmation");
  const answering = controller.dispatch([{ type: "continue", teamId: "green" }]);
  if (!answering) throw new Error("Expected active match");
  return answering;
}

describe("GameController", () => {
  it("persists the chosen topic before the question is created", () => {
    const storage = new MemoryStorage();
    const controller = makeController(storage);
    const initial = controller.start(CONFIG);
    if (initial.phase.kind !== "normal-topic") throw new Error("Expected topic choice");
    const confirmation = controller.dispatch([{
      type: "choose-topic",
      teamId: initial.phase.chooser,
      topicId: initial.phase.candidates[0]
    }]);
    expect(confirmation?.phase.kind).toBe("topic-confirmation");
    expect(controller.questionHistory.serial).toBe(0);
    expect((loadPersistedData(storage, makeCatalog().revision).lastMatch?.state as MatchState).phase.kind).toBe(
      "topic-confirmation"
    );
  });
  it("starts and restarts with injected clock and fresh seeds while replacing one snapshot", () => {
    const storage = new MemoryStorage();
    const clock = new FakeClock();
    const controller = makeController(storage, clock);
    const first = controller.start(CONFIG);
    expect(first.seed).toBe("seed-a");
    expect(first.lastFrameAtMs).toBe(1_000);
    let persisted = loadPersistedData(storage, makeCatalog().revision);
    expect(persisted.lastMatch?.status).toBe("in-progress");
    expect((persisted.lastMatch?.state as MatchState).seed).toBe("seed-a");

    clock.advance(500);
    const restarted = controller.restart();
    expect(restarted.seed).toBe("seed-b");
    expect(restarted.lastFrameAtMs).toBe(1_500);
    persisted = loadPersistedData(storage, makeCatalog().revision);
    expect((persisted.lastMatch?.state as MatchState).seed).toBe("seed-b");
    expect(controller.questionHistory.serial).toBe(0);
  });

  it("persists controller assignments needed to resume the last match", () => {
    const storage = new MemoryStorage();
    const controller = makeController(storage);
    const assignments = [
      { teamId: "green", source: { kind: "keyboard" as const, layout: "wasd" as const } },
      { teamId: "blue", source: { kind: "keyboard" as const, layout: "arrows" as const } }
    ];
    controller.updateControlAssignments(assignments);
    controller.start(CONFIG);

    const restored = makeController(storage, new FakeClock(), new FakeSeeds(["unused"]));
    expect(restored.controlAssignments).toEqual(assignments);
  });

  it("dispatches a frame and saves question history together with the snapshot", () => {
    const storage = new MemoryStorage();
    const controller = makeController(storage);
    controller.start(CONFIG);
    const writesBefore = storage.writes;
    const answering = chooseFirstTopic(controller);
    expect(answering.phase.kind).toBe("answering");
    expect(controller.questionHistory.serial).toBe(1);
    const persisted = loadPersistedData(storage, makeCatalog().revision);
    expect(persisted.history.serial).toBe(1);
    expect((persisted.lastMatch?.state as MatchState).phase.kind).toBe("answering");
    expect(storage.writes).toBe(writesBefore + 2);
  });

  it("restores an in-progress match paused at a fresh monotonic anchor", () => {
    const storage = new MemoryStorage();
    const firstClock = new FakeClock();
    const first = makeController(storage, firstClock);
    first.start(CONFIG);
    chooseFirstTopic(first);

    const restoreClock = new FakeClock();
    restoreClock.value = 80_000;
    const restoredController = makeController(
      storage,
      restoreClock,
      new FakeSeeds(["unused"])
    );
    expect(restoredController.savedMatchStatus).toBe("in-progress");
    const restored = restoredController.restoreLastMatch();
    expect(restored?.pause?.reasons).toContainEqual({ kind: "restored-snapshot" });
    expect(restored?.lastFrameAtMs).toBe(80_000);
    expect(restored?.phase.kind === "answering" && restored.phase.baseRemainingMs).toBe(10_000);

    restoreClock.advance(20_000);
    restoredController.tick();
    expect(
      restoredController.state?.phase.kind === "answering" &&
        restoredController.state.phase.baseRemainingMs
    ).toBe(10_000);
    restoredController.dispatch([{ type: "resume" }]);
    restoreClock.advance(1_000);
    restoredController.tick();
    expect(
      restoredController.state?.phase.kind === "answering" &&
        restoredController.state.phase.baseRemainingMs
    ).toBe(9_000);
  });

  it("restores topic confirmation paused with its remaining countdown", () => {
    const storage = new MemoryStorage();
    const firstClock = new FakeClock();
    const first = makeController(storage, firstClock);
    const initial = first.start(CONFIG);
    if (initial.phase.kind !== "normal-topic") throw new Error("Expected topic choice");
    first.dispatch([{
      type: "choose-topic",
      teamId: initial.phase.chooser,
      topicId: initial.phase.candidates[0]
    }]);
    firstClock.advance(1_000);
    first.tick();
    expect(first.state?.phase.kind === "topic-confirmation" && first.state.phase.remainingMs).toBe(2_000);

    const restoreClock = new FakeClock();
    restoreClock.value = 80_000;
    const restoredController = makeController(storage, restoreClock, new FakeSeeds(["unused"]));
    const restored = restoredController.restoreLastMatch();
    expect(restored?.phase.kind === "topic-confirmation" && restored.phase.remainingMs).toBe(2_000);
    expect(restored?.pause?.reasons).toContainEqual({ kind: "restored-snapshot" });
    restoreClock.advance(20_000);
    restoredController.tick();
    expect(
      restoredController.state?.phase.kind === "topic-confirmation" &&
        restoredController.state.phase.remainingMs
    ).toBe(2_000);
    restoredController.dispatch([{ type: "resume" }]);
    restoreClock.advance(2_000);
    restoredController.tick();
    expect(restoredController.state?.phase.kind).toBe("answering");
  });

  it("restores a completed result without adding a pause", () => {
    const storage = new MemoryStorage();
    const catalog = makeCatalog();
    const clock = new FakeClock();
    const context = new CatalogDomainContext(catalog, emptyPersistedData(catalog.revision).history);
    const active = createMatch(CONFIG, "finished-seed", clock.now(), context);
    const finished: MatchState = {
      ...active,
      phase: { kind: "finished", winnerId: "blue" }
    };
    const data = {
      ...emptyPersistedData(catalog.revision),
      lastMatch: {
        status: "completed" as const,
        savedAt: clock.wallTime(),
        state: finished
      }
    };
    expect(savePersistedData(storage, data)).toBe(true);

    const controller = new GameController({
      catalog,
      storage,
      clock,
      seeds: new FakeSeeds(["unused"])
    });
    expect(controller.savedMatchStatus).toBe("completed");
    expect(controller.restoreLastMatch()?.phase).toEqual({ kind: "finished", winnerId: "blue" });
    expect(controller.state?.pause).toBeNull();
  });

  it("resets history without removing the last snapshot", () => {
    const storage = new MemoryStorage();
    const controller = makeController(storage);
    controller.start(CONFIG);
    chooseFirstTopic(controller);
    const before = loadPersistedData(storage, makeCatalog().revision).lastMatch;
    expect(controller.questionHistory.serial).toBe(1);

    controller.resetQuestionHistory();
    const after = loadPersistedData(storage, makeCatalog().revision);
    expect(after.history.serial).toBe(0);
    expect(after.lastMatch).toEqual(before);
    expect(controller.state?.phase.kind).toBe("answering");
  });

  it("persists preferences independently and rejects invalid volume", () => {
    const storage = new MemoryStorage();
    const controller = makeController(storage);
    controller.start(CONFIG);
    const snapshot = loadPersistedData(storage, makeCatalog().revision).lastMatch;
    expect(controller.updatePreferences({ muted: true, textSize: "large" })).toMatchObject({
      muted: true,
      textSize: "large"
    });
    expect(loadPersistedData(storage, makeCatalog().revision).lastMatch).toEqual(snapshot);
    expect(() => controller.updatePreferences({ volume: 2 })).toThrow(RangeError);

    const reloaded = makeController(storage, new FakeClock(), new FakeSeeds(["unused"]));
    expect(reloaded.preferences).toMatchObject({ muted: true, textSize: "large" });
  });
});

describe("CatalogDomainContext tie-break exhaustion", () => {
  it("recycles hard questions only after every hard question was excluded", () => {
    const catalog = makeCatalog();
    const context = new CatalogDomainContext(catalog, EMPTY_QUESTION_HISTORY);
    const allHardIds = catalog.topics.flatMap((topic) =>
      topic.questions
        .filter((question) => question.difficulty === "hard")
        .map((question) => question.id)
    );
    const request = {
      topicId: null,
      difficulty: "hard" as const,
      excludedQuestionIds: allHardIds,
      random: seedRandom("hard-cycle")
    };

    expect(() => context.selectQuestion(request)).toThrow("Нет доступной темы");
    const recycled = context.selectQuestion({
      ...request,
      allowRecycleWhenExhausted: true
    });
    expect(allHardIds).toContain(recycled.question.id);
    expect(recycled.recycledAfterExhaustion).toBe(true);
  });
});
