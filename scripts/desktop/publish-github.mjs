// Explicit release operation. Upload binaries before switching the VPS catalog.
import { execFileSync } from "node:child_process";
import { readFile } from "node:fs/promises";
const repo = "afonasev/mindbattle";
const config = JSON.parse(await readFile("desktop/config.json", "utf8"));
const tag = `v${config.shellVersion}`;
const gh = (...args) => execFileSync("gh", args, { encoding: "utf8" });
const catalog = JSON.parse(await readFile("desktop-release/installers/downloads.json", "utf8"));
const releases = JSON.parse(gh("api", `repos/${repo}/releases?per_page=100`));
let release = releases.find(r => r.tag_name === tag);
if (!release) {
  const commit = execFileSync("git", ["rev-parse", "HEAD"], { encoding: "utf8" }).trim();
  gh("release", "create", tag, "--repo", repo, "--target", commit, "--draft", "--title", `Mindbattle ${config.shellVersion}`, "--notes", "Windows: Program Files installation, game icon, desktop shortcut and launch options together on the finish page. macOS: universal Intel/Apple Silicon DMG. Installers are unsigned. Windows installation acceptance remains pending.");
  release = JSON.parse(gh("api", `repos/${repo}/releases?per_page=100`)).find(r => r.tag_name === tag);
}
if (!release) throw new Error(`Release ${tag} missing after creation`);
for (const item of Object.values(catalog)) {
  const name = item.url.split("/").at(-1);
  if (!release.assets.some(a => a.name === name)) {
    gh("release", "upload", tag, `desktop-release/installers/installers/${name}`, "--repo", repo);
  }
}
release = JSON.parse(gh("api", `repos/${repo}/releases?per_page=100`)).find(r => r.tag_name === tag);
for (const item of Object.values(catalog)) {
  const asset = release.assets.find(a => a.browser_download_url === item.url);
  if (!asset || asset.size !== item.size || asset.digest !== `sha256:${item.sha256}`) {
    throw new Error(`GitHub asset integrity mismatch: ${item.url}; current VPS files retained`);
  }
}
gh("release", "edit", tag, "--repo", repo, "--draft=false", "--latest");
console.log(`Verified GitHub assets: https://github.com/${repo}/releases/tag/${tag}`);
