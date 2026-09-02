import type { Difficulty, TopicPack } from "./types";

export type TopicTargetSize = 100 | 200 | 300;

export interface DifficultyQuota {
  readonly easy: number;
  readonly medium: number;
  readonly hard: number;
}

export interface TopicTaxonomyEntry {
  readonly id: string;
  readonly title: string;
  readonly scope: string;
  readonly antiOverlap: string;
  readonly sourceStrategy: string;
  readonly sourceInventory: readonly string[];
  readonly capacityEvidence: {
    readonly independentFacts: number;
    readonly easyCandidates: number;
  };
  readonly targetSize: TopicTargetSize;
  readonly quota: DifficultyQuota;
}

export interface TaxonomyManifest {
  readonly revision: string;
  readonly topics: readonly TopicTaxonomyEntry[];
}

export const QUOTA_BY_TARGET_SIZE: Readonly<Record<TopicTargetSize, DifficultyQuota>> = {
  100: { easy: 40, medium: 40, hard: 20 },
  200: { easy: 80, medium: 80, hard: 40 },
  300: { easy: 120, medium: 120, hard: 60 }
};

const ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const difficulties: readonly Difficulty[] = ["easy", "medium", "hard"];

export class TaxonomyValidationError extends Error {
  constructor(readonly issues: readonly string[]) {
    super(issues.join("\n"));
    this.name = "TaxonomyValidationError";
  }
}

export function quotaForTopicSize(size: number): DifficultyQuota | undefined {
  return QUOTA_BY_TARGET_SIZE[size as TopicTargetSize];
}

export function validateTaxonomyManifest(
  manifest: TaxonomyManifest,
  packs?: readonly TopicPack[]
): TaxonomyManifest {
  const issues: string[] = [];
  if (!manifest.revision.trim()) issues.push("taxonomy: пустая revision");
  if (manifest.topics.length !== 110) {
    issues.push(`taxonomy: ожидалось 110 тем, получено ${manifest.topics.length}`);
  }
  const ids = new Set<string>();
  const titles = new Set<string>();
  for (const entry of manifest.topics) {
    if (!ID.test(entry.id)) issues.push(`${entry.id || "<topic>"}: некорректный topic id`);
    if (ids.has(entry.id)) issues.push(`${entry.id}: повтор topic id`);
    ids.add(entry.id);
    const titleKey = entry.title.trim().toLocaleLowerCase("ru");
    if (!titleKey) issues.push(`${entry.id}: пустое название темы`);
    if (titles.has(titleKey)) issues.push(`${entry.id}: повтор названия темы`);
    titles.add(titleKey);
    if (!entry.scope.trim()) issues.push(`${entry.id}: пустой scope`);
    if (!entry.antiOverlap.trim()) issues.push(`${entry.id}: пустой antiOverlap`);
    if (!entry.sourceStrategy.trim()) issues.push(`${entry.id}: пустой sourceStrategy`);
    if (entry.sourceInventory.length < 2) {
      issues.push(`${entry.id}: sourceInventory должен содержать минимум 2 источника`);
    }
    for (const source of entry.sourceInventory) {
      if (!/^https:\/\//u.test(source)) issues.push(`${entry.id}: sourceInventory требует HTTPS URL`);
    }
    if (entry.capacityEvidence.independentFacts < 100) {
      issues.push(`${entry.id}: подтверждено меньше 100 независимых фактов`);
    }
    if (entry.capacityEvidence.easyCandidates < 40) {
      issues.push(`${entry.id}: подтверждено меньше 40 easy-кандидатов`);
    }
    const expected = quotaForTopicSize(entry.targetSize);
    if (!expected) {
      issues.push(`${entry.id}: недопустимый targetSize ${entry.targetSize}`);
    } else {
      for (const difficulty of difficulties) {
        if (entry.quota[difficulty] !== expected[difficulty]) {
          issues.push(
            `${entry.id}: ${difficulty} должно быть ${expected[difficulty]}, получено ${entry.quota[difficulty]}`
          );
        }
      }
    }
  }

  if (packs) {
    const packsById = new Map(packs.map((pack) => [pack.id, pack]));
    for (const entry of manifest.topics) {
      const pack = packsById.get(entry.id);
      if (!pack) {
        issues.push(`${entry.id}: отсутствует topic pack`);
        continue;
      }
      if (pack.title !== entry.title) issues.push(`${entry.id}: название pack не совпадает с taxonomy`);
      if (pack.questions.length !== entry.targetSize) {
        issues.push(
          `${entry.id}: ожидалось ${entry.targetSize} вопросов, получено ${pack.questions.length}`
        );
      }
      for (const difficulty of difficulties) {
        const count = pack.questions.filter((question) => question.difficulty === difficulty).length;
        if (count !== entry.quota[difficulty]) {
          issues.push(
            `${entry.id}: pack ${difficulty} должно быть ${entry.quota[difficulty]}, получено ${count}`
          );
        }
      }
    }
    for (const pack of packs) {
      if (!ids.has(pack.id)) issues.push(`${pack.id}: topic pack отсутствует в taxonomy`);
    }
  }

  if (issues.length) throw new TaxonomyValidationError(issues);
  return manifest;
}
