import { TOPIC_DEFINITIONS } from "./topicDefinitions";
import { contentReviews } from "./reviews";
import type { ContentCatalog, TopicPack } from "./types";
import { validateCatalog } from "./validator";

const topicModules = import.meta.glob("./topics/*.json", {
  eager: true,
  import: "default"
}) as Readonly<Record<string, TopicPack>>;

const definitionOrder = new Map(
  TOPIC_DEFINITIONS.map(([id], index) => [id, index] as const)
);

export function buildCatalog(topics: readonly TopicPack[]): ContentCatalog {
  const ordered = [...topics].sort(
    (left, right) =>
      (definitionOrder.get(left.id as never) ?? Number.MAX_SAFE_INTEGER) -
      (definitionOrder.get(right.id as never) ?? Number.MAX_SAFE_INTEGER)
  );
  return {
    revision: "mindbattle-questions-2026-09-02-r3",
    topics: ordered
  };
}

export const catalog = buildCatalog(Object.values(topicModules));

export function assertFullCatalog(): ContentCatalog {
  return validateCatalog(catalog, contentReviews);
}
