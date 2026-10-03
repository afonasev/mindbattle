// Explicit native runtime release, run only when rebuilding installers.
import { readdir, readFile, writeFile, mkdir, rm, stat, readlink, cp, link } from 'node:fs/promises';
import { createPrivateKey, createPublicKey, sign } from 'node:crypto';
import path from 'node:path';
import { fileHash, shellManifest } from '../../desktop/shell.mjs';
const key = createPrivateKey(await readFile(process.env.MINDBATTLE_CONTENT_KEY));
const publicKey = await readFile('desktop/content-public.pem', 'utf8');
if (createPublicKey(key).export({ type: 'spki', format: 'pem' }).toString() !== publicKey)
    throw Error('Signing key mismatch');
const config = JSON.parse(await readFile('desktop/config.json', 'utf8'));
const output = path.resolve('desktop-release/shell');
await rm(output, { recursive: true, force: true });
await mkdir(path.join(output, 'objects'), { recursive: true });
const sequence = Number(process.env.MINDBATTLE_SHELL_SEQUENCE || Date.now());
for (const platform of ['darwin-universal', 'win32-x64']) {
    const root = platform === 'darwin-universal' ? 'desktop-installers/mac-universal/Mindbattle.app' : 'desktop-installers/win-unpacked';
    const files = [], links = [];
    async function walk(dir, rel = '') {
        for (const item of (await readdir(dir, { withFileTypes: true })).sort((a, b) => a.name.localeCompare(b.name))) {
            const name = rel ? `${rel}/${item.name}` : item.name, source = path.join(dir, item.name);
            if (item.isSymbolicLink())
                links.push({ path: name, target: await readlink(source) });
            else if (item.isDirectory())
                await walk(source, name);
            else if (item.isFile()) {
                const info = await stat(source), sha256 = await fileHash(source);
                files.push({ path: name, sha256, size: info.size, mode: info.mode & 0o111 ? 0o755 : 0o644 });
                try {
                    await link(source, path.join(output, 'objects', sha256));
                }
                catch (e) {
                    if (e.code != 'EEXIST')
                        await cp(source, path.join(output, 'objects', sha256));
                }
            }
            else
                throw Error(`Unsupported runtime file ${name}`);
        }
    }
    await walk(root);
    const payload = JSON.stringify({ format: 1, product: 'tech.afonasev.mindbattle', sequence, version: config.shellVersion, platform, helper: 1, entry: platform === 'darwin-universal' ? 'Contents/MacOS/Mindbattle' : 'Mindbattle.exe', files, links });
    const envelope = { payload, signature: sign(null, Buffer.from(payload), key).toString('base64') };
    shellManifest(envelope, publicKey, platform);
    await mkdir(path.join(output, platform));
    await writeFile(path.join(output, platform, 'latest.json'), JSON.stringify(envelope));
    console.log(`${platform} ${config.shellVersion}: ${files.length} files, ${links.length} links`);
}
