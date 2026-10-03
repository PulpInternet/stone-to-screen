"""v8: smaller accent disc, centered bubble, hover previews, collapse on leave, phone flashes, Part I and Part II links in the bottom bar."""
SRC = '/mnt/user-data/outputs/From_Stone_to_Screen_v7.html'
OUT = '/mnt/user-data/outputs/From_Stone_to_Screen_v8.html'
t = open(SRC, encoding='utf8').read()
def once(a, b):
    global t
    assert t.count(a) == 1, a[:90]
    t = t.replace(a, b)

# ghost bubble for hover previews, and the strip that slides out under the bar
once('<i id="btip" aria-hidden="true"></i>', '<i id="btip" aria-hidden="true"></i><div id="gbubble" aria-hidden="true"><span class="btx"></span></div><i id="gtip" aria-hidden="true"></i>')
once('</div>\n</nav>\n<div id="vtl">', '</div>\n  <span id="tbarx" aria-hidden="true"></span>\n</nav>\n<div id="vtl">')
# bottom bar: Part I left, New here center, Part II right
once('<div id="bbar"><button id="bbtn" type="button" aria-haspopup="dialog">',
     '<div id="bbar"><a class="plink p1" href="#"><span class="pk">Part I</span><span class="pt">: From Stone to Screen</span></a><button id="bbtn" type="button" aria-haspopup="dialog">')
once('<span class="more" aria-hidden="true">+</span>\n</button></div>',
     '<span class="more" aria-hidden="true">+</span>\n</button><a class="plink p2" href="#part-ii"><span class="pk">Part II</span><span class="pt">: What to keep, what to spend</span></a></div>')

JS = r'''
/* v8: bubble states, hover previews, phone flashes, page links */
var tbar = document.getElementById('tbar'), gb = document.getElementById('gbubble'), gbtx = gb.querySelector('.btx'), gtip = document.getElementById('gtip');
var expanded = false, hoverPi = -1, flashT = null, snapT = null;
var REST_W = 18;
function bubbleW(text){ measure.textContent = text; return Math.ceil(measure.getBoundingClientRect().width) + 22; }
function centerOn(el, tipEl, pi, w){
  var ic = iconFor(pi); if (!ic) return;
  var wr = wrapEl.getBoundingClientRect(), r = ic.getBoundingClientRect(), cx = r.left + r.width / 2 - wr.left;
  var left = Math.min(Math.max(cx - w / 2, 0), wr.width - w);
  el.style.width = w + 'px'; el.style.transform = 'translateX(' + left + 'px)'; tipEl.style.left = cx + 'px';
}
function snap(){ [bubble, btip, gb, gtip].forEach(function(e){ e.classList.add('snap'); }); clearTimeout(snapT); snapT = setTimeout(function(){ [bubble, btip, gb, gtip].forEach(function(e){ e.classList.remove('snap'); }); }, 130); }
placeBubble = function(pi, instant){
  if (instant) { bubble.classList.add('noanim'); btip.classList.add('noanim'); }
  var showText = expanded && (hoverPi < 0 || hoverPi === pi);
  if (pi !== bPi) {
    if (bPi < 0 || instant || !showText) btx.textContent = PARTS[pi].t;
    else { btx.classList.add('out'); clearTimeout(fadeT); fadeT = setTimeout(function(){ btx.textContent = PARTS[pi].t; btx.classList.remove('out'); }, 140); }
    bPi = pi;
  }
  bubble.classList.toggle('tx', showText);
  centerOn(bubble, btip, pi, showText ? bubbleW(PARTS[pi].t) : REST_W);
  var ghost = expanded && hoverPi >= 0 && hoverPi !== pi;
  gb.classList.toggle('on', ghost); gtip.classList.toggle('on', ghost);
  if (ghost) { gbtx.textContent = PARTS[hoverPi].t; centerOn(gb, gtip, hoverPi, bubbleW(PARTS[hoverPi].t)); }
  if (instant) { bubble.getBoundingClientRect(); bubble.classList.remove('noanim'); btip.classList.remove('noanim'); }
};
function render(){ placeBubble(PARTOF[active < 0 ? 0 : active], false); }
function setExpanded(v){
  if (v === expanded) return;
  expanded = v; tbar.classList.toggle('xp', v); snap();
  if (!v) { hoverPi = -1; bubble.classList.remove('tx'); gb.classList.remove('on'); gtip.classList.remove('on'); }
  render();
}
var canHover = matchMedia('(hover: hover) and (pointer: fine)').matches;
if (canHover) {
  tbar.addEventListener('pointerenter', function(){ setExpanded(true); });
  tbar.addEventListener('pointerleave', function(){ setExpanded(false); });
}
toc.querySelectorAll('.tocb').forEach(function(btn, k){
  btn.addEventListener('pointerenter', function(){ if (!canHover) return; hoverPi = k; setExpanded(true); render(); });
  btn.addEventListener('focus', function(){ hoverPi = k; setExpanded(true); render(); });
  btn.addEventListener('blur', function(){ hoverPi = -1; if (!tbar.matches(':hover')) setExpanded(false); else render(); });
});
toc.addEventListener('pointerleave', function(){ hoverPi = -1; render(); });
/* phones and tablets: show the name briefly on each chapter change */
var lastPi = PARTOF[active < 0 ? 0 : active];
var _tocUpdate2 = tocUpdate; tocUpdate = function(i){
  _tocUpdate2(i);
  var pi = PARTOF[i];
  if (!canHover && pi !== lastPi) { setExpanded(true); clearTimeout(flashT); flashT = setTimeout(function(){ setExpanded(false); }, 2400); }
  lastPi = pi;
};
render();
/* page links in the bottom bar */
document.querySelectorAll('.plink').forEach(function(a){
  var mine = a.classList.contains(P2 ? 'p2' : 'p1');
  if (mine) { a.setAttribute('aria-current', 'page'); a.addEventListener('click', function(e){ e.preventDefault(); window.scrollTo({top: 0, behavior: reduced ? 'auto' : 'smooth'}); }); }
});
'''
last = t.rfind('})();'); t = t[:last] + JS + t[last:]

CSS = '''
/* v8: smaller disc, bubble states, hover previews */
.tocb{position:relative}
.tocb.on{background:transparent}
.tocb::before{content:""; position:absolute; left:6px; top:6px; right:6px; bottom:6px; border-radius:50%; background:var(--yellow); opacity:0; transition:opacity .25s ease}
.tocb.on::before{opacity:1}
.tocb svg{position:relative; z-index:1; width:19px; height:19px}
.tocwrap{padding-bottom:16px}
#btip,#gtip{top:41px}
#bubble{top:46px; height:10px; transition:transform .46s cubic-bezier(.2,.8,.2,1) .12s, width .46s cubic-bezier(.2,.8,.2,1) .12s, height .099s ease}
#bubble .btx{opacity:0; transition:none}
#bubble.tx{height:24px}
#bubble.tx .btx{opacity:1; transition:opacity .14s ease}
#bubble.tx .btx.out{opacity:0}
#gbubble{position:absolute; z-index:2; left:0; top:46px; height:24px; border-radius:999px; background:var(--yellow); color:#161716; opacity:0; display:flex; align-items:center; justify-content:center; pointer-events:none; transition:transform .2s cubic-bezier(.2,.8,.2,1), width .2s cubic-bezier(.2,.8,.2,1), opacity .12s ease}
#gbubble .btx{font-size:.72rem; font-weight:600; white-space:nowrap; padding:0 11px}
#gtip{position:absolute; z-index:3; left:0; width:0; height:0; border-left:5px solid transparent; border-right:5px solid transparent; border-bottom:6px solid var(--yellow); transform:translateX(-50%); opacity:0; transition:left .2s cubic-bezier(.2,.8,.2,1), opacity .12s ease}
#gbubble.on{opacity:.38}
#gtip.on{opacity:.38}
#bubble.snap,#btip.snap,#gbubble.snap,#gtip.snap{transition:height .099s ease, opacity .099s ease}
#tbarx{position:absolute; left:0; right:0; top:100%; height:0; background:var(--bg); border-bottom:1px solid transparent; transition:height .099s ease; pointer-events:none}
#tbar{position:sticky}
#tbar.xp #tbarx{height:16px; border-bottom-color:var(--line)}
#tbar.xp{border-bottom-color:transparent}
@media (prefers-reduced-motion:reduce){ #bubble,#gbubble,#gtip,#tbarx{transition:none} }
/* v8: Part I and Part II links in the bottom bar */
#bbar{display:grid; grid-template-columns:minmax(0,1fr) minmax(0,680px) minmax(0,1fr); align-items:center; column-gap:16px}
#bbtn{max-width:none; grid-column:2}
.plink{display:flex; align-items:center; min-height:44px; min-width:0; color:var(--mut); text-decoration:none; font-size:.8rem; font-weight:600; white-space:nowrap}
.plink.p1{grid-column:1; justify-self:start}
.plink.p2{grid-column:3; justify-self:end}
.plink .pk{color:var(--fg)}
.plink .pt{overflow:hidden; text-overflow:ellipsis; min-width:0}
.plink[aria-current="page"]{color:var(--fg)}
.plink[aria-current="page"] .pk{box-shadow:inset 0 -2px 0 var(--yellow)}
@media (hover:hover) and (pointer:fine){ .plink:hover{color:var(--fg)} }
.plink:focus-visible{outline:2px solid var(--fg); outline-offset:2px}
@media (max-width:1100px){ .plink .pt{display:none} }
@media (max-width:1100px){ #bbar{grid-template-columns:auto minmax(0,1fr) auto; column-gap:12px} #bbtn{max-width:680px; justify-self:center} }
@media (max-width:560px){ #bbar{column-gap:10px} #bbtn .lab{display:none} .plink{font-size:.74rem} }
'''
last = t.rfind('</style>'); t = t[:last] + CSS + t[last:]
open(OUT, 'w', encoding='utf8').write(t)
print('written', round(len(t) / 1e6, 2), 'MB')
