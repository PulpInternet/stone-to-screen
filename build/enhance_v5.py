"""v5: Part I and Part II as two pages in one file, with an introduction and a button between them."""
import re
SRC = '/mnt/user-data/outputs/From_Stone_to_Screen_v4.html'
OUT = '/mnt/user-data/outputs/From_Stone_to_Screen_v5.html'
t = open(SRC, encoding='utf8').read()
def once(a, b):
    global t
    assert t.count(a) == 1, a[:80]
    t = t.replace(a, b)

# Part I hero, then Part II hero right after it
once('<header class="hero" id="hero">', '<header class="hero" id="hero" data-page="1">')
i = t.find('<header class="hero" id="hero" data-page="1">'); j = t.find('</header>', i) + len('</header>')
modes = re.search(r'<div id="modes".*?</div>', t[i:j], re.S).group(0)
P2LEDE = "Part I ends with machines that hold a memory of almost everything and spend energy every time they use it. Part II is about doing that well: deciding what a machine must remember, what it can compress, and what it needs to spend. It comes from Pulp Corporation, established 2026 in Brooklyn, New York, which builds tools for reading language well and studies how messages move the people who receive them."
hero2 = ('\n<header class="hero" id="hero" data-page="2">\n  ' + modes + '\n  <p class="kicker">From Stone to Screen, Part II</p>\n'
         '  <h1>What to keep, what to <span class="marker">spend</span></h1>\n'
         f'  <p class="lede">{P2LEDE}</p>\n'
         '  <p class="sub">Four chapters and eight moments on the crafts we work on, then a record of how we check our own claims. Every number comes from our own tests.</p>\n'
         '  <p class="backrow"><a class="pagebtn ghost" href="#">Back to Part I</a></p>\n</header>')
t = t[:j] + hero2 + t[j:]

# tag Part I chapters, coda, and image sources; Part II chapters and proof
for k in range(1, 11):
    once(f'<section class="part vert" id="part{k}">' if f'<section class="part vert" id="part{k}">' in t else f'<section class="part horz" id="part{k}">',
         (f'<section class="part vert" id="part{k}" data-page="1">' if f'<section class="part vert" id="part{k}">' in t else f'<section class="part horz" id="part{k}" data-page="1">'))
once('<section class="coda" id="coda">', '<section class="coda" id="coda" data-page="1">')
for k, kind in ((11, 'vert'), (12, 'horz'), (13, 'vert'), (14, 'vert')):
    once(f'<section class="part {kind}" id="p2part{k}">', f'<section class="part {kind}" id="p2part{k}" data-page="2">')
once('<section class="endnote">', '<section class="endnote" data-page="1">')
once('<section class="proof" id="proof" aria-labelledby="proofh">', '<section class="proof" id="proof" aria-labelledby="proofh" data-page="2">')
once('<p class="pnote">The full research report, with its data and code, is available from Pulp.</p>',
     '<p class="pnote">The full research report, with its data and code, is available from Pulp.</p>\n<p class="backrow"><a class="pagebtn ghost" href="#">Back to Part I</a></p>')
# the old Part II divider is replaced by Part II's own hero
t, n = re.subn(r'<section class="p2div" id="partII".*?</section>\n?', '', t, count=1, flags=re.S); assert n == 1

# Part I ends with an introduction to Part II and a button
nextpart = '''<section class="nextpart" data-page="1" aria-labelledby="nph">
<p class="pnum">Next, Part II</p>
<h2 id="nph">What to keep, what to spend</h2>
<p class="np-lede">Part I ends with machines that remember almost everything and spend energy every time they answer. Part II is Pulp's contribution: reading what people write and say with less memory, less compute, and more care.</p>
<div class="np-grid">
<div><h3>What to expect</h3><ul>
<li>Reading: why a few dozen shapes cover almost every request, and what a machine should remember.</li>
<li>Measuring: how a message moves the person who receives it, and the electricity it takes to read it.</li>
<li>Making: Thinkwell for conversations and typodojo for letters.</li>
<li>A live reader you can try, and a record of how we check our own claims.</li></ul></div>
<div><h3>What we did</h3><ul>
<li>Collected 11,508 requests from 44 public collections and our own simulations, from voice commands to parliamentary hearings.</li>
<li>Wrote down 31 predictions before testing them. 19 were met, 3 partly met, and 9 were not, and all of them are published.</li>
<li>Rebuilt our research from public files with one script and matched every result exactly.</li></ul></div>
</div>
<a class="pagebtn" href="#part-ii">Read Part II</a>
</section>
'''
once('</section>\n<section class="part vert" id="p2part11"', '</section>\n' + nextpart + '<section class="part vert" id="p2part11"')

# a small script runs first: keep only this page's elements, renumber Part II from 1, reload on page change
pre = '''<script>
(function(){
  var P2 = location.hash === '#part-ii'; window.__P2 = P2;
  try { history.scrollRestoration = 'manual'; } catch (e) {}
  document.querySelectorAll('[data-page]').forEach(function(el){ if (el.getAttribute('data-page') !== (P2 ? '2' : '1')) el.remove(); });
  if (P2) document.querySelectorAll('.beat[data-i]').forEach(function(b){ b.setAttribute('data-i', String(+b.getAttribute('data-i') - 34)); });
  document.title = P2 ? 'From Stone to Screen, Part II' : 'From Stone to Screen';
  addEventListener('hashchange', function(){ location.reload(); });
  window.scrollTo(0, 0);
})();
</script>
<script>
(function(){'''
once('<script>\n(function(){', pre)

# the main script works on this page's range only
once('var N = KEYS.length;', '''var P2 = !!window.__P2, LO = P2 ? 34 : 0, HI = P2 ? 42 : 34;
KEYS = KEYS.slice(LO, HI); TITLES = TITLES.slice(LO, HI); DATES = DATES.slice(LO, HI); INNOV = INNOV.slice(LO, HI);
PARTS = P2 ? PARTS.slice(10) : PARTS.slice(0, 10);
var N = KEYS.length;
document.getElementById('track').setAttribute('aria-valuemax', N);''')
once('if (pi === 10) {', 'if (false) {')
once("if (pi === 0 || pi === 10) { var s = document.createElement('p'); s.className = 'cgsep'; s.textContent = pi === 0 ? 'Part I' : 'Part II'; g.appendChild(s); }",
     "if (pi === 0) { var s = document.createElement('p'); s.className = 'cgsep'; s.textContent = P2 ? 'Part II' : 'Part I'; g.appendChild(s); }")
once("ICONS[pi] + '</g></svg>'", "ICONS[pi + (P2 ? 10 : 0)] + '</g></svg>'")
once("function num(pi){ return String(pi + 1).padStart(2, '0'); }", "function num(pi){ return String(pi + 1 + (P2 ? 10 : 0)).padStart(2, '0'); }")

CSS = '''
/* v5: pages */
.nextpart{border-top:1px solid var(--line); padding-block:52px 60px}
.nextpart h2{font-size:clamp(1.9rem,4.6vw,2.8rem); line-height:1.05; letter-spacing:-0.02em; margin:0 0 14px; font-weight:800}
.np-lede{font-size:1.05rem; max-width:36rem; margin:0 0 22px}
.np-grid{display:grid; grid-template-columns:1fr; gap:4px 28px; margin:0 0 26px}
@media (min-width:640px){ .np-grid{grid-template-columns:1fr 1fr} }
.np-grid h3{font-size:1rem; margin:0 0 6px}
.np-grid ul{margin:0 0 14px; padding-left:18px; font-size:.92rem}
.np-grid li{margin-bottom:6px}
.pagebtn{display:inline-flex; align-items:center; justify-content:center; min-height:48px; padding:12px 26px; border-radius:999px; background:var(--btn-bg); color:var(--btn-fg); border:1px solid var(--btn-bg); font-weight:600; font-size:.95rem; text-decoration:none}
.pagebtn.ghost{background:transparent; color:var(--fg); border-color:var(--fg); min-height:44px; padding:10px 20px; font-size:.85rem}
.pagebtn:focus-visible{outline:2px solid var(--fg); outline-offset:3px}
@media (hover:hover) and (pointer:fine){ .pagebtn:hover{opacity:.88} }
.backrow{margin:22px 0 0}
'''
once('html{scroll-behavior:smooth}\n', 'html{scroll-behavior:smooth}\n' + CSS)
open(OUT, 'w', encoding='utf8').write(t)
print('written', round(len(t) / 1e6, 2), 'MB; em dash:', '\u2014' in re.sub(r'src="data:[^"]+"', '', t))
