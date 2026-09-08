import { defineConfig, devices } from '@playwright/test';
const externalURL = process.env.OMNIMED_E2E_BASE_URL;
export default defineConfig({
  testDir: '../tests/e2e',
  timeout: 20000,
  use: { baseURL: externalURL || 'http://127.0.0.1:3000', trace: 'retain-on-failure' },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'], viewport: { width: 1366, height: 768 } } }],
  webServer: externalURL ? undefined : { command: 'npm run start', url: 'http://127.0.0.1:3000', reuseExistingServer: false, timeout: 60000 },
});
