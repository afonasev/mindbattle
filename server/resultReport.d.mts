import type { ResultEvent } from '../src/statistics/events';
export function readResults(path: string): Promise<{ events: ResultEvent[]; corruptLines: number }>;
export function resultReport(events: ResultEvent[]): { questions: { mode: string; questionId: string; observations: number; correctRate: number | null; noSelectionObservations: number }[]; hundredPercent: unknown[]; zeroPercent: unknown[]; noSelection: unknown[]; matches: ResultEvent[] };

export function interruptedNetworkCheckpoints(events: ResultEvent[]): ResultEvent[];
