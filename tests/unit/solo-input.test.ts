import { describe, expect, it } from "vitest";
import { soloGamepadCommand, soloKeyboardCommand } from "../../src/adapters/soloInput";
import type { SoloState } from "../../src/domain/solo";

const topic = { kind: "topic", candidates: ["one", "two", "three"], cursor: 0 } as Extract<SoloState["phase"], { kind: "topic" }>;
const risk = { kind: "risk", difficulty: "medium", cursor: 0 } as Extract<SoloState["phase"], { kind: "risk" }>;
const answering = { kind: "answering" } as Extract<SoloState["phase"], { kind: "answering" }>;
const reveal = { kind: "reveal" } as Extract<SoloState["phase"], { kind: "reveal" }>;

describe("solo input adapter", () => {
  it("maps both keyboard layouts only to commands allowed by the phase", () => {
    expect(soloKeyboardCommand("KeyD", topic)).toEqual({ source: "wasd", command: { type: "move-topic", delta: 1 } });
    expect(soloKeyboardCommand("ArrowLeft", topic)).toEqual({ source: "arrows", command: { type: "move-topic", delta: -1 } });
    expect(soloKeyboardCommand("Enter", topic)).toEqual({ source: "wasd", command: { type: "confirm-topic" } });
    expect(soloKeyboardCommand("KeyW", answering)).toEqual({ source: "wasd", command: { type: "answer", position: "up" } });
    expect(soloKeyboardCommand("ArrowUp", answering)).toEqual({ source: "arrows", command: { type: "answer", position: "up" } });
    expect(soloKeyboardCommand("KeyW", risk)).toBeNull();
    expect(soloKeyboardCommand("KeyD", risk)).toEqual({ source: "wasd", command: { type: "move-risk", delta: 1 } });
    expect(soloKeyboardCommand("ArrowLeft", risk)).toEqual({ source: "arrows", command: { type: "move-risk", delta: -1 } });
    expect(soloKeyboardCommand("Enter", risk)).toEqual({ source: "wasd", command: { type: "confirm-risk" } });
    expect(soloKeyboardCommand("Space", reveal)).toEqual({ source: "wasd", command: { type: "continue" } });
  });

  it("maps standard face buttons and d-pad without leaking commands across phases", () => {
    expect(soloGamepadCommand(15, topic)).toEqual({ type: "move-topic", delta: 1 });
    expect(soloGamepadCommand(0, topic)).toEqual({ type: "confirm-topic" });
    expect(soloGamepadCommand(15, risk)).toEqual({ type: "move-risk", delta: 1 });
    expect(soloGamepadCommand(0, risk)).toEqual({ type: "confirm-risk" });
    expect(soloGamepadCommand(3, answering)).toEqual({ type: "answer", position: "up" });
    expect(soloGamepadCommand(12, answering)).toEqual({ type: "answer", position: "up" });
    expect(soloGamepadCommand(0, reveal)).toEqual({ type: "continue" });
    expect(soloGamepadCommand(3, risk)).toBeNull();
  });
});
