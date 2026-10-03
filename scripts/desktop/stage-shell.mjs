import { mkdir, readFile, cp, writeFile } from "node:fs/promises";
const config = JSON.parse(await readFile("desktop/config.json", "utf8"));
await readFile("desktop/bundle/release.json");
await mkdir("desktop-app", { recursive: true });
const { execFileSync } = await import("node:child_process");
execFileSync(process.execPath, ["scripts/desktop/build-helper.mjs"], {stdio:"inherit"});
await cp("desktop", "desktop-app/desktop", { recursive: true });
await writeFile(
  "desktop-app/package.json",
  JSON.stringify({
    name: "mindbattle-desktop",
    productName: "Mindbattle",
    version: config.shellVersion,
    description: "Mindbattle — интеллектуальная битва",
    author: "Mindbattle",
    main: "desktop/main.mjs",
    type: "module",
  }),
);
