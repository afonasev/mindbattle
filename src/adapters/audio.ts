export type AudioCue =
  | "menu-theme"
  | "game-theme"
  | "game-theme-two"
  | "game-theme-three"
  | "screen-transition"
  | "countdown"
  | "question-start"
  | "timer-last-second"
  | "reserve-start"
  | "answer-locked"
  | "timeout"
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
  readonly durationMs?: number;
  readonly duckMusic?: boolean;
}

export const AUDIO_CUE_MANIFEST: Readonly<Record<AudioCue, AudioCueDefinition>> = {
  "menu-theme": { track: "music", url: "/audio/quiz-v1/menu.mp3", loop: true },
  "game-theme": { track: "music", url: "/audio/quiz-v1/stage-one.mp3", loop: true },
  "game-theme-two": { track: "music", url: "/audio/quiz-v1/stage-two.mp3", loop: true },
  "game-theme-three": { track: "music", url: "/audio/quiz-v1/stage-three.mp3", loop: true },
  "screen-transition": { track: "event", url: "/audio/quiz-sfx-v1/screen-transition.wav", durationMs: 300 },
  countdown: { track: "event", url: "/audio/quiz-sfx-v1/countdown.wav", durationMs: 180 },
  "question-start": { track: "event", url: "/audio/quiz-sfx-v1/question-start.wav", durationMs: 600 },
  "timer-last-second": { track: "event", url: "/audio/quiz-sfx-v1/timer-last-second.wav", durationMs: 200 },
  "reserve-start": { track: "event", url: "/audio/quiz-sfx-v1/reserve-start.wav", durationMs: 800 },
  "answer-locked": { track: "event", url: "/audio/quiz-sfx-v1/answer-locked.wav", durationMs: 120 },
  timeout: { track: "event", url: "/audio/quiz-sfx-v1/timeout.wav", durationMs: 3000, duckMusic: true },
  reveal: { track: "event", url: "/audio/quiz-sfx-v1/reveal.wav", durationMs: 2000, duckMusic: true },
  "reveal-all": { track: "event", url: "/audio/quiz-sfx-v1/reveal-all.wav", durationMs: 3000, duckMusic: true },
  "reveal-some": { track: "event", url: "/audio/quiz-sfx-v1/reveal-some.wav", durationMs: 2000, duckMusic: true },
  "reveal-none": { track: "event", url: "/audio/quiz-sfx-v1/reveal-none.wav", durationMs: 3000, duckMusic: true },
  bonus: { track: "event", url: "/audio/quiz-sfx-v1/bonus.wav", durationMs: 2000, duckMusic: true },
  winner: { track: "event", url: "/audio/quiz-sfx-v1/winner.wav", durationMs: 4000, duckMusic: true }
};

export interface AudioSettings {
  readonly musicVolume: number;
  readonly effectsVolume: number;
  readonly muted: boolean;
}

export interface AudioSource {
  volume: number;
  currentTime: number;
  loop: boolean;
  play(): void | Promise<void>;
  pause(): void;
  addEventListener?(type: string, listener: () => void, options?: { once?: boolean }): void;
}

export interface AudioSourceFactory {
  create(url: string): AudioSource;
}

export class AudioController {
  private settings: AudioSettings;
  private activeMusic: AudioSource | null = null;
  private activeMusicCue: AudioCue | null = null;
  private musicDucked = false;
  private retiringMusic: AudioSource | null = null;
  private fadeTimer: ReturnType<typeof setInterval> | null = null;
  private fadeProgress = 1;
  private readonly events = new Map<AudioSource, { cue: AudioCue; timer: ReturnType<typeof setTimeout>; duckMusic: boolean }>();

  constructor(
    private readonly sourceFactory: AudioSourceFactory,
    initial: AudioSettings = { musicVolume: 0.7, effectsVolume: 0.7, muted: false },
    private readonly musicTransitionMs = 0
  ) {
    this.settings = initial;
  }

  update(settings: AudioSettings) {
    this.settings = {
      muted: settings.muted,
      musicVolume: Math.min(1, Math.max(0, settings.musicVolume)),
      effectsVolume: Math.min(1, Math.max(0, settings.effectsVolume))
    };
    if (this.settings.muted) {
      this.stopMusic();
      this.stopEvents();
    }
    for (const source of this.events.keys()) source.volume = this.settings.effectsVolume;
    this.applyMusicVolume();
  }

  setMusicDucked(ducked: boolean): void {
    this.musicDucked = ducked;
    this.applyMusicVolume();
  }

  private applyMusicVolume(): void {
    const eventDuck = [...this.events.values()].some(event => event.duckMusic);
    if (this.activeMusic) this.activeMusic.volume = this.settings.musicVolume * (this.musicDucked || eventDuck ? 0.28 : 1) * this.fadeProgress;
  }

  private finishEvent(source: AudioSource): void {
    const event = this.events.get(source);
    if (!event) return;
    clearTimeout(event.timer);
    this.events.delete(source);
    this.applyMusicVolume();
  }

  stopEvents(): void {
    for (const [source, event] of this.events) {
      clearTimeout(event.timer);
      try { source.pause(); source.currentTime = 0; } catch { /* Optional audio. */ }
    }
    this.events.clear();
    this.applyMusicVolume();
  }

  private clearTransition(): void {
    if (this.fadeTimer !== null) clearInterval(this.fadeTimer);
    this.fadeTimer = null;
    if (this.retiringMusic) {
      this.retiringMusic.pause();
      this.retiringMusic.currentTime = 0;
      this.retiringMusic = null;
    }
    this.fadeProgress = 1;
  }

  stopMusic(): void {
    this.clearTransition();
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
    const definition = AUDIO_CUE_MANIFEST[cue];
    const volume = definition.track === "music" ? this.settings.musicVolume : this.settings.effectsVolume;
    if (this.settings.muted || volume === 0) return false;
    if (definition.track === "music" && this.activeMusic && this.activeMusicCue === cue) {
      this.applyMusicVolume();
      return true;
    }
    let source: AudioSource | null = null;
    try {
      source = this.sourceFactory.create(definition.url);
      const playingSource = source;
      source.volume = volume * (definition.track === "music" && this.musicDucked ? 0.28 : 1);
      source.currentTime = 0;
      source.loop = definition.loop === true;
      if (definition.track === "event") {
        // Outcome replaces countdown/reserve tails, but preserves the brief neutral lock.
        if (definition.duckMusic) {
          for (const [playing, event] of this.events) {
            if (event.cue === "answer-locked") continue;
            try { playing.pause(); playing.currentTime = 0; } catch { /* Optional audio. */ }
            this.finishEvent(playing);
          }
        }
        const timer = setTimeout(() => this.finishEvent(playingSource), (definition.durationMs ?? 3000) + 500);
        this.events.set(source, { cue, timer, duckMusic: definition.duckMusic === true });
        source.addEventListener?.("ended", () => this.finishEvent(playingSource), { once: true });
        this.applyMusicVolume();
      }
      if (definition.track === "music") {
        const previousMusic = this.activeMusic;
        this.clearTransition();
        if (previousMusic && this.musicTransitionMs <= 0) this.stopMusic();
        this.activeMusic = source;
        this.activeMusicCue = cue;
        if (previousMusic && this.musicTransitionMs > 0) {
          this.retiringMusic = previousMusic;
          const previousVolume = previousMusic.volume;
          const startedAt = Date.now();
          this.fadeProgress = 0;
          this.applyMusicVolume();
          this.fadeTimer = setInterval(() => {
            this.fadeProgress = Math.min(1, (Date.now() - startedAt) / this.musicTransitionMs);
            previousMusic.volume = previousVolume * (1 - this.fadeProgress);
            this.applyMusicVolume();
            if (this.fadeProgress === 1) this.clearTransition();
          }, 25);
        }
      }
      this.applyMusicVolume();
      const result = source.play();
      if (result instanceof Promise) void result.catch(() => {
        // Allow the next user gesture to retry after an autoplay denial.
        if (this.activeMusic === source) this.stopMusic();
        this.finishEvent(playingSource);
      });
      return true;
    } catch {
      if (source) this.finishEvent(source);
      return false;
    }
  }
}

let activeSharedAudioController: AudioController | null = null;

/**
 * Keeps presentation audio alive while the SPA switches between game modes.
 * Audio is intentionally shared only within one browser document.
 */
export function sharedAudioController(initial: AudioSettings): AudioController {
  if (!activeSharedAudioController) {
    activeSharedAudioController = new AudioController(createHtmlAudioSourceFactory(), initial, 650);
  } else {
    activeSharedAudioController.update(initial);
  }
  return activeSharedAudioController;
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

/** Presentation-only stage selection; index is zero-based, network questionNumber is not. */
export function classicMusicStage(questionIndex: number, questionCount: number, tieBreak = false): 0 | 1 | 2 {
  if (tieBreak) return 2;
  return Math.min(2, Math.max(0, Math.floor(questionIndex / (questionCount / 3)))) as 0 | 1 | 2;
}

export function presentationMusicCue(phase: string | null, stage: 0 | 1 | 2 = 0): AudioCue | null {
  if (!phase || phase === "lobby") return "menu-theme";
  if (phase === "finished") return null;
  return (["game-theme", "game-theme-two", "game-theme-three"] as const)[stage];
}

export function phaseAudioActions(
  previousPhase: string | null,
  currentPhase: string | null
): readonly PhaseAudioAction[] {
  if (previousPhase === currentPhase) return [];
  if (!currentPhase) return [];
  if (["normal-topic", "final-veto", "difficulty-feedback", "standings"].includes(currentPhase)) {
    return [{ type: "set-music-ducked", ducked: false }];
  }
  if (currentPhase === "topic-confirmation") return [{ type: "play", cue: "screen-transition" }];
  if (currentPhase === "answering") return [{ type: "set-music-ducked", ducked: true }, { type: "play", cue: "question-start" }];
  if (currentPhase === "bonus-veto") return [{ type: "set-music-ducked", ducked: false }, { type: "play", cue: "bonus" }];
  if (currentPhase === "reveal") return [{ type: "set-music-ducked", ducked: false }];
  if (currentPhase === "finished") return [
    { type: "stop-music" },
    ...(previousPhase ? [{ type: "play" as const, cue: "winner" as const }] : [])
  ];
  return [{ type: "play", cue: "screen-transition" }];
}

export function revealOutcomeCue(
  resolutions: readonly { readonly result: "correct" | "wrong" | "no-answer" | "spectator" }[]
): AudioCue {
  const active = resolutions.filter(({ result }) => result !== "spectator");
  const correct = active.filter(({ result }) => result === "correct").length;
  if (active.length > 0 && active.every(({ result }) => result === "no-answer")) return "timeout";
  if (correct === 0) return "reveal-none";
  return correct === active.length ? "reveal-all" : "reveal-some";
}

/** Observes acceptance only; never sees an answer position or correct result. */
export class AnswerCommitAudioMonitor {
  private signature: string | null = null;
  private answered = new Set<string>();

  observe(signature: string, answeredIds: readonly string[]): readonly AudioCue[] {
    const current = new Set(answeredIds);
    if (signature !== this.signature) {
      this.signature = signature;
      this.answered = current; // Restored/reconnected answers must stay silent.
      return [];
    }
    const added = [...current].some(id => !this.answered.has(id));
    this.answered = current;
    return added ? ["answer-locked"] : [];
  }
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
