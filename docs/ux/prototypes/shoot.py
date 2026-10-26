"""Shoots the UX pass evidence: finding screenshots, epic prototypes, and the gallery.

Usage: python docs/ux/prototypes/shoot.py http://127.0.0.1:<port>
Serve the local build first (node e2e/serve.mjs). Prototypes are the real pages with markup injected
in the browser, so they use the shipped CSS and tokens. Nothing here changes the site.
"""
import json, os, sys
from playwright.sync_api import sync_playwright

B = sys.argv[1].rstrip("/")
TOOLS = {t["slug"]: t for t in json.load(open(os.path.join(os.path.dirname(__file__), "..", "..", "..", "tools.json")))}
ROOT = os.path.join(os.path.dirname(__file__), "..", "screenshots")
for d in ("findings", "prototypes", "gallery"):
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)
NOTE = """(t)=>{const n=document.createElementNS('http://www.w3.org/1999/xhtml','div');n.textContent=t;n.style.cssText='position:fixed;right:16px;bottom:16px;z-index:9;max-width:420px;padding:12px 16px;background:#fff;color:#000;border:3px solid #c2185b;font:15px/1.4 sans-serif';(document.body||document.documentElement).append(n)}"""

def shot(pg, name, full=False, clip=None):
    pg.screenshot(path=os.path.join(ROOT, name), full_page=full, clip=clip)

def ctx(br, w=1280, h=800, scheme="light"):
    return br.new_context(viewport={"width": w, "height": h}, color_scheme=scheme).new_page()

with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=os.environ.get("CHROME", "/usr/bin/google-chrome"))

    # ---- Findings ----
    pg = ctx(br)
    pg.goto(B + "/"); pg.wait_for_load_state("networkidle")
    pg.select_option("[data-filter-category]", "Ambient documentation"); pg.check("[data-filter-trait=nurses]")
    pg.locator("[data-card]:visible a").first.click(); pg.wait_for_url("**/tools/**")
    pg.go_back(); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(300)
    pg.locator(".find").scroll_into_view_if_needed(); pg.evaluate("scrollBy(0,-40)")
    pg.evaluate(NOTE, "After Back: the controls say Ambient documentation + Built for nurses, but the count says 79 tools and every category shows.")
    shot(pg, "findings/back-filters-mismatch.png")

    pg.goto(B + "/"); pg.wait_for_load_state("networkidle"); pg.check("[data-filter-trait=hipaa]")
    pg.locator(".find").scroll_into_view_if_needed(); pg.evaluate("scrollBy(0,-40)")
    pg.evaluate(NOTE, 'The filter says "HIPAA-ready". The rows it selects only say the vendor website mentions HIPAA; the tool page adds "BAA availability not confirmed".')
    shot(pg, "findings/hipaa-ready-label.png")

    pg.goto(B + "/"); pg.wait_for_load_state("networkidle")
    for term, name, msg in (("charting", "search-charting-zero.png", '"charting" finds 0 of 79. Fifteen ambient documentation tools draft notes, but search reads only name, vendor and description.'),
                            ("nclex free", "search-phrase-only.png", '"nclex free" finds 0. Several NCLEX tools say "free" in their entry; search matches the exact phrase only.')):
        pg.fill("[data-filter-query]", term); pg.wait_for_timeout(200)
        pg.locator(".find").scroll_into_view_if_needed(); pg.evaluate("scrollBy(0,-40)")
        pg.evaluate("document.querySelectorAll('body>div[style*=c2185b]').forEach(n=>n.remove())")
        pg.evaluate(NOTE, msg); shot(pg, "findings/" + name)

    pg.goto(B + "/?q=scheduling"); pg.wait_for_load_state("networkidle")
    pg.locator(".find").scroll_into_view_if_needed(); pg.evaluate("scrollBy(0,-40)")
    pg.evaluate(NOTE, "Opened /?q=scheduling. The search box is empty and all 79 tools show. A shared or bookmarked search link does nothing.")
    shot(pg, "findings/q-param-ignored.png")

    pg.goto(B + "/tools/goodnurse"); pg.click("text=Back to the directory"); pg.wait_for_load_state("networkidle")
    pg.evaluate(NOTE, '"Back to the directory" from a tool page lands here, at the top of the hero. The first row is 1,275px down at 1280x800.')
    shot(pg, "findings/back-link-lands-on-hero.png")

    pg.goto(B + "/tools/abridge")
    pg.evaluate(NOTE, "No date anywhere on this page, no author, no link to how listings work. Only \"Mentions HIPAA\" tools carry \"(checked Oct 2026)\" in one row.")
    shot(pg, "findings/tool-page-no-date.png", full=True)
    pg.evaluate("document.querySelectorAll('body>div[style*=c2185b]').forEach(n=>n.remove())")
    pg.evaluate(NOTE, 'The lede names "Abridge for Nurses", which is in the directory, but does not link it.')
    shot(pg, "findings/abridge-cross-ref-unlinked.png")

    pg.goto(B + "/tools/shiftmed"); pg.evaluate("scrollTo(0, document.querySelector('.fine').getBoundingClientRect().top+scrollY-300)")
    pg.evaluate(NOTE, "End of a tool page: the only links on are Back and submit corrections. No other scheduling tools, no next step.")
    shot(pg, "findings/tool-page-dead-end.png")

    pg.goto(B + "/no-such-page")
    pg.evaluate(NOTE, '404 page: "Directory" is marked current, the head has rel=canonical "https://nurseaitools.com/" and no noindex, and there is no search or next step.')
    shot(pg, "findings/404-page.png")

    pg.goto(B + "/"); pg.wait_for_load_state("networkidle"); pg.fill("[data-filter-query]", "zzzz"); pg.wait_for_timeout(200)
    pg.locator(".find").scroll_into_view_if_needed(); pg.evaluate("scrollBy(0,-40)")
    pg.evaluate(NOTE, 'Empty state says "this filter" after a search, offers no suggestion or submit link. The search clear x is Chrome default blue, off the one-accent palette.')
    shot(pg, "findings/empty-state-and-blue-x.png")

    pg.goto(B + "/sitemap.xml")
    pg.evaluate(NOTE, "Every URL says lastmod 2026-10-17, including tool pages changed on Oct 25 (Healthleap added, Andor Health updated).")
    shot(pg, "findings/sitemap-lastmod.png")

    pg.goto(B + "/students/")
    pg.evaluate(NOTE, "/students/ (trailing slash) answers 200 with canonical /students. Google lists it as 'Alternate page with proper canonical'. A 301 to /students removes the copy.")
    shot(pg, "findings/trailing-slash-copy.png")

    pg.goto(B + "/")
    pg.evaluate(NOTE, 'The h1 says "reviewed by a nurse". Tool pages say "From vendor or public info only" and /students says "No star ratings... we only rate tools we have used". A reader cannot tell what the review was.')
    shot(pg, "findings/hero-reviewed-claim.png")
    pg.context.close()

    pg = ctx(br, 390, 844)
    pg.goto(B + "/"); pg.wait_for_load_state("networkidle")
    y = pg.evaluate("document.querySelector('.news').getBoundingClientRect().top+scrollY")
    pg.evaluate(f"scrollTo(0,{y}-300)")
    pg.evaluate(NOTE, f"Phone, home: the newsletter starts {int(y):,}px down, after all 79 rows. Page height {pg.evaluate('document.documentElement.scrollHeight'):,}px.")
    shot(pg, "findings/newsletter-buried-phone.png")
    pg.evaluate("scrollTo(0, document.querySelectorAll('[data-card]')[30].getBoundingClientRect().top+scrollY)")
    pg.evaluate("document.querySelectorAll('body>div[style*=c2185b]').forEach(n=>n.remove())")
    pg.evaluate(NOTE, "Phone, row 31 of 79: the search and filters are 3,000px back up. No sticky filter bar, no back-to-top, no count on screen.")
    shot(pg, "findings/phone-filters-scrolled-away.png")
    pg.goto(B + "/tools/abridge-for-nurses"); pg.evaluate("scrollTo(0, document.querySelector('.spec').getBoundingClientRect().top+scrollY-80)")
    pg.evaluate(NOTE, "Official site opens a new tab with no visible or spoken warning.")
    shot(pg, "findings/external-link-new-tab.png")
    pg.context.close()

    # ---- Prototypes (epics) ----
    def tool_page(w=1280, scheme="light"):
        p = ctx(br, w, 900 if w > 400 else 844, scheme); p.goto(B + "/tools/abridge-for-nurses"); return p

    # Trust A: a checked ledger under the reality check.
    for w in (1280, 390):
        p = tool_page(w)
        p.evaluate("""()=>{const n=document.querySelector('.check .note');n.innerHTML='<b>Checked Oct 25, 2026</b> by the editor, a critical care RN, from the vendor homepage and product page. <a href="/about">How listings work</a>. <a href="/submit">Report a change</a>.'}""")
        p.evaluate("scrollTo(0, document.querySelector('.check').getBoundingClientRect().top+scrollY-24)")
        shot(p, f"prototypes/trust-a-checked-line-{w}.png"); p.context.close()
    # Trust B: a source ledger table, one row per claim with its source and date.
    p = tool_page()
    p.evaluate("""()=>{const s=document.createElement('section');s.className='prose';s.innerHTML='<h2>Where each fact comes from</h2><dl class=spec style="margin-top:0"><dt>Built for: Nurses</dt><dd>Vendor product page names nurses as the user. <a href="https://www.abridge.com/platform/nursing">abridge.com/platform/nursing</a>, checked Oct 25, 2026</dd><dt>HIPAA: Mentions HIPAA</dt><dd>Vendor site mentions HIPAA. No BAA published. Checked Oct 15, 2026</dd><dt>Bedside fit</dt><dd>Mobile capture during care is described on the product page. Checked Oct 25, 2026</dd><dt>Not checked</dt><dd>Hands-on use, pricing, outcomes. We say so instead of guessing.</dd></dl>';document.querySelector('.spec').after(s)}""")
    p.evaluate("scrollTo(0, document.querySelector('.prose h2').getBoundingClientRect().top+scrollY-24)")
    shot(p, "prototypes/trust-b-source-ledger-1280.png"); p.context.close()
    # Trust C: a "how this was vetted" stamp at the top, beside the h1.
    p = tool_page()
    p.evaluate("""()=>{const b=document.querySelector('.by');b.innerHTML='by Abridge <span aria-hidden=true>·</span> listing checked Oct 25, 2026 <span aria-hidden=true>·</span> 3 of 3 reality-check facts sourced <span aria-hidden=true>·</span> <a href="/about">how we vet</a>'}""")
    shot(p, "prototypes/trust-c-stamp-1280.png"); p.context.close()

    # Discovery A: task-first chips over the search.
    def home_dir(w=1280):
        p = ctx(br, w, 900 if w > 400 else 844); p.goto(B + "/"); p.wait_for_load_state("networkidle"); return p
    TASKS = ["Chart less", "Hand off a shift", "Catch deterioration", "Staff and schedule", "Talk with patients", "Study for NCLEX", "Write a care plan"]
    for w in (1280, 390):
        p = home_dir(w)
        p.evaluate("""(ts)=>{const d=document.createElement('div');d.className='filters';d.style.marginTop='0';d.innerHTML='<p class=kicker style="flex-basis:100%">What do you need help with?</p>'+ts.map((t,i)=>`<label class=toggle${i==0?' style="border-color:var(--accent);background:var(--bar)"':''}>${t}</label>`).join('');document.querySelector('.find').before(d)}""", TASKS)
        p.fill("[data-filter-query]", ""); p.select_option("[data-filter-category]", "Ambient documentation")
        p.evaluate("scrollTo(0, document.querySelector('#dir-h').getBoundingClientRect().top+scrollY-24)")
        shot(p, f"prototypes/discovery-a-task-chips-{w}.png"); p.context.close()
    # Discovery B: role tabs.
    p = home_dir()
    p.evaluate("""()=>{const d=document.createElement('nav');d.setAttribute('aria-label','Who is this for');d.style.cssText='display:flex;gap:0;border-bottom:1px solid var(--text);margin-bottom:24px';d.innerHTML=['At the bedside','Leading a unit','In school','Teaching'].map((t,i)=>`<a href="#" style="display:inline-flex;align-items:center;min-height:44px;padding:0 24px;color:var(--text);text-decoration:none;${i==0?'border-bottom:2px solid var(--accent);font-weight:500':''}">${t}</a>`).join('');document.querySelector('.find').before(d)}""")
    p.check("[data-filter-trait=nurses]")
    p.evaluate("scrollTo(0, document.querySelector('#dir-h').getBoundingClientRect().top+scrollY-24)")
    shot(p, "prototypes/discovery-b-role-tabs-1280.png"); p.context.close()
    # Discovery C: a three-question guided path on home.
    for w in (1280, 390):
        p = home_dir(w)
        p.evaluate("""()=>{const s=document.createElement('section');s.className='corners';s.style.marginTop='48px';s.innerHTML='<span class=cb></span><p class=kicker>Find a tool in three questions</p><h2 style="margin:12px 0 24px">Where will you use it?</h2><div class=filters style="margin:0">'+['On the unit','At a desk','For school'].map((t,i)=>`<button type=button${i==0?' class=primary':''}>${t}</button>`).join('')+'</div><p class=foot-note style="margin-top:24px">Next: what slows you down, and can it touch patient information? Then we show 3 to 5 tools with their reality checks.</p>';document.querySelector('.hero').after(s)}""")
        p.evaluate("scrollTo(0, document.querySelector('.hero').getBoundingClientRect().bottom+scrollY-24)")
        shot(p, f"prototypes/discovery-c-guided-{w}.png"); p.context.close()

    # Newsletter A: what you get, with a sample issue link.
    for scheme in ("light", "dark"):
        p = ctx(br, 1280, 800, scheme); p.goto(B + "/tools/goodnurse")
        p.evaluate("""()=>{const s=document.querySelector('.news .sub');s.innerHTML='Every Tuesday, five minutes:';const ul=document.createElement('ul');ul.style.cssText='margin:12px 0 0;padding-left:20px;color:var(--menuText);display:grid;gap:4px';ul.innerHTML='<li>New and changed listings, with what changed in the reality check</li><li>One rollout story from a real unit</li><li>One safe-use tip for the bedside or for school</li>';s.after(ul);const a=document.createElement('p');a.className='sub';a.innerHTML='<a href="#" style="color:var(--menuText)">Read the latest issue</a>. Unsubscribe in one click. We never share your address.';ul.after(a)}""")
        p.evaluate("scrollTo(0, document.querySelector('.news').getBoundingClientRect().top+scrollY-24)")
        shot(p, f"prototypes/newsletter-a-what-you-get-{scheme}.png"); p.context.close()
    # Newsletter B: an inline card inside the directory after row 8.
    p = home_dir(390)
    p.evaluate("""()=>{const li=document.createElement('li');li.style.cssText='list-style:none;margin:24px 0;padding:24px 16px;background:var(--menu);color:var(--menuText)';li.innerHTML='<p class=kicker style="color:var(--bandSoft)">The weekly note</p><p style="font:500 22px/1.2 var(--f-display);margin:8px 0 16px">Get changes to these listings once a week.</p><div style="display:flex;flex-wrap:wrap;gap:8px"><input type=email placeholder="you@example.com" style="flex:1 1 200px"><button class=primary style="border-color:var(--menuText);background:var(--menuText);color:var(--menu)">Subscribe</button></div>';const rows=document.querySelectorAll('[data-card]');rows[7].after(li);scrollTo(0,li.getBoundingClientRect().top+scrollY-200)}""")
    shot(p, "prototypes/newsletter-b-inline-phone.png"); p.context.close()

    # Persona entry points: nav plus a leaders page sketch.
    for w in (1280, 390):
        p = ctx(br, w, 800 if w > 400 else 844); p.goto(B + "/students")
        p.evaluate("""()=>{const nav=document.querySelector('.mast nav');nav.innerHTML='<a href="/">Directory</a><a href="/students">Students</a><a href="/leaders" aria-current=page>Leaders</a><a href="/educators">Educators</a><a href="/about">About</a>';const d=document.querySelector('.deck');d.querySelector('.kicker').textContent='Nurse managers and informatics';d.querySelector('h1').textContent='Choosing AI for your unit';d.querySelector('.lede').textContent='What to pilot for documentation, handoff and staffing, the questions to ask a vendor, and what other units learned.';d.querySelector('.sub').textContent='Every listing shows who it is built for, its HIPAA statement and bedside fit, sourced from the vendor and dated.';const g=document.querySelectorAll('.guides a');['Ambient documentation for nurses: a pilot checklist','Twelve questions to ask an AI vendor','Handoff and summaries tools compared','Staffing and scheduling tools compared','Getting a BAA: what to ask and who signs','Measuring a pilot: workarounds removed, not minutes saved','Browse the directory by unit need'].forEach((t,i)=>{if(g[i])g[i].textContent=t})}""")
        shot(p, f"prototypes/personas-leaders-hub-{w}.png"); p.context.close()

    # Starter guide on a tool page: "Before you use it".
    for w in (1280, 390):
        p = tool_page(w)
        p.evaluate("""()=>{const s=document.createElement('section');s.className='rule';s.style.maxWidth='860px';s.innerHTML='<p class=kicker>Before you use it</p><h2 style="font-size:28px;margin:8px 0 16px">Starting with Abridge for Nurses on your unit</h2><ol style="display:grid;gap:8px;padding-left:20px;margin:0"><li>Ask your nurse informatics team whether your facility has an approved deployment. Do not install a consumer copy.</li><li>Ask whether it connects to your EHR so drafts land in the chart. The vendor does not list integrations publicly.</li><li>Read every draft before you sign it. You are still the author of the note.</li></ol><p class=note>Questions to bring: Is there a BAA? Who reviews errors? Can I turn it off for a patient who declines?</p>';document.querySelector('.check').after(s)}""")
        p.evaluate("scrollTo(0, document.querySelector('.rule').getBoundingClientRect().top+scrollY-24)")
        shot(p, f"prototypes/starter-before-you-use-{w}.png"); p.context.close()
    # Comparison: two ambient tools side by side, values from tools.json.
    a, b = TOOLS["abridge-for-nurses"], TOOLS["nabla"]
    rows = "".join(f"<dt>{l}</dt><dd>{a[k]}</dd><dd>{b[k]}</dd>" for l, k in (("Built for", "built"), ("HIPAA status", "hstat"), ("Bedside fit", "fit"), ("EHR", "ehr"), ("Category", "category")))
    p = ctx(br, 1280, 800); p.goto(B + "/students/best-ai-nclex-prep")
    p.evaluate("""([a,b,rows])=>{const d=document.querySelector('.deck');d.querySelector('.kicker').textContent='Compare';d.querySelector('h1').textContent=a+' vs '+b;d.querySelector('.lede').textContent='Two ambient documentation tools, the same facts in the same order.';d.querySelector('.sub').textContent='Values are the directory entries as of this build.';document.querySelector('.prose').innerHTML='<dl class=spec style="grid-template-columns:200px 1fr 1fr"><dt></dt><dd><b>'+a+'</b></dd><dd><b>'+b+'</b></dd>'+rows+'</dl>'}""", [a["name"], b["name"], rows])
    shot(p, "prototypes/compare-two-tools-1280.png"); p.context.close()

    # ---- Gallery ----
    PAGES = {"home": "/", "directory-filtered": "/#directory", "tool": "/tools/abridge-for-nurses", "students": "/students",
             "guide": "/students/best-ai-nclex-prep", "about": "/about", "submit": "/submit", "404": "/no-such-page"}
    for (w, h) in ((390, 844), (1280, 800)):
        for scheme in ("light", "dark"):
            p = ctx(br, w, h, scheme)
            for name, path in PAGES.items():
                p.goto(B + path); p.wait_for_load_state("networkidle")
                if name == "directory-filtered":
                    p.select_option("[data-filter-category]", "Education / NCLEX"); p.check("[data-filter-trait=nurses]")
                    p.evaluate("scrollTo(0, document.querySelector('#dir-h').getBoundingClientRect().top+scrollY-24)")
                shot(p, f"gallery/{name}-{w}-{scheme}.png")
            p.context.close()
    br.close()
print("ok")
