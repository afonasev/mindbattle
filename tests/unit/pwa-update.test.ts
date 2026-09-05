import { describe, expect, it } from "vitest";
import { canApplyPwaUpdate } from "../../src/pwaUpdate";

describe("PWA update safety", () => {
  it("waits for menu or finished solo run", () => {
    expect(canApplyPwaUpdate(false, null)).toBe(true);
    expect(canApplyPwaUpdate(false, "finished")).toBe(true);
    expect(canApplyPwaUpdate(false, "answering")).toBe(false);
    expect(canApplyPwaUpdate(true, null)).toBe(false);
  });
});
