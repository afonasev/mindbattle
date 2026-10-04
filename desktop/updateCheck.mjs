// Startup, timer and manual requests await the same download.
export function createUpdateCheck(shellStore, contentStore, onReady) {
  let pending;
  return () => {
    if (pending) return pending;
    pending = (async () => {
      let error;
      let ready = Boolean(shellStore.state.pending || contentStore.state.pending);
      if (!ready) {
        try { ready = await shellStore.check(); } catch (cause) { error = cause; }
        if (!ready) {
          try { ready = await contentStore.check(); } catch (cause) { error = cause; }
        }
      }
      if (ready) await onReady();
      else if (error) throw new Error("Не удалось проверить обновления. Проверьте подключение и попробуйте ещё раз.", { cause: error });
      return { ready };
    })().finally(() => { pending = undefined; });
    return pending;
  };
}

// Follow the same priority as desktop:apply and use verified pending metadata.
export async function pendingUpdateVersion(shellStore, contentStore) {
  if (shellStore.state.pending) return (await shellStore.pendingManifest()).version;
  if (contentStore.state.pending) {
    const manifest = await contentStore.manifestAt(contentStore.directory(contentStore.state.pending));
    return manifest.version;
  }
}
