import { validateResult } from './resultStore.mjs';
import { readFile } from 'node:fs/promises';
export async function readResults(path) {
  const events = new Map(); let corruptLines = 0;
  const source = await readFile(path, 'utf8');
  for (const line of source.split('\n').filter(Boolean)) {
    try { const e = JSON.parse(line); if (!validateResult(e)) throw Error(); if (!events.has(e.eventId)) events.set(e.eventId, e); }
    catch { corruptLines++; }
  }
  return { events: [...events.values()], corruptLines };
}
export function resultReport(events) {
  const groups = new Map(), matches = new Map(), totals = new Map(), seen = new Set();
  for (const e of events) {
    if (seen.has(e.eventId)) continue;
    seen.add(e.eventId);
    if (e.kind === 'match') {
      const previous = matches.get(e.matchId);
      if (!previous || (previous.status === 'in-progress' && (e.status !== 'in-progress' || e.ordinal >= previous.ordinal))) matches.set(e.matchId, e);
      continue;
    }
    if (e.kind !== 'question') continue;
    const t = totals.get(e.matchId) ?? { observedQuestions: 0, eligible: 0, correct: 0, wrong: 0, noAnswer: 0, timeout: 0 };
    t.observedQuestions++;
    for (const k of ['eligible', 'correct', 'wrong', 'noAnswer', 'timeout']) t[k] += e[k];
    totals.set(e.matchId, t);
    const key = JSON.stringify([e.mode, e.catalogRevision, e.questionId, e.questionVersion]);
    const g = groups.get(key) ?? { mode: e.mode, catalogRevision: e.catalogRevision, questionId: e.questionId, questionVersion: e.questionVersion, observations: 0, eligible: 0, correct: 0, wrong: 0, noAnswer: 0, timeout: 0, allCorrectObservations: 0, noneCorrectObservations: 0, noSelectionObservations: 0, zeroEligibleObservations: 0, choices: {} };
    g.observations++;
    for (const k of ['eligible', 'correct', 'wrong', 'noAnswer', 'timeout']) g[k] += e[k];
    if (e.eligible > 0) {
      g.allCorrectObservations += +(e.correct === e.eligible);
      g.noneCorrectObservations += +(e.correct === 0);
      g.noSelectionObservations += +(e.correct + e.wrong === 0);
    } else g.zeroEligibleObservations++;
    for (const [id, n] of Object.entries(e.choices)) g.choices[id] = (g.choices[id] ?? 0) + n;
    groups.set(key, g);
  }
  const questions = [...groups.values()].map(g => ({ ...g, correctRate: g.eligible ? g.correct / g.eligible : null })).sort((a, b) => a.mode.localeCompare(b.mode) || a.questionId.localeCompare(b.questionId));
  return { questions, hundredPercent: questions.filter(g => g.correctRate === 1), zeroPercent: questions.filter(g => g.correctRate === 0), noSelection: questions.filter(g => g.noSelectionObservations > 0), matches: [...matches.values()].map(e => ({ ...e, observed: totals.get(e.matchId) ?? null })) };
}

export function interruptedNetworkCheckpoints(events) {
  return resultReport(events).matches.filter(e => e.mode === 'network-v1' && e.status === 'in-progress').map(({ observed: _observed, ...e }) => ({ ...e, eventId: `${e.matchId}:match:end`, status: 'interrupted', reason: 'server-restart' }));
}
