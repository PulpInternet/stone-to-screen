# enhance_v12.py  (run after enhance_v11.py)
# Carries the research palette through every Part II chart, not just the energy card:
# Damani cyan marks measured results (bars, the 48-scale grid, "Measured" in the record);
# Hannah green marks efficiency and sustainability (power, the rules-first result, savings).
# Comparison series (meeting turns, rules alone) stay gray. Mono mode stays gray throughout.
import sys
SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding="utf-8").read()
def sub1(old, new):
    global s
    assert old in s, "missing: " + old[:80]
    s = s.replace(old, new, 1)
# rules alone is the baseline; the second layer is the efficiency result
sub1('aria-label="Rules alone: 44%"><i class=""', 'aria-label="Rules alone: 44%"><i class="m"')
sub1('aria-label="With the second layer: 64%"><i class=""', 'aria-label="With the second layer: 64%"><i class="g"')
CSS = r"""<style>
/* v12: research palette across Part II */
[data-page="2"] .vbar i{background:var(--aqua)}
[data-page="2"] .vbar i.m{background:var(--mut); opacity:.55}
[data-page="2"] .vbar i.g{background:var(--sus)}
[data-page="2"] .vbar{background:color-mix(in srgb, var(--line) 70%, transparent)}
[data-page="2"] .dots i{background:var(--aqua)}
[data-page="2"] .dots i.e{background:transparent; border-color:var(--mut)}
#proof .pr .st{display:inline-flex; align-items:center; gap:7px}
#proof .pr .st::before{content:""; width:9px; height:9px; border-radius:50%; background:var(--fg)}
#proof .pr .st.ms::before{background:var(--aqua)}
#proof .pr .st.ip::before{background:var(--sus)}
#proof .pr .st.pm::before{background:transparent; border:1.5px solid var(--mut); width:6px; height:6px}
.vleg{display:flex; flex-wrap:wrap; gap:6px 16px; font-size:.74rem; color:var(--mut); margin:0 0 6px}
.vleg span{display:inline-flex; align-items:center; gap:6px}
.vleg i{width:14px; height:8px; display:inline-block}
@media (forced-colors:active){ [data-page="2"] .vbar i, [data-page="2"] .dots i{background:CanvasText} }
</style>
<script>
(function(){
document.querySelectorAll('#proof .pr .st').forEach(function(el){
  var t = el.textContent.trim();
  el.classList.add(t === 'Measured' ? 'ms' : t === 'In the product' ? 'ip' : 'pm');
});
var th = document.querySelector('#p2thinking .viz');
if (th){ var l = document.createElement('p'); l.className = 'vleg';
  l.innerHTML = '<span><i style="background:var(--aqua)"></i>Requests</span><span><i style="background:var(--mut);opacity:.55"></i>Meeting turns</span>';
  th.insertBefore(l, th.firstChild); }
var rf = document.querySelector('#p2rules .viz');
if (rf){ var l2 = document.createElement('p'); l2.className = 'vleg';
  l2.innerHTML = '<span><i style="background:var(--mut);opacity:.55"></i>Rules alone</span><span><i style="background:var(--sus)"></i>With the second layer</span>';
  rf.insertBefore(l2, rf.firstChild); }
})();
</script>"""
s = s.replace("Dark bars are requests; gray bars are meeting turns.", "Cyan bars are requests; gray bars are meeting turns.")
s = s.replace("</body>", CSS + "</body>", 1)
open(OUT, "w", encoding="utf-8").write(s)
print("wrote", OUT)
