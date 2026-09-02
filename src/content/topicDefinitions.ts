import taxonomyManifest from "./taxonomy-manifest.json";

export const TOPIC_DEFINITIONS: readonly (readonly [string, string])[] =
  taxonomyManifest.topics.map(({ id, title }) => [id, title] as const);

export const TOPIC_TITLE_BY_ID = Object.fromEntries(TOPIC_DEFINITIONS) as Readonly<
  Record<string, string>
>;
