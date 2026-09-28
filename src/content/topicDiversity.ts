export type TopicChoiceKind = "normal" | "bonus" | "final";

export const TOPIC_DIVERSITY_V1 = {
  id: "topic-diversity-v1",
  normal: { minCount: 3, maxCount: 3, maxPerGroup: 1 },
  final: { minCount: 3, maxCount: 5, maxPerGroup: 1 },
  bonus: { minCount: 3, maxCount: 5, smallCount: 3, smallMaxPerGroup: 1, largeMaxPerGroup: 2 }
} as const;

export function topicGroupLimit(kind: TopicChoiceKind, count: number): number {
  if (!["normal", "bonus", "final"].includes(kind)) throw new Error(`Недопустимый вид выбора тем: ${kind}`);
  const rule = TOPIC_DIVERSITY_V1[kind];
  if (!rule || !Number.isInteger(count) || count < rule.minCount || count > rule.maxCount) {
    throw new Error(`Недопустимый выбор тем: ${kind}/${count}`);
  }
  return kind === "bonus"
    ? count === TOPIC_DIVERSITY_V1.bonus.smallCount
      ? TOPIC_DIVERSITY_V1.bonus.smallMaxPerGroup
      : TOPIC_DIVERSITY_V1.bonus.largeMaxPerGroup
    : TOPIC_DIVERSITY_V1[kind].maxPerGroup;
}
