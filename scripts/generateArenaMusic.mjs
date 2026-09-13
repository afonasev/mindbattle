import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const rate = 22_050;
const output = resolve("public/audio/arena-v2");
mkdirSync(output, { recursive: true });

const note = {
  C3: 130.81, D3: 146.83, E3: 164.81, F3: 174.61, G3: 196, A3: 220, B3: 246.94,
  C4: 261.63, D4: 293.66, E4: 329.63, F4: 349.23, G4: 392, A4: 440, B4: 493.88,
  C5: 523.25, D5: 587.33, E5: 659.25, F5: 698.46, G5: 783.99, A5: 880
};

function envelope(time, start, duration, attack = 0.025, release = 0.12) {
  const local = time - start;
  if (local < 0 || local > duration) return 0;
  if (local < attack) return local / attack;
  if (local > duration - release) return Math.max(0, (duration - local) / release);
  return 1;
}

function tone(time, start, duration, frequency, amplitude, shape = "sine") {
  const env = envelope(time, start, duration);
  const phase = 2 * Math.PI * frequency * (time - start);
  const oscillator = shape === "triangle" ? (2 / Math.PI) * Math.asin(Math.sin(phase)) : Math.sin(phase);
  return oscillator * amplitude * env;
}

function writeWav(name, seconds, render) {
  const frames = Math.round(seconds * rate);
  const data = Buffer.alloc(frames * 2);
  for (let frame = 0; frame < frames; frame += 1) {
    const sample = Math.max(-0.96, Math.min(0.96, render(frame / rate, seconds)));
    data.writeInt16LE(Math.round(sample * 32767), frame * 2);
  }
  const header = Buffer.alloc(44);
  header.write("RIFF", 0);
  header.writeUInt32LE(36 + data.length, 4);
  header.write("WAVEfmt ", 8);
  header.writeUInt32LE(16, 16);
  header.writeUInt16LE(1, 20);
  header.writeUInt16LE(1, 22);
  header.writeUInt32LE(rate, 24);
  header.writeUInt32LE(rate * 2, 28);
  header.writeUInt16LE(2, 32);
  header.writeUInt16LE(16, 34);
  header.write("data", 36);
  header.writeUInt32LE(data.length, 40);
  writeFileSync(resolve(output, name), Buffer.concat([header, data]));
}

function theme(name, bpm, chords, melody, seconds) {
  const beat = 60 / bpm;
  writeWav(name, seconds, (time) => {
    const bar = Math.floor(time / (beat * 4));
    const chord = chords[bar % chords.length];
    let value = 0;
    chord.forEach((frequency, index) => {
      value += tone(time, bar * beat * 4, beat * 4, frequency, 0.045 - index * 0.006, "triangle");
      value += tone(time, bar * beat * 4, beat * 4, frequency * 2, 0.010, "sine");
    });
    const step = Math.floor(time / beat);
    const pitch = melody[step % melody.length];
    value += tone(time, step * beat, beat * 0.82, pitch, 0.11, "sine");
    if (step % 2 === 0) value += tone(time, step * beat, beat * 0.13, chord[0] / 2, 0.11, "sine");
    if (step % 4 === 2) value += tone(time, step * beat, beat * 0.07, 1_600, 0.018, "sine");
    return value;
  });
}

theme("menu-theme.wav", 80,
  [[note.A3, note.C4, note.E4], [note.F3, note.A3, note.C4], [note.C3, note.E3, note.G3], [note.G3, note.B3, note.D4]],
  [note.E4, note.G4, note.A4, note.G4, note.E4, note.D4, note.C4, note.E4, note.A4, note.G4, note.E4, note.D4, note.C4, note.D4, note.E4, note.G4],
  24);

theme("game-theme.wav", 96,
  [[note.D3, note.F3, note.A3], [note.B3, note.D4, note.F4], [note.G3, note.B3, note.D4], [note.A3, note.C4, note.E4]],
  [note.F4, note.A4, note.G4, note.F4, note.D4, note.F4, note.A4, note.C5, note.B4, note.A4, note.G4, note.F4, note.E4, note.F4, note.D4, note.A3],
  20);

function flourish(name, sequence, seconds = 0.9) {
  writeWav(name, seconds, (time) => {
    const stepDuration = seconds / sequence.length;
    const step = Math.min(sequence.length - 1, Math.floor(time / stepDuration));
    const start = step * stepDuration;
    const fade = Math.max(0, 1 - Math.max(0, time - seconds + 0.16) / 0.16);
    return fade * (tone(time, start, stepDuration, sequence[step], 0.25, "triangle") + tone(time, start, stepDuration, sequence[step] * 2, 0.055));
  });
}

flourish("reveal-all.wav", [note.C4, note.E4, note.G4, note.C5]);
flourish("reveal-some.wav", [note.A3, note.C4, note.E4, note.G4]);
flourish("reveal-none.wav", [note.E4, note.D4, note.C4, note.A3]);
flourish("screen-transition.wav", [note.C4, note.E4, note.G4], 0.42);
