import { defineConfig } from "vite";
export default defineConfig({
  build: {
    ssr: "server/network.ts",
    outDir: "server-dist",
    emptyOutDir: true,
    copyPublicDir: false,
  },
});
