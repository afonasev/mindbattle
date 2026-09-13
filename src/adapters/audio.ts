export type AudioCue =
  | "menu-theme"
  | "game-theme"
  | "screen-transition"
  | "countdown"
  | "question-start"
  | "timer-last-second"
  | "reserve-start"
  | "reveal"
  | "reveal-all"
  | "reveal-some"
  | "reveal-none"
  | "bonus"
  | "winner";

type AudioTrack = "event" | "music";

export interface AudioCueDefinition {
  readonly track: AudioTrack;
  readonly url: string;
  readonly loop?: boolean;
}

export const AUDIO_CUE_MANIFEST: Readonly<Record<AudioCue, AudioCueDefinition>> = {
  "menu-theme": { track: "music", url: "/audio/arena-v2/menu-theme.wav", loop: true },
  "game-theme": { track: "music", url: "/audio/arena-v2/game-theme.wav", loop: true },
  "screen-transition": { track: "event", url: "/audio/arena-v2/screen-transition.wav" },
  countdown: { track: "event", url: "/audio/arena-v1/topic-countdown.wav" },
  "question-start": { track: "event", url: "/audio/arena-v1/question-start.wav" },
  "timer-last-second": { track: "event", url: "/audio/arena-v1/timer-last-second.wav" },
  "reserve-start": { track: "event", url: "/audio/arena-v1/reserve-start.wav" },
  reveal: { track: "event", url: "/audio/arena-v1/reveal.wav" },
  "reveal-all": { track: "event", url: "/audio/arena-v2/reveal-all.wav" },
  "reveal-some": { track: "event", url: "/audio/arena-v2/reveal-some.wav" },
  "reveal-none": { track: "event", url: "/audio/arena-v2/reveal-none.wav" },
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
  loop: boolean;
  play(): void | Promise<void>;
  pause(): void;
}

export interface AudioSourceFactory {
  create(url: string): AudioSource;
}

export class AudioController {
  private settings: AudioSettings;
  private activeMusic: AudioSource | null = null;
  private activeMusicCue: AudioCue | null = null;
  private musicDucked = false;

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
    this.applyMusicVolume();
  }

  setMusicDucked(ducked: boolean): void {
    this.musicDucked = ducked;
    this.applyMusicVolume();
  }

  private applyMusicVolume(): void {
    if (this.activeMusic) this.activeMusic.volume = this.settings.volume * (this.musicDucked ? 0.28 : 1);
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
    this.activeMusicCue = null;
  }

  play(cue: AudioCue): boolean {
    if (this.settings.muted || this.settings.volume === 0) return false;
    const definition = AUDIO_CUE_MANIFEST[cue];
    if (definition.track === "music" && this.activeMusic && this.activeMusicCue === cue) {
      this.applyMusicVolume();
      return true;
    }
    try {
      const source = this.sourceFactory.create(definition.url);
      source.volume = this.settings.volume * (definition.track === "music" && this.musicDucked ? 0.28 : 1);
      source.currentTime = 0;
      source.loop = definition.loop === true;
      if (definition.track === "music") {
        this.stopMusic();
        this.activeMusic = source;
        this.activeMusicCue = cue;
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

export class TopicCountdownAudioMonitor {
  private previousSecond: number | null = null;

  reset(): void {
    this.previousSecond = null;
  }

  observe(remainingMs: number): readonly AudioCue[] {
    const second = Math.ceil(Math.max(0, remainingMs) / 1_000);
    const cues = second > 0 && second !== this.previousSecond ? ["countdown" as const] : [];
    this.previousSecond = second;
    return cues;
  }
}

export type PhaseAudioAction =
  | { readonly type: "play"; readonly cue: AudioCue }
  | { readonly type: "stop-music" }
  | { readonly type: "set-music-ducked"; readonly ducked: boolean };

export function phaseAudioActions(
  previousPhase: string | null,
  currentPhase: string | null
): readonly PhaseAudioAction[] {
  if (previousPhase === currentPhase) return [];
  if (!currentPhase) return [];
  if (["normal-topic", "final-veto", "difficulty-feedback", "standings"].includes(currentPhase)) {
    return [{ type: "set-music-ducked", ducked: false }, { type: "play", cue: "game-theme" }];
  }
  if (currentPhase === "topic-confirmation") return [{ type: "play", cue: "screen-transition" }];
  if (currentPhase === "answering") return [{ type: "set-music-ducked", ducked: true }, { type: "play", cue: "question-start" }];
  if (currentPhase === "bonus-veto") return [{ type: "set-music-ducked", ducked: false }, { type: "play", cue: "bonus" }];
  if (currentPhase === "reveal") return [{ type: "set-music-ducked", ducked: false }];
  if (currentPhase === "finished") return [{ type: "set-music-ducked", ducked: false }, { type: "play", cue: "winner" }];
  return [{ type: "play", cue: "screen-transition" }];
}

export function revealOutcomeCue(
  resolutions: readonly { readonly result: "correct" | "wrong" | "no-answer" | "spectator" }[]
): AudioCue {
  const active = resolutions.filter(({ result }) => result !== "spectator");
  const correct = active.filter(({ result }) => result === "correct").length;
  if (correct === 0) return "reveal-none";
  return correct === active.length ? "reveal-all" : "reveal-some";
}

export class RevealAudioMonitor {
  private previousSignature: string | null = null;

  reset(): void {
    this.previousSignature = null;
  }

  observe(
    signature: string,
    resolutions: readonly { readonly result: "correct" | "wrong" | "no-answer" | "spectator" }[]
  ): readonly AudioCue[] {
    if (signature === this.previousSignature) return [];
    this.previousSignature = signature;
    return [revealOutcomeCue(resolutions)];
  }
}

export function shouldPlayNetworkAudio(role: "display" | "player" | undefined, mobile: boolean): boolean {
  return role === "display" && !mobile;
}

export function createHtmlAudioSourceFactory(): AudioSourceFactory {
  return {
    create(url) {
      return new Audio(url);
    }
  };
}
