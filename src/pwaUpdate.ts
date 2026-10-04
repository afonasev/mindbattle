export function canApplyPwaUpdate(matchActive: boolean, soloPhase: string | null): boolean {
  return !matchActive && (soloPhase === null || soloPhase === "finished");
}

export async function checkForPwaUpdate(
  registration: Pick<ServiceWorkerRegistration, "update"> | undefined
): Promise<void> {
  await registration?.update();
}

// update() can resolve before the worker finishes downloading its precache.
export function findPwaUpdate(registration: ServiceWorkerRegistration, timeoutMs = 60_000): Promise<boolean> {
  if (registration.waiting) return Promise.resolve(true);
  return new Promise((resolve, reject) => {
    const workers = new Set<ServiceWorker>();
    let checked = false;
    let finished = false;
    const timer = setTimeout(() => finish(new Error("Загрузка обновления заняла слишком много времени. Попробуйте ещё раз.")), timeoutMs);
    function finish(error?: Error, ready = false) {
      if (finished) return;
      finished = true;
      clearTimeout(timer);
      registration.removeEventListener("updatefound", inspect);
      workers.forEach(worker => worker.removeEventListener("statechange", inspect));
      if (error) reject(error); else resolve(ready);
    }
    function inspect() {
      if (finished) return;
      const worker = registration.installing;
      if (worker && !workers.has(worker)) {
        workers.add(worker);
        worker.addEventListener("statechange", inspect);
      }
      if ([...workers].some(candidate => candidate.state === "redundant")) {
        finish(new Error("Не удалось загрузить обновление. Попробуйте ещё раз."));
      } else if (registration.waiting) {
        finish(undefined, true);
      } else if (checked && (!worker || worker.state === "activated")) {
        finish();
      }
    }
    registration.addEventListener("updatefound", inspect);
    inspect();
    void registration.update().then(() => { checked = true; inspect(); }, (error: unknown) => {
      finish(error instanceof Error ? error : new Error("Не удалось проверить обновления."));
    });
  });
}
