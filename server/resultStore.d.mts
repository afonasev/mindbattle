import type { ResultEvent } from '../src/statistics/events';
export function validateResult(e: unknown, allowNetwork?: boolean): boolean;
export function createResultStore(filePath: string): Promise<{ append(e: ResultEvent): Promise<{ status: string; eventId: string }> }>;
export function createServerResultQueue(directory: string, append: (e: ResultEvent) => Promise<{ status: string; eventId: string }>): { enqueue(e: ResultEvent): void; disableMatch(matchId: string): Promise<void>; flush(): Promise<void>; stop(): void };
