# checks/check_functional.py
# Drives the page like a reader: every control is clicked or typed into, on desktop and phone,
# and the result is checked. Usage:
#   python3 checks/check_functional.py index.html            (local file)
#   python3 checks/check_functional.py https://.../          (a live URL)
# Exits 1 on any failure.
import asyncio, json, os, sys
from playwright.async_api import async_playwright

ARG = sys.argv[1] if len(sys.argv) > 1 else "index.html"
BASE = ARG if ARG.startswith("http") else "file://" + os.path.abspath(ARG)
fails, passes = [], 0

def ok(cond, what):
    global passes
    if cond: passes += 1
    else: fails.append(what)

async def fresh(b, w, h, hsh="", scheme="light"):
    ctx = await b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme, has_touch=w < 900)
    pg = await ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto("about:blank"); await pg.goto(BASE + hsh, wait_until="domcontentloaded"); await pg.wait_for_timeout(600)
    return ctx, pg, errs

async def opened_modal(pg):
    return await pg.evaluate("!!document.getElementById('overlay') && !!document.getElementById('modal')")

async def run(b, w, h, tag):
    # ---------- Part I ----------
    ctx, pg, errs = await fresh(b, w, h)
    ok(await pg.evaluate("document.documentElement.getAttribute('data-page')") == "1", f"{tag} P1: root data-page is 1")
    ok(await pg.evaluate("document.querySelectorAll('meta[name=viewport]').length") == 1, f"{tag} P1: one viewport meta")
    ok(await pg.evaluate("!!document.querySelector('#tbar') && !!document.querySelector('#vtl') && !!document.querySelector('#bbtn')"), f"{tag} P1: has chapter bar, timeline, New here")
    acc = await pg.evaluate("getComputedStyle(document.querySelector('#hero .marker'),'::before').backgroundColor")
    ok(acc == "rgb(239, 240, 0)", f"{tag} P1: hero highlight is electric yellow (got {acc})")
    gap = await pg.evaluate("""(()=>{const m=document.querySelector('#hero .marker'); const r=document.createRange(); const t=m.previousSibling; r.setStart(t, Math.max(0,t.length-2)); r.setEnd(t, t.length-1); return Math.round(m.getBoundingClientRect().left - r.getBoundingClientRect().right)})()""")
    ok(gap >= 4, f"{tag} P1: space between the word before the highlight and the highlight ({gap}px)")
    # mode switch persists
    await pg.click("#modes button[data-m=dark]")
    ok(await pg.evaluate("document.documentElement.getAttribute('data-pmode')") == "dark", f"{tag} mode: dark applies")
    await pg.reload(wait_until="domcontentloaded"); await pg.wait_for_timeout(400)
    ok(await pg.evaluate("document.documentElement.getAttribute('data-pmode')") == "dark", f"{tag} mode: dark persists after reload")
    await pg.click("#modes button[data-m=dark]")
    ok(await pg.evaluate("document.documentElement.getAttribute('data-pmode')") is None, f"{tag} mode: clicking again returns to system")
    # chapter bar or mini list
    if w >= 860:
        await pg.evaluate("document.querySelectorAll('#toc button')[4].click()"); await pg.wait_for_timeout(700)
        tn = await pg.evaluate("document.getElementById('tnum').textContent")
        want = await pg.evaluate("String(+document.querySelector('#part5 .beat').dataset.i + 1).padStart(2,'0')")
        ok(tn.startswith(want), f"{tag} chapter bar: jumps to chapter 5 (counter {tn}, expected {want})")
    # index modal jump
    await pg.evaluate("window.scrollTo(0,0)")
    await pg.click("#jump") if await pg.is_visible("#jump") else await pg.click("#tocmini")
    await pg.wait_for_timeout(200)
    ok(await opened_modal(pg), f"{tag} index: opens a modal")
    items = await pg.evaluate("document.querySelectorAll('#modal ol button, #modal li button, #modal .cg').length")
    ok(items >= 10, f"{tag} index: lists entries ({items})")
    if items:
        await pg.evaluate("(function(){var l=document.querySelectorAll('#modal ol button, #modal li button, #modal .cg'); l[Math.min(20, l.length-1)].click();})()")
        await pg.wait_for_timeout(800)
        ok(not await opened_modal(pg), f"{tag} index: modal closes after choosing")
        ok(await pg.evaluate("scrollY") > 300, f"{tag} index: page moved to the chosen moment")
    # fact chip modal + escape
    await pg.evaluate("document.querySelector('.chip').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(200)
    await pg.click(".chip >> nth=0"); await pg.wait_for_timeout(200)
    ok(await opened_modal(pg), f"{tag} chip: opens a modal")
    await pg.keyboard.press("Escape"); await pg.wait_for_timeout(150)
    ok(not await opened_modal(pg), f"{tag} chip: Escape closes it")
    # bottom New here modal + outside click
    await pg.click("#bbtn"); await pg.wait_for_timeout(200)
    ok(await opened_modal(pg), f"{tag} New here: opens a modal")
    await pg.mouse.click(5, 120); await pg.wait_for_timeout(150)
    ok(not await opened_modal(pg), f"{tag} New here: outside click closes it")
    # horizontal strip arrows
    await pg.evaluate("document.querySelector('.part.horz .snav').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(200)
    x0 = await pg.evaluate("document.querySelector('.part.horz .strip').scrollLeft")
    await pg.click(".part.horz .sbtn.next >> nth=0"); await pg.wait_for_timeout(700)
    x1 = await pg.evaluate("document.querySelector('.part.horz .strip').scrollLeft")
    ok(x1 > x0, f"{tag} strip: next arrow scrolls sideways ({x0} to {x1})")
    # Part II link
    await pg.click(".plink.p2"); await pg.wait_for_timeout(900)
    ok(await pg.evaluate("document.documentElement.getAttribute('data-page')") == "2", f"{tag} Part II link: switches to Part II")
    ok(errs == [], f"{tag} P1: no script errors {errs[:2]}")
    await ctx.close()

    # ---------- Part II ----------
    ctx, pg, errs = await fresh(b, w, h, "#part-ii")
    acc = await pg.evaluate("getComputedStyle(document.querySelector('#hero .marker'),'::before').backgroundColor")
    ok(acc == "rgb(0, 158, 96)", f"{tag} P2: hero highlight is Hannah green (got {acc})")
    ok(await pg.evaluate("document.title").__contains__("Part II") if False else "Part II" in await pg.evaluate("document.title"), f"{tag} P2: title")
    ok(await pg.evaluate("!document.querySelector('#part1')"), f"{tag} P2: Part I content removed")
    await pg.evaluate("document.querySelector('.predbtn').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(200)
    await pg.click(".predbtn"); await pg.wait_for_timeout(200)
    ok(await pg.evaluate("document.querySelectorAll('.plist li').length") == 31, f"{tag} P2: predictions modal lists 31")
    await pg.keyboard.press("Escape")
    await pg.evaluate("document.querySelector('[data-ch=p2energy][data-f=\"3\"]').click()"); await pg.wait_for_timeout(150)
    ok(await opened_modal(pg), f"{tag} P2: water chip opens")
    await pg.keyboard.press("Escape")
    await pg.click(".plink.p3"); await pg.wait_for_timeout(900)
    ok(await pg.evaluate("document.documentElement.getAttribute('data-page')") == "3", f"{tag} Part III link: switches to Part III")
    ok(errs == [], f"{tag} P2: no script errors {errs[:2]}")
    await ctx.close()

    # ---------- Part III ----------
    ctx, pg, errs = await fresh(b, w, h, "#part-iii")
    for name, sel in (("chapter bar", "#tbar"), ("scroll timeline", "#vtl"), ("New here", "#bbtn")):
        ok(await pg.evaluate(f"!!document.querySelector('{sel}')"), f"{tag} P3: has the {name}")
    n3 = await pg.evaluate("document.querySelectorAll('#toc .tocb, #tocmini .mi').length")
    ok(n3 >= 3, f"{tag} P3: chapter bar lists Part III chapters ({n3})")
    ok("15" in await pg.evaluate("document.querySelector('.pnum').textContent"), f"{tag} P3: chapters numbered from 15")
    await pg.evaluate("document.getElementById('part17').scrollIntoView()"); await pg.wait_for_timeout(500)
    tn3 = await pg.evaluate("document.getElementById('tnum').textContent")
    ok(("03" in tn3) if w >= 860 else True, f"{tag} P3: timeline follows scroll to the last chapter")
    await pg.evaluate("scrollTo(0,0)"); await pg.wait_for_timeout(200)
    before = await pg.evaluate("document.getElementById('orows').innerText")
    await pg.fill("#cvol", "5000000"); await pg.wait_for_timeout(150)
    after = await pg.evaluate("document.getElementById('orows').innerText")
    ok(before != after, f"{tag} P3: volume changes the results")
    await pg.select_option("#cregion", "Oregon"); await pg.wait_for_timeout(150)
    ok("Oregon" in await pg.evaluate("document.getElementById('cnote').textContent"), f"{tag} P3: region changes the note")
    await pg.evaluate("const s=document.getElementById('mx0'); s.value=100; s.dispatchEvent(new Event('input'))"); await pg.wait_for_timeout(150)
    shares = await pg.evaluate("[...document.querySelectorAll('.mxv')].map(o=>parseInt(o.textContent))")
    ok(abs(sum(shares) - 100) <= 3, f"{tag} P3: mix shares add to about 100 ({shares})")
    await pg.click("#modes button[data-m=mono]")
    ok(await pg.evaluate("document.documentElement.getAttribute('data-pmode')") == "mono", f"{tag} P3: mode switch works")
    await pg.click("#modes button[data-m=mono]")
    await pg.click(".plink.p1"); await pg.wait_for_timeout(900)
    ok(await pg.evaluate("document.documentElement.getAttribute('data-page')") == "1", f"{tag} Part I link from Part III")
    ok(errs == [], f"{tag} P3: no script errors {errs[:2]}")
    await ctx.close()

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, h, tag in [(1440, 900, "desktop"), (390, 844, "phone")]:
            try: await run(b, w, h, tag)
            except Exception as e: fails.append(f"{tag}: check crashed: {str(e).splitlines()[0][:160]}")
        await b.close()
    print(f"check_functional: {passes} passed, {len(fails)} failed")
    for f in fails: print("  FAIL", f)
    sys.exit(1 if fails else 0)

asyncio.run(main())
