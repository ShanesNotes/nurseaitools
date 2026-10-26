import { test as base, expect, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';

export const LIVE = process.env.E2E_LIVE === '1';
export const SITE = 'https://nurseaitools.com';

export type Tool = { slug: string; name: string; vendor: string; url: string; category: string; built: string; hstat: string; fit: string; hipaa: string; ehr: string };
/** tools.json is the local build's data. Live is an older deploy, so live checks read counts from the page instead. */
export const TOOLS: Tool[] = JSON.parse(readFileSync(new URL('../tools.json', import.meta.url), 'utf8'));

type Guard = { blocked: string[]; beacons: string[]; errors: string[] };
// Live has Cloudflare Web Analytics injected by the zone. It is still blocked, so the suite sends no analytics, but it is expected.
const BEACON = /^https:\/\/static\.cloudflareinsights\.com\//;

export const test = base.extend<{ guard: Guard }>({
  guard: [async ({ page, baseURL }, use) => {
    const guard: Guard = { blocked: [], beacons: [], errors: [] };
    const origin = new URL(baseURL!).origin;
    await page.route('**/*', (route) => {
      const req = route.request();
      const sameOrigin = req.url().startsWith(origin + '/') || req.url() === origin;
      // Local: only the local worker. Live: only GETs to the site itself, so no form can ever be submitted.
      if (!sameOrigin || (LIVE && req.method() !== 'GET')) {
        (LIVE && BEACON.test(req.url()) ? guard.beacons : guard.blocked).push(`${req.method()} ${req.url()}`);
        return route.abort('blockedbyclient');
      }
      return route.continue();
    });
    page.on('pageerror', (err) => guard.errors.push(err.message));
    await use(guard);
    // ALL.a and ALL.b, after every test.
    expect(guard.blocked, 'ALL.a no request leaves the server under test').toEqual([]);
    expect(guard.errors, 'ALL.b no script errors').toEqual([]);
  }, { auto: true }],
});
export { expect };

export const isPhone = (name: string) => name.startsWith('phone');

/** ALL.c, ALL.d, ALL.e on the page as it stands. */
export async function siteChecks(page: Page) {
  const r = await page.evaluate(() => {
    const visible = (el: Element) => { const b = el.getBoundingClientRect(); return b.width > 0 && b.height > 0 && getComputedStyle(el).visibility !== 'hidden'; };
    const h1 = [...document.querySelectorAll('h1')].filter(visible).length;
    const sideways = document.documentElement.scrollWidth - document.documentElement.clientWidth;
    const small = [...document.querySelectorAll('button, input:not([type=checkbox]):not(.hp), select, textarea, label.toggle')]
      .filter(visible).map((el) => [el.outerHTML.slice(0, 60), Math.round(el.getBoundingClientRect().height)] as const).filter(([, h]) => h < 44);
    return { h1, sideways, small };
  });
  expect(r.h1, 'ALL.c exactly one visible h1').toBe(1);
  expect(r.sideways, 'ALL.d no sideways scroll').toBeLessThanOrEqual(0);
  expect(r.small, 'ALL.e controls are at least 44px tall').toEqual([]);
}

export async function canonical(page: Page) {
  return page.locator('link[rel=canonical]').evaluateAll((ls) => ls.map((l) => l.getAttribute('href')));
}

export const rows = (page: Page) => page.locator('[data-card]:visible');
export const count = (page: Page) => page.locator('[data-catalog-count]');

/** Category counts from the rows on the page, so the same check works on live's older data. */
export async function categoryCounts(page: Page) {
  const cats = await page.locator('[data-card]').evaluateAll((els) => els.map((el) => (el as HTMLElement).dataset.category ?? ''));
  return cats.reduce<Record<string, number>>((m, c) => ({ ...m, [c]: (m[c] ?? 0) + 1 }), {});
}

/** Relative luminance contrast between an element's text and the first opaque background up its tree. */
export async function contrastOf(page: Page, selector: string) {
  return page.locator(selector).first().evaluate((el) => {
    const parse = (c: string) => (c.match(/[\d.]+/g) ?? []).map(Number);
    const lum = ([r, g, b]: number[]) => {
      const f = (v: number) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
      return 0.2126 * f(r!) + 0.7152 * f(g!) + 0.0722 * f(b!);
    };
    let bgEl: Element | null = el, bg = [255, 255, 255];
    while (bgEl) { const c = parse(getComputedStyle(bgEl).backgroundColor); if (c.length >= 3 && (c[3] ?? 1) === 1) { bg = c; break; } bgEl = bgEl.parentElement; }
    const fg = parse(getComputedStyle(el).color);
    const [a, b] = [lum(fg), lum(bg)].sort((x, y) => y - x);
    return (a! + 0.05) / (b! + 0.05);
  });
}

export function uniqueEmail(project: string) {
  return `e2e+${project}-${Date.now()}@example.invalid`;
}
