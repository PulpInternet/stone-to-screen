# enhance_v10.py
# 1. Fast jumps: clicks on the chapter bar, scroll timeline, and Index scroll in about 0.4 s.
# 2. Padding: photos align to the text column, timeline sits clear of the column,
#    counter and Index line up with the bottom bar's right edge, jumps land below the top bar.
# 3. Left timeline: while scrolling and for 1.5 s after, it shows at very low opacity;
#    hover or keyboard focus brings it to full strength.
# 4. Energy chart: sustainability green (Hannah's greens) with electricity and water pictograms.
import re, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "v6.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "index.html"
s = open(SRC, encoding="utf-8").read()

def must_replace(old, new, count=1):
    global s
    n = s.count(old)
    assert n >= 1, "not found: " + old[:80]
    s = s.replace(old, new) if count == 0 else s.replace(old, new, count)

# ---------- 1. fast jumps ----------
must_replace("beats[i].scrollIntoView({behavior:reduced?'auto':'smooth', block:'start', inline:'center'});",
             "window.fastGo(beats[i]);")
FAST = r"""<script>
/* v10: quick, consistent jumps. 0.4 s ease-out; instant under reduced motion. */
window.fastGo = function(el){
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var strip = el.closest && el.closest('.strip');
  if (strip) {
    var sr = strip.getBoundingClientRect(), er = el.getBoundingClientRect();
    strip.scrollLeft += (er.left + er.width / 2) - (sr.left + sr.width / 2);
  }
  var bar = document.getElementById('tbar');
  var off = (bar ? bar.getBoundingClientRect().height : 0) + 20;
  var anchor = strip ? strip.closest('.part') : el;
  if (strip) { var h = anchor.querySelector('.phead'); if (h) anchor = h; }
  var target = Math.max(0, anchor.getBoundingClientRect().top + window.scrollY - off);
  if (reduced) { window.scrollTo(0, target); return; }
  var start = window.scrollY, dist = target - start, t0 = null, dur = 400;
  if (Math.abs(dist) < 2) return;
  function step(ts){
    if (t0 === null) t0 = ts;
    var p = Math.min(1, (ts - t0) / dur), e = 1 - Math.pow(1 - p, 3);
    window.scrollTo(0, start + dist * e);
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
};
</script>"""
s = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + FAST, s, count=1)

# ---------- 3. timeline: 1.5 s, very low opacity unless hovered ----------
must_replace("if (!holding) vtl.classList.remove('show'); }, 5500);",
             "if (!holding) vtl.classList.remove('show'); }, 1500);")

# ---------- 4. energy pictograms ----------
BOLT = '<svg viewBox="0 0 12 16" aria-hidden="true"><path d="M7 0 0 9h5l-1 7 8-10H7l1-6z"/></svg>'
DROP = '<svg viewBox="0 0 12 16" aria-hidden="true"><path d="M6 0C6 0 0 7.2 0 10.4A6 5.6 0 0 0 12 10.4C12 7.2 6 0 6 0z"/></svg>'
HOME_DAY = 29.6        # kWh, average US home per day (from the page)
L_PER_KWH = 1.8        # liters per kWh, LBNL 2016 average on-site data-center water use
L_PER_DROP = 5

def icons(svg, n, cls):
    out, full = [], int(n)
    for _ in range(full):
        out.append(f'<span class="pg {cls}">{svg}</span>')
    frac = n - full
    if frac >= 0.05:
        out.append(f'<span class="pg {cls} frac" style="--f:{frac:.2f}">{svg}</span>')
    return "".join(out)

rows = [("A model reads everything", 26.6),
        ("Rules first, outside knowledge needed", 16.6),
        ("Rules first, structure only", 6.3)]
html_rows = []
for name, kwh in rows:
    hours = kwh / HOME_DAY * 24
    liters = kwh * L_PER_KWH
    html_rows.append(
        f'<div class="erow"><div class="ehead"><span class="en">{name}</span>'
        f'<span class="ev">{kwh} kWh</span></div>'
        f'<div class="eline" role="img" aria-label="{name}: {kwh} kWh, about {round(hours)} hours of an average US home\'s electricity">'
        f'<span class="ek">Power</span><span class="pgs">{icons(BOLT, hours, "bolt")}</span>'
        f'<span class="eq">{round(hours)} h</span></div>'
        f'<div class="eline" role="img" aria-label="{name}: about {round(liters)} liters of cooling water">'
        f'<span class="ek">Water</span><span class="pgs">{icons(DROP, liters / L_PER_DROP, "drop")}</span>'
        f'<span class="eq">{round(liters)} L</span></div></div>')

new_fig = ('<figure class="viz eviz">'
           '<div class="ekey"><span><span class="pg bolt">' + BOLT + '</span> 1 hour of an average US home&#x27;s electricity</span>'
           '<span><span class="pg drop">' + DROP + '</span> 5 liters of data-center cooling water</span></div>'
           + "".join(html_rows) +
           '<figcaption class="vcap">Electricity to understand one million requests with Claude Sonnet 5.5. An average US home uses about 29.6 kWh a day. '
           'Water is estimated at 1.8 liters per kWh, the average on-site use reported for US data centers by Lawrence Berkeley National Laboratory (2016).</figcaption></figure>')
m = re.search(r'(<article class="beat card" id="p2energy".*?)<figure class="viz">.*?</figure>', s, flags=re.S)
assert m, "energy figure not found"
s = s[:m.start()] + m.group(1) + new_fig + s[m.end():]

# ---------- CSS: padding, timeline, energy ----------
CSS = r"""<style>
/* v10 */
html{scroll-behavior:auto}
/* photos share the text column's left edge */
figure img{margin-inline:0; width:min(100%, calc(49.3vh * var(--w) / var(--h)))}
.card figure img{width:min(100%, calc(25.5vh * var(--w) / var(--h)))}
/* scroll timeline: clear of the column, quiet while you read */
#vtl.show{opacity:.14}
#vtl.show:hover, #vtl.show:focus-within, #vtl:hover{opacity:1}
@media (min-width:860px){ #vtl{left:max(2px, calc((100vw - 680px) / 2 - 116px))} }
@media (prefers-reduced-motion:reduce){ #vtl{transition:opacity .12s ease} }
/* top bar: chapter icons centered, counter and Index on the same right edge as the bottom bar */
@media (min-width:1100px){
  #tbar{padding-inline:16px}
  #tbar .inner{max-width:none; display:grid; grid-template-columns:1fr auto 1fr; align-items:center}
  #tbar .tocwrap{grid-column:2}
  #tbar .tocright{grid-column:3; justify-self:end}
}
/* even rhythm between moments and chapters */
.part{padding-block:48px 40px}
.part.vert .beat{padding-block:32px 32px}
.phead{margin-bottom:8px}
.beat header{margin-bottom:14px}
figure{margin:18px 0}
/* energy chart: sustainability green, electricity and water pictograms */
:root{--sus:#009E60; --sus2:#50C878}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]):not([data-pmode="light"]){--sus:#50C878; --sus2:#3FB37F} }
:root[data-theme="dark"], :root[data-pmode="dark"]{--sus:#50C878; --sus2:#3FB37F}
:root[data-pmode="light"]{--sus:#009E60; --sus2:#50C878}
:root[data-pmode="mono"]{--sus:#C9C9C5; --sus2:#8E8E8A}
.eviz{padding:16px 0 12px}
.ekey{display:flex; flex-wrap:wrap; gap:6px 18px; font-size:.76rem; color:var(--mut); margin-bottom:10px}
.ekey > span{display:inline-flex; align-items:center; gap:6px}
.erow{padding:10px 0; border-top:1px solid var(--line)}
.erow:first-of-type{border-top:0}
.ehead{display:grid; grid-template-columns:minmax(0,1fr) auto; gap:12px; font-size:.86rem; margin-bottom:6px}
.ehead .ev{font-weight:600; font-variant-numeric:tabular-nums}
.eline{display:grid; grid-template-columns:44px minmax(0,1fr) 40px; align-items:center; gap:8px; min-height:22px}
.ek{font-size:.68rem; text-transform:uppercase; letter-spacing:.1em; color:var(--mut); font-weight:600}
.eq{font-size:.76rem; color:var(--mut); text-align:right; font-variant-numeric:tabular-nums}
.pgs{display:flex; flex-wrap:wrap; gap:2px; min-width:0}
.pg{display:inline-block; width:11px; height:15px; line-height:0}
.pg svg{width:100%; height:100%; display:block}
.pg.bolt svg{fill:var(--sus)}
.pg.drop svg{fill:var(--sus2)}
.pg.frac{clip-path:inset(0 calc((1 - var(--f)) * 100%) 0 0)}
@media (forced-colors:active){ .pg svg{fill:CanvasText} }
</style>"""
s = s.replace("</body>", CSS + "</body>", 1)

open(OUT, "w", encoding="utf-8").write(s)
print("wrote", OUT, len(s))
