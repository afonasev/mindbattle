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
      if (ready) { await onReady(); emit({ phase: 'ready', version: await pendingUpdateVersion(shellStore, contentStore) }); }
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
  if (shellStore.state.pending) return (await shellStore.pendingManifest()).version;
  if (contentStore.state.pending) {
    const manifest = await contentStore.manifestAt(contentStore.directory(contentStore.state.pending));
    return manifest.version;
  }
}
