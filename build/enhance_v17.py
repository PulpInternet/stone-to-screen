# enhance_v17.py  (run after enhance_v16.py, then enhance_v15.py last)
# Part III: "Run the numbers", the estimator from the first research page, rebuilt for the
# public page. It opens at index.html#part-iii.
#  - Traffic is a mix of the six public kinds of requests from the research, not the internal
#    customer profiles (research/internal is never used).
#  - Dollars are AI-provider spend at the list prices used in the research, labeled as such.
#    No Pulp or Thinkwell prices appear anywhere.
#  - Every input number is read here from research/data/results, never typed in.
#  - Electricity uses energy_stats_r11.json, so Part III agrees with the Part II chart.
import json, sys, re
SRC, OUT, RES = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(SRC, encoding="utf-8").read()
SD = json.load(open(RES + "/story_data.json"))
ES = json.load(open(RES + "/energy_stats_r11.json"))["models"]

def sub1(old, new, count=1):
    global s
    assert old in s, "missing: " + old[:90]
    s = s.replace(old, new, count)

MODELS = ["Claude Haiku 4.5", "Claude Sonnet 5.5", "Claude Opus 5.5"]
DATA = {
  "arenas": SD["arenas"], "mean": SD["mean"], "price": {m: SD["price"][m] for m in MODELS},
  "weighted": SD["weighted"], "reasoning": SD["reasoning"], "regions": SD["regions"],
  "energy": {m: {"kwh": ES[m]["pure_kwh"], "lat": ES[m]["hyb_latent_saved"][2], "str": ES[m]["hyb_struct_saved"][2],
                 "confidence": ES[m]["confidence"]} for m in MODELS},
  "home_kwh_day": 29.6, "site_l_per_kwh": 0.12,
}

# ---------- page routing: a third page ----------
sub1('location.hash === "#part-ii" ? "2" : "1"', 'location.hash === "#part-iii" ? "3" : location.hash === "#part-ii" ? "2" : "1"')
sub1("var P2 = location.hash === '#part-ii'; window.__P2 = P2;",
     "var P2 = location.hash === '#part-ii'; window.__P2 = P2; var P3 = location.hash === '#part-iii'; window.__P3 = P3; var PG = P3 ? '3' : P2 ? '2' : '1';")
sub1("if (el.getAttribute('data-page') !== (P2 ? '2' : '1')) el.remove();",
     "if (el.getAttribute('data-page').split(' ').indexOf(PG) < 0) el.remove();")
sub1("document.title = P2 ? 'From Stone to Screen, Part II' : 'From Stone to Screen';",
     "document.title = P3 ? 'From Stone to Screen, Part III' : P2 ? 'From Stone to Screen, Part II' : 'From Stone to Screen';")
# the chapter machinery belongs to Parts I and II; Part III is a single tool
sub1('<nav id="tbar" aria-label="Chapters">', '<nav id="tbar" aria-label="Chapters" data-page="1 2">')
sub1('<div id="vtl">', '<div id="vtl" data-page="1 2">')
sub1('<button id="bbtn" type="button" aria-haspopup="dialog">', '<button id="bbtn" type="button" aria-haspopup="dialog" data-page="1 2">')
sub1("(function(){\nvar FACTS = {", "(function(){\nif (window.__P3) return;\nvar FACTS = {")

# ---------- bottom bar: Part III link ----------
m = re.search(r'<a class="plink p2" href="#part-ii">.*?</a>', s, flags=re.S)
assert m
s = s[:m.start()] + '<span class="pright">' + m.group(0) + \
    '<a class="plink p3" href="#part-iii"><span class="pk">Part III</span><span class="pt">: Run the numbers</span></a></span>' + s[m.end():]

# ---------- end of Part II: lead into Part III ----------
proof_end = s.find('<p class="backrow"><a class="pagebtn ghost" href="#">Back to Part I</a></p>\n</div></section>', s.find('id="proof"'))
assert proof_end > 0
credit = re.search(r'<p style="margin:0 0 12px">Example requests in the live reader.*?</p>', s, flags=re.S)
credit_html = credit.group(0).replace('style="margin:0 0 12px"', 'class="pnote"') if credit else ""
if credit: s = s[:credit.start()] + s[credit.end():]; proof_end = s.find('<p class="backrow"><a class="pagebtn ghost" href="#">Back to Part I</a></p>\n</div></section>', s.find('id="proof"'))
lead = (credit_html +
        '<div class="p3lead"><p class="pnum">Next, Part III</p><h2>Run the <span class="marker p2m">numbers</span></h2>'
        '<p>Pick the kinds of requests you handle, how many, which model, and where it runs. The estimator applies the measurements above and shows what reading with rules first would save in provider spend, electricity, carbon, and water.</p>'
        '<p class="backrow"><a class="pagebtn" href="#part-iii">Open Part III</a> <a class="pagebtn ghost" href="#">Back to Part I</a></p></div>')
old = '<p class="backrow"><a class="pagebtn ghost" href="#">Back to Part I</a></p>\n</div></section>'
s = s[:proof_end] + lead + "\n</div></section>" + s[proof_end + len(old):]

# ---------- Part III page ----------
ARENA_SUB = {k: f"{v['n']:,} requests in the research" for k, v in SD["arenas"].items()}
sliders = "".join(
  f'<div class="mixrow"><label for="mx{i}"><span class="mxn">{k}</span><span class="mxs">{ARENA_SUB[k]}</span></label>'
  f'<input id="mx{i}" type="range" min="0" max="100" step="5" value="50" data-arena="{k}"><output for="mx{i}" class="mxv">17%</output></div>'
  for i, k in enumerate(SD["arenas"].keys()))
regions = "".join(f'<option value="{k}">{k}</option>' for k in SD["regions"])
models = "".join(f'<option value="{m}"{" selected" if m=="Claude Sonnet 5.5" else ""}>{m.replace("Claude ", "")}</option>' for m in MODELS)
PAGE3 = f"""<div class="wrap" data-page="3"><header class="hero" id="hero3">
  <div id="modes3" class="modes3" role="group" aria-label="Color mode">
    <button type="button" data-m="light" aria-pressed="false">Light</button>
    <button type="button" data-m="dark" aria-pressed="false">Dark</button>
    <button type="button" data-m="mono" aria-pressed="false">Mono</button>
  </div>
  <p class="kicker">From Stone to Screen, Part III</p>
  <h1>Run the <span class="marker">numbers</span></h1>
  <p class="lede">Part II measured what reading with rules first saves. Here you can apply it to your own traffic. Set the kinds of requests you handle, how many you send a year, the model, and where it runs.</p>
  <p class="sub">Estimates, calculated from the research in Part II, not metered. They cover understanding each request, not writing the answer.</p>
</header>
<main class="est">
<section class="estin" aria-labelledby="inh">
  <h2 id="inh">Your traffic</h2>
  <p class="esthint">How much of each kind of request you handle. The shares always add up to 100%.</p>
  <div class="mix">{sliders}</div>
  <div class="estgrid">
    <label class="fld" for="cvol"><span>Requests a year</span><input id="cvol" type="number" inputmode="numeric" min="0" step="1000" value="1000000"></label>
    <label class="fld" for="cmodel"><span>Model</span><select id="cmodel">{models}</select></label>
    <label class="fld" for="creason"><span>Reasoning mode</span><select id="creason"><option value="0">Off</option><option value="1">On</option></select></label>
    <label class="fld" for="cregion"><span>Where it runs</span><select id="cregion">{regions}</select></label>
  </div>
</section>
<section class="estout" aria-labelledby="outh" aria-live="polite">
  <h2 id="outh">What reading with rules first saves, per year</h2>
  <p id="cbase" class="cbase"></p>
  <div class="otable" role="table" aria-label="Savings per year">
    <div class="orow ohead" role="row"><span role="columnheader"></span><span role="columnheader">Outside knowledge needed</span><span role="columnheader">Structure only</span></div>
    <div id="orows"></div>
  </div>
  <figure class="viz eviz" id="cpicto"></figure>
  <p id="cnote" class="vcap"></p>
</section>
<section class="estmethod" aria-labelledby="mh">
  <h2 id="mh">How this is calculated</h2>
  <ul>
    <li><b>Two cases.</b> Outside knowledge needed: the request still goes to a model, but rules have already read its structure, so the model reads less. Structure only: rules handle the request and no model is called for understanding it.</li>
    <li><b>Traffic.</b> Each kind of request carries its measured share of saved work and its average length from the research. Your mix weights them.</li>
    <li><b>Provider spend.</b> Calculated at the AI providers' published list prices used in the research. It is what you would pay the model provider, never a Pulp or Thinkwell price.</li>
    <li><b>Electricity, carbon, and water.</b> Electricity uses the middle estimate for the chosen model from the energy research, with its 80% range shown. Carbon and water use the chosen grid's figures; water counts the power plants and the data center.</li>
    <li><b>Reasoning mode</b> multiplies the work, because thinking tokens are billed and computed too.</li>
  </ul>
  <p class="backrow"><a class="pagebtn ghost" href="#part-ii">Back to Part II</a> <a class="pagebtn ghost" href="#">Back to Part I</a></p>
</section>
</main></div>"""
sub1('<section class="endnote" data-page="1">', PAGE3 + '\n<section class="endnote" data-page="1">')

ESTJS = r"""<script>
(function(){
if (!window.__P3) return;
var D = %s;
var $ = function(id){ return document.getElementById(id); };
/* mode switch and page links (Parts I and II handle these in their own script) */
function setMode(m, persist){
  if (m) document.documentElement.setAttribute('data-pmode', m); else document.documentElement.removeAttribute('data-pmode');
  document.querySelectorAll('#modes3 button').forEach(function(b){ b.setAttribute('aria-pressed', String(b.dataset.m === m)); });
  if (persist) { try { m ? localStorage.setItem('pmode', m) : localStorage.removeItem('pmode'); } catch (e) {} }
}
var saved = null; try { saved = localStorage.getItem('pmode'); } catch (e) {}
if (saved === 'light' || saved === 'dark' || saved === 'mono') setMode(saved, false);
document.querySelectorAll('#modes3 button').forEach(function(b){
  b.addEventListener('click', function(){ var cur = document.documentElement.getAttribute('data-pmode'); setMode(cur === b.dataset.m ? null : b.dataset.m, true); });
});
document.querySelectorAll('.plink').forEach(function(a){ if (a.classList.contains('p3')) { a.setAttribute('aria-current', 'page'); a.addEventListener('click', function(e){ e.preventDefault(); scrollTo(0, 0); }); } });
addEventListener('hashchange', function(){ location.reload(); });
if (!matchMedia('(prefers-reduced-motion: reduce)').matches) { var h = $('hero3'); if (h) h.classList.add('sweep'); }

/* estimator */
var sliders = [].slice.call(document.querySelectorAll('.mix input[type=range]'));
var fmt = function(v, d){ return v.toLocaleString('en-US', {maximumFractionDigits: d === undefined ? 0 : d}); };
function usd(v){ return v >= 100 ? '$' + fmt(Math.round(v)) : '$' + fmt(v, 2); }
function qty(v, unit){ return (v >= 100 ? fmt(Math.round(v)) : v >= 10 ? fmt(v, 1) : fmt(v, 2)) + ' ' + unit; }
function mixStats(){
  var tot = sliders.reduce(function(a, s){ return a + (+s.value); }, 0) || 1, inten = 0, sd = 0, ss = 0;
  sliders.forEach(function(s){
    var w = (+s.value) / tot, A = D.arenas[s.dataset.arena], t = w * A.tok / D.mean;
    s.nextElementSibling.textContent = Math.round(w * 100) + '%%';
    inten += t; sd += t * A.sd; ss += t * A.ss;
  });
  return { inten: inten, sd: sd / inten, ss: ss / inten };
}
function icons(cls, n){ var o = '', full = Math.floor(n); for (var i = 0; i < Math.min(full, 40); i++) o += '<span class="pg ' + cls + '">' + ICON[cls] + '</span>'; if (full < 40 && n - full >= .05) o += '<span class="pg ' + cls + ' frac" style="--f:' + (n - full).toFixed(2) + '">' + ICON[cls] + '</span>'; return o; }
var ICON = { bolt: '<svg viewBox="0 0 12 16" aria-hidden="true"><path d="M7 0 0 9h5l-1 7 8-10H7l1-6z"/></svg>', drop: '<svg viewBox="0 0 12 16" aria-hidden="true"><path d="M6 .8C6 .8.6 7.4.6 10.4a5.4 5.2 0 0 0 10.8 0C11.4 7.4 6 .8 6 .8z"/></svg>' };
function niceUnit(maxv){ var steps = [1, 2, 5]; for (var e = 0; e < 9; e++) for (var i = 0; i < 3; i++) { var u = steps[i] * Math.pow(10, e); if (maxv / u <= 30) return u; } return 1e9; }
function calc(){
  var s = mixStats(), vol = Math.max(0, +$('cvol').value || 0), m = $('cmodel').value, on = $('creason').value === '1';
  var reg = D.regions[$('cregion').value], R = D.reasoning, E = D.energy[m], mm = vol / 1e6;
  var base = mm * D.price[m] * s.inten, shD = s.sd, shS = s.ss;
  if (on) { base *= R.cost; shD = R.sd; shS = R.ss; }
  var bk = mm * E.kwh[2] * s.inten, kD, kS;
  if (on) { kD = bk * (R.e_pure - R.e_lat * (1 - s.sd)); kS = bk * (R.e_pure - R.e_str * (1 - s.ss)); }
  else { kD = bk * s.sd * (E.lat / D.weighted.save_data); kS = bk * s.ss * (E.str / D.weighted.save_struct_l2); }
  var lo = E.kwh[1] / E.kwh[2], hi = E.kwh[3] / E.kwh[2], w = reg.ewif + D.site_l_per_kwh;
  $('cbase').textContent = 'Without rules first, understanding ' + fmt(vol) + ' requests a year with ' + m.replace('Claude ', '') + (on ? ' and reasoning' : '') +
    ' would cost about ' + usd(base) + ' in provider spend and use about ' + qty(bk * (on ? R.e_pure : 1), 'kWh') + '.';
  var rows = [
    ['Provider spend', usd(base * shD), usd(base * shS), 'At provider list prices'],
    ['Share of model work', Math.round(shD * 100) + '%%', Math.round(shS * 100) + '%%', ''],
    ['Electricity', qty(kD, 'kWh'), qty(kS, 'kWh'), 'Likely ' + qty(kD * lo, '') + 'to ' + qty(kD * hi, 'kWh') + ' and ' + qty(kS * lo, '') + 'to ' + qty(kS * hi, 'kWh')],
    ['Days of a US home', qty(kD / D.home_kwh_day, 'days'), qty(kS / D.home_kwh_day, 'days'), ''],
    ['Carbon', qty(kD * reg.ci, 'kg'), qty(kS * reg.ci, 'kg'), ''],
    ['Water', qty(kD * w, 'liters'), qty(kS * w, 'liters'), '']
  ];
  $('orows').innerHTML = rows.map(function(r){ return '<div class="orow" role="row"><span role="rowheader">' + r[0] + (r[3] ? '<span class="osub">' + r[3] + '</span>' : '') + '</span><span role="cell">' + r[1] + '</span><span role="cell" class="ohi">' + r[2] + '</span></div>'; }).join('');
  var kh = kS / D.home_kwh_day * 24, wl = kS * w, uh = niceUnit(kh), ul = niceUnit(wl);
  $('cpicto').innerHTML = '<div class="ekey"><span><span class="pg bolt">' + ICON.bolt + '</span> ' + fmt(uh) + (uh === 1 ? ' hour' : ' hours') + ' of a US home&#x27;s electricity</span><span><span class="pg drop">' + ICON.drop + '</span> ' + fmt(ul) + (ul === 1 ? ' liter' : ' liters') + ' of water</span></div>' +
    '<div class="erow"><div class="ehead"><span class="en">Saved a year, structure only</span><span class="ev">' + qty(kS, 'kWh') + '</span></div>' +
    '<div class="eline" role="img" aria-label="Electricity saved: about ' + fmt(Math.round(kh)) + ' hours of an average US home"><span class="ek">Power</span><span class="pgs">' + icons('bolt', kh / uh) + '</span><span class="eq">' + qty(kh, 'h') + '</span></div>' +
    '<div class="eline" role="img" aria-label="Water saved: about ' + fmt(Math.round(wl)) + ' liters"><span class="ek">Water</span><span class="pgs">' + icons('drop', wl / ul) + '</span><span class="eq">' + qty(wl, 'L') + '</span></div></div>' +
    '<figcaption class="vcap">Pictograms show the structure-only case. Each icon is a round unit chosen for your volume.</figcaption>';
  $('cnote').textContent = 'Model: ' + m + ', energy estimate confidence ' + E.confidence.toLowerCase() + '. Grid: ' + $('cregion').value + ', ' + Math.round(reg.ci * 1000) + ' g of carbon and ' + w.toFixed(2) + ' liters of water per kWh' + (reg.stress != null ? ', ' + Math.round(reg.stress * 100) + '%% of its data centers in high water-stress areas' : '') + '. Electricity ranges are the 80%% range of the energy research.';
}
sliders.concat([$('cvol'), $('cmodel'), $('creason'), $('cregion')]).forEach(function(el){ el.addEventListener('input', calc); el.addEventListener('change', calc); });
calc();
})();
</script>""" % json.dumps(DATA)

CSS = r"""<style>
/* v17: Part III, the estimator. Same tokens and chart parts as Part II. */
:root[data-page="3"]{--yellow:var(--p2acc)}
.pright{grid-column:3; justify-self:end; display:flex; align-items:center; gap:var(--s5); min-width:0}
@media (max-width:1100px){ .pright{gap:var(--s4)} }
@media (max-width:560px){ .pright{gap:var(--s3)} }
:root[data-page="3"] #bbar{grid-template-columns:auto minmax(0,1fr) auto}
.p3lead{border-top:1px solid var(--line); margin-top:var(--s7); padding-top:var(--s6)}
.p3lead h2{font-size:clamp(1.9rem,4.6vw,2.8rem); line-height:1.05; letter-spacing:-0.02em; margin:0 0 var(--s3); font-weight:800}
.p3lead p{max-width:40rem}
.modes3{position:absolute; top:18px; right:0; display:flex; border:1px solid var(--line); border-radius:999px; overflow:hidden}
.modes3 button{font:inherit; font-size:.7rem; font-weight:600; letter-spacing:.06em; text-transform:uppercase; padding:6px 11px; min-height:var(--tap); background:var(--bg); color:var(--mut); border:0; cursor:pointer}
.modes3 button[aria-pressed="true"]{background:var(--btn-bg); color:var(--btn-fg)}
.modes3 button:focus-visible{outline:2px solid var(--fg); outline-offset:-2px}
.est{display:flex; flex-direction:column; gap:var(--s7); padding-block:var(--s5) var(--s7)}
.est h2{font-size:1.35rem; letter-spacing:-0.01em; margin:0 0 var(--s3); font-weight:800}
.esthint{color:var(--mut); font-size:.9rem; margin:0 0 var(--s4)}
.mix{display:flex; flex-direction:column; gap:var(--s3)}
.mixrow{display:grid; grid-template-columns:minmax(0,1fr) minmax(120px,1.1fr) 3.2em; align-items:center; gap:var(--s4); min-height:var(--tap)}
.mixrow label{display:flex; flex-direction:column; min-width:0}
.mxn{font-weight:600; font-size:.92rem}
.mxs{color:var(--mut); font-size:.74rem}
.mixrow input[type=range]{width:100%; min-height:var(--tap); accent-color:var(--p2acc); margin:0}
.mxv{font-variant-numeric:tabular-nums; text-align:right; font-weight:600}
.estgrid{display:grid; grid-template-columns:repeat(auto-fit, minmax(150px, 1fr)); gap:var(--s4); margin-top:var(--s5)}
.fld{display:flex; flex-direction:column; gap:var(--s1); min-width:0}
.fld span{font-size:.7rem; text-transform:uppercase; letter-spacing:.1em; color:var(--mut); font-weight:600}
.fld input, .fld select{font:inherit; font-size:1rem; min-height:var(--tap); padding:0 var(--s3); border:1px solid var(--line); border-radius:6px; background:var(--card); color:var(--fg); min-width:0; width:100%}
.fld input:focus-visible, .fld select:focus-visible{outline:2px solid var(--fg); outline-offset:1px}
.cbase{font-size:1rem; margin:0 0 var(--s4); max-width:40rem}
.otable{border-top:1px solid var(--line)}
.orow{display:grid; grid-template-columns:minmax(0,1.2fr) minmax(0,1fr) minmax(0,1fr); gap:var(--s3); padding:var(--s3) 0; border-bottom:1px solid var(--line); align-items:baseline; font-variant-numeric:tabular-nums}
.orow > span:not(:first-child){text-align:right}
.ohead span{font-size:.7rem; text-transform:uppercase; letter-spacing:.1em; color:var(--mut); font-weight:600}
.orow .ohi{font-weight:700}
.osub{display:block; font-style:normal; font-size:.72rem; color:var(--mut); font-weight:400}
.estmethod ul{margin:0; padding-left:var(--s5); display:flex; flex-direction:column; gap:var(--s2); max-width:40rem}
.estmethod li{font-size:.92rem}
@media (max-width:560px){
  .mixrow{grid-template-columns:minmax(0,1fr) 3em; row-gap:0}
  .mixrow input[type=range]{grid-column:1 / -1; grid-row:2}
  .orow{grid-template-columns:minmax(0,1fr) minmax(0,1fr); }
  .orow > span:first-child{grid-column:1 / -1}
  .orow > span:not(:first-child){text-align:left}
  .ohead > span:first-child{display:none}
}
</style>"""
s = s.replace("</body>", ESTJS + CSS + "</body>", 1)
open(OUT, "w", encoding="utf-8").write(s)
print("wrote", OUT)
