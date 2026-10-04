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
      if (ready) onReady();
      else if (error) throw new Error("Не удалось проверить обновления. Проверьте подключение и попробуйте ещё раз.", { cause: error });
      return { ready };
    })().finally(() => { pending = undefined; });
    return pending;
  };
}
