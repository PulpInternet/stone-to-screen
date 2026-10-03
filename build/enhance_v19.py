# enhance_v19.py  (run after enhance_v18.py, then enhance_v15.py last)
# Part III joins the shared navigation. Every part now has the same furniture: the chapter bar,
# the left scroll timeline, the Index, and the New here bar. Part III's three sections become
# Chapters 15 to 17 with their own icons, titles, and New here notes, and the main script
# drives them exactly as it drives Parts I and II.
import sys, re
SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding="utf-8").read()
def sub1(old, new):
    global s
    assert s.count(old) == 1, f"expected once ({s.count(old)}): {old[:90]}"
    s = s.replace(old, new, 1)

# ---- 1. navigation belongs to every part ----
sub1('<nav id="tbar" aria-label="Chapters" data-page="1 2">', '<nav id="tbar" aria-label="Chapters">')
sub1('<div id="vtl" data-page="1 2">', '<div id="vtl">')
sub1('<button id="bbtn" type="button" aria-haspopup="dialog" data-page="1 2">', '<button id="bbtn" type="button" aria-haspopup="dialog">')
sub1("(function(){\nif (window.__P3) return;\nvar FACTS = {", "(function(){\nvar FACTS = {")
sub1(':root[data-page="3"] #bbar{grid-template-columns:auto minmax(0,1fr) auto}', '')

# ---- 2. the main script learns Part III ----
P3DATA = r"""
/* v19: Part III, Chapters 15 to 17 */
KEYS.push("p3mix", "p3save", "p3method");
TITLES.push("Set your traffic", "What you would save", "How it is calculated");
DATES.push("Your inputs", "Per year", "Method");
INNOV.push({"t": "Your own mix", "d": "Each kind of request carries its measured share of saved work and its average length. Set the mix that looks like your traffic and the estimate follows it."},
           {"t": "Savings you can check", "d": "Provider spend at list prices, share of model work, electricity with its 80% range, carbon, and water, all from the research in Part II."},
           {"t": "Calculated, not metered", "d": "These are estimates from measured token counts and published energy research. They cover understanding each request, not writing the answer."});
PARTS.push({"t": "Your traffic", "n": 1}, {"t": "Savings", "n": 1}, {"t": "Method", "n": 1});
"""
sub1("var P2 = !!window.__P2, LO = P2 ? 34 : 0, HI = P2 ? 42 : 34;",
     P3DATA + "var P2 = !!window.__P2, P3 = !!window.__P3, LO = P3 ? 42 : P2 ? 34 : 0, HI = P3 ? 45 : P2 ? 42 : 34;")
sub1("PARTS = P2 ? PARTS.slice(10) : PARTS.slice(0, 10);", "PARTS = P3 ? PARTS.slice(14) : P2 ? PARTS.slice(10, 14) : PARTS.slice(0, 10);")
sub1("ICONS[pi + (P2 ? 10 : 0)]", "ICONS[pi + (P3 ? 14 : P2 ? 10 : 0)]")
sub1("String(pi + 1 + (P2 ? 10 : 0))", "String(pi + 1 + (P3 ? 14 : P2 ? 10 : 0))")
sub1("P2 ? 'Part II' : 'Part I'", "P3 ? 'Part III' : P2 ? 'Part II' : 'Part I'")
sub1("P2 ? 'Research' : 'Antiquity'", "P3 ? 'Inputs' : P2 ? 'Research' : 'Antiquity'")
sub1("P2 ? 'Your turn' : 'Today'", "P3 ? 'Method' : P2 ? 'Your turn' : 'Today'")
sub1("a.classList.contains(P2 ? 'p2' : 'p1')", "a.classList.contains(P3 ? 'p3' : P2 ? 'p2' : 'p1')")
m = re.search(r"var ICONS = \[.*?\];", s, flags=re.S); assert m
icons = ['<path d=\\"M4 7h9M17 7h3M4 17h3M11 17h9M15 5v4M9 15v4\\"/>',
         '<path d=\\"M13 3 5 14h6l-1 7 8-11h-6l1-7z\\"/>',
         '<path d=\\"M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01\\"/>']
s = s[:m.end()] + "\nICONS.push(" + ", ".join('"%s"' % i for i in icons) + ");" + s[m.end():]
sub1("if (P2) document.querySelectorAll('.beat[data-i]')",
     "if (P3) document.querySelectorAll('.beat[data-i]').forEach(function(b){ b.setAttribute('data-i', String(+b.getAttribute('data-i') - 42)); });\n  if (P2) document.querySelectorAll('.beat[data-i]')")

# ---- 3. Part III markup as chapters ----
blk = re.search(r'<div class="wrap" data-page="3">(.*?)</main></div>', s, flags=re.S); assert blk
inner = blk.group(1)
hero = re.search(r'<header class="hero" id="hero3">.*?</header>', inner, flags=re.S).group(0)
hero = hero.replace('id="hero3"', 'id="hero" data-page="3"').replace('id="modes3" class="modes3"', 'id="modes"')
sec = lambda cls: re.search(r'<section class="%s".*?</section>' % cls, inner, flags=re.S).group(0)
estin, estout, estmethod = sec("estin"), sec("estout"), sec("estmethod")
def chapter(n, pid, bid, i, title, epi, body):
    body = body.replace("<section ", "<div ", 1)[:-len("</section>")] + "</div>"
    return (f'<section class="part vert" id="part{n}" data-page="3"><header class="phead"><p class="pnum">Chapter {n}</p>'
            f'<h2>{title}</h2><p class="epi">{epi}</p></header><article class="beat" id="{bid}" data-i="{i}">{body}</article></section>')
p3 = (chapter(15, "part15", "p3mix", 42, "Your traffic", "Set the kinds of requests you handle, how many, the model, and where it runs.",
              estin.replace('<h2 id="inh">Your traffic</h2>', '')) +
      chapter(16, "part16", "p3save", 43, "Savings", "What reading with rules first would save, per year.",
              estout.replace('<h2 id="outh">What reading with rules first saves, per year</h2>', '')) +
      chapter(17, "part17", "p3method", 44, "Method", "Calculated from the research in Part II, not metered.",
              estmethod.replace('<h2 id="mh">How this is calculated</h2>', '')))
p3 = p3.replace('aria-labelledby="inh"', '').replace('aria-labelledby="outh"', 'aria-label="Savings"').replace('aria-labelledby="mh"', '')
s = s[:blk.start()] + s[blk.end():]
h2 = s.find('<header class="hero" id="hero" data-page="2">'); e2 = s.find("</header>", h2) + len("</header>")
s = s[:e2] + "\n" + hero + s[e2:]
end_main = s.find("</main>")
s = s[:end_main] + p3 + "\n" + s[end_main:]

CSS = r"""<style>
/* v19: Part III chapters share the reading column and rhythm of Parts I and II */
.estin, .estout, .estmethod{display:flex; flex-direction:column}
.estgrid{margin-top:var(--s5)}
#p3save .otable{margin-top:var(--s2)}
/* a mouse click on a control never leaves a ring behind; keyboard focus still shows one */
:focus:not(:focus-visible){outline:none}
@media (hover:none){ #vtl:hover, .plink:hover, #bbtn:hover{opacity:inherit} }
</style>"""
s = s.replace("</body>", CSS + "</body>", 1)
open(OUT, "w", encoding="utf-8").write(s)
print("wrote", OUT)
