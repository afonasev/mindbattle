export interface RandomState {
  readonly value: number;
}

export function seedRandom(seed: string): RandomState {
  let value = 0x811c9dc5;
  for (let index = 0; index < seed.length; index += 1) {
    value ^= seed.charCodeAt(index);
    value = Math.imul(value, 0x01000193);
  }
  return { value: value >>> 0 || 0x6d2b79f5 };
}

export function nextRandom(state: RandomState): readonly [number, RandomState] {
  let value = state.value | 0;
  value ^= value << 13;
  value ^= value >>> 17;
  value ^= value << 5;
  const unsigned = value >>> 0;
  return [unsigned / 0x1_0000_0000, { value: unsigned || 0x6d2b79f5 }];
}

export function shuffle<T>(
  values: readonly T[],
  initialState: RandomState
): readonly [readonly T[], RandomState] {
  const result = [...values];
  let state = initialState;
  for (let index = result.length - 1; index > 0; index -= 1) {
    const [value, nextState] = nextRandom(state);
    state = nextState;
    const other = Math.floor(value * (index + 1));
    [result[index], result[other]] = [result[other], result[index]];
  }
  return [result, state];
}
