import {
  answerDirectionForGamepadButton,
  bonusActionForGamepadButton,
  detectGamepadProfile,
  type CardinalDirection,
  type GamepadProfile,
  isActionableGamepadButton,
} from "./gamepadProfiles";

export type TeamId = string;
export type KeyboardLayout = "wasd" | "arrows";

export type ControlSource =
  | { readonly kind: "keyboard"; readonly layout: KeyboardLayout }
  | {
      readonly kind: "gamepad";
      readonly index: number;
      readonly id: string;
      readonly profile: GamepadProfile;
    };

export interface TeamControlAssignment {
  readonly teamId: TeamId;
  readonly source: ControlSource;
}

export type AssignmentResult =
  | { readonly ok: true; readonly assignments: readonly TeamControlAssignment[] }
  | {
      readonly ok: false;
      readonly reason: "source-in-use";
      readonly conflictingTeamId: TeamId;
      readonly assignments: readonly TeamControlAssignment[];
    };

export function controlSourceKey(source: ControlSource): string {
  return source.kind === "keyboard"
    ? `keyboard:${source.layout}`
    : `gamepad:${source.index}`;
}

export function assignControlSource(
  assignments: readonly TeamControlAssignment[],
  teamId: TeamId,
  source: ControlSource,
): AssignmentResult {
  const sourceKey = controlSourceKey(source);
  const conflict = assignments.find(
    (assignment) =>
      assignment.teamId !== teamId && controlSourceKey(assignment.source) === sourceKey,
  );
  if (conflict) {
    return {
      ok: false,
      reason: "source-in-use",
      conflictingTeamId: conflict.teamId,
      assignments,
    };
  }

  return {
    ok: true,
    assignments: [
      ...assignments.filter((assignment) => assignment.teamId !== teamId),
      { teamId, source },
    ],
  };
}

export function assignmentsAreCompleteAndUnique(
  teamIds: readonly TeamId[],
  assignments: readonly TeamControlAssignment[],
): boolean {
  if (assignments.length !== teamIds.length) {
    return false;
  }
  const expectedTeams = new Set(teamIds);
  const assignedTeams = new Set(assignments.map(({ teamId }) => teamId));
  const sources = assignments.map(({ source }) => controlSourceKey(source));
  return (
    assignedTeams.size === teamIds.length &&
    [...assignedTeams].every((teamId) => expectedTeams.has(teamId)) &&
    new Set(sources).size === sources.length
  );
}

export type InputMode = "answer" | "normal-topic" | "bonus-veto" | "continue";

export type SemanticInputAction =
  | { readonly type: "answer"; readonly teamId: TeamId; readonly direction: CardinalDirection }
  | {
      readonly type: "topic-select";
      readonly teamId: TeamId;
      readonly direction: "west" | "north" | "east";
    }
  | { readonly type: "bonus-move"; readonly teamId: TeamId; readonly delta: -1 | 1 }
  | { readonly type: "bonus-confirm"; readonly teamId: TeamId }
  | { readonly type: "bonus-cancel"; readonly teamId: TeamId }
  | { readonly type: "continue"; readonly teamId: TeamId }
  | { readonly type: "pause"; readonly reason: "escape" | "blur" }
  | {
      readonly type: "pause";
      readonly reason: "gamepad-disconnected";
      readonly teamId: TeamId;
      readonly gamepadIndex: number;
    }
  | {
      readonly type: "gamepad-reconnected";
      readonly teamId: TeamId;
      readonly source: Extract<ControlSource, { kind: "gamepad" }>;
    };

export interface KeyboardInputEvent {
  readonly type: "keydown" | "keyup";
  readonly code: string;
  readonly repeat?: boolean;
}

export interface GamepadSnapshot {
  readonly index: number;
  readonly id: string;
  readonly mapping: string;
  readonly connected: boolean;
  readonly buttons: readonly boolean[];
}

export interface InputRouterState {
  readonly gate: "armed" | "waiting-neutral";
  readonly pressedKeys: ReadonlySet<string>;
  readonly gamepadButtons: ReadonlyMap<number, readonly boolean[]>;
  readonly disconnectedGamepads: ReadonlySet<number>;
}

export interface InputResult {
  readonly state: InputRouterState;
  readonly actions: readonly SemanticInputAction[];
}

export function createInputRouterState(armed = true): InputRouterState {
  return {
    gate: armed ? "armed" : "waiting-neutral",
    pressedKeys: new Set(),
    gamepadButtons: new Map(),
    disconnectedGamepads: new Set(),
  };
}

export function disarmUntilNeutral(state: InputRouterState): InputRouterState {
  return { ...state, gate: "waiting-neutral" };
}

const KEYBOARD_DIRECTIONS: Readonly<
  Record<KeyboardLayout, Readonly<Record<string, CardinalDirection>>>
> = {
  wasd: { KeyW: "north", KeyD: "east", KeyS: "south", KeyA: "west" },
  arrows: {
    ArrowUp: "north",
    ArrowRight: "east",
    ArrowDown: "south",
    ArrowLeft: "west",
  },
};

export const KEYBOARD_GLYPHS: Readonly<
  Record<KeyboardLayout, Readonly<Record<CardinalDirection, string>>>
> = {
  wasd: { north: "W", east: "D", south: "S", west: "A" },
  arrows: { north: "↑", east: "→", south: "↓", west: "←" },
};

export function keyboardDirection(
  layout: KeyboardLayout,
  code: string,
): CardinalDirection | undefined {
  return KEYBOARD_DIRECTIONS[layout][code];
}

function actionForDirection(
  teamId: TeamId,
  direction: CardinalDirection,
  mode: InputMode,
): SemanticInputAction | undefined {
  if (mode === "answer") {
    return { type: "answer", teamId, direction };
  }
  if (mode === "continue") {
    return { type: "continue", teamId };
  }
  if (mode === "normal-topic") {
    return direction === "west" || direction === "north" || direction === "east"
      ? { type: "topic-select", teamId, direction }
      : undefined;
  }
  switch (direction) {
    case "west":
      return { type: "bonus-move", teamId, delta: -1 };
    case "east":
      return { type: "bonus-move", teamId, delta: 1 };
    case "south":
      return { type: "bonus-confirm", teamId };
    case "north":
      return { type: "bonus-cancel", teamId };
  }
}

function keyboardAssignmentForCode(
  assignments: readonly TeamControlAssignment[],
  code: string,
): { readonly teamId: TeamId; readonly direction: CardinalDirection } | undefined {
  for (const assignment of assignments) {
    if (assignment.source.kind !== "keyboard") {
      continue;
    }
    const direction = keyboardDirection(assignment.source.layout, code);
    if (direction) {
      return { teamId: assignment.teamId, direction };
    }
  }
  return undefined;
}

function hasPressedActionableKey(state: InputRouterState): boolean {
  return [...state.pressedKeys].some((code) =>
    (Object.keys(KEYBOARD_DIRECTIONS) as KeyboardLayout[]).some(
      (layout) => keyboardDirection(layout, code) !== undefined,
    ),
  );
}

function hasPressedActionableGamepadButton(state: InputRouterState): boolean {
  for (const buttons of state.gamepadButtons.values()) {
    if (buttons.some((pressed, index) => pressed && isActionableGamepadButton(index))) {
      return true;
    }
  }
  return false;
}

function armIfNeutral(state: InputRouterState): InputRouterState {
  if (
    state.gate === "waiting-neutral" &&
    !hasPressedActionableKey(state) &&
    !hasPressedActionableGamepadButton(state)
  ) {
    return { ...state, gate: "armed" };
  }
  return state;
}

export function handleKeyboardInput(
  state: InputRouterState,
  event: KeyboardInputEvent,
  assignments: readonly TeamControlAssignment[],
  mode: InputMode,
): InputResult {
  const pressedKeys = new Set(state.pressedKeys);
  if (event.type === "keyup") {
    pressedKeys.delete(event.code);
    return {
      state: armIfNeutral({ ...state, pressedKeys }),
      actions: [],
    };
  }

  if (event.repeat || pressedKeys.has(event.code)) {
    return { state, actions: [] };
  }
  pressedKeys.add(event.code);
  let nextState: InputRouterState = { ...state, pressedKeys };

  if (event.code === "Escape") {
    nextState = disarmUntilNeutral(nextState);
    return { state: nextState, actions: [{ type: "pause", reason: "escape" }] };
  }
  if (state.gate !== "armed") {
    return { state: nextState, actions: [] };
  }

  const assigned = keyboardAssignmentForCode(assignments, event.code);
  const action = assigned
    ? actionForDirection(assigned.teamId, assigned.direction, mode)
    : undefined;
  return {
    state: nextState,
    actions: action ? [action] : [],
  };
}

function pressedButtons(snapshot: GamepadSnapshot): readonly boolean[] {
  return snapshot.connected ? snapshot.buttons : [];
}

function risingButtonIndices(
  previous: readonly boolean[] | undefined,
  current: readonly boolean[],
): readonly number[] {
  const result: number[] = [];
  current.forEach((pressed, index) => {
    if (pressed && !(previous?.[index] ?? false)) {
      result.push(index);
    }
  });
  return result;
}

function semanticGamepadAction(
  teamId: TeamId,
  buttonIndex: number,
  mode: InputMode,
): SemanticInputAction | undefined {
  if (mode === "answer") {
    const direction = answerDirectionForGamepadButton(buttonIndex);
    return direction ? { type: "answer", teamId, direction } : undefined;
  }
  if (mode === "continue") {
    return isActionableGamepadButton(buttonIndex)
      ? { type: "continue", teamId }
      : undefined;
  }

  if (mode === "normal-topic") {
    const direction = answerDirectionForGamepadButton(buttonIndex);
    return direction === "west" || direction === "north" || direction === "east"
      ? { type: "topic-select", teamId, direction }
      : undefined;
  }

  const action = bonusActionForGamepadButton(buttonIndex);
  switch (action) {
    case "move-left":
      return { type: "bonus-move", teamId, delta: -1 };
    case "move-right":
      return { type: "bonus-move", teamId, delta: 1 };
    case "confirm":
      return { type: "bonus-confirm", teamId };
    case "cancel":
      return { type: "bonus-cancel", teamId };
    default:
      return undefined;
  }
}

function gamepadSource(snapshot: GamepadSnapshot): Extract<ControlSource, { kind: "gamepad" }> {
  return {
    kind: "gamepad",
    index: snapshot.index,
    id: snapshot.id,
    profile: detectGamepadProfile(snapshot.id, snapshot.mapping),
  };
}

/**
 * Processes one deterministic Gamepad API snapshot. If reconnectTeamId is set,
 * a new press on a free gamepad is consumed exclusively by reconnection.
 */
export function handleGamepadPoll(
  state: InputRouterState,
  snapshots: readonly GamepadSnapshot[],
  assignments: readonly TeamControlAssignment[],
  mode: InputMode,
  reconnectTeamId?: TeamId,
): InputResult {
  const connected = new Map(
    snapshots.filter(({ connected }) => connected).map((snapshot) => [snapshot.index, snapshot]),
  );
  const gamepadButtons = new Map(state.gamepadButtons);
  for (const snapshot of snapshots) {
    gamepadButtons.set(snapshot.index, pressedButtons(snapshot));
  }

  const disconnectedGamepads = new Set(state.disconnectedGamepads);
  const actions: SemanticInputAction[] = [];
  for (const assignment of assignments) {
    if (assignment.source.kind !== "gamepad") {
      continue;
    }
    const index = assignment.source.index;
    if (!connected.has(index) && !disconnectedGamepads.has(index)) {
      disconnectedGamepads.add(index);
      actions.push({
        type: "pause",
        reason: "gamepad-disconnected",
        teamId: assignment.teamId,
        gamepadIndex: index,
      });
    }
  }

  let nextState: InputRouterState = {
    ...state,
    gamepadButtons,
    disconnectedGamepads,
  };

  const detectedDisconnect = actions.some(
    (action) => action.type === "pause" && action.reason === "gamepad-disconnected",
  );

  if (reconnectTeamId) {
    const occupiedByOtherTeams = new Set(
      assignments
        .filter(
          (assignment) =>
            assignment.teamId !== reconnectTeamId && assignment.source.kind === "gamepad",
        )
        .map((assignment) => (assignment.source as Extract<ControlSource, { kind: "gamepad" }>).index),
    );
    const candidate = snapshots
      .filter(({ connected: isConnected, index }) => isConnected && !occupiedByOtherTeams.has(index))
      .sort((left, right) => left.index - right.index)
      .find((snapshot) =>
        risingButtonIndices(state.gamepadButtons.get(snapshot.index), snapshot.buttons).some(
          isActionableGamepadButton,
        ),
      );

    if (candidate) {
      disconnectedGamepads.delete(candidate.index);
      nextState = disarmUntilNeutral({ ...nextState, disconnectedGamepads });
      return {
        state: nextState,
        actions: [
          ...actions,
          {
            type: "gamepad-reconnected",
            teamId: reconnectTeamId,
            source: gamepadSource(candidate),
          },
        ],
      };
    }

    // Reconnect mode belongs to the pause overlay. Input from controllers that
    // are still assigned must not leak through as menu/continue actions.
    nextState = armIfNeutral(nextState);
    return { state: nextState, actions };
  }

  if (detectedDisconnect) {
    return { state: disarmUntilNeutral(nextState), actions };
  }

  if (state.gate === "armed") {
    for (const assignment of assignments) {
      if (assignment.source.kind !== "gamepad") {
        continue;
      }
      const snapshot = connected.get(assignment.source.index);
      if (!snapshot || disconnectedGamepads.has(snapshot.index)) {
        continue;
      }
      const previous = state.gamepadButtons.get(snapshot.index);
      if (!previous) {
        continue;
      }
      for (const buttonIndex of risingButtonIndices(previous, snapshot.buttons)) {
        const action = semanticGamepadAction(assignment.teamId, buttonIndex, mode);
        if (action) {
          actions.push(action);
        }
      }
    }
  }

  nextState = armIfNeutral(nextState);
  return { state: nextState, actions };
}

export function handleWindowBlur(state: InputRouterState): InputResult {
  return {
    state: disarmUntilNeutral({ ...state, pressedKeys: new Set() }),
    actions: [{ type: "pause", reason: "blur" }],
  };
}

export function snapshotBrowserGamepads(
  gamepads: readonly (Gamepad | null)[],
): readonly GamepadSnapshot[] {
  return gamepads
    .filter((gamepad): gamepad is Gamepad => gamepad !== null)
    .map((gamepad) => ({
      index: gamepad.index,
      id: gamepad.id,
      mapping: gamepad.mapping,
      connected: gamepad.connected,
      buttons: gamepad.buttons.map((button) => button.pressed || button.value >= 0.5),
    }));
}
