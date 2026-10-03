"""v4: no layout shift from photos, recompressed photos, pictographic chapter bar, vertical timeline that shows on scroll."""
import re, base64, io
from PIL import Image
SRC = '/mnt/user-data/outputs/From_Stone_to_Screen_v3.html'
OUT = '/mnt/user-data/outputs/From_Stone_to_Screen_v4.html'
t = open(SRC, encoding='utf8').read()
before = len(t)

# 1. photos: recompress to WebP at the same pixel size, reserve their space, eager-load the first
count = [0]
def recompress(m):
    fmt, data, rest = m.group(1), m.group(2), m.group(3)
    im = Image.open(io.BytesIO(base64.b64decode(data)))
    if im.mode not in ('L', 'RGB'): im = im.convert('RGB')
    buf = io.BytesIO(); im.save(buf, 'WEBP', quality=74, method=6)
    w = int(re.search(r'width="(\d+)"', rest).group(1)); h = int(re.search(r'height="(\d+)"', rest).group(1))
    count[0] += 1
    rest = rest.replace(' loading="lazy"', ' loading="eager" fetchpriority="high"' if count[0] == 1 else ' loading="lazy"')
    return f'<img src="data:image/webp;base64,{base64.b64encode(buf.getvalue()).decode()}" style="--w:{w};--h:{h}" decoding="async"{rest}>'
t, n = re.subn(r'<img src="data:image/(jpeg);base64,([^"]+)"([^>]*)>', recompress, t); assert n == 32, n
old_img = 'figure img{max-width:100%; width:auto; height:auto; max-height:58vh; display:block; margin-inline:auto; border:1px solid var(--line)}'
assert t.count(old_img) == 1
t = t.replace(old_img, 'figure img{display:block; margin-inline:auto; border:1px solid var(--line); max-width:100%; height:auto; aspect-ratio:var(--w) / var(--h); width:min(100%, calc(58vh * var(--w) / var(--h)))}')
assert t.count('.card figure img{max-height:30vh}') == 1
t = t.replace('.card figure img{max-height:30vh}', '.card figure img{width:min(100%, calc(30vh * var(--w) / var(--h)))}')

# 2. chapter bar replaces the horizontal timeline; the track moves into a vertical timeline
old_nav = re.search(r'<nav id="tbar" aria-label="Timeline">.*?</nav>', t, re.S).group(0)
new_nav = ('<nav id="tbar" aria-label="Chapters">\n  <div class="inner">\n    <div id="toc" role="group" aria-label="Chapters"></div>\n'
  '    <button id="tocmini" type="button" aria-label="Open the chapter list"><span class="minirow" aria-hidden="true"></span></button>\n'
  '    <span id="tnum">01 / 42</span>\n    <span id="tlabel">Marks</span>\n    <button id="jump" type="button">Index</button>\n  </div>\n</nav>\n'
  '<div id="vtl">\n  <div id="track" role="slider" tabindex="0" aria-label="Timeline position" aria-valuemin="1" aria-valuemax="42" aria-valuenow="1" aria-valuetext="Moment 1">\n'
  '    <div class="rail"></div><div class="fill"></div><div class="cursor"></div>\n  </div>\n  <span id="vlabel" aria-hidden="true"></span>\n</div>')
t = t.replace(old_nav, new_nav, 1)
JS_SWAPS = [("t.style.left=(i/(N-1)*100)+'%';", "t.style.top=(i/(N-1)*100)+'%';"),
            ("fill.style.width=p+'%'; cur.style.left=p+'%';", "fill.style.height=p+'%'; cur.style.top=p+'%';"),
            ("var p=Math.min(1,Math.max(0,(clientX-r.left)/r.width));", "var p=Math.min(1,Math.max(0,(clientX-r.top)/r.height));"),
            ("track.addEventListener('click',function(e){ trackPick(e.clientX); });", "track.addEventListener('click',function(e){ trackPick(e.clientY); });")]
for a, b in JS_SWAPS:
    assert t.count(a) == 1, a
    t = t.replace(a, b)

ICONS = ['<path d="M6 5v14M10 5v14M14 5v14M18 5v14M4 16l16-7"/>',
  '<path d="M4 7l6 2.5L4 12zM12 12l6 2.5-6 2.5zM13 5h7M4 18h6"/>',
  '<path d="M8 4h10a2 2 0 0 1 0 4H8M8 4a2 2 0 0 0 0 4v10a2 2 0 0 0 2 2h9V8"/>',
  '<rect x="5" y="12" width="14" height="7" rx="1"/><path d="M12 12V6M9 4h6"/>',
  '<path d="M4 20h16M6 20V9h12v11M12 3v9M9 3h6"/>',
  '<circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/>',
  '<path d="M12 21V12M8.5 8.5a5 5 0 0 1 7 0M5.6 5.6a9 9 0 0 1 12.8 0"/><circle cx="12" cy="11" r="1"/>',
  '<rect x="3" y="6" width="18" height="12" rx="1"/><path d="M7 10h.01M10 14h.01M13 10h.01M16 14h.01M18 10h.01"/>',
  '<path d="M4 19L9 5l5 14M6 14h6M16 8h5M17 12h4M16 16h5"/>',
  '<path d="M6 4l5 15 2.2-6.2L19.5 10z"/>',
  '<path d="M2 12s3.8-6 10-6 10 6 10 6-3.8 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="2.5"/>',
  '<rect x="3" y="8" width="18" height="8" rx="1"/><path d="M7 8v3M11 8v4M15 8v3M19 8v4"/>',
  '<path d="M12 3l5 7-5 11-5-11zM12 10v4"/>',
  '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M9.8 9.5a2.2 2.2 0 1 1 2.9 2.1c-.5.2-.7.6-.7 1.1M12 16h.01"/>']
assert len(ICONS) == 14
import json
JS = r'''
/* Pictographic chapter bar and vertical timeline (v4) */
var ICONS = __ICONS__;
var toc = document.getElementById('toc'), mini = document.querySelector('#tocmini .minirow'), vtl = document.getElementById('vtl'), vlabel = document.getElementById('vlabel');
var firstOf = []; PARTS.forEach(function(p, pi){ for (var j = 0; j < N; j++) if (PARTOF[j] === pi) { firstOf.push(j); break; } });
function svg(pi){ return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' + ICONS[pi] + '</g></svg>'; }
function num(pi){ return String(pi + 1).padStart(2, '0'); }
PARTS.forEach(function(p, pi){
  if (pi === 10) { var d = document.createElement('span'); d.className = 'tocdiv'; d.setAttribute('aria-hidden', 'true'); toc.appendChild(d); var md = document.createElement('span'); md.className = 'mdiv'; mini.appendChild(md); }
  var b = document.createElement('button'); b.type = 'button'; b.className = 'tocb'; b.innerHTML = svg(pi);
  b.setAttribute('aria-label', 'Chapter ' + num(pi) + ': ' + p.t); b.title = p.t;
  b.addEventListener('click', function(){ go(firstOf[pi]); });
  toc.appendChild(b);
  var m = document.createElement('span'); m.className = 'mi'; m.innerHTML = svg(pi); mini.appendChild(m);
});
document.getElementById('tocmini').addEventListener('click', function(){
  openModal(function(m){
    var h = document.createElement('h3'); h.textContent = 'Chapters'; m.appendChild(h);
    var g = document.createElement('div'); g.className = 'cgrid';
    PARTS.forEach(function(p, pi){
      if (pi === 0 || pi === 10) { var s = document.createElement('p'); s.className = 'cgsep'; s.textContent = pi === 0 ? 'Part I' : 'Part II'; g.appendChild(s); }
      var b = document.createElement('button'); b.type = 'button'; b.className = 'cg';
      if (PARTOF[active] === pi) b.setAttribute('aria-current', 'true');
      b.innerHTML = svg(pi); var tx = document.createElement('span'); tx.innerHTML = '<span class="n">' + num(pi) + '</span> '; tx.appendChild(document.createTextNode(p.t)); b.appendChild(tx);
      b.addEventListener('click', function(){ closeModal(); go(firstOf[pi]); });
      g.appendChild(b);
    });
    m.appendChild(g);
    var all = document.createElement('button'); all.type = 'button'; all.className = 'cgall'; all.textContent = 'All ' + N + ' moments';
    all.addEventListener('click', function(){ closeModal(); document.getElementById('jump').click(); });
    m.appendChild(all);
  }, 'Chapters');
});
function tocUpdate(i){
  var pi = PARTOF[i];
  toc.querySelectorAll('.tocb').forEach(function(b, k){ var on = k === pi; b.classList.toggle('on', on); if (on) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current'); });
  mini.querySelectorAll('.mi').forEach(function(s, k){ s.classList.toggle('on', k === pi); });
  document.getElementById('tocmini').setAttribute('aria-label', 'Chapter ' + num(pi) + ': ' + PARTS[pi].t + '. Open the chapter list');
  vlabel.textContent = PARTS[pi].t + ' \u00b7 ' + String(i + 1).padStart(2, '0') + ' / ' + N;
  vlabel.style.top = (i / (N - 1) * 100) + '%';
}
var _setActive = setActive; setActive = function(i){ _setActive(i); tocUpdate(i); };
tocUpdate(active < 0 ? 0 : active);
/* the vertical timeline appears on scroll, hover, or focus, and fades after 5.5 s of stillness */
var hideT = null, holding = false;
function showV(){ vtl.classList.add('show'); clearTimeout(hideT); hideT = setTimeout(function(){ if (!holding) vtl.classList.remove('show'); }, 5500); }
addEventListener('scroll', showV, {passive: true});
document.querySelectorAll('.strip').forEach(function(s){ s.addEventListener('scroll', showV, {passive: true}); });
vtl.addEventListener('pointerenter', function(){ holding = true; vtl.classList.add('show'); });
vtl.addEventListener('pointerleave', function(){ holding = false; showV(); });
track.addEventListener('focus', function(){ holding = true; vtl.classList.add('show'); });
track.addEventListener('blur', function(){ holding = false; showV(); });
'''.replace('__ICONS__', json.dumps(ICONS))
last = t.rfind('})();'); t = t[:last] + JS + t[last:]

CSS = r'''
/* v4: chapter bar */
#tbar .inner{max-width:980px; gap:10px}
#tlabel{display:none !important}
#tnum{margin-left:auto}
#toc{display:none; align-items:center; gap:2px; flex:0 1 auto}
.tocb{width:44px; height:44px; border:0; background:none; color:var(--fg); opacity:.36; cursor:pointer; display:grid; place-items:center; border-radius:8px; padding:0; transition:opacity .12s ease}
.tocb svg{width:22px; height:22px}
.tocb.on{opacity:1}
@media (hover:hover) and (pointer:fine){ .tocb:hover{opacity:.8} .tocb.on:hover{opacity:1} }
.tocb:focus-visible{outline:2px solid var(--fg); outline-offset:-2px; opacity:1}
.tocdiv{width:1px; height:24px; background:var(--line); margin:0 6px; flex:none}
#tocmini{flex:0 1 auto; min-height:44px; min-width:44px; display:flex; align-items:center; border:0; background:none; color:var(--fg); padding:0 4px; cursor:pointer; border-radius:8px}
#tocmini:focus-visible{outline:2px solid var(--fg); outline-offset:2px}
.minirow{display:flex; align-items:center; gap:3px}
.mi{display:grid; place-items:center; opacity:.32; transition:opacity .12s ease}
.mi svg{width:14px; height:14px}
.mi.on{opacity:1}
.mdiv{width:1px; height:12px; background:var(--line); margin:0 3px}
@media (min-width:860px){ #toc{display:flex} #tocmini{display:none} }
@media (max-width:859px){ #jump{display:none} }
@media (max-width:340px){ .mi svg{width:12px; height:12px} .minirow{gap:2px} }
.cgrid{display:grid; grid-template-columns:1fr 1fr; gap:8px; margin:10px 0 14px}
.cgsep{grid-column:1 / -1; font-size:.7rem; text-transform:uppercase; letter-spacing:.12em; font-weight:600; color:var(--mut); margin:6px 0 0}
.cg{display:flex; align-items:center; gap:10px; min-height:52px; padding:8px 12px; border:1px solid var(--line); border-radius:8px; background:var(--bg); color:var(--fg); font:inherit; font-size:.86rem; text-align:left; cursor:pointer}
.cg svg{width:22px; height:22px; flex:none}
.cg .n{color:var(--mut); font-size:.72rem; font-variant-numeric:tabular-nums}
.cg[aria-current="true"]{border-color:var(--fg)}
.cg:focus-visible,.cgall:focus-visible{outline:2px solid var(--fg); outline-offset:2px}
.cgall{font:inherit; font-size:.8rem; font-weight:600; min-height:44px; padding:8px 16px; border:1px solid var(--fg); border-radius:999px; background:var(--bg); color:var(--fg); cursor:pointer}
@media (max-width:360px){ .cgrid{grid-template-columns:1fr} }
/* v4: vertical timeline, visible while scrolling */
#vtl{position:fixed; z-index:45; top:calc(84px + env(safe-area-inset-top,0px)); bottom:calc(84px + env(safe-area-inset-bottom,0px)); right:max(2px, calc((100vw - 680px) / 2 - 76px)); width:44px; opacity:0; pointer-events:none; transform:translateX(8px); transition:opacity .25s ease, transform .25s ease}
#vtl.show{opacity:1; pointer-events:auto; transform:none}
#track{position:absolute; left:0; right:0; top:0; bottom:0; width:44px; height:auto; flex:none; min-width:0}
#track .rail{left:21px; right:auto; top:0; bottom:0; width:2px; height:auto}
#track .fill{left:21px; top:0; width:2px; height:0}
#track .tick{left:17px; width:10px; height:1px; transform:translateY(-50%)}
#track .tick.era{left:14px; width:16px; height:2px}
#track .cursor{left:22px; transform:translate(-50%, -50%); transition:top .2s}
#vlabel{position:absolute; right:46px; transform:translateY(-50%); white-space:nowrap; background:var(--bg); color:var(--fg); border:1px solid var(--line); border-radius:999px; padding:3px 10px; font-size:.72rem; font-weight:600; font-variant-numeric:tabular-nums; pointer-events:none; transition:top .2s}
@media (prefers-reduced-motion:reduce){ #vtl{transform:none; transition:opacity .12s ease} #track .cursor,#vlabel{transition:none} }
@media (min-width:1100px){ #vlabel{right:auto; left:46px} }
@media (max-width:859px){
  #vtl{right:2px}
  #track .rail,#track .fill{left:35px}
  #track .tick{left:33px; width:6px}
  #track .tick.era{left:31px; width:10px}
  #track .cursor{left:36px; width:10px; height:10px; border-width:1px}
  #vlabel{right:24px}
}
'''
t = t.replace('html{scroll-behavior:smooth}\n', 'html{scroll-behavior:smooth}\n' + CSS, 1)
assert CSS in t
open(OUT, 'w', encoding='utf8').write(t)
print(f'{before/1e6:.2f} MB -> {len(t)/1e6:.2f} MB; photos recompressed: {count[0]}; em dash:', '\u2014' in re.sub(r'src="data:[^"]+"', '', t))
