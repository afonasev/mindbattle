import { desktop } from "./desktop";
import { browserResults } from './statistics/outbox';
import { StrictMode, Suspense, lazy, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { registerSW } from "virtual:pwa-register";
import { checkForPwaUpdate } from "./pwaUpdate";
import "@fontsource-variable/onest/wght.css";
const App = lazy(() => import("./ui/App").then(module => ({ default: module.App })));
const NetworkApp = lazy(() => import("./ui/NetworkApp").then(module => ({ default: module.NetworkApp })));
import "./ui/theme.css";

const appIcon = document.getElementById("app-icon");
if (appIcon instanceof HTMLLinkElement) {
  appIcon.href = import.meta.env.DEV
    ? "/icons/mindbattle-dev.png"
    : "/icons/mindbattle-192.png";
}

browserResults();

const root = document.getElementById("root");

let applyUpdate: (() => Promise<void>) | undefined;
let updateReady = false;
const updateListeners = new Set<(ready: boolean) => void>();
export const onPwaUpdate = (listener: (ready: boolean) => void) => { updateListeners.add(listener); listener(updateReady); return () => { updateListeners.delete(listener); }; };
export const applyPwaUpdate = () => applyUpdate?.() ?? Promise.resolve();
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
  return path === "/network" ? <NetworkApp /> : <App />;
}
function updateAvailable(ready: boolean) { updateReady = ready; updateListeners.forEach(listener => listener(ready)); }
if (desktop) {
  applyUpdate = async () => { if (!await desktop!.applyUpdate()) throw new Error("Update not applied"); };
  desktop.onUpdate(updateAvailable);
  void desktop.status().then(state => updateAvailable(state.ready));
} else if ("serviceWorker" in navigator) {
  applyUpdate = registerSW({
    immediate: true,
    onNeedRefresh: () => updateAvailable(true),
    onRegisteredSW: (_swScriptUrl, registration) => {
      void checkForPwaUpdate(registration).catch(() => undefined);
    }
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
