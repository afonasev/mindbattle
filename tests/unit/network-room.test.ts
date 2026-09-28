import { describe, it, expect, vi } from "vitest";
import { NetworkRoom } from "../../src/network/room";
import { makeContext } from "./network-fixture";
import type { NetworkAction } from "../../src/network/protocol";
import type { DifficultyFeedbackEventV3 } from "../../src/feedback/types";
function setup(count = 2, submit: (event: DifficultyFeedbackEventV3) => Promise<void> = async () => {}) {
  let serial = 0;
  const room = new NetworkRoom(
    "0001",
    "display",
    makeContext(),
    {},
    () => `secret-${++serial}`,
    submit,
  );
  room.connect("display", 0);
  const seats = Array.from({ length: count }, (_, i) =>
    room.join(`Игрок ${i + 1}`, 0),
  );
  for (const s of seats) room.connect(s.token, 0);
  let time = 0;
  return {
    room,
    seats,
    command(token: string, action: NetworkAction) {
      const envelope = {
        commandId: `cmd-${++serial}`,
        epoch: room.epoch,
        phaseRevision: room.phaseRevision,
        action,
      };
      room.command(token, envelope, time);
      return envelope;
    },
    setTime(at: number) {
      time = at;
    },
  };
}
describe("network room", () => {
  it("authorizes roles and enforces full lobby", () => {
    const { room, seats, command } = setup(12);
    expect(() => room.join("13", 0)).toThrow("12");
    expect(() => command(seats[1].token, { type: "start" })).toThrow();
    command("display", { type: "start" });
    expect(() => room.join("Поздний", 0)).toThrow();
    expect(() => command("display", { type: "continue" })).toThrow();
  });
  it("deduplicates commands and fences old screens", () => {
    const { room, command } = setup();
    const envelope = command("display", { type: "start" });
    const epoch = room.epoch;
    room.command("display", envelope, 0);
    expect(room.epoch).toBe(epoch);
    expect(() =>
      room.command("display", { ...envelope, commandId: "different" }, 0),
    ).toThrow("Экран");
  });
  it("names the player choosing the next normal topic on every phone", () => {
    const { room, seats, command } = setup();
    command("display", { type: "start" });
    const phase = room.state!.phase;
    if (phase.kind !== "normal-topic") throw Error();
    expect(room.snapshot(seats[0].token, 0).chooserName).toBe(
      room.players.find((player) => player.id === phase.chooser)?.name,
    );
  });
  it("lets only the leader skip a topic countdown", () => {
    const { room, seats, command } = setup();
    command("display", { type: "start" });
    const phase = room.state!.phase;
    if (phase.kind !== "normal-topic") throw Error();
    command(seats.find((seat) => seat.id === phase.chooser)!.token, {
      type: "topic",
      topicId: phase.candidates[0],
    });
    expect(room.state?.phase.kind).toBe("topic-confirmation");
    expect(() => command(seats[1].token, { type: "continue" })).toThrow();
    command(seats[0].token, { type: "continue" });
    expect(room.state?.phase.kind).toBe("answering");
  });
  it("hides every other card and answer, including from display before reveal", () => {
    const { room, seats, command } = setup();
    command("display", { type: "start" });
    const chooser = room.state!.phase;
    if (chooser.kind !== "normal-topic") throw Error();
    const token = seats.find((s) => s.id === chooser.chooser)!.token;
    command(token, { type: "topic", topicId: chooser.candidates[0] });
    command(seats[0].token, { type: "continue" });
    command(seats[0].token, { type: "answer", position: "up" });
    const display = room.snapshot("display", 0);
    const own = room.snapshot(seats[0].token, 0);
    const other = room.snapshot(seats[1].token, 0);
    expect(own.ownAnswer).toBe("up");
    expect(other.view?.teams).toHaveLength(1);
    expect(other.view?.teams[0].id).toBe(seats[1].id);
    expect(other.scoreboard).toEqual([
      expect.objectContaining({ name: "Игрок 1", score: 0 }),
      expect.objectContaining({ name: "Игрок 2", score: 0 }),
    ]);
    expect(display.view?.question?.correctPosition).toBeUndefined();
    expect(display.view?.teams[0].answerPosition).toBeUndefined();
    expect(JSON.stringify(other)).not.toContain("correctAnswerId");
    expect(JSON.stringify(other)).not.toContain("secret-");
  });
  it("shares revealed choices and four shuffled notes with every phone, including a final spectator", () => {
    const { room, seats, command } = setup(4);
    command("display", { type: "start" });
    const topic = room.state!.phase;
    if (topic.kind !== "normal-topic") throw Error();
    command(seats.find(s => s.id === topic.chooser)!.token, { type: "topic", topicId: topic.candidates[0] });
    command(seats[0].token, { type: "continue" });
    const answering = room.state!;
    if (answering.phase.kind !== "answering") throw Error();
    const round = answering.phase.round;
    for (const token of ["display", ...seats.map(s => s.token)]) {
      const snapshot = room.snapshot(token, 0);
      expect(snapshot.revealedChoices).toBeUndefined();
      expect(snapshot.view?.question?.answerNotes).toBeUndefined();
      expect(snapshot.view?.question?.explanation).toBeUndefined();
      expect(snapshot.view?.question?.correctPosition).toBeUndefined();
    }
    const wrong = (["up", "right", "down", "left"] as const).find(p => p !== round.correctPosition)!;
    room.state = {
      ...answering,
      tieBreak: { originalLeaders: [seats[0].id, seats[1].id], contenders: [seats[0].id, seats[1].id], questionNumber: 1 },
      phase: { kind: "reveal", round, continuation: { kind: "tie-break", contenders: [seats[0].id] }, resolutions: [
        { teamId: seats[0].id, answer: round.correctPosition, result: "correct" },
        { teamId: seats[1].id, answer: wrong, result: "wrong" },
        { teamId: seats[2].id, answer: null, result: "no-answer" },
        { teamId: seats[3].id, answer: null, result: "spectator" }
      ] }
    };
    const display = room.snapshot("display", 0);
    expect(display.view?.question?.answerNotes).toHaveLength(4);
    for (const seat of seats) {
      const snapshot = room.snapshot(seat.token, 0);
      expect(snapshot.view?.teams).toHaveLength(1);
      expect(snapshot.view?.teams[0].id).toBe(seat.id);
      expect(snapshot.revealedChoices).toEqual(display.revealedChoices);
      expect(snapshot.view?.question).toEqual(display.view?.question);
      expect(snapshot.revealedChoices?.filter(c => c.answerPosition != null)).toHaveLength(2);
      for (const note of snapshot.view!.question!.answerNotes!) {
        expect(note.answer).toBe(snapshot.view!.question!.options[note.position]);
      }
    }
    expect(room.snapshot(seats[3].token, 0).spectating).toBe(true);
  });

  it("sends full tied standings and departed rows to every phone at every results phase", () => {
    const { room, seats, command } = setup(12);
    command("display", { type: "start" });
    const state = room.state!;
    room.players[11].departed = true;
    for (const phase of [
      { kind: "standings" as const, completedStage: 1 as const },
      { kind: "standings" as const, completedStage: 3 as const, tieBreakContenders: [seats[0].id, seats[1].id] },
      { kind: "finished" as const, winnerId: seats[1].id }
    ]) {
      room.state = { ...state, departedTeamIds: [seats[11].id], phase };
      const display = room.snapshot("display", 0);
      for (const seat of seats.slice(0, 11)) {
        const snapshot = room.snapshot(seat.token, 0);
        expect(snapshot.view?.standings).toEqual(display.view?.standings);
        expect(snapshot.view?.standings).toHaveLength(12);
        expect(snapshot.players).toHaveLength(12);
        expect(snapshot.players[11].departed).toBe(true);
        expect(snapshot.view?.winnerId).toBe(display.view?.winnerId);
        expect(snapshot.view?.standings?.at(-1)?.rank).toBe(0);
      }
    }
  });

  it("shares named bonus vetoes and rejects another player's topic", () => {
    const { room, seats, command } = setup();
    command("display", { type: "start" });
    const state = room.state!;
    room.state = {
      ...state,
      phase: {
        kind: "bonus-veto",
        candidates: ["topic-1", "topic-2", "topic-3"],
        cursors: { [seats[0].id]: 0, [seats[1].id]: 0 },
        vetoes: { [seats[0].id]: "topic-1" },
      },
    };
    const snapshot = room.snapshot(seats[1].token, 0);
    expect(snapshot.vetoes).toEqual([
      { playerId: seats[0].id, name: "Игрок 1", topicId: "topic-1" },
    ]);
    expect(snapshot.view?.vetoes).toBeUndefined();
    expect(() =>
      command(seats[1].token, { type: "veto", topicId: "topic-1" }),
    ).toThrow("уже исключил");
    command(seats[1].token, { type: "veto", topicId: "topic-2" });
    expect(room.state?.phase.kind).toBe("topic-confirmation");
  });
  it("restores identity, ignores stale stream close, and waits for leader", () => {
    const { room, seats, command } = setup();
    command("display", { type: "start" });
    room.disconnect(seats[0].token, 1, 0);
    expect(room.state?.pause).not.toBeNull();
    expect(() => command(seats[0].token, { type: "resume" })).toThrow();
    const generation = room.connect(seats[0].token, 0);
    room.disconnect(seats[0].token, 1, 0);
    expect(room.snapshot(seats[0].token, 0).players[0].connected).toBe(true);
    expect(generation).toBe(2);
    expect(room.state?.pause).not.toBeNull();
    command(seats[0].token, { type: "resume" });
    expect(room.state?.pause).toBeNull();
  });
  it("requires display restoration and detects missing heartbeat", () => {
    const { room, seats, command, setTime } = setup();
    command("display", { type: "start" });
    setTime(8001);
    room.tick(8001);
    expect(room.display.connected).toBe(false);
    expect(room.state?.pause).not.toBeNull();
    for (const s of seats) room.connect(s.token, 8001);
    expect(() => command(seats[0].token, { type: "resume" })).toThrow();
    room.connect("display", 8001);
    command(seats[0].token, { type: "resume" });
    expect(room.state?.pause).toBeNull();
  });
  it("transfers leader and denies excluded token, then reuses lobby", () => {
    const { room, seats, command } = setup(3);
    command("display", { type: "start" });
    room.disconnect(seats[0].token, 1, 0);
    command("display", { type: "exclude", playerId: seats[0].id });
    expect(room.leaderId).toBe(seats[1].id);
    expect(() => room.connect(seats[0].token, 0)).toThrow();
    expect(room.snapshot("display", 0).view?.teams[0].departed).toBe(true);
    command(seats[1].token, { type: "replay" });
    expect(room.state).toBeNull();
    expect(room.code).toBe("0001");
    expect(room.players).toHaveLength(2);
  });
  it("fences feedback stages and rejects a repeated choice on the reasons screen", () => {
    const { room, seats, command } = setup();
    command("display", { type: "start" });
    const phase = room.state!.phase;
    if (phase.kind !== "normal-topic") throw Error();
    command(seats.find((s) => s.id === phase.chooser)!.token, {
      type: "topic",
      topicId: phase.candidates[0],
    });
    command(seats[0].token, { type: "continue" });
    for (const seat of seats)
      command(seat.token, { type: "answer", position: "up" });
    command(seats[0].token, { type: "continue" });
    const envelope = command(seats[0].token, {
      type: "feedback-choice",
      complaint: true,
    });
    expect(() =>
      room.command(
        seats[0].token,
        { ...envelope, commandId: "late-choice" },
        0,
      ),
    ).toThrow("Экран");
    expect(() =>
      command(seats[0].token, { type: "feedback-choice", complaint: true }),
    ).toThrow("Экран");
    expect(room.state!.phase).toMatchObject({
      kind: "difficulty-feedback",
      stage: "reasons",
      complaintReasons: [],
    });
  });
  it("offers the leader a skip after three seconds and ignores a late write", async () => {
    vi.useFakeTimers();
    try {
      const completeWrites: (() => void)[] = [];
      const events: DifficultyFeedbackEventV3[] = [];
      const { room, seats, command } = setup(2, async (event) => {
        events.push(event);
        await new Promise<void>((resolve) => { completeWrites.push(resolve); });
      });
      command("display", { type: "start" });
      const topic = room.state!.phase;
      if (topic.kind !== "normal-topic") throw Error();
      command(seats.find((s) => s.id === topic.chooser)!.token, { type: "topic", topicId: topic.candidates[0] });
      command(seats[0].token, { type: "continue" });
      for (const seat of seats) command(seat.token, { type: "answer", position: "up" });
      command(seats[0].token, { type: "continue" });
      command(seats[0].token, { type: "feedback-choice", complaint: false });
      expect(room.state?.phase.kind).toBe("difficulty-feedback");
      await vi.advanceTimersByTimeAsync(2_999);
      expect(room.snapshot(seats[0].token, 0).feedbackError).toBe("");
      await vi.advanceTimersByTimeAsync(1);
      expect(room.snapshot(seats[0].token, 0).feedbackError).toContain("Не удалось");
      expect(events).toHaveLength(1);
      command(seats[0].token, { type: "retry-feedback" });
      expect(room.snapshot(seats[0].token, 0).feedbackError).toBe("");
      await vi.advanceTimersByTimeAsync(3_000);
      expect(room.snapshot(seats[0].token, 0).feedbackError).toContain("Не удалось");
      expect(events).toHaveLength(2);
      expect(events[1].eventId).toBe(events[0].eventId);
      command(seats[0].token, { type: "skip-feedback" });
      expect(room.state?.phase.kind).toBe("normal-topic");
      completeWrites.forEach((resolve) => resolve());
      await Promise.resolve();
      expect(room.state?.phase.kind).toBe("normal-topic");
      expect(events).toHaveLength(2);
    } finally {
      vi.useRealTimers();
    }
  });
  it("freezes even when a disconnect lands exactly as unanswered time expires", () => {
    const { room, seats, command } = setup();
    command("display", { type: "start" });
    const phase = room.state!.phase;
    if (phase.kind !== "normal-topic") throw Error();
    command(seats.find((s) => s.id === phase.chooser)!.token, {
      type: "topic",
      topicId: phase.candidates[0],
    });
    command(seats[0].token, { type: "continue" });
    room.disconnect(seats[0].token, 1, 110000);
    expect(room.state!.phase.kind).toBe("reveal");
    expect(room.state!.pause).not.toBeNull();
  });
});
