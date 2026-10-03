import { _electron as electron } from "@playwright/test";
import assert from "node:assert/strict";
import { mkdir, mkdtemp, readFile, writeFile, rm, cp } from "node:fs/promises";
import { createPrivateKey, sign } from "node:crypto";
import os from "node:os";
import path from "node:path";
import { digest } from "../../desktop/content.mjs";
const evidence =
  process.env.MINDBATTLE_DESKTOP_EVIDENCE || "/tmp/mindbattle-desktop-evidence";
await mkdir(evidence, { recursive: true });
const temp = await mkdtemp(path.join(os.tmpdir(), "mindbattle-native-"));
const user = path.join(temp, "user");
await mkdir(user);
const content = path.join(temp, "content");
await cp("desktop-release/content", content, { recursive: true });
const envelope = JSON.parse(
  await readFile(path.join(content, "latest.json"), "utf8"),
);
const manifest = JSON.parse(envelope.payload);
manifest.sequence++;
const html = manifest.files.find((f) => f.path === "index.html");
const changed = Buffer.from(
  (await readFile(path.join(content, "objects", html.sha256), "utf8")).replace(
    "<html",
    '<html data-desktop-updated="yes"',
  ),
);
html.sha256 = digest(changed);
html.size = changed.length;
await writeFile(path.join(content, "objects", html.sha256), changed);
envelope.payload = JSON.stringify(manifest);
envelope.signature = sign(
  null,
  Buffer.from(envelope.payload),
  createPrivateKey(await readFile(process.env.MINDBATTLE_CONTENT_KEY)),
).toString("base64");
await writeFile(path.join(content, "latest.json"), JSON.stringify(envelope));
let app;
const launch = async () => {
  app = await electron.launch({
    args: ["tests/desktop/harness.mjs"],
    env: {
      ...process.env,
      MINDBATTLE_DESKTOP_TEST_DIR: user,
      MINDBATTLE_DESKTOP_TEST_CONTENT: content,
    },
  });
  const page = await app.firstWindow();
  await app.evaluate(({ BrowserWindow }) =>
    BrowserWindow.getAllWindows().forEach((w) =>
      w.webContents.setAudioMuted(true),
    ),
  );
  await page
    .getByRole("button", { name: "Выход из игры", exact: true })
    .waitFor();
  return page;
};
try {
  let page = await launch();
  assert.equal(await page.evaluate(() => !!window.mindbattleDesktop), true);
  await page.screenshot({ path: path.join(evidence, "desktop-menu.png") });
  await page.getByRole("button", { name: "Настройки", exact: true }).click();
  await page.getByLabel("Разрешение окна").selectOption("1600x900");
  await page.getByLabel("Режим экрана").selectOption("full");
  for (
    let i = 0;
    i < 50 &&
    !(await app.evaluate(({ BrowserWindow }) =>
      BrowserWindow.getAllWindows()[0].isFullScreen(),
    ));
    i++
  )
    await new Promise((r) => setTimeout(r, 100));
  assert.equal(
    await app.evaluate(({ BrowserWindow }) =>
      BrowserWindow.getAllWindows()[0].isFullScreen(),
    ),
    true,
  );
  await page.getByLabel("Режим экрана").selectOption("window");
  for (
    let i = 0;
    i < 50 &&
    (await app.evaluate(({ BrowserWindow }) =>
      BrowserWindow.getAllWindows()[0].isFullScreen(),
    ));
    i++
  )
    await new Promise((r) => setTimeout(r, 100));
  assert.equal(
    await app.evaluate(({ BrowserWindow }) =>
      BrowserWindow.getAllWindows()[0].isFullScreen(),
    ),
    false,
  );
  await page.screenshot({ path: path.join(evidence, "desktop-settings.png") });
  await page.evaluate(() => localStorage.setItem("desktop-smoke", "preserved"));
  await page.evaluate(
    () =>
      new Promise((resolve, reject) => {
        const req = indexedDB.open("mindbattle-results-v1", 1);
        req.onsuccess = () => {
          const tx = req.result.transaction("outbox", "readwrite");
          tx.objectStore("outbox").put({
            schemaVersion: 1,
            eventId: "offline-smoke",
            matchId: "smoke",
            mode: "solo-endless-v1",
            kind: "match",
            ordinal: 0,
            catalogRevision: "fixture",
            status: "completed",
          });
          tx.oncomplete = resolve;
          tx.onerror = reject;
        };
        req.onerror = reject;
      }),
  );
  await app.close();
  app = null;
  page = await launch();
  assert.equal(
    await page.evaluate(() => localStorage.getItem("desktop-smoke")),
    "preserved",
  );
  assert.equal(
    (await page.evaluate(() => window.mindbattleDesktop.display())).width,
    1600,
  );
  const queueCount = () =>
    page.evaluate(
      () =>
        new Promise((resolve, reject) => {
          const r = indexedDB.open("mindbattle-results-v1", 1);
          r.onsuccess = () => {
            const q = r.result
              .transaction("outbox")
              .objectStore("outbox")
              .count();
            q.onsuccess = () => resolve(q.result);
            q.onerror = reject;
          };
        }),
    );
  assert.equal(await queueCount(), 1);
  await app.evaluate(() => {
    globalThis.testNetwork.online = true;
  });
  await page.evaluate(() => window.dispatchEvent(new Event("online")));
  for (let i = 0; i < 50 && (await queueCount()); i++)
    await new Promise((r) => setTimeout(r, 100));
  assert.equal(await queueCount(), 0);
  if (process.env.MINDBATTLE_DESKTOP_TEST_API) {
    const stream = await page.evaluate(async () => {
      const r = await fetch("/api/network/create", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: "{}",
      });
      const c = await r.json();
      const abort = new AbortController();
      const response = await fetch(`/api/network/stream?code=${c.code}`, {
        headers: { authorization: `Bearer ${c.token}` },
        signal: abort.signal,
      });
      const reader = response.body.getReader();
      const first = await reader.read();
      abort.abort();
      await reader.cancel().catch(() => {});
      return new TextDecoder().decode(first.value);
    });
    assert.match(stream, /event: connected/);
  }
  assert.deepEqual(await app.evaluate(() => globalThis.testNetwork.events), [
    "offline-smoke",
  ]);
  // Restart with network enabled from harness flag so automatic startup update check runs.
  await app.close();
  app = null;
  await writeFile(path.join(user, "fixture-online"), "yes");
  page = await launch();
  await page
    .getByRole("button", {
      name: "Доступно обновление · Обновить",
      exact: true,
    })
    .waitFor({ timeout: 30000 });
  await page.screenshot({ path: path.join(evidence, "desktop-update.png") });
  await page
    .getByRole("button", {
      name: "Доступно обновление · Обновить",
      exact: true,
    })
    .click();
  await page.waitForFunction(
    () => document.documentElement.dataset.desktopUpdated === "yes",
  );
  assert.equal(
    await page.evaluate(() => localStorage.getItem("desktop-smoke")),
    "preserved",
  );
  await Promise.all([
    app.waitForEvent("close"),
    page.getByRole("button", { name: "Выход из игры", exact: true }).click(),
  ]);
  app = null;
  console.log(
    JSON.stringify({
      quitFromMenu: true,
      offlineFirstLaunch: true,
      persistentDisplay: true,
      fullScreenAndWindow: true,
      liveSse: Boolean(process.env.MINDBATTLE_DESKTOP_TEST_API),
      offlineStatisticsSurviveRestart: true,
      reconnectAck: true,
      explicitSignedContentUpdate: true,
      storagePreserved: true,
      evidence,
    }),
  );
} finally {
  if (app) await app.close();
  await rm(temp, { recursive: true, force: true });
}
