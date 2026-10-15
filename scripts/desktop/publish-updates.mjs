import { releaseNotes } from "./release-notes.mjs";
// Explicit publication only. Build and web-deploy never invoke this script.
import { execFileSync } from 'node:child_process';
import { readFile, writeFile, mkdir, mkdtemp, rm, cp } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { checkManifest } from '../../desktop/content.mjs';
import { shellManifest, fileHash } from '../../desktop/shell.mjs';
import { objectBase, updateOrigin, validPublishedAt } from '../../desktop/updateTransport.mjs';

const repo = 'afonasev/mindbattle';
const branch = 'desktop-updates';
const execute = (command, args, cwd) => execFileSync(command, args, { cwd, encoding: 'utf8', maxBuffer: 32 * 1024 ** 2 });

export function checkAssets(assets, expected) {
  for (const file of expected) {
    const asset = assets.find(a => a.name === file.name);
    if (!asset || asset.size !== file.size || asset.digest !== `sha256:${file.sha256}`) {
      throw Error(`GitHub asset integrity mismatch: ${file.name}; feed retained`);
    }
  }
}

export function checkAdvance(previous, candidate) {
  if (previous.sequence > candidate.sequence || previous.sequence === candidate.sequence && JSON.stringify(previous) !== JSON.stringify(candidate)) {
    throw Error('Update sequence must advance; feed retained');
  }
}

export async function publishUpdates(kind, { cwd = process.cwd(), run = execute, fetcher = fetch } = {}) {
  if (!['content', 'shell'].includes(kind)) throw Error('Expected content|shell');
  const git = (...args) => run('git', args, cwd).trim();
  const gh = (...args) => run('gh', args, cwd);
  if (git('status', '--porcelain')) throw Error('Publication requires a clean source checkout');
  const commit = git('rev-parse', 'HEAD');
  const remoteMain = git('ls-remote', '--heads', 'origin', 'main').split(/\s/)[0];
  if (remoteMain !== commit) throw Error('Publication must use the verified origin/main revision');
  const config = JSON.parse(await readFile(path.join(cwd, 'desktop/config.json'), 'utf8'));
  if (config.updateOrigin !== updateOrigin) throw Error('Unexpected GitHub update origin');
  const key = await readFile(path.join(cwd, 'desktop/content-public.pem'), 'utf8');
  const names = kind === 'content' ? ['latest.json'] : ['darwin-universal/latest.json', 'win32-x64/latest.json'];
  const manifests = [];
  const expected = new Map();
  for (const name of names) {
    const source = path.join(cwd, 'desktop-release', kind, name);
    const envelope = JSON.parse(await readFile(source, 'utf8'));
    const m = kind === 'content' ? checkManifest(envelope, key, config.shellVersion) : shellManifest(envelope, key, name.split('/')[0]);
    objectBase(m, kind, updateOrigin);
    if (!validPublishedAt(m.publishedAt)) throw Error('Publication requires MINDBATTLE_PUBLISHED_AT in the signed manifest');
    if (kind === 'shell' && m.version !== config.shellVersion) throw Error('Shell version mismatch');
    manifests.push({ name, source, envelope, manifest: m });
    for (const f of m.files) {
      if (expected.has(f.sha256) && expected.get(f.sha256).size !== f.size) throw Error('Conflicting object sizes');
      expected.set(f.sha256, { name: f.sha256, size: f.size, sha256: f.sha256, source: path.join(cwd, 'desktop-release', kind, 'objects', f.sha256) });
    }
  }
  if (manifests.some(m => m.manifest.sequence !== manifests[0].manifest.sequence)) throw Error('Shell platforms must share a sequence');
  const tag = `${kind}-${manifests[0].manifest.sequence}`;
  for (const m of manifests) expected.set(m.name.replaceAll('/', '-'), {
    name: m.name.replaceAll('/', '-'), source: m.source, sha256: await fileHash(m.source), size: Buffer.byteLength(await readFile(m.source)),
  });
  if (expected.size > 1000) throw Error('Release exceeds GitHub limit of 1000 assets');
  // Verify all local bytes before any external mutation, including direct CLI use.
  for (const f of expected.values()) {
    const { size } = await (await import('node:fs/promises')).stat(f.source);
    if (size !== f.size || await fileHash(f.source) !== f.sha256) throw Error(`Invalid local update object: ${f.name}`);
  }
  const temporary = await mkdtemp(path.join(os.tmpdir(), 'mindbattle-update-publish-'));
  const pg = (...args) => run('git', args, temporary).trim();
  try {
    pg('init', '--quiet');
    pg('remote', 'add', 'origin', git('remote', 'get-url', 'origin'));
    const exists = pg('ls-remote', '--heads', 'origin', branch);
    if (exists) { pg('fetch', '--quiet', '--depth=1', 'origin', branch); pg('checkout', '--quiet', '-b', branch, 'FETCH_HEAD'); }
    else pg('checkout', '--quiet', '--orphan', branch);
    pg('config', 'user.name', git('config', 'user.name'));
    pg('config', 'user.email', git('config', 'user.email'));
    for (const m of manifests) {
      const target = path.join(temporary, 'desktop', kind, m.name);
      let previous;
      try { previous = JSON.parse(await readFile(target, 'utf8')); } catch (e) { if (e.code !== 'ENOENT') throw e; }
      if (previous) {
        const prior = kind === 'content' ? checkManifest(previous, key, config.shellVersion) : shellManifest(previous, key, m.manifest.platform);
        checkAdvance(prior, m.manifest);
      }
    }
    // Pages configuration is inspected before uploading anything. Never overwrite another site.
    let pagesResult;
    try { pagesResult = run('gh', ['api', '--include', `repos/${repo}/pages`], cwd); }
    catch (error) {
      pagesResult = String(error.stdout || '');
      if (!/HTTP\/[^ ]+ 404\b/.test(pagesResult)) throw error;
    }
    const status = Number(pagesResult.match(/HTTP\/[^ ]+ (\d+)/)?.[1]);
    const pages = status === 200 ? JSON.parse(pagesResult.slice(pagesResult.indexOf('{'))) : null;
    if (status !== 200 && status !== 404) throw Error('Cannot inspect GitHub Pages');
    if (pages && (pages.build_type !== 'legacy' || pages.source?.branch !== branch || pages.source?.path !== '/' || pages.cname)) {
      throw Error('GitHub Pages already has another publishing source; retained');
    }
    const releases = JSON.parse(gh('api', '--paginate', '--slurp', `repos/${repo}/releases?per_page=100`)).flat();
    let release = releases.find(r => r.tag_name === tag);
    if (!release) {
      gh('release', 'create', tag, '--repo', repo, '--target', commit, '--draft', '--title', `Mindbattle ${kind} ${manifests[0].manifest.version}`, '--notes', releaseNotes({ cwd, channel: kind, revision: commit, run: args => git(...args) }));
      release = JSON.parse(gh('api', '--paginate', '--slurp', `repos/${repo}/releases?per_page=100`)).flat().find(r => r.tag_name === tag);
    }
    if (!release) throw Error('Release missing after creation');
    if (release.draft && release.target_commitish !== commit) throw Error('Draft belongs to another source revision');
    const assets = () => JSON.parse(gh('api', '--paginate', '--slurp', `repos/${repo}/releases/${release.id}/assets?per_page=100`)).flat();
    const existing = assets();
    // Existing bytes are never overwritten, including a partially uploaded draft.
    for (const f of expected.values()) {
      if (existing.some(a => a.name === f.name)) checkAssets(existing, [f]);
      else {
        if (!release.draft) throw Error(`Published release is incomplete: ${f.name}`);
        const upload = path.join(temporary, 'upload', f.name);
        await mkdir(path.dirname(upload), { recursive: true });
        await cp(f.source, upload);
        gh('release', 'upload', tag, upload, '--repo', repo);
        await rm(upload);
      }
    }
    checkAssets(assets(), [...expected.values()]);
    if (release.draft) gh('release', 'edit', tag, '--repo', repo, '--draft=false', '--latest=false');
    const tagRef = JSON.parse(gh('api', `repos/${repo}/git/ref/tags/${tag}`));
    if (tagRef.object?.type !== 'commit' || tagRef.object.sha !== commit) throw Error('Release tag source mismatch; feed retained');
    for (const m of manifests) {
      const target = path.join(temporary, 'desktop', kind, m.name);
      await mkdir(path.dirname(target), { recursive: true }); await cp(m.source, target);
    }
    await writeFile(path.join(temporary, '.nojekyll'), '');
    await writeFile(path.join(temporary, 'index.html'), '<!doctype html><meta charset="utf-8"><title>Mindbattle updates</title>Signed desktop update feeds.');
    // Only metadata goes into Git/Pages; upload staging never enters the branch.
    pg('add', 'desktop', '.nojekyll', 'index.html');
    if (pg('status', '--porcelain')) pg('commit', '--quiet', '-m', `Publish ${tag} from ${commit}`);
    pg('push', 'origin', `HEAD:refs/heads/${branch}`); // No force: concurrent publishers fail safely.
    const tip = pg('rev-parse', 'HEAD');
    if (pg('ls-remote', '--heads', 'origin', branch).split(/\s/)[0] !== tip) throw Error('Pages branch changed concurrently; inspect before retry');
    if (!pages) {
      const input = path.join(temporary, 'pages.json');
      await writeFile(input, JSON.stringify({ build_type: 'legacy', source: { branch, path: '/' } }));
      gh('api', '--method', 'POST', `repos/${repo}/pages`, '--input', input);
    }
    console.log(`Uploaded and committed ${tag}; waiting for Pages ${tip}`);
    // A branch push is not proof the public endpoint serves the new signed bytes.
    const deadline = Date.now() + 5 * 60_000;
    while (Date.now() < deadline) {
      let visible = true;
      for (const m of manifests) {
        try {
          const response = await fetcher(`${updateOrigin}/desktop/${kind}/${m.name}`, { cache: 'no-store', redirect: 'error', signal: AbortSignal.timeout(15_000) });
          if (!response.ok || await response.text() !== await readFile(m.source, 'utf8')) visible = false;
        } catch { visible = false; }
      }
      if (visible) { console.log(`Verified public ${kind} feed: ${tag}; source ${commit}; Pages ${tip}`); return; }
      await new Promise(resolve => setTimeout(resolve, 5000));
    }
    throw Error('GitHub assets/branch preserved, but public Pages readback is pending. Retry these exact files.');
  } finally { await rm(temporary, { recursive: true, force: true }); }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await publishUpdates(process.argv[2]);
}
