import asyncio, re
from playwright.async_api import async_playwright
LOGO = open("/home/claude/teste/helpfarm/assets/hf-icone.svg").read()
def wordmark(size=22, light=True):
    c1 = "#F4EBDD" if light else "#2E1D10"
    return f"<span class='wm' style='font-size:{size}pt'><span class='wmi' style='width:{size*1.45}pt;height:{size*1.45}pt'>{LOGO}</span><b style='color:{c1}'>Help</b><b style='color:#8FCB5A'>Farm</b></span>"
src = open("/home/claude/hfm/gen_manual.py").read()
CSS = src[src.find('CSS = """')+9: src.find('"""', src.find('CSS = """')+9)]
CSS += """
.rapp{background:linear-gradient(135deg,#2E1D10,#4A2F1B);color:#F4EBDD;border-radius:4mm;padding:4.5mm 5mm;margin-top:5mm}
.rapp b.t{color:#8FCB5A;font-family:'Inter Display',Inter;font-size:12pt;display:block;margin-bottom:1.5mm}
.ben{display:grid;grid-template-columns:1fr 1fr;gap:3mm}.ben div{background:#fff;border:.6pt solid var(--line);border-radius:3mm;padding:3mm 3.5mm}
.ben b{display:block;font-size:10pt;color:var(--g1);margin-bottom:1mm}
.flow{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin:3mm 0}.flow div{background:var(--sand);border-radius:3mm;padding:3.5mm;position:relative}
.flow b{display:block;font-family:'Inter Display',Inter;font-size:16pt;color:var(--terra)}.flow h3{margin:1mm 0}
"""
def foot(n, label):
    return f"<div class='foot'>{wordmark(8.5, False)}<span>{label} · tudo controlado pelo RAPP</span><span>{n}</span></div>"
def cover(img, kicker, title_html, lead, kpis, note="Imagem ilustrativa gerada por IA"):
    k = "".join(f"<div><b style='font-family:\"Inter Display\";font-size:17pt;color:#8FCB5A'>{a}</b><br><span style='font-size:7.6pt;opacity:.85'>{b}</span></div>" for a, b in kpis)
    return f"""<div class='pg' style='background:#2E1D10'>
<img src='{img}' style='position:absolute;top:0;left:0;width:100%;height:178mm;object-fit:cover'>
<div style='position:absolute;top:0;left:0;right:0;height:178mm;background:linear-gradient(180deg,rgba(46,29,16,.55) 0%,rgba(46,29,16,0) 30%,rgba(46,29,16,0) 62%,#2E1D10 100%)'></div>
<div style='position:absolute;top:13mm;left:15mm'>{wordmark(20)}</div>
<div style='position:absolute;top:14mm;right:15mm;color:#F4EBDD;font-size:8pt;letter-spacing:.14em;text-transform:uppercase;opacity:.9'>Dispositivo exclusivo Help Farm · Nov 2026</div>
<div style='position:absolute;left:15mm;right:15mm;top:148mm;color:#F4EBDD'>
<span class='eyebrow' style='color:#FFB500'>{kicker}</span>
<div style='font-family:"Inter Display";font-weight:800;font-size:38pt;line-height:1;letter-spacing:-.02em'>{title_html}</div>
<p style='font-size:11pt;margin-top:5mm;max-width:160mm;color:#E9DCC6'>{lead}</p></div>
<div style='position:absolute;left:15mm;right:15mm;bottom:16mm;display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;color:#F4EBDD'>{k}</div>
<div style='position:absolute;right:15mm;top:160mm;font-size:6.5pt;color:#C9B79C'>{note}</div></div>"""
async def render(html, out, landscape=False):
    open(out.replace('.pdf', '.html'), 'w').write(html)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto("file://" + out.replace('.pdf', '.html')); await pg.wait_for_timeout(1500)
        await pg.pdf(path=out, width="297mm" if landscape else "210mm", height="210mm" if landscape else "297mm", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        await b.close()
def page(html): return "<!doctype html><html><head><meta charset='utf-8'><style>" + CSS + "</style></head><body>" + html + "</body></html>"
