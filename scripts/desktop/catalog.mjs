import { cp, mkdir, readFile, readdir, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { digest } from "../../desktop/content.mjs";
const config = JSON.parse(await readFile("desktop/config.json", "utf8"));
const files = await readdir("desktop-installers");
const choices = {
  mac: `Mindbattle-${config.shellVersion}-mac-universal.dmg`,
  windows: `Mindbattle-${config.shellVersion}.exe`,
};
const root = "desktop-release/installers";
await rm(root, { recursive: true, force: true });
await mkdir(path.join(root, "installers"), { recursive: true });
const catalog = {};
for (const [platform, name] of Object.entries(choices)) {
  if (!files.includes(name)) throw new Error(`Missing installer: ${name}`);
  const source = path.join("desktop-installers", name);
  const bytes = await readFile(source);
  await cp(source, path.join(root, "installers", name));
  catalog[platform] = {
    version: config.shellVersion,
    url: `https://github.com/afonasev/mindbattle/releases/download/v${config.shellVersion}/${name}`,
    size: bytes.length,
    sha256: digest(bytes),
  };
}
await writeFile(
  path.join(root, "downloads.json"),
  JSON.stringify(catalog, null, 2),
);
console.log(
  "Latest-only installer catalog ready; neither upload nor deployment performed.",
);
