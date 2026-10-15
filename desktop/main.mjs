import { createDisplayController } from "./display.mjs";
import { ReleaseCatalog, localizedNotes } from "./releases.mjs";
import { app, BrowserWindow, ipcMain, protocol, shell, session, screen, Menu, } from "electron";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { ShellStore, acknowledgeShell } from "./shell.mjs";
import { ContentStore, atomicJson } from "./content.mjs";
import { createHandler, APP_ORIGIN } from "./protocol.mjs";
import { gameLaunchUrl, isMutedLaunch } from "./launch.mjs";
import { createUpdateCoordinator, pendingUpdateInfo } from "./updateCheck.mjs";
const here = path.dirname(fileURLToPath(import.meta.url));
const config = JSON.parse(await readFile(path.join(here, "config.json"), "utf8"));
const launchMuted = isMutedLaunch();
const launchArgs = process.argv.slice(app.isPackaged ? 1 : 2).filter(arg => !arg.startsWith("--user-data-dir="));
const gameUrl = gameLaunchUrl(APP_ORIGIN, launchMuted);
if (process.platform === "win32") app.setAppUserModelId("tech.afonasev.mindbattle");
protocol.registerSchemesAsPrivileged([
    {
        scheme: "mindbattle",
        privileges: {
            standard: true,
            secure: true,
            supportFetchAPI: true,
            corsEnabled: true,
            stream: true,
        },
    },
]);
if (!app.requestSingleInstanceLock())
    app.quit();
else {
    let window;
    let safe = false;
    let stopUpdateChecks;
    app.on("second-instance", () => {
        if (window) {
            if (window.isMinimized())
                window.restore();
            window.focus();
        }
    });
    app.on("window-all-closed", () => app.quit());
    app.on("before-quit", () => stopUpdateChecks?.());
    app
        .whenReady()
        .then(async () => {
        Menu.setApplicationMenu(null);
        const userRoot = app.getPath("userData");
        const publicKey = await readFile(path.join(here, "content-public.pem"), "utf8");
        const store = new ContentStore({
            root: path.join(userRoot, "content"),
            bundle: path.join(here, "bundle"),
            publicKey,
            shellVersion: config.shellVersion,
            origin: config.updateOrigin || config.origin,
        });
        const catalog = new ReleaseCatalog({ cache: path.join(userRoot, "github-releases.json") });
        const platform = process.platform === "darwin" ? "darwin-universal" : "win32-x64";
        const shellStore = new ShellStore({ root: path.join(userRoot, "shell"), key: publicKey, version: config.shellVersion, platform, origin: config.updateOrigin || config.origin });
        await shellStore.initialize();
        let servedDirectory = await store.initialize();
        // A prepared shell is applied before opening the first game window.
        if (app.isPackaged && shellStore.state.pending) {
          const target = process.platform === "darwin" ? path.resolve(path.dirname(process.execPath), "../..") : path.dirname(process.execPath);
          try {
            const tx = await shellStore.prepare({ target, userData: userRoot, helper: path.join(here, "helper-bin", process.platform === "win32" ? "updater.exe" : "updater"), isSafe: () => true, launchMuted, launchArgs });
            if (tx && await shellStore.start(tx, () => true)) { app.quit(); return; }
          } catch (cause) { console.warn("Prepared update retained:", cause.message); }
        }
        let display = { width: 1280, height: 720, fullscreen: false, auto: true };
        try {
            const saved = JSON.parse(await readFile(path.join(userRoot, "display.json"), "utf8"));
            if (validDisplay(saved))
                display = saved;
        }
        catch {
            /* default */
        }
        function validDisplay(d) {
            return (d &&
                Number.isInteger(d.width) &&
                Number.isInteger(d.height) &&
                d.width >= 800 &&
                d.width <= 7680 &&
                d.height >= 600 &&
                d.height <= 4320 &&
                typeof d.fullscreen === "boolean" && (d.auto === undefined || typeof d.auto === "boolean"));
        }
        const bounds = screen.getPrimaryDisplay().workAreaSize;
        if (display.auto || display.width > bounds.width || display.height > bounds.height - 40) display = { width: Math.min(1280, bounds.width), height: Math.min(720, bounds.height - 40), fullscreen: display.fullscreen, auto: true };
        const ses = session.fromPartition("persist:mindbattle");
        ses.setPermissionRequestHandler((_wc, _permission, callback) => callback(false));
        ses.setPermissionCheckHandler(() => false);
        ses.protocol.handle("mindbattle", createHandler({
            directory: () => servedDirectory,
            origin: config.origin,
            fetcher: fetch,
        }));
        window = new BrowserWindow({
            width: Math.min(display.width, bounds.width),
            height: Math.min(display.height, bounds.height - 40),
            useContentSize: true,
            minWidth: 800,
            minHeight: 600,
            fullscreenable: true,
            fullscreen: display.fullscreen,
            show: false,
            backgroundColor: "#07101f",
            icon: app.isPackaged ? path.join(process.resourcesPath, "mindbattle-icon.png") : path.join(here, "../public/icons/mindbattle-512.png"),
            webPreferences: {
                preload: path.join(here, "preload.cjs"),
                session: ses,
                contextIsolation: true,
                sandbox: true,
                nodeIntegration: false,
                webSecurity: true,
            },
        });
        window.once("ready-to-show", () => window.show());
        function external(url) {
            try {
                const u = new URL(url);
                if (u.protocol === "https:" || u.protocol === "http:")
                    void shell.openExternal(u.href);
            }
            catch { }
        }
        window.webContents.setWindowOpenHandler(({ url }) => {
            external(url);
            return { action: "deny" };
        });
        window.webContents.on("will-navigate", (event, url) => {
            if (!url.startsWith(`${APP_ORIGIN}/`)) {
                event.preventDefault();
                external(url);
            }
        });
        window.webContents.on("will-attach-webview", (event) => event.preventDefault());
        const trusted = (event) => event.sender === window.webContents &&
            event.senderFrame === window.webContents.mainFrame &&
            event.senderFrame.url.startsWith(`${APP_ORIGIN}/`);
        const handle = (name, fn) => ipcMain.handle(name, (event, ...args) => {
            if (!trusted(event))
                throw new Error("Forbidden");
            return fn(...args);
        });
        let historyAbort, historyTask;
        handle("desktop:safe", async value => { safe = value === true; if (!safe) historyAbort?.abort(); await Promise.allSettled([check.setSafe(safe), !safe ? historyTask : undefined]); });
        handle("desktop:download", () => check.download());
        handle("desktop:cancel-download", () => check.cancel());
        handle("desktop:history", async () => {
          if (!safe) throw Error("История доступна после возвращения в меню.");
          historyAbort?.abort(); historyAbort = new AbortController();
          const signal = historyAbort.signal;
          historyTask = (async () => {
            const manifest = await store.manifestAt(store.currentDirectory());
            const tag = manifest.sequence ? `content-${manifest.sequence}` : `v${config.shellVersion}`;
            return (await catalog.history(tag, manifest, signal)).map(r => ({ ...r, notes: localizedNotes(r.body, 'ru') }));
          })();
          return historyTask;
        });
        handle("desktop:status", async () => {
            const info = await pendingUpdateInfo(shellStore, store);
            return {
            ready: Boolean(shellStore.state.pending || store.state.pending),
            shellVersion: config.shellVersion,
            platform: process.platform, architecture: process.arch, channel: "stable",
            updateVersion: info?.version,
            updatePublishedAt: info?.publishedAt,
            updateStatus: check.status(),
        }; });
        handle("desktop:apply", async () => {
            if (!safe)
                return false;
            if (shellStore.state.pending) {
                if (!app.isPackaged)
                    throw new Error("Обновление оболочки доступно только в установленной игре.");
                const target = process.platform === "darwin" ? path.resolve(path.dirname(process.execPath), "../..") : path.dirname(process.execPath);
                const tx = await shellStore.prepare({ target, userData: userRoot, helper: path.join(here, "helper-bin", process.platform === "win32" ? "updater.exe" : "updater"), isSafe: () => safe, launchMuted, launchArgs });
                if (!tx || !await shellStore.start(tx, () => safe))
                    return false;
                safe = false;
                app.quit();
                return true;
            }
            if (await store.activate(() => safe)) {
                servedDirectory = store.currentDirectory();
                safe = false;
                await window.loadURL(gameUrl);
                return true;
            }
            return false;
        });
        handle("desktop:ready", async () => { await store.confirm(); await acknowledgeShell(userRoot); });
        const displayController = createDisplayController({
          initial: display,
          persist: next => atomicJson(path.join(userRoot, "display.json"), next),
          apply: async next => {
            window.setFullScreen(next.fullscreen);
            if (!next.fullscreen) {
              if (process.platform === "darwin" && window.isFullScreen()) await new Promise(resolve => window.once("leave-full-screen", resolve));
              const area = screen.getDisplayMatching(window.getBounds()).workAreaSize;
              const width = next.auto ? Math.min(1280, area.width) : next.width;
              const height = next.auto ? Math.min(720, area.height - 40) : next.height;
              window.setContentSize(Math.min(width, area.width - (window.getBounds().width - window.getContentBounds().width)), Math.min(height, area.height - (window.getBounds().height - window.getContentBounds().height)));
              window.center();
            }
          }
        });
        handle("desktop:display", () => displayController.value());
        handle("desktop:display-options", () => {
          const area = screen.getDisplayMatching(window.getBounds()).workAreaSize;
          const selected = displayController.value();
          return [...new Map([[selected.width,selected.height],[1024,768],[1280,720],[1366,768],[1600,900],[1920,1080],[2560,1440],[3840,2160]].map(([w,h]) => [`${w}x${h}`,[w,h]])).values()].filter(([w,h]) => w <= area.width && h <= area.height).map(([width,height]) => ({ width,height }));
        });
        handle("desktop:set-display", next => { if (!validDisplay(next)) throw Error("Invalid display settings"); return displayController.preview(next); });
        handle("desktop:confirm-display", () => displayController.confirm());
        handle("desktop:cancel-display", () => displayController.cancel());
        handle("desktop:quit", () => {
            app.quit();
        });
        const check = createUpdateCoordinator({ shellStore, contentStore: store, catalog, onReady: async () => {
            const info = await pendingUpdateInfo(shellStore, store);
            if (!window.isDestroyed()) window.webContents.send("desktop:update", true, info?.version, info?.publishedAt);
        }, onStatus: status => {
            if (!window.isDestroyed()) window.webContents.send("desktop:update-status", status);
        } });

        await window.loadURL(gameUrl);
        let closing = false;
        app.on('before-quit', event => {
          if (closing) return;
          event.preventDefault(); closing = true; check.stop();
          void store.prepareNextStart().catch(error => console.warn('Prepared update retained:', error.message)).finally(() => app.quit());
        });
        void check.start();
        stopUpdateChecks = () => check.stop();
    })
        .catch((error) => {
        console.error(error);
        app.quit();
    });
}
