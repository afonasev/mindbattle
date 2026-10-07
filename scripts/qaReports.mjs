import { selectedSpec } from './qaScope.mjs';
const requireValue = (ok, message) => { if (!ok) throw new Error(message); };
export function verifyVitest(report, files) {
  requireValue(report.success === true && report.numTotalTests > 0, 'Unit report is failed or empty');
  const assertions = report.testResults?.flatMap(result => result.assertionResults) ?? [];
  requireValue(report.numFailedTests === 0 && report.numPendingTests === 0 && report.numTodoTests === 0 && report.numFailedTestSuites === 0,
    'Unit report has failed/skipped/todo tests or suites');
  requireValue(assertions.length === report.numTotalTests && report.numPassedTests === assertions.length && assertions.every(a => a.status === 'passed'), 'Unit assertions incomplete');
  for (const file of files ?? []) requireValue(report.testResults.some(result => result.name.endsWith(file) && result.assertionResults.length > 0), `Missing unit file: ${file}`);
  return { passed: assertions.length, files: report.testResults.length };
}
export function browserSpecs(suites) {
  return suites.flatMap(suite => [...suite.specs, ...browserSpecs(suite.suites ?? [])]);
}
export function verifyBrowser(report, scope, projects = ['chromium-1280', 'chromium-1920']) {
  requireValue(Array.isArray(report.errors) && report.errors.length === 0, 'Browser runner errors');
  const specs = browserSpecs(report.suites ?? []);
  const tests = specs.flatMap(spec => spec.tests);
  requireValue(tests.length > 0, 'Empty browser report');
  requireValue(report.stats.unexpected === 0 && report.stats.flaky === 0, 'Failed/flaky browser report');
  // Existing full-suite viewport exclusions are explicit and retained. Fast routes accept no skip.
  const full = scope.browser === null;
  requireValue(full || report.stats.skipped === 0, 'Skipped focused browser test');
  for (const spec of specs) for (const t of spec.tests) {
    if (full && t.status === 'skipped') {
      requireValue(t.projectName === 'chromium-1920' && (
        spec.file.endsWith('solo.spec.ts') && /^(accepts a neutral virtual gamepad|uses D-pad left and right)/.test(spec.title) ||
        spec.file.endsWith('game.spec.ts') && /^(supports N\+1 public bonus veto|marks a zero-reserve team|shows each unanswered team)/.test(spec.title) ||
        spec.file.endsWith('desktop-download.spec.ts') && spec.title === 'Windows installer downloads with an active PWA without replacing the game' ||
        spec.file.endsWith('manual-update.spec.ts') && spec.title === 'web/mobile hides current, offers a ready update and applies A→B offline'
      ), 'Unapproved full-suite skip');
      requireValue(specs.some(other => other.file === spec.file && other.title === spec.title && other.tests.some(test =>
        test.projectName === 'chromium-1280' && test.status === 'expected' && test.expectedStatus === 'passed' &&
        test.results.length === 1 && test.results[0].status === 'passed'
      )), 'Skipped duplicate has no successful primary viewport');
      requireValue(t.results.length === 1 && t.results[0].status === 'skipped', 'Invalid full-suite skip');
      continue;
    }
    requireValue(t.expectedStatus === 'passed' && t.status === 'expected' && t.results.length === 1 && t.results[0].status === 'passed', 'Browser test did not pass once');
  }
  if (!full) {
    for (const [file, pattern, count = 1] of scope.browser) for (const project of projects) {
      requireValue(specs.filter(spec => spec.file.endsWith(file) && new RegExp(pattern).test(spec.title)).flatMap(spec => spec.tests.filter(t => t.projectName === project)).length === count, `Missing browser selector/project: ${file} / ${pattern} / ${project}`);
    }
    requireValue(specs.every(spec => selectedSpec(scope, spec.file, spec.title)), 'Unexpected browser selection');
  }
  const passed = tests.filter(t => t.status === 'expected').length;
  requireValue(passed > 0 && passed === report.stats.expected && tests.length === report.stats.expected + report.stats.skipped, 'Incomplete browser counters');
  return { passed, skipped: report.stats.skipped, durationMs: report.stats.duration };
}

export function verifyNodeTap(tap, minimum = 23) {
  const counter = name => Number(tap.match(new RegExp(`^# ${name} (\\d+)$`, 'm'))?.[1] ?? NaN);
  const total = counter('tests');
  requireValue(total >= minimum && counter('pass') === total && ['fail', 'cancelled', 'skipped', 'todo'].every(name => counter(name) === 0), 'Tooling TAP report incomplete/failed/skipped');
  return { passed: total };
}

export function verifyUnittest(log) {
  const count = Number(log.match(/Ran (\d+) tests? in/)?.[1] ?? NaN);
  requireValue(count > 0 && /^OK$/m.test(log) && !/FAILED|skipped=/m.test(log), 'Python unittest report incomplete/failed/skipped');
  return { passed: count };
}
