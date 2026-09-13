import taxonomyManifest from "./taxonomy-manifest.json";
import type { TopicDomain } from "./taxonomy";

export const TOPIC_DEFINITIONS: readonly (readonly [string, string])[] =
  taxonomyManifest.topics.map(({ id, title }) => [id, title] as const);

export const TOPIC_TITLE_BY_ID = Object.fromEntries(TOPIC_DEFINITIONS) as Readonly<
  Record<string, string>
>;

export const TOPIC_DOMAIN_BY_ID = Object.fromEntries(
  taxonomyManifest.topics.map(({ id, domain }) => [id, domain] as const)
) as Readonly<Record<string, TopicDomain>>;
