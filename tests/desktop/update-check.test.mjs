import { test } from "node:test";
import assert from "node:assert/strict";
import { createUpdateCheck, pendingUpdateVersion } from "../../desktop/updateCheck.mjs";
const store = (check) => ({ state: { pending: null }, check });
test("background and manual callers await one download", async () => {
  let release;
  let calls = 0;
  const shell = store(() => { calls++; return new Promise(resolve => { release = resolve; }); });
  let notified = 0;
  const check = createUpdateCheck(shell, store(async () => false), () => notified++);
  const first = check(), second = check();
  assert.equal(first, second);
  assert.equal(calls, 1);
  release(true);
  assert.deepEqual(await second, { ready: true });
  assert.equal(notified, 1);
  const next = check();
  assert.equal(calls, 2);
  release(false);
  await next;
});
test("shell failure still allows ready content, but not a false current result", async () => {
  const shell = store(async () => { throw Error("shell offline"); });
  assert.deepEqual(await createUpdateCheck(shell, store(async () => true), () => {})(), { ready: true });
  await assert.rejects(createUpdateCheck(shell, store(async () => false), () => {})(), /Не удалось проверить/);
  await assert.rejects(createUpdateCheck(shell, store(async () => { throw Error("content offline"); }), () => {})(), /Не удалось проверить/);
});
test("a ready cached update is available offline and shell keeps priority", async () => {
  let contentChecked = false;
  const shell = store(async () => { throw Error("offline"); });
  shell.state.pending = "ready";
  assert.deepEqual(await createUpdateCheck(shell, store(async () => { contentChecked = true; return false; }), () => {})(), { ready: true });
  assert.equal(contentChecked, false);
});
test("current requires both channels to succeed", async () => {
  assert.deepEqual(await createUpdateCheck(store(async () => false), store(async () => false), () => {})(), { ready: false });
});

test("pending version follows apply priority and never uses current shell version", async () => {
  const shell = { state: { pending: "shell" }, pendingManifest: async () => ({ version: "1.2.0" }) };
  const content = { state: { pending: "content" }, directory: id => id, manifestAt: async () => ({ version: "0.1.0+abcd1234" }) };
  assert.equal(await pendingUpdateVersion(shell, content), "1.2.0");
  shell.state.pending = null;
  assert.equal(await pendingUpdateVersion(shell, content), "0.1.0+abcd1234");
  content.manifestAt = async () => ({ sequence: 3 }); // older signed content
  assert.equal(await pendingUpdateVersion(shell, content), undefined);
  content.state.pending = null;
  assert.equal(await pendingUpdateVersion(shell, content), undefined);
});
