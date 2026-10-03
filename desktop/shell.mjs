import { createHash, verify, randomBytes } from 'node:crypto';
import { readFile as packagedReadFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
// Electron treats app.asar as a virtual directory. Runtime updates need raw bytes.
const fs = createRequire(import.meta.url)(process.versions.electron ? 'original-fs' : 'node:fs');
const { readFile, writeFile, mkdir, rename, rm, readdir, lstat, readlink, realpath, cp, open, chmod, symlink } = fs.promises;
const { createReadStream } = fs;
import { spawn } from 'node:child_process';
import path from 'node:path';
import { digest, atomicJson, boundedBytes } from './content.mjs';
export const shellPath = value => typeof value === 'string' && value.length > 0 && !/[\\:\x00\r\n\t]/.test(value) && !value.startsWith('/') && value.split('/').every(p => p && p !== '.' && p !== '..' && !/[. ]$/.test(p));
export async function fileHash(file) { const h = createHash('sha256'); for await (const bytes of createReadStream(file))
    h.update(bytes); return h.digest('hex'); }
export const versionNumber = version => { if (!/^\d+\.\d+\.\d+$/.test(version))
    throw Error('Invalid shell version'); return version.split('.').map(Number); };
export function newerVersion(a, b) { const x = versionNumber(a), y = versionNumber(b); for (let i = 0; i < 3; i++) {
    if (x[i] !== y[i])
        return x[i] > y[i];
} return false; }
export function shellManifest(envelope, key, platform) {
    if (typeof envelope?.payload !== 'string' || envelope.payload.length > 8 * 1024 ** 2 || typeof envelope.signature !== 'string' || !verify(null, Buffer.from(envelope.payload), key, Buffer.from(envelope.signature, 'base64')))
        throw Error('Invalid shell signature');
    const m = JSON.parse(envelope.payload);
    versionNumber(m.version);
    if (m.format !== 1 || m.product !== 'tech.afonasev.mindbattle' || m.platform !== platform || m.helper !== 1 || !Number.isSafeInteger(m.sequence) || m.sequence < 1 || !shellPath(m.entry) || !Array.isArray(m.files) || !m.files.length || m.files.length > 20000 || !Array.isArray(m.links))
        throw Error('Incompatible shell');
    const names = new Set();
    let total = 0;
    for (const f of m.files) {
        if (!shellPath(f.path) || names.has(f.path) || !/^[a-f0-9]{64}$/.test(f.sha256) || !Number.isSafeInteger(f.size) || f.size < 0 || f.size > 1024 ** 3 || ![0o644, 0o755].includes(f.mode))
            throw Error('Invalid shell file');
        names.add(f.path);
        total += f.size;
    }
    if (total > 3 * 1024 ** 3 || !names.has(m.entry))
        throw Error('Invalid shell size');
    for (const l of m.links) {
        const resolved = path.posix.normalize(path.posix.join(path.posix.dirname(l.path), l.target || ''));
        if (!shellPath(l.path) || names.has(l.path) || typeof l.target !== 'string' || !l.target || /[\\:\x00\r\n\t]/.test(l.target) || path.posix.isAbsolute(l.target) || resolved === '..' || resolved.startsWith('../'))
            throw Error('Unsafe shell link');
        names.add(l.path);
    }
    if (platform === 'win32-x64' && m.links.length)
        throw Error('Windows runtime links not supported');
    return m;
}
async function downloadFile(response, file, expected) {
    if (!response.ok)
        throw Error(`Shell download failed: ${response.status}`);
    await mkdir(path.dirname(file), { recursive: true });
    const handle = await open(file, 'wx', expected.mode);
    const reader = response.body.getReader();
    let size = 0;
    const h = createHash('sha256');
    try {
        for (;;) {
            const { done, value } = await reader.read();
            if (done)
                break;
            size += value.length;
            if (size > expected.size)
                throw Error('Shell download too large');
            h.update(value);
            await handle.writeFile(Buffer.from(value));
        }
        if (size !== expected.size || h.digest('hex') !== expected.sha256)
            throw Error('Shell hash mismatch');
        await handle.sync();
    }
    finally {
        await reader.cancel().catch(() => { });
        await handle.close();
    }
    await chmod(file, expected.mode);
}
export async function validateShellTree(root, m) {
    for (const f of m.files) {
        const file = path.join(root, f.path);
        const info = await lstat(file);
        if (!info.isFile() || info.size !== f.size || await realpath(file) !== file || await fileHash(file) !== f.sha256)
            throw Error('Shell file verification failed');
    }
    for (const l of m.links) {
        const file = path.join(root, l.path);
        if (await readlink(file) !== l.target || !(await realpath(file)).startsWith(root + path.sep))
            throw Error('Shell link verification failed');
    }
}
export class ShellStore {
    constructor({ root, key, version, platform, origin, fetcher = fetch }) { Object.assign(this, { root, key, version, platform, origin, fetcher }); this.state = { highWater: 0, pending: null }; this.busy = false; }
    async initialize() {
        try {
            this.state = JSON.parse(await readFile(path.join(this.root, 'state.json'), 'utf8'));
        }
        catch { }
        if (!Number.isSafeInteger(this.state.highWater))
            this.state.highWater = 0;
        if (this.state.transaction) {
            try {
                const tx = this.state.transaction;
                if (!tx.startsWith(path.join(this.root, "transactions") + path.sep))
                    throw Error("Invalid transaction");
                const j = JSON.parse(await readFile(path.join(tx, "journal.json"), "utf8"));
                if (["rolled-back", "error", "recovery-required"].includes(j.phase)) {
                    this.state.pending = null;
                    this.lastError = j.error;
                    this.state.transaction = null;
                }
            }
            catch { }
        }
        if (this.state.pending) {
            try {
                const m = await this.pendingManifest();
                if (!newerVersion(m.version, this.version))
                    this.state.pending = null;
            }
            catch {
                this.state.pending = null;
            }
        }
        await this.save();
        return Boolean(this.state.pending);
    }
    async save() { await atomicJson(path.join(this.root, 'state.json'), this.state); }
    releaseDir(id = this.state.pending) { if (!/^[a-f0-9]{64}$/.test(id || ''))
        throw Error('Invalid shell release'); return path.join(this.root, 'releases', id); }
    async pendingManifest() { return shellManifest(JSON.parse(await readFile(path.join(this.releaseDir(), 'release.json'), 'utf8')), this.key, this.platform); }
    async check() {
        if (this.busy)
            return Boolean(this.state.pending);
        this.busy = true;
        let stage;
        try {
            const raw = await boundedBytes(await this.fetcher(`${this.origin}/desktop/shell/${this.platform}/latest.json`, { redirect: 'error', signal: AbortSignal.timeout(30000), cache: 'no-store' }), 8 * 1024 ** 2);
            const env = JSON.parse(raw.toString());
            const m = shellManifest(env, this.key, this.platform);
            if (m.sequence <= this.state.highWater || !newerVersion(m.version, this.version))
                return Boolean(this.state.pending);
            const id = digest(Buffer.from(env.payload));
            stage = path.join(this.root, 'staging');
            await rm(stage, { recursive: true, force: true });
            await mkdir(stage, { recursive: true });
            for (const f of m.files)
                await downloadFile(await this.fetcher(`${this.origin}/desktop/shell/objects/${f.sha256}`, { redirect: 'error', signal: AbortSignal.timeout(120000) }), path.join(stage, 'runtime', f.path), f);

            for (const l of m.links) {
                const file = path.join(stage, 'runtime', l.path);
                await mkdir(path.dirname(file), { recursive: true });
                await symlink(l.target, file);
            }
            await writeFile(path.join(stage, 'release.json'), raw);
            await validateShellTree(path.join(stage, 'runtime'), m);
            const target = this.releaseDir(id);
            await mkdir(path.dirname(target), { recursive: true });
            await rm(target, { recursive: true, force: true });
            await rename(stage, target);
            stage = null;
            this.state.pending = id;
            this.state.highWater = m.sequence;
            await this.save();
            return true;
        }
        finally {
            if (stage)
                await rm(stage, { recursive: true, force: true });
            this.busy = false;
        }
    }
    async prepare({ target, userData, helper, isSafe, parent = process.pid }) {
        if (this.busy || !this.state.pending)
            return null;
        this.busy = true;
        let candidate;
        try {
            const m = await this.pendingManifest();
            const source = path.join(this.releaseDir(), 'runtime');
            await validateShellTree(source, m);
            if (!isSafe())
                return null;
            target = await realpath(target);
            userData = await realpath(userData);
            if (this.platform === 'darwin-universal' && (target.startsWith('/Volumes/') || target.includes('/AppTranslocation/')))
                throw Error('Переместите игру из DMG в доступную для записи папку и повторите обновление.');
            const token = randomBytes(32).toString('hex');
            candidate = `${target}.candidate-${token}`;
            const backup = `${target}.backup-${token}`;
            try {
                await mkdir(candidate, { mode: 0o700 });
            }
            catch {
                throw Error('Папка установки недоступна для записи. Переместите игру в свою папку или используйте установщик.');
            }
            await cp(source, candidate, { recursive: true, dereference: false, verbatimSymlinks: true });
            // Preserve installer-owned and user-added files; obsolete payload files are excluded using the installed inventory.
            const resources = this.platform === 'darwin-universal' ? 'Contents/Resources' : 'resources';
            const layout = JSON.parse(await readFile(path.join(target, resources, 'mindbattle-layout.json'), 'utf8'));
            const owned = new Set(layout.paths);
            owned.add(`${resources}/mindbattle-layout.json`);
            const next = new Set([...m.files.map(f => f.path), ...m.links.map(l => l.path)]);
            const extras = async (dir, rel = '') => { for (const item of await readdir(dir, { withFileTypes: true })) {
                const name = rel ? `${rel}/${item.name}` : item.name;
                const old = path.join(dir, item.name);
                if (item.isDirectory())
                    await extras(old, name);
                else if (!owned.has(name) && !next.has(name)) {
                    if (!shellPath(name) || item.isSymbolicLink())
                        throw Error('Unsupported extra installation file');
                    await mkdir(path.dirname(path.join(candidate, name)), { recursive: true });
                    await cp(old, path.join(candidate, name));
                }
            } };
            await extras(target);
            await validateShellTree(candidate, m);
            if (!isSafe()) {
                await rm(candidate, { recursive: true, force: true });
                return null;
            }
            const tx = path.join(this.root, 'transactions', token);
            await mkdir(tx, { recursive: true, mode: 0o700 });
            const manifest = path.join(tx, 'release.json');
            await cp(path.join(this.releaseDir(), 'release.json'), manifest);
            const helperCopy = path.join(tx, this.platform === 'win32-x64' ? 'updater.exe' : 'updater');
            await writeFile(helperCopy, await packagedReadFile(helper), {mode:0o755});
            await chmod(helperCopy, 0o755);
            const plan = { target, candidate, backup, root: tx, manifest, journal: path.join(tx, 'journal.json'), ack: path.join(tx, 'ready'), started: path.join(tx, 'started'), token, parent, userData, timeout: 60 };
            const planFile = path.join(tx, 'plan.json');
            const bytes = Buffer.from(JSON.stringify(plan));
            await writeFile(planFile, bytes, { mode: 0o600 });
            return { plan, planFile, planHash: digest(bytes), helper: helperCopy };
        }
        catch (e) {
            if (candidate)
                await rm(candidate, { recursive: true, force: true });
            throw e;
        }
        finally {
            this.busy = false;
        }
    }
    async start(tx, isSafe) {
        if (!isSafe()) {
            await rm(tx.plan.candidate, { recursive: true, force: true });
            return false;
        }
        this.state.transaction = tx.plan.root;
        await this.save();
        const log = await open(path.join(tx.plan.root, 'helper.log'), 'a', 0o600);
        let child;
        try {
            child = spawn(tx.helper, [tx.planFile, tx.planHash], { detached: true, cwd: tx.plan.root, stdio: ['ignore', log.fd, log.fd] });
            child.unref();
        }
        finally {
            await log.close();
        }
        let error;
        child.on('error', e => { error = e; });
        for (let i = 0; i < 600; i++) {
            if (error)
                throw error;
            try {
                if (await readFile(tx.plan.started, 'utf8') === tx.plan.token) {
                    if (!isSafe()) {
                        child.kill();
                        await rm(tx.plan.candidate, { recursive: true, force: true });
                        return false;
                    }
                    return true;
                }
            }
            catch { }
            try {
                const j = JSON.parse(await readFile(tx.plan.journal, 'utf8'));
                if (j.phase === 'error')
                    throw Error(j.error);
            }
            catch (e) {
                if (e.code !== 'ENOENT' && !(e instanceof SyntaxError))
                    throw e;
            }
            await new Promise(r => setTimeout(r, 100));
        }
        child.kill();
        throw Error('Не удалось подготовить обновление оболочки.');
    }
}
export async function acknowledgeShell(userData) {
    const file = process.env.MINDBATTLE_SHELL_ACK, token = process.env.MINDBATTLE_SHELL_TOKEN;
    if (!file && !token)
        return;
    if (!/^[a-f0-9]{64}$/.test(token || '') || path.resolve(file) !== path.join(await realpath(userData), 'shell', 'transactions', token, 'ready'))
        throw Error('Invalid shell acknowledgement');
    const plan = JSON.parse(await readFile(path.join(path.dirname(file), 'plan.json'), 'utf8'));
    if (plan.token !== token)
        throw Error('Invalid update token');
    await writeFile(file, token, { mode: 0o600 });
    delete process.env.MINDBATTLE_SHELL_ACK;
    delete process.env.MINDBATTLE_SHELL_TOKEN;
}
