# enhance_v11.py  (run after enhance_v10.py)
# Final review pass against research/ (AGENT_NOTES.md, facts.json, energy_stats_r11.json,
# story_data.json, meta_results.json, sources_results.json, LICENSES.md).
#  1. Water figures come from energy_stats_r11.json (total and data-center water), replacing
#     the v10 estimate. Electricity stays per the same file. Region trade-off goes in a chip.
#  2. Palette for the research charts: Hannah green for electricity, Damani cyan for water.
#     Electric yellow stays the interface accent only. Mono mode stays gray.
#  3. Copy corrections: source-need findings are hand labels, not system output; source detection
#     did not beat its baseline; fresh-request baseline shown; Sonnet electricity savings stated;
#     reproducibility scoped to rounds 9 to 11; external figures acknowledged.
#  4. The 31 predictions open in a floating modal from "Show our work", grouped by round.
#  5. Simulated examples say "written in the style of" their venue; dataset licenses credited.
import json, re, sys, html

SRC = sys.argv[1]; OUT = sys.argv[2]; RES = sys.argv[3]   # RES = path to research/data/results
s = open(SRC, encoding="utf-8").read()
E = json.load(open(RES + "/energy_stats_r11.json"))["models"]["Claude Sonnet 5.5"]
SD = json.load(open(RES + "/story_data.json"))

def sub1(old, new):
    global s
    assert s.count(old) >= 1, "missing: " + old[:90]
    s = s.replace(old, new, 1)

med = lambda k: E[k][2]
HOME_DAY = 29.6
L_PER_DROP = 10

BOLT = '<svg viewBox="0 0 12 16" aria-hidden="true"><path d="M7 0 0 9h5l-1 7 8-10H7l1-6z"/></svg>'
DROP = '<svg viewBox="0 0 12 16" aria-hidden="true"><path d="M6 .8C6 .8.6 7.4.6 10.4a5.4 5.2 0 0 0 10.8 0C11.4 7.4 6 .8 6 .8z"/></svg>'

def icons(svg, n, cls):
    full = int(n); out = [f'<span class="pg {cls}">{svg}</span>'] * full
    if n - full >= 0.05:
        out.append(f'<span class="pg {cls} frac" style="--f:{n-full:.2f}">{svg}</span>')
    return "".join(out)

rows = [("A model reads everything", "pure"),
        ("Rules first, outside knowledge needed", "hyb_latent"),
        ("Rules first, structure only", "hyb_struct")]
parts = []
for name, k in rows:
    kwh = med(k + "_kwh"); wt = med(k + "_water_total"); ws = med(k + "_water_site")
    hrs = kwh / HOME_DAY * 24
    site = f"{ws:.1f}" if ws >= 1 else f"{ws:.2f}".rstrip("0")
    parts.append(
        f'<div class="erow"><div class="ehead"><span class="en">{name}</span><span class="ev">{kwh:.1f} kWh</span></div>'
        f'<div class="eline" role="img" aria-label="{name}: {kwh:.1f} kWh, about {round(hrs)} hours of an average US home&#x27;s electricity">'
        f'<span class="ek">Power</span><span class="pgs">{icons(BOLT, hrs, "bolt")}</span><span class="eq">{round(hrs)} h</span></div>'
        f'<div class="eline" role="img" aria-label="{name}: about {round(wt)} liters of water in all, {site} liters of it at the data center">'
        f'<span class="ek">Water</span><span class="pgs">{icons(DROP, wt / L_PER_DROP, "drop")}</span><span class="eq">{round(wt)} L</span></div>'
        f'<p class="esite">{site} L of that at the data center itself</p></div>')

lo, hi = E["pure_kwh"][1], E["pure_kwh"][3]
fig = ('<figure class="viz eviz">'
       '<div class="ekey"><span><span class="pg bolt">' + BOLT + '</span> 1 hour of an average US home&#x27;s electricity</span>'
       '<span><span class="pg drop">' + DROP + '</span> 10 liters of water</span></div>'
       + "".join(parts) +
       f'<figcaption class="vcap">Middle estimates to understand one million requests with Claude Sonnet 5.5. '
       f'For a model reading everything, the 80% range runs from {lo:.0f} to {hi:.0f} kWh. '
       'Water counts the data center and the power plants that supply it; most of it is at the power plant. '
       'An average US home uses about 29.6 kWh a day (US Energy Information Administration).</figcaption></figure>')
m = re.search(r'<figure class="viz eviz">.*?</figure>', s, flags=re.S)
assert m, "v10 energy figure missing (run enhance_v10.py first)"
s = s[:m.start()] + fig + s[m.end():]

# energy copy: tie the chart to the token savings
lat = 1 - med("hyb_latent_kwh") / med("pure_kwh"); st = 1 - med("hyb_struct_kwh") / med("pure_kwh")
sub1("Across 2,000 different traffic mixes, those figures stayed between 38% and 42%, and between 78% and 90%.</p>",
     f"Across 2,000 different traffic mixes, those figures stayed between 38% and 42%, and between 78% and 90%. "
     f"For Claude Sonnet 5.5, the model in the chart, the middle estimates come to about {lat:.0%} and {st:.0%} less electricity, with water falling in step.</p>")

# region trade-off chip
sub1('<button class="chip" data-ch="p2energy" data-f="2" type="button">Every model we checked</button>',
     '<button class="chip" data-ch="p2energy" data-f="2" type="button">Every model we checked</button>'
     '<button class="chip" data-ch="p2energy" data-f="3" type="button">Where the water goes</button>')
water_chip = {"t": "Where the water goes",
  "d": "Most of the water is used by the power plants that supply a data center, so location decides most of it. "
       "For Claude Sonnet 5.5 reading a million requests in full, that is about 36 liters on the Texas grid, 60 in Iowa, "
       "68 in Virginia or Ohio, 71 in Georgia, and 380 in Oregon, against 123 for the average US data center. "
       "There is no single best place: Texas uses the least power-plant water per kWh, but 59% of its data centers sit in areas of high water stress."}
s = s.replace("</script>\n</body>", "</script>\n</body>", 1)
sub1('FACTS["p2live"] = ', 'FACTS["p2energy"].push(' + json.dumps(water_chip) + ');\nFACTS["p2live"] = ')
inject_js = ""

# ---------- copy corrections ----------
sub1("Every request is checked for how many and what kind of sources it needs. In testing, claims about value were sent to crowd sources 5 of 15 times against 6 of 315 for other claims, and government-relations requests needed several sources 50% of the time against 11% for the rest.",
     "Requests are read for how many and what kind of sources they need. In 330 hand-labeled requests, claims about value called for crowd sources 5 of 15 times against 6 of 315 for other claims, and government-relations requests needed several sources 50% of the time against 11% for the rest.")
sub1("They identify the kind of thinking a request needs 76% of the time on fresh requests.",
     "They identify the kind of thinking a request needs 76% of the time on 120 fresh requests, against 58% for always guessing facts.")
sub1("<li>Whether our measures predict what people actually do afterward.",
     "<li>Source detection. Rules do not yet beat a simple baseline at telling how many sources a request needs (69% against 73%) or what kind (60% against 67%).</li><li>Whether our measures predict what people actually do afterward.")
sub1("Every number comes from our own tests.",
     "Every number comes from our own tests, except a few cited outside figures such as household electricity.")
sub1("Rebuilt our research from public files with one script and matched every result exactly.",
     "Rebuilt three rounds of research from public files, one script each, and matched every output exactly.")
sub1("(x.real ? 'Real request, ' : 'Simulated request, ') + x.source",
     "(x.real ? 'Real request, ' + x.source : 'Simulated request, written for this study in the style of ' + x.source)")
for old in ["written by Pulp in the voices of its customers, are labeled and never counted as real",
            "Requests marked simulated were written by Pulp in the voices of its customers."]:
    if old in s:
        s = s.replace(old, old.replace("written by Pulp in the voices of its customers", "written for this study in the voices of Pulp's customers"))

# dataset credits in the sources band (CC BY requires attribution for quoted examples)
sub1("converted to grayscale for this essay.</p>", "converted to grayscale for this essay.</p><p style=\"margin:0 0 12px\">Example requests in the live reader come from Taskmaster-1 (CC BY 4.0), StaQC (CC BY 4.0), CLINC150 (CC BY 3.0), and TabFact, nvBench, and QMSum (MIT). Simulated examples were written for this study.</p>") if "Example requests in the live reader" not in s else None

# ---------- 31 predictions modal ----------
pred = SD["pred"]
sub1("All of them are published, including the misses.</p>",
     "All of them are published, including the misses.</p><button class=\"predbtn\" type=\"button\" aria-haspopup=\"dialog\">See all 31</button>")
PRED_JS = r"""<script>
(function(){
var PRED = %s;
var btn = document.querySelector('.predbtn'); if (!btn) return;
var ov = null, last = null;
function close(){ if (ov){ ov.remove(); ov = null; document.removeEventListener('keydown', key); if (last) last.focus(); } }
function key(e){ if (e.key === 'Escape') close(); }
btn.addEventListener('click', function(){
  last = document.activeElement;
  ov = document.createElement('div'); ov.id = 'overlay';
  var m = document.createElement('div'); m.id = 'modal'; m.className = 'predmodal';
  m.setAttribute('role', 'dialog'); m.setAttribute('aria-modal', 'true'); m.setAttribute('aria-label', 'All 31 predictions');
  var x = document.createElement('button'); x.id = 'mclose'; x.setAttribute('aria-label', 'Close'); x.textContent = '×';
  var h = document.createElement('h3'); h.textContent = 'All 31 predictions';
  var sub = document.createElement('p'); sub.className = 'psub';
  sub.textContent = 'Written down with a timestamp and fingerprint before each round was tested. 19 met, 3 partly met, 9 not met.';
  m.appendChild(x); m.appendChild(h); m.appendChild(sub);
  var rounds = []; PRED.forEach(function(p){ if (rounds.indexOf(p[0]) < 0) rounds.push(p[0]); });
  rounds.forEach(function(r){
    var g = document.createElement('h4'); g.textContent = 'Round ' + r; m.appendChild(g);
    var ul = document.createElement('ul'); ul.className = 'plist';
    PRED.filter(function(p){ return p[0] === r; }).forEach(function(p){
      var li = document.createElement('li');
      var t = document.createElement('span'); t.className = 'ptx'; t.textContent = p[2];
      var v = document.createElement('span'); v.className = 'pv ' + (p[3] === 'Met' ? 'met' : p[3] === 'Not met' ? 'not' : 'part'); v.textContent = p[3];
      li.appendChild(t); li.appendChild(v); ul.appendChild(li);
    });
    m.appendChild(ul);
  });
  ov.appendChild(m); document.body.appendChild(ov);
  ov.addEventListener('click', function(e){ if (e.target === ov) close(); });
  x.addEventListener('click', close); document.addEventListener('keydown', key); x.focus();
});
})();
</script>""" % json.dumps(pred)

CSS = r"""<style>
/* v11: research palette. Yellow stays the interface accent; green and cyan are data only. */
:root{--sus:#009E60; --aqua:#12C8E0; --aqua-edge:#0E7C8B}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]):not([data-pmode="light"]){--sus:#50C878; --aqua:#12C8E0; --aqua-edge:#12C8E0} }
:root[data-theme="dark"], :root[data-pmode="dark"]{--sus:#50C878; --aqua:#12C8E0; --aqua-edge:#12C8E0}
:root[data-pmode="light"]{--sus:#009E60; --aqua:#12C8E0; --aqua-edge:#0E7C8B}
:root[data-pmode="mono"]{--sus:#C9C9C5; --aqua:#8E8E8A; --aqua-edge:#8E8E8A}
.pg.bolt svg{fill:var(--sus)}
.pg.drop svg{fill:var(--aqua); stroke:var(--aqua-edge); stroke-width:1.1px}
.pg{width:11px; height:15px}
.esite{margin:2px 0 0 52px; font-size:.72rem; color:var(--mut)}
@media (max-width:420px){ .esite{margin-left:0} .eline{grid-template-columns:40px minmax(0,1fr) 34px} .pg{width:9px; height:13px} }
/* predictions modal */
.predbtn{margin-top:12px; font:inherit; font-size:.78rem; font-weight:600; color:var(--fg); background:transparent; border:1px solid var(--fg); border-radius:999px; padding:7px 13px; min-height:44px; cursor:pointer}
.predbtn:hover{background:var(--btn-bg); color:var(--btn-fg); border-color:var(--btn-bg)}
.predbtn:focus-visible{outline:2px solid var(--fg); outline-offset:2px}
/* timeline label only on hover or keyboard focus, so it never sits over the reading column */
#vlabel{opacity:0; visibility:hidden; transition:opacity .12s ease}
#vtl:hover #vlabel, #vtl:focus-within #vlabel{opacity:1; visibility:visible}
@media (hover:none){ #vtl.show #vlabel{opacity:0; visibility:hidden} }
.predmodal{max-width:36rem}
.predmodal .psub{font-size:.86rem; color:var(--mut); margin:0 0 6px}
.predmodal h4{font-size:.7rem; text-transform:uppercase; letter-spacing:.12em; color:var(--mut); margin:18px 0 6px; font-weight:600}
.plist{list-style:none; margin:0; padding:0}
.plist li{display:grid; grid-template-columns:minmax(0,1fr) auto; gap:12px; align-items:baseline; padding:8px 0; border-top:1px solid var(--line); font-size:.88rem}
.pv{font-size:.72rem; font-weight:600; white-space:nowrap; padding:2px 8px; border-radius:999px; border:1px solid var(--line)}
.pv.met{background:var(--btn-bg); color:var(--btn-fg); border-color:var(--btn-bg)}
.pv.not{background:transparent; color:var(--fg)}
.pv.part{background:transparent; color:var(--mut); border-style:dashed}
</style>"""
s = s.replace("</body>", inject_js + PRED_JS + CSS + "</body>", 1)
open(OUT, "w", encoding="utf-8").write(s)
print("wrote", OUT, len(s), "| sonnet savings", f"{lat:.1%}", f"{st:.1%}")
