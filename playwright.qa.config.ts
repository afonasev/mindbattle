import { defineConfig } from '@playwright/test';
import base from './playwright.config';
import { scopes } from './scripts/qaScope.mjs';
const scope = scopes[process.env.MINDBATTLE_QA_SCOPE ?? 'ui'];
const port = process.env.MINDBATTLE_TEST_PORT;
if (!scope || !port) throw new Error('Run through npm run qa:ui/network/input (owned host required)');
export default defineConfig({
  ...base,
  workers: 2, // Network scenarios open up to 13 contexts each; bound host contention.
  webServer: undefined, // The runner starts and verifies its own host; never reuse a foreign one.
  testMatch: scope.browser ? [...new Set(scope.browser.map(([file]) => file))] : undefined,
  grep: scope.browser ? new RegExp(scope.browser.map(([, pattern]) => `(?:${pattern})`).join('|')) : undefined,
  projects: base.projects?.filter(project => !scope.projects || scope.projects.includes(project.name!)),
  outputDir: process.env.MINDBATTLE_QA_OUTPUT,
  reporter: [['json', { outputFile: process.env.MINDBATTLE_QA_REPORT }]],
  use: { ...base.use, launchOptions: { args: ['--mute-audio'] }, baseURL: `http://127.0.0.1:${port}` }
});
