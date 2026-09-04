export type AudioCue =
  | "lobby-theme"
  | "countdown"
  | "question-start"
  | "timer-last-second"
  | "reserve-start"
  | "reveal"
  | "bonus"
  | "winner";

type AudioTrack = "event" | "music";

export interface AudioCueDefinition {
  readonly track: AudioTrack;
  readonly url: string;
}

export const AUDIO_CUE_MANIFEST: Readonly<Record<AudioCue, AudioCueDefinition>> = {
  "lobby-theme": { track: "music", url: "/audio/arena-v1/neon-arena.wav" },
  countdown: { track: "event", url: "/audio/arena-v1/topic-countdown.wav" },
  "question-start": { track: "event", url: "/audio/arena-v1/question-start.wav" },
  "timer-last-second": { track: "event", url: "/audio/arena-v1/timer-last-second.wav" },
  "reserve-start": { track: "event", url: "/audio/arena-v1/reserve-start.wav" },
  reveal: { track: "event", url: "/audio/arena-v1/reveal.wav" },
  bonus: { track: "music", url: "/audio/arena-v1/bonus.wav" },
  winner: { track: "music", url: "/audio/arena-v1/violet-victory.wav" }
};

export interface AudioSettings {
  readonly volume: number;
  readonly muted: boolean;
}

export interface AudioSource {
  volume: number;
  currentTime: number;
  play(): void | Promise<void>;
  pause(): void;
}

export interface AudioSourceFactory {
  create(url: string): AudioSource;
}

export class AudioController {
  private settings: AudioSettings;
  private activeMusic: AudioSource | null = null;

  constructor(
    private readonly sourceFactory: AudioSourceFactory,
    initial: AudioSettings = { volume: 0.7, muted: false }
  ) {
    this.settings = initial;
  }

  update(settings: AudioSettings) {
    this.settings = {
      muted: settings.muted,
      volume: Math.min(1, Math.max(0, settings.volume))
    };
  }

  stopMusic(): void {
    if (!this.activeMusic) return;
    try {
      this.activeMusic.pause();
      this.activeMusic.currentTime = 0;
    } catch {
      // Audio remains presentation-only even for broken browser implementations.
    }
    this.activeMusic = null;
  }

  play(cue: AudioCue): boolean {
    if (this.settings.muted || this.settings.volume === 0) return false;
    const definition = AUDIO_CUE_MANIFEST[cue];
    try {
      const source = this.sourceFactory.create(definition.url);
      source.volume = this.settings.volume;
      source.currentTime = 0;
      if (definition.track === "music") {
        this.stopMusic();
        this.activeMusic = source;
      }
      const result = source.play();
      if (result instanceof Promise) void result.catch(() => undefined);
      return true;
    } catch {
      return false;
    }
  }
}

export class AnsweringAudioMonitor {
  private previousBaseRemainingMs: number | null = null;
  private previousBaseSecond: number | null = null;

  reset(): void {
    this.previousBaseRemainingMs = null;
    this.previousBaseSecond = null;
  }

  observe(baseRemainingMs: number): readonly AudioCue[] {
    const cues: AudioCue[] = [];
    const second = Math.ceil(Math.max(0, baseRemainingMs) / 1_000);
    if (
      baseRemainingMs > 0 &&
      second >= 1 &&
      second <= 5 &&
      second !== this.previousBaseSecond
    ) {
      cues.push("timer-last-second");
    }
    if (this.previousBaseRemainingMs !== null && this.previousBaseRemainingMs > 0 && baseRemainingMs === 0) {
      cues.push("reserve-start");
    }
    this.previousBaseRemainingMs = baseRemainingMs;
    this.previousBaseSecond = second;
    return cues;
  }
}

export type PhaseAudioAction =
  | { readonly type: "play"; readonly cue: AudioCue }
  | { readonly type: "stop-music" };

export function phaseAudioActions(
  previousPhase: string | null,
  currentPhase: string | null
): readonly PhaseAudioAction[] {
  if (previousPhase === currentPhase) return [];
  if (!currentPhase || currentPhase === "topic-confirmation" || currentPhase === "answering") {
    return currentPhase === "answering"
      ? [{ type: "stop-music" }, { type: "play", cue: "question-start" }]
      : [{ type: "stop-music" }];
  }
  if (currentPhase === "normal-topic") return [{ type: "play", cue: "lobby-theme" }];
  if (currentPhase === "bonus-veto") return [{ type: "play", cue: "bonus" }];
  if (currentPhase === "reveal") return [{ type: "play", cue: "reveal" }];
  if (currentPhase === "finished") return [{ type: "play", cue: "winner" }];
  return [];
}

export function createHtmlAudioSourceFactory(): AudioSourceFactory {
  return {
    create(url) {
      return new Audio(url);
    }
  };
}
