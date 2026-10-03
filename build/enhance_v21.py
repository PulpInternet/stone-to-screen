# enhance_v21.py  (run after enhance_v20.py, then enhance_v15.py last)
# The three part links sit together, in order, at the right of the bottom bar.
import sys, re
SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding="utf-8").read()
m = re.search(r'<a class="plink p1"[^>]*>.*?</a>', s, flags=re.S); assert m
p1 = m.group(0); s = s[:m.start()] + s[m.end():]
i = s.find('<span class="pright"'); assert i > 0
j = s.find('>', i) + 1
s = s[:j] + p1 + s[j:]
s = s.replace("</body>", """<style>
/* v21: Part I joins Parts II and III; the links read as one group, in order */
#bbar .pright .plink.p1, #bbar .pright .plink.p2{grid-column:auto; justify-self:auto}
</style></body>""", 1)
open(OUT, "w", encoding="utf-8").write(s); print("wrote", OUT)
