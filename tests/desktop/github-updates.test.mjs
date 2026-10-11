import { test } from 'node:test';
import assert from 'node:assert/strict';
import { generateKeyPairSync, sign } from 'node:crypto';
import { mkdir, mkdtemp, readFile, writeFile, rm, realpath } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import os from 'node:os';
import path from 'node:path';
import { fetchUpdate, objectBase, releaseBase, updateOrigin } from '../../desktop/updateTransport.mjs';
import { ContentStore, digest } from '../../desktop/content.mjs';
import { ShellStore } from '../../desktop/shell.mjs';
import { publishUpdates } from '../../scripts/desktop/publish-updates.mjs';

test('GitHub redirects permit the release CDN but refuse other hosts, credentials, downgrade and loops', async () => {
  const url = `${releaseBase('content', 2)}/${'a'.repeat(64)}`;
  let calls = 0;
  const result = await fetchUpdate(async (address, options) => {
    calls++; assert.equal(options.redirect, 'manual');
    return address === url ? new Response(null, { status: 302, headers: { location: 'https://release-assets.githubusercontent.com/github-production-release-asset/123?token=fixture' } }) : new Response('verified');
  }, url);
  assert.equal(await result.text(), 'verified'); assert.equal(calls, 2);
  for (const destination of ['http://release-assets.githubusercontent.com/x', 'https://evil.test/x', 'https://user@release-assets.githubusercontent.com/x', 'https://github.com/other/repo/releases/download/x', 'https://release-assets.githubusercontent.com:444/x']) {
    let requests = 0;
    await assert.rejects(fetchUpdate(async () => { requests++; return new Response(null, { status: 302, headers: { location: destination } }); }, url), /Unsafe/);
    assert.equal(requests, 1);
  }
  await assert.rejects(fetchUpdate(async () => new Response(null, { status: 302, headers: { location: url } }), url), /Too many/);
  assert.throws(() => objectBase({ sequence: 2, objectBaseUrl: releaseBase('shell', 2) }, 'content', updateOrigin));
  assert.throws(() => objectBase({ sequence: 2 }, 'content', updateOrigin));
});

for (const kind of ['content', 'shell']) {
  test(`${kind} signed GitHub store downloads via CDN, reports progress and keeps replay protection`, async t => {
    const root = await realpath(await mkdtemp(path.join(os.tmpdir(), 'mindbattle-github-store-')));
    t.after(() => rm(root, { recursive: true, force: true }));
    const { privateKey, publicKey } = generateKeyPairSync('ed25519');
    const bytes = Buffer.from('game data');
    const file = kind === 'content' ? 'index.html' : 'Contents/MacOS/Mindbattle';
    const payload = JSON.stringify({ format: 1, sequence: 2, version: '1.0.5', bridge: 1, shellMajor: 1,
      product: 'tech.afonasev.mindbattle', platform: 'darwin-universal', helper: 1, entry: file, links: [],
      objectBaseUrl: releaseBase(kind, 2), files: [{ path: file, size: bytes.length, sha256: digest(bytes), mode: 0o755 }] });
    const envelope = { payload, signature: sign(null, Buffer.from(payload), privateKey).toString('base64') };
    const requests = [];
    const fetcher = async address => {
      requests.push(address);
      if (address.endsWith('latest.json')) return Response.json(envelope);
      if (address.startsWith(releaseBase(kind, 2))) return new Response(null, { status: 302, headers: { location: 'https://release-assets.githubusercontent.com/object' } });
      return new Response(bytes);
    };
    const store = kind === 'content' ? new ContentStore({ root, bundle: path.join(root, 'bundle'), publicKey, shellVersion: '1.0.4', origin: updateOrigin, fetcher }) : new ShellStore({ root, key: publicKey, version: '1.0.4', platform: 'darwin-universal', origin: updateOrigin, fetcher });
    const progress = [];
    assert.equal(await store.check(status => progress.push(status)), true);
    assert.equal(store.state.highWater, 2);
    assert.equal(progress[0].completed, 0); assert.equal(progress.at(-1).completed, 1);
    assert.equal(progress[0].version, '1.0.5');
    assert.ok(requests.every(r => !r.includes('afonasev.tech')));
    const installed = kind === 'content' ? path.join(store.directory(store.state.pending), file) : path.join(store.releaseDir(), 'runtime', file);
    assert.equal(await readFile(installed, 'utf8'), bytes.toString());
    const count = requests.length;
    assert.equal(await store.check(), true);
    assert.equal(requests.length, count + 1); // no replay download
  });
}

test('publication uploads and verifies before switching Pages, resumes safely and retains feed on corruption/replay', async t => {
  const root = await mkdtemp(path.join(os.tmpdir(), 'mindbattle-github-publisher-test-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const cwd = path.join(root, 'source'); const remote = path.join(root, 'remote.git');
  await mkdir(cwd);
  const git = (...args) => execFileSync('git', args, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
  git('init', '--bare', remote); git('init', '-b', 'main'); git('config', 'user.name', 'Fixture'); git('config', 'user.email', 'fixture@example.test');
  const { privateKey, publicKey } = generateKeyPairSync('ed25519');
  await mkdir(path.join(cwd, 'desktop'));
  await writeFile(path.join(cwd, '.gitignore'), 'desktop-release/\n');
  await writeFile(path.join(cwd, 'desktop/config.json'), JSON.stringify({ shellVersion: '1.0.5', updateOrigin }));
  await writeFile(path.join(cwd, 'desktop/content-public.pem'), publicKey.export({ type: 'spki', format: 'pem' }));
  git('add', '.'); git('commit', '-m', 'fixture'); git('remote', 'add', 'origin', remote); git('push', 'origin', 'main');
  let envelope; let bytes;
  const stage = async (sequence, body) => {
    bytes = Buffer.from(body);
    const payload = JSON.stringify({ format: 1, sequence, version: '0.1.0', bridge: 1, shellMajor: 1, objectBaseUrl: releaseBase('content', sequence), files: [{ path: 'index.html', size: bytes.length, sha256: digest(bytes) }] });
    envelope = { payload, signature: sign(null, Buffer.from(payload), privateKey).toString('base64') };
    await mkdir(path.join(cwd, 'desktop-release/content/objects'), { recursive: true });
    await writeFile(path.join(cwd, 'desktop-release/content/latest.json'), JSON.stringify(envelope));
    await writeFile(path.join(cwd, 'desktop-release/content/objects', digest(bytes)), bytes);
  };
  let pages = null; const releases = []; const mutations = []; let corrupt = false;
  const run = (command, args, directory) => {
    if (command === 'git') return execFileSync(command, args, { cwd: directory, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    if (args.includes('--include')) {
      if (pages) return `HTTP/2.0 200 OK\n\n${JSON.stringify(pages)}`;
      throw Object.assign(Error('not found'), { stdout: 'HTTP/2.0 404 Not Found\n\n{}' });
    }
    if (args.includes('--method')) { pages = { build_type: 'legacy', source: { branch: 'desktop-updates', path: '/' } }; return '{}'; }
    if (args[0] === 'api') {
      const endpoint = args.at(-1);
      if (endpoint.includes('/git/ref/tags/')) return JSON.stringify({ object: { type: 'commit', sha: git('rev-parse', 'HEAD') } });
      if (endpoint.includes('/assets?')) {
        const r = releases.find(r => endpoint.includes(`/${r.id}/assets`)); return JSON.stringify([r.assets]);
      }
      return JSON.stringify([releases]);
    }
    const tag = args[2]; mutations.push(args[1]);
    if (args[1] === 'create') { releases.push({ id: releases.length + 1, tag_name: tag, target_commitish: git('rev-parse', 'HEAD'), draft: true, assets: [] }); return ''; }
    const r = releases.find(r => r.tag_name === tag);
    if (args[1] === 'upload') {
      const f = args[3]; const b = execFileSync(process.execPath, ['-e', 'process.stdout.write(require("fs").readFileSync(process.argv[1]))', f]);
      r.assets.push({ name: path.basename(f), size: b.length, digest: `sha256:${corrupt ? '0'.repeat(64) : digest(b)}` }); return '';
    }
    if (args[1] === 'edit') { r.draft = false; assert.ok(args.includes('--latest=false')); return ''; }
    throw Error(`Unexpected gh invocation ${args}`);
  };
  const fetcher = async () => new Response(JSON.stringify(envelope));
  await stage(2, 'first'); await publishUpdates('content', { cwd, run, fetcher });
  const first = git('ls-remote', 'origin', 'desktop-updates');
  assert.equal(releases[0].draft, false); assert.ok(mutations.includes('upload'));
  await publishUpdates('content', { cwd, run, fetcher }); // same release is idempotent
  assert.equal(git('ls-remote', 'origin', 'desktop-updates'), first);
  await stage(3, 'second'); corrupt = true;
  await assert.rejects(publishUpdates('content', { cwd, run, fetcher }), /integrity mismatch/);
  assert.equal(git('ls-remote', 'origin', 'desktop-updates'), first);
  assert.equal(releases[1].draft, true);
  // Simulate correcting this owned, never-published draft's bad fixture digest.
  corrupt = false; for (const asset of releases[1].assets) asset.digest = `sha256:${asset.name === 'latest.json' ? digest(Buffer.from(JSON.stringify(envelope))) : digest(bytes)}`;
  await publishUpdates('content', { cwd, run, fetcher });
  const second = git('ls-remote', 'origin', 'desktop-updates'); assert.notEqual(second, first);
  const count = mutations.length;
  await stage(2, 'replay'); await assert.rejects(publishUpdates('content', { cwd, run, fetcher }), /sequence must advance/);
  assert.equal(mutations.length, count); assert.equal(git('ls-remote', 'origin', 'desktop-updates'), second);
  pages.source.branch = 'another-site';
  await stage(4, 'third'); await assert.rejects(publishUpdates('content', { cwd, run, fetcher }), /another publishing source/);
  assert.equal(mutations.length, count);
  pages.source.branch = 'desktop-updates';
  const shellEnvelopes = {};
  const runtime = Buffer.from('runtime');
  await mkdir(path.join(cwd, 'desktop-release/shell/objects'), { recursive: true });
  await writeFile(path.join(cwd, 'desktop-release/shell/objects', digest(runtime)), runtime);
  async function stageShell(platform, sequence) {
    const entry = platform === 'darwin-universal' ? 'Contents/MacOS/Mindbattle' : 'Mindbattle.exe';
    const payload = JSON.stringify({ format: 1, product: 'tech.afonasev.mindbattle', version: '1.0.5', sequence, platform, helper: 1, entry, links: [], objectBaseUrl: releaseBase('shell', sequence), files: [{ path: entry, size: runtime.length, sha256: digest(runtime), mode: 0o755 }] });
    const env = { payload, signature: sign(null, Buffer.from(payload), privateKey).toString('base64') };
    shellEnvelopes[platform] = env;
    await mkdir(path.join(cwd, 'desktop-release/shell', platform), { recursive: true });
    await writeFile(path.join(cwd, 'desktop-release/shell', platform, 'latest.json'), JSON.stringify(env));
  }
  await stageShell('darwin-universal', 5); await stageShell('win32-x64', 6);
  await assert.rejects(publishUpdates('shell', { cwd, run, fetcher }), /share a sequence/);
  assert.equal(mutations.length, count);
  await stageShell('win32-x64', 5);
  await publishUpdates('shell', { cwd, run, fetcher: async url => Response.json(shellEnvelopes[url.split('/').at(-2)]) });
  assert.equal(releases.at(-1).tag_name, 'shell-5'); assert.equal(releases.at(-1).assets.length, 3);
  const activeContent = git('--git-dir', remote, 'show', 'desktop-updates:desktop/content/latest.json');
  assert.equal(JSON.parse(JSON.parse(activeContent).payload).sequence, 3);
  for (const platform of ['darwin-universal', 'win32-x64']) {
    const active = git('--git-dir', remote, 'show', `desktop-updates:desktop/shell/${platform}/latest.json`);
    assert.deepEqual(JSON.parse(active), shellEnvelopes[platform]);
  }
});
