import { test, expect } from '../../frontend/tests/browser-fixture';

test('role preview changes worklists, never enables clinical write actions', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'ทะเบียนผู้ป่วย', exact: true })).toBeVisible();
  await expect(page.getByRole('button', { name: 'ลงทะเบียนผู้ป่วย', exact: true })).toBeDisabled();
  await page.getByLabel('สำรวจหน้าจอตามบทบาท').selectOption('R-FIN');
  await expect(page.getByRole('heading', { name: 'รายการค่าใช้จ่าย', exact: true })).toBeVisible();
  await expect(page.getByRole('columnheader', { name: 'ยอดเงิน (บาท)' })).toBeVisible();
  await expect(page.getByLabel('ยังไม่ได้เลือกผู้ป่วย', { exact: true })).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'ดูค่าใช้จ่าย', exact: true })).toBeDisabled();
  await page.getByLabel('สำรวจหน้าจอตามบทบาท').selectOption('R-DOC');
  await expect(page.getByLabel('ยังไม่ได้เลือกผู้ป่วย', { exact: true })).toBeVisible();
});

test('keyboard, language and desktop layout remain usable', async ({ page }) => {
  await page.goto('/');
  await page.keyboard.press('Tab');
  await expect(page.getByRole('link', { name: 'ข้ามไปเนื้อหาหลัก' })).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.locator('#main')).toBeFocused();
  await page.getByRole('button', { name: 'Switch to English' }).click();
  await expect(page.locator('html')).toHaveAttribute('lang', 'en');
  await expect(page.getByRole('heading', { name: 'Patient registry', exact: true })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBeTruthy();
  await page.setViewportSize({ width: 390, height: 844 });
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBeTruthy();
});

test('connection failure is shown honestly', async ({ page }) => {
  await page.route('**/api/status', route => route.fulfill({ status: 503, contentType: 'application/json', body: '{"status":"unavailable"}' }));
  await page.goto('/');
  await page.getByRole('button', { name: 'สถานะโครงระบบ' }).click();
  await page.getByRole('button', { name: 'ตรวจอีกครั้ง' }).click();
  await expect(page.getByRole('status')).toHaveText('ยังไม่พร้อม');
});
