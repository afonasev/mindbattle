import { defineConfig, devices } from "@playwright/test";

const testPort = Number(process.env.MINDBATTLE_TEST_PORT ?? 4187);

export default defineConfig({
  testDir: "./tests/browser",
  fullyParallel: false,
  retries: 0,
  reporter: "list",
  use: {
    baseURL: `http://127.0.0.1:${testPort}`,
    trace: "retain-on-failure"
  },
  projects: [
    {
      name: "chromium-1280",
      use: { ...devices["Desktop Chrome"], viewport: { width: 1280, height: 720 } }
    },
    {
      name: "chromium-1920",
      use: { ...devices["Desktop Chrome"], viewport: { width: 1920, height: 1080 } }
    }
  ],
  webServer: {
    command: `MINDBATTLE_PORT=${testPort} npm run preview`,
    url: `http://127.0.0.1:${testPort}`,
    reuseExistingServer: true,
    timeout: 120000
  }
});
