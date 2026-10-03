import { generateKeyPairSync } from "node:crypto";
import { writeFile, mkdir, access } from "node:fs/promises";
import path from "node:path";
const target = process.env.MINDBATTLE_CONTENT_KEY;
if (!target || !path.isAbsolute(target))
  throw new Error(
    "Set MINDBATTLE_CONTENT_KEY to an absolute private key path outside the repository",
  );
if (path.resolve(target).startsWith(`${process.cwd()}${path.sep}`))
  throw new Error("Private key must live outside the repository");
try {
  await access("desktop/content-public.pem");
  throw new Error(
    "Pinned public key exists. Do not rotate it: existing installations depend on it.",
  );
} catch (e) {
  if (e.code !== "ENOENT") throw e;
}
const { privateKey, publicKey } = generateKeyPairSync("ed25519");
await mkdir(path.dirname(target), { recursive: true, mode: 0o700 });
await writeFile(target, privateKey.export({ type: "pkcs8", format: "pem" }), {
  mode: 0o600,
  flag: "wx",
});
await writeFile(
  "desktop/content-public.pem",
  publicKey.export({ type: "spki", format: "pem" }),
  { flag: "wx" },
);
console.log(
  "Release signing key created outside repository; pinned public key saved. Back up the private key securely.",
);
