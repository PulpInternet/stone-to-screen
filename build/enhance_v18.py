# enhance_v18.py  (run after enhance_v17.py, then enhance_v15.py last)
# Consolidation pass. Folds the old raw values into tokens (rule: fix at the source when a rule
# keeps being overridden), makes the page-hiding rule work for three parts, fixes the hero
# highlight spacing, and evens the hero measures.
import sys, re
SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding="utf-8").read()
n = 0
def rep(old, new, count=0):
    global s, n
    c = s.count(old); assert c, "missing: " + old[:80]
    s = s.replace(old, new) if not count else s.replace(old, new, count); n += c if not count else 1

# ---- fold legacy raw values into tokens ----
rep("background:rgba(0,0,0,.5)", "background:var(--scrim)")
rep("box-shadow:0 18px 50px rgba(0,0,0,.35)", "box-shadow:var(--shadow)")
rep("color:#161716", "color:var(--on-accent)")
rep("body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#faf9f5;color:#141413}",
    "body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg,Canvas);color:var(--fg,CanvasText)}")
for sel, z in (("#tbar{", "50"), ("#bbar{", "50")):
    pass
s = re.sub(r"(#overlay\{[^}]*?)z-index:80", r"\1z-index:var(--z-modal)", s)
s = re.sub(r"(#vtl\{[^}]*?)z-index:45", r"\1z-index:var(--z-rail)", s)
s = re.sub(r"(#(?:tbar|bbar)\{[^}]*?)z-index:50", r"\1z-index:var(--z-bar)", s)
s = re.sub(r"z-index:(-1|0|1|2|3)\b", lambda m: "z-index:var(--z-%s)" % ("under" if m.group(1) == "-1" else m.group(1)), s)
# ---- three parts: hide other parts before scripts run, by word match ----
rep('html[data-page="1"] [data-page="2"], html[data-page="2"] [data-page="1"]{display:none !important}',
    'html[data-page="1"] [data-page]:not([data-page~="1"]):not(html), html[data-page="2"] [data-page]:not([data-page~="2"]):not(html), html[data-page="3"] [data-page]:not([data-page~="3"]):not(html){display:none !important}')
rep("#tlabel{display:none !important}", "#tbar #tlabel{display:none}")
CSS = r"""<style>
/* v18: consolidation */
:root{--scrim:rgba(0,0,0,.5); --shadow:0 18px 50px rgba(0,0,0,.35); --on-accent:#161716;
  --z-under:-1; --z-0:0; --z-1:1; --z-2:2; --z-3:3}
/* hero highlight: the block sits inside the word's own box, so the space before it stays a space */
.marker{margin:0; padding:0 .06em}
.marker::before{left:0; right:0; top:.1em; bottom:.02em}
/* one reading measure in the hero */
.hero p.lede, .hero p.sub{max-width:40rem}
.hero p.sub{margin-top:var(--s2)}
/* bottom bar: part names only where all three fit beside the middle button */
#bbar .plink .pt{display:none}  /* three part links never fit with their titles beside the middle button */
/* mode switch: aligned to the column's right edge, never under the browser bar */
#modes, .modes3{top:var(--s5)}
</style>"""
s = s.replace("</body>", CSS + "</body>", 1)
open(OUT, "w", encoding="utf-8").write(s)
print("wrote", OUT, "replacements", n)
