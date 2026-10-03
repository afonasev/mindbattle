import { test } from "node:test";
import assert from "node:assert/strict";
import { generateKeyPairSync, sign } from "node:crypto";
import { mkdtemp, mkdir, writeFile, readFile, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import {
  ContentStore,
  checkManifest,
  digest,
  validPath,
} from "../../desktop/content.mjs";
const { privateKey, publicKey } = generateKeyPairSync("ed25519");
function release(sequence, content = "hello", extra = {}) {
  const bytes = Buffer.from(content);
  const payload = JSON.stringify({
    format: 1,
    sequence,
    bridge: 1,
    shellMajor: 1,
    files: [{ path: "index.html", sha256: digest(bytes), size: bytes.length }],
    ...extra,
  });
  return {
    envelope: {
      payload,
      signature: sign(null, Buffer.from(payload), privateKey).toString(
        "base64",
      ),
    },
    bytes,
  };
}
async function fixture(t) {
  const root = await mkdtemp(path.join(os.tmpdir(), "mindbattle-update-"));
  t.after(() => rm(root, { recursive: true, force: true }));
  const bundle = path.join(root, "bundle");
  await mkdir(bundle);
  const base = release(1);
  await writeFile(path.join(bundle, "index.html"), base.bytes);
  await writeFile(
    path.join(bundle, "release.json"),
    JSON.stringify(base.envelope),
  );
  let next = release(2, "new content");
  let broken = false;
  const options = {
    root: path.join(root, "user"),
    bundle,
    publicKey,
    shellVersion: "1.0.0",
    origin: "https://example.test",
    fetcher: async (url) =>
      new Response(
        url.endsWith("latest.json")
          ? JSON.stringify(next.envelope)
          : broken
            ? "corrupt"
            : next.bytes,
      ),
  };
  return {
    options,
    setNext: (r) => {
      next = r;
    },
    breakDownload: () => {
      broken = true;
    },
  };
}
test("rejects forged, incompatible and unsafe manifests", () => {
  const r = release(2);
  assert.equal(checkManifest(r.envelope, publicKey, "1.0.0").sequence, 2);
  assert.throws(() =>
    checkManifest(
      { ...r.envelope, payload: r.envelope.payload + " " },
      publicKey,
      "1.0.0",
    ),
  );
  assert.throws(() =>
    checkManifest(
      release(2, "x", { shellMajor: 2 }).envelope,
      publicKey,
      "1.0.0",
    ),
  );
  for (const name of [
    "../outside",
    "x/../../secret",
    "/abs",
    "C:/file",
    "x\\y",
    "a/./b",
  ])
    assert.equal(validPath(name), false);
  assert.throws(() =>
    checkManifest(
      release(2, "x", {
        files: [{ path: "../x", sha256: "0".repeat(64), size: 1 }],
      }).envelope,
      publicKey,
      "1.0.0",
    ),
  );
});
test("offline bundle, staged explicit activation, persistent confirmation and replay protection", async (t) => {
  const f = await fixture(t);
  const s = new ContentStore(f.options);
  await s.initialize();
  assert.equal(s.currentDirectory(), f.options.bundle);
  await s.check();
  assert.equal(s.currentDirectory(), f.options.bundle);
  assert.ok(s.state.pending);
  await s.activate();
  assert.equal(
    await readFile(path.join(s.currentDirectory(), "index.html"), "utf8"),
    "new content",
  );
  await s.confirm();
  const restarted = new ContentStore(f.options);
  await restarted.initialize();
  assert.equal(restarted.state.active, s.state.active);
  f.setNext(release(1));
  assert.equal(await restarted.check(), false);
  assert.equal(restarted.state.highWater, 2);
});
test("failed download preserves active bundle and high-water", async (t) => {
  const f = await fixture(t);
  const s = new ContentStore(f.options);
  await s.initialize();
  f.breakDownload();
  await assert.rejects(s.check());
  assert.equal(s.state.highWater, 1);
  assert.equal(s.state.pending, null);
  assert.equal(s.currentDirectory(), f.options.bundle);
});
test("unconfirmed activation rolls back on next start without accepting old releases", async (t) => {
  const f = await fixture(t);
  const s = new ContentStore(f.options);
  await s.initialize();
  await s.check();
  await s.activate();
  const restarted = new ContentStore(f.options);
  await restarted.initialize();
  assert.equal(restarted.currentDirectory(), f.options.bundle);
  assert.equal(restarted.state.highWater, 2);
});
test("corrupt downloaded active release falls back to known good bundle", async (t) => {
  const f = await fixture(t);
  const s = new ContentStore(f.options);
  await s.initialize();
  await s.check();
  await s.activate();
  await s.confirm();
  await writeFile(path.join(s.currentDirectory(), "index.html"), "tampered");
  const restarted = new ContentStore(f.options);
  await restarted.initialize();
  assert.equal(restarted.currentDirectory(), f.options.bundle);
});
test("serializes activation and rechecks match safety after validation", async (t) => {
  const f = await fixture(t);
  const s = new ContentStore(f.options);
  await s.initialize();
  await s.check();
  let safe = true;
  const validate = s.validRelease.bind(s);
  s.validRelease = async (id) => {
    await new Promise((r) => setTimeout(r, 5));
    safe = false;
    return validate(id);
  };
  const result = await Promise.all([
    s.activate(() => safe),
    s.activate(() => safe),
  ]);
  assert.deepEqual(result, [false, false]);
  assert.equal(s.currentDirectory(), f.options.bundle);
  assert.ok(s.state.pending);
  s.validRelease = validate;
  safe = true;
  assert.equal(await s.activate(() => safe), true);
});
test("cancels activation if a match starts during atomic state save", async (t) => {
  const f = await fixture(t);
  const s = new ContentStore(f.options);
  await s.initialize();
  await s.check();
  const save = s.save.bind(s);
  let safe = true;
  s.save = async () => {
    await save();
    safe = false;
  };
  assert.equal(await s.activate(() => safe), false);
  assert.equal(s.currentDirectory(), f.options.bundle);
  assert.ok(s.state.pending);
});
test("failed state commit retains the serving release and pending candidate", async (t) => {
  const f = await fixture(t);
  const s = new ContentStore(f.options);
  await s.initialize();
  await s.check();
  s.save = async () => {
    throw Error("disk full");
  };
  await assert.rejects(s.activate());
  assert.equal(s.currentDirectory(), f.options.bundle);
  assert.ok(s.state.pending);
  assert.equal(s.busy, false);
});
