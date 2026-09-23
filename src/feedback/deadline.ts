export const FEEDBACK_SEND_TIMEOUT_MS = 3_000;

/** Wait the full attempt window before reporting an early failure. */
export async function sendFeedbackWithinDeadline(
  send: (signal: AbortSignal) => Promise<void>,
  timeoutMs = FEEDBACK_SEND_TIMEOUT_MS,
): Promise<void> {
  const controller = new AbortController();
  let timer: ReturnType<typeof setTimeout> | undefined;
  const deadline = new Promise<never>((_, reject) => {
    timer = setTimeout(() => {
      controller.abort();
      reject(new Error("Отправка фидбэка временно недоступна"));
    }, timeoutMs);
  });
  try {
    await Promise.race([send(controller.signal), deadline]);
  } catch (error) {
    // A quick network/validation error gets the same three-second wait as a
    // request that never answers. The deadline also aborts an HTTP request.
    await deadline.catch(() => undefined);
    throw error;
  } finally {
    if (timer !== undefined) clearTimeout(timer);
  }
}
