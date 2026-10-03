"""v6: scroll timeline on the left; photos 15% smaller."""
SRC = '/mnt/user-data/outputs/From_Stone_to_Screen_v5.html'
OUT = '/mnt/user-data/outputs/From_Stone_to_Screen_v6.html'
t = open(SRC, encoding='utf8').read()
def once(a, b):
    global t
    assert t.count(a) == 1, a[:80]
    t = t.replace(a, b)
once('width:min(100%, calc(58vh * var(--w) / var(--h)))}', 'width:min(85%, calc(49.3vh * var(--w) / var(--h)))}')
once('.card figure img{width:min(100%, calc(30vh * var(--w) / var(--h)))}', '.card figure img{width:min(85%, calc(25.5vh * var(--w) / var(--h)))}')
CSS = '''
/* v6: the scroll timeline sits on the left, where reading starts */
#vtl{right:auto; left:max(2px, calc((100vw - 680px) / 2 - 76px)); transform:translateX(-8px)}
#vtl.show{transform:none}
#vlabel{left:46px; right:auto}
@media (min-width:1100px){ #vlabel{left:auto; right:46px} }
@media (max-width:859px){
  #vtl{left:2px; right:auto}
  #track .rail,#track .fill{left:7px}
  #track .tick{left:5px; width:6px}
  #track .tick.era{left:3px; width:10px}
  #track .cursor{left:8px}
  #vlabel{left:22px; right:auto}
}
@media (prefers-reduced-motion:reduce){ #vtl{transform:none} }
'''
import re
last = t.rfind('</style>'); assert last > 0
t = t[:last] + CSS + t[last:]
# decide the page before the first paint, so the other page's elements never render
first_style = t.find('<style>'); assert first_style > 0
t = t[:first_style] + '<script>document.documentElement.setAttribute("data-page", location.hash === "#part-ii" ? "2" : "1");</script>\n' + t[first_style:]
last = t.rfind('</style>')
t = t[:last] + 'html[data-page="1"] [data-page="2"], html[data-page="2"] [data-page="1"]{display:none !important}\n' + t[last:]
open(OUT, 'w', encoding='utf8').write(t)
print('written', round(len(t) / 1e6, 2), 'MB')
