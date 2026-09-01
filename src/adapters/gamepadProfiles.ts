export type GamepadProfile = "xbox" | "playstation" | "nintendo" | "universal";

export type CardinalDirection = "north" | "east" | "south" | "west";

export const GAMEPAD_BUTTON = {
  south: 0,
  east: 1,
  west: 2,
  north: 3,
  dpadNorth: 12,
  dpadSouth: 13,
  dpadWest: 14,
  dpadEast: 15,
} as const;

export interface GamepadGlyphSet {
  readonly answer: Readonly<Record<CardinalDirection, string>>;
  readonly bonus: Readonly<Record<"up" | "down" | "confirm" | "cancel", string>>;
}

const DPAD_GLYPHS = {
  up: "D-pad ↑",
  down: "D-pad ↓",
  confirm: "D-pad →",
  cancel: "D-pad ←",
} as const;

export const GAMEPAD_GLYPHS: Readonly<Record<GamepadProfile, GamepadGlyphSet>> = {
  xbox: {
    answer: { north: "Y", east: "B", south: "A", west: "X" },
    bonus: DPAD_GLYPHS,
  },
  playstation: {
    answer: { north: "△", east: "○", south: "×", west: "□" },
    bonus: DPAD_GLYPHS,
  },
  nintendo: {
    answer: { north: "X", east: "A", south: "B", west: "Y" },
    bonus: DPAD_GLYPHS,
  },
  universal: {
    answer: { north: "▲", east: "▶", south: "▼", west: "◀" },
    bonus: DPAD_GLYPHS,
  },
};

/** Detects label profile only; game rules always use physical button positions. */
export function detectGamepadProfile(id: string, mapping: string): GamepadProfile {
  if (mapping !== "standard") {
    return "universal";
  }

  const normalized = id.toLocaleLowerCase("en-US");
  if (/(xbox|xinput)/u.test(normalized)) {
    return "xbox";
  }
  if (/(dualsense|dualshock|playstation|wireless controller)/u.test(normalized)) {
    return "playstation";
  }
  if (/(nintendo|switch|joy-con|pro controller)/u.test(normalized)) {
    return "nintendo";
  }
  return "universal";
}

export function answerDirectionForGamepadButton(
  buttonIndex: number,
): CardinalDirection | undefined {
  switch (buttonIndex) {
    case GAMEPAD_BUTTON.north:
      return "north";
    case GAMEPAD_BUTTON.east:
      return "east";
    case GAMEPAD_BUTTON.south:
      return "south";
    case GAMEPAD_BUTTON.west:
      return "west";
    default:
      return undefined;
  }
}

export type BonusGamepadAction = "move-up" | "move-down" | "confirm" | "cancel";

export function bonusActionForGamepadButton(
  buttonIndex: number,
): BonusGamepadAction | undefined {
  switch (buttonIndex) {
    case GAMEPAD_BUTTON.dpadNorth:
      return "move-up";
    case GAMEPAD_BUTTON.dpadSouth:
      return "move-down";
    case GAMEPAD_BUTTON.dpadEast:
      return "confirm";
    case GAMEPAD_BUTTON.dpadWest:
      return "cancel";
    default:
      return undefined;
  }
}

export function isActionableGamepadButton(buttonIndex: number): boolean {
  return (
    answerDirectionForGamepadButton(buttonIndex) !== undefined ||
    bonusActionForGamepadButton(buttonIndex) !== undefined
  );
}
