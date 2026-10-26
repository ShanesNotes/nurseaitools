// Site-wide checks ALL.a to ALL.f. ALL.a and ALL.b run after every test in fixtures.ts.
import { test, expect, LIVE, siteChecks } from './fixtures';

for (const path of ['/', '/students', '/about', '/submit', '/students/ngn-practice-tools']) {
  test(`ALL.c-e ${path}`, async ({ page }) => {
    await page.goto(path);
    await siteChecks(page);
  });
}

test('ALL.f the 404 page is 404, noindex, with no canonical and no current nav item', async ({ page }) => {
  const res = await page.goto('/no-such-page-e2e');
  expect(res?.status()).toBe(404);
  await expect(page.locator('link[rel=canonical]')).toHaveCount(0);
  await expect(page.locator('meta[name=robots]')).toHaveAttribute('content', /noindex/);
  await expect(page.locator('[aria-current]')).toHaveCount(0);
});

test('ALL.a the submit form is never sent on live', async ({ page, guard }) => {
  test.skip(!LIVE, 'Live only: proves the guard blocks a POST before it leaves the browser.');
  await page.goto('/submit');
  const status = await page.evaluate(() => fetch('/api/submit', { method: 'POST', body: '' }).then(() => 'sent', () => 'blocked'));
  expect(status).toBe('blocked');
  expect(guard.blocked).toEqual([expect.stringMatching(/^POST .*\/api\/submit$/)]);
  guard.blocked.length = 0; // Blocked on purpose. Anything else blocked still fails the test.
});
