import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { createPublicKey } from 'node:crypto';
import { execFileSync } from 'node:child_process';
const pin = createPublicKey(await readFile('desktop/content-public.pem')).export({ type: 'spki', format: 'der' }).toString('base64');
await mkdir('desktop/helper-bin', { recursive: true });
for (const [os, arch, name] of [['darwin', 'arm64', 'updater-arm64'], ['darwin', 'amd64', 'updater-x64'], ['windows', 'amd64', 'updater.exe']]) {
    execFileSync('go', ['build', '-trimpath', '-ldflags', `-s -w -X main.pinnedKey=${pin}`, '-o', `../helper-bin/${name}`, '.'], { cwd: 'desktop/updater', env: { ...process.env, GOOS: os, GOARCH: arch, CGO_ENABLED: '0' }, stdio: 'inherit' });
}
execFileSync('lipo', ['-create', 'desktop/helper-bin/updater-arm64', 'desktop/helper-bin/updater-x64', '-output', 'desktop/helper-bin/updater']);
await writeFile('desktop/install-identity.json', JSON.stringify({ product: 'tech.afonasev.mindbattle', pin, helper: 1 }));
console.log('Native updater compiled for macOS universal and Windows x64');
