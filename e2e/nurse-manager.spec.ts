// Nurse manager stories, NM-1 to NM-4. See docs/ux/user-stories.md.
import { test, expect, SITE, siteChecks, canonical, rows, count, categoryCounts } from './fixtures';

test.describe('NM-1 arrive from search on a category need', () => {
  test('NM-1.a-b home has a self canonical and lists Scheduling & staffing', async ({ page }) => {
    await page.goto('/');
    expect(await canonical(page)).toEqual([`${SITE}/`]);
    await expect(page.locator('meta[name=description]')).toHaveAttribute('content', /.{50,}/);
    await expect(page.locator('[data-filter-category] option', { hasText: 'Scheduling & staffing' })).toHaveCount(1);
    await siteChecks(page);
  });

  test('NM-1.c a ?q= deep link opens with the search filled in', async ({ page }) => {
    test.fail(true, 'Open: the query string is ignored. #20');
    await page.goto('/?q=scheduling');
    await page.waitForLoadState('networkidle');
    await expect(page.locator('[data-filter-query]')).toHaveValue('scheduling');
    await expect(count(page)).toHaveText(/ of /);
  });
});

test.describe('NM-2 shortlist tools for one problem', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/'); await page.waitForLoadState('networkidle'); });

  test('NM-2.a the category filter shows exactly that category', async ({ page }) => {
    const want = (await categoryCounts(page))['Scheduling & staffing'];
    await page.selectOption('[data-filter-category]', 'Scheduling & staffing');
    await expect(rows(page)).toHaveCount(want!);
    expect(await page.locator('[data-card]:visible:not([data-category="Scheduling & staffing"])').count()).toBe(0);
  });

  test('NM-2.b a two-word query matches both words in any order', async ({ page }) => {
    test.fail(true, 'Open: search is an exact-phrase match. #19');
    await page.fill('[data-filter-query]', 'nclex free');
    await expect(rows(page).first()).toBeVisible();
  });

  test('NM-2.c nonsense shows the empty state and Clear brings every row back', async ({ page }) => {
    const total = await page.locator('[data-card]').count();
    await page.fill('[data-filter-query]', 'zzqqxx');
    await expect(page.locator('[data-catalog-empty]')).toBeVisible();
    await expect(rows(page)).toHaveCount(0);
    await page.locator('[data-filter-clear]').click();
    await expect(rows(page)).toHaveCount(total);
    await expect(count(page)).toHaveText(`${total} tools`);
    await expect(page.locator('[data-filter-query]')).toHaveValue('');
  });
});

test.describe('NM-3 compare two tools', () => {
  test('NM-3.a two tool pages have the same spec rows in the same order', async ({ page }) => {
    const terms = [];
    for (const slug of ['shiftmed', 'nursegrid']) {
      await page.goto(`/tools/${slug}`);
      terms.push(await page.locator('.spec dt').allInnerTexts());
    }
    const want = ['Official site', 'EHR integrations', 'HIPAA / BAA status', 'Category', 'Vendor'];
    expect(terms[0]!.map((t) => t.trim())).toEqual(want);
    expect(terms[1]!.map((t) => t.trim())).toEqual(want);
  });
});

test.describe('NM-4 check who is behind the directory', () => {
  test('NM-4.a-b About says who, how, and what Unknown means; footer says independent', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('link', { name: 'How listings work' }).click();
    await expect(page).toHaveURL(/\/about$/);
    const main = page.locator('main');
    await expect(main).toContainText('registered nurse');
    await expect(main).toContainText('How listings work');
    await expect(main).toContainText('Unknown');
    await expect(page.locator('footer')).toContainText('Independent directory');
    await expect(page.locator('footer')).toContainText('Not medical advice');
    await siteChecks(page);
  });
});
