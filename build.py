import base64,glob,html,json,os,re
exec(open('tools.py').read());exec(open('reality.py').read())
BASE="https://nurseaitools.com"
HIP={"deepscribe","nabla","navina","caregility","clinicalkey","lyrebird","tali.ai","sully","getfreed","hippocratic","care.coach","heidihealth","hyro","suki","artisight","andorhealth","abridge.com/platform/nursing","hellocare"}
CATS=[A,H,C,E,K,S,P,G]
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
e=html.escape
tools=[]
for n,v,u,c,d,x in T:
    h=("Vendor website mentions HIPAA (checked Oct 2026). BAA availability not confirmed here; ask the vendor." if any(k in u for k in HIP)
       else "Consumer version: do not enter patient information (PHI). Enterprise/BAA terms vary; check with your organization." if c==G
       else "Study tool: never enter real patient information (PHI). Use made-up or de-identified cases only." if c in (E,K)
       else "Not publicly stated on vendor homepage; verify with vendor.")
    hs=("Mentions HIPAA" if any(k in u for k in HIP) else "Not for patient info" if c in (G,E,K) else "Unknown")
    bf,fit=R[n]
    tools.append(dict(built=bf,hstat=hs,fit=fit,slug=slug(n),name=n,vendor=v,url=u,category=c,what=d,ehr=x or "Not publicly listed; check with vendor",hipaa=h))

TRAITS=[{"key":"nurses","label":"Built for nurses","match":lambda t:t["built"]=="Nurses"},{"key":"hipaa","label":"HIPAA-ready","match":lambda t:t["hstat"]=="Mentions HIPAA"}]
BAYS=[("Built for","built"),("HIPAA status","hstat"),("Bedside fit","fit")]
TONE={"Unknown":"caution","Not for patient info":"harm","Mentions HIPAA":"stated"}
SCRIPTS={"/js/"+os.path.basename(f):open(f).read() for f in sorted(glob.glob("web/*.js"))}
FONTS={}
for f in sorted(glob.glob("fonts/*")):
    name=os.path.basename(f); raw=open(f,"rb").read(); key="/fonts/"+name
    FONTS[key]={"type":"font/woff2","b64":base64.b64encode(raw).decode()} if name.endswith(".woff2") else {"type":"text/plain;charset=utf-8","text":raw.decode()}

CSS="""
@font-face{font-family:"Host Grotesk";src:url("/fonts/host-grotesk-latin-400-normal.woff2") format("woff2");font-weight:400;font-style:normal;font-display:swap}
@font-face{font-family:"Host Grotesk";src:url("/fonts/host-grotesk-latin-500-normal.woff2") format("woff2");font-weight:500;font-style:normal;font-display:swap}
@font-face{font-family:"Host Grotesk";src:url("/fonts/host-grotesk-latin-700-normal.woff2") format("woff2");font-weight:700;font-style:normal;font-display:swap}
@font-face{font-family:"JetBrains Mono";src:url("/fonts/jetbrains-mono-latin-400-normal.woff2") format("woff2");font-weight:400;font-style:normal;font-display:swap}
@font-face{font-family:"JetBrains Mono";src:url("/fonts/jetbrains-mono-latin-700-normal.woff2") format("woff2");font-weight:700;font-style:normal;font-display:swap}
:root{color-scheme:light dark;
 --ground:#f6f1e8;--panel:#efe8db;--raised:#fffaf3;--hover:#e9e1d2;--rule:#8a7d68;
 --text:#1c1611;--soft:#5c5348;--muted:#6e4e0c;--pencil:#5e584e;--accent:#6e4e0c;--line:#6e4e0c;
 --up:#1f6b3a;--down:#8d2c1e;--fresh:#1f6b3a;--buy:#1e3f86;--sale:#c9925a;
 --gold:#ffd700;--silver:#c7c7cf;--copper:#eda55f;
 --frame:#e7dfd0;--edge:#6b5e4a;--bar:#dfd3bc;--heading:#6e4e0c;--trim:#6e4e0c;--trimDark:#6b5220;
 --tab:#efe8db;--button:#6e4e0c;--skill:#2f237c;--menu:#1c1611;--menuEdge:#6b5e4a;--menuText:#ece5d3;
 --objective:#1c1611;--complete:#1f6b3a;--orange:#ff8040;--yellow:#ffff00;--green:#40bf40;--gray:#808080;
 --q0:#9d9d9d;--q1:#ffffff;--q2:#1eff00;--q3:#0070dd;--q4:#a335ee;--q5:#ff8000;--q6:#e6cc80;--q7:#00ccff;
 --pace1:#28ff28;--pace2:#40bf40;--pace3:#ffff00;--pace4:#ff6a50;--pace5:#e8655c;
 --f-display:"Host Grotesk","Helvetica Neue",Arial,sans-serif;
 --f-body:"Host Grotesk","Helvetica Neue",Arial,sans-serif;
 --f-figure:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;
 --display:18px;--title:14px;--body:18px;--figure:15px;--lead:18px;--small:12px;--micro:12px;--button-size:18px;--tracker-head:12px;--tracker-line:12px;
 --s-xs:2px;--s-s:4px;--s-m:8px;--s-l:12px;--s-xl:16px;
 --reach:44px;--rule-w:1px;--ring:2px;--radius:0;
 --viewport:100vh;--wrap:1200px;--measure:68ch;--what:62ch;
 --field-min:220px;--select-min:220px;--term:200px;--label:112px;
 --index:220px minmax(0,1fr) 120px 168px 188px}
@media (prefers-color-scheme:dark){:root{
 --ground:#1c1611;--panel:#211a14;--raised:#221f18;--hover:#2c281f;--rule:#7d7262;
 --text:#ffffff;--soft:#a49d89;--muted:#ffd100;--pencil:#9a9a9a;--accent:#e2b55c;--line:#e2b55c;
 --up:#72c48e;--down:#e4705f;--fresh:#72c48e;--buy:#6a95d8;
 --frame:#1a1712;--edge:#7d7262;--bar:#2a2318;--heading:#ffd100;--trim:#c9a24a;--trimDark:#6b5220;
 --tab:#1c1912;--button:#ffd100;--menu:#0b0a08;--menuEdge:#8e8671;--menuText:#ece5d3;
 --objective:#eeeeee;--complete:#28ff28}}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scrollbar-color:var(--pencil) var(--ground);caret-color:var(--text)}
body{margin:0;min-height:var(--viewport);display:flex;flex-direction:column;background:var(--ground);color:var(--text);font:400 var(--body)/1.5 var(--f-body);font-variant-ligatures:none;font-variant-numeric:tabular-nums slashed-zero;overflow-wrap:break-word}
main{flex:1;padding-bottom:var(--s-xl)}
::selection{background:var(--menu);color:var(--menuText)}
::placeholder{color:var(--pencil);opacity:1}
[hidden]{display:none!important}
h1,h2,p,ul{margin:0}
h1,h2{font-family:var(--f-display);font-weight:500;line-height:1.2;color:var(--heading);text-wrap:balance}
h1,h2,.mark{font-size:var(--display)}
a{color:var(--buy);text-decoration-thickness:var(--rule-w);text-underline-offset:var(--s-s)}
a:hover{text-decoration-thickness:var(--ring)}
:focus-visible{outline:var(--ring) solid var(--accent);outline-offset:var(--ring)}
.wrap{width:100%;max-width:var(--wrap);margin-inline:auto;padding-inline:var(--s-xl)}
.sr,.skip:not(:focus),.entry .bay dt{position:absolute;width:var(--rule-w);height:var(--rule-w);overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.skip{position:absolute;top:var(--s-m);left:var(--s-xl);z-index:2;display:inline-flex;align-items:center;min-height:var(--reach);padding-inline:var(--s-l);background:var(--menu);color:var(--menuText);font:500 var(--button-size)/1.2 var(--f-display);text-decoration:none}
.mast{border-bottom:var(--rule-w) solid var(--edge);background:var(--panel)}
.mast .wrap{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:0 var(--s-xl);padding-block:var(--s-xs)}
.mark{display:inline-flex;align-items:center;min-height:var(--reach);color:var(--heading);font-weight:500;line-height:1;text-decoration:none}
.mast nav{display:flex;flex-wrap:wrap;column-gap:var(--s-xl);font:400 var(--title)/1.2 var(--f-display)}
.mast nav a{display:inline-flex;align-items:center;min-height:var(--reach);color:var(--heading);text-decoration:none}
.mast nav a:hover,.mast nav a[aria-current=page]{text-decoration:underline;text-underline-offset:var(--s-m)}
.mast nav a[aria-current=page]{text-decoration-thickness:var(--ring)}
.deck{display:grid;gap:var(--s-l);max-width:var(--measure);padding-block:var(--s-xl)}
.lede{color:var(--text);font:400 var(--lead)/1.5 var(--f-body)}
.sub,.by,.meta,.fine,.note,.foot{color:var(--soft)}
.sub{font:400 var(--lead)/1.5 var(--f-body)}
.meta,.fine,.note,.what,.bay dd,.spec dt{font-family:var(--f-body)}
.doors{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--s-l);margin-bottom:var(--s-xl)}
.doors a{display:flex;flex-direction:column;justify-content:center;gap:var(--s-s);min-height:var(--reach);padding:var(--s-xl);border:var(--rule-w) solid var(--edge);background:var(--raised);color:var(--text);text-decoration:none}
.doors a:first-child{border-left:var(--ring) solid var(--buy)}
.doors a:hover{background:var(--hover)}
.doors strong{color:var(--text);font:500 var(--body)/1.3 var(--f-display)}
.doors span{color:var(--soft);font:400 var(--small)/1.4 var(--f-body)}
input:not([type=checkbox]),select,textarea{width:100%;min-height:var(--reach);margin:0;padding:var(--s-m) var(--s-l);border:var(--rule-w) solid var(--edge);border-radius:var(--radius);background:var(--raised);color:var(--text);font:400 var(--lead)/1.4 var(--f-body)}
textarea{resize:vertical}
input[aria-invalid=true],select[aria-invalid=true],textarea[aria-invalid=true]{border-color:var(--down)}
button{min-height:var(--reach);margin:0;padding:var(--s-m) var(--s-xl);border:var(--rule-w) solid var(--edge);border-radius:var(--radius);background:var(--raised);color:var(--text);font:400 var(--button-size)/1.2 var(--f-display);cursor:pointer}
button:hover{background:var(--hover)}
button:disabled{cursor:wait}
.primary,.primary:hover{border-color:var(--menu);background:var(--menu);color:var(--menuText)}
.find{display:grid;gap:var(--s-m)}
.find label,.pick,.field{font:500 var(--micro)/1.3 var(--f-display);color:var(--heading)}
.filters{display:flex;flex-wrap:wrap;align-items:center;gap:var(--s-m) var(--s-l);margin-block:var(--s-l)}
.pick{display:flex;align-items:center;gap:var(--s-m)}
.pick select{width:auto;min-width:var(--select-min);font-weight:400;color:var(--text);font-family:var(--f-body)}
.toggle{display:inline-flex;align-items:center;gap:var(--s-m);min-height:var(--reach);padding-inline:var(--s-l);border:var(--rule-w) solid var(--edge);border-radius:var(--radius);background:var(--raised);font:400 var(--small)/1.2 var(--f-body);color:var(--text);cursor:pointer;-webkit-user-select:none;user-select:none}
.toggle:hover{background:var(--hover)}
.toggle:has(:checked){border-color:var(--edge);background:var(--bar)}
.toggle input{width:var(--s-xl);height:var(--s-xl);margin:0;accent-color:var(--text)}
.count{margin-left:auto;color:var(--text);font:400 var(--figure)/1.2 var(--f-figure)}
.sheet{border:var(--rule-w) solid var(--edge);border-radius:var(--radius);background:var(--raised)}
.cols{position:sticky;top:0;z-index:1;display:grid;grid-template-columns:var(--index);column-gap:var(--s-xl);row-gap:var(--s-s);align-items:end;padding:var(--s-m) var(--s-xl);border-bottom:var(--rule-w) solid var(--edge);background:var(--bar);color:var(--heading);font:500 var(--micro)/1.3 var(--f-display)}
.cols span{grid-row:2}
.cols .group{grid-row:1;grid-column:3/-1;padding-bottom:var(--s-s);border-bottom:var(--ring) solid var(--heading)}
.index{list-style:none;margin:0;padding:0}
.entry{position:relative;display:grid;grid-template-columns:var(--index);column-gap:var(--s-xl);row-gap:var(--s-m);align-items:start;padding:var(--s-l) var(--s-xl);border-bottom:var(--rule-w) solid var(--rule)}
.entry:last-child{border-bottom:0}
.entry:hover,.entry:has(a:focus-visible){background:var(--hover)}
.entry h2{color:var(--text);font-size:var(--body)}
.entry h2 a{color:var(--text);text-decoration:none}
.entry h2 a::after{content:"";position:absolute;inset:0}
.entry:hover h2 a{text-decoration:underline}
.meta{margin-top:var(--s-s);font-size:var(--small)}
.cat{white-space:nowrap}
.what{max-width:var(--what);font-size:var(--body);line-height:1.45}
.rc{margin:0}
.entry .rc{display:contents}
.bay{display:grid;align-content:start;gap:var(--s-s)}
.bay dt{color:var(--heading);font:500 var(--micro)/1.3 var(--f-display)}
.bay dd{justify-self:start;margin:0;font-size:var(--body);line-height:1.35}
.caution dd,.stated dd,.harm dd{padding-inline:var(--s-s);border:var(--rule-w) dashed var(--pencil);border-radius:var(--radius)}
.stated dd{border-style:solid;border-color:var(--up)}
.harm dd{border-style:solid;border-color:var(--down)}
.empty{display:flex;flex-wrap:wrap;align-items:center;gap:var(--s-l) var(--s-xl);padding:var(--s-xl)}
.news{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:start;gap:var(--s-xl);margin-top:var(--s-xl);padding:var(--s-xl);border:var(--rule-w) solid var(--edge);border-radius:var(--radius);background:var(--raised)}
.news h2{margin-bottom:var(--s-m)}
.phrase{white-space:nowrap}
.news form{display:flex;flex-wrap:wrap;gap:var(--s-m)}
.news input{flex:1 1 var(--field-min);width:auto}
.msg{flex-basis:100%;font:500 var(--body)/1.3 var(--f-display);color:var(--text)}
.msg:empty{display:none}
.hp{display:none}
.prose{max-width:var(--measure);padding-top:var(--s-xl)}
.deck+.prose{padding-top:0}
.deck+.prose>h2:first-child{margin-top:0}
.prose+section,.prose+.sheet{margin-top:var(--s-xl)}
.prose h1{margin-bottom:var(--s-xl)}
.prose h2{margin:var(--s-xl) 0 var(--s-xl);padding-top:var(--s-l);border-top:var(--rule-w) solid var(--edge)}
.prose p+p,.prose ul+p{margin-top:var(--s-xl)}
.prose ul{display:grid;gap:var(--s-m);padding-left:var(--s-xl)}
.prose .guides{gap:0}
.guides a,.back a,.spec a,.fine a{display:inline-flex;align-items:center;min-height:var(--reach)}
.back{padding-top:var(--s-xl);font:400 var(--small)/1.2 var(--f-body)}
.rule{margin-top:var(--s-xl);padding:var(--s-xl);border:var(--rule-w) solid var(--edge);border-left:var(--ring) solid var(--down);background:var(--raised)}
.prose .rule h2{margin-top:0;padding-top:0;border-top:0}
.stack{display:grid;gap:var(--s-xl);margin-top:var(--s-xl)}
form.stack{padding:var(--s-xl);border:var(--rule-w) solid var(--edge);border-radius:var(--radius);background:var(--raised)}
.field{display:grid;gap:var(--s-m)}
.field input,.field select,.field textarea{font-weight:400}
.actions{display:flex;flex-wrap:wrap;align-items:center;gap:var(--s-l) var(--s-xl)}
.actions .msg{flex-basis:auto}
.tool{max-width:var(--measure);padding-top:var(--s-xl)}
.by{margin-top:var(--s-s);font:400 var(--small)/1.4 var(--f-body)}
.check{margin-top:var(--s-xl);border:var(--rule-w) solid var(--edge);border-left:var(--ring) solid var(--buy);border-radius:var(--radius);background:var(--raised)}
.check h2{margin:0;padding:var(--s-m) var(--s-xl);background:var(--bar);border-bottom:var(--rule-w) solid var(--edge);color:var(--heading);font:500 var(--micro)/1.3 var(--f-display)}
.check .rc{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--s-xl);padding:var(--s-xl)}
.check dd{font-size:var(--body)}
.note{margin:0;padding:0 var(--s-xl) var(--s-xl);font-size:var(--small)}
.spec{display:grid;grid-template-columns:var(--term) minmax(0,1fr);margin:var(--s-xl) 0 0;border-top:var(--rule-w) solid var(--edge)}
.spec dt,.spec dd{margin:0;padding-block:var(--s-l);border-bottom:var(--rule-w) solid var(--rule)}
.spec dt{padding-right:var(--s-xl);font-size:var(--small);font-weight:400;color:var(--heading)}
.spec dd{overflow-wrap:anywhere}
.fine{margin-top:var(--s-xl);font-size:var(--small)}
.foot{padding-block:var(--s-xl);font:400 var(--small)/1.5 var(--f-body)}
.foot p{padding-top:var(--s-xl);border-top:var(--rule-w) solid var(--edge)}
@media (max-width:960px){
.cols{display:none}
.entry{grid-template-columns:minmax(0,1fr)}
.entry .rc{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--s-l);margin-top:var(--s-m)}
.entry .bay dt{position:static;width:auto;height:auto;overflow:visible;clip-path:none;white-space:normal}
.news,.doors{grid-template-columns:minmax(0,1fr)}
}
@media (max-width:560px){
.rc,.entry .rc,.check .rc{grid-template-columns:minmax(0,1fr);gap:var(--s-m)}
.bay{grid-template-columns:var(--label) minmax(0,1fr);align-items:baseline;gap:var(--s-l)}
.pick{flex:1 1 100%;flex-direction:column;align-items:stretch;min-width:0}
.pick select{width:100%;min-width:0;max-width:100%}
.toggle{flex:1 1 auto}
.count{flex-basis:100%;margin-left:0}
.news{padding:var(--s-xl)}
.spec{grid-template-columns:minmax(0,1fr)}
.spec dt{padding-bottom:0;border-bottom:0}
.spec dd{padding-top:var(--s-s)}
}
"""
CSS="".join(l.strip() for l in CSS.splitlines())
HEAD=("".join(f'<link rel=modulepreload href="{s}">' for s in SCRIPTS if s!="/js/page.js")
 +"".join(f'<link rel=preload href="{n}" as=font type="font/woff2" crossorigin>' for n in ("/fonts/host-grotesk-latin-400-normal.woff2","/fonts/host-grotesk-latin-500-normal.woff2","/fonts/jetbrains-mono-latin-400-normal.woff2")))
NAV=[("/","Directory"),("/students","Students"),("/submit","Submit a tool"),("/about","About")]
def page(title,desc,body,path):
    nav="".join(f'<a href="{h}"{" aria-current=page" if h==path else ""}>{t}</a>' for h,t in NAV)
    return f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name=description content="{e(desc)}"><link rel=canonical href="{BASE}{path}"><meta property=og:title content="{e(title)}"><meta property=og:description content="{e(desc)}"><meta property=og:type content=website><meta property=og:url content="{BASE}{path}"><meta name=theme-color content="#f6f1e8" media="(prefers-color-scheme: light)"><meta name=theme-color content="#1c1611" media="(prefers-color-scheme: dark)">{HEAD}<style>{CSS}</style></head><body><a class=skip href="#main">Skip to content</a><header class=mast><div class=wrap><a class=mark href="/">Nurse AI Tools</a><nav aria-label=Site>{nav}</nav></div></header><main id=main class=wrap>{body}</main><footer class="wrap foot"><p>© 2026 Nurse AI Tools · Independent directory, not affiliated with listed vendors · Not medical advice. Always follow your facility's policies.</p></footer><script type=module src="/js/page.js"></script></body></html>"""
def bay(label,value): return f'<div class="bay{" "+TONE[value] if value in TONE else ""}"><dt>{label}</dt><dd>{e(value)}</dd></div>'
def plate(t): return "<dl class=rc>"+"".join(bay(l,t[k]) for l,k in BAYS)+"</dl>"
NEWS="""<section class=news aria-labelledby=news-h><div><h2 id=news-h>Get the weekly <span class=phrase>"AI at the bedside"</span> note</h2><p class=sub>New tools, rollouts, and what nurses are saying. No spam.</p></div>
<form action="/api/subscribe" novalidate><label class=sr for=news-email>Email address</label><input id=news-email type=email name=email required autocomplete=email placeholder="you@example.com"><input name=hp class=hp tabindex=-1 autocomplete=off><button class=primary>Subscribe</button><p class=msg id=form-msg data-form-message role=status></p></form></section>"""
P_={}
rows="".join(f'<li class=entry data-card data-id="{t["slug"]}" data-category="{e(t["category"])}" data-text="{e((t["name"]+" "+t["vendor"]+" "+t["what"]).lower())}" data-traits="{" ".join(row["key"] for row in TRAITS if row["match"](t))}"><div class=head><h2><a href="/tools/{t["slug"]}">{e(t["name"])}</a></h2><p class=meta>{e(t["vendor"])} <span aria-hidden=true>·</span> <span class=cat>{e(t["category"])}</span></p></div><p class=what>{e(t["what"])}</p>{plate(t)}</li>' for t in tools)
filters=('<label class=pick>Category<select data-filter-category><option value="">All categories</option>'+"".join(f"<option>{e(c)}</option>" for c in CATS)+"</select></label>"
         +"".join(f'<label class=toggle><input type=checkbox data-filter-trait="{row["key"]}">{e(row["label"])}</label>' for row in TRAITS))
home=f"""<section class=deck><h1>AI tools for nurses, reviewed by a nurse</h1><p class=lede>AI should run the rules in the background so nurses can run the care.</p><p class=sub>Most clinical AI is built for physicians. Very few tools are made for bedside nurses yet. This independent directory of {len(tools)} tools says, from public vendor information only, what is safe to use.</p></section>
<nav class=doors aria-label="Start here"><a href="/students"><strong>Students and new grads</strong><span>Guides for care plans, NCLEX, and free study tools.</span></a><a href="#directory"><strong>The directory</strong><span>Built for, HIPAA status, and bedside fit on every row.</span></a><a href="/submit"><strong>Submit a tool</strong><span>Vendors and nurses. Reviewed before listing.</span></a></nav>
<section id=directory data-catalog data-state=idle aria-label=Directory><div class=find><label for=q>Search tools, vendors, or tasks</label><input id=q type=search data-filter-query placeholder="e.g. flowsheet, sepsis, NCLEX" autocomplete=off></div><div class=filters>{filters}<p class=count data-catalog-count aria-live=polite>{len(tools)} tools</p></div><div class=sheet><div class=cols aria-hidden=true><span>Tool</span><span>What it does</span><span class=group>RN reality check</span><span>Built for</span><span>HIPAA status</span><span>Bedside fit</span></div><ul class=index>{rows}</ul><div class=empty data-catalog-empty hidden><p>No tools match this filter.</p><button type=button data-filter-clear>Clear filters</button></div></div></section>{NEWS}"""
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
VALUES={"PAGES":json.dumps(P_),"NOT_FOUND":json.dumps(NOT_FOUND),"SITEMAP":json.dumps(sm),"SCRIPTS":json.dumps(SCRIPTS),"FONTS":json.dumps(FONTS),"BASE":BASE}
def fill(src): return re.sub(r"__(PAGES|NOT_FOUND|SITEMAP|SCRIPTS|FONTS|BASE)__",lambda m:VALUES[m.group(1)],src)
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
