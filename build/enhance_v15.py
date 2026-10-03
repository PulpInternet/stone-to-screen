# enhance_v15.py  (run after enhance_v14.py)
# Fresh-version check for GitHub Pages. Pages serves files with a 10-minute cache and we
# cannot change its headers, so the page checks itself: on load it fetches its own URL with a
# unique query (which skips both the browser cache and GitHub's CDN), reads the build id, and,
# if a newer build is live, reloads once onto it. Runs only on github.io; elsewhere it does nothing.
import sys, hashlib, re
SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding="utf-8").read()
# idempotent: remove an earlier copy of this block before adding the new one
s = re.sub(r'<!--fresh-->.*?<!--/fresh-->', '', s, flags=re.S)
s = re.sub(r'<meta name="build-id" content="[0-9a-f]+">.*?<script id="freshcheck">.*?</script>', '', s, count=1, flags=re.S)
BUILD = hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]
HEAD = ('<!--fresh--><meta name="build-id" content="%s">'
        '<meta http-equiv="Cache-Control" content="no-cache, must-revalidate">'
        '<meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="0">'
        '<script id="freshcheck">(function(){'
        'if(!/github\\.io$/.test(location.hostname)||!window.fetch)return;'
        'var mine=document.querySelector(\'meta[name="build-id"]\').content;'
        'fetch(location.pathname+"?fresh="+Date.now(),{cache:"no-store"}).then(function(r){return r.ok?r.text():"";}).then(function(t){'
        'var m=t.match(/<meta name="build-id" content="([0-9a-f]+)"/);'
        'if(!m||m[1]===mine)return;'
        'var q=new URLSearchParams(location.search);if(q.get("v")===m[1])return;'
        'q.set("v",m[1]);location.replace(location.pathname+"?"+q.toString()+location.hash);'
        '}).catch(function(){});})();</script><!--/fresh-->') % BUILD
s = s.replace('<meta charset=utf8>', '<meta charset=utf8>' + HEAD, 1) if '<meta charset=utf8>' in s else re.sub(r'(<head[^>]*>)', lambda m: m.group(1) + HEAD, s, count=1)
open(OUT, "w", encoding="utf-8").write(s)
print("wrote", OUT, "build", BUILD)
