import json
from playwright.sync_api import sync_playwright
BASE = "file:///mnt/user-data/outputs/From_Stone_to_Screen_v9.html"
R = {}; errs = []
STATE = """() => ({title: document.title, scrollY: Math.round(scrollY), hash: location.hash, moments: document.querySelectorAll('#track .tick').length, valuemax: document.getElementById('track').getAttribute('aria-valuemax'),
  pictograms: document.querySelectorAll('.tocb').length, tnum: document.getElementById('tnum').textContent, h1: document.querySelector('h1').textContent,
  has_p1: !!document.getElementById('part1'), has_p2: !!document.getElementById('p2part11'), nextpart: !!document.querySelector('.nextpart'), proof: !!document.getElementById('proof'), sources: !!document.querySelector('.endnote'), explorer: !!document.getElementById('reader'), heroes: document.querySelectorAll('header.hero').length})"""
GATE = r"""() => { const I = [], Rr = e => e.getBoundingClientRect(), hit = (a, b) => !(a.right <= b.left + 1 || b.right <= a.left + 1 || a.bottom <= b.top + 1 || b.bottom <= a.top + 1);
 if (document.documentElement.scrollWidth > innerWidth + 1) I.push('sideways scroll');
 const bar = document.querySelector('#tbar .inner'); if (bar.scrollWidth > bar.clientWidth + 1) I.push('bar overflow');
 document.querySelectorAll('.pagebtn, .tocb, .ex').forEach(b => { const r = Rr(b); if (r.width && (r.height < 44 || r.width < 44)) I.push('small target ' + b.className); });
 document.querySelectorAll('.vh').forEach(h => { if (hit(Rr(h.querySelector('.vn')), Rr(h.querySelector('.vv')))) I.push('chart overlap'); });
 return I; }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1280, 'height': 900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(BASE); pg.wait_for_timeout(500); R['part I'] = pg.evaluate(STATE)
    pg.add_style_tag(content="html{scroll-behavior:auto !important}")
    pg.evaluate("document.querySelector('.nextpart').scrollIntoView()"); pg.wait_for_timeout(300)
    with pg.expect_navigation(): pg.click('.nextpart .pagebtn')
    pg.wait_for_timeout(700); R['part II via button'] = pg.evaluate(STATE)
    pg.add_style_tag(content="html{scroll-behavior:auto !important}")
    jumps = []
    for k in range(4):
        pg.evaluate(f"document.querySelectorAll('.tocb')[{k}].click()")
        last = None
        for _ in range(30):
            pg.wait_for_timeout(120); y = pg.evaluate("scrollY")
            if y == last: break
            last = y
        jumps.append(pg.evaluate("() => document.getElementById('vlabel').textContent + ' | on ' + [...document.querySelectorAll('.tocb')].findIndex(b => b.classList.contains('on'))"))
    R['part II pictogram jumps'] = jumps
    fails = 0
    for k in ['p2shapes', 'p2rules', 'p2thinking', 'p2measure', 'p2energy', 'p2thinkwell', 'p2dojo', 'p2live']:
        for i in range(pg.locator(f'#{k} .chip').count()):
            pg.evaluate(f"document.querySelectorAll('#{k} .chip')[{i}].click()"); pg.wait_for_timeout(30)
            if len(pg.evaluate("() => (document.getElementById('modal') || {}).textContent || ''")) < 40: fails += 1
            pg.keyboard.press('Escape')
    R['part II chip failures'] = fails
    R['part II explorer rows'] = [pg.evaluate(f"(() => {{ document.querySelectorAll('.ex')[{i}].click(); return document.querySelectorAll('.exr dd').length }})()") for i in range(pg.locator('.ex').count())]
    pg.evaluate("document.getElementById('jump').click()"); pg.wait_for_timeout(80); R['part II index entries'] = pg.evaluate("() => document.querySelectorAll('#modal ol li').length"); pg.keyboard.press('Escape')
    pg.evaluate("document.querySelector('#proof .pagebtn').scrollIntoView()"); pg.wait_for_timeout(200)
    with pg.expect_navigation(): pg.click('#proof .pagebtn')
    pg.wait_for_timeout(600); s = pg.evaluate(STATE); R['back via bottom button'] = [s['h1'], s['moments'], s['scrollY']]
    with pg.expect_navigation(): pg.go_back()
    pg.wait_for_timeout(600); s = pg.evaluate(STATE); R['browser back'] = [s['hash'], s['h1'], s['moments']]
    with pg.expect_navigation(): pg.click('header.hero .pagebtn')
    pg.wait_for_timeout(600); s = pg.evaluate(STATE); R['back via top button'] = [s['h1'], s['moments']]
    pg.close()
    issues = {}
    for url, name in ((BASE, 'I'), (BASE + '#part-ii', 'II')):
        for w, h in [(320, 700), (390, 844), (844, 390), (768, 1024), (1440, 900)]:
            q = b.new_page(viewport={'width': w, 'height': h}); q.goto(url); q.wait_for_timeout(300)
            for m in ('light', 'dark', 'mono'):
                q.evaluate(f"document.documentElement.setAttribute('data-pmode','{m}')"); q.wait_for_timeout(40)
                iss = q.evaluate(GATE)
                if iss: issues[f'part {name} {m} {w}'] = sorted(set(iss))
            if w == 390 and name == 'II': q.screenshot(path='p2_page_390.png')
            q.close()
        q = b.new_page(viewport={'width': 390, 'height': 844}); q.goto(url); q.wait_for_timeout(300)
        if name == 'I':
            q.evaluate("document.querySelector('.nextpart').scrollIntoView({block:'start'})"); q.wait_for_timeout(900); q.screenshot(path='p1_next_390.png')
        q.close()
    R['layout gates'] = issues or 'clean'
    b.close()
R['script errors'] = errs
print(json.dumps(R, indent=1))
