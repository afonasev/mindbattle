export interface RandomState {
  readonly value: number;
}

const NON_ZERO_FALLBACK = 0x6d2b79f5;

export function seedRandom(seed: string): RandomState {
  let value = 0x811c9dc5;
  for (let index = 0; index < seed.length; index += 1) {
    value ^= seed.charCodeAt(index);
    value = Math.imul(value, 0x01000193);
  }
  return { value: value >>> 0 || NON_ZERO_FALLBACK };
}

export function nextUint32(state: RandomState): readonly [number, RandomState] {
  let value = state.value | 0;
  value ^= value << 13;
  value ^= value >>> 17;
  value ^= value << 5;
  const unsigned = value >>> 0 || NON_ZERO_FALLBACK;
  return [unsigned, { value: unsigned }];
}

export function nextInt(
  state: RandomState,
  exclusiveMax: number
): readonly [number, RandomState] {
  if (!Number.isSafeInteger(exclusiveMax) || exclusiveMax <= 0) {
    throw new RangeError("exclusiveMax must be a positive safe integer");
  }
  const [value, nextState] = nextUint32(state);
  return [value % exclusiveMax, nextState];
}

export function shuffle<T>(
  values: readonly T[],
  initialState: RandomState
): readonly [readonly T[], RandomState] {
  const shuffled = [...values];
  let state = initialState;
  for (let index = shuffled.length - 1; index > 0; index -= 1) {
    const [other, nextState] = nextInt(state, index + 1);
    state = nextState;
    [shuffled[index], shuffled[other]] = [shuffled[other], shuffled[index]];
  }
  return [shuffled, state];
}
