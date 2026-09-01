import { describe, expect, it } from "vitest";

import {
  assignControlSource,
  assignmentsAreCompleteAndUnique,
  createInputRouterState,
  disarmUntilNeutral,
  handleGamepadPoll,
  handleKeyboardInput,
  handleWindowBlur,
  type ControlSource,
  type GamepadSnapshot,
  type InputRouterState,
  type TeamControlAssignment,
} from "./input";
import {
  answerDirectionForGamepadButton,
  detectGamepadProfile,
  GAMEPAD_GLYPHS,
} from "./gamepadProfiles";

const keyboardAssignments: readonly TeamControlAssignment[] = [
  { teamId: "green", source: { kind: "keyboard", layout: "wasd" } },
  { teamId: "blue", source: { kind: "keyboard", layout: "arrows" } },
];

function gamepadSource(index: number, id = `Pad ${index}`): ControlSource {
  return { kind: "gamepad", index, id, profile: "universal" };
}

function pad(
  index: number,
  pressed: readonly number[] = [],
  id = `Pad ${index}`,
): GamepadSnapshot {
  const buttons = Array.from({ length: 16 }, (_, buttonIndex) =>
    pressed.includes(buttonIndex),
  );
  return { index, id, mapping: "standard", connected: true, buttons };
}

function pollBaseline(
  state: InputRouterState,
  assignments: readonly TeamControlAssignment[],
  snapshots: readonly GamepadSnapshot[],
): InputRouterState {
  return handleGamepadPoll(state, snapshots, assignments, "answer").state;
}

describe("control assignments and glyph profiles", () => {
  it("rejects a keyboard or gamepad source owned by another team", () => {
    const first = assignControlSource([], "green", {
      kind: "keyboard",
      layout: "wasd",
    });
    expect(first.ok).toBe(true);
    if (!first.ok) return;

    expect(assignControlSource(first.assignments, "blue", {
      kind: "keyboard",
      layout: "wasd",
    })).toMatchObject({ ok: false, conflictingTeamId: "green" });

    const withPad = assignControlSource(first.assignments, "blue", gamepadSource(2));
    expect(withPad.ok).toBe(true);
    if (!withPad.ok) return;
    expect(assignControlSource(withPad.assignments, "yellow", gamepadSource(2))).toMatchObject({
      ok: false,
      conflictingTeamId: "blue",
    });
  });

  it("allows a team to replace its source and validates a complete unique roster", () => {
    const reassigned = assignControlSource(keyboardAssignments, "green", gamepadSource(0));
    expect(reassigned.ok).toBe(true);
    if (!reassigned.ok) return;
    expect(assignmentsAreCompleteAndUnique(["green", "blue"], reassigned.assignments)).toBe(
      true,
    );
  });

  it("maps physical face positions and detects label-only profiles", () => {
    expect([3, 1, 0, 2].map(answerDirectionForGamepadButton)).toEqual([
      "north",
      "east",
      "south",
      "west",
    ]);
    expect(detectGamepadProfile("Xbox Wireless Controller", "standard")).toBe("xbox");
    expect(detectGamepadProfile("DualSense Wireless Controller", "standard")).toBe(
      "playstation",
    );
    expect(detectGamepadProfile("Nintendo Switch Pro Controller", "standard")).toBe(
      "nintendo",
    );
    expect(detectGamepadProfile("Mystery Pad", "standard")).toBe("universal");
    expect(GAMEPAD_GLYPHS.universal.answer).toEqual({
      north: "▲",
      east: "▶",
      south: "▼",
      west: "◀",
    });
  });
});

describe("keyboard routing", () => {
  it("routes WASD and arrows to the same positional answers", () => {
    let state = createInputRouterState();
    const green = handleKeyboardInput(
      state,
      { type: "keydown", code: "KeyD" },
      keyboardAssignments,
      "answer",
    );
    expect(green.actions).toEqual([{ type: "answer", teamId: "green", direction: "east" }]);
    state = green.state;
    const blue = handleKeyboardInput(
      state,
      { type: "keydown", code: "ArrowRight" },
      keyboardAssignments,
      "answer",
    );
    expect(blue.actions).toEqual([{ type: "answer", teamId: "blue", direction: "east" }]);
  });

  it("ignores repeat and duplicate keydown until keyup", () => {
    let state = createInputRouterState();
    const first = handleKeyboardInput(
      state,
      { type: "keydown", code: "KeyW" },
      keyboardAssignments,
      "answer",
    );
    state = first.state;
    expect(
      handleKeyboardInput(
        state,
        { type: "keydown", code: "KeyW", repeat: true },
        keyboardAssignments,
        "answer",
      ).actions,
    ).toEqual([]);
    expect(
      handleKeyboardInput(
        state,
        { type: "keydown", code: "KeyW" },
        keyboardAssignments,
        "answer",
      ).actions,
    ).toEqual([]);
  });

  it("maps bonus navigation to move, confirm and cancel", () => {
    let state = createInputRouterState();
    const expected = [
      ["KeyW", { type: "bonus-move", teamId: "green", delta: -1 }],
      ["KeyS", { type: "bonus-move", teamId: "green", delta: 1 }],
      ["KeyD", { type: "bonus-confirm", teamId: "green" }],
      ["KeyA", { type: "bonus-cancel", teamId: "green" }],
    ] as const;
    for (const [code, action] of expected) {
      const pressed = handleKeyboardInput(
        state,
        { type: "keydown", code },
        keyboardAssignments,
        "bonus-veto",
      );
      expect(pressed.actions).toEqual([action]);
      state = handleKeyboardInput(
        pressed.state,
        { type: "keyup", code },
        keyboardAssignments,
        "bonus-veto",
      ).state;
    }
  });

  it("selects three normal topics directly with west, north and east", () => {
    for (const [code, direction] of [
      ["KeyA", "west"],
      ["KeyW", "north"],
      ["KeyD", "east"],
    ] as const) {
      const result = handleKeyboardInput(
        createInputRouterState(),
        { type: "keydown", code },
        keyboardAssignments,
        "normal-topic",
      );
      expect(result.actions).toEqual([{ type: "topic-select", teamId: "green", direction }]);
    }
    expect(
      handleKeyboardInput(
        createInputRouterState(),
        { type: "keydown", code: "KeyS" },
        keyboardAssignments,
        "normal-topic",
      ).actions,
    ).toEqual([]);
  });

  it("requires neutral after a screen transition", () => {
    const pressed = handleKeyboardInput(
      createInputRouterState(),
      { type: "keydown", code: "KeyW" },
      keyboardAssignments,
      "answer",
    );
    let state = disarmUntilNeutral(pressed.state);
    expect(
      handleKeyboardInput(
        state,
        { type: "keydown", code: "KeyW", repeat: true },
        keyboardAssignments,
        "continue",
      ).actions,
    ).toEqual([]);
    state = handleKeyboardInput(
      state,
      { type: "keyup", code: "KeyW" },
      keyboardAssignments,
      "continue",
    ).state;
    const continued = handleKeyboardInput(
      state,
      { type: "keydown", code: "KeyW" },
      keyboardAssignments,
      "continue",
    );
    expect(continued.actions).toEqual([{ type: "continue", teamId: "green" }]);
  });
});

describe("gamepad polling and lifecycle", () => {
  const assignments: readonly TeamControlAssignment[] = [
    { teamId: "green", source: gamepadSource(0) },
    { teamId: "blue", source: gamepadSource(1) },
  ];

  it("emits only rising edges and routes D-pad bonus actions", () => {
    let state = pollBaseline(createInputRouterState(), assignments, [pad(0), pad(1)]);
    const pressed = handleGamepadPoll(state, [pad(0, [15]), pad(1)], assignments, "bonus-veto");
    expect(pressed.actions).toEqual([{ type: "bonus-confirm", teamId: "green" }]);
    state = pressed.state;
    expect(
      handleGamepadPoll(state, [pad(0, [15]), pad(1)], assignments, "bonus-veto").actions,
    ).toEqual([]);
  });

  it("uses face-west, face-north and face-east for direct normal topics", () => {
    let state = pollBaseline(createInputRouterState(), assignments, [pad(0), pad(1)]);
    const west = handleGamepadPoll(state, [pad(0, [2]), pad(1)], assignments, "normal-topic");
    expect(west.actions).toEqual([
      { type: "topic-select", teamId: "green", direction: "west" }
    ]);
    state = handleGamepadPoll(west.state, [pad(0), pad(1)], assignments, "normal-topic").state;
    const north = handleGamepadPoll(state, [pad(0, [3]), pad(1)], assignments, "normal-topic");
    expect(north.actions).toEqual([
      { type: "topic-select", teamId: "green", direction: "north" }
    ]);
    state = handleGamepadPoll(north.state, [pad(0), pad(1)], assignments, "normal-topic").state;
    const east = handleGamepadPoll(state, [pad(0, [1]), pad(1)], assignments, "normal-topic");
    expect(east.actions).toEqual([
      { type: "topic-select", teamId: "green", direction: "east" }
    ]);
  });

  it("does not pass a held button through a neutral gate", () => {
    let state = pollBaseline(createInputRouterState(), assignments, [pad(0), pad(1)]);
    state = handleGamepadPoll(state, [pad(0, [0]), pad(1)], assignments, "answer").state;
    state = disarmUntilNeutral(state);
    const held = handleGamepadPoll(state, [pad(0, [0]), pad(1)], assignments, "continue");
    expect(held.actions).toEqual([]);
    const released = handleGamepadPoll(
      held.state,
      [pad(0), pad(1)],
      assignments,
      "continue",
    );
    expect(released.state.gate).toBe("armed");
    const pressedAgain = handleGamepadPoll(
      released.state,
      [pad(0, [0]), pad(1)],
      assignments,
      "continue",
    );
    expect(pressedAgain.actions).toEqual([{ type: "continue", teamId: "green" }]);
  });

  it("pauses once when an assigned gamepad disconnects", () => {
    let state = pollBaseline(createInputRouterState(), assignments, [pad(0), pad(1)]);
    const disconnected = handleGamepadPoll(state, [pad(1, [0])], assignments, "answer");
    expect(disconnected.actions).toEqual([
      {
        type: "pause",
        reason: "gamepad-disconnected",
        teamId: "green",
        gamepadIndex: 0,
      },
    ]);
    expect(disconnected.state.gate).toBe("waiting-neutral");
    state = disconnected.state;
    expect(handleGamepadPoll(state, [pad(1)], assignments, "answer").actions).toEqual([]);
  });

  it("reconnects only a free gamepad and consumes its press", () => {
    let state = pollBaseline(createInputRouterState(), assignments, [pad(0), pad(1)]);
    state = handleGamepadPoll(state, [pad(1)], assignments, "continue").state;

    const occupied = handleGamepadPoll(
      state,
      [pad(1, [0])],
      assignments,
      "continue",
      "green",
    );
    expect(occupied.actions).toEqual([]);

    const connectedFree = handleGamepadPoll(
      occupied.state,
      [pad(1), pad(2, [0], "Xbox Controller")],
      assignments,
      "continue",
      "green",
    );
    expect(connectedFree.actions).toEqual([
      {
        type: "gamepad-reconnected",
        teamId: "green",
        source: {
          kind: "gamepad",
          index: 2,
          id: "Xbox Controller",
          profile: "xbox",
        },
      },
    ]);
    expect(connectedFree.state.gate).toBe("waiting-neutral");
  });

  it("pauses on blur and disarms subsequent input", () => {
    const blurred = handleWindowBlur(createInputRouterState());
    expect(blurred.actions).toEqual([{ type: "pause", reason: "blur" }]);
    expect(blurred.state.gate).toBe("waiting-neutral");
  });
});
