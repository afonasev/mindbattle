import { test } from 'node:test';
import assert from 'node:assert/strict';
import { generateKeyPairSync } from 'node:crypto';
import { mkdtemp, mkdir, writeFile, readFile, rm } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import os from 'node:os';
import { checkManifest } from '../../desktop/content.mjs';
import { shellManifest } from '../../desktop/shell.mjs';

test('real preparation signs the release publication date into content and both shell manifests', async t => {
  const root = await mkdtemp(path.join(os.tmpdir(), 'mindbattle-publication-date-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const { privateKey, publicKey } = generateKeyPairSync('ed25519');
  const date = '2026-10-11T07:00:00.000Z';
  await mkdir(path.join(root, 'desktop'));
  await mkdir(path.join(root, 'dist'));
  await writeFile(path.join(root, 'desktop/config.json'), JSON.stringify({ shellVersion: '1.0.5' }));
  await writeFile(path.join(root, 'desktop/content-public.pem'), publicKey.export({ type: 'spki', format: 'pem' }));
  const keyPath = path.join(root, 'signing.pem');
  await writeFile(keyPath, privateKey.export({ type: 'pkcs8', format: 'pem' }), { mode: 0o600 });
  await writeFile(path.join(root, 'dist/index.html'), '<!doctype html>fixture');
  await writeFile(path.join(root, 'dist/game-version.json'), JSON.stringify({ version: '0.2.0+1234abcd', publishedAt: date }));
  const env = { ...process.env, MINDBATTLE_CONTENT_KEY: keyPath, MINDBATTLE_CONTENT_SEQUENCE: '2', MINDBATTLE_SHELL_SEQUENCE: '3', MINDBATTLE_PUBLISHED_AT: date };
  execFileSync(process.execPath, [path.resolve('scripts/desktop/prepare.mjs')], { cwd: root, env, stdio: 'pipe' });
  const content = JSON.parse(await readFile(path.join(root, 'desktop-release/content/latest.json'), 'utf8'));
  assert.equal(checkManifest(content, publicKey, '1.0.5').publishedAt, date);
  for (const [directory, entry] of [['mac-universal/Mindbattle.app', 'Contents/MacOS/Mindbattle'], ['win-unpacked', 'Mindbattle.exe']]) {
    const filename = path.join(root, 'desktop-installers', directory, entry);
    await mkdir(path.dirname(filename), { recursive: true }); await writeFile(filename, 'runtime', { mode: 0o755 });
  }
  execFileSync(process.execPath, [path.resolve('scripts/desktop/prepare-shell.mjs')], { cwd: root, env, stdio: 'pipe' });
  for (const platform of ['darwin-universal', 'win32-x64']) {
    const envelope = JSON.parse(await readFile(path.join(root, 'desktop-release/shell', platform, 'latest.json'), 'utf8'));
    assert.equal(shellManifest(envelope, publicKey, platform).publishedAt, date);
  }
});
