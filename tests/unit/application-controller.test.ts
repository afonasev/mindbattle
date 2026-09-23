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
import { SoloController } from "../../src/application/soloController";
import { createMatch } from "../../src/domain/match";
import { CatalogDomainContext } from "../../src/application/contentContext";
import type { ContentCatalog, TopicPack } from "../../src/content/types";
import { EMPTY_QUESTION_HISTORY, seedRandom } from "../../src/content";
import type { MatchConfig, MatchState } from "../../src/domain/types";
import type { DifficultyFeedbackEvent, DifficultyFeedbackSink } from "../../src/feedback";

class MemoryStorage implements StorageLike {
  value: string | null = null;
  writes = 0;
  private additional = new Map<string, string>();

  getItem(key: string): string | null {
    return key === STORAGE_KEY ? this.value : this.additional.get(key) ?? null;
  }

  setItem(key: string, value: string): void {
    if (key !== STORAGE_KEY) { this.additional.set(key, value); return; }
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

class FakeFeedback implements DifficultyFeedbackSink {
  readonly events: DifficultyFeedbackEvent[] = [];
  fail = false;

  async submit(event: DifficultyFeedbackEvent): Promise<void> {
    this.events.push(event);
    if (this.fail) throw new Error("disk unavailable");
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
  seeds = new FakeSeeds(["seed-a", "seed-b"]),
  feedback?: DifficultyFeedbackSink
): GameController {
  return new GameController({ catalog: makeCatalog(), storage, clock, seeds, feedback });
}

function chooseFirstTopic(controller: GameController): MatchState {
  const state = controller.state;
  if (!state || state.phase.kind !== "normal-topic") throw new Error("Expected topic choice");
  const next = controller.dispatch([
    {
      type: "confirm-topic",
      teamId: state.phase.chooser
    }
  ]);
  if (!next) throw new Error("Expected active match");
  if (next.phase.kind !== "topic-confirmation") throw new Error("Expected topic confirmation");
  const answering = controller.dispatch([{ type: "continue", teamId: "green" }]);
  if (!answering) throw new Error("Expected active match");
  return answering;
}

describe("GameController", () => {
  it("persists one shared positive signal before advancing and retries the same event after failure", async () => {
    const storage = new MemoryStorage();
    const feedback = new FakeFeedback();
    feedback.fail = true;
    const controller = makeController(storage, new FakeClock(), new FakeSeeds(["feedback-seed"]), feedback);
    controller.start(CONFIG);
    let state = chooseFirstTopic(controller);
    if (state.phase.kind !== "answering") throw new Error("Expected answering");
    const position = state.phase.round.correctPosition;
    controller.dispatch(CONFIG.teams.map((teamId) => ({ type: "answer" as const, teamId, position })));
    controller.dispatch([{ type: "continue", teamId: "green" }]);
    expect(controller.state?.phase.kind).toBe("difficulty-feedback");
    expect(await controller.handleFeedbackConfirmation()).toBe(false);
    expect(controller.difficultyFeedbackStatus).toBe("error");
    const failedEventId = feedback.events[0].eventId;
    expect(feedback.events[0].matchId).toBe("match-v1:feedback-seed");
    expect(feedback.events[0]).toMatchObject({ schemaVersion: 3, hasComplaint: false, complaintReasons: [] });
    feedback.fail = false;
    expect(await controller.handleFeedbackConfirmation()).toBe(true);
    expect(feedback.events[1].eventId).toBe(failedEventId);
    expect(feedback.events[1]).toMatchObject({ hasComplaint: false, complaintReasons: [] });
    expect(controller.state?.phase.kind).toBe("normal-topic");
  });

  it("lets a shared match skip a failed feedback write without another submission", async () => {
    const feedback = new FakeFeedback();
    feedback.fail = true;
    const controller = makeController(new MemoryStorage(), new FakeClock(), new FakeSeeds(["skip-seed"]), feedback);
    controller.start(CONFIG);
    const state = chooseFirstTopic(controller);
    if (state.phase.kind !== "answering") throw new Error("Expected answering");
    const position = state.phase.round.correctPosition;
    controller.dispatch(CONFIG.teams.map((teamId) => ({ type: "answer" as const, teamId, position })));
    controller.dispatch([{ type: "continue", teamId: "green" }]);
    expect(await controller.handleFeedbackConfirmation()).toBe(false);
    expect(controller.skipCompletedFeedback()).toBe(true);
    expect(controller.state?.phase.kind).toBe("normal-topic");
    expect(feedback.events).toHaveLength(1);
  });

  it("persists the chosen topic before the question is created", () => {
    const storage = new MemoryStorage();
    const controller = makeController(storage);
    const initial = controller.start(CONFIG);
    if (initial.phase.kind !== "normal-topic") throw new Error("Expected topic choice");
    const confirmation = controller.dispatch([{
      type: "confirm-topic",
      teamId: initial.phase.chooser
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
      type: "confirm-topic",
      teamId: initial.phase.chooser
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

describe("SoloController", () => {
  it("retries one anonymous v3 feedback event before opening the next slot", async () => {
    const storage = new MemoryStorage();
    const clock = new FakeClock();
    const feedback = new FakeFeedback();
    feedback.fail = true;
    const controller = new SoloController({
      catalog: makeCatalog(),
      storage,
      clock,
      seeds: new FakeSeeds(["solo-feedback-seed"]),
      feedback
    });
    controller.start({ profile: "solo-endless-v1" });
    const topic = controller.state;
    if (!topic || topic.phase.kind !== "topic") throw new Error("Expected solo topic choice");
    controller.dispatch([{ type: "confirm-topic" }]);
    const answering = controller.state;
    if (!answering || answering.phase.kind !== "answering") throw new Error("Expected solo question");
    controller.dispatch([{ type: "answer", position: answering.phase.round.correctPosition }]);
    controller.dispatch([{ type: "continue" }]);
    expect(controller.state?.phase.kind).toBe("feedback");
    controller.setFeedbackChoice(false);
    expect(await controller.submitFeedback()).toBe(false);
    expect(controller.state?.phase.kind).toBe("feedback");
    const eventId = feedback.events[0].eventId;
    expect(feedback.events[0]).toMatchObject({ schemaVersion: 3, hasComplaint: false, complaintReasons: [] });
    feedback.fail = false;
    expect(await controller.submitFeedback()).toBe(true);
    expect(feedback.events[1].eventId).toBe(eventId);
    expect(controller.state?.phase.kind).toBe("topic");
  });

  it("lets a solo run skip a failed feedback write", async () => {
    const feedback = new FakeFeedback();
    feedback.fail = true;
    const controller = new SoloController({
      catalog: makeCatalog(), storage: new MemoryStorage(), clock: new FakeClock(),
      seeds: new FakeSeeds(["solo-skip-seed"]), feedback
    });
    controller.start({ profile: "solo-endless-v1" });
    controller.dispatch([{ type: "confirm-topic" }]);
    const answering = controller.state;
    if (answering?.phase.kind !== "answering") throw new Error("Expected solo question");
    controller.dispatch([{ type: "answer", position: answering.phase.round.correctPosition }]);
    controller.dispatch([{ type: "continue" }]);
    controller.setFeedbackChoice(false);
    expect(await controller.submitFeedback()).toBe(false);
    expect(controller.skipFeedback()).toBe(true);
    expect(controller.state?.phase.kind).toBe("topic");
    expect(feedback.events).toHaveLength(1);
  });

  it("restores an unfinished solo run paused and saves the finished local result", () => {
    const storage = new MemoryStorage();
    const clock = new FakeClock();
    const controller = new SoloController({
      catalog: makeCatalog(),
      storage,
      clock,
      seeds: new FakeSeeds(["solo-restore-seed"])
    });
    controller.start({ profile: "solo-endless-v1", collectQuestionFeedback: false });
    controller.dispatch([{ type: "confirm-topic" }]);
    const restoredController = new SoloController({
      catalog: makeCatalog(),
      storage,
      clock,
      seeds: new FakeSeeds(["unused"])
    });
    expect(restoredController.canRestore).toBe(true);
    expect(restoredController.restore()?.paused).toBe(true);
    restoredController.dispatch([{ type: "resume" }]);

    for (let index = 0; index < 3; index += 1) {
      const state = restoredController.state;
      if (!state) throw new Error("Expected active solo run");
      if (state.phase.kind === "topic") restoredController.dispatch([{ type: "confirm-topic" }]);
      const answering = restoredController.state;
      if (!answering || answering.phase.kind !== "answering") throw new Error("Expected solo question");
      const wrong = answering.phase.round.correctPosition === "up" ? "right" : "up";
      restoredController.dispatch([{ type: "answer", position: wrong }]);
      if (index < 2) restoredController.dispatch([{ type: "continue" }]);
    }
    expect(restoredController.state?.phase.kind).toBe("reveal");
    restoredController.dispatch([{ type: "continue" }]);
    expect(restoredController.state?.phase.kind).toBe("finished");
    const record = restoredController.saveResult("Игрок");
    expect(record).toMatchObject({ name: "Игрок", score: 0 });
    expect(restoredController.records[0]).toEqual(record);
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
