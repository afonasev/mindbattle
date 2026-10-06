import { test } from "node:test";
import assert from "node:assert/strict";
import {
  mkdtemp,
  mkdir,
  writeFile,
  readFile,
  readdir,
  rm,
  readlink,
} from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { digest } from "../../desktop/content.mjs";
test("publication preserves current on failure and retains only latest complete installer pair", async (t) => {
  const root = await mkdtemp(path.join(os.tmpdir(), "mindbattle-publish-"));
  t.after(() => rm(root, { recursive: true, force: true }));
  const code = (
    await readFile("scripts/desktop/publish-remote.py", "utf8")
  ).replace(
    "Path('/var/lib/mindbattle-desktop')",
    `Path(${JSON.stringify(root)})`,
  );
  const script = path.join(root, "publish.py");
  // Deterministic upstream fixture: exercise remote digest checking without real network.
  await writeFile(script, code.replace("kind, release = sys.argv[1:]", `import io
kind, release = sys.argv[1:]
def urlopen(request, timeout):
    platform = request.full_url.rsplit('/', 1)[1].split('.')[0].removeprefix('Mindbattle-')
    return io.BytesIO((release + '-' + platform).encode())`));
  const base = path.join(root, "installers");
  await mkdir(base);
  async function stage(id, corrupt = false) {
    const dir = path.join(base, `incoming-${id}`);
    await mkdir(dir, { recursive: true });
    const catalog = {};
    for (const p of ["mac", "windows"]) {
      const bytes = Buffer.from(`${id}-${p}`);

      catalog[p] = {
        url: `https://github.com/afonasev/mindbattle/releases/download/v1.0.4/Mindbattle-${p}.bin`,
        sha256: digest(bytes),
        size: bytes.length + (corrupt ? 1 : 0),
      };
    }
    await writeFile(path.join(dir, "downloads.json"), JSON.stringify(catalog));
    return spawnSync("python3", [script, "installers", id], {
      encoding: "utf8",
    });
  }
  const first = "20261003T010101-123456789abc",
    bad = "20261003T010102-123456789abc",
    last = "20261003T010103-123456789abc";
  assert.equal((await stage(first)).status, 0);
  assert.notEqual((await stage(bad, true)).status, 0);
  assert.equal(await readlink(path.join(base, "current")), `release-${first}`);
  // A legacy payload is removed only after the verified metadata replaces it.
  await mkdir(path.join(base, `release-${first}`, "installers"));
  assert.equal((await stage(last)).status, 0);
  assert.deepEqual(
    (await readdir(base)).filter((x) => x.startsWith("release-")),
    [`release-${last}`],
  );
});
