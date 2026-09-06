import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

const appIcons = [
  { src: "/icons/mindbattle-192.png", sizes: "192x192", type: "image/png", purpose: "any" },
  { src: "/icons/mindbattle-512.png", sizes: "512x512", type: "image/png", purpose: "any maskable" }
];

export default defineConfig({
  plugins: [react(), VitePWA({ registerType: "prompt", injectRegister: false, manifest: { name: "Mindbattle — интеллектуальная битва", short_name: "Mindbattle", lang: "ru", theme_color: "#07101f", background_color: "#07101f", display: "standalone", icons: appIcons }, workbox: { navigateFallback: "/index.html", globPatterns: ["**/*.{js,css,html,ico,png,svg,json,wav,woff2}"], maximumFileSizeToCacheInBytes: 20 * 1024 * 1024 } })],
  server: {
    host: "127.0.0.1",
    port: 4173,
    strictPort: true
  },
  preview: {
    host: "127.0.0.1",
    port: 4173,
    strictPort: true
  }
});
