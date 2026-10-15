// Real packaged macOS N -> N+1, isolated profile and locally signed test releases.
import { _electron } from '@playwright/test';
import * as asar from '@electron/asar';
import { constants, createReadStream } from 'node:fs';
import { cp, mkdtemp, mkdir, readFile, writeFile, readdir, stat, readlink, rm, realpath } from 'node:fs/promises';
import { createServer } from 'node:http';
import { execFileSync } from 'node:child_process';
import { createPrivateKey, sign } from 'node:crypto';
import path from 'node:path';
import os from 'node:os';
import assert from 'node:assert/strict';
import { releaseBase } from '../../desktop/updateTransport.mjs';
import { fileHash } from '../../desktop/shell.mjs';
const evidence = process.env.MINDBATTLE_DESKTOP_EVIDENCE || '/tmp/mindbattle-desktop-evidence';
await mkdir(evidence, { recursive: true });
const key = createPrivateKey(await readFile(process.env.MINDBATTLE_CONTENT_KEY));
for (const outcome of ['confirmed', 'rolled-back']) {
    const root = await realpath(await mkdtemp(path.join(os.tmpdir(), 'mindbattle-packaged-shell-')));
    const user = path.join(root, 'user');
    await mkdir(user);
    let game;
    const server = createServer((req, res) => { const url = req.url; if (url === '/releases') { const m = JSON.parse(envelope.payload); res.setHeader('content-type','application/json'); res.end(JSON.stringify([{tag_name:`shell-${m.sequence}`,draft:false,prerelease:false,assets:[{name:'darwin-universal-latest.json',state:'uploaded',browser_download_url:`${m.objectBaseUrl}/darwin-universal-latest.json`},...m.files.map(f=>({name:f.sha256,size:f.size,state:'uploaded'}))]}])); }
    else if (url === '/desktop/shell/darwin-universal/latest.json' || url?.endsWith('/darwin-universal-latest.json')) {
        res.setHeader('content-type', 'application/json');
        res.end(JSON.stringify(envelope));
    }
    else {
        const file = objects.get(url?.split('/').at(-1));
        if (file) {
            res.setHeader('content-length', file.size);
            createReadStream(file.source).pipe(res);
        }
        else {
            res.writeHead(503);
            res.end();
        }
    } });
    let envelope;
    const objects = new Map();
    await new Promise(r => server.listen(0, '127.0.0.1', r));
    const origin = `http://127.0.0.1:${server.address().port}`;
    try {
        const old = path.join(root, 'Mindbattle.app'), next = path.join(root, 'Next.app');
        await cp('desktop-installers/mac-universal/Mindbattle.app', old, { recursive: true, dereference: false, verbatimSymlinks: true, mode: constants.COPYFILE_FICLONE });
        async function patch(app, version, broken = false) { const archive = path.join(app, 'Contents/Resources/app.asar'), unpacked = path.join(root, 'unpacked'); await rm(unpacked, { recursive: true, force: true }); asar.extractAll(archive, unpacked); await writeFile(path.join(unpacked, 'desktop/shell.mjs'), await readFile('desktop/shell.mjs'));
            await writeFile(path.join(unpacked, 'desktop/config.json'), JSON.stringify({ shellVersion: version, origin, updateOrigin:'https://afonasev.github.io/mindbattle' })); await writeFile(path.join(unpacked, 'desktop/main.mjs'), `const fixtureFetch=globalThis.fetch; globalThis.fetch=(url,options)=>{const u=String(url);if(u.startsWith('https://api.github.com/repos/afonasev/mindbattle/releases'))return fixtureFetch('${origin}/releases',options);if(u.startsWith('https://github.com/afonasev/mindbattle/releases/download/'))return fixtureFetch('${origin}/'+u.split('/').at(-1),options);return fixtureFetch(url,options);};\n` + await readFile('desktop/main.mjs','utf8'));
            if (broken)
            await writeFile(path.join(unpacked, 'desktop/main.mjs'), `import {app} from 'electron'; app.whenReady().then(()=>app.quit());`); await asar.createPackage(unpacked, archive); asar.uncache(archive); await rm(unpacked, { recursive: true, force: true }); }
        await patch(old, '1.0.6');
        await cp(old, next, { recursive: true, dereference: false, verbatimSymlinks: true, mode: constants.COPYFILE_FICLONE });
        await patch(next, '1.0.7', outcome === 'rolled-back');
        const files = [], links = [];
        async function walk(dir, rel = '') { for (const e of await readdir(dir, { withFileTypes: true })) {
            const name = rel ? `${rel}/${e.name}` : e.name, source = path.join(dir, e.name);
            if (e.isSymbolicLink())
                links.push({ path: name, target: await readlink(source) });
            else if (e.isDirectory())
                await walk(source, name);
            else {
                const info = await stat(source), sha256 = await fileHash(source);
                files.push({ path: name, sha256, size: info.size, mode: info.mode & 0o111 ? 0o755 : 0o644 });
                objects.set(sha256, { source, size: info.size });
            }
        } }
        await walk(next);
        const sequence = Date.now();
        const payload = JSON.stringify({ objectBaseUrl:releaseBase('shell',sequence), channel:'stable', publishedAt:new Date().toISOString(), format: 1, product: 'tech.afonasev.mindbattle', sequence, version: '1.0.7', platform: 'darwin-universal', helper: 1, entry: 'Contents/MacOS/Mindbattle', files, links });
        envelope = { payload, signature: sign(null, Buffer.from(payload), key).toString('base64') };
        await writeFile(path.join(user, 'display.json'), JSON.stringify({ width: 1024, height: 768, fullscreen: false }));
        game = await _electron.launch({ executablePath: path.join(old, 'Contents/MacOS/Mindbattle'), args: [`--user-data-dir=${user}`, "-muted", "--mute-audio"], timeout: 30000 });
        game.process().stderr.on("data", bytes => process.stderr.write(bytes));
        game.process().stdout.on("data", bytes => process.stdout.write(bytes));
        const page = await game.firstWindow();
        await page.waitForSelector('text=Mindbattle');
        await page.getByRole('button', { name: /^(?:(?:Доступно обновление · )?Обновить|Обновить)$/ }).waitFor({ timeout: 180000 });
        await page.screenshot({ path: path.join(evidence, `shell-${outcome}-ready.png`) });
        await page.getByRole('button', { name: /^(?:(?:Доступно обновление · )?Обновить|Обновить)$/ }).click();
        await page.getByRole('button', {name:'Перезапустить',exact:true}).waitFor({timeout:180000});
        await page.getByRole('button', {name:'Перезапустить',exact:true}).click();
        let journal; let disconnected=false;
        for (let i = 0; i < 1200; i++) {
            try {
                const dirs = await readdir(path.join(user, 'shell/transactions'));
                journal = JSON.parse(await readFile(path.join(user, 'shell/transactions', dirs[0], 'journal.json')));
                if(journal.phase==='prepared'&&!disconnected){await readFile(path.join(user,'shell/transactions',dirs[0],'started'));disconnected=true;await game.close().catch(()=>{});}
                if (['confirmed', 'rolled-back', 'error', 'recovery-required'].includes(journal.phase))
                    break;
            }
            catch { }
            await new Promise(r => setTimeout(r, 100));
        }
        assert.equal(journal?.phase, outcome);
        asar.uncache(path.join(old, 'Contents/Resources/app.asar'));
        const config = JSON.parse(asar.extractFile(path.join(old, 'Contents/Resources/app.asar'), 'desktop/config.json').toString());
        assert.equal(config.shellVersion, outcome === 'confirmed' ? '1.0.7' : '1.0.6');
        assert.deepEqual(JSON.parse(await readFile(path.join(user, 'display.json'))), { width: 1024, height: 768, fullscreen: false });
        await writeFile(path.join(evidence, `shell-${outcome}.json`), JSON.stringify({ phase: journal.phase, version: config.shellVersion, profilePreserved: true, realPackagedApp: true }, null, 2));
        console.log(`Packaged shell ${outcome}: ${config.shellVersion}, same installation path and user profile`);
    }
    finally {
        await game?.close().catch(() => { });
        const lines = execFileSync('/bin/ps', ['-axo', 'pid=,command='], { encoding: 'utf8' }).split('\n');
        for (const line of lines) {
            const match = line.trim().match(/^(\d+)\s+(.*)$/);
            if (match && match[2].startsWith(root + '/')) {
                try {
                    process.kill(Number(match[1]), 'SIGKILL');
                }
                catch { }
            }
        }
        await new Promise(r => server.close(r));
        await rm(root, { recursive: true, force: true });
    }
}
