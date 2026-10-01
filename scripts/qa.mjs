import { spawn, execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { createServer } from 'node:net';
import { mkdir, mkdtemp, readFile, writeFile, rm } from 'node:fs/promises';
import { openSync, closeSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve, join } from 'node:path';
import { once } from 'node:events';
import { scopes } from './qaScope.mjs';
import { verifyVitest, verifyBrowser, verifyNodeTap, verifyUnittest } from './qaReports.mjs';
const args = process.argv.slice(2);
let scopeName = 'full', output;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--scope' && args[i + 1]) scopeName = args[++i];
  else if (args[i] === '--evidence' && args[i + 1]) output = args[++i];
  else throw new Error(`Unknown/incomplete argument: ${args[i]}`);
}
const scope = scopes[scopeName];
if (!scope) throw new Error(`Unknown scope: ${scopeName}`);
const evidence = output ? resolve(output) : await mkdtemp(join(tmpdir(), `mindbattle-qa-${scopeName}-`));
await mkdir(evidence, { recursive: true });
// A new directory prevents old successful reports from satisfying a failed run.
const runDir = await mkdtemp(join(evidence, 'run-'));
const git = (...argv) => execFileSync('git', argv, { encoding: 'utf8' }).trim();
const status = git('status', '--porcelain');
const diff = execFileSync('git', ['diff', 'HEAD', '--binary']);
const untracked = git('ls-files', '--others', '--exclude-standard').split('\n').filter(Boolean);
const hash = createHash('sha256').update(diff);
for (const file of untracked) hash.update(file).update(readFileSync(file));
const summary = { scope: scopeName, revision: git('rev-parse', 'HEAD'), dirty: !!status, diffSha256: hash.digest('hex'), status,
  node: process.version, startedAt: new Date().toISOString(), evidence: runDir, phases: [], success: false };
let active, host, interrupted = false;
const started = performance.now();
const childEnv = { ...process.env };
// Reports and target origins must come from this run, not shell overrides.
delete childEnv.PLAYWRIGHT_JSON_OUTPUT_FILE;
delete childEnv.PLAYWRIGHT_JSON_OUTPUT_DIR;
delete childEnv.PLAYWRIGHT_JSON_OUTPUT_NAME;
delete childEnv.MINDBATTLE_TEST_ORIGIN;
async function command(name, executable, argv, env = childEnv) {
  if (interrupted) throw new Error('QA interrupted');
  const fd = openSync(join(runDir, `${name}.log`), 'w');
  const begin = performance.now();
  try {
    active = spawn(executable, argv, { env, stdio: ['ignore', fd, fd] });
    const [code, signal] = await once(active, 'exit');
    const phase = { name, command: [executable, ...argv], exitCode: code, signal, wallMs: Math.round(performance.now() - begin) };
    summary.phases.push(phase);
    if (code !== 0) throw new Error(`${name} failed (${code ?? signal}); see ${name}.log`);
    return phase;
  } finally { active = undefined; closeSync(fd); }
}
async function ownedHost(dev) {
  const probe = createServer();
  probe.listen(0, '127.0.0.1'); await once(probe, 'listening');
  const port = probe.address().port;
  await new Promise((done, fail) => probe.close(error => error ? fail(error) : done()));
  const data = await mkdtemp(join(tmpdir(), 'mindbattle-qa-data-'));
  summary.host = { port, data, kind: dev ? 'dev' : 'production-preview' };
  const env = { ...childEnv, MINDBATTLE_HOST: '127.0.0.1', MINDBATTLE_PORT: String(port), MINDBATTLE_FEEDBACK_PATH: join(data, 'feedback.ndjson'), MINDBATTLE_RESULTS_PATH: join(data, 'results.ndjson') };
  const fd = openSync(join(runDir, 'host.log'), 'w');
  const begin = performance.now();
  host = spawn(process.execPath, ['server/index.mjs', ...(dev ? ['--dev'] : [])], { env, stdio: ['ignore', fd, fd] });
  closeSync(fd);
  summary.host.pid = host.pid;
  let spawnError;
  host.on('error', error => { spawnError = error; });
  while (performance.now() - begin < 120000) {
    if (spawnError || host.exitCode !== null) throw new Error(`Owned host exited: ${spawnError ?? host.exitCode}`);
    // Do not accept an unrelated host that won a port race: our server must log its listen.
    const log = await readFile(join(runDir, 'host.log'), 'utf8');
    if (log.includes(`Mindbattle: http://127.0.0.1:${port}`)) {
      try { const response = await fetch(`http://127.0.0.1:${port}/`, { signal: AbortSignal.timeout(1000) }); if (response.ok) { summary.host.startupMs = Math.round(performance.now() - begin); return port; } } catch {}
    }
    await new Promise(done => setTimeout(done, 100));
  }
  throw new Error('Owned host readiness timeout');
}
const stop = () => { active?.kill('SIGTERM'); host?.kill('SIGTERM'); };
const interrupt = () => { interrupted = true; stop(); };
process.on('SIGINT', interrupt); process.on('SIGTERM', interrupt);
try {
  await command('tooling', process.execPath, ['--test', '--test-reporter=tap', 'tests/tooling/qa.test.mjs']);
  summary.tooling = verifyNodeTap(await readFile(join(runDir, 'tooling.log'), 'utf8'));
  if (scopeName === 'tooling' || scopeName === 'full') {
    await command('flow-contracts', 'python3', ['tools/test_flow.py']);
    summary.flowContracts = verifyUnittest(await readFile(join(runDir, 'flow-contracts.log'), 'utf8'));
    await command('flow-delivery-contracts', 'python3', ['-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_flow*.py']);
    summary.flowDeliveryContracts = verifyUnittest(await readFile(join(runDir, 'flow-delivery-contracts.log'), 'utf8'));
  }
  await command('typecheck', 'npm', ['run', 'typecheck']);
  if (scope.units === null || scope.units.length) {
    await command('unit', process.execPath, ['node_modules/vitest/vitest.mjs', 'run', ...(scope.units ?? []), '--reporter=default', '--reporter=json', `--outputFile.json=${join(runDir, 'unit.json')}`]);
    summary.unit = verifyVitest(JSON.parse(await readFile(join(runDir, 'unit.json'), 'utf8')), scope.units);
  }
  if (scopeName === 'full') await command('build', 'npm', ['run', 'build:assets']);
  if (scope.browser === null || scope.browser.length) {
    const port = await ownedHost(scopeName !== 'full');
    // Compile the dev module graph before timed scenarios; do not inflate their timeouts.
    const warmStart = performance.now();
    const { chromium } = await import('@playwright/test');
    const warmBrowser = await chromium.launch({ args: ['--mute-audio'] });
    try {
      const warmPage = await warmBrowser.newPage();
      await warmPage.goto(`http://127.0.0.1:${port}/?muted=1`);
      await warmPage.getByRole('button', { name: 'Одиночная игра', exact: true }).waitFor({ timeout: 30000 });
      await warmPage.goto(`http://127.0.0.1:${port}/network?muted=1`);
      await warmPage.locator('.network-app').waitFor({ timeout: 30000 });
    } finally { await warmBrowser.close(); }
    summary.host.warmupMs = Math.round(performance.now() - warmStart);
    const env = { ...childEnv, MINDBATTLE_QA_SCOPE: scopeName, MINDBATTLE_TEST_PORT: String(port), MINDBATTLE_QA_OUTPUT: join(runDir, 'browser-artifacts'), MINDBATTLE_QA_REPORT: join(runDir, 'browser.json') };
    await command('browser', process.execPath, ['node_modules/@playwright/test/cli.js', 'test', '--config=playwright.qa.config.ts'], env);
    summary.browser = verifyBrowser(JSON.parse(await readFile(join(runDir, 'browser.json'), 'utf8')), scope, scope.projects);
  }
  summary.success = true;
} catch (error) { summary.error = error.message; process.exitCode = 1; }
finally {
  stop();
  if (host && host.exitCode === null && host.signalCode === null) await once(host, 'exit');
  if (summary.host?.data) { await rm(summary.host.data, { recursive: true, force: true }); summary.host.cleaned = true; }
  summary.wallMs = Math.round(performance.now() - started);
  await writeFile(join(runDir, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
  console.log(JSON.stringify(summary, null, 2));
}
