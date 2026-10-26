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

TRAITS=[{"key":"nurses","label":"Built for nurses","match":lambda t:t["built"]=="Nurses"},{"key":"hipaa","label":"Mentions HIPAA","match":lambda t:t["hstat"]=="Mentions HIPAA"}]
BAYS=[("Built for","built"),("HIPAA status","hstat"),("Bedside fit","fit")]
TONE={"Unknown":"caution","Not for patient info":"harm"}
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
 --ground:#f6f1e8;--panel:#efe8db;--raised:#fffaf3;--hover:#e9e1d2;--bar:#dfd3bc;--rule:#8a7d68;--edge:#6b5e4a;
 --text:#1c1611;--soft:#5c5348;--pencil:#5e584e;--accent:#1f5550;
 --menu:#1c1611;--menuText:#ece5d3;--bandSoft:#b9b09c;
 --f-display:"Host Grotesk","Helvetica Neue",Arial,sans-serif;
 --f-body:"Host Grotesk","Helvetica Neue",Arial,sans-serif;
 --f-figure:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;
 --display:clamp(44px,7.4vw,112px);--headline:clamp(36px,4.6vw,64px);--proof:clamp(36px,5vw,72px);--title:28px;--lead:clamp(20px,1.8vw,24px);
 --body:18px;--figure:15px;--small:15px;--micro:12px;--button-size:18px;
 --tight:-0.035em;--snug:-0.02em;--tracked:0.02em;
 --s-xs:2px;--s-s:4px;--s-m:8px;--s-l:12px;--s-xl:16px;--s-2xl:24px;--s-3xl:32px;--s-4xl:48px;--s-5xl:64px;--s-6xl:96px;
 --section:96px;--reach:44px;--field-tall:56px;--corner:12px;--rule-w:1px;--ring:2px;--radius:0;
 --viewport:100vh;--wrap:1288px;--measure:66ch;--what:58ch;--lede-measure:32ch;
 --field-min:220px;--select-min:220px;--term:200px;--label:112px;
 --column:860px;
 --index:220px minmax(0,1fr) 104px 196px 208px}
@media (prefers-color-scheme:dark){:root{
 --ground:#1c1611;--panel:#211a14;--raised:#221f18;--hover:#2c281f;--bar:#2a2318;--rule:#7d7262;--edge:#7d7262;
 --text:#ffffff;--soft:#a49d89;--pencil:#9a9a9a;--accent:#7dbab0;
 --menu:#0b0a08;--menuText:#ece5d3}}
@media (max-width:720px){:root{--section:64px}}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scrollbar-color:var(--pencil) var(--ground);caret-color:var(--text)}
body{margin:0;min-height:var(--viewport);display:flex;flex-direction:column;background:var(--ground);color:var(--text);font:400 var(--body)/1.55 var(--f-body);font-variant-ligatures:none;font-variant-numeric:tabular-nums slashed-zero;overflow-wrap:break-word}
main{flex:1;padding-bottom:var(--section)}
::selection{background:var(--menu);color:var(--menuText)}
::placeholder{color:var(--pencil);opacity:1}
[hidden]{display:none!important}
h1,h2,p,ul,dl,dd{margin:0}
q{quotes:'"' '"' "'" "'"}
p,li,dd{text-wrap:pretty}
h1,h2{font-family:var(--f-display);font-weight:500;line-height:1.05;color:var(--text);letter-spacing:var(--snug);text-wrap:balance}
h1{font-size:var(--headline)}
h2{font-size:var(--title)}
a{color:var(--accent);text-decoration-thickness:var(--rule-w);text-underline-offset:var(--s-s);transition:text-decoration-color .15s,background-color .15s}
a:hover{text-decoration-thickness:var(--ring)}
:focus-visible{outline:var(--ring) solid var(--accent);outline-offset:var(--ring)}
.wrap{width:100%;max-width:var(--wrap);margin-inline:auto;padding-inline:var(--s-2xl)}
.sr,.skip:not(:focus),.entry .bay dt{position:absolute;width:var(--rule-w);height:var(--rule-w);overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.skip{position:absolute;top:var(--s-m);left:var(--s-xl);z-index:3;display:inline-flex;align-items:center;min-height:var(--reach);padding-inline:var(--s-l);background:var(--menu);color:var(--menuText);font:500 var(--button-size)/1.2 var(--f-display);text-decoration:none}
.kicker,.find label,.pick,.field,.cols,.bay dt,.spec dt,.check h2{color:var(--soft);font:400 var(--micro)/1.4 var(--f-figure);letter-spacing:var(--tracked)}
.mast{border-bottom:var(--rule-w) solid var(--rule)}
.mast .wrap{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:0 var(--s-2xl);padding-block:var(--s-s)}
.mark{display:inline-flex;align-items:center;min-height:var(--reach);color:var(--text);font:500 var(--lead)/1 var(--f-display);letter-spacing:var(--snug);text-decoration:none;white-space:nowrap}
.mast nav{display:flex;flex-wrap:wrap;column-gap:var(--s-2xl);font:400 var(--small)/1.2 var(--f-body)}
.mast nav a{display:inline-flex;align-items:center;min-height:var(--reach);color:var(--text);text-decoration:none}
.mast nav a:hover,.mast nav a[aria-current=page]{text-decoration:underline;text-underline-offset:var(--s-m)}
.mast nav a[aria-current=page]{text-decoration-thickness:var(--ring)}
.hero{padding-block:var(--s-5xl)}
.hero h1{margin-top:var(--s-2xl);font-size:var(--display);line-height:.92;letter-spacing:var(--tight)}
.hero .lede{max-width:var(--lede-measure);margin-top:var(--s-3xl)}
.acts{display:flex;flex-wrap:wrap;gap:var(--s-l) var(--s-4xl);margin-top:var(--s-4xl)}
.acts a{display:inline-flex;align-items:center;min-height:var(--reach);color:var(--text);font:500 var(--title)/1.2 var(--f-display);letter-spacing:var(--snug);text-decoration-thickness:var(--ring);text-underline-offset:var(--s-m)}
.acts a:hover{color:var(--accent)}
.corners{position:relative;padding:var(--s-3xl) var(--s-4xl)}
.corners::before,.corners::after,.corners>.cb::before,.corners>.cb::after{content:"";position:absolute;width:var(--corner);height:var(--corner);border:0 solid var(--text)}
.corners::before{top:0;left:0;border-top-width:var(--rule-w);border-left-width:var(--rule-w)}
.corners::after{top:0;right:0;border-top-width:var(--rule-w);border-right-width:var(--rule-w)}
.corners>.cb::before{bottom:0;left:0;border-bottom-width:var(--rule-w);border-left-width:var(--rule-w)}
.corners>.cb::after{bottom:0;right:0;border-bottom-width:var(--rule-w);border-right-width:var(--rule-w)}
.figs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--s-2xl);margin-block:var(--s-2xl)}
.fig{display:flex;flex-direction:column;gap:var(--s-m);padding-left:var(--s-xl);border-left:var(--rule-w) solid var(--text)}
.fig b{color:var(--text);font:400 var(--proof)/1 var(--f-figure);letter-spacing:var(--tight)}
.fig span{color:var(--text);font:400 var(--small)/1.35 var(--f-body)}
.fig.unk{border-left-style:dashed;border-left-color:var(--pencil)}
.fig.unk b{color:var(--pencil)}
.foot-note{color:var(--soft);font:400 var(--small)/1.5 var(--f-body)}
.sect{display:flex;flex-wrap:wrap;align-items:end;justify-content:space-between;gap:var(--s-m) var(--s-2xl);padding-top:var(--section);margin-bottom:var(--s-3xl)}
.sect h2{font-size:var(--headline);letter-spacing:var(--tight)}
.deck{display:grid;gap:var(--s-2xl);max-width:var(--measure);padding-block:var(--s-5xl) var(--s-3xl)}
.lede{color:var(--soft);font:400 var(--lead)/1.4 var(--f-body)}
.sub,.by,.meta,.fine,.note,.foot{color:var(--soft)}
.sub{font:400 var(--body)/1.55 var(--f-body)}
input:not([type=checkbox]),select,textarea{width:100%;min-height:var(--reach);margin:0;padding:var(--s-m) var(--s-l);border:var(--rule-w) solid var(--edge);border-radius:var(--radius);background:var(--raised);color:var(--text);font:400 var(--body)/1.4 var(--f-body)}
textarea{resize:vertical}
input[aria-invalid=true],select[aria-invalid=true],textarea[aria-invalid=true]{border-width:var(--ring);border-color:var(--text)}
button{min-height:var(--reach);margin:0;padding:var(--s-m) var(--s-2xl);border:var(--rule-w) solid var(--edge);border-radius:var(--radius);background:var(--raised);color:var(--text);font:500 var(--button-size)/1.2 var(--f-display);cursor:pointer;transition:background-color .15s}
button:hover{background:var(--hover)}
button:disabled{cursor:wait}
.primary,.primary:hover{border-color:var(--menu);background:var(--menu);color:var(--menuText)}
.find{display:grid;gap:var(--s-m)}
.find input{min-height:var(--field-tall);padding-inline:var(--s-xl);border-color:var(--text);font-size:var(--lead)}
.filters{display:flex;flex-wrap:wrap;align-items:center;gap:var(--s-m) var(--s-l);margin-block:var(--s-l) var(--s-3xl)}
.pick{display:flex;align-items:center;gap:var(--s-m)}
.pick select{width:auto;min-width:var(--select-min);color:var(--text);font:400 var(--small)/1.2 var(--f-body);letter-spacing:normal}
.toggle{display:inline-flex;align-items:center;gap:var(--s-m);min-height:var(--reach);padding-inline:var(--s-l);border:var(--rule-w) solid var(--edge);border-radius:var(--radius);background:var(--raised);font:400 var(--small)/1.2 var(--f-body);color:var(--text);cursor:pointer;-webkit-user-select:none;user-select:none;transition:background-color .15s}
.toggle:hover{background:var(--hover)}
.toggle:has(:checked){border-color:var(--accent);background:var(--bar)}
.toggle input{width:var(--s-xl);height:var(--s-xl);margin:0;accent-color:var(--accent)}
.count{margin-left:auto;color:var(--text);font:400 var(--figure)/1.2 var(--f-figure)}
.cols{position:sticky;top:0;z-index:1;display:grid;grid-template-columns:var(--index);column-gap:var(--s-2xl);row-gap:var(--s-s);align-items:end;padding:var(--s-l) 0;border-bottom:var(--rule-w) solid var(--text);background:var(--ground)}
.cols span{grid-row:2}
.cols .group{grid-row:1;grid-column:3/-1;padding-bottom:var(--s-s);border-bottom:var(--ring) solid var(--accent)}
.index{list-style:none;margin:0;padding:0}
.entry{position:relative;display:grid;grid-template-columns:var(--index);column-gap:var(--s-2xl);row-gap:var(--s-m);align-items:start;padding:var(--s-2xl) 0;border-bottom:var(--rule-w) solid var(--rule);transition:background-color .15s}
.entry:hover,.entry:has(a:focus-visible){background:var(--hover)}
.entry h2{font:500 var(--body)/1.3 var(--f-display);letter-spacing:normal}
.entry h2 a{color:var(--text);text-decoration:none}
.entry h2 a::after{content:"";position:absolute;inset:0}
.entry:hover h2 a{text-decoration:underline}
.meta{margin-top:var(--s-s);font:400 var(--micro)/1.5 var(--f-figure)}
.cat{white-space:nowrap}
.what{max-width:var(--what);font-size:var(--body);line-height:1.5}
.rc{margin:0}
.entry .rc{display:contents}
.bay{display:grid;align-content:start;gap:var(--s-s)}
.bay dd{justify-self:start;margin:0;font:400 var(--figure)/1.5 var(--f-figure)}
.entry .bay dd{white-space:nowrap}
.caution dd,.harm dd{padding-bottom:var(--s-xs);border-bottom:var(--ring) dashed var(--pencil)}
.harm dd{border-bottom-style:solid;border-bottom-color:var(--text)}
.caution dd{color:var(--pencil)}
.empty{display:flex;flex-wrap:wrap;align-items:center;gap:var(--s-l) var(--s-2xl);margin-top:var(--s-2xl);padding:var(--s-2xl);background:var(--panel)}
.news{margin-top:auto;padding-block:var(--section);border-top:var(--rule-w) solid var(--edge);background:var(--menu);color:var(--menuText)}
.news .wrap{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:end;gap:var(--s-3xl) var(--s-5xl)}
.news h2{color:var(--menuText);font-size:var(--title)}
.news .kicker{color:var(--bandSoft)}
.news .sub{margin-top:var(--s-xl);color:var(--bandSoft)}
.news form{display:flex;flex-wrap:wrap;gap:var(--s-m)}
.news input{flex:1 1 var(--field-min);width:auto;min-height:var(--field-tall)}
.news .primary,.news .primary:hover{min-height:var(--field-tall);border-color:var(--menuText);background:var(--menuText);color:var(--menu)}
.news .msg{color:var(--menuText)}
.news :focus-visible{outline-color:var(--menuText)}
.msg{flex-basis:100%;font:500 var(--body)/1.3 var(--f-display);color:var(--text)}
.msg:empty{display:none}
.hp{display:none}
.prose{max-width:var(--measure);padding-top:var(--s-2xl)}
.deck+.prose{padding-top:0}
.deck+.prose>h2:first-child{margin-top:var(--s-2xl)}
.prose+section,.prose+.sheet{margin-top:var(--s-5xl)}
.prose h1{margin-block:var(--s-5xl) var(--s-2xl)}
.prose h2{margin:var(--s-5xl) 0 var(--s-xl);padding-top:var(--s-xl);border-top:var(--rule-w) solid var(--text)}
.prose p+p,.prose ul+p{margin-top:var(--s-xl)}
.prose ul{display:grid;gap:var(--s-m);padding-left:var(--s-xl)}
.prose .guides{gap:0;padding-left:0;list-style:none;counter-reset:guide;border-top:var(--rule-w) solid var(--rule)}
.guides li{counter-increment:guide;display:flex;align-items:baseline;gap:var(--s-xl);border-bottom:var(--rule-w) solid var(--rule)}
.guides li::before{content:counter(guide,decimal-leading-zero);color:var(--accent);font:400 var(--micro)/1 var(--f-figure)}
.guides a{flex:1;padding-block:var(--s-m);color:var(--text);font:500 var(--lead)/1.3 var(--f-display);text-decoration:none}
.guides a:hover{text-decoration:underline}
.guides a,.back a,.spec a,.fine a{display:inline-flex;align-items:center;min-height:var(--reach)}
.back{padding-top:var(--s-3xl);font:400 var(--small)/1.2 var(--f-body)}
.rule{margin-top:var(--s-4xl);padding:var(--s-l) 0 var(--s-l) var(--s-2xl);border-left:var(--ring) solid var(--text)}
.prose .rule h2{margin:0 0 var(--s-m);padding-top:0;border-top:0;font-size:var(--body)}
.stack{display:grid;gap:var(--s-2xl);margin-top:var(--s-3xl)}
.field{display:grid;gap:var(--s-m)}
.field input,.field select,.field textarea{letter-spacing:normal}
.actions{display:flex;flex-wrap:wrap;align-items:center;gap:var(--s-l) var(--s-2xl)}
.actions .msg{flex-basis:auto}
.tool{padding-top:var(--s-3xl)}
.tool h1{margin-top:var(--s-l);max-width:var(--column)}
.by{margin-top:var(--s-m);font:400 var(--micro)/1.5 var(--f-figure)}
.tool .lede{max-width:var(--column);margin-top:var(--s-3xl);color:var(--text)}
.check{max-width:var(--column);margin-top:var(--s-4xl)}
.check h2{margin-bottom:var(--s-2xl)}
.check .rc{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--s-2xl)}
.check .bay{gap:var(--s-l);padding-left:var(--s-xl);border-left:var(--rule-w) solid var(--rule)}
.check dd{font:500 var(--title)/1.15 var(--f-display);letter-spacing:var(--snug)}
.note{margin-top:var(--s-2xl);font-size:var(--small)}
.spec{display:grid;grid-template-columns:var(--term) minmax(0,1fr);max-width:var(--column);margin:var(--s-4xl) 0 0;border-top:var(--rule-w) solid var(--text)}
.spec dt,.spec dd{margin:0;padding-block:var(--s-xl);border-bottom:var(--rule-w) solid var(--rule)}
.spec dt{padding-right:var(--s-2xl);padding-top:var(--s-l)}
.spec dd{overflow-wrap:anywhere}
.spec dt a{color:var(--text);font:500 var(--body)/1.3 var(--f-display);letter-spacing:normal}
.fine{margin-top:var(--s-2xl);font-size:var(--small)}
.foot{padding-block:var(--s-3xl);font:400 var(--small)/1.6 var(--f-body)}
.foot p{max-width:var(--measure)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{transition:none!important;scroll-behavior:auto!important}}
@media (max-width:960px){
.cols{display:none}
.entry{grid-template-columns:minmax(0,1fr)}
.entry .rc{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--s-l);margin-top:var(--s-m)}
.entry .bay dt{position:static;width:auto;height:auto;overflow:visible;clip-path:none;white-space:normal}
.figs{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
.news .wrap{grid-template-columns:minmax(0,1fr)}
.check .rc{grid-template-columns:minmax(0,1fr)}
}
@media (max-width:560px){
.wrap{padding-inline:var(--s-xl)}
.mast nav{column-gap:var(--s-xl)}
.corners{padding:var(--s-2xl) var(--s-xl)}
.acts{flex-direction:column;gap:0}
.rc,.entry .rc{grid-template-columns:minmax(0,1fr);gap:var(--s-s)}
.entry .bay{grid-template-columns:var(--label) minmax(0,1fr);align-items:baseline;gap:var(--s-l)}
.pick{flex:1 1 100%;flex-direction:column;align-items:stretch;min-width:0}
.pick select{width:100%;min-width:0;max-width:100%}
.toggle{flex:1 1 auto}
.count{flex-basis:100%;margin-left:0}
.spec{grid-template-columns:minmax(0,1fr)}
.spec dt{padding-bottom:0;border-bottom:0}
.spec dd{padding-top:var(--s-s)}
}
"""
CSS="".join(l.strip() for l in CSS.splitlines())
HEAD=("".join(f'<link rel=modulepreload href="{s}">' for s in SCRIPTS if s!="/js/page.js")
 +"".join(f'<link rel=preload href="{n}" as=font type="font/woff2" crossorigin>' for n in ("/fonts/host-grotesk-latin-400-normal.woff2","/fonts/host-grotesk-latin-500-normal.woff2","/fonts/jetbrains-mono-latin-400-normal.woff2")))
NAV=[("/","Directory"),("/students","Students"),("/submit","Submit a tool"),("/about","About")]
# path=None is the 404 page: no canonical, no og:url, noindex, and no nav item marked current.
def page(title,desc,body,path,news=True):
    nav="".join(f'<a href="{h}"{" aria-current=page" if h==path else ""}>{t}</a>' for h,t in NAV)
    return f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name=description content="{e(desc)}">{f'<link rel=canonical href="{BASE}{path}">' if path else "<meta name=robots content=noindex>"}<meta property=og:title content="{e(title)}"><meta property=og:description content="{e(desc)}"><meta property=og:type content=website>{f'<meta property=og:url content="{BASE}{path}">' if path else ""}<meta name=theme-color content="#f6f1e8" media="(prefers-color-scheme: light)"><meta name=theme-color content="#1c1611" media="(prefers-color-scheme: dark)">{HEAD}<style>{CSS}</style></head><body><a class=skip href="#main">Skip to content</a><header class=mast><div class=wrap><a class=mark href="/">Nurse AI Tools</a><nav aria-label=Site>{nav}</nav></div></header><main id=main class=wrap>{body}</main>{NEWS if news else ""}<footer class=foot><div class=wrap><p>© 2026 Nurse AI Tools. Independent directory, not affiliated with any vendor listed. Not medical advice. Follow your facility's policies.</p></div></footer><script type=module src="/js/page.js"></script></body></html>"""
def bay(label,value): return f'<div class="bay{" "+TONE[value] if value in TONE else ""}"><dt>{label}</dt><dd>{e(value)}</dd></div>'
def plate(t): return "<dl class=rc>"+"".join(bay(l,t[k]) for l,k in BAYS)+"</dl>"
NEWS="""<section class=news aria-labelledby=news-h><div class=wrap><div><p class=kicker>The weekly note</p><h2 id=news-h>AI at the bedside</h2><p class=sub>New tools, rollouts, and what nurses are saying. One email a week. No spam.</p></div>
<form action="/api/subscribe" novalidate><label class=sr for=news-email>Email address</label><input id=news-email type=email name=email required autocomplete=email placeholder="you@example.com"><input name=hp class=hp tabindex=-1 autocomplete=off><button class=primary>Subscribe</button><p class=msg id=form-msg data-form-message role=status></p></form></div></section>"""
P_={}
rows="".join(f'<li class=entry data-card data-id="{t["slug"]}" data-category="{e(t["category"])}" data-text="{e((t["name"]+" "+t["vendor"]+" "+t["what"]).lower())}" data-traits="{" ".join(row["key"] for row in TRAITS if row["match"](t))}"><div class=head><h2><a href="/tools/{t["slug"]}">{e(t["name"])}</a></h2><p class=meta>{e(t["vendor"])} <span aria-hidden=true>·</span> <span class=cat>{e(t["category"])}</span></p></div><p class=what>{e(t["what"])}</p>{plate(t)}</li>' for t in tools)
filters=('<label class=pick>Category<select data-filter-category><option value="">All categories</option>'+"".join(f"<option>{e(c)}</option>" for c in CATS)+"</select></label>"
         +"".join(f'<label class=toggle><input type=checkbox data-filter-trait="{row["key"]}">{e(row["label"])}</label>' for row in TRAITS))
FIGS=[(sum(t["built"]=="Nurses" for t in tools),"are built for nurses",""),(sum(t["hstat"]=="Mentions HIPAA" for t in tools),"mention HIPAA on their website",""),
      (sum(t["fit"]=="Bedside/mobile workflow" for t in tools),"fit a bedside or mobile workflow",""),(sum(t["hstat"]=="Unknown" for t in tools),"do not state a HIPAA status on their homepage"," unk")]
home=f"""<section class=hero><p class=kicker>Independent directory / checked Oct 2026</p><h1>AI tools for nurses, reviewed by a nurse</h1><p class=lede>AI should run the rules in the background so nurses can run the care.</p><nav class=acts aria-label="Start here"><a href="#directory">Browse {len(tools)} tools</a><a href="/students">For nursing students</a></nav></section>
<section class=corners aria-labelledby=proof-h><span class=cb></span><h2 id=proof-h class=kicker>Of {len(tools)} tools, from public vendor information</h2><div class=figs>{"".join(f'<p class="fig{c}"><b>{v}</b><span>{k}</span></p>' for v,k,c in FIGS)}</div><p class=foot-note>Most clinical AI is built for physicians. Unknown means the vendor does not say, so we do not guess. <a href="/about">How listings work</a></p></section>
<section id=directory data-catalog data-state=idle aria-labelledby=dir-h><div class=sect><h2 id=dir-h>The directory</h2></div><div class=find><label for=q>Search tools, vendors, or tasks</label><input id=q type=search data-filter-query placeholder="flowsheet, sepsis, NCLEX" autocomplete=off></div><div class=filters>{filters}<p class=count data-catalog-count aria-live=polite>{len(tools)} tools</p></div><div class=sheet><div class=cols aria-hidden=true><span>Tool</span><span>What it does</span><span class=group>RN reality check</span><span>Built for</span><span>HIPAA status</span><span>Bedside fit</span></div><ul class=index>{rows}</ul><div class=empty data-catalog-empty hidden><p>No tools match this filter.</p><button type=button data-filter-clear>Clear filters</button></div></div></section>"""
HOME_DESC="Independent directory of AI tools for nurses: ambient documentation, handoff, clinical decision support, NCLEX prep, scheduling and patient communication."
P_["/"]=page("Nurse AI Tools: AI tools for nurses",HOME_DESC,home,"/")
for t in tools:
    b=f"""<p class=back><a href="/">Back to the directory</a></p><article class=tool><p class=kicker>{e(t["category"])}</p><h1>{e(t["name"])}</h1><p class=by>by {e(t["vendor"])}</p><p class=lede>{e(t["what"])}</p><section class="check corners" aria-labelledby=rc-h><span class=cb></span><h2 id=rc-h>RN reality check</h2>{plate(t)}<p class=note>From vendor or public info only. Unknown means we could not verify it.</p></section>
<dl class=spec><dt>Official site</dt><dd><a href="{e(t["url"])}" rel="nofollow noopener" target=_blank>{e(t["url"])}</a></dd><dt>EHR integrations</dt><dd>{e(t["ehr"])}</dd><dt>HIPAA / BAA status</dt><dd>{e(t["hipaa"])}</dd><dt>Category</dt><dd>{e(t["category"])}</dd><dt>Vendor</dt><dd>{e(t["vendor"])}</dd></dl>
<p class=fine>Listing info is compiled from the vendor's public website and may change. Vendors can <a href="/submit">submit corrections</a>.</p></article>"""
    P_["/tools/"+t["slug"]]=page(f'{t["name"]} for nurses: features, EHR integrations, HIPAA | Nurse AI Tools',f'{t["name"]} by {t["vendor"]}: {t["what"]}'[:155],b,"/tools/"+t["slug"])
sub=f"""<div class=prose><h1>Submit a tool</h1><p class=sub>Know an AI tool nurses use? Vendors welcome too. Every submission is reviewed before listing.</p>
<form class=stack action="/api/submit" novalidate><label class=field>Tool name<input name=name required autocomplete=off></label><label class=field>Official website<input name=url type=url required placeholder="https://" autocomplete=url></label><label class=field>Category<select name=category>{"".join(f"<option>{e(c)}</option>" for c in CATS)}</select></label><label class=field>Notes<textarea name=notes rows=4 placeholder="What does it do for nurses? EHR integrations? HIPAA/BAA?"></textarea></label><label class=field>Your email (optional)<input name=email type=email autocomplete=email></label><input name=hp class=hp tabindex=-1 autocomplete=off><div class=actions><button class=primary>Submit</button><p class=msg id=form-msg data-form-message role=status></p></div></form></div>"""
P_["/submit"]=page("Submit an AI tool for nurses | Nurse AI Tools","Suggest an AI tool for nurses to be reviewed and listed in the Nurse AI Tools directory.",sub,"/submit",news=False)
ab="""<div class=prose><h1>About</h1><p>Nurse AI Tools is run by a registered nurse with 14 years of critical care experience who builds with AI on the side.</p><p>Hospitals are rolling out ambient charting, AI handoffs and early-warning tools fast, and nurses are often the last to hear how they actually work on a real shift. This site aims to be the plain-spoken, nurse-first reference.</p><h2>How listings work</h2><ul><li>Facts (vendor, integrations, HIPAA/BAA statements) come from vendors' public websites and are labeled when unconfirmed.</li><li>Every tool gets an <b>RN reality check</b>: who it is built for, its HIPAA status, and whether it fits a bedside workflow. Each answer comes only from vendor or public information. If we cannot verify it, we say Unknown.</li><li>Listings are independent. Any future sponsored placements will be clearly labeled.</li></ul><p>Nothing here is medical advice. Never enter patient information into a tool your facility hasn't approved.</p></div>"""
P_["/about"]=page("About Nurse AI Tools","Nurse AI Tools is an independent, nurse-run directory of AI tools for nurses, nursing students and new grads.",ab,"/about")

BY={t["name"]:t for t in tools}
def entry(t): return f'<li class=entry><div class=head><h2><a href="/tools/{t["slug"]}">{e(t["name"])}</a></h2><p class=meta>{e(t["vendor"])} <span aria-hidden=true>·</span> <span class=cat>{e(t["category"])}</span></p></div><p class=what>{e(t["what"])}</p>{plate(t)}</li>'
def picks(names): return '<div class=sheet><div class=cols aria-hidden=true><span>Tool</span><span>What it does</span><span class=group>RN reality check</span><span>Built for</span><span>HIPAA status</span><span>Bedside fit</span></div><ul class=index>'+"".join(entry(BY[n]) for n in names)+'</ul></div>'
RULE='<p class=sub>No star ratings here. We only rate tools we have used on real shifts or in real study, and we will say so when we do. Everything below is from vendor sites, checked Oct 2026.</p>'
PHI='<section class=rule aria-labelledby=phi-h><h2 id=phi-h>One rule before any of these</h2><p>Never paste real patient details from clinical into any study or AI tool. Change names, dates, ages and rare details, or make the case up. Your school and your clinical site both have policies on this.</p></section>'
SP=[("/students/best-free-ai","Best free AI for nursing students"),("/students/ai-care-plan-tools","AI care plan tools"),("/students/nclex-ai-tutors","NCLEX AI tutors compared")]
def stu(path,title,desc,body):
    side='<p class=back><a href="/students">Back to the students hub</a></p>' if path!="/students" else ""
    body=body.replace("<section class=deck>",f'<section class=deck><p class=kicker>{"Students and new grads" if path=="/students" else "Student guide"}</p>',1)
    P_[path]=page(title+" | Nurse AI Tools",desc,side+body+(related(path) if path!="/students" else ""),path)
exec(open('landing.py').read())
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
NOT_FOUND=page("Page not found | Nurse AI Tools",HOME_DESC,'<div class=prose><h1>Page not found</h1><p><a href="/">Back to the directory</a></p></div>',None,news=False)
sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{BASE}{p}</loc><lastmod>2026-10-17</lastmod></url>" for p in P_)+"</urlset>"
json.dump(tools,open("tools.json","w"),indent=1)

TEMPLATE=open("worker.template.js").read()
SHELL=page("%%TITLE%%","%%DESC%%","%%BODY%%","%%PATH%%")
VALUES={"PAGES":json.dumps(P_),"NOT_FOUND":json.dumps(NOT_FOUND),"SITEMAP":json.dumps(sm),"SCRIPTS":json.dumps(SCRIPTS),"FONTS":json.dumps(FONTS),"SHELL":json.dumps(SHELL),"BASE":BASE}
def fill(src): return re.sub(r"__(PAGES|NOT_FOUND|SITEMAP|SCRIPTS|FONTS|SHELL|BASE)__",lambda m:VALUES[m.group(1)],src)
W=fill(TEMPLATE)
os.makedirs("dist",exist_ok=True)
open("dist/worker.js","w").write(W); print(len(tools),"tools",len(P_),"pages",len(W),"bytes")

# deploy.js is one module with no bundler: paste each module the template imports, exports removed.
IMPORTS=re.findall(r"^import \{[^}]*\} from '\.\./([\w/]+\.js)';\n",TEMPLATE,re.M)
assert IMPORTS and len(IMPORTS)==len(re.findall(r"^\s*import\b",TEMPLATE,re.M))
code=TEMPLATE; names=re.findall(r"^(?:async )?(?:function|const|let|class) (\w+)",TEMPLATE,re.M)
for path in IMPORTS:
    src=open(path).read()
    assert not re.search(r"^\s*import\b",src,re.M), path+" must not import"
    inlined=re.sub(r"^export ","",src,flags=re.M)
    assert not re.search(r"^\s*export\b",inlined,re.M), path
    names+=re.findall(r"^(?:async )?(?:function|const|let|class) (\w+)",inlined,re.M)
    code=re.sub(r"^import \{[^}]*\} from '\.\./"+re.escape(path)+"';\n",lambda m:inlined+"\n",code,count=1,flags=re.M)
dupes=sorted({n for n in names if names.count(n)>1})
assert not dupes, "inlined modules share a scope; rename "+", ".join(dupes)
D=open("deploy.js").read(); start=D.index("const code=")+len("const code=")
_,end=json.JSONDecoder().raw_decode(D,start)
open("deploy.js","w").write(D[:start]+json.dumps(fill(code))+D[end:])
