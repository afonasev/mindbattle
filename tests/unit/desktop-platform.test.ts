import { describe, expect, it } from "vitest";
import { downloadPlatform } from "../../src/desktop";
describe("desktop download routing", () => {
  it("uses OS not window size and excludes iPad pretending to be Mac", () => {
    expect(downloadPlatform("Macintosh", "MacIntel", 0)).toBe("mac");
    expect(downloadPlatform("Windows NT 10.0", "Win32", 0)).toBe("windows");
    expect(downloadPlatform("Macintosh", "MacIntel", 5)).toBe(null);
    expect(downloadPlatform("Android", "Linux", 5)).toBe(null);
    expect(downloadPlatform("Linux", "Linux x86_64", 0)).toBe(null);
  });
});
