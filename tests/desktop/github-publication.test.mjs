import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, mkdir, writeFile, readFile, rm } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import path from "node:path";
import os from "node:os";

for (const corrupt of [false, true]) {
  test(`draft GitHub assets: ${corrupt ? "bad digest blocks publication" : "temporary URLs do not block verified publication"}`, async t => {
    const root = await mkdtemp(path.join(os.tmpdir(), "mindbattle-github-test-"));
    t.after(() => rm(root, { recursive: true, force: true }));
    await mkdir(path.join(root, "desktop"));
    await mkdir(path.join(root, "desktop-release/installers"), { recursive: true });
    await writeFile(path.join(root, "desktop/config.json"), JSON.stringify({ shellVersion: "1.0.4" }));
    const catalog = Object.fromEntries(["mac", "windows"].map(p => [p, { url: `https://github.com/afonasev/mindbattle/releases/download/v1.0.4/Mindbattle-${p}.bin`, size: 123, sha256: "a".repeat(64) }]));
    await writeFile(path.join(root, "desktop-release/installers/downloads.json"), JSON.stringify(catalog));
    const release = { tag_name: "v1.0.4", draft: true, assets: Object.values(catalog).map((item, i) => ({ name: item.url.split("/").at(-1), browser_download_url: item.url.replace("v1.0.4", "untagged-draft"), size: item.size, digest: `sha256:${corrupt && i === 1 ? "b".repeat(64) : item.sha256}` })) };
    await writeFile(path.join(root, "gh"), `#!/usr/bin/env node
import { writeFileSync } from 'node:fs';
if (process.argv[2] === 'api') console.log(${JSON.stringify(JSON.stringify([release]))});
else if (process.argv[2] === 'release' && process.argv[3] === 'edit') writeFileSync('published', 'yes');
else process.exit(2);
`, { mode: 0o755 });
    await writeFile(path.join(root, "git"), "#!/bin/sh\necho f2fbb85a88d39d5d2d5e47ccab7c872006079253\n", { mode: 0o755 });
    const result = spawnSync(process.execPath, [path.resolve("scripts/desktop/publish-github.mjs")], { cwd: root, env: { ...process.env, PATH: `${root}:${process.env.PATH}` }, encoding: "utf8" });
    if (corrupt) {
      assert.notEqual(result.status, 0);
      await assert.rejects(readFile(path.join(root, "published")), { code: "ENOENT" });
    } else {
      assert.equal(result.status, 0, result.stderr);
      assert.equal(await readFile(path.join(root, "published"), "utf8"), "yes");
    }
  });
}
