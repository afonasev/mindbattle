export const updateOrigin = 'https://afonasev.github.io/mindbattle';
export const releaseBase = (kind, sequence) => `https://github.com/afonasev/mindbattle/releases/download/${kind}-${sequence}`;
export function validPublishedAt(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/.test(value) || !Number.isFinite(Date.parse(value))) return false;
  const canonical = new Date(value).toISOString();
  return canonical === value || canonical.replace('.000Z', 'Z') === value;
}

// This field is inside the signed payload. A feed cannot select another repository,
// channel or release, even when its metadata is otherwise valid.
export function objectBase(manifest, kind, origin) {
  if (manifest.objectBaseUrl !== undefined) {
    if (manifest.objectBaseUrl !== releaseBase(kind, manifest.sequence)) throw Error('Invalid update object source');
    return manifest.objectBaseUrl;
  }
  if (origin === updateOrigin) throw Error('GitHub update object source missing');
  return `${origin}/desktop/${kind}/objects`; // Existing signed offline/VPS bundles.
}

export async function fetchUpdate(fetcher, url, options = {}) {
  if (!url.startsWith('https://github.com/afonasev/mindbattle/releases/download/')) {
    return fetcher(url, { ...options, redirect: 'error' });
  }
  let next = new URL(url);
  for (let hop = 0; hop < 5; hop++) {
    if (next.protocol !== 'https:' || next.username || next.password || next.port ||
        !(next.hostname === 'github.com' && next.pathname.startsWith('/afonasev/mindbattle/releases/download/') ||
          ['release-assets.githubusercontent.com', 'objects.githubusercontent.com'].includes(next.hostname))) {
      throw Error('Unsafe update redirect');
    }
    const response = await fetcher(next.href, { ...options, redirect: 'manual' });
    if (![301, 302, 303, 307, 308].includes(response.status)) return response;
    const location = response.headers.get('location');
    await response.body?.cancel();
    if (!location) throw Error('Missing update redirect');
    next = new URL(location, next);
  }
  throw Error('Too many update redirects');
}
