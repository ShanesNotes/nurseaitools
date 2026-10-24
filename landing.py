# Student landing pages. build.py runs this after stu() is defined and before the students hub is rendered.
# Every claim about a tool is a quote from its tools.json "what" text. The build fails if a quote is not found there.
NCLEX_AI=[t for t in tools if t["category"] in (E,K) and "NCLEX" in t["what"] and re.search(r"\bAI\b",t["what"])]
NCLEX_PLAIN=[t for t in tools if t["category"]==E and not re.search(r"\bAI\b",t["what"])]
NCLEX_FREE=[t for t in tools if t["category"] in (E,K) and "NCLEX" in t["what"] and re.search(r"\bfree\b",t["what"],re.I)]
NGN=[t for t in tools if re.search(r"\bNGN\b|Next Generation NCLEX",t["what"])]
LLMS=[t for t in tools if t["category"]==G and t["name"] in ("ChatGPT","Claude","Gemini")]
# Quotes per tool: AI feature, NGN coverage, and cost, each copied from the tool's "what" text. trial marks a trial with no free plan.
Q={
 "GoodNurse":dict(ai=["AI NCLEX tutor with 2,000+ practice questions and adaptive study plans","you can ask follow-up questions on a missed item"]),
 "NCLEXIT":dict(ai=["a 24/7 AI tutor and spoken clinical simulation"],ngn=["NGN practice questions, unfolding case studies, adaptive CAT-style mock exams"],cost=["Paid, with a 7-day free trial"],trial=True),
 "NurseSavvy":dict(ai=["per-question AI specialty tutors"],cost=["free CAT readiness exams","a free plan with a monthly allowance"]),
 "GCLEX":dict(ai=["an AI nurse tutor that knows your quiz history"],ngn=["an NGN unfolding patient simulator"],cost=["Free tier; Plus $29.99/mo; Pro with the AI tutor and AI question sets $39.99/mo (3-day trial)"]),
 "NurseReady":dict(ai=["2,000+ AI-generated questions","an AI coach that explains answers"],ngn=["all 5 NGN item types"],cost=["a free no-signup question generator","Free daily plan; full access $19.99 for 30 days or $29.99 for 60 days, one-time"]),
 "NCLEX IT (ngnsimulation)":dict(ai=["AI tutor built for the Next Generation NCLEX (NGN)","coaching across the six Clinical Judgment Measurement Model steps"],ngn=["case study, bowtie and trend items"],cost=["Free to start; Premium priced in-product"]),
 "NurseQuizAI":dict(ai=["it generates NCLEX-style quizzes","AI rationales and flashcards"],ngn=["including SATA and NGN formats"],cost=["Free plan with a daily quiz limit; paid plans raise the limits"]),
}
for n,q in Q.items():
    for k in ("ai","ngn","cost"):
        for s in q.get(k,[]): assert s in BY[n]["what"],f"{n}: {s!r} is not in its tools.json entry"
def said(t,k):
    q=Q.get(t["name"])
    if q is None: return f'<q>{e(t["what"])}</q>' if k=="ai" else ""
    return "; ".join(f"<q>{e(s)}</q>" for s in q.get(k,[]))
LABEL={"ai":"AI","ngn":"NGN","cost":"Free or paid"}
def compare(ts,keys):
    rows=""
    for t in ts:
        lines=[f'<b>{LABEL[k]}:</b> {said(t,k) or "Not stated in the directory entry."}' for k in keys]
        rows+=f'<dt><a href="/tools/{t["slug"]}">{e(t["name"])}</a></dt><dd>{"<br>".join(lines)}</dd>'
    return f"<dl class=spec>{rows}</dl>"
def names(ts): return ", ".join(f'<a href="/tools/{t["slug"]}">{e(t["name"])}</a>' for t in ts)
GUIDES=[("/students/best-ai-nclex-prep","Best AI NCLEX prep tools"),("/students/free-nclex-prep","Free NCLEX prep tools"),
        ("/students/ngn-practice-tools","NGN practice tools"),("/students/chatgpt-for-nclex","Using ChatGPT for NCLEX prep safely")]
SP+=GUIDES
def related(path):
    links=[(p,t) for p,t in SP if p!=path]
    return '<div class=prose><h2>Related guides</h2><ul class=guides>'+"".join(f'<li><a href="{p}">{t}</a></li>' for p,t in links)+f'<li><a href="/">Browse all {len(tools)} tools in the directory</a></li></ul></div>'
SOURCE=f'<p class=fine>Every quote on this page is from the tool&#39;s entry in the Nurse AI Tools directory, which is compiled from vendor sites in Oct 2026. Prices and plans change, so check the vendor site before you pay.</p>'

stu("/students/best-ai-nclex-prep","Best AI NCLEX prep tools (2026)",
 f"{len(NCLEX_AI)} NCLEX prep tools with an AI tutor, AI questions or AI rationales, compared from their directory entries: AI features, NGN coverage and free plans.",
 f'<section class=deck><h1>Best AI NCLEX prep tools</h1><p class=lede>{len(NCLEX_AI)} tools in the directory pair NCLEX prep with an AI feature. Here is what each entry says it does, side by side.</p>{RULE}</section>'
 f'<div class=prose><h2>Side by side</h2><p>Each line quotes the directory entry. If an entry does not mention something, we say so instead of guessing.</p>{compare(NCLEX_AI,("ai","ngn","cost"))}'
 f'<h2>Established question banks</h2><p>These are in the directory too. Their entries do not mention an AI feature: {names(NCLEX_PLAIN)}.</p>'
 f'<h2>How to choose</h2><ul><li>Want to ask why you missed a question? Look for a tutor that takes follow-up questions.</li><li>Testing soon? Check that the tool covers NGN items. See <a href="/students/ngn-practice-tools">NGN practice tools</a>.</li><li>On a budget? See <a href="/students/free-nclex-prep">free NCLEX prep tools</a>.</li><li>AI can be confidently wrong. If an explanation surprises you, check it against your textbook or a second question bank.</li></ul>{PHI}</div>'
 +picks([t["name"] for t in NCLEX_AI])+SOURCE)

stu("/students/free-nclex-prep","Free NCLEX prep tools with AI (2026)",
 "NCLEX prep tools whose directory entry lists a free plan, free tier or free trial, with the exact plan wording and price from each entry.",
 f'<section class=deck><h1>Free NCLEX prep tools</h1><p class=lede>{len(NCLEX_FREE)} NCLEX tools in the directory mention a free option. Some are a real free plan with limits. Some are a short trial.</p>{RULE}</section>'
 f'<div class=prose><h2>Free plan or free tier</h2>{compare([t for t in NCLEX_FREE if not Q.get(t["name"],{}).get("trial")],("cost","ai"))}'
 +(f'<h2>Free trial only</h2>{compare([t for t in NCLEX_FREE if Q.get(t["name"],{}).get("trial")],("cost","ai"))}' if any(Q.get(t["name"],{}).get("trial") for t in NCLEX_FREE) else "")
 +f'<h2>Make a free plan go further</h2><ul><li>Use the daily or monthly allowance every day rather than in one long session.</li><li>Read the rationale for every question, including the ones you got right.</li><li>For general study tools with a free option, see <a href="/students/best-free-ai">best free AI for nursing students</a>.</li></ul>{PHI}</div>'
 +picks([t["name"] for t in NCLEX_FREE])+SOURCE)

stu("/students/ngn-practice-tools","NGN practice tools: AI for the Next Generation NCLEX",
 "AI study tools whose directory entry mentions Next Generation NCLEX (NGN) items such as case studies, bowtie and SATA, compared from each entry.",
 f'<section class=deck><h1>NGN practice tools</h1><p class=lede>The Next Generation NCLEX tests clinical judgment with case studies and new item types. {len(NGN)} tools in the directory say they cover NGN.</p>{RULE}</section>'
 f'<div class=prose><h2>What each entry says about NGN</h2>{compare(NGN,("ngn","ai","cost"))}'
 f'<h2>Practice NGN well</h2><ul><li>Work whole case studies, not single items. In an NGN case study, every item follows the same patient.</li><li>After each case, say out loud which cue you noticed first and why. That is the clinical judgment NGN items are written to test.</li><li>Use made-up patients. Never rebuild a case from a patient you cared for in clinical.</li></ul>{PHI}</div>'
 +picks([t["name"] for t in NGN])+SOURCE)

P1='Here is an NCLEX-style practice question and my answer. Explain why each option is right or wrong, then ask me one follow-up question.'
P2='Quiz me on heart failure medications with 5 NCLEX-style questions. Ask one at a time and wait for my answer before you give the rationale.'
P3='Explain the difference between these two nursing concepts in plain words, then give me a made-up patient example.'
stu("/students/chatgpt-for-nclex","Using ChatGPT for NCLEX prep safely",
 "How nursing students can use ChatGPT, Claude or Gemini for NCLEX study without patient information, plus NCLEX tools with an AI tutor built in.",
 f'<section class=deck><h1>Using ChatGPT for NCLEX prep safely</h1><p class=lede>A general chatbot can explain a concept three different ways and quiz you on your own notes. It is a study partner, not a source, and it never sees a real patient.</p>{RULE}</section>'
 f'<div class=prose><h2>What the directory says</h2>{"".join(f"""<dl class=spec><dt><a href="/tools/{t["slug"]}">{e(t["name"])}</a></dt><dd><q>{e(t["what"])}</q><br><b>Patient information:</b> <q>{e(t["hipaa"])}</q></dd></dl>""" for t in LLMS)}'
 f'<h2>Rules for study use</h2><ul><li>Study only. Paste your own notes or a practice question, never anything from a chart, a shift or a clinical rotation.</li><li>Check every drug dose, lab value and priority answer against your drug guide, textbook or question bank. A chatbot can be confidently wrong.</li><li>Use it to quiz you and explain, not to write graded work. Ask your program what it allows.</li></ul>{PHI}'
 f'<h2>Prompts that keep it on study</h2><ul><li><q>{e(P1)}</q></li><li><q>{e(P2)}</q></li><li><q>{e(P3)}</q></li></ul>'
 f'<h2>Want a tutor built for NCLEX?</h2><p>These directory entries describe an AI tutor or coach inside an NCLEX prep tool.</p>{compare([t for t in NCLEX_AI if "tutor" in t["what"].lower() or "coach" in t["what"].lower()],("ai",))}'
 f'<p>To study from your own lecture notes: <a href="/tools/notebooklm">NotebookLM</a> is an <q>{e(BY["NotebookLM"]["what"])}</q> <a href="/tools/nursequizai">NurseQuizAI</a> says <q>{e(Q["NurseQuizAI"]["ai"][0])}</q> from slides or notes you upload.</p></div>'
 +picks([t["name"] for t in LLMS])+SOURCE)
