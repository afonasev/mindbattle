export type UpdateResult = "current" | "applied" | "deferred";

export async function runManualUpdate({ check, apply, isSafe, onApplying }: {
  check: () => Promise<boolean>;
  apply: () => Promise<void>;
  isSafe: () => boolean;
  onApplying: () => void;
}): Promise<UpdateResult> {
  const ready = await check();
  if (!isSafe()) return "deferred";
  if (!ready) return "current";
  onApplying();
  await apply();
  return "applied";
}

export async function withUpdateTimeout<T>(task: Promise<T>, timeoutMs: number): Promise<T> {
  let timer: ReturnType<typeof setTimeout> | undefined;
  try {
    return await Promise.race([task, new Promise<never>((_, reject) => {
      timer = setTimeout(() => reject(new Error("Проверка обновления заняла слишком много времени. Попробуйте ещё раз.")), timeoutMs);
    })]);
  } finally {
    clearTimeout(timer);
  }
}
