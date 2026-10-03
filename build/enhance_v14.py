# enhance_v14.py  (run after enhance_v13.py)
# Part II is all Hannah green. Damani cyan is kept for water only (the drops in the energy chart).
import sys
SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding="utf-8").read()
s = s.replace("Cyan bars are requests; gray bars are meeting turns.", "Green bars are requests; gray bars are meeting turns.")
s = s.replace('<span><i style="background:var(--aqua)"></i>Requests</span>', '<span><i style="background:var(--sus)"></i>Requests</span>')
CSS = r"""<style>
/* v14: Hannah green throughout Part II; cyan only for water */
[data-page="2"] .vbar i{background:var(--sus)}
[data-page="2"] .vbar i.m{background:var(--mut); opacity:.55}
[data-page="2"] .dots i{background:var(--sus)}
#proof .pr .st.ms::before{background:var(--sus)}
#proof .pr .st.ip::before{background:var(--fg)}
</style>"""
s = s.replace("</body>", CSS + "</body>", 1)
open(OUT, "w", encoding="utf-8").write(s)
print("wrote", OUT, "| aqua uses left:", s.count("var(--aqua)"))
