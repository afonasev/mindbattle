import { readFile } from "node:fs/promises";
import { checkManifest, digest } from "../../desktop/content.mjs";
const config = JSON.parse(await readFile("desktop/config.json", "utf8"));
const kind = process.argv[2];
if (kind === "content") {
  const envelope = JSON.parse(
    await readFile("desktop-release/content/latest.json", "utf8"),
  );
  const manifest = checkManifest(
    envelope,
    await readFile("desktop/content-public.pem", "utf8"),
    config.shellVersion,
  );
  for (const file of manifest.files) {
    const bytes = await readFile(
      `desktop-release/content/objects/${file.sha256}`,
    );
    if (bytes.length !== file.size || digest(bytes) !== file.sha256)
      throw new Error("Invalid content object");
  }
} else if (kind === "installers") {
  const catalog = JSON.parse(
    await readFile("desktop-release/installers/downloads.json", "utf8"),
  );
  if (Object.keys(catalog).sort().join(",") !== "mac,windows")
    throw new Error("Both platforms required");
  for (const entry of Object.values(catalog)) {
    if (!/^\/desktop\/installers\/[a-zA-Z0-9_.-]+$/.test(entry.url))
      throw new Error("Invalid installer path");
    const bytes = await readFile(
      `desktop-release/installers/${entry.url.slice("/desktop/".length)}`,
    );
    if (bytes.length !== entry.size || digest(bytes) !== entry.sha256)
      throw new Error("Invalid installer");
  }
} else throw new Error("Expected content|installers");
console.log(`Verified ${kind}`);
