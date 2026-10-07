import { describe, expect, it, vi } from "vitest";
import {
  AnsweringAudioMonitor,
  AnswerCommitAudioMonitor,
  AUDIO_CUE_MANIFEST,
  AudioController,
  phaseAudioActions,
  classicMusicStage,
  presentationMusicCue,
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
  it("keeps brief effects above the music at equal saved slider levels", () => {
    const sources: FakeSource[] = [];
    const audio = new AudioController(factory(sources), { musicVolume: .7, effectsVolume: .7, muted: false });
    audio.play("game-theme");
    audio.play("answer-locked");
    // The quietest cue is 8 dB below the music master; the mix must reverse that gap.
    const relativeDb = -8 + 20 * Math.log10(sources[1].volume / sources[0].volume);
    expect(relativeDb).toBeGreaterThan(4);
    audio.update({ musicVolume: 1, effectsVolume: 1, muted: false });
    expect(sources[0].volume).toBeCloseTo(.25);
    expect(sources[1].volume).toBe(1);
    audio.stopEvents();
    audio.stopMusic();
  });

  it("ducks both sides of a music transition and applies updated sliders to both", () => {
    vi.useFakeTimers();
    try {
      const sources: FakeSource[] = [];
      const audio = new AudioController(factory(sources), { musicVolume: 1, effectsVolume: 1, muted: false }, 650);
      audio.play("game-theme");
      audio.play("game-theme-two");
      vi.advanceTimersByTime(325);
      audio.play("reveal-all");
      expect(sources[0].volume + sources[1].volume).toBeCloseTo(.07);
      audio.update({ musicVolume: .4, effectsVolume: .8, muted: false });
      expect(sources[0].volume + sources[1].volume).toBeCloseTo(.028);
      expect(sources[2].volume).toBe(.8);
      audio.stopEvents();
      expect(sources[0].volume + sources[1].volume).toBeCloseTo(.1);
      vi.advanceTimersByTime(325);
      expect(sources[0].paused).toBe(true);
      expect(sources[1].volume).toBeCloseTo(.1);
      audio.stopMusic();
    } finally { vi.useRealTimers(); }
  });
  it("uses stable local URLs, loops themes and does not restart the active music cue", () => {
    expect(Object.values(AUDIO_CUE_MANIFEST).every(({ url }) => url.startsWith("/audio/"))).toBe(true);
    const sources: FakeSource[] = [];
    const audio = new AudioController(factory(sources), { musicVolume: 2, effectsVolume: 1, muted: false });
    audio.update({ musicVolume: 2, effectsVolume: 1, muted: false });
    expect(audio.play("menu-theme")).toBe(true);
    expect(audio.play("countdown")).toBe(true);
    expect(audio.play("game-theme")).toBe(true);
    expect(audio.play("game-theme")).toBe(true);
    expect(sources[0]).toMatchObject({ paused: true, currentTime: 0, volume: 0.25, loop: true });
    expect(sources[1]).toMatchObject({ paused: false, playCalls: 1 });
    expect(sources).toHaveLength(3);
  });

  it("ducks active game music while keeping events at the requested volume", () => {
    const sources: FakeSource[] = [];
    const audio = new AudioController(factory(sources), { musicVolume: 0.5, effectsVolume: 0.8, muted: false });
    audio.play("game-theme");
    audio.setMusicDucked(true);
    expect(sources[0].volume).toBeCloseTo(0.035);
    audio.play("timer-last-second");
    expect(sources[1].volume).toBeCloseTo(0.8);
    audio.setMusicDucked(false);
    expect(sources[0].volume).toBeCloseTo(0.125);
  });

  it("keeps music playback alive at zero volume and restores separate levels without restarting", () => {
    const sources: FakeSource[] = [];
    const audio = new AudioController(factory(sources), { musicVolume: 0.6, effectsVolume: 0.2, muted: false });
    audio.play("game-theme");
    audio.update({ musicVolume: 0, effectsVolume: 0.9, muted: false });
    expect(sources[0]).toMatchObject({ paused: false, volume: 0, playCalls: 1 });
    expect(audio.play("countdown")).toBe(true);
    expect(sources[1].volume).toBeCloseTo(0.9);
    audio.update({ musicVolume: 0.4, effectsVolume: 0.9, muted: false });
    expect(audio.play("game-theme")).toBe(true);
    expect(sources).toHaveLength(2);
    expect(sources[0]).toMatchObject({ paused: false, volume: 0.1, playCalls: 1 });
  });

  it("is silent when muted and survives source failure", async () => {
    const sources: FakeSource[] = [];
    const audio = new AudioController(factory(sources), { musicVolume: 0.5, effectsVolume: 0.5, muted: true });
    expect(audio.play("winner")).toBe(false);
    expect(sources).toEqual([]);
    audio.update({ musicVolume: 0.5, effectsVolume: 0.5, muted: false });
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
      { type: "set-music-ducked", ducked: false }
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
      { type: "stop-music" }, { type: "play", cue: "winner" }
    ]);
    expect(phaseAudioActions(null, "finished")).toEqual([{ type: "stop-music" }]);
  });
});

describe("stage music and lifecycle", () => {
  it.each([9, 15, 21])("selects all three stages and tie-break for %i questions", (count) => {
    const size = count / 3;
    expect(classicMusicStage(0, count)).toBe(0);
    expect(classicMusicStage(size - 1, count)).toBe(0);
    expect(classicMusicStage(size, count)).toBe(1);
    expect(classicMusicStage(2 * size - 1, count)).toBe(1);
    expect(classicMusicStage(2 * size, count)).toBe(2);
    expect(classicMusicStage(count, count, true)).toBe(2);
    expect(presentationMusicCue("answering", 1)).toBe("game-theme-two");
    expect(presentationMusicCue("reveal", 2)).toBe("game-theme-three");
    expect(presentationMusicCue("finished", 2)).toBeNull();
    expect(presentationMusicCue("lobby", 2)).toBe("menu-theme");
  });

  it("keeps the selected stage playing under bonus and restores it after mute/pause", () => {
    const sources: FakeSource[] = [];
    const audio = new AudioController(factory(sources));
    audio.play("game-theme-two");
    audio.play("bonus");
    expect(sources[0].paused).toBe(false);
    audio.update({ musicVolume: .4, effectsVolume: .2, muted: false });
    audio.play("game-theme-two");
    expect(sources).toHaveLength(2);
    audio.update({ musicVolume: .4, effectsVolume: .2, muted: true });
    expect(sources[0].paused).toBe(true);
    audio.update({ musicVolume: .4, effectsVolume: .2, muted: false });
    audio.play("game-theme-two");
    audio.stopMusic();
    audio.setMusicDucked(true);
    audio.play("game-theme-two");
    expect(sources[3].volume).toBeCloseTo(.028);
  });

  it("crossfades a theme change and stops both sources when muted mid-transition", () => {
    vi.useFakeTimers();
    try {
      const sources: FakeSource[] = [];
      const audio = new AudioController(factory(sources), { musicVolume: .5, effectsVolume: .5, muted: false }, 650);
      audio.play("game-theme");
      audio.play("game-theme-two");
      expect(sources[1].volume).toBe(0);
      vi.advanceTimersByTime(325);
      expect(sources[0].volume).toBeCloseTo(.0625);
      expect(sources[1].volume).toBeCloseTo(.0625);
      vi.advanceTimersByTime(325);
      expect(sources[0].paused).toBe(true);
      expect(sources[1].volume).toBeCloseTo(.125);
      audio.play("game-theme-three");
      vi.advanceTimersByTime(100);
      audio.update({ musicVolume: .5, effectsVolume: .5, muted: true });
      expect(sources[1].paused).toBe(true);
      expect(sources[2].paused).toBe(true);
      expect(vi.getTimerCount()).toBe(0);
    } finally { vi.useRealTimers(); }
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


describe("accepted answer and SFX lifecycle", () => {
  it("confirms new accepted players, deduplicates replacements, and silently primes reconnects", () => {
    const monitor = new AnswerCommitAudioMonitor();
    expect(monitor.observe("q1", [])).toEqual([]);
    expect(monitor.observe("q1", ["red"])).toEqual(["answer-locked"]);
    expect(monitor.observe("q1", ["red"])).toEqual([]);
    expect(monitor.observe("q1", ["red", "blue"])).toEqual(["answer-locked"]);
    expect(monitor.observe("q2", ["blue"])).toEqual([]);
    expect(monitor.observe("q2", ["blue", "red"])).toEqual(["answer-locked"]);
  });

  it("separates timeout from error while preserving mixed/all/none outcomes and spectators", () => {
    expect(revealOutcomeCue([{ result: "no-answer" }])).toBe("timeout");
    expect(revealOutcomeCue([{ result: "no-answer" }, { result: "spectator" }])).toBe("timeout");
    expect(revealOutcomeCue([{ result: "wrong" }, { result: "no-answer" }])).toBe("reveal-none");
    expect(revealOutcomeCue([{ result: "correct" }, { result: "no-answer" }])).toBe("reveal-some");
  });

  it("plays victory at effects volume with silent music, and stops all active tails on mute", () => {
    vi.useFakeTimers();
    try {
      const sources: FakeSource[] = [];
      const audio = new AudioController(factory(sources), { musicVolume: 0, effectsVolume: .6, muted: false });
      expect(audio.play("winner")).toBe(true);
      expect(sources[0].volume).toBeCloseTo(.6);
      audio.update({ musicVolume: 0, effectsVolume: .2, muted: false });
      expect(sources[0]).toMatchObject({ volume: .2, playCalls: 1 });
      audio.update({ musicVolume: 0, effectsVolume: .2, muted: true });
      expect(sources[0]).toMatchObject({ paused: true, currentTime: 0 });
      expect(vi.getTimerCount()).toBe(0);
    } finally { vi.useRealTimers(); }
  });

  it("gives a result space in the mix, preserves neutral lock, and releases ducking on ended", () => {
    vi.useFakeTimers();
    try {
      const sources: FakeSource[] = [];
      const audio = new AudioController(factory(sources), { musicVolume: .5, effectsVolume: .7, muted: false });
      audio.play("game-theme");
      audio.play("timer-last-second");
      audio.play("answer-locked");
      audio.play("reveal-all");
      expect(sources[1].paused).toBe(true);
      expect(sources[2].paused).toBe(false);
      expect(sources[0].volume).toBeCloseTo(.035);
      vi.advanceTimersByTime(3500);
      expect(sources[0].volume).toBeCloseTo(.125);
      audio.play("reveal-none");
      audio.setMusicDucked(true);
      audio.stopEvents();
      expect(sources[4].paused).toBe(true);
      expect(sources[0].volume).toBeCloseTo(.035);
      expect(vi.getTimerCount()).toBe(0);
    } finally { vi.useRealTimers(); }
  });

  it("clears rejected effects without leaving the music ducked", async () => {
    vi.useFakeTimers();
    try {
      const sources: FakeSource[] = [];
      const audio = new AudioController(factory(sources, { reject: true }));
      audio.play("reveal-all");
      await Promise.resolve();
      expect(vi.getTimerCount()).toBe(0);
    } finally { vi.useRealTimers(); }
  });
});
