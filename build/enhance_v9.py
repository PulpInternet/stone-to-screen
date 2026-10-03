"""v9: the speech bubble shows only while the bar is hovered (or briefly on touch); slimmer bar at rest."""
SRC = '/mnt/user-data/outputs/From_Stone_to_Screen_v8.html'
OUT = '/mnt/user-data/outputs/From_Stone_to_Screen_v9.html'
t = open(SRC, encoding='utf8').read()
CSS = '''
/* v9: no speech bubble at rest; the disc stays */
#tbar:not(.xp) #bubble, #tbar:not(.xp) #btip{opacity:0; transition:none}
#tbar.xp #bubble, #tbar.xp #btip{opacity:1}
.tocwrap{padding-bottom:4px}
#tbar.xp #tbarx{height:22px}
#vtl{top:calc(96px + env(safe-area-inset-top,0px))}
'''
last = t.rfind('</style>'); t = t[:last] + CSS + t[last:]
open(OUT, 'w', encoding='utf8').write(t)
print('written', round(len(t) / 1e6, 2), 'MB')
