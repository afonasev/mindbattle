import type { DifficultyFeedbackEvent } from './types';

/** Exact payloads are retained: changing whitespace would conflict after a lost ACK. */
export function legacySnapshotFeedback(source: string | null): DifficultyFeedbackEvent[] {
  try {
    const data = JSON.parse(source ?? 'null');
    const pending: DifficultyFeedbackEvent[] = Array.isArray(data?.pendingFeedback)
      ? data.pendingFeedback.filter((event: any) => event && typeof event.eventId === 'string') : [];
    const state = data?.lastMatch?.state;
    const phase = state?.phase;
    if (phase?.kind === 'difficulty-feedback' && phase.stage === 'done' && phase.hasComplaint === true &&
        typeof phase.eventId === 'string' && typeof state.matchId === 'string' && typeof state.catalogRevision === 'string' &&
        typeof phase.round?.questionId === 'string' && ['easy', 'medium', 'hard'].includes(phase.round?.difficulty) &&
        Array.isArray(phase.complaintReasons) && (phase.complaintReasons.length || phase.complaintNote?.trim())) {
      const event: DifficultyFeedbackEvent = { schemaVersion: 3, eventId: phase.eventId, matchId: state.matchId,
        catalogRevision: state.catalogRevision, questionId: phase.round.questionId, assignedDifficulty: phase.round.difficulty,
        hasComplaint: true, complaintReasons: phase.complaintReasons,
        ...(phase.complaintNote ? { complaintNote: phase.complaintNote } : {}) };
      if (!pending.some(item => item.eventId === event.eventId)) pending.push(event);
    }
    return pending;
  } catch { return []; }
}
