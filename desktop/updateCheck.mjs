// Startup, timer and manual requests await the same download.
export function createUpdateCheck(shellStore, contentStore, onReady, onStatus = () => {}) {
  let pending;
  let status = { phase: 'idle' };
  const emit = value => { status = value; onStatus(value); };
  const check = () => {
    if (pending) return pending;
    emit({ phase: 'checking' });
    pending = (async () => {
      let error;
      let ready = Boolean(shellStore.state.pending || contentStore.state.pending);
      if (!ready) {
        try { ready = await shellStore.check(emit); } catch (cause) { error = cause; }
        if (!ready) {
          try { ready = await contentStore.check(emit); } catch (cause) { error = cause; }
        }
      }
      if (ready) { await onReady(); emit({ phase: 'ready', ...await pendingUpdateInfo(shellStore, contentStore) }); }
      else if (error) throw new Error("Не удалось проверить обновления. Проверьте подключение и попробуйте ещё раз.", { cause: error });
      else emit({ phase: 'current' });
      return { ready };
    })().catch(error => { emit({ phase: 'error', message: error.message }); throw error; }).finally(() => { pending = undefined; });
    return pending;
  };
  check.status = () => status;
  return check;
}

// Follow the same priority as desktop:apply and use verified pending metadata.
export async function pendingUpdateVersion(shellStore, contentStore) {
  return (await pendingUpdateInfo(shellStore, contentStore))?.version;
}
export async function pendingUpdateInfo(shellStore, contentStore) {
  let manifest;
  if (shellStore.state.pending) manifest = await shellStore.pendingManifest();
  if (contentStore.state.pending) {
    if (!manifest) manifest = await contentStore.manifestAt(contentStore.directory(contentStore.state.pending));
  }
  return manifest ? { version: manifest.version, publishedAt: manifest.publishedAt ?? undefined } : undefined;
}

export function startAutomaticUpdateChecks(check, onError, timers = { setInterval, clearInterval }) {
  const run = () => { void check().catch(onError); };
  run();
  return () => {};
}

// Discovery is a single immutable promise per process. Downloads only use its selected bytes.
export function createUpdateCoordinator({ shellStore, contentStore, catalog, onReady = () => {}, onStatus = () => {} }) {
  const stores = { shell: shellStore, content: contentStore };
  let discovery, candidate, transfer, abort, safe = false, consent = false;
  let status = { phase: 'idle' };
  const emit = next => { status = { ...next }; onStatus(status); };
  const ready = async () => { const info = await pendingUpdateInfo(shellStore, contentStore); await onReady(info); emit({ phase: 'ready', ...info }); };
  const start = () => discovery ??= (async () => {
    emit({ phase: 'checking' });
    if (shellStore.state.pending || contentStore.state.pending) { await ready(); return; }
    try {
      candidate = await catalog.candidate(stores);
      emit(candidate ? { phase: 'available', version: candidate.manifest.version, publishedAt: candidate.manifest.publishedAt } : { phase: 'current' });
    } catch (cause) { emit({ phase: 'error', message: 'Не удалось проверить обновления. Следующая проверка — при запуске игры.' }); }
  })();
  const download = () => {
    if (transfer || !candidate || !consent || !safe || status.phase === 'ready') return transfer;
    abort = new AbortController();
    const signal = abort.signal;
    transfer = (async () => {
      try {
        const total = candidate.manifest.files.reduce((sum, f) => sum + f.size, 0);
        const { mkdir, statfs } = await import('node:fs/promises');
        const store = stores[candidate.kind];
        await mkdir(store.root, { recursive: true });
        const disk = await statfs(store.root);
        if (disk.bavail * disk.bsize < total * 2 + 64 * 1024 ** 2) throw Error('Недостаточно места для обновления.');
        signal.throwIfAborted();
        emit({ phase: 'downloading', version: candidate.manifest.version, completed: 0, total: candidate.manifest.files.length });
        await store.check(value => emit(value), { raw: candidate.raw, signal });
        signal.throwIfAborted();
        emit({ phase: 'verifying', version: candidate.manifest.version });
        await ready();
      } catch (cause) {
        if (signal.aborted) emit({ phase: consent ? 'paused' : 'available', version: candidate.manifest.version });
        else emit({ phase: 'download-error', version: candidate.manifest.version, message: cause.message });
      } finally { transfer = undefined; abort = undefined; }
    })();
    return transfer;
  };
  return {
    start, status: () => status,
    async setSafe(value) {
      safe = value === true;
      if (!safe && transfer) { abort?.abort(); await transfer; }
      if (safe && consent && status.phase === 'paused') void download();
    },
    async download() { await start(); if (!candidate || !safe) return false; consent = true; void download(); return true; },
    async cancel() { consent = false; abort?.abort(); await transfer; if (candidate && status.phase !== 'ready') emit({ phase: 'available', version: candidate.manifest.version }); },
    stop() { consent = false; abort?.abort(); },
  };
}
