import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
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

if (!root) {
  throw new Error("Mindbattle root element is missing");
}

createRoot(root).render(
  <StrictMode>
    <App />
  </StrictMode>
);
