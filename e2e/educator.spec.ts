// Nurse educator stories, ED-1 to ED-3. See docs/ux/user-stories.md.
import { test, expect, SITE, siteChecks, canonical } from './fixtures';

test.describe('ED-1 arrive on the students hub from X', () => {
  test('ED-1.a-c clean canonical, the PHI rule, and the no-ratings line', async ({ page }) => {
    const res = await page.goto('/students?utm_source=x');
    expect(res?.status()).toBe(200);
    expect(await canonical(page)).toEqual([`${SITE}/students`]);
    await expect(page.getByRole('heading', { name: 'One rule before any of these' })).toBeVisible();
    await expect(page.locator('main')).toContainText('No star ratings here');
    await expect(page.locator('main')).toContainText('from vendor sites');
    await siteChecks(page);
  });
});

test.describe('ED-2 arrive on the care plan guide from search', () => {
  test('ED-2.a it cites the review and says to ask the instructor', async ({ page }) => {
    await page.goto('/students/ai-care-plan-tools');
    await expect(page.locator('main')).toContainText('scoping review');
    await expect(page.locator('main')).toContainText('Ask your instructor');
    await siteChecks(page);
  });
});

test.describe('ED-3 find a page for educators', () => {
  test('ED-3.a the nav has an entry for educators or leaders', async ({ page }) => {
    test.fail(true, 'Open: only Students has an entry point. See the persona entry points epic. #11');
    await page.goto('/');
    await expect(page.locator('.mast nav')).toContainText(/educator|leader|manager/i);
  });
});
