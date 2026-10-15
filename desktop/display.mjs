// Persist only confirmed settings. Timer and cancellation live in the main process.
export function createDisplayController({ initial, apply, persist, seconds = 15, timers = { setTimeout, clearTimeout } }) {
  let current = { ...initial }, trial, timer;
  let writing = Promise.resolve();
  const queue = operation => { const next = writing.then(operation); writing = next.catch(() => {}); return next; };
  const cancel = () => queue(async () => { if (timer) timers.clearTimeout(timer); timer = undefined; if (trial) await apply(current); trial = undefined; return current; });
  return {
    value: () => ({ ...current }),
    preview: next => queue(async () => {
      if (timer) timers.clearTimeout(timer);
      try { await apply(next); } catch (cause) { await apply(current); throw cause; }
      trial = { ...next };
      timer = timers.setTimeout(() => { void cancel(); }, seconds * 1000);
      return { ...trial };
    }),
    confirm: () => queue(async () => {
      if (!trial) return { ...current };
      const next = trial;
      try { await persist(next); current = { ...next }; }
      catch (cause) { await apply(current); throw cause; }
      finally { if (timer) timers.clearTimeout(timer); trial = undefined; timer = undefined; }
      return { ...current };
    }),
    cancel,
  };
}
