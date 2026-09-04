import { describe, expect, it } from "vitest";
import {
  AnsweringAudioMonitor,
  AUDIO_CUE_MANIFEST,
  AudioController,
  phaseAudioActions,
  type AudioSource,
  type AudioSourceFactory
} from "../../src/adapters/audio";

class FakeSource implements AudioSource {
  volume = 0;
  currentTime = 4;
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
  it("uses stable local URLs and replaces only the active music cue", () => {
    expect(Object.values(AUDIO_CUE_MANIFEST).every(({ url }) => url.startsWith("/audio/arena-v1/"))).toBe(true);
    const sources: FakeSource[] = [];
    const audio = new AudioController(factory(sources), { volume: 2, muted: false });
    audio.update({ volume: 2, muted: false });
    expect(audio.play("lobby-theme")).toBe(true);
    expect(audio.play("countdown")).toBe(true);
    expect(audio.play("winner")).toBe(true);
    expect(sources[0]).toMatchObject({ paused: true, currentTime: 0, volume: 1 });
    expect(sources[1]).toMatchObject({ paused: false, playCalls: 1 });
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

describe("phase audio orchestration", () => {
  it("starts music only outside a question and stops it before the question cue", () => {
    expect(phaseAudioActions(null, "normal-topic")).toEqual([{ type: "play", cue: "lobby-theme" }]);
    expect(phaseAudioActions("normal-topic", "topic-confirmation")).toEqual([{ type: "stop-music" }]);
    expect(phaseAudioActions("topic-confirmation", "answering")).toEqual([
      { type: "stop-music" },
      { type: "play", cue: "question-start" }
    ]);
    expect(phaseAudioActions("answering", "bonus-veto")).toEqual([{ type: "play", cue: "bonus" }]);
    expect(phaseAudioActions("reveal", "finished")).toEqual([{ type: "play", cue: "winner" }]);
  });
});
