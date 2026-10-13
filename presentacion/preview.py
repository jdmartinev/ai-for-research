"""Vista previa local: cada diapositiva a PNG con Chromium (sin el runtime del tipo Slides)."""
import json, re, sys, asyncio
from pathlib import Path
from playwright.async_api import async_playwright
HERE = Path(__file__).parent
order = json.loads((HERE/"project/deck.json").read_text())["order"]
only = sys.argv[1:] or order
CSS = "*{margin:0;padding:0;box-sizing:border-box} section{position:relative;width:1920px;height:1080px;overflow:hidden} aside{display:none} ul{padding-left:36px} table{border-collapse:collapse;width:100%} th,td{text-align:left;padding:14px 16px;border-bottom:1px solid #2A3550}"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":1920,"height":1080})
        for sid in only:
            h = (HERE/f"web/slides/{sid}.html").read_text()
            h = re.sub(r'src="/_blob/[0-9a-f]+"', 'src="data:image/gif;base64,R0lGODlhAQABAAAAACw="', h)
            h = h.replace('object-fit:contain"', 'object-fit:contain;background:#333"')
            await pg.set_content(f"<html><head><style>{CSS}</style></head><body>{h}</body></html>")
            # overflow check: any element bottom > 920 except footer
            over = await pg.evaluate("""() => { const r=[]; document.querySelectorAll('section *').forEach(el=>{const b=el.getBoundingClientRect(); const st=getComputedStyle(el); if(st.position!=='absolute' && el.tagName!=='ASIDE' && b.bottom>925 && b.height>0 && !el.closest('aside')) r.push(el.tagName+':'+Math.round(b.bottom)); if(el.scrollWidth>el.clientWidth+2 && el.tagName==='P') r.push('wide:'+el.textContent.slice(0,30));}); return r.slice(0,4); }""")
            await pg.screenshot(path=str(HERE/f"prev/{order.index(sid):02d}_{sid}.png"))
            if over: print(sid, over)
        await b.close()
asyncio.run(main())
