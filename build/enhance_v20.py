# enhance_v20.py  (run after enhance_v19.py, then enhance_v15.py last)
# 1. Reading focus: the one section that holds the reading line gets a light tint.
#    A tall section keeps it until the next section reaches the line, so the tint never
#    flickers off in the gaps. One section at a time.
# 2. The Light, Dark, Mono switch moves out of each hero into the top bar's left corner, as
#    icons. On phones it is one button that cycles through the three.
import sys, re
SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding="utf-8").read()

old = re.findall(r'\s*<div id="modes" role="group" aria-label="Color mode">.*?</div>', s, flags=re.S)
assert len(old) == 3, len(old)
for o in old: s = s.replace(o, "", 1)

SUN = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.5M12 19v2.5M2.5 12H5M19 12h2.5M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M5.3 18.7l1.8-1.8M16.9 7.1l1.8-1.8"/></svg>'
MOON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>'
MONO = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M12 3.5v17a8.5 8.5 0 0 0 0-17z" class="fill"/></svg>'
MODES = ('<div id="modes" role="group" aria-label="Color mode">'
         f'<button type="button" data-m="light" aria-pressed="false" aria-label="Light mode" title="Light">{SUN}</button>'
         f'<button type="button" data-m="dark" aria-pressed="false" aria-label="Dark mode" title="Dark">{MOON}</button>'
         f'<button type="button" data-m="mono" aria-pressed="false" aria-label="Mono mode" title="Mono">{MONO}</button></div>')
a = '<nav id="tbar" aria-label="Chapters">\n  <div class="inner">'
assert s.count(a) == 1
s = s.replace(a, a + "\n    " + MODES, 1)

CSS = r"""<style>
/* v20: reading focus tint, and the mode switch as icons in the top bar */
:root{--z-float:55; --focus-bg:color-mix(in srgb, var(--fg) 4%, var(--bg)); --focus-t:.45s}
.hero, .part{transition:background-color var(--focus-t) ease, box-shadow var(--focus-t) ease}
.hero.is-main, .part.is-main{background-color:var(--focus-bg); box-shadow:0 0 0 100vmax var(--focus-bg); clip-path:inset(0 -100vmax)}
@media (prefers-reduced-motion:reduce){ :root{--focus-t:.12s} }
@media (forced-colors:active){ .hero.is-main, .part.is-main{box-shadow:none} }

#modes{position:fixed; z-index:var(--z-float); top:calc(env(safe-area-inset-top,0px) + 10px); left:max(var(--frame-pad), env(safe-area-inset-left,0px)); right:auto;
  display:flex; gap:0; border:1px solid var(--line); border-radius:999px; overflow:hidden; height:calc(var(--tap) + 2px); background:var(--bg)}
#modes button{display:grid; place-items:center; width:var(--tap); min-height:0; height:100%; padding:0; background:var(--bg); color:var(--mut)}
#modes button svg{width:18px; height:18px; fill:none; stroke:currentColor; stroke-width:1.7; stroke-linecap:round; stroke-linejoin:round}
#modes button svg .fill{fill:currentColor; stroke:none}
#modes button[aria-pressed="true"]{background:var(--btn-bg); color:var(--btn-fg)}
@media (hover:hover){ #modes button:hover{color:var(--fg)} #modes button[aria-pressed="true"]:hover{color:var(--btn-fg)} }

/* phones: one button that cycles, showing the mode in use */
@media (max-width:859px){
  #modes{border-radius:50%; width:calc(var(--tap) + 2px)}
  #modes button{display:none}
  #modes button[aria-pressed="true"]{display:grid}
  #modes:not(:has([aria-pressed="true"])) button[data-m="light"]{display:grid}
}
@media (max-width:859px) and (prefers-color-scheme:dark){
  #modes:not(:has([aria-pressed="true"])) button[data-m="light"]{display:none}
  #modes:not(:has([aria-pressed="true"])) button[data-m="dark"]{display:grid}
}
</style>"""

JS = r"""<script>
/* v20: reading focus and the phone mode cycle */
(function(){
  var cands = [].slice.call(document.querySelectorAll('.hero, .part')).filter(function(e){ return e.offsetParent !== null || e.getClientRects().length; });
  var main = null, ticking = false;
  function pick(){
    ticking = false;
    var line = innerHeight * 0.42, hit = null;
    for (var i = 0; i < cands.length; i++){
      var r = cands[i].getBoundingClientRect();
      if (r.top <= line && r.bottom > line){ hit = cands[i]; break; }
    }
    if (hit && hit !== main){ if (main) main.classList.remove('is-main'); hit.classList.add('is-main'); main = hit; }
  }
  addEventListener('scroll', function(){ if (!ticking){ ticking = true; requestAnimationFrame(pick); } }, {passive:true});
  addEventListener('resize', pick); pick();

  var modes = document.getElementById('modes'), order = ['light', 'dark', 'mono'], passing = false;
  if (!modes) return;
  modes.addEventListener('click', function(ev){
    if (passing || !matchMedia('(max-width:859px)').matches) return;
    var b = ev.target.closest('button'); if (!b) return;
    ev.stopPropagation(); ev.preventDefault();
    var next = order[(order.indexOf(b.dataset.m) + 1) % 3];
    passing = true; modes.querySelector('[data-m="' + next + '"]').click(); passing = false;
    var nb = modes.querySelector('[data-m="' + next + '"]'); if (nb) nb.focus({preventScroll:true});
  }, true);
})();
</script>"""
s = s.replace("</body>", CSS + JS + "</body>", 1)
open(OUT, "w", encoding="utf-8").write(s)
print("wrote", OUT)
