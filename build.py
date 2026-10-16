import base64,glob,html,json,os,re
exec(open('tools.py').read());exec(open('reality.py').read())
BASE="https://nurseaitools.com"
HIP={"deepscribe","nabla","navina","caregility","clinicalkey","lyrebird","tali.ai","sully","getfreed","hippocratic","care.coach","heidihealth","hyro","suki","artisight","andorhealth"}
CATS=[A,H,C,E,S,P,G]
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
e=html.escape
tools=[]
for n,v,u,c,d,x in T:
    h=("Vendor website mentions HIPAA (checked Oct 15, 2026). BAA availability not confirmed here; ask the vendor." if any(k in u for k in HIP)
       else "Consumer version: do not enter patient information (PHI). Enterprise/BAA terms vary; check with your organization." if c==G
       else "Not publicly stated on vendor homepage; verify with vendor.")
    hs=("Mentions HIPAA" if any(k in u for k in HIP) else "Not for patient info" if c in (G,E) else "Unknown")
    bf,fit=R[n]
    tools.append(dict(built=bf,hstat=hs,fit=fit,slug=slug(n),name=n,vendor=v,url=u,category=c,what=d,ehr=x or "Not publicly listed; check with vendor",hipaa=h))

# Each filter is one row. page.js treats the key as an opaque string.
TRAITS=[("nurses","Built for nurses",lambda t:t["built"]=="Nurses"),("hipaa","HIPAA-ready",lambda t:t["hstat"]=="Mentions HIPAA")]
BAYS=[("Built for","built"),("HIPAA status","hstat"),("Bedside fit","fit")]
TONE={"Unknown":"caution","Not for patient info":"caution","Mentions HIPAA":"stated"}
SCRIPTS={"/js/"+os.path.basename(f):open(f).read() for f in sorted(glob.glob("web/*.js"))}
FONTS={"/fonts/"+os.path.basename(f):base64.b64encode(open(f,"rb").read()).decode() for f in sorted(glob.glob("fonts/*.woff2"))}

CSS="""
@font-face{font-family:"Syncopate";src:url(/fonts/syncopate-700.woff2) format("woff2");font-weight:700;font-display:swap}
@font-face{font-family:"Source Sans 3";src:url(/fonts/source-sans-3-400.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"Source Sans 3";src:url(/fonts/source-sans-3-600.woff2) format("woff2");font-weight:600;font-display:swap}
:root{--paper:#e7eef2;--ink:#14202b;--field:#123655;--ivory:#f4f1e6;--copper:#8c4a32;--amber:#7a4e00;--amber-bg:#f8edd4;--teal:#0c5c4c;--teal-bg:#e4f3ee;
 --line:#737d85;--hair:#b9c1c6;--muted:#535e67;--cut:10px;--index:minmax(11rem,15rem) minmax(0,1fr) minmax(20.5rem,26rem);--sans:"Source Sans 3",sans-serif;--wide:"Syncopate","Source Sans 3",sans-serif;color-scheme:light}
*,*::before,*::after{box-sizing:border-box}
html{background:var(--paper);color:var(--ink);font:400 1.0625rem/1.5 var(--sans);-webkit-text-size-adjust:100%;scrollbar-color:var(--line) var(--paper);caret-color:var(--field)}
body{margin:0;min-height:100vh;display:flex;flex-direction:column}
main{flex:1;padding-bottom:3rem}
::selection{background:var(--field);color:var(--ivory)}
[hidden]{display:none!important}
h1,h2{font-weight:600;line-height:1.15;margin:0;text-wrap:balance}
h1,.news h2,.prose h2,.check h2,.cols{font-family:var(--wide);font-weight:700;letter-spacing:.03em;line-height:1.25;text-transform:uppercase}
p,ul{margin:0}
a{color:var(--field);text-decoration-thickness:1px;text-underline-offset:.2em}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:2px solid var(--field);outline-offset:2px}
.wrap{width:100%;max-width:72rem;margin-inline:auto;padding-inline:clamp(1rem,4vw,2.5rem)}
.sr,.skip:not(:focus){position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.skip{position:absolute;top:.5rem;left:.5rem;z-index:2;padding:.5rem .75rem;background:var(--ivory);color:var(--ink)}
.mast{background-color:var(--field);background-image:repeating-linear-gradient(135deg,rgb(244 241 230/.05) 0 1px,transparent 1px 5px);color:var(--ivory)}
.mast .wrap{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:.85rem 2.5rem;padding-block:clamp(1.35rem,2.5vw,2rem)}
.mark{font:700 clamp(1.25rem,.1rem + 7.2vw,3rem)/1.05 var(--wide);letter-spacing:.02em;text-transform:uppercase;color:var(--ivory);text-decoration:none}
.mast nav{display:flex;flex-wrap:wrap;column-gap:1.5rem}
.mast nav a{color:var(--ivory);text-decoration:none;display:inline-block;padding-block:.625rem}
.mast nav a:hover,.mast nav a[aria-current=page]{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.4em}
.mast :focus-visible{outline-color:var(--ivory)}
.deck{display:grid;gap:.75rem;max-width:44rem;padding-block:clamp(1.75rem,4vw,2.75rem) 1.5rem}
.deck h1,.prose h1,.tool h1{font-size:clamp(1.35rem,1.05rem + .8vw,1.75rem);max-width:16em}
.lede{font-size:clamp(1.125rem,1rem + .5vw,1.3125rem);line-height:1.45}
.sub{color:var(--muted)}
input:not([type=checkbox]),select,textarea,button,.toggle{
 --edge:var(--line);--fill:var(--ivory);--ring:transparent;--rw:0px;--d:calc(var(--cut)*.7071);
 --cutline:linear-gradient(225deg,transparent var(--d),var(--edge) 0 calc(var(--d) + 1px),var(--ring) 0 calc(var(--d) + 1px + var(--rw)),transparent 0) border-box;
 font:inherit;font-weight:400;color:var(--ink);min-height:2.75rem;margin:0;padding:.5rem .875rem;border:1px solid var(--edge);border-radius:0;
 clip-path:polygon(0 0,calc(100% - var(--cut)) 0,100% var(--cut),100% 100%,0 100%);
 background:var(--cutline),var(--fill);box-shadow:inset 0 0 0 var(--rw) var(--ring)}
input:not([type=checkbox]),select,textarea{width:100%}
textarea{resize:vertical}
::placeholder{color:var(--muted);opacity:1}
input[type=search]::-webkit-search-cancel-button{-webkit-appearance:none}
select{-webkit-appearance:none;appearance:none;padding-right:2.5rem;background:var(--cutline),url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8'%3E%3Cpath d='M1 1.5l5 5 5-5' fill='none' stroke='%2314202b' stroke-width='1.6'/%3E%3C/svg%3E") right .875rem center/12px 8px no-repeat,var(--fill)}
button{font-weight:600;cursor:pointer}
button:hover,.toggle:hover{--edge:var(--ink)}
button:disabled{cursor:wait}
input:not([type=checkbox]):focus-visible,select:focus-visible,textarea:focus-visible,button:focus-visible,.toggle:has(:focus-visible){outline:0;--edge:var(--field);--ring:var(--field);--rw:1px}
input[aria-invalid=true]:not(:focus-visible),select[aria-invalid=true]:not(:focus-visible),textarea[aria-invalid=true]:not(:focus-visible){--edge:var(--amber)}
.primary,.toggle:has(:checked){--edge:var(--field);--fill:var(--field);color:var(--ivory)}
.primary{padding-inline:1.25rem}
.primary:hover{--edge:var(--field);--fill:#1d4a72}
.primary:focus-visible,.toggle:has(:checked):has(:focus-visible){--ring:var(--ivory);--rw:2px}
.toggle{display:inline-flex;align-items:center;gap:.625rem;font-weight:600;cursor:pointer;padding-inline:.875rem 1.125rem;-webkit-user-select:none;user-select:none}
.toggle input{-webkit-appearance:none;appearance:none;flex:none;display:grid;place-content:center;width:1.125rem;height:1.125rem;margin:0;border:1.5px solid currentColor;color:inherit}
.toggle input::before{content:"";width:.6875rem;height:.6875rem;background:currentColor;clip-path:polygon(12% 46%,0 64%,42% 100%,100% 18%,84% 4%,40% 68%);transform:scale(0)}
.toggle input:checked::before{transform:none}
.toggle input:focus-visible{outline:0}
.find{display:grid;gap:.375rem}
.find label,.field,.pick{font-weight:600}
.find input{min-height:3.25rem;font-size:1.125rem;padding-inline:1rem}
.filters{display:flex;flex-wrap:wrap;align-items:center;gap:.75rem 1rem;margin-block:1rem 1.25rem}
.pick{display:flex;align-items:center;gap:.625rem}
.pick select{width:auto;min-width:15rem}
.count{margin-left:auto;color:var(--muted);font-variant-numeric:tabular-nums}
.empty{display:flex;flex-wrap:wrap;align-items:center;gap:.75rem 1.5rem;padding-block:1.5rem;border-bottom:1px solid var(--hair);font-weight:600;font-size:1.125rem}
.cols{display:grid;grid-template-columns:var(--index);column-gap:clamp(1.25rem,3vw,2.5rem);align-items:end;padding-bottom:.625rem;border-bottom:2px solid var(--ink);font-size:.8125rem}
.index{list-style:none;padding:0}
.entry{position:relative;display:grid;grid-template-columns:var(--index);grid-template-areas:"head what rc";column-gap:clamp(1.25rem,3vw,2.5rem);row-gap:.375rem;align-items:start;padding-block:1.125rem 1.25rem;border-bottom:1px solid var(--hair)}
.entry .head{grid-area:head}
.entry h2{font-size:1.1875rem;line-height:1.25}
.entry h2 a{color:var(--ink);text-decoration:none}
.entry h2 a::after{content:"";position:absolute;inset:0}
.entry:hover h2 a{text-decoration:underline;text-decoration-thickness:1px}
.entry h2 a:focus-visible{outline:0}
.entry:has(a:focus-visible){outline:2px solid var(--field);outline-offset:2px}
.meta{color:var(--muted);font-size:.9375rem;margin-top:.125rem}
.what{grid-area:what;max-width:62ch}
.entry .rc{grid-area:rc;align-self:start}
.rc{position:relative;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));margin:0;padding-top:2px;border-bottom:1px solid var(--hair)}
.rc::before{content:"";position:absolute;inset:0 0 auto;height:2px;background:var(--copper);transform-origin:left}
.bay{display:grid;align-content:start;gap:.3125rem;padding:.5rem .625rem .625rem;border-left:1px solid var(--hair)}
.bay:first-child{border-left:0}
.bay dt{font:700 .8125rem/1.25 var(--wide);letter-spacing:.03em;text-transform:uppercase;color:var(--muted)}
.entry .bay dt{min-height:2.5em}
.bay dd{margin:0;font-weight:600;font-size:.9375rem;line-height:1.25}
.caution{background:var(--amber-bg);color:var(--amber)}
.stated{background:var(--teal-bg);color:var(--teal)}
.caution dt,.stated dt{color:inherit}
@keyframes draw{from{transform:scaleX(0)}}
[data-state=filtering] .rc::before{animation:draw 180ms ease-out}
.news{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,28rem);align-items:start;gap:1rem 2.5rem;margin-top:3.5rem;padding-top:1.5rem;border-top:2px solid var(--ink)}
.news h2{font-size:1.0625rem;margin-bottom:.5rem;max-width:22em}
.phrase{white-space:nowrap}
.news form{display:flex;flex-wrap:wrap;gap:.5rem}
.news input{flex:1 1 13rem;width:auto}
.msg{flex-basis:100%;font-weight:600}
.msg:empty{display:none}
[data-state=error] .msg{color:var(--amber)}
[data-state=success] .msg{color:var(--teal)}
.hp{display:none}
.prose{max-width:42rem;padding-top:clamp(1.75rem,4vw,2.75rem)}
.prose h1{margin-bottom:.75rem}
.prose h2{font-size:1rem;margin:2rem 0 .625rem}
.prose p+p,.prose ul+p{margin-top:1rem}
.prose ul{padding-left:1.25rem;display:grid;gap:.5rem}
.stack{display:grid;gap:1.125rem;margin-top:1.75rem}
.field{display:grid;gap:.375rem}
.actions{display:flex;flex-wrap:wrap;align-items:center;gap:.75rem 1.25rem}
.actions .msg{flex-basis:auto}
.back{padding-top:1.5rem}
.tool{max-width:46rem;padding-top:1rem}
.by{color:var(--muted);font-size:1.125rem;margin-top:.375rem}
.check{margin-top:1.75rem}
.check h2{font-size:.9375rem;margin-bottom:.625rem}
.note{color:var(--muted);font-size:.875rem;margin-top:.5rem}
.spec{display:grid;grid-template-columns:minmax(8rem,13rem) minmax(0,1fr);margin:2rem 0 0;border-top:1px solid var(--ink)}
.spec dt,.spec dd{margin:0;padding-block:.75rem;border-bottom:1px solid var(--hair)}
.spec dt{font-weight:600;padding-right:1.5rem}
.spec dd{overflow-wrap:anywhere}
.fine{color:var(--muted);font-size:.875rem;margin-top:1.25rem}
.foot{color:var(--muted);font-size:.875rem;padding-bottom:2rem}
.foot p{padding-top:1.5rem;border-top:1px solid var(--hair)}
@media (max-width:52rem){.cols{display:none}.index{border-top:2px solid var(--ink)}.entry{grid-template-columns:minmax(0,1fr);grid-template-areas:"head" "what" "rc"}.entry .rc{margin-top:.5rem}.news{grid-template-columns:minmax(0,1fr)}}
@media (max-width:32rem){.rc{grid-template-columns:minmax(0,1fr)}.bay{grid-template-columns:7.5rem minmax(0,1fr);align-items:baseline;border-left:0;border-top:1px solid var(--hair)}.bay:first-child{border-top:0}.entry .bay dt{min-height:0}
 .pick{flex:1 1 100%}.pick select{flex:1;min-width:0}.count{flex-basis:100%;margin-left:0}.spec{grid-template-columns:minmax(0,1fr)}.spec dt{border-bottom:0;padding-bottom:0}}
@media (prefers-reduced-motion:reduce){[data-state=filtering] .rc::before{animation:none}}
"""
CSS="".join(l.strip() for l in CSS.splitlines())
HEAD=("".join(f'<link rel=preload href="{f}" as=font type=font/woff2 crossorigin>' for f in FONTS)
      +"".join(f'<link rel=modulepreload href="{s}">' for s in SCRIPTS if s!="/js/page.js"))
NAV=[("/","Directory"),("/submit","Submit a tool"),("/about","About")]
def page(title,desc,body,path):
    nav="".join(f'<a href="{h}"{" aria-current=page" if h==path else ""}>{t}</a>' for h,t in NAV)
    return f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name=description content="{e(desc)}"><link rel=canonical href="{BASE}{path}"><meta property=og:title content="{e(title)}"><meta property=og:description content="{e(desc)}"><meta property=og:type content=website><meta property=og:url content="{BASE}{path}"><meta name=theme-color content="#123655">{HEAD}<style>{CSS}</style></head><body><a class=skip href="#main">Skip to content</a><header class=mast><div class=wrap><a class=mark href="/">Nurse AI Tools</a><nav aria-label=Site>{nav}</nav></div></header><main id=main class=wrap>{body}</main><footer class="wrap foot"><p>© 2026 Nurse AI Tools · Independent directory, not affiliated with listed vendors · Not medical advice. Always follow your facility's policies.</p></footer><script type=module src="/js/page.js"></script></body></html>"""
def bay(label,value): return f'<div class="bay{" "+TONE[value] if value in TONE else ""}"><dt>{label}</dt><dd>{e(value)}</dd></div>'
def plate(t): return "<dl class=rc>"+"".join(bay(l,t[k]) for l,k in BAYS)+"</dl>"
NEWS="""<section class=news aria-labelledby=news-h><div><h2 id=news-h>Get the weekly <span class=phrase>"AI at the bedside"</span> note</h2><p class=sub>New tools, rollouts, and what nurses are saying. No spam.</p></div>
<form action="/api/subscribe" novalidate><label class=sr for=news-email>Email address</label><input id=news-email type=email name=email required autocomplete=email placeholder="you@example.com"><input name=hp class=hp tabindex=-1 autocomplete=off><button class=primary>Subscribe</button><p class=msg id=form-msg data-form-message role=status></p></form></section>"""
P_={}
rows="".join(f'<li class=entry data-card data-id="{t["slug"]}" data-category="{e(t["category"])}" data-text="{e((t["name"]+" "+t["vendor"]+" "+t["what"]).lower())}" data-traits="{" ".join(k for k,_,p in TRAITS if p(t))}"><div class=head><h2><a href="/tools/{t["slug"]}">{e(t["name"])}</a></h2><p class=meta>{e(t["vendor"])} <span aria-hidden=true>·</span> {e(t["category"])}</p></div><p class=what>{e(t["what"])}</p>{plate(t)}</li>' for t in tools)
filters=('<label class=pick>Category<select data-filter-category><option value="">All categories</option>'+"".join(f"<option>{e(c)}</option>" for c in CATS)+"</select></label>"
         +"".join(f'<label class=toggle><input type=checkbox data-filter-trait="{k}">{e(l)}</label>' for k,l,_ in TRAITS))
home=f"""<section class=deck><h1>AI tools for nurses, reviewed by a nurse</h1><p class=lede>Most clinical AI is built for physicians. Very few tools are made for bedside nurses yet. We track the ones that are, and tell you what&#39;s safe to use.</p><p class=sub>An independent directory of {len(tools)} AI tools nurses actually run into: ambient charting, handoff, decision support, NCLEX prep, staffing and more.</p></section>
<section data-catalog data-state=idle aria-label=Directory><div class=find><label for=q>Search tools, vendors, or tasks</label><input id=q type=search data-filter-query placeholder="e.g. flowsheet, sepsis, NCLEX" autocomplete=off></div><div class=filters>{filters}<p class=count data-catalog-count aria-live=polite>{len(tools)} tools</p></div><div class=cols aria-hidden=true><span>Tool</span><span>What it does</span><span>RN reality check</span></div><ul class=index>{rows}</ul><div class=empty data-catalog-empty hidden><p>No tools match this filter.</p><button type=button data-filter-clear>Clear filters</button></div></section>{NEWS}"""
HOME_DESC="Independent directory of AI tools for nurses: ambient documentation, handoff, clinical decision support, NCLEX prep, scheduling and patient communication."
P_["/"]=page("Nurse AI Tools: AI tools for nurses",HOME_DESC,home,"/")
for t in tools:
    b=f"""<p class=back><a href="/">Back to the directory</a></p><article class=tool><h1>{e(t["name"])}</h1><p class=by>by {e(t["vendor"])}</p><section class=check aria-labelledby=rc-h><h2 id=rc-h>RN reality check</h2>{plate(t)}<p class=note>From vendor or public info only. "Unknown" means we could not verify it.</p></section>
<dl class=spec><dt>What it does for nurses</dt><dd>{e(t["what"])}</dd><dt>Category</dt><dd>{e(t["category"])}</dd><dt>Vendor</dt><dd>{e(t["vendor"])}</dd><dt>Official site</dt><dd><a href="{e(t["url"])}" rel="nofollow noopener" target=_blank>{e(t["url"])}</a></dd><dt>EHR integrations</dt><dd>{e(t["ehr"])}</dd><dt>HIPAA / BAA status</dt><dd>{e(t["hipaa"])}</dd></dl>
<p class=fine>Listing info is compiled from the vendor's public website and may change. Vendors can <a href="/submit">submit corrections</a>.</p></article>{NEWS}"""
    P_["/tools/"+t["slug"]]=page(f'{t["name"]} for nurses: features, EHR integrations, HIPAA | Nurse AI Tools',f'{t["name"]} by {t["vendor"]}: {t["what"]}'[:155],b,"/tools/"+t["slug"])
sub=f"""<div class=prose><h1>Submit a tool</h1><p class=sub>Know an AI tool nurses use? Vendors welcome too. Every submission is reviewed before listing.</p>
<form class=stack action="/api/submit" novalidate><label class=field>Tool name<input name=name required autocomplete=off></label><label class=field>Official website<input name=url type=url required placeholder="https://" autocomplete=url></label><label class=field>Category<select name=category>{"".join(f"<option>{e(c)}</option>" for c in CATS)}</select></label><label class=field>Notes<textarea name=notes rows=4 placeholder="What does it do for nurses? EHR integrations? HIPAA/BAA?"></textarea></label><label class=field>Your email (optional)<input name=email type=email autocomplete=email></label><input name=hp class=hp tabindex=-1 autocomplete=off><div class=actions><button class=primary>Submit</button><p class=msg id=form-msg data-form-message role=status></p></div></form></div>"""
P_["/submit"]=page("Submit an AI tool for nurses | Nurse AI Tools","Suggest an AI tool for nurses to be reviewed and listed in the Nurse AI Tools directory.",sub,"/submit")
ab="""<div class=prose><h1>About</h1><p>Nurse AI Tools is curated by a registered nurse with 14 years of critical care experience who builds with AI on the side.</p><p>Hospitals are rolling out ambient charting, AI handoffs and early-warning tools fast, and nurses are often the last to hear how they actually work on a real shift. This site aims to be the plain-spoken, nurse-first reference.</p><h2>How listings work</h2><ul><li>Facts (vendor, integrations, HIPAA/BAA statements) come from vendors' public websites and are labeled when unconfirmed.</li><li>Every tool gets an <b>RN reality check</b>: who it is built for, its HIPAA status, and whether it fits a bedside workflow. Each answer comes only from vendor or public information. If we cannot verify it, we say Unknown.</li><li>Listings are independent. Any future sponsored placements will be clearly labeled.</li></ul><p>Nothing here is medical advice. Never enter patient information into a tool your facility hasn't approved.</p></div>"""+NEWS
P_["/about"]=page("About Nurse AI Tools: curated by a critical care RN","Nurse AI Tools is an independent directory of AI tools for nurses, curated by a critical care registered nurse.",ab,"/about")
# Kept out of P_ so the sitemap skips it. It keeps the homepage canonical the old 404 had.
NOT_FOUND=page("Page not found | Nurse AI Tools",HOME_DESC,'<div class=prose><h1>Page not found</h1><p><a href="/">Back to the directory</a></p></div>',"/")
sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{BASE}{p}</loc><lastmod>2026-10-15</lastmod></url>" for p in P_)+"</urlset>"
json.dump(tools,open("tools.json","w"),indent=1)

TEMPLATE=open("worker.template.js").read()
VALUES={"PAGES":json.dumps(P_),"NOT_FOUND":json.dumps(NOT_FOUND),"SITEMAP":json.dumps(sm),"SCRIPTS":json.dumps(SCRIPTS),"FONTS":json.dumps(FONTS),"BASE":BASE}
def fill(src): return re.sub(r"__(PAGES|NOT_FOUND|SITEMAP|SCRIPTS|FONTS|BASE)__",lambda m:VALUES[m.group(1)],src)
W=fill(TEMPLATE)
open("dist/worker.js","w").write(W); print(len(tools),"tools",len(P_),"pages",len(W),"bytes")

# deploy.js uploads one module with no bundler, so contract.js is inlined in place of its import.
IMPORT="import { formAt, decide, encodeReply } from '../web/contract.js';\n"
contract=open("web/contract.js").read()
assert TEMPLATE.count(IMPORT)==1 and not re.search(r"^\s*import\b",contract,re.M)
inlined=re.sub(r"^export ","",contract,flags=re.M)
assert not re.search(r"^\s*export\b",inlined,re.M)
D=open("deploy.js").read(); start=D.index("const code=")+len("const code=")
_,end=json.JSONDecoder().raw_decode(D,start)
open("deploy.js","w").write(D[:start]+json.dumps(fill(TEMPLATE.replace(IMPORT,inlined+"\n")))+D[end:])
