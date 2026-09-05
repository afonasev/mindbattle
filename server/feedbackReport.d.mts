export interface ProductionFeedbackReport {
  readonly schemaVersion: 1;
  readonly catalogRevision: string;
  readonly totals: { readonly total: number; readonly complaints: number; readonly noComplaints: number; readonly complaintRate: number; readonly reasons: Record<string, number> };
  readonly byQuestion: Record<string, { readonly total: number; readonly complaints: number; readonly noComplaints: number; readonly complaintRate: number; readonly reasons: Record<string, number> }>;
  readonly byAssignedDifficulty: Record<string, { readonly total: number; readonly complaints: number; readonly noComplaints: number; readonly complaintRate: number; readonly reasons: Record<string, number> }>;
  readonly diagnostics: { readonly invalidLines: number; readonly historicalEvents: number; readonly duplicateEventIds: readonly string[]; readonly unknownQuestionIds: readonly string[]; readonly catalogRevisions: Record<string, number> };
}

export function analyzeProductionFeedback(source: string, options: { questions?: ReadonlyMap<string, string>; catalogRevision: string }): ProductionFeedbackReport;
