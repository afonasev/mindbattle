import { createHash, verify } from "node:crypto";
import {
  readFile,
  writeFile,
  mkdir,
  rename,
  rm,
  access,
} from "node:fs/promises";
import path from "node:path";

export const digest = (bytes) =>
  createHash("sha256").update(bytes).digest("hex");
export const validPath = (value) =>
  typeof value === "string" &&
  /^(?:[a-zA-Z0-9_-]+\/)*[a-zA-Z0-9_.-]+$/.test(value) &&
  !value.split("/").some((x) => x === "." || x === "..") &&
  !value.includes("\\");
export async function atomicJson(file, data) {
  await mkdir(path.dirname(file), { recursive: true });
  await writeFile(`${file}.tmp`, JSON.stringify(data));
  await rename(`${file}.tmp`, file);
}
export function checkManifest(envelope, publicKey, shellVersion) {
  if (
    typeof envelope?.payload !== "string" ||
    envelope.payload.length > 4_000_000 ||
    typeof envelope.signature !== "string" ||
    !verify(
      null,
      Buffer.from(envelope.payload),
      publicKey,
      Buffer.from(envelope.signature, "base64"),
    )
  )
    throw new Error("Invalid content signature");
  const m = JSON.parse(envelope.payload);
  if (
    m.format !== 1 ||
    !Number.isSafeInteger(m.sequence) ||
    m.sequence < 1 ||
    m.bridge !== 1 ||
    !Number.isInteger(m.shellMajor) ||
    m.shellMajor !== Number(shellVersion.split(".")[0])
  )
    throw new Error("Incompatible content");
  if (!Array.isArray(m.files) || !m.files.length || m.files.length > 20000)
    throw new Error("Invalid files");
  const names = new Set();
  let total = 0;
  for (const file of m.files) {
    if (
      !validPath(file.path) ||
      names.has(file.path) ||
      !/^[a-f0-9]{64}$/.test(file.sha256) ||
      !Number.isSafeInteger(file.size) ||
      file.size < 0 ||
      file.size > 64 * 1024 ** 2
    )
      throw new Error("Invalid content file");
    names.add(file.path);
    total += file.size;
  }
  if (!names.has("index.html") || total > 512 * 1024 ** 2)
    throw new Error("Invalid content size");
  return m;
}
export async function boundedBytes(response, max) {
  if (!response.ok) throw new Error(`Download failed: ${response.status}`);
  const reader = response.body.getReader();
  const chunks = [];
  let size = 0;
  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      size += value.length;
      if (size > max) throw new Error("Download too large");
      chunks.push(value);
    }
  } finally {
    await reader.cancel().catch(() => {});
  }
  return Buffer.concat(chunks);
}
export class ContentStore {
  constructor({
    root,
    bundle,
    publicKey,
    shellVersion,
    origin,
    fetcher = fetch,
  }) {
    Object.assign(this, {
      root,
      bundle,
      publicKey,
      shellVersion,
      origin,
      fetcher,
    });
    this.state = {
      active: null,
      previous: null,
      pending: null,
      highWater: 0,
      trial: false,
    };
    this.busy = false;
    this.writing = Promise.resolve();
  }
  directory(id) {
    if (!/^[a-f0-9]{64}$/.test(id)) throw new Error("Invalid release");
    return path.join(this.root, "releases", id);
  }
  async save() {
    const snapshot = structuredClone(this.state);
    this.writing = this.writing
      .catch(() => {})
      .then(() => atomicJson(path.join(this.root, "state.json"), snapshot));
    await this.writing;
  }
  async manifestAt(dir) {
    const envelope = JSON.parse(
      await readFile(path.join(dir, "release.json"), "utf8"),
    );
    return checkManifest(envelope, this.publicKey, this.shellVersion);
  }
  async validRelease(id) {
    if (!id) return false;
    try {
      const dir = this.directory(id);
      const m = await this.manifestAt(dir);
      for (const file of m.files) {
        const bytes = await readFile(path.join(dir, file.path));
        if (bytes.length !== file.size || digest(bytes) !== file.sha256)
          return false;
      }
      return true;
    } catch {
      return false;
    }
  }
  async initialize() {
    const base = await this.manifestAt(this.bundle);
    try {
      this.state = {
        ...this.state,
        ...JSON.parse(
          await readFile(path.join(this.root, "state.json"), "utf8"),
        ),
      };
    } catch {
      /* first launch */
    }
    this.state.highWater = Math.max(
      Number.isSafeInteger(this.state.highWater) ? this.state.highWater : 0,
      base.sequence,
    );
    if (this.state.trial || !(await this.validRelease(this.state.active))) {
      this.state.active = (await this.validRelease(this.state.previous))
        ? this.state.previous
        : null;
      this.state.trial = false;
    }
    if (
      this.state.active &&
      (await this.manifestAt(this.directory(this.state.active))).sequence <
        base.sequence
    )
      this.state.active = null;
    if (!(await this.validRelease(this.state.pending)))
      this.state.pending = null;
    if (
      this.state.pending &&
      (await this.manifestAt(this.directory(this.state.pending))).sequence <=
        base.sequence
    )
      this.state.pending = null;
    await this.save();
    return this.currentDirectory();
  }
  currentDirectory() {
    return this.state.active ? this.directory(this.state.active) : this.bundle;
  }
  async check() {
    if (this.busy) return Boolean(this.state.pending);
    this.busy = true;
    let staging;
    try {
      const response = await this.fetcher(
        `${this.origin}/desktop/content/latest.json`,
        {
          redirect: "error",
          signal: AbortSignal.timeout(30000),
          cache: "no-store",
        },
      );
      const raw = await boundedBytes(response, 4_100_000);
      const envelope = JSON.parse(raw.toString());
      const manifest = checkManifest(
        envelope,
        this.publicKey,
        this.shellVersion,
      );
      if (manifest.sequence <= this.state.highWater)
        return Boolean(this.state.pending);
      const id = digest(Buffer.from(envelope.payload));
      staging = path.join(this.root, "staging");
      await rm(staging, { recursive: true, force: true });
      await mkdir(staging, { recursive: true });
      for (const file of manifest.files) {
        let bytes;
        try {
          const old = await readFile(
            path.join(this.currentDirectory(), file.path),
          );
          if (old.length === file.size && digest(old) === file.sha256)
            bytes = old;
        } catch {
          /* changed */
        }
        if (!bytes)
          bytes = await boundedBytes(
            await this.fetcher(
              `${this.origin}/desktop/content/objects/${file.sha256}`,
              { redirect: "error", signal: AbortSignal.timeout(60000) },
            ),
            file.size,
          );
        if (bytes.length !== file.size || digest(bytes) !== file.sha256)
          throw new Error("Content hash mismatch");
        const target = path.join(staging, file.path);
        await mkdir(path.dirname(target), { recursive: true });
        await writeFile(target, bytes);
      }
      await writeFile(path.join(staging, "release.json"), raw);
      const destination = this.directory(id);
      await mkdir(path.dirname(destination), { recursive: true });
      try {
        await access(destination);
        await rm(destination, { recursive: true });
      } catch {
        /* new release */
      }
      await rename(staging, destination);
      staging = null;
      this.state.pending = id;
      this.state.highWater = manifest.sequence;
      await this.save();
      return true;
    } finally {
      if (staging) await rm(staging, { recursive: true, force: true });
      this.busy = false;
    }
  }
  async activate(isSafe = () => true) {
    if (this.busy || !this.state.pending) return false;
    this.busy = true;
    const before = structuredClone(this.state);
    try {
      if (!(await this.validRelease(before.pending)) || !isSafe()) return false;
      this.state.previous = before.active;
      this.state.active = before.pending;
      this.state.pending = null;
      this.state.trial = true;
      await this.save();
      if (!isSafe()) {
        this.state = before;
        await this.save();
        return false;
      }
      return true;
    } catch (error) {
      this.state = before;
      throw error;
    } finally {
      this.busy = false;
    }
  }
  async confirm() {
    if (this.state.trial) {
      this.state.trial = false;
      await this.save();
    }
  }
}
