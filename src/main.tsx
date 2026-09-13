import { StrictMode, Suspense, lazy } from "react";
import { createRoot } from "react-dom/client";
import { registerSW } from "virtual:pwa-register";
import "@fontsource-variable/onest/wght.css";
const App = lazy(() => location.pathname === "/network"
  ? import("./ui/NetworkApp").then(module => ({ default: module.NetworkApp }))
  : import("./ui/App").then(module => ({ default: module.App })));
import "./ui/theme.css";

const appIcon = document.getElementById("app-icon");
if (appIcon instanceof HTMLLinkElement) {
  appIcon.href = import.meta.env.DEV
    ? "/icons/mindbattle-dev.png"
    : "/icons/mindbattle-192.png";
}

const root = document.getElementById("root");

let applyUpdate: (() => Promise<void>) | undefined;
const updateListeners = new Set<(ready: boolean) => void>();
export const onPwaUpdate = (listener: (ready: boolean) => void) => { updateListeners.add(listener); return () => { updateListeners.delete(listener); }; };
export const applyPwaUpdate = () => applyUpdate?.() ?? Promise.resolve();
if ("serviceWorker" in navigator) {
  applyUpdate = registerSW({ onNeedRefresh: () => updateListeners.forEach((listener) => listener(true)) });
}

if (!root) {
  throw new Error("Mindbattle root element is missing");
}

createRoot(root).render(
  <StrictMode>
    <Suspense fallback={<p role="status">Загружаем Mindbattle…</p>}><App /></Suspense>
  </StrictMode>
);
