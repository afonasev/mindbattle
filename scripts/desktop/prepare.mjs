import { readdir, readFile, writeFile, mkdir, cp, rm } from "node:fs/promises";
import { createPrivateKey, createPublicKey, sign } from "node:crypto";
import path from "node:path";
import { digest } from "../../desktop/content.mjs";
const keyPath = process.env.MINDBATTLE_CONTENT_KEY;
if (!keyPath)
  throw new Error(
    "Set MINDBATTLE_CONTENT_KEY to the private Ed25519 signing key path (outside the repository).",
  );
const key = createPrivateKey(await readFile(keyPath));
const pinned = await readFile("desktop/content-public.pem", "utf8");
if (
  createPublicKey(key).export({ type: "spki", format: "pem" }).toString() !==
  pinned
)
  throw new Error("Private key does not match pinned desktop key");
const sequence = Number(process.env.MINDBATTLE_CONTENT_SEQUENCE || Date.now());
if (!Number.isSafeInteger(sequence) || sequence < 1)
  throw new Error("Invalid sequence");
const config = JSON.parse(await readFile("desktop/config.json", "utf8"));
const output = path.resolve("desktop-release");
await rm(output, { recursive: true, force: true });
await mkdir(path.join(output, "content", "objects"), { recursive: true });
const files = [];
async function walk(dir, relative = "") {
  for (const entry of (await readdir(dir, { withFileTypes: true })).sort(
    (a, b) => a.name.localeCompare(b.name),
  )) {
    const name = relative ? `${relative}/${entry.name}` : entry.name;
    if (entry.isDirectory()) await walk(path.join(dir, entry.name), name);
    else if (
      entry.isFile() &&
      !/^(sw\.js|workbox-.*\.js|manifest\.webmanifest)$/.test(name)
    ) {
      const bytes = await readFile(path.join(dir, entry.name));
      const sha256 = digest(bytes);
      files.push({ path: name, sha256, size: bytes.length });
      await writeFile(path.join(output, "content", "objects", sha256), bytes);
    }
  }
}
await walk("dist");
const payload = JSON.stringify({
  format: 1,
  sequence,
  bridge: 1,
  shellMajor: Number(config.shellVersion.split(".")[0]),
  files,
});
const envelope = {
  payload,
  signature: sign(null, Buffer.from(payload), key).toString("base64"),
};
await writeFile(
  path.join(output, "content", "latest.json"),
  JSON.stringify(envelope),
);
await rm("desktop/bundle", { recursive: true, force: true });
await mkdir("desktop/bundle", { recursive: true });
for (const file of files) {
  const dest = path.join("desktop/bundle", file.path);
  await mkdir(path.dirname(dest), { recursive: true });
  await cp(path.join("dist", file.path), dest);
}
await writeFile("desktop/bundle/release.json", JSON.stringify(envelope));
await rm("desktop-app", { recursive: true, force: true });
await mkdir("desktop-app", { recursive: true });
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
console.log(
  `Content ${sequence}: ${files.length} files. Prepared offline bundle; installers have not been rebuilt.`,
);
