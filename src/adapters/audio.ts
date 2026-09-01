export type AudioCue =
  | "question-start"
  | "countdown"
  | "reserve"
  | "reveal"
  | "bonus"
  | "winner";

const cueNotes: Readonly<Record<AudioCue, readonly [number, number]>> = {
  "question-start": [440, 0.09],
  countdown: [660, 0.06],
  reserve: [220, 0.16],
  reveal: [520, 0.13],
  bonus: [780, 0.18],
  winner: [880, 0.3]
};

export interface AudioSettings {
  readonly volume: number;
  readonly muted: boolean;
}

export interface CueSink {
  play(frequency: number, durationSeconds: number, volume: number): void | Promise<void>;
}

export class AudioController {
  private settings: AudioSettings;

  constructor(
    private readonly sink: CueSink,
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

  play(cue: AudioCue): boolean {
    if (this.settings.muted || this.settings.volume === 0) return false;
    const [frequency, duration] = cueNotes[cue];
    try {
      const result = this.sink.play(frequency, duration, this.settings.volume);
      if (result instanceof Promise) void result.catch(() => undefined);
      return true;
    } catch {
      return false;
    }
  }
}

export function createWebAudioSink(): CueSink {
  let context: AudioContext | null = null;
  return {
    async play(frequency, durationSeconds, volume) {
      context ??= new AudioContext();
      if (context.state === "suspended") await context.resume();
      const oscillator = context.createOscillator();
      const gain = context.createGain();
      const now = context.currentTime;
      oscillator.type = "sine";
      oscillator.frequency.setValueAtTime(frequency, now);
      gain.gain.setValueAtTime(0.0001, now);
      gain.gain.exponentialRampToValueAtTime(Math.max(0.0001, volume * 0.12), now + 0.01);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + durationSeconds);
      oscillator.connect(gain);
      gain.connect(context.destination);
      oscillator.start(now);
      oscillator.stop(now + durationSeconds + 0.01);
    }
  };
}
