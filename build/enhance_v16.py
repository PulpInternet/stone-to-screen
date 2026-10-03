# enhance_v16.py  (run after enhance_v15.py)
# Layout tokens, and the bars built on them. Both fixed bars share one frame: content sits
# inside --frame (1180 px) with at least --gutter of padding, so nothing pins to the screen
# edges on wide displays and the middle column always lines up with the reading column.
import sys, re
SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding="utf-8").read()
CSS = r"""<style>
/* v16: layout tokens. Every new rule uses these instead of raw numbers. */
:root{
  --col:680px;          /* reading column */
  --frame:1180px;       /* fixed bars and wide furniture */
  --gutter:24px;        /* minimum side padding, 16px on phones */
  --frame-pad:max(var(--gutter), calc((100vw - var(--frame)) / 2));
  --s1:4px; --s2:8px; --s3:12px; --s4:16px; --s5:24px; --s6:32px; --s7:48px;
  --tap:44px;           /* minimum touch target */
  --z-rail:45; --z-bar:50; --z-modal:80;
}
@media (max-width:560px){ :root{--gutter:16px} }
#bbar{padding-left:var(--frame-pad); padding-right:var(--frame-pad); column-gap:var(--s5); z-index:var(--z-bar)}
#bbar .plink{min-height:var(--tap)}
@media (max-width:1100px){ #bbar{column-gap:var(--s4)} }
@media (max-width:560px){ #bbar{column-gap:var(--s3)} }
@media (min-width:1100px){ #tbar{padding-left:var(--frame-pad); padding-right:var(--frame-pad)} }
/* every control reaches --tap; small pills keep their look and get an invisible hit area */
#modes button, #jump, .sbtn, .predbtn{min-height:var(--tap)}
#mclose{width:var(--tap); height:var(--tap)}
.chip{position:relative}
.chip::after{content:""; position:absolute; left:0; right:0; top:min(0px, calc((100% - var(--tap)) / 2)); bottom:min(0px, calc((100% - var(--tap)) / 2))}
.chips{row-gap:var(--s3)}
</style>"""
s = s.replace("</body>", CSS + "</body>", 1)
open(OUT, "w", encoding="utf-8").write(s)
print("wrote", OUT)
