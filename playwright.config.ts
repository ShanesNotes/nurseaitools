import { defineConfig } from '@playwright/test';
import { existsSync } from 'node:fs';

// Local by default: build, then serve dist/worker.js with wrangler dev --local and a fresh local D1 (e2e/serve.mjs).
// E2E_LIVE=1 points the suite at https://nurseaitools.com in read-only mode: GET and navigation only, no form is submitted.
const live = process.env.E2E_LIVE === '1';
const port = process.env.E2E_PORT || '8812';
const baseURL = live ? 'https://nurseaitools.com' : process.env.E2E_BASE_URL || `http://127.0.0.1:${port}`;
const chrome = process.env.CHROME || (existsSync('/usr/bin/google-chrome') ? '/usr/bin/google-chrome' : undefined);

const phone = { width: 390, height: 844 };
const desktop = { width: 1280, height: 800 };

export default defineConfig({
  testDir: 'e2e',
  outputDir: 'e2e-results',
  workers: Number(process.env.E2E_WORKERS || 2),
  retries: 0,
  timeout: 30_000,
  reporter: [['list'], ['json', { outputFile: 'e2e-results/report.json' }]],
  use: {
    baseURL,
    launchOptions: chrome ? { executablePath: chrome } : {},
    screenshot: 'only-on-failure',
    trace: 'off',
  },
  projects: [
    { name: 'phone-light', use: { viewport: phone, colorScheme: 'light', isMobile: false, hasTouch: true } },
    { name: 'phone-dark', use: { viewport: phone, colorScheme: 'dark', isMobile: false, hasTouch: true } },
    { name: 'desktop-light', use: { viewport: desktop, colorScheme: 'light' } },
    { name: 'desktop-dark', use: { viewport: desktop, colorScheme: 'dark' } },
  ],
  webServer: live || process.env.E2E_BASE_URL ? undefined : {
    command: 'python3 build.py && node e2e/serve.mjs',
    url: `${baseURL}/robots.txt`,
    env: { E2E_PORT: port },
    reuseExistingServer: false,
    timeout: 120_000,
    stdout: 'ignore',
    stderr: 'pipe',
  },
});
