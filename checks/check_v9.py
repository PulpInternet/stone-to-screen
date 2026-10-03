import json
from playwright.sync_api import sync_playwright
base = "file:///mnt/user-data/outputs/From_Stone_to_Screen_v9.html"
R = {}; errs = []
BUB = """() => { const Rr = e => e.getBoundingClientRect(), b = Rr(document.getElementById('bubble')), t = Rr(document.getElementById('btip')), g = Rr(document.getElementById('gbubble')), gt = Rr(document.getElementById('gtip'));
  const on = document.querySelector('.tocb.on'), oc = Rr(on), disc = getComputedStyle(on, '::before');
  return {xp: document.getElementById('tbar').classList.contains('xp'), text_opacity: +getComputedStyle(document.querySelector('#bubble .btx')).opacity, bubble_w: Math.round(b.width), bubble_h: Math.round(b.height),
    centered_on_tip: Math.abs((b.left + b.right) / 2 - (t.left + t.right) / 2) <= 1, tip_on_active: Math.abs((t.left + t.right) / 2 - (oc.left + oc.right) / 2) <= 1,
    ghost: +getComputedStyle(document.getElementById('gbubble')).opacity, ghost_text: document.querySelector('#gbubble .btx').textContent, ghost_centered: Math.abs((g.left + g.right) / 2 - (gt.left + gt.right) / 2) <= 1,
    strip_h: Math.round(Rr(document.getElementById('tbarx')).height), disc: [disc.width, disc.height].join(' x '), first_beat_y: Math.round(Rr(document.querySelector('.beat')).top + scrollY)} }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(base); pg.wait_for_timeout(500); pg.add_style_tag(content="html{scroll-behavior:auto !important}")
    pg.evaluate("document.getElementById('part5').scrollIntoView({block:'start'}); window.scrollBy(0,30)"); pg.wait_for_timeout(900)
    pg.mouse.move(720, 600); pg.wait_for_timeout(300); R['1 at rest'] = pg.evaluate(BUB)
    y0 = pg.evaluate("Math.round(document.getElementById('gutenberg').getBoundingClientRect().top)")
    box = pg.locator('.tocb.on').bounding_box(); pg.mouse.move(box['x'] + 22, box['y'] + 22); pg.wait_for_timeout(700); R['2 hovering the active chapter'] = pg.evaluate(BUB)
    R['2b page content moved when the bar expanded (px)'] = pg.evaluate("Math.round(document.getElementById('gutenberg').getBoundingClientRect().top)") - y0
    other = pg.locator('.tocb').nth(7).bounding_box(); pg.mouse.move(other['x'] + 22, other['y'] + 22); pg.wait_for_timeout(500); R['3 hovering Code'] = pg.evaluate(BUB)
    pg.mouse.click(other['x'] + 22, other['y'] + 22)
    last = None
    for _ in range(30):
        pg.wait_for_timeout(120); yy = pg.evaluate("scrollY")
        if yy == last: break
        last = yy
    pg.wait_for_timeout(700); s = pg.evaluate(BUB); R['4 after clicking Code'] = {k: s[k] for k in ('xp', 'text_opacity', 'ghost', 'centered_on_tip', 'tip_on_active')} | {'bubble_text': pg.evaluate("document.querySelector('#bubble .btx').textContent")}
    pg.mouse.move(720, 600); pg.wait_for_timeout(20); s1 = pg.evaluate(BUB); pg.wait_for_timeout(160); s2 = pg.evaluate(BUB)
    R['5 pointer leaves: after 20 ms / after 180 ms'] = [{k: s1[k] for k in ('xp', 'text_opacity', 'ghost')}, {k: s2[k] for k in ('strip_h', 'bubble_w', 'bubble_h')}]
    pg.close()
    # touch device: flash the name on chapter change
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True); q = ctx.new_page(); q.goto(base); q.wait_for_timeout(500)
    q.add_style_tag(content="html{scroll-behavior:auto !important}")
    R['6 touch: hover media'] = q.evaluate("matchMedia('(hover: none)').matches")
    q.evaluate("document.getElementById('part3').scrollIntoView({block:'start'}); window.scrollBy(0,30)"); q.wait_for_timeout(600)
    f1 = q.evaluate("() => [document.getElementById('tbar').classList.contains('xp'), document.querySelector('#bubble .btx').textContent, +getComputedStyle(document.querySelector('#bubble .btx')).opacity]")
    q.wait_for_timeout(2600); f2 = q.evaluate("() => [document.getElementById('tbar').classList.contains('xp'), +getComputedStyle(document.querySelector('#bubble .btx')).opacity]")
    R['6 touch: on chapter change / 2.6 s later [expanded, word, opacity]'] = [f1, f2]
    q.evaluate("document.getElementById('tocmini').click()"); q.wait_for_timeout(150); R['6 touch: tapping the bar opens the list'] = q.evaluate("document.querySelectorAll('#modal .cg').length")
    ctx.close()
    # bottom links
    links = {}
    for w in (320, 390, 768, 1100, 1280, 1440):
        for url, nm in ((base, 'I'), (base + '#part-ii', 'II')):
            q = b.new_page(viewport={'width': w, 'height': 800}); q.goto(url); q.wait_for_timeout(300)
            links[f'{nm} {w}'] = q.evaluate("""() => { const Rr = e => e.getBoundingClientRect(), a = [...document.querySelectorAll('.plink')], bar = document.getElementById('bbar'), bt = Rr(document.getElementById('bbtn'));
              const hit = (x, y) => !(x.right <= y.left || y.right <= x.left);
              return {texts: a.map(x => x.innerText.trim()), current: a.map(x => x.getAttribute('aria-current')), min_h: Math.min(...a.map(x => Math.round(Rr(x).height))), clear_of_new_here: a.every(x => !hit(Rr(x), bt)), no_sideways: document.documentElement.scrollWidth <= innerWidth + 1} }""")
            q.close()
    R['7 bottom links'] = links
    q = b.new_page(viewport={'width': 1280, 'height': 800}); q.goto(base); q.wait_for_timeout(300)
    with q.expect_navigation(): q.click('.plink.p2')
    q.wait_for_timeout(500); R['7b Part II link goes to'] = q.evaluate("document.querySelector('h1').textContent")
    with q.expect_navigation(): q.click('.plink.p1')
    q.wait_for_timeout(500); R['7c Part I link goes to'] = q.evaluate("document.querySelector('h1').textContent")
    q.close(); b.close()
R['script errors'] = errs
print(json.dumps(R, indent=1))
