import type { SoloCommand, SoloState } from "../domain/solo";

export type SoloInputKind = "pointer" | "wasd" | "arrows" | "gamepad";
type SoloPhase = SoloState["phase"];

function sourceForKeyboard(code: string): SoloInputKind {
  return code.startsWith("Arrow") ? "arrows" : "wasd";
}

export function soloKeyboardCommand(code: string, phase: SoloPhase | undefined): {
  readonly source: SoloInputKind;
  readonly command: SoloCommand;
} | null {
  if (!phase) return null;
  const key = code === "Space" ? " " : code.startsWith("Key") ? code.slice(3).toLowerCase() : code.toLowerCase();
  const answerPosition = ({ ArrowUp: "up", KeyW: "up", ArrowRight: "right", KeyD: "right", ArrowDown: "down", KeyS: "down", ArrowLeft: "left", KeyA: "left" } as const)[code];
  const command: SoloCommand | null = phase.kind === "topic"
    ? code === "ArrowLeft" || key === "a" ? { type: "move-topic", delta: -1 } : code === "ArrowRight" || key === "d" ? { type: "move-topic", delta: 1 } : code === "Enter" || code === "Space" ? { type: "confirm-topic" } : null
    : phase.kind === "risk"
      ? code === "ArrowLeft" || key === "a" ? { type: "move-risk", delta: -1 } : code === "ArrowRight" || key === "d" ? { type: "move-risk", delta: 1 } : code === "Enter" || code === "Space" ? { type: "confirm-risk" } : null
      : phase.kind === "answering" && answerPosition
        ? { type: "answer", position: answerPosition }
        : phase.kind === "reveal" && (code === "Enter" || code === "Space") ? { type: "continue" } : null;
  return command ? { source: sourceForKeyboard(code), command } : null;
}

export function soloGamepadCommand(button: number, phase: SoloPhase | undefined): SoloCommand | null {
  if (!phase) return null;
  const direction = ({ 3: "up", 1: "right", 0: "down", 2: "left", 12: "up", 15: "right", 13: "down", 14: "left" } as const)[button];
  if (phase.kind === "answering" && direction) return { type: "answer", position: direction };
  if (phase.kind === "topic" && button === 14) return { type: "move-topic", delta: -1 };
  if (phase.kind === "topic" && button === 15) return { type: "move-topic", delta: 1 };
  if (phase.kind === "topic" && button === 0) return { type: "confirm-topic" };
  if (phase.kind === "risk" && button === 14) return { type: "move-risk", delta: -1 };
  if (phase.kind === "risk" && button === 15) return { type: "move-risk", delta: 1 };
  if (phase.kind === "risk" && button === 0) return { type: "confirm-risk" };
  if (phase.kind === "reveal" && button === 0) return { type: "continue" };
  return null;
}
