import { browserFeedback } from './feedback/outbox';
import { desktop } from "./desktop";
import { browserResults } from './statistics/outbox';
import { StrictMode, Suspense, lazy, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { registerSW } from "virtual:pwa-register";
import { checkForPwaUpdate, findPwaUpdate, waitingUpdateVersion } from "./pwaUpdate";
import { runManualUpdate, withUpdateTimeout } from "./gameUpdate";
import "@fontsource-variable/onest/wght.css";
const App = lazy(() => import("./ui/App").then(module => ({ default: module.App })));
const NetworkApp = lazy(() => import("./ui/NetworkApp").then(module => ({ default: module.NetworkApp })));
import "./ui/theme.css";
import { AppFooter } from "./ui/AppFooter";

const appIcon = document.getElementById("app-icon");
if (appIcon instanceof HTMLLinkElement) {
  appIcon.href = import.meta.env.DEV
    ? "/icons/mindbattle-dev.png"
    : "/icons/mindbattle-192.png";
}

browserResults();
browserFeedback();

const root = document.getElementById("root");

let applyUpdate: (() => Promise<void>) | undefined;
let updateReady = false;
let updateVersion: string | undefined;
const updateListeners = new Set<(ready: boolean, version?: string) => void>();
export const onPwaUpdate = (listener: (ready: boolean, version?: string) => void) => { updateListeners.add(listener); listener(updateReady, updateVersion); return () => { updateListeners.delete(listener); }; };
export const applyPwaUpdate = () => applyUpdate?.() ?? Promise.reject(new Error("Обновление пока недоступно. Попробуйте ещё раз."));
let registrationError: unknown;
let registered: (registration: ServiceWorkerRegistration | undefined) => void;
const registrationReady = new Promise<ServiceWorkerRegistration | undefined>(resolve => { registered = resolve; });
export function updateGame(isSafe: () => boolean, onApplying: () => void) {
  return runManualUpdate({ isSafe, onApplying, apply: applyPwaUpdate, check: async () => {
    if (updateReady) return true;
    if (desktop) {
      if (desktop.checkUpdate) return (await desktop.checkUpdate()).ready;
      if ((await desktop.status()).ready) return true;
      throw new Error("В этой версии приложения обновления проверяются автоматически. Попробуйте ещё раз чуть позже.");
    }
    if (!("serviceWorker" in navigator)) throw new Error("Обновление недоступно в этом браузере.");
    const registration = await withUpdateTimeout(registrationReady, 15_000);
    if (!registration) throw new Error("Не удалось подготовить обновление. Попробуйте перезапустить игру.", { cause: registrationError });
    if (!navigator.onLine && !registration.waiting) throw new Error("Не удалось обновить игру. Проверьте подключение и попробуйте ещё раз.");
    if (!await findPwaUpdate(registration)) return false;
    // Workbox installs its reload listener when it emits onNeedRefresh.
    await new Promise<void>((resolve, reject) => {
      const timer = setTimeout(() => { unsubscribe(); reject(new Error("Обновление загружено. Нажмите «Обновить» ещё раз.")); }, 5_000);
      let unsubscribe = () => {};
      const listener = (ready: boolean) => { if (ready) { clearTimeout(timer); unsubscribe(); resolve(); } };
      unsubscribe = onPwaUpdate(listener);
      if (updateReady) unsubscribe();
    });
    return true;
  } });
}
export function navigate(path: string) {
  if (location.pathname === path) return;
  history.pushState(null, "", path);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

function RoutedApp() {
  useEffect(() => { void desktop?.ready(); }, []);
  const [path, setPath] = useState(location.pathname);
  useEffect(() => {
    const syncPath = () => setPath(location.pathname);
    window.addEventListener("popstate", syncPath);
    return () => window.removeEventListener("popstate", syncPath);
  }, []);
  return <>{path === "/network" ? <NetworkApp /> : <App />}<AppFooter /></>;
}
function updateAvailable(ready: boolean, version?: string) { updateReady = ready; updateVersion = ready ? version : undefined; updateListeners.forEach(listener => listener(ready, updateVersion)); }
if (desktop) {
  applyUpdate = async () => { if (!await desktop!.applyUpdate()) throw new Error("Update not applied"); };
  desktop.onUpdate(updateAvailable);
  void desktop.status().then(state => updateAvailable(state.ready, state.updateVersion));
} else if ("serviceWorker" in navigator) {
  applyUpdate = registerSW({
    immediate: true,
    onNeedRefresh: () => {
      updateAvailable(true);
      void registrationReady.then(async registration => {
        const worker = registration?.waiting;
        if (!worker) return;
        const version = await waitingUpdateVersion(worker);
        if (registration.waiting === worker && updateReady) updateAvailable(true, version);
      });
    },
    onRegisteredSW: (_swScriptUrl, registration) => {
      registered(registration);
      void checkForPwaUpdate(registration).catch(() => undefined);
    },
    onRegisterError: (error) => { registrationError = error; registered(undefined); }
  });
}

if (!root) {
  throw new Error("Mindbattle root element is missing");
}

createRoot(root).render(
  <StrictMode>
    <Suspense fallback={<p role="status">Загружаем Mindbattle…</p>}><RoutedApp /></Suspense>
  </StrictMode>
);
