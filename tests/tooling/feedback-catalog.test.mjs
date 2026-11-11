import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import { readFeedbackCatalog } from '../../server/feedbackCatalog.mjs';

const root = fileURLToPath(new URL('../../', import.meta.url));

function run(script, args, input) {
  return spawnSync(process.execPath, [script, ...args], { cwd: root, input, encoding: 'utf8' });
}

test('catalog preflight accepts an identical manifest and rejects a reused revision with changed difficulty', async () => {
  const { catalogRevision, questions } = await readFeedbackCatalog();
  const [questionId, difficulty] = questions.entries().next().value;
  const registry = { [catalogRevision]: Object.fromEntries([...questions].reverse()) };
  const check = () => run('scripts/checkFeedbackCatalog.mjs', ['--registry-stdin'], JSON.stringify(registry));
  const unchanged = check();
  assert.equal(unchanged.status, 0, unchanged.stderr);
  assert.match(unchanged.stdout, /Feedback catalog compatible:/);

  registry[catalogRevision][questionId] = difficulty === 'easy' ? 'hard' : 'easy';
  const conflict = check();
  assert.equal(conflict.status, 1);
  assert.ok(conflict.stderr.includes(`Conflicting feedback catalog manifest: ${catalogRevision}`));
});

test('the report CLI counts feedback from the checked-out catalog and keeps older events historical', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'mindbattle-feedback-report-'));
  try {
    const { catalogRevision, questions } = await readFeedbackCatalog();
    const [questionId, assignedDifficulty] = questions.entries().next().value;
    const current = {
      schemaVersion: 3, eventId: 'current', matchId: 'match', catalogRevision, questionId,
      assignedDifficulty, hasComplaint: true, complaintReasons: ['too-hard'], complaintNote: 'private note'
    };
    const historical = { ...current, eventId: 'historical', catalogRevision: 'test-old-revision' };
    const journal = join(directory, 'feedback.ndjson');
    const contents = [current, historical].map(event => JSON.stringify(event)).join('\n');
    await writeFile(journal, contents);

    const result = run('scripts/generateProductionFeedbackReport.mjs', [journal]);
    assert.equal(result.status, 0, result.stderr);
    const report = JSON.parse(result.stdout);
    assert.equal(report.catalogRevision, catalogRevision);
    assert.equal(report.totals.total, 1);
    assert.equal(report.byQuestion[questionId].complaints, 1);
    assert.equal(report.diagnostics.historicalEvents, 1);
    assert.ok(!result.stdout.includes(current.complaintNote));
    assert.equal(await readFile(journal, 'utf8'), contents);
  } finally {
    await rm(directory, { recursive: true });
  }
});
