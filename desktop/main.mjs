import { app, BrowserWindow, ipcMain, protocol, shell, session, screen, Menu, } from "electron";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { ShellStore, acknowledgeShell } from "./shell.mjs";
import { ContentStore, atomicJson } from "./content.mjs";
import { createHandler, APP_ORIGIN } from "./protocol.mjs";
import { createUpdateCheck } from "./updateCheck.mjs";
const here = path.dirname(fileURLToPath(import.meta.url));
const config = JSON.parse(await readFile(path.join(here, "config.json"), "utf8"));
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
    let checkTimer;
    app.on("second-instance", () => {
        if (window) {
            if (window.isMinimized())
                window.restore();
            window.focus();
        }
    });
    app.on("window-all-closed", () => app.quit());
    app.on("before-quit", () => clearInterval(checkTimer));
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
            origin: config.origin,
        });
        const platform = process.platform === "darwin" ? "darwin-universal" : "win32-x64";
        const shellStore = new ShellStore({ root: path.join(userRoot, "shell"), key: publicKey, version: config.shellVersion, platform, origin: config.origin });
        await shellStore.initialize();
        let servedDirectory = await store.initialize();
        let display = { width: 1280, height: 720, fullscreen: false };
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
                typeof d.fullscreen === "boolean");
        }
        const bounds = screen.getPrimaryDisplay().workAreaSize;
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
        ipcMain.on("desktop:safe", (event, value) => {
            if (trusted(event))
                safe = value === true;
        });
        handle("desktop:status", () => ({
            ready: Boolean(shellStore.state.pending || store.state.pending),
            shellVersion: config.shellVersion,
        }));
        handle("desktop:apply", async () => {
            if (!safe)
                return false;
            if (shellStore.state.pending) {
                if (!app.isPackaged)
                    throw new Error("Обновление оболочки доступно только в установленной игре.");
                const target = process.platform === "darwin" ? path.resolve(path.dirname(process.execPath), "../..") : path.dirname(process.execPath);
                const tx = await shellStore.prepare({ target, userData: userRoot, helper: path.join(here, "helper-bin", process.platform === "win32" ? "updater.exe" : "updater"), isSafe: () => safe });
                if (!tx || !await shellStore.start(tx, () => safe))
                    return false;
                safe = false;
                app.quit();
                return true;
            }
            if (await store.activate(() => safe)) {
                servedDirectory = store.currentDirectory();
                safe = false;
                await window.loadURL(`${APP_ORIGIN}/`);
                return true;
            }
            return false;
        });
        handle("desktop:ready", async () => { await store.confirm(); await acknowledgeShell(userRoot); });
        handle("desktop:display", () => display);
        let displayWriting = Promise.resolve();
        handle("desktop:set-display", (next) => {
          const update = displayWriting.then(async () => {
            if (!validDisplay(next))
                throw new Error("Invalid display settings");
            display = {
                width: next.width,
                height: next.height,
                fullscreen: next.fullscreen,
            };
            await atomicJson(path.join(userRoot, "display.json"), display);
            const area = screen.getDisplayMatching(window.getBounds()).workAreaSize;
            window.setFullScreen(display.fullscreen);
            if (!display.fullscreen) {
                const resize = () => {
                    window.setContentSize(Math.min(display.width, area.width - (window.getBounds().width - window.getContentBounds().width)), Math.min(display.height, area.height - (window.getBounds().height - window.getContentBounds().height)));
                    window.center();
                };
                if (process.platform === "darwin" && window.isFullScreen())
                    window.once("leave-full-screen", resize);
                else
                    resize();
            }
            return display;
          });
          displayWriting = update.catch(() => {});
          return update;
        });
        handle("desktop:quit", () => {
            app.quit();
        });
        const check = createUpdateCheck(shellStore, store, () => {
            if (!window.isDestroyed()) window.webContents.send("desktop:update", true);
        });
        handle("desktop:check-update", check);
        const backgroundCheck = () => void check().catch(error => console.warn("Update unavailable:", error.message));
        await window.loadURL(`${APP_ORIGIN}/`);
        backgroundCheck();
        checkTimer = setInterval(backgroundCheck, 5 * 60 * 1000);
    })
        .catch((error) => {
        console.error(error);
        app.quit();
    });
}
