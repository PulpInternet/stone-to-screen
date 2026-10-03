import asyncio, json, sys, os
PAGE = 'file://' + os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
from playwright.async_api import async_playwright
CHK="""()=>{const iss=[];const d=document.documentElement;
 if(d.scrollWidth>innerWidth+1) iss.push('overflow');
 function inter(a,b){return !(a.right<=b.left||b.right<=a.left||a.bottom<=b.top||b.bottom<=a.top);}
 for(const f of document.querySelectorAll('figure')){const img=f.querySelector('img'); if(!img) continue; const art=f.closest('article'); const h=art&&art.querySelector('h3'); if(!h) continue;
   const ir=img.getBoundingClientRect(), hr=h.getBoundingClientRect(); if(ir.width>0 && Math.abs(ir.left-hr.left)>1) iss.push('img misaligned '+art.id+' '+Math.round(ir.left-hr.left));}
 const ve=document.getElementById('vtl'), v=ve?ve.getBoundingClientRect():null, m=document.querySelector('main').getBoundingClientRect(); if(v && innerWidth>=860 && v.right>m.left-24) iss.push('vtl close '+Math.round(m.left-v.right));
 const kids=[...document.querySelectorAll('#tbar .tocwrap, #tbar .tocright')].map(e=>e.getBoundingClientRect()).filter(r=>r.width>0); if(kids.length==2&&inter(kids[0],kids[1])) iss.push('tbar overlap');
 for(const r of document.querySelectorAll('.eline')){const a=[...r.children].map(e=>e.getBoundingClientRect()).filter(x=>x.width>0); for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++) if(inter(a[i],a[j])) iss.push('eline overlap');}
 const bb=document.getElementById('bbtn'), mn=document.querySelector('main');
 if(bb&&mn&&innerWidth>1100&&bb.getBoundingClientRect().width){const a=bb.getBoundingClientRect(), c=mn.getBoundingClientRect(); if(Math.abs(a.left-c.left)>3) iss.push('bottom bar off column '+Math.round(a.left-c.left));}
 for(const el of document.querySelectorAll('#bbar a,#bbtn,#tbar button,#modes button,#jump,.chip,.sbtn,.predbtn')){const r=el.getBoundingClientRect(); if(!r.width) continue;
   const af=getComputedStyle(el,'::after'); const ok=r.height>=43.5 || (af.content!=='none' && el.classList.contains('chip'));
   if(!ok) iss.push('tap target '+Math.round(r.height)+'px: '+(el.id||el.className||el.tagName));}
 const p1=document.querySelector('.plink.p1'); if(p1&&innerWidth>1200&&p1.getBoundingClientRect().left<23) iss.push('bottom bar pinned to edge');
 return iss;}"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); out={}; errs=[]
    for name,w,h in [("phone",390,844),("phone-land",844,390),("tablet",834,1112),("tablet-land",1112,834),("desktop",1440,900),("wide",2000,1068)]:
      for hsh in ["","#part-ii","#part-iii"]:
        pg=await b.new_page(viewport={"width":w,"height":h}); pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto(PAGE+hsh, wait_until="domcontentloaded"); await pg.wait_for_timeout(500)
        iss=await pg.evaluate(CHK)
        for fr in (.3,.6,1):
          await pg.evaluate(f"scrollTo(0,document.body.scrollHeight*{fr})"); await pg.wait_for_timeout(150); iss+=await pg.evaluate(CHK)
        await pg.evaluate("document.querySelectorAll('.strip').forEach(s=>s.scrollLeft=s.scrollWidth)"); await pg.wait_for_timeout(150); iss+=await pg.evaluate(CHK)
        out[name+hsh]=sorted(set(iss)); await pg.close()
    pg=await b.new_page(viewport={"width":2000,"height":1068}, color_scheme="dark")
    await pg.goto(PAGE, wait_until="domcontentloaded"); await pg.wait_for_timeout(400)
    nb=await pg.evaluate("document.querySelectorAll('#toc button').length")
    await pg.evaluate("document.querySelectorAll('#toc button')[7].click()")
    await pg.wait_for_timeout(450); y1=await pg.evaluate("scrollY"); await pg.wait_for_timeout(600); y2=await pg.evaluate("scrollY")
    tn=await pg.evaluate("document.getElementById('tnum').textContent")
    await pg.mouse.move(1000,500); await pg.mouse.wheel(0,600); await pg.wait_for_timeout(350)
    op1=await pg.evaluate("getComputedStyle(document.getElementById('vtl')).opacity")
    await pg.wait_for_timeout(1800); op2=await pg.evaluate("getComputedStyle(document.getElementById('vtl')).opacity")
    await pg.mouse.wheel(0,300); await pg.wait_for_timeout(300)
    r=await pg.evaluate("(()=>{const r=document.getElementById('track').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()")
    await pg.mouse.move(r[0],r[1]); await pg.wait_for_timeout(400); op3=await pg.evaluate("getComputedStyle(document.getElementById('vtl')).opacity")
    await pg.mouse.move(1000,500)
    await pg.goto("about:blank"); await pg.goto(PAGE+"#part-ii", wait_until="domcontentloaded"); await pg.wait_for_timeout(500)
    y=await pg.evaluate("document.getElementById('p2energy').getBoundingClientRect().top+scrollY")
    await pg.evaluate(f"scrollTo(0,{y}-130); document.querySelector('#p2energy').closest('.strip').scrollLeft=99999"); await pg.wait_for_timeout(500)
    await pg.screenshot(path="energy-dark.png")
    await pg.evaluate("document.documentElement.setAttribute('data-pmode','light')"); await pg.wait_for_timeout(200); await pg.screenshot(path="energy-light.png")
    await pg.evaluate("document.documentElement.setAttribute('data-pmode','dark')")
    await pg.goto(PAGE, wait_until="domcontentloaded"); await pg.wait_for_timeout(300)
    y=await pg.evaluate("document.getElementById('punches').getBoundingClientRect().top+scrollY"); await pg.evaluate(f"scrollTo(0,{y}-340)"); await pg.wait_for_timeout(300)
    await pg.screenshot(path="after.png")
    print(json.dumps({"issues":out,"toc_buttons":nb,"jump_done_by_450ms":abs(y2-y1)<2,"y":[y1,y2],"tnum":tn,"opacity_scrolling":op1,"after_1.8s":op2,"hovered":op3,"errors":errs},indent=1))
    await b.close()
asyncio.run(main())
