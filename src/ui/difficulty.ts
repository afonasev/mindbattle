import type { Difficulty } from "../domain";

const DIFFICULTY_LABELS: Readonly<Record<Difficulty, string>> = {
  easy: "Лёгкий",
  medium: "Средний",
  hard: "Сложный"
};

export function difficultyLabel(difficulty: Difficulty): string {
  return DIFFICULTY_LABELS[difficulty];
}
