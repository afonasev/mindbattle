import type { DomainContext, MatchState, AnswerPosition } from '../domain/types';
import { ANSWER_POSITIONS } from '../domain/types';
import type { SoloState } from '../domain/solo';
export type Mode = 'solo-endless-v1' | 'classic-v1' | 'network-v1';
export interface ResultEvent {
  schemaVersion: 1; eventId: string; matchId: string; mode: Mode; catalogRevision: string;
  kind: 'question' | 'match'; ordinal: number;
  questionId?: string; questionVersion?: string; assignedDifficulty?: string;
  roundKind?: 'normal' | 'bonus' | 'tie-break';
  eligible?: number; correct?: number; wrong?: number; noAnswer?: number; timeout?: number;
  choices?: Record<string, number>;
  status?: 'in-progress' | 'completed' | 'interrupted'; reason?: string;
  units?: { id: string; score: number; correct: number; incorrect: number; noAnswer: number }[];
  score?: number; lives?: number; winnerId?: string;
}
export interface ResultSink { enqueue(event: ResultEvent): void }
// Content fingerprint of the complete domain question; not a cryptographic signature.
export function questionVersion(context: DomainContext, id: string): string {
  let hash = 14695981039346656037n;
  for (const byte of new TextEncoder().encode(JSON.stringify(context.getQuestion(id)))) {
    hash = BigInt.asUintN(64, (hash ^ BigInt(byte)) * 1099511628211n);
  }
  return `domain-v1-fnv64:${hash.toString(16).padStart(16, '0')}`;
}
export function metrics(e: ResultEvent) {
  const n = e.eligible ?? 0, c = e.correct ?? 0, w = e.wrong ?? 0;
  return { allCorrect: n > 0 && c === n, noneCorrect: n > 0 && c === 0,
    noSelection: n > 0 && c + w === 0, correctRate: n > 0 ? c / n : null };
}
export class ResultObserver {
  private seen = new Set<string>();
  constructor(private sink: ResultSink | undefined, private context: DomainContext) {}
  private emit(e: ResultEvent) {
    if (!this.sink || this.seen.has(e.eventId)) return;
    this.seen.add(e.eventId);
    try { this.sink.enqueue(e); } catch { /* diagnostics must never break play */ }
  }
  match(state: MatchState, interrupted?: string, starting = false) {
    try { this.captureMatch(state, interrupted, starting); } catch { /* isolated diagnostics */ }
  }
  private captureMatch(state: MatchState, interrupted?: string, starting: boolean = false) {
    const ordinal = state.tieBreak ? state.config.questionCount + state.tieBreak.questionNumber : state.mainQuestionIndex;
    const base = { schemaVersion: 1 as const, matchId: state.matchId, mode: state.config.profile, catalogRevision: state.catalogRevision, ordinal };
    const p = state.phase;
    if ((p.kind === 'reveal' || p.kind === 'difficulty-feedback') && !this.seen.has(`${state.matchId}:question:${ordinal}`)) {
      const units = p.resolutions.filter(r => r.result !== 'spectator');
      const choices: Record<string, number> = Object.fromEntries(p.round.answerOrder.map(id => [id, 0]));
      for (const u of units) if (u.answer) choices[p.round.answerOrder[ANSWER_POSITIONS.indexOf(u.answer)]]++;
      this.emit({ ...base, kind: 'question', eventId: `${state.matchId}:question:${ordinal}`,
        questionId: p.round.questionId, questionVersion: questionVersion(this.context, p.round.questionId),
        assignedDifficulty: p.round.difficulty, roundKind: p.round.mode === 'tie-break' ? 'tie-break' : p.round.points > ({ easy: 100, medium: 200, hard: 300 }[p.round.difficulty]) ? 'bonus' : 'normal',
        eligible: units.length, correct: units.filter(r => r.result === 'correct').length,
        wrong: units.filter(r => r.result === 'wrong').length, noAnswer: units.filter(r => r.result === 'no-answer').length,
        timeout: p.round.attempts.filter(a => a.status === 'timed-out' && units.some(u => u.teamId === a.teamId)).length, choices });
    }
    if (starting || interrupted || p.kind === 'finished' || p.kind === 'reveal') {
      const status = interrupted || state.endReason ? 'interrupted' : p.kind === 'finished' ? 'completed' : 'in-progress';
      this.emit({ ...base, kind: 'match', eventId: `${state.matchId}:match:${status === 'in-progress' ? starting ? 'start' : ordinal : 'end'}`, status,
        reason: interrupted ?? state.endReason ?? (status === 'completed' ? 'finished' : 'checkpoint'),
        units: state.teams.map(t => ({ id: t.id, score: t.score, correct: t.correct, incorrect: t.incorrect, noAnswer: t.noAnswer })),
        ...(p.kind === 'finished' ? { winnerId: p.winnerId } : {}) });
    }
  }
  solo(state: SoloState, interrupted?: string, starting = false) {
    try { this.captureSolo(state, interrupted, starting); } catch { /* isolated diagnostics */ }
  }
  private captureSolo(state: SoloState, interrupted?: string, starting: boolean = false) {
    const base = { schemaVersion: 1 as const, matchId: state.runId, mode: state.config.profile, catalogRevision: state.catalogRevision, ordinal: state.slotIndex };
    const p = state.phase;
    if (p.kind === 'reveal' && !this.seen.has(`${state.runId}:question:${state.slotIndex}`)) {
      const choices: Record<string, number> = Object.fromEntries(p.round.answerOrder.map(id => [id, 0]));
      if (p.answer) choices[p.round.answerOrder[ANSWER_POSITIONS.indexOf(p.answer as AnswerPosition)]]++;
      this.emit({ ...base, kind: 'question', eventId: `${state.runId}:question:${state.slotIndex}`, questionId: p.round.questionId,
        questionVersion: questionVersion(this.context, p.round.questionId), assignedDifficulty: p.round.difficulty,
        roundKind: p.round.risk ? 'bonus' : 'normal', eligible: 1, correct: +(p.result === 'correct'), wrong: +(p.result === 'wrong'),
        noAnswer: +(p.result === 'no-answer'), timeout: +(p.result === 'no-answer'), choices });
    }
    if (starting || interrupted || p.kind === 'finished' || p.kind === 'reveal') {
      const status = interrupted ? 'interrupted' : p.kind === 'finished' ? 'completed' : 'in-progress';
      this.emit({ ...base, kind: 'match', eventId: `${state.runId}:match:${status === 'in-progress' ? starting ? 'start' : state.slotIndex : 'end'}`,
        status, reason: interrupted ?? (status === 'completed' ? 'lives-exhausted' : 'checkpoint'), score: state.score, lives: state.lives });
    }
  }
}
