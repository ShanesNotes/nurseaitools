// Runs in the page. Measures rendered text size, control height, text contrast, and sideways scroll.
// Reads computed styles only, so it holds for any design the build ships.
({ minFont, minControl, minLink, minContrast }) => {
  const parse = (c) => {
    const m = c.match(/rgba?\(([^)]+)\)/);
    if (!m) return [0, 0, 0, 0];
    const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number);
    return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1];
  };
  const over = (top, under) => {
    const a = top[3];
    return [0, 1, 2].map((i) => top[i] * a + under[i] * (1 - a)).concat(1);
  };
  const lum = ([r, g, b]) => {
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
  const hidden = (el) => {
    const r = el.getBoundingClientRect();
    if (r.width <= 1 || r.height <= 1) return true;
    for (let n = el; n && n !== document.documentElement; n = n.parentElement) {
      const s = getComputedStyle(n);
      if (s.display === 'none' || s.visibility === 'hidden' || Number(s.opacity) === 0) return true;
      if (/inset\(50%\)/.test(s.clipPath) || s.clip === 'rect(0px, 0px, 0px, 0px)') return true;
    }
    return false;
  };
  const ground = (el) => {
    const layers = [];
    for (let n = el; n; n = n.parentElement) {
      const bg = parse(getComputedStyle(n).backgroundColor);
      if (bg[3] > 0) { layers.push(bg); if (bg[3] >= 1) break; }
    }
    let c = [255, 255, 255, 1];
    for (const l of layers.reverse()) c = over(l, c);
    return c;
  };
  const label = (el) => {
    const t = (el.innerText || el.value || el.getAttribute('aria-label') || el.placeholder || '').trim().replace(/\s+/g, ' ').slice(0, 40);
    return `${el.tagName.toLowerCase()}${el.className ? '.' + String(el.className).split(' ')[0] : ''} "${t}"`;
  };

  const small = [], short = [], low = [];
  let texts = 0;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  for (let t = walker.nextNode(); t; t = walker.nextNode()) {
    const el = t.parentElement;
    if (!t.textContent.trim() || !el || seen.has(el) || /^(SCRIPT|STYLE|NOSCRIPT|OPTION)$/.test(el.tagName) || hidden(el)) continue;
    seen.add(el);
    texts++;
    const s = getComputedStyle(el);
    const size = parseFloat(s.fontSize);
    if (size < minFont) small.push(`${label(el)} ${size}px`);
    const fg = over(parse(s.color), ground(el));
    const large = size >= 24 || (size >= 18.66 && Number(s.fontWeight) >= 700);
    const need = large ? Math.min(3, minContrast) : minContrast;
    const r = ratio(fg, ground(el));
    if (r + 1e-6 < need) low.push(`${label(el)} ${r.toFixed(2)}:1 (${s.color} on rgb(${ground(el).slice(0, 3).map(Math.round)}))`);
  }

  for (const el of document.querySelectorAll('button, select, textarea, input:not([type=checkbox]):not([type=radio]):not([type=hidden]), label:has(> input[type=checkbox])')) {
    if (hidden(el) || el.tabIndex < 0) continue;
    const h = el.getBoundingClientRect().height;
    if (h + 0.5 < minControl) short.push(`${label(el)} ${h.toFixed(1)}px tall`);
  }
  // WCAG 2.5.8: a link set inside a sentence is exempt. A link that stands alone is a target. An undersized
  // target still passes when a minLink-wide circle on its center touches no other target and no other such circle.
  const targets = [...document.querySelectorAll('a[href], button, select, textarea, input:not([type=hidden])')]
    .filter((el) => !hidden(el) && el.tabIndex >= 0)
    .map((el) => ({ el, r: el.getBoundingClientRect() }));
  const centre = ({ r }) => [r.left + r.width / 2, r.top + r.height / 2];
  const under = (t) => t.r.width + 0.5 < minLink || t.r.height + 0.5 < minLink;
  const dist = ([x, y], r) => Math.hypot(Math.max(r.left - x, 0, x - r.right), Math.max(r.top - y, 0, y - r.bottom));
  for (const t of targets) {
    if (t.el.tagName !== 'A' || !under(t)) continue;
    const parent = t.el.parentElement;
    const alone = getComputedStyle(t.el).display !== 'inline' || (parent && parent.innerText.trim() === t.el.innerText.trim());
    if (!alone) continue;
    const c = centre(t);
    const near = targets.find((o) => o !== t && !t.el.contains(o.el) && !o.el.contains(t.el) &&
      (dist(c, o.r) < minLink / 2 || (under(o) && Math.hypot(c[0] - centre(o)[0], c[1] - centre(o)[1]) < minLink)));
    if (near) short.push(`${label(t.el)} ${t.r.height.toFixed(1)}px tall, crowds ${label(near.el)}`);
  }

  return { scrollWidth: document.documentElement.scrollWidth, texts, small, short, low };
}
