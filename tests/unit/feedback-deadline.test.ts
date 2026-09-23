import { afterEach, describe, expect, it, vi } from "vitest";
import { sendFeedbackWithinDeadline } from "../../src/feedback/deadline";

afterEach(() => vi.useRealTimers());

describe("feedback attempt deadline", () => {
  it("shows failure after exactly three seconds when the request never answers", async () => {
    vi.useFakeTimers();
    let signal: AbortSignal | undefined;
    let settled = false;
    const attempt = sendFeedbackWithinDeadline(async (nextSignal) => {
      signal = nextSignal;
      await new Promise<void>(() => {});
    }).catch(() => { settled = true; });
    await vi.advanceTimersByTimeAsync(2_999);
    expect(settled).toBe(false);
    expect(signal?.aborted).toBe(false);
    await vi.advanceTimersByTimeAsync(1);
    await attempt;
    expect(settled).toBe(true);
    expect(signal?.aborted).toBe(true);
  });

  it("waits three seconds before showing a quick server error", async () => {
    vi.useFakeTimers();
    const attempt = sendFeedbackWithinDeadline(async () => { throw new Error("500"); });
    let settled = false;
    const result = attempt.catch((error: Error) => { settled = true; return error.message; });
    await vi.advanceTimersByTimeAsync(2_999);
    expect(settled).toBe(false);
    await vi.advanceTimersByTimeAsync(1);
    expect(await result).toBe("500");
  });

  it("accepts an immediate success without waiting", async () => {
    vi.useFakeTimers();
    await expect(sendFeedbackWithinDeadline(async () => {})).resolves.toBeUndefined();
    expect(vi.getTimerCount()).toBe(0);
  });
});
