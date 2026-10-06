import { readFile } from "node:fs/promises";
import { checkManifest, digest } from "../../desktop/content.mjs";
import { shellManifest, fileHash } from "../../desktop/shell.mjs";
import { stat } from "node:fs/promises";
const config = JSON.parse(await readFile("desktop/config.json", "utf8"));
const kind = process.argv[2];
if (kind === "content") {
    const envelope = JSON.parse(await readFile("desktop-release/content/latest.json", "utf8"));
    const manifest = checkManifest(envelope, await readFile("desktop/content-public.pem", "utf8"), config.shellVersion);
    for (const file of manifest.files) {
        const bytes = await readFile(`desktop-release/content/objects/${file.sha256}`);
        if (bytes.length !== file.size || digest(bytes) !== file.sha256)
            throw new Error("Invalid content object");
    }
}
else if (kind === "shell") {
    for (const platform of ["darwin-universal", "win32-x64"]) {
        const env = JSON.parse(await readFile(`desktop-release/shell/${platform}/latest.json`, "utf8"));
        const m = shellManifest(env, await readFile("desktop/content-public.pem", "utf8"), platform);
        if (m.version !== config.shellVersion)
            throw Error("Shell version mismatch");
        for (const f of m.files) {
            const name = `desktop-release/shell/objects/${f.sha256}`;
            if ((await stat(name)).size !== f.size || await fileHash(name) !== f.sha256)
                throw Error("Invalid shell object");
        }
    }
}
else if (kind === "installers") {
    const catalog = JSON.parse(await readFile("desktop-release/installers/downloads.json", "utf8"));
    if (Object.keys(catalog).sort().join(",") !== "mac,windows")
        throw new Error("Both platforms required");
    for (const entry of Object.values(catalog)) {
        if (!/^https:\/\/github\.com\/afonasev\/mindbattle\/releases\/download\/v[0-9]+\.[0-9]+\.[0-9]+\/Mindbattle-[a-zA-Z0-9_.-]+$/.test(entry.url))
            throw new Error("Invalid installer path");
        const bytes = await readFile(`desktop-release/installers/installers/${entry.url.split("/").at(-1)}`);
        if (bytes.length !== entry.size || digest(bytes) !== entry.sha256)
            throw new Error("Invalid installer");
    }
}
else
    throw new Error("Expected content|shell|installers");
console.log(`Verified ${kind}`);
