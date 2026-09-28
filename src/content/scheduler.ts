import { nextRandom, seedRandom, shuffle, type RandomState } from "./random";
import type { Difficulty, TopicPack } from "./types";
import { topicGroupLimit, type TopicChoiceKind } from "./topicDiversity";

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
  domainForTopic: (topicId: string) => string = (topicId) => topicId,
  kind: TopicChoiceKind = count === 3 ? "normal" : "bonus"
): {
  readonly topicIds: readonly string[];
  readonly reusedTopicIds: readonly string[];
  readonly random: RandomState;
  readonly matchHistory: MatchTopicHistory;
} {
  const cap = topicGroupLimit(kind, count);
  const selected = new Set(matchHistory.selected);
  let state = random;
  const ranked = topics.map((topic) => {
    const [tie, nextState] = nextRandom(state);
    state = nextState;
    const domain = domainForTopic(topic.id);
    if (!domain) throw new Error(`Для темы ${topic.id} не задана область`);
    return { id: topic.id, domain, reused: selected.has(topic.id) ? 1 : 0, penalty: matchHistory.shownCounts[topic.id] ?? 0, tie };
  });
  if (new Set(ranked.map(({ id }) => id)).size !== ranked.length) throw new Error("Повтор идентификатора темы");
  type Candidate = (typeof ranked)[number];
  interface Plan { topics: readonly Candidate[]; reused: number; groups: number; penalty: number; tie: number }
  const groups = new Map<string, Candidate[]>();
  for (const candidate of ranked) {
    const group = groups.get(candidate.domain) ?? [];
    group.push(candidate);
    groups.set(candidate.domain, group);
  }
  const better = (left: Plan, right: Plan | undefined) => !right ||
    left.reused < right.reused || left.reused === right.reused && (
      left.groups > right.groups || left.groups === right.groups && (
        left.penalty < right.penalty || left.penalty === right.penalty && left.tie < right.tie
      )
    );
  // One DP layer per group: every retained plan has respected the group cap.
  // Additive priorities let us keep only the best plan for each cardinality.
  let plans: (Plan | undefined)[] = [{ topics: [], reused: 0, groups: 0, penalty: 0, tie: 0 }];
  for (const group of groups.values()) {
    const options: Candidate[][] = [[], ...group.map((candidate) => [candidate])];
    if (cap === 2) {
      for (let a = 0; a < group.length; a += 1) {
        for (let b = a + 1; b < group.length; b += 1) options.push([group[a], group[b]]);
      }
    }
    const next: (Plan | undefined)[] = [];
    for (const plan of plans) {
      if (!plan) continue;
      for (const option of options) {
        const size = plan.topics.length + option.length;
        if (size > count) continue;
        const candidate: Plan = {
          topics: [...plan.topics, ...option],
          reused: plan.reused + option.reduce((sum, item) => sum + item.reused, 0),
          groups: plan.groups + (option.length > 0 ? 1 : 0),
          penalty: plan.penalty + option.reduce((sum, item) => sum + item.penalty, 0),
          tie: plan.tie + option.reduce((sum, item) => sum + item.tie, 0)
        };
        if (better(candidate, next[size])) next[size] = candidate;
      }
    }
    plans = next;
  }
  const plan = plans[count];
  if (!plan) throw new Error(`Недостаточно допустимых групп тем: требуется ${count}, лимит ${cap}`);
  const topicIds = [...plan.topics].sort((left, right) => left.tie - right.tie).map(({ id }) => id);
  const reusedTopicIds = topicIds.filter((id) => selected.has(id));
  const shownCounts = { ...matchHistory.shownCounts };
  for (const id of topicIds) shownCounts[id] = (shownCounts[id] ?? 0) + 1;
  return { topicIds, reusedTopicIds, random: state, matchHistory: { ...matchHistory, shownCounts } };
}

export { seedRandom };
