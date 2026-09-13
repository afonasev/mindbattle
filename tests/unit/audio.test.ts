import { describe, expect, it } from "vitest";
import {
  AnsweringAudioMonitor,
  AUDIO_CUE_MANIFEST,
  AudioController,
  phaseAudioActions,
  RevealAudioMonitor,
  shouldPlayNetworkAudio,
  revealOutcomeCue,
  TopicCountdownAudioMonitor,
  type AudioSource,
  type AudioSourceFactory
} from "../../src/adapters/audio";

class FakeSource implements AudioSource {
  volume = 0;
  currentTime = 4;
  loop = false;
  paused = false;
  playCalls = 0;

  constructor(private readonly reject = false) {}

  play(): Promise<void> {
    this.playCalls += 1;
    return this.reject ? Promise.reject(new Error("autoplay denied")) : Promise.resolve();
  }

  pause(): void {
    this.paused = true;
  }
}

function factory(sources: FakeSource[], options: { reject?: boolean; throwOnCreate?: boolean } = {}): AudioSourceFactory {
  return {
    create() {
      if (options.throwOnCreate) throw new Error("audio unavailable");
      const source = new FakeSource(options.reject);
      sources.push(source);
      return source;
    }
  };
}

describe("audio controller", () => {
  it("uses stable local URLs, loops themes and does not restart the active music cue", () => {
    expect(Object.values(AUDIO_CUE_MANIFEST).every(({ url }) => url.startsWith("/audio/"))).toBe(true);
    const sources: FakeSource[] = [];
    const audio = new AudioController(factory(sources), { volume: 2, muted: false });
    audio.update({ volume: 2, muted: false });
    expect(audio.play("menu-theme")).toBe(true);
    expect(audio.play("countdown")).toBe(true);
    expect(audio.play("game-theme")).toBe(true);
    expect(audio.play("game-theme")).toBe(true);
    expect(sources[0]).toMatchObject({ paused: true, currentTime: 0, volume: 1, loop: true });
    expect(sources[1]).toMatchObject({ paused: false, playCalls: 1 });
    expect(sources).toHaveLength(3);
  });

  it("ducks active game music while keeping events at the requested volume", () => {
    const sources: FakeSource[] = [];
    const audio = new AudioController(factory(sources), { volume: 0.5, muted: false });
    audio.play("game-theme");
    audio.setMusicDucked(true);
    expect(sources[0].volume).toBeCloseTo(0.14);
    audio.play("timer-last-second");
    expect(sources[1].volume).toBeCloseTo(0.5);
    audio.setMusicDucked(false);
    expect(sources[0].volume).toBeCloseTo(0.5);
  });

  it("is silent when muted and survives source failure", async () => {
    const sources: FakeSource[] = [];
    const audio = new AudioController(factory(sources), { volume: 0.5, muted: true });
    expect(audio.play("winner")).toBe(false);
    expect(sources).toEqual([]);
    audio.update({ volume: 0.5, muted: false });
    expect(audio.play("winner")).toBe(true);
    await Promise.resolve();
    expect(new AudioController(factory([], { throwOnCreate: true })).play("winner")).toBe(false);
  });
});

describe("answering audio monitor", () => {
  it("deduplicates displayed last seconds and reports base-to-reserve once", () => {
    const monitor = new AnsweringAudioMonitor();
    expect(monitor.observe(6_000)).toEqual([]);
    expect(monitor.observe(5_000)).toEqual(["timer-last-second"]);
    expect(monitor.observe(4_950)).toEqual([]);
    expect(monitor.observe(2_100)).toEqual(["timer-last-second"]);
    expect(monitor.observe(0)).toEqual(["reserve-start"]);
    expect(monitor.observe(0)).toEqual([]);
  });
});

describe("topic countdown audio monitor", () => {
  it("plays once for every displayed countdown digit", () => {
    const monitor = new TopicCountdownAudioMonitor();
    expect(monitor.observe(3_000)).toEqual(["countdown"]);
    expect(monitor.observe(2_950)).toEqual([]);
    expect(monitor.observe(2_000)).toEqual(["countdown"]);
    expect(monitor.observe(1_000)).toEqual(["countdown"]);
    expect(monitor.observe(0)).toEqual([]);
    monitor.reset();
    expect(monitor.observe(3_000)).toEqual(["countdown"]);
  });
});

describe("phase audio orchestration", () => {
  it("keeps the game theme under a question and ducks it before the question cue", () => {
    expect(phaseAudioActions(null, "normal-topic")).toEqual([
      { type: "set-music-ducked", ducked: false },
      { type: "play", cue: "game-theme" }
    ]);
    expect(phaseAudioActions("normal-topic", "topic-confirmation")).toEqual([{ type: "play", cue: "screen-transition" }]);
    expect(phaseAudioActions("topic-confirmation", "answering")).toEqual([
      { type: "set-music-ducked", ducked: true },
      { type: "play", cue: "question-start" }
    ]);
    expect(phaseAudioActions("answering", "reveal")).toEqual([{ type: "set-music-ducked", ducked: false }]);
    expect(phaseAudioActions("answering", "bonus-veto")).toEqual([
      { type: "set-music-ducked", ducked: false },
      { type: "play", cue: "bonus" }
    ]);
    expect(phaseAudioActions("reveal", "finished")).toEqual([
      { type: "set-music-ducked", ducked: false },
      { type: "play", cue: "winner" }
    ]);
  });
});

describe("reveal outcome audio", () => {
  it("classifies only already-resolved team outcomes", () => {
    expect(revealOutcomeCue([{ result: "correct" }, { result: "correct" }])).toBe("reveal-all");
    expect(revealOutcomeCue([{ result: "correct" }, { result: "wrong" }])).toBe("reveal-some");
    expect(revealOutcomeCue([{ result: "wrong" }, { result: "no-answer" }, { result: "spectator" }])).toBe("reveal-none");
  });

  it("plays an outcome once per revealed state even if the UI renders again", () => {
    const monitor = new RevealAudioMonitor();
    const resolutions = [{ result: "correct" as const }, { result: "wrong" as const }];
    expect(monitor.observe("round-1", resolutions)).toEqual(["reveal-some"]);
    expect(monitor.observe("round-1", resolutions)).toEqual([]);
    expect(monitor.observe("round-2", resolutions)).toEqual(["reveal-some"]);
    monitor.reset();
    expect(monitor.observe("round-1", resolutions)).toEqual(["reveal-some"]);
  });
});

describe("network audio role", () => {
  it("limits audio to the shared desktop display", () => {
    expect(shouldPlayNetworkAudio("display", false)).toBe(true);
    expect(shouldPlayNetworkAudio("player", false)).toBe(false);
    expect(shouldPlayNetworkAudio("display", true)).toBe(false);
  });
});
