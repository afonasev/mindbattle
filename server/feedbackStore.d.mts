export interface FeedbackStoreOptions {
  filePath: string;
  questions: ReadonlyMap<string, string>;
  catalogRevision: string;
}

export function validateFeedbackEvent(
  value: unknown,
  questions: ReadonlyMap<string, string>,
  catalogRevision: string
): string | null;

export function createFeedbackStore(options: FeedbackStoreOptions): Promise<{
  filePath: string;
  append(event: Record<string, unknown>): Promise<{ status: "created" | "duplicate" | "invalid" | "conflict"; error?: string }>;
  summary(): any;
}>;
