import { expect, test } from "@playwright/test";

test.use({ serviceWorkers: "block" });
for (const platform of ["MacIntel", "Win32"]) {
  test(`download points to the matching GitHub asset on ${platform}`, async ({ page }, info) => {
    await page.addInitScript(platform => {
      Object.defineProperty(navigator, "platform", { get: () => platform });
      HTMLMediaElement.prototype.play = async () => {};
    }, platform);
    const mac = "https://github.com/afonasev/mindbattle/releases/download/v1.0.4/Mindbattle-1.0.4-mac-universal.dmg";
    const windows = "https://github.com/afonasev/mindbattle/releases/download/v1.0.4/Mindbattle-1.0.4.exe";
    await page.route("**/desktop/downloads.json", route => route.fulfill({ json: { mac: { url: mac }, windows: { url: windows } } }));
    await page.goto("/");
    await expect(page.getByRole("link", { name: "Скачать игру" })).toHaveAttribute("href", platform === "MacIntel" ? mac : windows);
    await page.screenshot({ path: info.outputPath(`github-${platform}.png`), fullPage: true });
  });
}
test("foreign repository download links are rejected", async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(navigator, "platform", { get: () => "Win32" });
    HTMLMediaElement.prototype.play = async () => {};
  });
  await page.route("**/desktop/downloads.json", route => route.fulfill({ json: { windows: { url: "https://github.com/other/repo/releases/download/v1.0.4/Mindbattle-1.0.4.exe" } } }));
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Mindbattle", exact: true })).toBeVisible();
  await expect(page.getByRole("link", { name: "Скачать игру" })).toHaveCount(0);
});
