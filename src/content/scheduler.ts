import { nextRandom, seedRandom, shuffle, type RandomState } from "./random";
import type { Difficulty, TopicPack } from "./types";

export interface BagHistory {
  readonly cycle: number;
  readonly remaining: readonly string[];
  readonly previousOrder: readonly string[];
  readonly lastShownId: string | null;
  readonly shownCount: Readonly<Record<string, number>>;
  readonly lastShownSerial: Readonly<Record<string, number>>;
}

export interface QuestionHistory {
  readonly version: 1;
  readonly serial: number;
  readonly bags: Readonly<Record<string, BagHistory>>;
}

export interface MatchTopicHistory {
  readonly selected: readonly string[];
  readonly shownCounts: Readonly<Record<string, number>>;
}

export const EMPTY_QUESTION_HISTORY: QuestionHistory = {
  version: 1,
  serial: 0,
  bags: {}
};

export function migrateQuestionHistory(
  topics: readonly TopicPack[],
  history: QuestionHistory
): QuestionHistory {
  const shownCount: Record<string, number> = {};
  const lastShownSerial: Record<string, number> = {};
  for (const bag of Object.values(history.bags)) {
    for (const [id, count] of Object.entries(bag.shownCount)) {
      shownCount[id] = Math.max(shownCount[id] ?? 0, count);
    }
    for (const [id, serial] of Object.entries(bag.lastShownSerial)) {
      lastShownSerial[id] = Math.max(lastShownSerial[id] ?? 0, serial);
    }
  }

  const bags: Record<string, BagHistory> = {};
  for (const topic of topics) {
    for (const difficulty of ["easy", "medium", "hard"] as const) {
      const ids = topic.questions
        .filter((question) => question.difficulty === difficulty)
        .map((question) => question.id);
      const counts = Object.fromEntries(ids.filter((id) => shownCount[id]).map((id) => [id, shownCount[id]]));
      const serials = Object.fromEntries(ids.filter((id) => lastShownSerial[id]).map((id) => [id, lastShownSerial[id]]));
      if (Object.keys(counts).length === 0) continue;
      const lastShownId = ids.reduce<string | null>(
        (latest, id) =>
          latest === null || (lastShownSerial[id] ?? 0) > (lastShownSerial[latest] ?? 0)
            ? id
            : latest,
        null
      );
      bags[`${topic.id}:${difficulty}`] = {
        cycle: 0,
        remaining: [],
        previousOrder: [],
        lastShownId,
        shownCount: counts,
        lastShownSerial: serials
      };
    }
  }
  return { version: 1, serial: history.serial, bags };
}

function sameOrder(left: readonly string[], right: readonly string[]): boolean {
  return left.length === right.length && left.every((value, index) => value === right[index]);
}

function prioritize(
  ids: readonly string[],
  previous: BagHistory | undefined,
  random: RandomState
): readonly [readonly string[], RandomState] {
  const unseen = ids.filter((id) => (previous?.shownCount[id] ?? 0) === 0);
  const seen = ids.filter((id) => !unseen.includes(id));
  let [unseenOrder, state] = shuffle(unseen, random);
  const pool = [...seen].sort((left, right) => {
    const count = (previous?.shownCount[left] ?? 0) - (previous?.shownCount[right] ?? 0);
    if (count !== 0) return count;
    return (previous?.lastShownSerial[left] ?? 0) - (previous?.lastShownSerial[right] ?? 0);
  });
  const seenOrder: string[] = [];
  while (pool.length > 0) {
    const [value, nextState] = nextRandom(state);
    state = nextState;
    const window = Math.min(4, pool.length);
    seenOrder.push(...pool.splice(Math.floor(value * window), 1));
  }
  let order = [...unseenOrder, ...seenOrder];
  if (order.length > 1 && previous?.lastShownId === order[0]) {
    order = [...order.slice(1), order[0]];
  }
  if (order.length > 1 && previous && sameOrder(order, previous.previousOrder)) {
    order = [order[1], order[0], ...order.slice(2)];
    if (previous.lastShownId === order[0]) order = [...order.slice(1), order[0]];
  }
  return [order, state];
}

export function drawQuestion(
  topic: TopicPack,
  difficulty: Difficulty,
  history: QuestionHistory,
  random: RandomState,
  excludedIds: ReadonlySet<string> = new Set()
): {
  readonly questionId: string;
  readonly history: QuestionHistory;
  readonly random: RandomState;
} {
  const ids = topic.questions
    .filter((question) => question.difficulty === difficulty)
    .map((question) => question.id);
  const key = `${topic.id}:${difficulty}`;
  let bag = history.bags[key];
  let state = random;
  let remaining: readonly string[] = bag?.remaining.filter((id) => ids.includes(id)) ?? [];

  if (remaining.length === 0) {
    [remaining, state] = prioritize(ids, bag, state);
    bag = {
      cycle: (bag?.cycle ?? -1) + 1,
      remaining,
      previousOrder: remaining,
      lastShownId: bag?.lastShownId ?? null,
      shownCount: bag?.shownCount ?? {},
      lastShownSerial: bag?.lastShownSerial ?? {}
    };
  }

  const questionId = remaining.find((id) => !excludedIds.has(id));
  if (!questionId) throw new Error(`Нет доступных вопросов для ${key}`);
  const serial = history.serial + 1;
  const nextBag: BagHistory = {
    ...bag,
    remaining: remaining.filter((id) => id !== questionId),
    lastShownId: questionId,
    shownCount: {
      ...bag.shownCount,
      [questionId]: (bag.shownCount[questionId] ?? 0) + 1
    },
    lastShownSerial: { ...bag.lastShownSerial, [questionId]: serial }
  };
  return {
    questionId,
    random: state,
    history: {
      version: 1,
      serial,
      bags: { ...history.bags, [key]: nextBag }
    }
  };
}

export function chooseTopicCandidates(
  topics: readonly TopicPack[],
  count: number,
  matchHistory: MatchTopicHistory,
  random: RandomState,
  domainForTopic: (topicId: string) => string = (topicId) => topicId
): {
  readonly topicIds: readonly string[];
  readonly random: RandomState;
  readonly matchHistory: MatchTopicHistory;
} {
  const selected = new Set(matchHistory.selected);
  const candidates = topics.filter((topic) => !selected.has(topic.id));
  if (candidates.length < count) throw new Error(`Недостаточно тем: требуется ${count}`);

  let state = random;
  const ranked = candidates.map((topic) => {
    const [tie, nextState] = nextRandom(state);
    state = nextState;
    const domain = domainForTopic(topic.id);
    if (!domain) throw new Error(`Для темы ${topic.id} не задана область`);
    return { id: topic.id, domain, penalty: matchHistory.shownCounts[topic.id] ?? 0, tie };
  });
  const topicIds: string[] = [];
  const selectedDomains = new Set<string>();
  const remaining = [...ranked];
  while (topicIds.length < count) {
    const unseenDomainCandidates = remaining.filter(({ domain }) => !selectedDomains.has(domain));
    const pool = unseenDomainCandidates.length > 0 ? unseenDomainCandidates : remaining;
    pool.sort((left, right) => left.penalty - right.penalty || left.tie - right.tie);
    const next = pool[0];
    topicIds.push(next.id);
    selectedDomains.add(next.domain);
    remaining.splice(remaining.indexOf(next), 1);
  }
  const shownCounts = { ...matchHistory.shownCounts };
  for (const id of topicIds) shownCounts[id] = (shownCounts[id] ?? 0) + 1;
  return {
    topicIds,
    random: state,
    matchHistory: { ...matchHistory, shownCounts }
  };
}

export { seedRandom };
