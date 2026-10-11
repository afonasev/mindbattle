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
  const timer = timers.setInterval(run, 5 * 60 * 1000);
  return () => timers.clearInterval(timer);
}
