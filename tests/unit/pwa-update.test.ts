import { describe, expect, it, vi } from "vitest";
import { canApplyPwaUpdate, checkForPwaUpdate } from "../../src/pwaUpdate";

describe("PWA update safety", () => {
  it("waits for menu or finished solo run", () => {
    expect(canApplyPwaUpdate(false, null)).toBe(true);
    expect(canApplyPwaUpdate(false, "finished")).toBe(true);
    expect(canApplyPwaUpdate(false, "answering")).toBe(false);
    expect(canApplyPwaUpdate(true, null)).toBe(false);
  });

  it("checks the registered worker immediately when the application starts", async () => {
    const update = vi.fn().mockResolvedValue(undefined);
    await checkForPwaUpdate({ update });
    expect(update).toHaveBeenCalledOnce();
  });

  it("does nothing when service workers are unavailable", async () => {
    await expect(checkForPwaUpdate(undefined)).resolves.toBeUndefined();
  });
});
