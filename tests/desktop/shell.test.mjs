import { test } from 'node:test';
import assert from 'node:assert/strict';
import { generateKeyPairSync, sign, randomBytes } from 'node:crypto';
import { mkdtemp, mkdir, writeFile, readFile, rm, cp, realpath } from 'node:fs/promises';
import { execFileSync, spawn } from 'node:child_process';
import path from 'node:path';
import os from 'node:os';
import { ShellStore, shellManifest } from '../../desktop/shell.mjs';
import { digest } from '../../desktop/content.mjs';
const { privateKey, publicKey } = generateKeyPairSync('ed25519');
const pin = publicKey.export({ type: 'spki', format: 'der' }).toString('base64');
function release(sequence = 2, script = 'new', extra = {}) {
    const files = { 'Contents/MacOS/Mindbattle': script, 'Contents/Resources/mindbattle-installation.json': JSON.stringify({ product: 'tech.afonasev.mindbattle', pin }), 'Contents/Resources/mindbattle-layout.json': JSON.stringify({ paths: ['Contents/MacOS/Mindbattle', 'Contents/Resources/mindbattle-installation.json'] }) };
    const payload = JSON.stringify({ format: 1, product: 'tech.afonasev.mindbattle', helper: 1, sequence, version: '1.1.0', platform: 'darwin-universal', entry: 'Contents/MacOS/Mindbattle', files: Object.entries(files).map(([name, text]) => ({ path: name, sha256: digest(Buffer.from(text)), size: Buffer.byteLength(text), mode: name.includes('/MacOS/') ? 0o755 : 0o644 })), links: [], ...extra });
    return { env: { payload, signature: sign(null, Buffer.from(payload), privateKey).toString('base64') }, files };
}
async function fixture(t, r = release()) {
    const root = await realpath(await mkdtemp(path.join(os.tmpdir(), 'mindbattle-shell-test-')));
    t.after(() => rm(root, { recursive: true, force: true }));
    const userData = path.join(root, 'user');
    await mkdir(userData);
    const store = new ShellStore({ root: path.join(userData, 'shell'), key: publicKey, version: '1.0.0', platform: 'darwin-universal', origin: 'https://test.invalid', fetcher: async (url) => new Response(url.endsWith('latest.json') ? JSON.stringify(r.env) : Object.values(r.files).find(x => digest(Buffer.from(x)) === url.split('/').at(-1))) });
    await store.initialize();
    await store.check();
    const target = path.join(root, 'Mindbattle.app');
    await cp(path.join(store.releaseDir(), 'runtime'), target, { recursive: true });
    await writeFile(path.join(target, 'Contents/MacOS/Mindbattle'), '#!/bin/sh\nexit 0\n', { mode: 0o755 });
    await writeFile(path.join(target, 'Uninstall Mindbattle.exe'), 'preserved');
    return { root, userData, store, target };
}
test('signed shell rejects tampering, platform, traversal and escaped links', () => {
    const r = release();
    assert.equal(shellManifest(r.env, publicKey, 'darwin-universal').version, '1.1.0');
    assert.throws(() => shellManifest({ ...r.env, payload: r.env.payload + ' ' }, publicKey, 'darwin-universal'));
    assert.throws(() => shellManifest(r.env, publicKey, 'win32-x64'));
    assert.throws(() => shellManifest(release(2, 'x', { links: [{ path: 'escape', target: '../outside' }] }).env, publicKey, 'darwin-universal'));
});
test('candidate preserves uninstall extras, refuses unsafe apply, and retains replay protection after rollback', async (t) => {
    const f = await fixture(t);
    let safe = false;
    assert.equal(await f.store.prepare({ ...f, helper: '/unused', isSafe: () => safe }), null);
    safe = true;
    const helper = path.join(f.root, 'helper');
    await writeFile(helper, 'x');
    const tx = await f.store.prepare({ ...f, helper, isSafe: () => safe });
    assert.equal(await readFile(path.join(tx.plan.candidate, 'Uninstall Mindbattle.exe'), 'utf8'), 'preserved');
    safe = false;
    assert.equal(await f.store.start(tx, () => safe), false);
    const txRoot = path.join(f.store.root, 'transactions', randomBytes(32).toString('hex'));
    await mkdir(txRoot, { recursive: true });
    await writeFile(path.join(txRoot, 'journal.json'), JSON.stringify({ phase: 'rolled-back', error: 'startup timeout' }));
    f.store.state.transaction = txRoot;
    await f.store.save();
    const restarted = new ShellStore({ ...f.store });
    await restarted.initialize();
    assert.equal(restarted.state.pending, null);
    assert.equal(restarted.state.highWater, 2);
    assert.equal(await restarted.check(), false);
});
let helper;
test('real native helper replacement, startup ACK, rollback and corrupted candidate refusal', { skip: process.platform !== 'darwin' }, async (t) => {
    const buildRoot = await realpath(await mkdtemp(path.join(os.tmpdir(), 'mindbattle-go-test-')));
    t.after(() => rm(buildRoot, { recursive: true, force: true }));
    helper = path.join(buildRoot, 'updater');
    execFileSync('/opt/homebrew/bin/go', ['build', '-trimpath', '-ldflags', `-s -w -X main.pinnedKey=${pin}`, '-o', helper, '.'], { cwd: path.resolve('desktop/updater') });
    for (const outcome of ['confirmed', 'rolled-back', 'error']) {
        const script = outcome === 'confirmed' ? '#!/bin/sh\nprintf %s "$MINDBATTLE_SHELL_TOKEN" > "$MINDBATTLE_SHELL_ACK"\nexit 0\n' : '#!/bin/sh\nexit 1\n';
        const f = await fixture(t, release(2, script));
        const parent = spawn('/bin/sleep', ['30']);
        t.after(() => parent.kill());
        const tx = await f.store.prepare({ ...f, helper, isSafe: () => true, parent: parent.pid });
        tx.plan.timeout = 5;
        await writeFile(tx.planFile, JSON.stringify(tx.plan));
        tx.planHash = digest(Buffer.from(JSON.stringify(tx.plan)));
        if (outcome === 'error')
            await writeFile(path.join(tx.plan.candidate, 'Contents/MacOS/Mindbattle'), 'tampered');
        const child = spawn(tx.helper, [tx.planFile, tx.planHash], { stdio: 'ignore' });
        const done = new Promise(resolve => child.on('close', resolve));
        if (outcome !== 'error') {
            for (let i = 0; i < 100; i++) {
                try {
                    await readFile(tx.plan.started);
                    break;
                }
                catch { }
                await new Promise(r => setTimeout(r, 50));
            }
            parent.kill();
        }
        const code = await done;
        const j = JSON.parse(await readFile(tx.plan.journal));
        assert.equal(j.phase, outcome);
        assert.equal(code, outcome === 'confirmed' ? 0 : 1);
        assert.equal(await readFile(path.join(f.target, 'Contents/MacOS/Mindbattle'), 'utf8'), outcome === 'confirmed' ? script : '#!/bin/sh\nexit 0\n');
        assert.equal(await readFile(path.join(f.target, 'Uninstall Mindbattle.exe'), 'utf8'), 'preserved');
    }
});
