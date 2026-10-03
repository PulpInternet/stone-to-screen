import json, re, html as H
SRC = '/home/claude/v3/part1_rewritten.html'
OUT = '/mnt/user-data/outputs/From_Stone_to_Screen_v3.html'
t = open(SRC, encoding='utf8').read()
D = json.load(open('/home/claude/story/story_data.json'))
e = H.escape

def bars(rows, cap, maxv=None, fmt=lambda v: f"{v:.0%}"):
    mx = maxv or max(r[1] for r in rows)
    out = []
    for name, v, sub, *rest in rows:
        cls = rest[0] if rest else ''
        out.append(f'<div class="vrow"><div class="vh"><span class="vn">{e(name)}{f"<span class=vs>{e(sub)}</span>" if sub else ""}</span><span class="vv">{e(fmt(v))}</span></div>'
                   f'<div class="vbar" role="img" aria-label="{e(name)}: {e(fmt(v))}"><i class="{cls}" style="width:{max(0.8, v / mx * 100):.1f}%"></i></div></div>')
    return f'<figure class="viz">{"".join(out)}<figcaption class="vcap">{e(cap)}</figcaption></figure>'

def chips(key, labels):
    return '<div class="chips" role="group" aria-label="Details">' + ''.join(f'<button class="chip" data-ch="{key}" data-f="{i}" type="button">{e(l)}</button>' for i, l in enumerate(labels)) + '</div>'

def chapter(key, idx, era, date, place, title, viz, body, chip_labels, card=False):
    return (f'<article class="beat{" card" if card else ""}" id="{key}" data-i="{idx}">\n<header><p class="meta"><span class="date">{e(date)}</span>'
            f'<span class="sep" aria-hidden="true"></span><span>{e(place)}</span></p><h3>{e(title)}</h3></header>\n{viz}\n'
            + ''.join(f'<p class="body">{e(p)}</p>' for p in body) + '\n' + chips(key, chip_labels) + '\n</article>')

# ---------- data for the figures ----------
hist = [h for h in D['hist']]
shape_rows = [(f"{h['n']:,} requests", h['s99'], None) for h in hist]
real = D['sets']['real held out']
th = D['thinking']; TN = [("D", "Facts"), ("P", "Steps"), ("C", "If-then"), ("PL", "Plan"), ("M", "Monitor"), ("E", "Evaluate"), ("S", "Social")]
think_rows = []
for k, n in TN:
    think_rows.append((f"{n}, requests", th['requests'].get(k, 0), None))
    think_rows.append((f"{n}, meeting turns", th['meetings'].get(k, 0), None, 'm'))

KEY0 = 34
P2 = []
P2.append(chapter("p2shapes", KEY0, "Reading", "2026", "11,508 requests", "A few dozen shapes",
    bars(shape_rows, "Shapes needed to cover 99% of requests as the collection grew.", maxv=60, fmt=lambda v: f"{v} shapes"),
    ["The alphabet compressed hundreds of signs into about twenty-two letters. Requests compress too. We collected 11,508 requests from 44 public collections and from our own simulations, from voice commands to parliamentary hearings, and read each one for its shape: the kind of statement it is and the main thing it asks for.",
     "Forty-seven shapes cover 99% of them. As the collection grew from fewer than 2,000 requests to more than 11,500, the number needed for 99% rose slowly and then held. A small, stable set means a small memory serves almost everything, and rules that cost almost nothing to run can read most requests."],
    ["What a shape is", "Where the requests come from", "How slowly shapes grow"]))
P2.append(chapter("p2rules", KEY0 + 1, "Reading", "2026", "About 9 milliseconds", "Rules first",
    bars([("Rules alone", real['rules alone'], "180 real requests"), ("With the second layer", real['round 9 layer'], "Same 180 requests")],
         "Share of held-out requests read correctly before any model was called. The correct readings were written down before testing.", maxv=1),
    ["The Linotype replaced the compositor's hand with a keyboard and cast whole lines at once. Our engine does something similar for reading. A linguistic parser reads each request into a structured frame: what kind of statement it is, what it asks for, what it refers to, and what form the answer should take.",
     "A second small layer reads the turn before it in a conversation and recognizes common tasks. Only what neither can settle goes to a large AI model, and the model receives a short outline with the gap marked, not the whole request."],
    ["Written down first", "Reading the turn before", "Where it falls short"]))
P2.append(chapter("p2thinking", KEY0 + 2, "Reading", "2026", "450 labeled examples", "Kinds of thinking",
    bars(think_rows, "Share of 330 requests and 120 meeting turns, labeled by hand before any detector was built. Dark bars are requests; gray bars are meeting turns.", maxv=0.6),
    ["A request asks for more than an answer. It asks for a kind of thinking. Some ask for facts, some for steps where order matters, and some for an if-then judgment. Others plan, check progress, or evaluate how something went. Deciding what to look up, what to reuse, and what needs fresh judgment is how people manage their own memory, and a system can do the same.",
     "Most requests ask for facts and steps. More than half of meeting turns plan, monitor, evaluate, or weigh options, which is why meetings are the hardest material we read."],
    ["Knowledge and regulation", "Why it matters for cost", "How well rules detect it"]))
dots = ''.join('<i class="e"></i>' if i in (5, 13, 22, 30, 39, 44) else '<i></i>' for i in range(48))
P2.append(chapter("p2measure", KEY0 + 3, "Measuring", "2026", "48 anchored scales", "How a message moves",
    f'<figure class="viz"><div class="dots" role="img" aria-label="A grid of 48 scales, eight channels by six dimensions, with six scales left empty">{dots}</div>'
    '<figcaption class="vcap">48 scales: eight channels across six dimensions. In this illustrative message, six circles are empty: abstentions, scores left blank for lack of evidence.</figcaption></figure>',
    ["Part I is a history of how messages travel. Pulp also studies what happens when they arrive. Our measurement core scores a message on 48 anchored scales, eight channels across six dimensions, each running from minus one to plus one.",
     "Rhetorical mass describes how much attention a message asks of the person receiving it. Persuasive force describes how hard it pushes toward its purpose. Resonance describes how well it fits a particular listener at a particular moment.",
     "When there is not enough evidence to score something, the score stays empty. It is never set to zero, because zero would claim a measurement that was not made."],
    ["Anchored scales", "Empty, not zero", "Where this research stands"], card=True))
parts = ''.join(f'<div><b>{n}</b><span>{d}</span></div>' for n, d in (("Speaker", "who says it"), ("Listener", "who hears it"), ("Information", "what is said"), ("Medium", "how it travels"), ("Purpose", "what it is for")))
P2.append(chapter("p2thinkwell", KEY0 + 4, "Making", "2026", "Thinkwell", "Every conversation, read well",
    f'<figure class="viz"><div class="parts">{parts}</div><figcaption class="vcap">The five parts every conversation is modeled with.</figcaption></figure>',
    ["Thinkwell, Pulp's first product, applies this work to conversations people already have, from a meeting to a public engagement campaign. It points to the exact words where a claim, a fallacy, or a bias appears. It never grades the person speaking, and people set their own goals.",
     "Screen moments captured during a recording stay on the device. Sharing one into Thinkwell's AI is a separate choice, made moment by moment."],
    ["Your exact words", "Kept versus shared", "Every scale of conversation"]))
P2.append(chapter("p2dojo", KEY0 + 5, "Making", "2026", "typodojo", "Letters by hand, again",
    '<figure class="viz"><div class="prov"><span>Drawn by hand</span><span>AI-assisted</span><span>Uploaded</span></div><figcaption class="vcap">The three provenance labels. Every font page on typodojo carries one.</figcaption></figure>',
    ["typodojo, a Pulp special project, is a dojo for learning to draw letters and a marketplace for the fonts people make. Every font page says how the font was made: drawn by hand, AI-assisted, or uploaded. AI-assisted fonts need real human editing before they can be published, and typodojo's AI will never be trained on the fonts its members make.",
     "Its feed is one daily edition of cited quotes and claims about the craft, deliberately slower than social media. Members comment only after drawing a reaction by hand."],
    ["Provenance labels", "Members' fonts stay theirs", "Type that moves"]))
kwh = (26.6, 16.6, 6.3)
P2.append(chapter("p2energy", KEY0 + 6, "Measuring", "2026", "Per million requests", "Less compute, on the record",
    bars([("A model reads everything", kwh[0], "About 22 hours of an average US home's electricity"), ("Rules first, outside knowledge needed", kwh[1], "About 13 hours"), ("Rules first, structure only", kwh[2], "About 5 hours")],
         "Electricity to understand one million requests with Claude Sonnet 5.5. An average US home uses about 29.6 kWh a day.", fmt=lambda v: f"{v} kWh"),
    ["Every request a large model reads uses electricity in a data center, and that use grows with the amount of text the model reads and writes. Reading with rules first cuts the work.",
     "Averaged across six kinds of traffic, it saves about 40% of a model's work when outside knowledge is needed and about 85% when only the structure of a request is. Across 2,000 different traffic mixes, those figures stayed between 38% and 42%, and between 78% and 90%.",
     "These figures are calculated from measured token counts and published energy research, not metered in a live deployment. They cover understanding a request, not writing the answer."],
    ["Where the model runs", "A home for comparison", "Every model we checked"], card=True))
P2.append(chapter("p2live", KEY0 + 7, "Now", "2026", "Your screen", "Watch a request get read",
    '<div id="reader"><div class="exl" role="group" aria-label="Example requests"></div><div class="exr" aria-live="polite"></div></div>',
    ["Part I has a glyph that answers as you move across it. Part II ends the same way, and shows what each reading costs. Pick a request. Each one was read by the engine. Where the correct reading was written down before testing, the result is marked as a match or a miss."],
    ["Real and simulated", "What stays the same"]))

FACTS2 = {
 "p2shapes": [("What a shape is", "A shape is the kind of statement plus the main operation it asks for: for example, a question asking to look something up, or a request asking to schedule something. Different wordings of the same need share a shape."),
              ("Where the requests come from", "The real requests come from 44 public research collections, including voice-assistant commands, task conversations, search queries, financial and table questions, and transcripts of parliamentary committees and working meetings. 1,044 simulated requests, written by Pulp in the voices of its customers, are labeled and never counted as real."),
              ("How slowly shapes grow", "The number of distinct shapes grows with the size of the collection raised to the power 0.22. Distinct wordings grow almost one for one, at the power 0.91. That gap is why a fixed set of rules can keep up.")],
 "p2rules": [("Written down first", "Before each round of testing, we saved our predictions to a file with a timestamp and a fingerprint, then labeled the data, then ran the tests. Results are compared against those records, including the predictions that failed."),
             ("Reading the turn before", "A reply like \u201cthe one on Main Street\u201d makes no sense alone. Reading the assistant's previous question raised accuracy on dialog turns by 15 to 26 points in our tests."),
             ("Where it falls short", "Long, multi-speaker turns from meetings and hearings are hard for cheap layers. Rules read 31% of meeting turns correctly, and those turns still need a model most of the time.")],
 "p2thinking": [("Knowledge and regulation", "The study of metacognition divides thinking about thinking into knowledge (facts, procedures, and conditions) and regulation (planning, monitoring, and evaluating). We use that division as a data structure: facts, ordered steps, and if-then rules."),
                ("Why it matters for cost", "Facts can often be answered from a lookup, and steps can reuse a template. In our tests those two were the largest sources of savings."),
                ("How well rules detect it", "Rules identified the kind of thinking 76% of the time on 120 fresh requests. On meeting turns they managed 33%, close to guessing the most common type. We publish both.")],
 "p2measure": [("Anchored scales", "Each scale has written descriptions at fixed points and moves in steps of 0.05, so two people scoring the same message have the same reference points."),
               ("Empty, not zero", "A missing score and a zero score mean different things. Zero says the quality is absent; empty says it could not be judged. Keeping them apart is how the system says when it does not know."),
               ("Where this research stands", "These measures are defined and in use. Testing whether they predict what people actually do afterward is the next body of research, and we will publish it the same way.")],
 "p2thinkwell": [("Your exact words", "Thinkwell shows the words that triggered a finding, so a person can judge it for themselves. It does not score the speaker."),
                 ("Kept versus shared", "Keeping and sharing are separate decisions. Captures stay on the device; each one is shared only if the person chooses."),
                 ("Every scale of conversation", "The same tools serve one person reflecting, two people talking, one speaking to many, and many speaking with many.")],
 "p2dojo": [("Provenance labels", "Readers and buyers can see how every font was made. A hand-drawn font made freehand also carries a seal."),
            ("Members' fonts stay theirs", "typodojo's AI is never trained on the fonts its members make. A Pro tier, coming soon, adds watermarks that help makers find unlicensed use of their fonts."),
            ("Type that moves", "typodojo also lets people design text animation, continuing where Part I ends. In typodojo's words: making words that move people sometimes means making words move themselves.")],
 "p2energy": [("Where the model runs", "The same work in a data center in Oregon emits 72% more carbon than in Texas, and its power plants use about ten times the water. Texas uses less water, but 59% of its data centers sit in areas of high water stress."),
              ("A home for comparison", "An average US home uses about 10,791 kWh of electricity a year, about 29.6 kWh a day, according to the US Energy Information Administration."),
              ("Every model we checked", "The saving comes from sending fewer tokens to the model, not from one model's efficiency, so the share saved holds on every model we checked.")],
 "p2live": [("Real and simulated", "Requests marked simulated were written by Pulp in the voices of its customers. They are labeled as simulated and never counted as real."),
            ("What stays the same", "Part I closes on a job that never changed: keep what matters, spend only what it takes, and keep honest books. Part II applies the same job to machines that read.")]}
INNOV2 = [("Shapes of asking", "Requests, like letters, fall into a small reusable set. Recognizing the shape of a request is the first step to understanding it without a large model."),
          ("Understanding before compute", "Reading a request with inexpensive rules first, and sending a model only the part they cannot settle."),
          ("Thinking as data", "Typing each request by the kind of thinking it calls for, so the system knows what to look up, what to reuse, and what needs judgment."),
          ("Persuasion as measurement", "Scoring how a message moves its receiver on defined, anchored scales, with missing evidence recorded as empty rather than zero."),
          ("Conversation as a measured object", "Treating a conversation as five parts that can be read and checked, while the people in it keep control of what is shared."),
          ("Provenance for letterforms", "Every font labeled by how it was made, so craft, assistance, and upload are never confused."),
          ("A measured footprint", "Electricity per request, calculated and published, with the method stated."),
          ("Reading you can check", "Results shown alongside the readings that were written down before testing, misses included.")]
P2KEYS = ["p2shapes", "p2rules", "p2thinking", "p2measure", "p2thinkwell", "p2dojo", "p2energy", "p2live"]
P2ERAS = None
P2TITLES = ["A few dozen shapes", "Rules first", "Kinds of thinking", "How a message moves", "Every conversation, read well", "Letters by hand, again", "Less compute, on the record", "Watch a request get read"]

def part(num, pid, kind, title, epi, beats_html):
    head = f'<section class="part {kind}" id="{pid}"><header class="phead"><p class="pnum">Chapter {num}</p><h2>{e(title)}</h2><p class="epi">{e(epi)}</p></header>'
    if kind == 'horz':
        return (head + f'<div class="striprow"><div class="strip" tabindex="0" aria-label="{e(title)}, scroll sideways">' + ''.join(beats_html) + '</div></div>'
                '<div class="snav"><button class="sbtn prev" type="button" aria-label="Previous">&#8592;</button><span class="shint">Scroll sideways</span><button class="sbtn next" type="button" aria-label="Next">&#8594;</button></div></section>')
    return head + ''.join(beats_html) + '</section>'
by = dict(zip(["p2shapes", "p2rules", "p2thinking", "p2measure", "p2thinkwell", "p2dojo", "p2energy", "p2live"], P2))
ORDER = ["p2shapes", "p2rules", "p2thinking", "p2measure", "p2energy", "p2thinkwell", "p2dojo", "p2live"]
CH = [(11, "p2part11", "vert", "Reading", "What can be compressed, and what must be kept.", ORDER[0:3]),
      (12, "p2part12", "horz", "Measuring", "What a message asks of people, and what reading it costs.", ORDER[3:5]),
      (13, "p2part13", "vert", "Making", "Tools that keep people in charge of what is kept and shared.", ORDER[5:7]),
      (14, "p2part14", "vert", "Read one yourself", "Pick a request and see what it takes to read it.", ORDER[7:8])]
P2PARTS = [{"t": c[3], "n": len(c[5])} for c in CH]
divider = ('<section class="p2div" id="partII" aria-labelledby="p2h">\n<p class="kicker">Part II</p>\n<h2 id="p2h">What to keep, what to spend</h2>\n'
  '<p class="lede">Part I ends with machines that hold a memory of almost everything and spend energy every time they use it. Part II is about doing that well: deciding what a machine must remember, what it can compress, and what it needs to spend. '
  'It comes from Pulp Corporation, established 2026 in Brooklyn, New York, which builds tools for reading language well and studies how messages move the people who receive them.</p>\n'
  '<p class="sub">Four chapters and eight moments on the crafts we work on, then a record of how we check our own claims. Every number comes from our own tests.</p>\n</section>')

# ---------- proof section ----------
cnt = {k: sum(1 for p in D['pred'] if p[3] == k) for k in ("Met", "Partly met", "Not met")}
proof = [
 ("Measured", "Show our work", "Thinkwell: no gimmicks. Pulp: quality.", f"We wrote down {len(D['pred'])} predictions before testing them across five rounds. {cnt['Met']} were met, {cnt['Partly met']} partly met, and {cnt['Not met']} were not. All of them are published, including the misses."),
 ("Measured", "Say when we do not know", "Thinkwell: no gimmicks.", "Scores without evidence stay empty, never zero. When we found errors in our own published claims, we corrected them in the open: a statistic that partly reflected our own routing rule, an overstated count of test examples, duplicate simulations that were removed before rerunning everything, and a speed claim corrected to the measured figure."),
 ("Measured", "Less compute, on the record", "Thinkwell: sustainability. Pulp: value.", "Reading with rules first saves about 40% of a model's work when outside knowledge is needed and about 85% when only structure is. Calculated from measured token counts, not metered."),
 ("Measured", "Efficiency", "Thinkwell: efficiency.", f"Rules and the second layer read a request in about 9 milliseconds. They resolve {real['round 9 layer']:.0%} of real requests correctly before any model is called."),
 ("Measured", "Critical thinking", "Thinkwell and Pulp: critical thinking.", "Rules sort claims into fact, value, and policy 74% of the time on 330 held-out requests, against 62% for always guessing fact. They identify the kind of thinking a request needs 76% of the time on fresh requests."),
 ("Measured", "Data literacy", "Pulp: data literacy and misinformation.", "Every request is checked for how many and what kind of sources it needs. In testing, claims about value were sent to crowd sources 5 of 15 times against 6 of 315 for other claims, and government-relations requests needed several sources 50% of the time against 11% for the rest."),
 ("Measured", "Reliability", "Pulp: reliability. typodojo: updates that never break existing accounts.", "Three rounds of research were rebuilt from public files with one script each, and every output matched its recorded fingerprint exactly. typodojo runs a test harness that every product update must pass before it reaches existing accounts."),
 ("In the product", "Consent and provenance", "Thinkwell: consent. typodojo: provenance.", "Thinkwell keeps screen moments on the device and asks before sharing each one. typodojo labels every font by how it was made."),
 ("Promised", "Members' work stays theirs", "typodojo.", "typodojo's AI will never be trained on the fonts its members make. It is listed here as a promise because a promise is what it is."),
 ("Promised", "Human to human", "Pulp: engagement at every scale.", "typodojo comments open only after a hand-drawn reaction. Thinkwell campaigns let organizations require verified participation, so the responses come from people."),
]
open_items = ["Whether our measures predict what people actually do afterward. That is the next body of research.",
              "Agreement between annotators. One person wrote the expected readings; a second annotator is labeling a sample so agreement can be measured.",
              "Metered energy. Our electricity figures are calculated, not read from a meter in a live product.",
              "Accessibility. Thinkwell has not yet had an accessibility audit, so we say accessible by design, not compliant.",
              "Meetings. Rules read 31% of meeting turns correctly. Long, multi-speaker discussion still needs a model."]
proof_html = ('<section class="proof" id="proof" aria-labelledby="proofh"><div class="inner">\n<p class="kicker">Part II, the record</p>\n<h2 id="proofh">How we check ourselves</h2>\n'
  '<p class="pintro">The first writing in Part I was a ledger kept by clerks in Uruk. This is ours. Our sites say what we stand for. Each commitment below is paired with what we did about it and marked as measured, in the product, or promised. A promise is listed as a promise.</p>\n'
  + ''.join(f'<div class="pr"><p class="st">{e(s)}</p><h3>{e(h)}</h3><p>{e(d)}</p><p class="where">{e(w)}</p></div>' for s, h, w, d in proof)
  + '<h3 class="oh">What we have not proved yet</h3><ul class="open">' + ''.join(f'<li>{e(x)}</li>' for x in open_items) + '</ul>\n'
  '<p class="pnote">The full research report, with its data and code, is available from Pulp.</p>\n</div></section>')

# ---------- assemble ----------
coda_end = '</section>\n</main>'
assert t.count(coda_end) == 1 and 'id="coda"' in t
# reorder P2 html to ORDER and fix data-i to match registration order
p2map = {}
for i, k in enumerate(ORDER):
    p2map[k] = re.sub(r'data-i="\d+"', f'data-i="{KEY0 + i}"', by[k], count=1)
    if k in ("p2measure", "p2energy") and 'beat card' not in p2map[k]: raise SystemExit('card flag missing')
chapters_html = ''.join(part(n, pid, kind, title, epi, [p2map[k] for k in keys]) for n, pid, kind, title, epi, keys in CH)
t = t.replace(coda_end, '</section>\n' + divider + '\n' + chapters_html + '\n</main>', 1)
endnote = '<section class="endnote">'
assert t.count(endnote) == 1
t = t.replace('</main>\n</div>\n' + endnote, '</main>\n</div>\n' + proof_html + '\n' + endnote, 1)
assert proof_html in t
assert t.count('aria-valuemax="34"') == 1 and t.count('<span id="tnum">01 / 34</span>') == 1
t = t.replace('aria-valuemax="34"', 'aria-valuemax="42"', 1).replace('<span id="tnum">01 / 34</span>', '<span id="tnum">01 / 42</span>', 1)
assert t.count('<p class="sub">Ten chapters, 34 moments.') == 1
t = t.replace('<p class="sub">Ten chapters, 34 moments.', '<p class="sub">Ten chapters and 34 moments, then a Part II from Pulp.', 1)
t = t.replace('<footer>From Stone to Screen. Draft for review, October 2026.</footer>', '<footer>From Stone to Screen, with Part II by Pulp Corporation, Brooklyn, New York. Draft for review, October 2026.</footer>', 1)
# Part I fixes: strip arrows to the 44 px tap minimum; stale comment
assert '.sbtn{font:inherit; width:40px; height:36px;' in t
t = t.replace('.sbtn{font:inherit; width:40px; height:36px;', '.sbtn{font:inherit; width:44px; height:44px;', 1)
# chips keep their look; their tap area extends invisibly to 45 px tall
assert '.chip{font:inherit;' in t
t = t.replace('.chip{font:inherit;', '.chip{position:relative; font:inherit;', 1)
t = t.replace('/* Pulp Mode system v1. Nine chapters alternating', '/* Pulp Mode system v1. Ten chapters alternating', 1)

css = r'''
.chip::after{content:""; position:absolute; left:0; right:0; top:-5px; bottom:-5px}
/* Part II */
.p2div{padding-block:14vh 4vh; border-top:1px solid var(--line); margin-top:6vh}
.p2div h2{font-size:clamp(2.2rem,6.4vw,3.9rem); line-height:1.04; letter-spacing:-0.02em; font-weight:800; margin:0 0 20px; text-wrap:balance}
.p2div .lede{font-size:1.05rem; max-width:34rem; margin:0 0 10px}
.p2div .sub{color:var(--mut); font-size:.85rem; margin:0}
.viz{margin:18px 0 14px; padding:14px 0; border-top:1px solid var(--line); border-bottom:1px solid var(--line)}
.vrow{padding:7px 0}
.vh{display:grid; grid-template-columns:minmax(0,1fr) auto; gap:2px 14px; align-items:start; font-size:.86rem}
.vn{font-weight:600}
.vs{display:block; color:var(--mut); font-size:.78rem; font-weight:400}
.vv{font-variant-numeric:tabular-nums; white-space:nowrap}
.vbar{height:10px; background:var(--line); position:relative; margin-top:5px}
.vbar i{position:absolute; left:0; top:0; bottom:0; background:var(--fg)}
.vbar i.m{background:var(--mut)}
.vcap{font-size:.78rem; color:var(--mut); margin:10px 0 0; line-height:1.45}
.dots{display:grid; grid-template-columns:repeat(8,minmax(0,1fr)); gap:10px; max-width:340px}
.dots i{display:block; aspect-ratio:1/1; border-radius:50%; background:var(--fg)}
.dots i.e{background:transparent; border:1.5px solid var(--fg)}
.parts{display:grid; grid-template-columns:repeat(auto-fit,minmax(112px,1fr)); gap:8px}
.parts div{border:1px solid var(--line); padding:10px; font-size:.84rem}
.parts b{display:block}
.parts span{color:var(--mut); font-size:.78rem}
.prov{display:flex; flex-wrap:wrap; gap:10px}
.prov span{border:1.5px solid var(--fg); border-radius:999px; padding:6px 14px; font-weight:600; font-size:.85rem}
.exl{display:flex; flex-wrap:wrap; gap:8px; margin:14px 0 16px}
.ex{font:inherit; font-size:.82rem; min-height:44px; padding:8px 14px; border:1px solid var(--fg); background:var(--bg); color:var(--fg); border-radius:999px; cursor:pointer; opacity:.7; transition:opacity .12s ease}
.ex[aria-pressed="true"]{opacity:1; background:var(--btn-bg); color:var(--btn-fg)}
@media (hover:hover) and (pointer:fine){ .ex:hover{opacity:1} }
.ex:focus-visible{outline:2px solid var(--fg); outline-offset:2px}
.exr{border-top:2px solid var(--fg); padding-top:12px}
.exr .q{font-size:1.15rem; font-weight:600; margin:0 0 4px; overflow-wrap:anywhere}
.exr .src{font-size:.78rem; color:var(--mut); margin:0 0 10px}
.exr .prev{font-size:.82rem; color:var(--mut); margin:0 0 10px}
.exr dl{display:grid; grid-template-columns:minmax(110px,36%) minmax(0,1fr); margin:0}
.exr dt,.exr dd{margin:0; padding:8px 0; border-bottom:1px solid var(--line); font-size:.86rem}
.exr dt{color:var(--mut); padding-right:12px}
.proof{background:var(--band); margin-inline:-16px; padding:56px 16px 40px}
.proof .inner{max-width:680px; margin:0 auto}
.proof h2{font-size:clamp(1.8rem,4.6vw,2.6rem); line-height:1.08; font-weight:800; margin:0 0 12px}
.pintro{margin:0 0 18px; max-width:36rem}
.pr{padding:14px 0; border-top:1px solid var(--line)}
.pr .st{font-size:.7rem; text-transform:uppercase; letter-spacing:.11em; font-weight:600; color:var(--mut); margin:0}
.pr h3{font-size:1.02rem; margin:2px 0 4px}
.pr p{margin:0; font-size:.92rem}
.pr .where{color:var(--mut); font-size:.78rem; margin-top:4px}
.oh{font-size:1.1rem; margin:26px 0 8px}
.open{margin:0; padding-left:18px; font-size:.92rem}
.open li{margin-bottom:6px}
.pnote{color:var(--mut); font-size:.82rem; margin:18px 0 0}
@media (max-width:560px){ .exr dl{grid-template-columns:1fr} .exr dt{border-bottom:0; padding-bottom:0} .exr dd{padding-top:2px} .p2div{padding-block:10vh 3vh} }
'''
t = t.replace('html{scroll-behavior:smooth}\n</style>', 'html{scroll-behavior:smooth}\n' + css + '</style>', 1)
assert css in t

js_arrays = ('\n/* Part II registration */\n'
  + ''.join(f'FACTS[{json.dumps(k)}] = {json.dumps([{"t": a, "d": b} for a, b in v])};\n' for k, v in FACTS2.items())
  + f'KEYS = KEYS.concat({json.dumps(ORDER)});\nTITLES = TITLES.concat({json.dumps([dict(zip(P2KEYS, P2TITLES))[k] for k in ORDER])});\n'
  + f'DATES = DATES.concat({json.dumps(["2026"] * 8)});\nPARTS = PARTS.concat({json.dumps(P2PARTS)});\n'
  + f'INNOV = INNOV.concat({json.dumps([dict(zip(P2KEYS, [{"t": a, "d": b} for a, b in INNOV2]))[k] for k in ORDER])});\n')
t = t.replace('var N = KEYS.length;', js_arrays + 'var N = KEYS.length;', 1)
assert js_arrays in t

ex = D['ex']
EXDATA = [dict(label=x['label'], text=x['text'], source=x['source'], real=x['real'], spoken=x.get('modality') == 'spoken', prev=x.get('prev'), force=x['force'], ops=x['ops'],
               mc=x['mc'], flags=x['flags'], amb=x['amb'], why=x['why'], how=x['how'], save=x['save_struct'], expected=x.get('expected'), match=x.get('match')) for x in ex]
explorer = r'''
/* Part II live reader */
var EX = __EX__;
var reader = document.getElementById('reader');
if (reader) {
  var list = reader.querySelector('.exl'), out = reader.querySelector('.exr'), sel = 0;
  function txt(tag, cls, s){ var n = document.createElement(tag); if (cls) n.className = cls; n.textContent = s; return n; }
  function draw(){
    list.querySelectorAll('.ex').forEach(function(b, i){ b.setAttribute('aria-pressed', String(i === sel)); });
    var x = EX[sel]; out.innerHTML = '';
    out.appendChild(txt('p', 'q', x.text));
    out.appendChild(txt('p', 'src', (x.real ? 'Real request, ' : 'Simulated request, ') + x.source + (x.spoken ? ', spoken' : '') + '.'));
    if (x.prev) out.appendChild(txt('p', 'prev', 'The turn before: \u201c' + x.prev + '\u201d'));
    var dl = document.createElement('dl');
    function row(k, v){ dl.appendChild(txt('dt', '', k)); dl.appendChild(txt('dd', '', v)); }
    row('Statement type', x.force);
    row('What it asks for', x.ops.join(', '));
    if (x.expected) row('Written down before testing', x.expected.join(', ') + '. ' + (x.match ? 'Match.' : 'Miss.'));
    row('Kind of thinking', x.mc);
    row('Structure found', x.flags.length ? x.flags.join('; ') : 'None');
    row('Ambiguity signals', x.amb === 0 ? 'None' : x.amb + (x.why.length ? ': ' + x.why.join('; ') : ''));
    row('Who reads it', x.how);
    row('Model work saved', Math.round(x.save * 100) + '% when only structure is needed');
    out.appendChild(dl);
  }
  EX.forEach(function(x, i){
    var b = document.createElement('button'); b.type = 'button'; b.className = 'ex'; b.textContent = x.label;
    b.addEventListener('click', function(){ sel = i; draw(); });
    list.appendChild(b);
  });
  draw();
}
'''.replace('__EX__', json.dumps(EXDATA))
assert t.rstrip().endswith('</html>') or True
last = t.rfind('})();')
t = t[:last] + explorer + t[last:]
open(OUT, 'w', encoding='utf8').write(t)
print('written', len(t), 'bytes; em dash:', '\u2014' in t, '| chapters registered:', len(P2KEYS))
