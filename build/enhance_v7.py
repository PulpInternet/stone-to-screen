"""v7: centered chapter bar from Antiquity to Today, yellow accent on the current chapter, and a speech bubble under it."""
import re
SRC = '/mnt/user-data/outputs/From_Stone_to_Screen_v6.html'
OUT = '/mnt/user-data/outputs/From_Stone_to_Screen_v7.html'
t = open(SRC, encoding='utf8').read()
def once(a, b):
    global t
    assert t.count(a) == 1, a[:90]
    t = t.replace(a, b)
old_inner = re.search(r'<nav id="tbar" aria-label="Chapters">\n  <div class="inner">.*?\n  </div>\n</nav>', t, re.S).group(0)
new_nav = '''<nav id="tbar" aria-label="Chapters">
  <div class="inner">
    <div class="tocwrap">
      <span class="tend tl">Antiquity</span>
      <div id="toc" role="group" aria-label="Chapters"></div>
      <button id="tocmini" type="button" aria-label="Open the chapter list"><span class="minirow" aria-hidden="true"></span></button>
      <span class="tend tr">Today</span>
      <span class="tocline" aria-hidden="true"></span>
      <div id="bubble" aria-hidden="true"><span class="btx"></span></div><i id="btip" aria-hidden="true"></i>
    </div>
    <div class="tocright"><span id="tnum">01 / 34</span><span id="tlabel">Marks</span><button id="jump" type="button">Index</button></div>
  </div>
</nav>'''
t = t.replace(old_inner, new_nav, 1)

JS = r'''
/* v7: end labels, yellow accent, and the speech bubble under the current chapter */
document.querySelector('.tend.tl').textContent = P2 ? 'Research' : 'Antiquity';
document.querySelector('.tend.tr').textContent = P2 ? 'Your turn' : 'Today';
var bubble = document.getElementById('bubble'), btx = bubble.querySelector('.btx'), btip = document.getElementById('btip'), wrapEl = document.querySelector('.tocwrap');
var bLeft = null, bPi = -1, fadeT = null;
var measure = document.createElement('span'); measure.className = 'btx'; measure.style.cssText = 'position:absolute; visibility:hidden; white-space:nowrap; left:-9999px'; bubble.appendChild(measure);
function iconFor(pi){
  var big = toc.querySelectorAll('.tocb')[pi], small = mini.querySelectorAll('.mi')[pi];
  return (big && big.getBoundingClientRect().width) ? big : small;
}
function placeBubble(pi, instant){
  var ic = iconFor(pi); if (!ic) return;
  var wr = wrapEl.getBoundingClientRect(), r = ic.getBoundingClientRect();
  var cx = r.left + r.width / 2 - wr.left;
  measure.textContent = PARTS[pi].t;
  var bw = Math.ceil(measure.getBoundingClientRect().width) + 22, edge = 14;
  bw = Math.min(bw, wr.width);
  var left = bLeft === null ? cx - bw / 2 : bLeft;
  left = Math.min(Math.max(left, cx - bw + edge), cx - edge);
  left = Math.min(Math.max(left, 0), wr.width - bw);
  if (instant) { bubble.classList.add('noanim'); btip.classList.add('noanim'); }
  bubble.style.width = bw + 'px'; bubble.style.transform = 'translateX(' + left + 'px)'; btip.style.left = cx + 'px';
  if (pi !== bPi) {
    if (bPi < 0 || instant) btx.textContent = PARTS[pi].t;
    else { btx.classList.add('out'); clearTimeout(fadeT); fadeT = setTimeout(function(){ btx.textContent = PARTS[pi].t; btx.classList.remove('out'); }, 140); }
    bPi = pi;
  }
  bLeft = left;
  if (instant) { bubble.getBoundingClientRect(); bubble.classList.remove('noanim'); btip.classList.remove('noanim'); }
}
var _tocUpdate = tocUpdate; tocUpdate = function(i){ _tocUpdate(i); placeBubble(PARTOF[i], false); };
placeBubble(PARTOF[active < 0 ? 0 : active], true);
wrapEl.classList.add('ready');
addEventListener('resize', function(){ bLeft = null; placeBubble(PARTOF[active < 0 ? 0 : active], true); });
'''
last = t.rfind('})();'); t = t[:last] + JS + t[last:]

CSS = '''
/* v7: centered chapter bar, yellow accent, speech bubble */
#tbar{padding-block:8px 6px}
#tbar .inner{max-width:1100px; display:grid; grid-template-columns:1fr auto 1fr; align-items:start; gap:10px}
.tocwrap.ready{visibility:visible}
.tocwrap{visibility:hidden; grid-column:2; position:relative; display:flex; align-items:center; gap:8px; padding-bottom:34px}
.tocright{grid-column:3; justify-self:end; display:flex; align-items:center; gap:10px; height:44px}
#tnum{margin-left:0}
.tend{position:relative; z-index:1; background:var(--bg); padding:0 6px; font-size:.68rem; font-weight:600; text-transform:uppercase; letter-spacing:.12em; color:var(--mut); white-space:nowrap}
.tocline{position:absolute; z-index:0; left:0; right:0; top:22px; height:1px; background:var(--line)}
#toc, #tocmini{position:relative; z-index:1}
#toc{gap:4px}
.tocb{background:var(--bg); transition:opacity .25s ease, background-color .25s ease, color .25s ease}
.tocb{border-radius:50%}
.tocb.on{background:var(--yellow); color:#161716; opacity:1}
.tocb svg{width:21px; height:21px}
#tocmini{background:transparent; height:44px}
.minirow{background:var(--bg); padding:0 4px; gap:4px}
.mi{width:18px; height:18px; border-radius:50%; transition:opacity .25s ease, background-color .25s ease, color .25s ease}
.mi svg{width:12px; height:12px}
.mi.on{background:var(--yellow); color:#161716; opacity:1}
.mdiv,.tocdiv{display:none}
#bubble{position:absolute; z-index:2; left:0; top:48px; height:24px; transform:translateX(0); background:var(--yellow); color:#161716; border-radius:999px; display:flex; align-items:center; justify-content:center; pointer-events:none;
  transition:transform .46s cubic-bezier(.2,.8,.2,1) .12s, width .46s cubic-bezier(.2,.8,.2,1) .12s}
#bubble .btx{font-size:.72rem; font-weight:600; letter-spacing:.01em; white-space:nowrap; padding:0 11px; transition:opacity .14s ease}
#bubble .btx.out{opacity:0}
#btip{position:absolute; z-index:3; top:43px; left:0; width:0; height:0; border-left:5px solid transparent; border-right:5px solid transparent; border-bottom:6px solid var(--yellow); transform:translateX(-50%); transition:left .3s cubic-bezier(.2,.8,.2,1)}
#bubble.noanim, #btip.noanim{transition:none}
@media (max-width:859px){
  .tocwrap{gap:4px}
  .tend{font-size:.6rem; letter-spacing:.08em; padding:0 3px}
  #tnum{display:none}
  #tbar .inner{display:flex; justify-content:center}
  .tocright{display:none}
}
@media (max-width:420px){ .tend{font-size:.56rem; letter-spacing:.04em; padding:0 2px} .minirow{gap:2px; padding:0 2px} .mi{width:15px; height:15px} .mi svg{width:11px; height:11px} .tocwrap{gap:3px} }
@media (prefers-reduced-motion:reduce){ #bubble, #btip{transition:none} #bubble .btx{transition:opacity .12s ease} }
#vtl{top:calc(108px + env(safe-area-inset-top,0px))}
'''
last = t.rfind('</style>'); t = t[:last] + CSS + t[last:]
open(OUT, 'w', encoding='utf8').write(t)
print('written', round(len(t) / 1e6, 2), 'MB')
