import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

// NSIS on macOS needs an available UTF-8 locale to expand Russian page text.
// Linux's C.UTF-8 locale is not available on macOS.
const env = process.platform === "darwin"
  ? { ...process.env, LC_ALL: "en_US.UTF-8", LANG: "en_US.UTF-8" }
  : process.env;
execFileSync(process.execPath, [
  fileURLToPath(new URL("../../node_modules/electron-builder/cli.js", import.meta.url)),
  "--win", "--publish", "never",
], { stdio: "inherit", env });
