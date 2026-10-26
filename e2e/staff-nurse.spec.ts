// Staff nurse stories, SN-1 to SN-5. See docs/ux/user-stories.md.
import { test, expect, LIVE, SITE, TOOLS, siteChecks, canonical, rows, count, uniqueEmail } from './fixtures';

const SLUG = 'abridge-for-nurses';
const tool = TOOLS.find((t) => t.slug === SLUG)!;

test.describe('SN-1 arrive on a tool page from a reply on X', () => {
  test('SN-1.a-d the utm link opens the tool with a clean canonical and the reality check', async ({ page }) => {
    const res = await page.goto(`/tools/${SLUG}?utm_source=x&utm_medium=social`);
    expect(res?.status(), 'SN-1.a 200').toBe(200);
    expect(await canonical(page), 'SN-1.a clean canonical').toEqual([`${SITE}/tools/${SLUG}`]);
    await expect(page.locator('h1'), 'SN-1.b h1 is the tool name').toHaveText(tool.name);
    const check = page.locator('.check');
    for (const label of ['Built for', 'HIPAA status', 'Bedside fit']) await expect(check.getByText(label, { exact: true })).toBeVisible();
    await expect(check.locator('dd'), 'SN-1.c three reality-check values').toHaveCount(3);
    await siteChecks(page); // SN-1.d
  });

  test('SN-1.e a trailing-slash copy redirects to the clean URL', async ({ request }) => {
    test.fail(true, 'Open: /tools/<slug>/ is a 200 copy, not a 301. Trailing-slash 301 PR. #26');
    const res = await request.get(`/tools/${SLUG}/`, { maxRedirects: 0 });
    expect(res.status()).toBe(301);
    expect(new URL(res.headers()['location']!, SITE).pathname).toBe(`/tools/${SLUG}`);
  });
});

test.describe('SN-2 find nurse-built tools for charting', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/'); await page.waitForLoadState('networkidle'); });

  test('SN-2.a "Browse tools" takes the nurse to the directory', async ({ page }) => {
    await page.getByRole('link', { name: /^Browse \d+ tools$/ }).click();
    await expect(page).toHaveURL(/#directory$/);
    await expect(page.locator('#dir-h')).toBeInViewport();
  });

  test('SN-2.b category plus "Built for nurses" narrows the rows and the count says so', async ({ page }) => {
    const total = await page.locator('[data-card]').count();
    await page.selectOption('[data-filter-category]', 'Ambient documentation');
    await page.locator('[data-filter-trait=nurses]').check();
    const shown = await rows(page).count();
    const expected = await page.locator('[data-card][data-category="Ambient documentation"][data-traits~=nurses]').count();
    expect(shown).toBe(expected);
    expect(shown).toBeGreaterThan(0);
    await expect(count(page)).toHaveText(`${shown} of ${total} tools`);
  });

  test('SN-2.c after Back, the rows match the filters shown in the controls', async ({ page }) => {
    test.fail(true, 'Open: the browser restores the controls on Back but the list shows every row. #13');
    await page.selectOption('[data-filter-category]', 'Ambient documentation');
    await page.locator('[data-filter-trait=nurses]').check();
    const shown = await rows(page).count();
    await rows(page).first().locator('h2 a').click();
    await page.waitForURL(/\/tools\//);
    await page.goBack();
    await page.waitForLoadState('networkidle');
    await expect(page.locator('[data-filter-category]')).toHaveValue('Ambient documentation');
    await expect(page.locator('[data-filter-trait=nurses]')).toBeChecked();
    await expect(rows(page)).toHaveCount(shown);
  });

  test('SN-2.d searching "charting" finds an ambient documentation tool', async ({ page }) => {
    test.fail(true, 'Open: search reads only name, vendor and description, so "charting" finds 0. #18');
    await page.fill('[data-filter-query]', 'charting');
    await expect(rows(page).first()).toBeVisible();
    expect(await page.locator('[data-card]:visible[data-category="Ambient documentation"]').count()).toBeGreaterThan(0);
  });
});

test.describe('SN-3 read a tool page', () => {
  test.beforeEach(async ({ page }) => { await page.goto(`/tools/${SLUG}`); });

  test('SN-3.a-b official site, EHR and HIPAA rows', async ({ page }) => {
    const site = page.locator('.spec a[target=_blank]');
    if (!LIVE) await expect(site).toHaveAttribute('href', tool.url);
    await expect(site).toHaveAttribute('rel', /noopener/);
    for (const term of ['Official site', 'EHR integrations', 'HIPAA / BAA status']) await expect(page.locator('.spec dt', { hasText: term })).toBeVisible();
    await siteChecks(page);
  });

  test('SN-3.c "Back to the directory" lands on the directory, not the top of the hero', async ({ page }) => {
    test.fail(true, 'Open: the link goes to "/", so the nurse scrolls past the hero again. #21');
    await page.getByRole('link', { name: 'Back to the directory' }).click();
    await page.waitForLoadState('networkidle');
    await expect(page.locator('#dir-h')).toBeInViewport();
  });

  test('SN-3.d the page links another tool in the same category', async ({ page }) => {
    test.fail(true, 'Open: a tool page links no other tool. #22');
    const others = page.locator(`main a[href^="/tools/"]:not([href="/tools/${SLUG}"])`);
    expect(await others.count()).toBeGreaterThan(0);
  });
});

test.describe('SN-4 decide whether to trust the HIPAA line', () => {
  test('SN-4.a the HIPAA row says the BAA is not confirmed', async ({ page }) => {
    await page.goto(`/tools/${SLUG}`);
    await expect(page.locator('.check dd').nth(1)).toHaveText('Mentions HIPAA');
    await expect(page.locator('.spec dd', { hasText: 'HIPAA' })).toContainText('BAA availability not confirmed');
  });

  test('SN-4.b the HIPAA filter does not promise more than the data', async ({ page }) => {
    test.fail(true, 'Open: the filter is labeled "HIPAA-ready"; the data only says the vendor website mentions HIPAA. #14');
    await page.goto('/');
    await expect(page.locator('label.toggle', { has: page.locator('[data-filter-trait=hipaa]') })).not.toContainText('HIPAA-ready');
  });

  test('SN-4.c a tool page with an Unknown HIPAA status still shows when it was checked', async ({ page }) => {
    test.fail(true, 'Open: only "Mentions HIPAA" rows carry a date. Unknown and study-tool pages show none. #15');
    await page.goto('/tools/abridge');
    await expect(page.locator('main')).toContainText(/checked \w+ \d{4}/i);
  });

  test('SN-4.d the tool page links to how listings work', async ({ page }) => {
    test.fail(true, 'Open: the tool page does not link /about. #16');
    await page.goto(`/tools/${SLUG}`);
    expect(await page.locator('main a[href="/about"]').count()).toBeGreaterThan(0);
  });
});

test.describe('SN-5 sign up for the weekly note from a tool page', () => {
  test('SN-5.a a bad address is refused and nothing is posted', async ({ page }) => {
    await page.goto(`/tools/${SLUG}`);
    const form = page.locator('form[action="/api/subscribe"]');
    const posts: string[] = [];
    page.on('request', (r) => { if (r.method() === 'POST') posts.push(r.url()); });
    await form.locator('input[type=email]').fill('not-an-email');
    if (LIVE) return; // Live: stop before any click on Subscribe.
    await form.locator('button').click();
    await expect(form.locator('[data-form-message]')).toHaveText('Please enter a valid email.');
    expect(posts).toEqual([]);
  });

  test('SN-5.b local: a good address makes one POST and says subscribed', async ({ page }, info) => {
    test.skip(LIVE, 'Never submit on live.');
    await page.goto(`/tools/${SLUG}`);
    const form = page.locator('form[action="/api/subscribe"]');
    const posts: string[] = [];
    page.on('request', (r) => { if (r.method() === 'POST') posts.push(new URL(r.url()).pathname); });
    await form.locator('input[type=email]').fill(uniqueEmail(info.project.name));
    await form.locator('button').click();
    await expect(form.locator('[data-form-message]')).toHaveText("You're subscribed. Thanks!");
    expect(posts).toEqual(['/api/subscribe']);
  });

  test('SN-5.c live: the form is ready and the suite stops before submit', async ({ page }) => {
    test.skip(!LIVE, 'Live only.');
    await page.goto(`/tools/${SLUG}`);
    const form = page.locator('form[action="/api/subscribe"]');
    await form.locator('input[type=email]').fill('read-only-check@example.invalid');
    await expect(form.locator('button')).toBeEnabled();
    // Stop here. The guard would also abort any POST.
  });
});
