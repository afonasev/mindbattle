import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { registerSW } from "virtual:pwa-register";
import "@fontsource-variable/onest/wght.css";
import { App } from "./ui/App";
import "./ui/theme.css";

const appIcon = document.getElementById("app-icon");
if (appIcon instanceof HTMLLinkElement) {
  appIcon.href = import.meta.env.DEV
    ? "/icons/mindbattle-dev.png"
    : "/icons/mindbattle.png";
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
    <App />
  </StrictMode>
);
