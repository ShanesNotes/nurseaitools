import glob,html,json,os,re
exec(open('tools.py').read());exec(open('reality.py').read())
BASE="https://nurseaitools.com"
HIP={"deepscribe","nabla","navina","caregility","clinicalkey","lyrebird","tali.ai","sully","getfreed","hippocratic","care.coach","heidihealth","hyro","suki","artisight","andorhealth"}
CATS=[A,H,C,E,K,S,P,G]
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
e=html.escape
tools=[]
for n,v,u,c,d,x in T:
    h=("Vendor website mentions HIPAA (checked Oct 15, 2026). BAA availability not confirmed here; ask the vendor." if any(k in u for k in HIP)
       else "Consumer version: do not enter patient information (PHI). Enterprise/BAA terms vary; check with your organization." if c==G
       else "Study tool: never enter real patient information (PHI). Use made-up or de-identified cases only." if c in (E,K)
       else "Not publicly stated on vendor homepage; verify with vendor.")
    hs=("Mentions HIPAA" if any(k in u for k in HIP) else "Not for patient info" if c in (G,E,K) else "Unknown")
    bf,fit=R[n]
    tools.append(dict(built=bf,hstat=hs,fit=fit,slug=slug(n),name=n,vendor=v,url=u,category=c,what=d,ehr=x or "Not publicly listed; check with vendor",hipaa=h))

TRAITS=[{"key":"nurses","label":"Built for nurses","match":lambda t:t["built"]=="Nurses"},{"key":"hipaa","label":"HIPAA-ready","match":lambda t:t["hstat"]=="Mentions HIPAA"}]
BAYS=[("Built for","built"),("HIPAA status","hstat"),("Bedside fit","fit")]
TONE={"Unknown":"caution","Not for patient info":"caution","Mentions HIPAA":"stated"}
SCRIPTS={"/js/"+os.path.basename(f):open(f).read() for f in sorted(glob.glob("web/*.js"))}

CSS="""
:root{--color-bg:#0a0c10;--color-surface:#11141a;--color-thead:#141821;--color-hover:#1d222c;
 --color-text:#e7e9ee;--color-muted:#8b93a1;--color-faint:#868d99;--color-line:#3a4250;--color-line-strong:#5c6578;
 --color-mark:#e6c87e;--color-accent:#e7e9ee;--color-accent-text:#0a0c10;
 --accent-red:#e87878;--accent-blue:#4aa3ff;--accent-green:#3fae5c;--accent-yellow:#e6c87e;
 --font:ui-monospace,"Cascadia Mono","Segoe UI Mono",Menlo,Consolas,monospace;
 --text-12:12px;--text-13:13px;--text-14:14px;--text-16:16px;--text-20:20px;--text-24:24px;
 --space-2:4px;--space-3:8px;--space-4:12px;--space-5:16px;--space-6:24px;--space-7:32px;
 --viewport:100vh;--radius:2px;--rule:1px;--ring:2px;--stripe:4px;--tap:44px;--box:16px;
 --wrap:1200px;--measure:72ch;--what:62ch;--field-min:240px;--select-min:240px;--term:200px;--label:112px;
 --index:240px minmax(0,1fr) 96px 176px 184px;color-scheme:dark}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scrollbar-color:var(--color-line-strong) var(--color-bg);caret-color:var(--color-text)}
body{margin:0;min-height:var(--viewport);display:flex;flex-direction:column;background:var(--color-bg);color:var(--color-text);font:var(--text-16)/1.5 var(--font);font-variant-ligatures:none;font-variant-numeric:tabular-nums slashed-zero;overflow-wrap:break-word}
main{flex:1;padding-bottom:var(--space-7)}
::selection{background:var(--color-text);color:var(--color-bg)}
::placeholder{color:var(--color-faint);opacity:1}
[hidden]{display:none!important}
h1,h2,p,ul{margin:0}
h1,h2{font-weight:600;line-height:1.25;text-wrap:balance}
a{color:inherit;text-decoration-thickness:var(--rule);text-underline-offset:var(--space-2)}
a:hover{text-decoration-thickness:var(--ring)}
:focus-visible{outline:var(--ring) solid var(--color-mark);outline-offset:var(--ring)}
.wrap{width:100%;max-width:var(--wrap);margin-inline:auto;padding-inline:var(--space-5)}
.sr,.skip:not(:focus),.entry .bay dt{position:absolute;width:var(--rule);height:var(--rule);overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.skip{position:absolute;top:var(--space-3);left:var(--space-5);z-index:2;display:inline-flex;align-items:center;min-height:var(--tap);padding-inline:var(--space-4);background:var(--color-accent);color:var(--color-accent-text);font-weight:600}
.stripe{display:grid;grid-template-columns:repeat(4,minmax(0,1fr))}
.stripe i{border-top:var(--stripe) solid var(--accent-red)}
.stripe i:nth-child(2){border-top-color:var(--accent-blue)}
.stripe i:nth-child(3){border-top-color:var(--accent-green)}
.stripe i:nth-child(4){border-top-color:var(--accent-yellow)}
.mast{border-bottom:var(--rule) solid var(--color-line-strong)}
.mast .wrap{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:0 var(--space-6);padding-block:var(--space-3)}
.mark{display:inline-flex;align-items:center;min-height:var(--tap);font-size:var(--text-20);font-weight:600;text-decoration:none}
.mast nav{display:flex;flex-wrap:wrap;column-gap:var(--space-5);font-size:var(--text-14)}
.mast nav a{display:inline-flex;align-items:center;min-height:var(--tap);text-decoration:none}
.mast nav a:hover,.mast nav a[aria-current=page]{text-decoration:underline}
.mast nav a[aria-current=page]{text-decoration-thickness:var(--ring)}
.deck{display:grid;gap:var(--space-4);max-width:var(--measure);padding-block:var(--space-7) var(--space-6)}
h1{font-size:var(--text-24)}
.sub{color:var(--color-muted);font-size:var(--text-14)}
input:not([type=checkbox]),select,textarea{width:100%;min-height:var(--tap);margin:0;padding:var(--space-3) var(--space-4);border:var(--rule) solid var(--color-line-strong);border-radius:var(--radius);background:var(--color-bg);color:var(--color-text);font:inherit}
textarea{resize:vertical}
input[aria-invalid=true],select[aria-invalid=true],textarea[aria-invalid=true]{border-color:var(--accent-red)}
button{min-height:var(--tap);margin:0;padding:var(--space-3) var(--space-5);border:var(--rule) solid var(--color-line-strong);border-radius:var(--radius);background:var(--color-surface);color:var(--color-text);font:600 var(--text-14)/1.2 var(--font);cursor:pointer}
button:hover{background:var(--color-hover)}
button:disabled{cursor:wait}
.primary,.primary:hover{border-color:var(--color-accent);background:var(--color-accent);color:var(--color-accent-text)}
.find{display:grid;gap:var(--space-3)}
.find label,.pick,.field{font-size:var(--text-14);font-weight:600}
.filters{display:flex;flex-wrap:wrap;align-items:center;gap:var(--space-3) var(--space-4);margin-block:var(--space-4) var(--space-5)}
.pick{display:flex;align-items:center;gap:var(--space-3)}
.pick select{width:auto;min-width:var(--select-min);font-weight:400}
.toggle{display:inline-flex;align-items:center;gap:var(--space-3);min-height:var(--tap);padding-inline:var(--space-4);border:var(--rule) solid var(--color-line-strong);border-radius:var(--radius);background:var(--color-surface);font-size:var(--text-14);font-weight:600;cursor:pointer;-webkit-user-select:none;user-select:none}
.toggle:hover{background:var(--color-hover)}
.toggle:has(:checked){border-color:var(--color-text)}
.toggle input{width:var(--box);height:var(--box);margin:0;accent-color:var(--color-text)}
.count{margin-left:auto;color:var(--color-muted);font-size:var(--text-14)}
.sheet{border:var(--rule) solid var(--color-line-strong);border-radius:var(--radius);background:var(--color-surface)}
.cols{position:sticky;top:0;z-index:1;display:grid;grid-template-columns:var(--index);column-gap:var(--space-5);row-gap:var(--space-2);align-items:end;padding:var(--space-3) var(--space-5);border-bottom:var(--rule) solid var(--color-line-strong);background:var(--color-thead);color:var(--color-muted);font-size:var(--text-12);font-weight:600}
.cols span{grid-row:2}
.cols .group{grid-row:1;grid-column:3/-1;padding-bottom:var(--space-2);border-bottom:var(--ring) solid var(--accent-blue)}
.index{list-style:none;margin:0;padding:0}
.entry{position:relative;display:grid;grid-template-columns:var(--index);column-gap:var(--space-5);row-gap:var(--space-3);align-items:start;padding:var(--space-4) var(--space-5);border-bottom:var(--rule) solid var(--color-line)}
.entry:last-child{border-bottom:0}
.entry:hover,.entry:has(a:focus-visible){background:var(--color-hover)}
.entry h2{font-size:var(--text-16)}
.entry h2 a{text-decoration:none}
.entry h2 a::after{content:"";position:absolute;inset:0}
.entry:hover h2 a{text-decoration:underline}
.meta{margin-top:var(--space-2);color:var(--color-muted);font-size:var(--text-13)}
.cat{white-space:nowrap}
.what{max-width:var(--what);font-size:var(--text-14)}
.rc{margin:0}
.entry .rc{display:contents}
.bay{display:grid;align-content:start;gap:var(--space-2)}
.bay dt{color:var(--color-muted);font-size:var(--text-12);font-weight:600}
.bay dd{justify-self:start;margin:0;font-size:var(--text-13);font-weight:600;line-height:1.35}
.caution dd,.stated dd{padding-inline:var(--space-2);border:var(--rule) dashed var(--color-muted);border-radius:var(--radius)}
.stated dd{border-style:solid;border-color:var(--accent-green)}
.empty{display:flex;flex-wrap:wrap;align-items:center;gap:var(--space-4) var(--space-6);padding:var(--space-6) var(--space-5)}
.news{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:start;gap:var(--space-5) var(--space-6);margin-top:var(--space-7);padding:var(--space-6);border:var(--rule) solid var(--color-line-strong);border-radius:var(--radius);background:var(--color-surface)}
.news h2{margin-bottom:var(--space-3);font-size:var(--text-20)}
.phrase{white-space:nowrap}
.news form{display:flex;flex-wrap:wrap;gap:var(--space-3)}
.news input{flex:1 1 var(--field-min);width:auto}
.msg{flex-basis:100%;font-size:var(--text-14);font-weight:600}
.msg:empty{display:none}
.hp{display:none}
.prose{max-width:var(--measure);padding-top:var(--space-7)}
.deck+.prose{padding-top:0}
.deck+.prose>h2:first-child{margin-top:0}
.prose+section,.prose+.sheet{margin-top:var(--space-7)}
.prose h1{margin-bottom:var(--space-4)}
.prose h2{margin:var(--space-7) 0 var(--space-4);font-size:var(--text-20)}
.prose p+p,.prose ul+p{margin-top:var(--space-5)}
.prose ul{display:grid;gap:var(--space-3);padding-left:var(--space-6)}
.prose .guides{gap:0}
.guides a,.back a{display:inline-flex;align-items:center;min-height:var(--tap)}
.rule{margin-top:var(--space-7);padding-left:var(--space-5);border-left:var(--ring) solid var(--accent-red)}
.prose .rule h2{margin-top:0}
.stack{display:grid;gap:var(--space-5);margin-top:var(--space-6)}
.field{display:grid;gap:var(--space-3)}
.field input,.field select,.field textarea{font-weight:400}
.actions{display:flex;flex-wrap:wrap;align-items:center;gap:var(--space-4) var(--space-5)}
.actions .msg{flex-basis:auto}
.back{padding-top:var(--space-5);font-size:var(--text-14)}
.tool{max-width:var(--measure);padding-top:var(--space-4)}
.by{margin-top:var(--space-2);color:var(--color-muted)}
.check{margin-top:var(--space-6);padding:var(--space-5);border:var(--rule) solid var(--color-line-strong);border-left:var(--ring) solid var(--accent-blue);border-radius:var(--radius);background:var(--color-surface)}
.check h2{margin-bottom:var(--space-4);font-size:var(--text-16)}
.check .rc{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--space-5)}
.check dd{font-size:var(--text-16)}
.note{margin-top:var(--space-4);color:var(--color-muted);font-size:var(--text-13)}
.spec{display:grid;grid-template-columns:var(--term) minmax(0,1fr);margin:var(--space-6) 0 0;border-top:var(--rule) solid var(--color-line-strong)}
.spec dt,.spec dd{margin:0;padding-block:var(--space-4);border-bottom:var(--rule) solid var(--color-line)}
.spec dt{padding-right:var(--space-5);color:var(--color-muted);font-size:var(--text-14);font-weight:600}
.spec dd{overflow-wrap:anywhere}
.fine{margin-top:var(--space-5);color:var(--color-muted);font-size:var(--text-13)}
.foot{padding-block:var(--space-6) var(--space-7);color:var(--color-muted);font-size:var(--text-13)}
.foot p{padding-top:var(--space-5);border-top:var(--rule) solid var(--color-line-strong)}
@media (max-width:960px){.cols{display:none}.entry{grid-template-columns:minmax(0,1fr)}.entry .rc{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--space-4);margin-top:var(--space-2)}
 .entry .bay dt{position:static;width:auto;height:auto;overflow:visible;clip-path:none;white-space:normal}.news{grid-template-columns:minmax(0,1fr)}}
@media (max-width:560px){.rc,.entry .rc,.check .rc{grid-template-columns:minmax(0,1fr);gap:var(--space-3)}.bay{grid-template-columns:var(--label) minmax(0,1fr);align-items:baseline;gap:var(--space-4)}
 .pick{flex:1 1 100%}.pick select{flex:1;min-width:0}.toggle{flex:1 1 auto}.count{flex-basis:100%;margin-left:0}.news{padding:var(--space-5)}.spec{grid-template-columns:minmax(0,1fr)}.spec dt{padding-bottom:0;border-bottom:0}.spec dd{padding-top:var(--space-2)}.check dd{font-size:var(--text-14)}}
"""
CSS="".join(l.strip() for l in CSS.splitlines())
HEAD=("".join(f'<link rel=modulepreload href="{s}">' for s in SCRIPTS if s!="/js/page.js"))
NAV=[("/","Directory"),("/students","Students"),("/submit","Submit a tool"),("/about","About")]
def page(title,desc,body,path):
    nav="".join(f'<a href="{h}"{" aria-current=page" if h==path else ""}>{t}</a>' for h,t in NAV)
    return f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name=description content="{e(desc)}"><link rel=canonical href="{BASE}{path}"><meta property=og:title content="{e(title)}"><meta property=og:description content="{e(desc)}"><meta property=og:type content=website><meta property=og:url content="{BASE}{path}"><meta name=theme-color content="#0a0c10">{HEAD}<style>{CSS}</style></head><body><a class=skip href="#main">Skip to content</a><div class=stripe aria-hidden=true><i></i><i></i><i></i><i></i></div><header class=mast><div class=wrap><a class=mark href="/">Nurse AI Tools</a><nav aria-label=Site>{nav}</nav></div></header><main id=main class=wrap>{body}</main><footer class="wrap foot"><p>© 2026 Nurse AI Tools · Independent directory, not affiliated with listed vendors · Not medical advice. Always follow your facility's policies.</p></footer><script type=module src="/js/page.js"></script></body></html>"""
def bay(label,value): return f'<div class="bay{" "+TONE[value] if value in TONE else ""}"><dt>{label}</dt><dd>{e(value)}</dd></div>'
def plate(t): return "<dl class=rc>"+"".join(bay(l,t[k]) for l,k in BAYS)+"</dl>"
NEWS="""<section class=news aria-labelledby=news-h><div><h2 id=news-h>Get the weekly <span class=phrase>"AI at the bedside"</span> note</h2><p class=sub>New tools, rollouts, and what nurses are saying. No spam.</p></div>
<form action="/api/subscribe" novalidate><label class=sr for=news-email>Email address</label><input id=news-email type=email name=email required autocomplete=email placeholder="you@example.com"><input name=hp class=hp tabindex=-1 autocomplete=off><button class=primary>Subscribe</button><p class=msg id=form-msg data-form-message role=status></p></form></section>"""
P_={}
rows="".join(f'<li class=entry data-card data-id="{t["slug"]}" data-category="{e(t["category"])}" data-text="{e((t["name"]+" "+t["vendor"]+" "+t["what"]).lower())}" data-traits="{" ".join(row["key"] for row in TRAITS if row["match"](t))}"><div class=head><h2><a href="/tools/{t["slug"]}">{e(t["name"])}</a></h2><p class=meta>{e(t["vendor"])} <span aria-hidden=true>·</span> <span class=cat>{e(t["category"])}</span></p></div><p class=what>{e(t["what"])}</p>{plate(t)}</li>' for t in tools)
filters=('<label class=pick>Category<select data-filter-category><option value="">All categories</option>'+"".join(f"<option>{e(c)}</option>" for c in CATS)+"</select></label>"
         +"".join(f'<label class=toggle><input type=checkbox data-filter-trait="{row["key"]}">{e(row["label"])}</label>' for row in TRAITS))
home=f"""<section class=deck><h1>AI tools for nurses, reviewed by a nurse</h1><p class=lede>Most clinical AI is built for physicians. Very few tools are made for bedside nurses yet. We track the ones that are, and tell you what&#39;s safe to use.</p><p class=sub>An independent directory of {len(tools)} AI tools nurses actually run into: ambient charting, handoff, decision support, NCLEX prep, staffing and more.</p></section>
<section data-catalog data-state=idle aria-label=Directory><div class=find><label for=q>Search tools, vendors, or tasks</label><input id=q type=search data-filter-query placeholder="e.g. flowsheet, sepsis, NCLEX" autocomplete=off></div><div class=filters>{filters}<p class=count data-catalog-count aria-live=polite>{len(tools)} tools</p></div><div class=sheet><div class=cols aria-hidden=true><span>Tool</span><span>What it does</span><span class=group>RN reality check</span><span>Built for</span><span>HIPAA status</span><span>Bedside fit</span></div><ul class=index>{rows}</ul><div class=empty data-catalog-empty hidden><p>No tools match this filter.</p><button type=button data-filter-clear>Clear filters</button></div></div></section>{NEWS}"""
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
ab="""<div class=prose><h1>About</h1><p>Nurse AI Tools is run by a registered nurse with 14 years of critical care experience who builds with AI on the side.</p><p>Hospitals are rolling out ambient charting, AI handoffs and early-warning tools fast, and nurses are often the last to hear how they actually work on a real shift. This site aims to be the plain-spoken, nurse-first reference.</p><h2>How listings work</h2><ul><li>Facts (vendor, integrations, HIPAA/BAA statements) come from vendors' public websites and are labeled when unconfirmed.</li><li>Every tool gets an <b>RN reality check</b>: who it is built for, its HIPAA status, and whether it fits a bedside workflow. Each answer comes only from vendor or public information. If we cannot verify it, we say Unknown.</li><li>Listings are independent. Any future sponsored placements will be clearly labeled.</li></ul><p>Nothing here is medical advice. Never enter patient information into a tool your facility hasn't approved.</p></div>"""+NEWS
P_["/about"]=page("About Nurse AI Tools","Nurse AI Tools is an independent, nurse-run directory of AI tools for nurses, nursing students and new grads.",ab,"/about")

BY={t["name"]:t for t in tools}
def entry(t): return f'<li class=entry><div class=head><h2><a href="/tools/{t["slug"]}">{e(t["name"])}</a></h2><p class=meta>{e(t["vendor"])} <span aria-hidden=true>·</span> <span class=cat>{e(t["category"])}</span></p></div><p class=what>{e(t["what"])}</p>{plate(t)}</li>'
def picks(names): return '<div class=sheet><div class=cols aria-hidden=true><span>Tool</span><span>What it does</span><span class=group>RN reality check</span><span>Built for</span><span>HIPAA status</span><span>Bedside fit</span></div><ul class=index>'+"".join(entry(BY[n]) for n in names)+'</ul></div>'
RULE='<p class=sub>No star ratings here. We only rate tools we have used on real shifts or in real study, and we will say so when we do. Everything below is from vendor sites, checked Oct 2026.</p>'
PHI='<section class=rule aria-labelledby=phi-h><h2 id=phi-h>One rule before any of these</h2><p>Never paste real patient details from clinical into any study or AI tool. Change names, dates, ages and rare details, or make the case up. Your school and your clinical site both have policies on this.</p></section>'
SP=[("/students/best-free-ai","Best free AI for nursing students"),("/students/ai-care-plan-tools","AI care plan tools"),("/students/nclex-ai-tutors","NCLEX AI tutors compared")]
def stu(path,title,desc,body):
    side='<p class=back><a href="/students">Back to the students hub</a></p>' if path!="/students" else ""
    P_[path]=page(title+" | Nurse AI Tools",desc,side+body+NEWS,path)
stu("/students","AI tools for nursing students and new grads","AI study tools, care plan helpers and NCLEX AI tutors for nursing students and new grads, with an RN reality check on each.",
 f'<section class=deck><h1>AI for nursing students and new grads</h1><p class=lede>Care plans, pharm, NCLEX, your first year on the floor. Here is which AI tools actually help, and where they can steer you wrong.</p>{RULE}</section><div class=prose><h2>Guides</h2><ul class=guides>'+"".join(f'<li><a href="{p}">{t}</a></li>' for p,t in SP)+f'</ul>{PHI}</div><section aria-label="Student tools">'+picks([t["name"] for t in tools if t["category"] in (E,K)])+'</section>')
stu("/students/best-free-ai","Best free AI for nursing students (2026)","Free and free-tier AI tools nursing students use for studying, flashcards, lecture notes and NCLEX practice, with honest caveats.",
 f'<section class=deck><h1>Best free AI for nursing students</h1><p class=lede>You do not need to pay for AI to get through nursing school. These have a real free option.</p>{RULE}</section><div class=prose><h2>How to use them without getting burned</h2><ul><li>Upload your own lecture slides to NotebookLM so answers come from your course, not the open web.</li><li>General chatbots like ChatGPT and Claude are good at explaining a concept three different ways. They are not a source. Check drug doses and lab values in your drug guide or your school&#39;s references.</li><li>Use AI to quiz you, not to write your graded work. Most programs treat that as an academic integrity issue.</li></ul>{PHI}</div>'
 +picks(["NotebookLM","Knowt","NurseSavvy","ChatGPT","Claude","Gemini","Quizlet","StudyFetch","OpenEvidence"])+'<p class=fine>Free tiers change often. "Free" here means the vendor offers a free plan or free access as of Oct 2026. Some limit how much you can use.</p>')
stu("/students/ai-care-plan-tools","AI care plan tools for nursing students","AI nursing care plan generators compared: CarePlanHQ, Care Plan Genie, PEPID and general chatbots, plus what research says about AI care plan accuracy.",
 f'<section class=deck><h1>AI care plan tools</h1><p class=lede>AI can draft a NANDA-style care plan in seconds. Whether it is right for your patient is still on you.</p>{RULE}</section><div class=prose><h2>What the research says</h2><p>A 2026 scoping review of 15 studies in the Journal of Clinical Nursing found large language models are useful for organizing text, matching standard terminology and drafting goals and interventions, but that privacy, hallucination and bias remain problems and they cannot replace clinical judgment. A scenario study comparing ChatGPT, Gemini and DeepSeek found moderate-to-high quality plans that were still incomplete and written at a college reading level.</p><h2>How to use one well</h2><ul><li>Do your own assessment and pick your priority diagnosis first. Then compare it to what the tool suggests.</li><li>Check every intervention has a rationale you could defend to your instructor.</li><li>Ask your instructor whether AI drafts are allowed for the assignment.</li></ul>{PHI}</div>'
 +picks(["CarePlanHQ","Care Plan Genie","PEPID Nursing Student Care Plan","ChatGPT","Claude"]))
stu("/students/nclex-ai-tutors","NCLEX AI tutors compared (2026)","NCLEX AI tutors and adaptive question banks compared: GoodNurse, NCLEXIT, NurseSavvy, UWorld, Archer Review and more.",
 f'<section class=deck><h1>NCLEX AI tutors compared</h1><p class=lede>The newer NCLEX prep tools add an AI tutor you can argue with. The older question banks have years of polished rationales. Here is how they line up.</p>{RULE}</section><div class=prose><h2>What to compare</h2><ul><li><b>NGN coverage.</b> The current NCLEX tests clinical judgment with case studies, bow-tie, matrix and highlight items. Make sure the bank has all of them.</li><li><b>Rationales vs a tutor.</b> A tutor that answers follow-ups helps when a rationale does not click. AI can also be confidently wrong, so cross-check anything that surprises you.</li><li><b>Readiness exams.</b> Adaptive CAT-style practice tests tell you more than raw percent correct.</li><li><b>Price and free trials.</b> Check the current plan on the vendor site. Prices change.</li></ul></div>'
 +picks(["GoodNurse","NCLEXIT","NurseSavvy","UWorld Nursing","Archer Review","Kaplan NCLEX Prep","SimpleNursing","Lecturio Nursing"])+'<p class=fine>Feature descriptions come from each vendor&#39;s site in Oct 2026. Nurse AI Tools may earn a commission from some NCLEX prep links in the future; that will never change what we write.</p>')
NOT_FOUND=page("Page not found | Nurse AI Tools",HOME_DESC,'<div class=prose><h1>Page not found</h1><p><a href="/">Back to the directory</a></p></div>',"/")
sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{BASE}{p}</loc><lastmod>2026-10-17</lastmod></url>" for p in P_)+"</urlset>"
json.dump(tools,open("tools.json","w"),indent=1)

TEMPLATE=open("worker.template.js").read()
VALUES={"PAGES":json.dumps(P_),"NOT_FOUND":json.dumps(NOT_FOUND),"SITEMAP":json.dumps(sm),"SCRIPTS":json.dumps(SCRIPTS),"BASE":BASE}
def fill(src): return re.sub(r"__(PAGES|NOT_FOUND|SITEMAP|SCRIPTS|BASE)__",lambda m:VALUES[m.group(1)],src)
W=fill(TEMPLATE)
open("dist/worker.js","w").write(W); print(len(tools),"tools",len(P_),"pages",len(W),"bytes")

IMPORT="import { formAt, decide, encodeReply } from '../web/contract.js';\n"
contract=open("web/contract.js").read()
assert TEMPLATE.count(IMPORT)==1 and not re.search(r"^\s*import\b",contract,re.M)
inlined=re.sub(r"^export ","",contract,flags=re.M)
assert not re.search(r"^\s*export\b",inlined,re.M)
D=open("deploy.js").read(); start=D.index("const code=")+len("const code=")
_,end=json.JSONDecoder().raw_decode(D,start)
open("deploy.js","w").write(D[:start]+json.dumps(fill(TEMPLATE.replace(IMPORT,inlined+"\n")))+D[end:])
