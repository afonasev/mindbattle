import { readFile } from 'node:fs/promises';
import { atomicJson, boundedBytes } from './content.mjs';
import { fetchUpdate, releaseBase } from './updateTransport.mjs';
const api = 'https://api.github.com/repos/afonasev/mindbattle';
export const releaseManifestName = (kind, platform) => kind === 'shell' ? `${platform}-latest.json` : 'latest.json';

export class ReleaseCatalog {
  constructor({ cache, fetcher = fetch }) { Object.assign(this, { cache, fetcher }); this.cacheWrites = Promise.resolve(); }
  async list({ signal } = {}) {
    signal?.throwIfAborted();
    let stored = {};
    try { stored = JSON.parse(await readFile(this.cache, 'utf8')); } catch { /* no cache */ }
    const releases = [];
    const pages = {};
    // GitHub permits up to 100 per page. Bound discovery to 1000 recent releases.
    for (let page = 1; page <= 10; page++) {
      const url = `${api}/releases?per_page=100&page=${page}`;
      const old = stored.pages?.[page];
      const response = await this.fetcher(url, { headers: { Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28', ...(old?.etag ? { 'If-None-Match': old.etag } : {}) }, signal: signal ? AbortSignal.any([signal, AbortSignal.timeout(30000)]) : AbortSignal.timeout(30000), redirect: 'error' });
      let items;
      if (response.status === 304 && Array.isArray(old?.items)) items = old.items;
      else {
        if (!response.ok) throw Error('GitHub недоступен или исчерпан лимит запросов.');
        items = JSON.parse((await boundedBytes(response, 16 * 1024 ** 2)).toString());
        if (!Array.isArray(items)) throw Error('Некорректный каталог GitHub Releases.');
      }
      pages[page] = { etag: response.headers.get('etag') ?? old?.etag, items };
      releases.push(...items.filter(r => !r.draft && !r.prerelease));
      if (items.length < 100) break;
    }
    signal?.throwIfAborted();
    this.cacheWrites = this.cacheWrites.catch(() => {}).then(() => atomicJson(this.cache, { pages }));
    await this.cacheWrites;
    return releases;
  }
  async candidate(stores) {
    const signal = undefined;
    const releases = await this.list();
    for (const kind of ['shell', 'content']) {
      const store = stores[kind];
      const ordered = releases.filter(r => new RegExp(`^${kind}-[1-9][0-9]*$`).test(r.tag_name)).sort((a,b) => Number(b.tag_name.split('-')[1]) - Number(a.tag_name.split('-')[1]));
      for (const release of ordered) {
        const sequence = Number(release.tag_name.split('-')[1]);
        if (sequence <= store.state.highWater) continue;
        const name = releaseManifestName(kind, store.platform);
        const asset = release.assets?.find(a => a.name === name && a.state === 'uploaded');
        const base = releaseBase(kind, sequence);
        if (!asset || asset.browser_download_url !== `${base}/${name}`) continue;
        const raw = await boundedBytes(await fetchUpdate(this.fetcher, asset.browser_download_url, { signal: signal ? AbortSignal.any([signal, AbortSignal.timeout(30000)]) : AbortSignal.timeout(30000) }), 8 * 1024 ** 2);
        let candidate;
        try { candidate = store.candidate(raw); } catch { continue; }
        if (!candidate) continue;
        if (candidate.manifest.sequence !== sequence || candidate.manifest.objectBaseUrl !== base) throw Error('Релиз не соответствует подписанным метаданным.');
        // A published but incomplete release must never be offered.
        if (!candidate.manifest.files.every(f => release.assets.some(a => a.name === f.sha256 && a.state === 'uploaded' && a.size === f.size))) continue;
        return { ...candidate, kind, release: { tag: release.tag_name, date: release.published_at, body: release.body ?? '' } };
      }
    }
    return null;
  }
  async history(installedTag, installedInfo = {}, signal) {
    const releases = await this.list({ signal });
    const history = releases.slice(0, 8);
    if (installedTag && !history.some(r => r.tag_name === installedTag)) {
      let installed = releases.find(r => r.tag_name === installedTag);
      if (!installed) {
        const response = await this.fetcher(`${api}/releases/tags/${encodeURIComponent(installedTag)}`, { headers: { Accept: 'application/vnd.github+json' }, signal: signal ? AbortSignal.any([signal, AbortSignal.timeout(30000)]) : AbortSignal.timeout(30000), redirect: 'error' });
        if (response.status === 404) installed = { tag_name: installedTag, name: installedInfo.version || installedTag, published_at: installedInfo.publishedAt, body: '## Русский\nОписание этой установленной версии отсутствует в GitHub Releases.\n\n## English\nRelease notes for this installed version are unavailable on GitHub.' };
        else { if (!response.ok) throw Error('Не удалось получить историю установленной версии.'); installed = JSON.parse((await boundedBytes(response, 2 * 1024 ** 2)).toString()); }
      }
      if (!installed.draft && !installed.prerelease) history.push(installed);
    }
    return history.map(r => ({ tag: r.tag_name, version: r.name || r.tag_name, date: r.published_at, body: r.body || '' }));
  }
}
export function localizedNotes(body, language = 'ru') {
  const heading = language === 'ru' ? /(?:^|\n)##\s+(?:Русский|Russian|RU)\s*\n/i : /(?:^|\n)##\s+(?:English|EN)\s*\n/i;
  const match = heading.exec(body);
  if (!match) return language === 'ru' ? 'Описание на русском языке отсутствует.' : 'English description is unavailable.';
  return body.slice(match.index + match[0].length).split(/\n##\s+/)[0].trim();
}
