import { describe, expect, it, vi } from "vitest";
import { AudioController } from "../../src/adapters/audio";

describe("audio controller", () => {
  it("plays a local cue with bounded volume", () => {
    const play = vi.fn();
    const audio = new AudioController({ play }, { volume: 2, muted: false });
    audio.update({ volume: 2, muted: false });
    expect(audio.play("bonus")).toBe(true);
    expect(play).toHaveBeenCalledWith(780, 0.18, 1);
  });

  it("is silent when muted and survives sink failure", () => {
    const play = vi.fn(() => {
      throw new Error("unavailable");
    });
    const audio = new AudioController({ play }, { volume: 0.5, muted: true });
    expect(audio.play("winner")).toBe(false);
    expect(play).not.toHaveBeenCalled();
    audio.update({ volume: 0.5, muted: false });
    expect(audio.play("winner")).toBe(false);
  });
});
