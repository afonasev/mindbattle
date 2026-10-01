import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { scopes } from '../../scripts/qaScope.mjs';
import { verifyVitest, verifyBrowser, verifyNodeTap, verifyUnittest } from '../../scripts/qaReports.mjs';
const unit = () => ({ success: true, numTotalTests: 1, numPassedTests: 1, numFailedTests: 0, numPendingTests: 0, numTodoTests: 0, numFailedTestSuites: 0,
  testResults: [{ name: '/project/test.ts', assertionResults: [{ status: 'passed' }] }] });
const scope = { browser: [['smoke.spec.ts', '^smoke$']] };
const browser = () => ({ errors: [], stats: { expected: 1, unexpected: 0, flaky: 0, skipped: 0, duration: 3 }, suites: [{ specs: [{ file: 'smoke.spec.ts', title: 'smoke', tests: [{ projectName: 'chromium-1280', expectedStatus: 'passed', status: 'expected', results: [{ status: 'passed' }] }] }] }] });
test('valid executed reports include counts', () => {
  assert.equal(verifyVitest(unit(), ['test.ts']).passed, 1);
  assert.equal(verifyBrowser(browser(), scope, ['chromium-1280']).passed, 1);
});
for (const [name, patch] of Object.entries({ empty: { numTotalTests: 0 }, failed: { success: false }, skipped: { numPendingTests: 1 }, todo: { numTodoTests: 1 }, counterMismatch: { numPassedTests: 2 }, failedSuite: { numFailedTestSuites: 1 }, missingAssertions: { testResults: [] } })) {
  test(`unit rejects ${name}`, () => assert.throws(() => verifyVitest({ ...unit(), ...patch }, ['test.ts'])));
}
test('unit rejects missing selected files and failed assertions', () => {
  assert.throws(() => verifyVitest(unit(), ['missing.ts']));
  const r = unit(); r.testResults[0].assertionResults[0].status = 'failed';
  assert.throws(() => verifyVitest(r, ['test.ts']));
});
for (const name of ['empty', 'errors', 'skipped', 'flaky', 'failed', 'noResult', 'retries', 'counterMismatch', 'missingSelector', 'missingProject', 'unexpectedSelection']) {
  test(`browser rejects ${name}`, () => {
    const r = browser(), t = r.suites[0].specs[0].tests[0];
    if (name === 'empty') r.suites = [];
    if (name === 'errors') r.errors.push({ message: 'host failed' });
    if (name === 'skipped') { t.status = 'skipped'; r.stats.skipped = 1; }
    if (name === 'flaky') r.stats.flaky = 1;
    if (name === 'failed') t.results[0].status = 'failed';
    if (name === 'noResult') t.results = [];
    if (name === 'retries') t.results.push({ status: 'passed' });
    if (name === 'counterMismatch') r.stats.expected = 2;
    if (name === 'missingSelector') r.suites[0].specs[0].title = 'renamed';
    if (name === 'missingProject') t.projectName = 'other';
    if (name === 'unexpectedSelection') r.suites[0].specs.push({ file: 'other.spec.ts', title: 'other', tests: [] });
    assert.throws(() => verifyBrowser(r, scope, ['chromium-1280']));
  });
}
test('full rejects arbitrary skips, expected failures, and all-skipped reports', () => {
  const r = browser(); r.suites[0].specs[0].tests[0].status = 'skipped'; r.suites[0].specs[0].tests[0].results = [{ status: 'skipped' }];
  r.stats.expected = 0; r.stats.skipped = 1;
  assert.throws(() => verifyBrowser(r, scopes.full));
  const failed = browser(); failed.suites[0].specs[0].tests[0].expectedStatus = 'failed';
  assert.throws(() => verifyBrowser(failed, scopes.full));
});
test('CLI rejects unknown scope and arguments before running checks', () => {
  for (const args of [['--scope', 'unknown'], ['--scope'], ['--typo']]) {
    const result = spawnSync(process.execPath, ['scripts/qa.mjs', ...args], { encoding: 'utf8' });
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /Unknown/);
  }
});
test('focused UI and input preserve meaningful separated contracts', () => {
  assert.ok(scopes.ui.browser.some(([file]) => file === 'phone-reveal.spec.ts'));
  assert.ok(scopes.ui.browser.some(([file, title]) => file === 'qa-display.spec.ts' && title.includes('display')));
  assert.ok(scopes.network.browser.some(([, title]) => title.includes('12 phones')));
  assert.deepEqual(scopes.input.projects, ['chromium-1280']);
  assert.equal(scopes.full.units, null);
});

test('TAP evidence rejects empty, missing, failed and skipped contracts', () => {
  const tap = '# tests 23\n# pass 23\n# fail 0\n# cancelled 0\n# skipped 0\n# todo 0\n';
  assert.equal(verifyNodeTap(tap).passed, 23);
  for (const bad of ['', tap.replace('tests 23', 'tests 0'), tap.replace('pass 23', 'pass 22'), tap.replace('fail 0', 'fail 1'), tap.replace('skipped 0', 'skipped 1')]) assert.throws(() => verifyNodeTap(bad));
});

test('check and standalone build both enforce types exactly once', () => {
  const scripts = JSON.parse(readFileSync('package.json', 'utf8')).scripts;
  const expand = name => scripts[name].replace(/npm run ([\w:-]+)/g, (_, child) => expand(child));
  for (const route of ['check', 'build']) {
    const command = expand(route);
    assert.equal((command.match(/tsc --noEmit/g) ?? []).length, 1);
    assert.equal((command.match(/vite build/g) ?? []).length, 2);
  }
});

test('Python unittest evidence must include executed passing tests', () => {
  assert.equal(verifyUnittest('Ran 3 tests in 0.01s\n\nOK\n').passed, 3);
  for (const log of ['', 'Ran 0 tests in 0.00s\nOK', 'Ran 3 tests in 0.01s\nFAILED (errors=1)', 'Ran 3 tests in 0.01s\nOK (skipped=1)']) assert.throws(() => verifyUnittest(log));
});
