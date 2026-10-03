# enhance_v13.py  (run after enhance_v12.py)
# Part II's accent is Hannah green. It takes over from electric yellow everywhere on Part II
# (hero highlight, current-chapter disc, speech bubble, timeline cursor, Part II underline),
# and it first appears at the end of Part I, on "spend" in the Next, Part II teaser,
# the moment the page turns to Part II's subject.
import sys
SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding="utf-8").read()
old = '<h2 id="nph">What to keep, what to spend</h2>'
assert old in s
s = s.replace(old, '<h2 id="nph">What to keep, what to <span class="marker p2m">spend</span></h2>', 1)
CSS = r"""<style>
/* v13: Hannah green is Part II's accent */
:root{--p2acc:#009E60}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]):not([data-pmode="light"]){--p2acc:#50C878} }
:root[data-theme="dark"], :root[data-pmode="dark"], :root[data-pmode="mono"]{--p2acc:#50C878}
:root[data-pmode="light"]{--p2acc:#009E60}
:root[data-page="2"]{--yellow:var(--p2acc)}
.marker.p2m::before{background:var(--p2acc)}
.nextpart .marker{color:var(--ink)}
</style>"""
s = s.replace("</body>", CSS + "</body>", 1)
open(OUT, "w", encoding="utf-8").write(s)
print("wrote", OUT)
