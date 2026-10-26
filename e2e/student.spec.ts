// Nursing student stories, ST-1 to ST-4. See docs/ux/user-stories.md.
import { test, expect, LIVE, SITE, siteChecks, canonical, rows, categoryCounts, contrastOf, uniqueEmail } from './fixtures';

const GUIDE = '/students/best-ai-nclex-prep';

test.describe('ST-1 arrive on an NCLEX guide from search', () => {
  test('ST-1.a-c the guide has a self canonical, live tool links, and links onward', async ({ page, request }) => {
    await page.goto(GUIDE);
    expect(await canonical(page)).toEqual([`${SITE}${GUIDE}`]);
    const hrefs = [...new Set(await page.locator('main a[href^="/tools/"]').evaluateAll((as) => as.map((a) => a.getAttribute('href')!)))];
    expect(hrefs.length).toBeGreaterThan(0);
    for (const h of hrefs) expect((await request.get(h)).status(), `ST-1.b ${h}`).toBe(200);
    await expect(page.locator('main a[href="/students/free-nclex-prep"]').first()).toBeVisible();
    await expect(page.getByRole('link', { name: 'Back to the students hub' })).toBeVisible();
    await siteChecks(page);
  });

  test('ST-1.d lede and body text meet 4.5:1', async ({ page }) => {
    await page.goto(GUIDE);
    for (const sel of ['.deck .lede', '.deck .sub', '.prose p']) expect(await contrastOf(page, sel), sel).toBeGreaterThanOrEqual(4.5);
  });
});

test.describe('ST-2 find a free NCLEX tool', () => {
  test('ST-2.a-b the hub links all seven guides and the free guide lists a free plan', async ({ page }) => {
    await page.goto('/students');
    await expect(page.locator('.guides a')).toHaveCount(7);
    await page.getByRole('link', { name: 'Free NCLEX prep tools' }).click();
    await expect(page).toHaveURL(/\/students\/free-nclex-prep$/);
    await expect(page.locator('main')).toContainText(/free plan|Free tier|Free daily plan/i);
    await siteChecks(page);
  });

  test('ST-2.c the Education / NCLEX filter matches the data', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const want = (await categoryCounts(page))['Education / NCLEX'];
    await page.selectOption('[data-filter-category]', 'Education / NCLEX');
    await expect(rows(page)).toHaveCount(want!);
  });
});

test.describe('ST-3 read the safe-use rule', () => {
  test('ST-3.a-b a study tool says never enter real patient information', async ({ page }) => {
    await page.goto('/tools/goodnurse');
    await expect(page.locator('.check dd').nth(1)).toHaveText('Not for patient info');
    await expect(page.locator('.spec')).toContainText('never enter real patient information');
  });
});

test.describe('ST-4 sign up from a guide', () => {
  test('ST-4.a-b the form controls are 44px and a local signup works', async ({ page }, info) => {
    await page.goto('/students/free-nclex-prep');
    const form = page.locator('form[action="/api/subscribe"]');
    for (const el of [form.locator('input[type=email]'), form.locator('button')]) {
      expect((await el.boundingBox())!.height).toBeGreaterThanOrEqual(44);
    }
    if (LIVE) return; // Never submit on live.
    await form.locator('input[type=email]').fill(uniqueEmail(info.project.name + '-guide'));
    await form.locator('button').click();
    await expect(form.locator('[data-form-message]')).toHaveText("You're subscribed. Thanks!");
  });
});
