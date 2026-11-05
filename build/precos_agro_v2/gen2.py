# Gera os dois PDFs do Help Farm no mesmo modelo dos documentos do Help Cure.
import json, asyncio, html as H
from refs_en import REFS
from playwright.async_api import async_playwright
from pypdf import PdfWriter, PdfReader

C = json.load(open("calc.json")); EN = json.load(open("calc_en.json"))
def r(*n): return "<sup>[" + ",".join(map(str, n)) + "]</sup>"
def us(v, d=0): return ("US$ " + f"{v:,.{d}f}").replace(",", "X").replace(".", ",").replace("X", ".")
def n0(v): return f"{v:,.0f}".replace(",", ".")

CSS = """
@font-face{font-family:Inter}
:root{--ink:#2E1D10;--ink2:#5E4A38;--g:#3F7A22;--g2:#5E9F3A;--t:#B5642F;--line:#E6D9C4;--soft:#F6EFE3;--card:#FFFDF8;--dk:#2E1D10}
*{box-sizing:border-box}
body{font-family:Inter,Arial,sans-serif;color:var(--ink);font-size:9.4pt;line-height:1.45;margin:0}
h1{font-family:'Inter Display',Inter,sans-serif;font-size:19pt;margin:0 0 7pt;letter-spacing:-.01em}
h2{font-size:11.5pt;margin:12pt 0 5pt;color:var(--ink)}
h3{font-size:10pt;margin:8pt 0 3pt}
p{margin:0 0 6pt}
.sec{page-break-before:always}.sec.first{page-break-before:auto}
table{width:100%;border-collapse:collapse;font-size:7.8pt;margin:4pt 0 8pt}
tr{page-break-inside:avoid}thead{display:table-header-group}
th{background:var(--dk);color:#fff;text-align:left;padding:4pt 5pt;font-weight:600;vertical-align:bottom}
td{padding:3.2pt 5pt;border-bottom:1px solid var(--line);vertical-align:top}
td.n,th.n{text-align:right;white-space:nowrap}
tr.grp td{background:var(--soft);font-weight:700;color:var(--g)}
tr.hl td{background:#EDF4E6;font-weight:600}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:7pt;margin:8pt 0 10pt}
.kpi{background:var(--dk);color:#fff;border-radius:7pt;padding:9pt 10pt}
.kpi b{display:block;font-size:15pt;line-height:1.1;color:#9BD06A;font-family:'Inter Display',Inter}
.kpi span{font-size:7.4pt;color:#E8DCC8}
.pts{display:grid;gap:6pt;margin:6pt 0}
.pt{background:var(--soft);border-radius:6pt;padding:7pt 9pt 7pt 32pt;position:relative}
.pt i{position:absolute;left:8pt;top:7pt;width:17pt;height:17pt;border-radius:50%;background:var(--dk);color:#fff;font-style:normal;font-weight:700;font-size:8pt;display:flex;align-items:center;justify-content:center}
.note{font-size:7.6pt;color:var(--ink2)}
.box{background:#EDF4E6;border-left:4px solid var(--g);padding:8pt 10pt;border-radius:4pt;margin:8pt 0;font-size:8.8pt}
.warn{background:#FBF0E2;border-left:4px solid var(--t);padding:8pt 10pt;border-radius:4pt;margin:8pt 0;font-size:8.6pt}
.warn b.h{color:#8A4A1A}
.dark{background:var(--dk);color:#F3E9D8;border-radius:8pt;padding:10pt 12pt;margin:8pt 0}
.dark h3{color:#9BD06A;margin-top:0}
.chart{border:1px solid var(--line);border-radius:8pt;padding:8pt 10pt;margin:6pt 0 8pt}
.chart .t{font-weight:700;font-size:8.6pt;margin-bottom:4pt}
ul{margin:2pt 0 6pt 13pt;padding:0}li{margin-bottom:3pt}
.refs{font-size:7pt;padding-left:14pt}.refs li{margin-bottom:2.2pt;word-break:break-all}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:8pt;margin:6pt 0}
.card{border:1px solid var(--line);border-radius:8pt;padding:8pt 10pt;page-break-inside:avoid}
.card h3{margin:0 0 4pt;font-size:9.6pt}.card h3 em{font-style:normal;color:var(--g2);margin-right:5pt}
.card .s{border-top:1px dashed var(--line);margin-top:5pt;padding-top:4pt;font-size:7.6pt;color:var(--ink2)}
svg text{font-family:Inter,Arial,sans-serif}
"""

def page(body): return f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"

def cover(kicker, title_html, sub, stats, img):
    st = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in stats)
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>
@page{{size:A4;margin:0}}html,body{{margin:0;width:210mm;height:297mm}}
body{{background:#2E1D10;color:#fff;font-family:Inter,Arial,sans-serif;position:relative;overflow:hidden}}
.img{{position:absolute;top:0;left:0;right:0;height:150mm;background:url('{img}') center/cover}}
.img:after{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(46,29,16,.15) 40%,#2E1D10 100%)}}
.brand{{position:absolute;top:118mm;left:20mm;display:flex;align-items:center;gap:4mm;font-family:'Inter Display',Inter;font-weight:800;font-size:22pt}}
.brand b{{color:#9BD06A}}
.k{{position:absolute;top:142mm;left:20mm;right:20mm;font-size:8.5pt;letter-spacing:.16em;text-transform:uppercase;color:#9BD06A;font-weight:700}}
h1{{position:absolute;top:150mm;left:20mm;right:20mm;font-family:'Inter Display',Inter;font-size:30pt;line-height:1.08;margin:0;font-weight:800}}
h1 em{{font-style:normal;color:#9BD06A}}
.sub{{position:absolute;top:208mm;left:20mm;right:28mm;font-size:12pt;color:#E8DCC8;line-height:1.45}}
.st{{position:absolute;top:236mm;left:20mm;right:20mm;display:grid;grid-template-columns:repeat(3,1fr);gap:6mm;border:1px solid #5a4330;border-radius:10px;padding:6mm 7mm;background:#3a2716}}
.st b{{display:block;font-size:12pt;margin-bottom:1mm}}.st span{{font-size:8.5pt;color:#D9C9B0}}
.f{{position:absolute;bottom:12mm;left:20mm;right:20mm;border-top:1px solid #5a4330;padding-top:4mm;font-size:8pt;color:#C8B79C;display:flex;justify-content:space-between}}
</style></head><body><div class='img'></div>
<div class='brand'><svg width='40' height='40' viewBox='0 0 40 40'><rect x='1' y='1' width='38' height='38' rx='10' fill='#4A2F1B' stroke='#9BD06A' stroke-opacity='.5'/><path d='M7 29c6-3 20-3 26 0M7 24c6-3 20-3 26 0' fill='none' stroke='#C9A36B' stroke-width='2' stroke-linecap='round' opacity='.8'/><path d='M8 19l6-1 4-6 4 9 4-4 6 0' fill='none' stroke='#8FCB5A' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'/><circle cx='32' cy='17' r='2.6' fill='#FFB500'/></svg><span>Help<b>Farm</b></span></div>
<div class='k'>{kicker}</div><h1>{title_html}</h1><div class='sub'>{sub}</div><div class='st'>{st}</div>
<div class='f'><span>Help Farm · helpcure.com.py/helpfarm</span><span>Novembro de 2026</span></div></body></html>"""

def range_chart(title, rows, band, maxv, unit, src, w=640):
    # rows: (label, lo, hi, txt, kind) kind: 'm' mercado, 'e' economia
    lh = 21; top = 8; left = 205; pw = w - left - 120; h = top + lh * len(rows) + 42
    sx = lambda v: left + pw * min(v, maxv) / maxv
    g = [f"<rect x='{sx(band[0]):.1f}' y='{top-4}' width='{sx(band[1])-sx(band[0]):.1f}' height='{lh*len(rows)+4}' fill='#9BD06A' opacity='.28'/>"]
    for k in range(6):
        v = maxv * k / 5; x = sx(v)
        g.append(f"<line x1='{x:.1f}' x2='{x:.1f}' y1='{top-4}' y2='{top+lh*len(rows)}' stroke='#E6D9C4'/><text x='{x:.1f}' y='{top+lh*len(rows)+12}' font-size='8' text-anchor='middle' fill='#5E4A38'>{v:g}</text>")
    for i, (lab, lo, hi, txt, kind) in enumerate(rows):
        y = top + lh * i + lh / 2
        col = "#B5642F" if kind == "e" else "#2E1D10"
        g.append(f"<text x='{left-8}' y='{y+3}' font-size='8.4' text-anchor='end' fill='#2E1D10'>{H.escape(lab)}</text>")
        if hi > lo: g.append(f"<line x1='{sx(lo):.1f}' x2='{sx(hi):.1f}' y1='{y}' y2='{y}' stroke='{col}' stroke-width='7' stroke-linecap='round'/>")
        else: g.append(f"<circle cx='{sx(lo):.1f}' cy='{y}' r='4.5' fill='{col}'/>")
        g.append(f"<text x='{sx(max(lo,hi))+8:.1f}' y='{y+3}' font-size='7.6' fill='#5E4A38'>{H.escape(txt)}</text>")
    g.append(f"<text x='{sx((band[0]+band[1])/2):.1f}' y='{top+lh*len(rows)+24}' font-size='8' font-weight='700' text-anchor='middle' fill='#3F7A22'>Help Farm: {H.escape(band[2])}</text>")
    g.append(f"<text x='{left+pw/2:.1f}' y='{h}' font-size='7.6' text-anchor='middle' fill='#5E4A38'>{unit}</text>")
    return f"<div class='chart'><div class='t'>{title}</div><svg viewBox='0 0 {w} {h+4}' width='100%'>{''.join(g)}</svg><div class='note'>{src}</div></div>"

def bars(title, rows, maxv, unit, w=640):
    lh = 20; left = 130; pw = w - left - 60; h = lh * len(rows) + 22
    cols = ["#2E1D10", "#3F7A22", "#5E9F3A", "#9BD06A", "#C9A36B", "#B5642F", "#FFB500"]
    g = []
    for i, (lab, parts, tot) in enumerate(rows):
        y = i * lh + 4; x = left
        g.append(f"<text x='{left-8}' y='{y+11}' font-size='8.4' text-anchor='end' font-weight='600'>{H.escape(lab)}</text>")
        for j, v in enumerate(parts):
            ww = pw * v / maxv; g.append(f"<rect x='{x:.1f}' y='{y}' width='{ww:.1f}' height='13' fill='{cols[j]}'/>"); x += ww
        g.append(f"<text x='{x+5:.1f}' y='{y+11}' font-size='8.4' font-weight='700'>{tot}</text>")
    return f"<div class='chart'><div class='t'>{title}</div><svg viewBox='0 0 {w} {h}' width='100%'>{''.join(g)}</svg>{unit}</div>"

# ============================================================== DOC 1
mix = C["mix"]; Pp = {p["pais"]: p for p in C["paises"]}
doc1 = []
F = EN["fazenda"]; A5 = EN["ano5"]; PRc = EN["precos"]
def mi1(v): return f"US$ {v/1e6:,.1f} mi".replace(".", ",")
doc1.append(f"""<div class='sec first'><h1>Resumo para investidores</h1>
<p><b>Quem já paga por monitoramento agro paga por unidade: por hectare, por cabeça, por máquina ou por contrato.</b> Na lavoura, vai de US$ 0,2/ha/ano (satélite puro no Brasil) a US$ 22/ha (vistoria de agrônomo nos EUA). No leite, de US$ 1,5 a 5,7 por vaca/mês. Em máquinas, de US$ 17 a 50 por máquina/mês. A Help Farm entrega satélite, sensores, visita da unidade móvel e alerta preditivo num só contrato e cobra no meio dessas faixas.</p>
<p><b>Novidade desta versão: a camada de energia do RAPP.</b> Os mesmos sensores que leem bombas e pivôs passam a aprender como a fazenda usa energia. O RAPP projeta a geração própria (principalmente solar na irrigação) atividade por atividade e depois verifica, mês a mês, a economia na conta. Nenhum concorrente pesquisado junta o dado agronômico, a medição de kWh e a verificação da economia (seção 5).</p>
<div class='kpis'>
<div class='kpi'><b>US$ 4–12</b><span>por hectare/ano de grãos (Paraguai a EUA), entre o satélite barato e o agrônomo caro</span></div>
<div class='kpi'><b>{F['B']['pct_conta']}%</b><span>de economia na conta de luz de uma fazenda irrigada de 500 ha no Brasil (gestão + usina solar; estimativa)</span></div>
<div class='kpi'><b>{str(round(F['B']['prod_liq']/F['B']['hf_ano'],1)).replace('.',',')}×</b><span>o ganho líquido do produtor sobre o que ele paga à Help Farm pela energia (faixa B)</span></div>
<div class='kpi'><b>+{mi1(A5['total'])}</b><span>de receita no Ano 5 (Paraguai + Brasil), +{str(A5['pct_receita']).replace('.',',')}% sobre o caso base; pré-money justo de ≈ US$ {str(round(A5['pre_novo']/1e6,1)).replace('.',',')} mi</span></div></div>
<h2>O conceito de valor em cinco pontos</h2>
<div class='pts'>
<div class='pt'><i>1</i><b>A perda evitada é muito maior que o preço.</b> Pragas e doenças tiram de 11% a 32% da soja no mundo{r(52)}; a seca de 2021/22 derrubou a safra paraguaia de soja em 58%{r(53)}; a doença respiratória custa US$ 111 por animal doente nos EUA{r(55)}. Um alerta por safra paga o ano.</div>
<div class='pt'><i>2</i><b>A conta de luz paga a assinatura.</b> Energia chega a 30–50% do custo de quem irriga{r(83,111)}. Numa fazenda irrigada típica, a economia de energia vale de 3 a 5 vezes o que a Help Farm cobra por todo o monitoramento, e aparece na fatura do mês seguinte.</div>
<div class='pt'><i>3</i><b>Um contrato no lugar de quatro.</b> Hoje o produtor compra satélite (US$ 1–11/ha), agrônomo (US$ 11–22/ha nos EUA), coleira (US$ 2–6/vaca/mês) e telemetria (US$ 17–50/máquina/mês) de fornecedores diferentes{r(1,2,5,14,21)}. A Help Farm junta tudo e cobra menos que a soma.</div>
<div class='pt'><i>4</i><b>Vários pagadores para o mesmo dado.</b> No Brasil, desde março de 2026 o banco é obrigado a monitorar por sensoriamento remoto o crédito rural acima de 300 ha{r(25)}. Seguradoras, cooperativas, distritos de irrigação e compradores (EUDR) também pagam pelo mesmo dado verificado{r(29,38,39)}.</div>
<div class='pt'><i>5</i><b>O equilíbrio exige pouca adesão.</b> Em todos os países, a operação local fica paga com 37 a 63 fazendas, já contando a energia: menos de 0,1% dos estabelecimentos de cada país.</div></div>
<h2>Preços</h2>
<p>A pesquisa mostrou que a tabela antiga estava <b>baixa em grãos</b> e <b>alta em leite, corte e máquinas</b>. Os preços de mercado (grãos US$ 4–12/ha/ano; corte US$ 0,35–1,20/cabeça/mês; leite US$ 3–5/vaca/mês; máquinas, pivôs e bombas US$ 20–40/ativo/mês) já estão no modelo v2 e reduziram o pré-money justo de US$ 9,2 mi para US$ 7,5 mi. A camada de energia é cobrada à parte: <b>diagnóstico e projeto de US$ 1.500–4.000 por fazenda, 30% da economia verificada por 4 anos e US$ 4–9 por kWp/ano para monitorar a usina</b>. O medidor de kWh por ativo vem incluído no preço da máquina, como porta de entrada.</p>
<h2>Onde entrar primeiro</h2>
<p>Pela pontuação da seção 7, agora com a dor de energia, o <b>Brasil</b> segue em primeiro (crédito rural obrigatório, maior base e energia cara de dia). A energia sobe <b>EUA</b> e <b>Portugal + Espanha</b> (energia até 50% do custo do regante); <b>Argentina</b> e <b>Paraguai</b> vêm logo atrás. No Paraguai o argumento de energia é o diesel do Chaco e a rede fraca, não a tarifa; a proximidade continua fazendo dele o piloto.</p>
<p class='note'>Valores em dólar convertidos pelo câmbio de referência de cada fonte (aprox. €1 = US$ 1,10; US$ 1 = R$ 5,40; NZ$ 1 = US$ 0,58; A$ 1 = US$ 0,65). Preços da Help Farm: aba Precos do modelo v2 (05/11/2026); preços da camada de energia: proposta desta versão, ainda fora da planilha. Estimativas estão marcadas como tal. Nenhum preço foi validado com clientes.</p></div>""")

# 1. quanto o mundo paga
g1 = range_chart("Lavoura de grãos — US$ por hectare por ano", [
 ("Brasil · satélite (Agronow, 2017)", .19, .19, "0,2", "m"),
 ("Canadá · FieldView (fazenda de 400 ha)", .9, .9, "≈0,9 (estim.)", "m"),
 ("Brasil · assistência técnica (Embrapa)", 2.8, 2.8, "2,8", "m"),
 ("Brasil · Solinftec (receita/ha)", 5.4, 5.4, "≈5,4 (calc.)", "m"),
 ("Europa · OneSoil / xarvio", 5.5, 11, "5,5–11", "m"),
 ("EUA · grid de solo (por coleta)", 8, 25, "8–25", "m"),
 ("EUA · vistoria de agrônomo", 14.8, 22.2, "15–22", "m"),
 ("Sensores + plataforma (CropX, Arable)", 6, 30, "6–75 (estim.)", "m"),
 ("Brasil · consultoria privada (50 ha)", 30, 30, "36–91", "m"),
], (4, 12, "US$ 4–12"), 30, "US$ por hectare por ano", f"Fontes: FieldView{r(1)}, OneSoil{r(2)}, xarvio{r(3)}, MSU{r(5)}, Iowa{r(6)}, Solinftec{r(7)}, Agronow{r(8)}, Embrapa{r(9)}. Barras cortadas em 30 (consultoria privada no Brasil chega a 91).")
g2 = range_chart("Pecuária de leite — US$ por vaca por mês (só assinatura)", [
 ("Nova Zelândia · SenseHub", 1.48, 2.56, "1,5–2,6", "m"),
 ("Irlanda · smaXtec (+ bolus)", 2.75, 3.3, "2,75–3,3", "m"),
 ("Irlanda · SenseHub", 3.85, 3.85, "3,85", "m"),
 ("Brasil · Cowmed", 4.0, 4.1, "≈4", "m"),
 ("Nova Zelândia · Halter (coleira + cerca)", 5.7, 5.7, "≈5,7", "m"),
], (3, 5, "US$ 3–5 com sensor em comodato"), 7, "US$ por vaca por mês", f"Fontes: SenseHub NZ{r(14)}, Farmers Journal{r(15)}, Cowmed{r(16)}, Halter{r(13)}.")
g3 = range_chart("Pecuária de corte — US$ por cabeça por mês", [
 ("Paraguai · brinco SENACSA (pago pelo Estado)", 0, 0, "0 ao produtor", "m"),
 ("Argentina · caravana (única vez, ÷ 36 meses)", .04, .06, "US$ 1,5–2 uma vez", "m"),
 ("Austrália · Ceres Tag (3 anos)", 1.2, 1.2, "≈1,2 (estim.)", "m"),
 ("Austrália · Smart Paddock GPS", 1.3, 1.3, "1,3", "m"),
 ("EUA · cerca virtual (+ coleira)", 1.5, 4, "1,5–4", "m"),
], (.35, 1.2, "US$ 0,35–1,20"), 5, "US$ por cabeça por mês", f"Fontes: SENACSA{r(18)}, Argentina{r(19)}, NSW AgTech{r(12)}, cerca virtual{r(17)}.")
g4 = range_chart("Máquinas, pivôs e bombas — US$ por ativo por mês", [
 ("Austrália · bomba (Grundfos, Goanna)", 10, 20, "10–20", "m"),
 ("EUA · JDLink (2019)", 16.7, 16.7, "16,7", "m"),
 ("EUA · pivô Lindsay (1º ano)", 36.7, 36.7, "≈37", "m"),
 ("EUA · telemetria pós-venda", 27, 50, "27–50 (não verificado)", "m"),
 ("EUA · licença Deere de precisão", 88, 88, "88–400", "m"),
], (20, 40, "US$ 20–40"), 100, "US$ por ativo por mês", f"Fontes: JDLink{r(21)}, licenças Deere{r(22)}, Lindsay{r(23)}, Grundfos{r(24)}, NSW AgTech{r(12)}.")
doc1.append(f"""<div class='sec'><h1>1. Quanto o mundo paga</h1>
<p>Os gráficos comparam o que produtores já pagam por monitoramento com a faixa de preço proposta para a Help Farm (área verde). Pontos são valores únicos; barras, faixas.</p>{g1}{g2}</div>
<div class='sec'>{g3}{g4}
<p>Três formas de cobrança aparecem no mercado:</p>
<ul><li><b>Por unidade (hectare, cabeça, máquina)</b> — Europa, Oceania, Brasil no leite, telemetria. É o modelo da Help Farm.</li>
<li><b>Por fazenda (valor fixo por ano)</b> — FieldView e Agworld: barato por hectare em fazendas grandes, mas sem sensor nem visita.</li>
<li><b>Por contrato ou por tonelada</b> — governos, bancos, seguradoras e compradores (seção 3).</li></ul></div>""")

# 2. tabela por país (produtores)
T = [
 ("América do Sul", None),
 ("Brasil", ("Produtor de leite", "Cowmed, coleira por assinatura", "R$ 22–23/vaca/mês", "≈4,0/vaca/mês", 16)),
 ("Brasil", ("Produtor de grãos", "Solinftec (ARR ÷ área)", "R$ 430 mi / >15 mi ha", "≈5,4/ha/ano (calc.)", 7)),
 ("Brasil", ("Produtor de grãos", "Assistência técnica (planilha de custo)", "R$ 14,96/ha", "≈2,8/ha/ano", 9)),
 ("Brasil", ("Produtor de grãos", "Consultoria paga em produto", "2 sacas/ha", "≈45/ha (estim.)", 10)),
 ("Brasil", ("Produtor de grãos", "Satélite (Agronow, 2017)", "R$ 1/ha/ano", "≈0,2/ha/ano", 8)),
 ("Paraguai", ("Estado (SENACSA)", "Caravana eletrônica bovina", "US$ 0,95/caravana", "0 ao produtor", 18)),
 ("Paraguai", ("Produtor", "Honorário mínimo do agrônomo (lei)", "13–16 jornales por serviço", "≈190/serviço (estim.)", 11)),
 ("Argentina", ("Produtor", "Caravana eletrônica SENASA", "US$ 1,50–2 (uma vez)", "≈0,05/cab./mês", 19)),
 ("Argentina", ("Produtor", "xarvio Pro (2021)", "≈US$ 500/ano", "por fazenda", 50)),
 ("Argentina", ("Produtor", "Auravant (2020)", "US$ 50–150 por plano", "por usuário", 47)),
 ("Uruguai", ("Estado", "Caravanas SNIG", "US$ 1,38/par", "0 ao produtor", 20)),
 ("Europa e Oceania", None),
 ("Europa", ("Produtor", "OneSoil Pro", "€5–6/ha/ano", "5,5–6,6/ha/ano", 2)),
 ("Alemanha", ("Produtor", "xarvio All-in-1 (valores antigos)", "€10/ha/ano", "≈11/ha/ano", 3)),
 ("Irlanda", ("Produtor de leite", "SenseHub", "€3,50/vaca/mês", "3,85/vaca/mês", 15)),
 ("Irlanda", ("Produtor de leite", "smaXtec + bolus", "€2,50–3/vaca/mês + €35–43", "2,75–3,3 + bolus", 15)),
 ("Nova Zelândia", ("Produtor de leite", "SenseHub (Farm Source)", "NZ$ 2,55–4,41/vaca/mês", "1,5–2,6", 14)),
 ("Nova Zelândia", ("Produtor de leite", "Halter", "NZ$ 9,90/vaca/mês", "≈5,7", 13)),
 ("Austrália", ("Produtor", "Agworld Grower Basic/Pro", "A$ 1.695–3.995/ano", "1.100–2.600/fazenda", 12)),
 ("Austrália", ("Pecuarista", "Smart Paddock (GPS)", "A$ 2/tag/mês", "1,30/cab./mês", 12)),
 ("Israel/UE", ("Produtor irrigante", "Manna Irrigation", "até US$ 5/ha/mês", "30–60/ha/temporada", 4)),
 ("América do Norte", None),
 ("Canadá", ("Produtor", "Climate FieldView", "a partir de C$ 499/ano", "≈360/fazenda", 1)),
 ("EUA", ("Produtor", "Vistoria de lavoura (Mississippi)", "US$ 6–9/acre", "15–22/ha", 5)),
 ("EUA", ("Produtor", "Grid de solo (Iowa)", "US$ 3,25–10/acre", "8–25/ha por coleta", 6)),
 ("EUA", ("Pecuarista", "Cerca virtual (Nofence, Gallagher, Vence)", "US$ 18–45/coleira/ano + coleira", "1,5–4/cab./mês", 17)),
 ("EUA", ("Produtor", "JDLink Ultimate (2019)", "US$ 200/ano", "16,7/máquina/mês", 21)),
 ("EUA", ("Irrigante", "Lindsay Pivot Watch", "US$ 440 com 1º ano", "≈37/pivô/mês", 23)),
]
rows = []
for k, v in T:
    if v is None: rows.append(f"<tr class='grp'><td colspan='5'>{k}</td></tr>"); continue
    rows.append(f"<tr><td><b>{k}</b></td><td>{v[0]}</td><td>{v[1]}{r(v[4])}</td><td>{v[2]}</td><td class='n'>{v[3]}</td></tr>")
doc1.append(f"""<div class='sec'><h1>2. O que o produtor já paga, por país</h1>
<p>Listas de preço, tabelas de extensão rural e imprensa especializada. Muitos fornecedores grandes não publicam preço (EOSDA, Cropwise/Strider, Taranis, Aegro, Agrosmart, telemetria CNH/AGCO/CLAAS); ficaram fora da tabela.</p>
<table><thead><tr><th>País</th><th>Quem paga</th><th>Produto ou serviço</th><th>Valor publicado</th><th class='n'>≈ US$</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>""")

# 3. pagadores institucionais
pag = [
 ("Produtor", "Satélite, agrônomo, coleiras e telemetria comprados separados", "Por hectare, cabeça, máquina ou fazenda", "Assinatura US$ 50–100/fazenda/mês + unidades (tabela da seção 4) + implantação US$ 7,5–15 mil", "Sim"),
 ("Cooperativa, laticínio, trading", f"Plataformas digitais dadas ao associado como fidelização; preço não publicado. Bunge monitora >2 mi ha{r(69)}", "Licença por cooperativa + desconto ao associado", "Licença US$ 30/36/60 mil/ano por faixa + 20% de desconto nas unidades do associado", "Sim"),
 ("Banco e gestor de CPR", f"Brasil: sensoriamento obrigatório no crédito >300 ha desde 01/03/2026{r(25)}; Serasa achou R$ 2,2 bi com divergência de área{r(26)}; AgroCPR: inadimplência −55%{r(27)}", "Por operação, por carteira ou por ha monitorado", "Produto de risco US$ 50/60/100 mil/ano por contrato (≈ US$ 1/ha sobre 50 mil ha)", "Sim"),
 ("Seguradora", f"Prêmio PSR ≈ US$ 93/ha (soja ≈ 77){r(29)}; laudo Proagro R$ 330{r(28)}; EUA: satélite contra fraude rende 23 por 1{r(31)}", "Por apólice ou por laudo de sinistro", "Mesmo produto de risco (1–3% do prêmio ≈ US$ 1–3/ha) + laudo remoto ≈ US$ 60", "Sim"),
 ("Governo", f"Contratos fechados: Conab × INPE ≈ US$ 93 mil/ano{r(34)}; Irlanda, monitoramento da PAC €4,8 mi{r(33)}; Paraguai paga a caravana bovina{r(18)}", "Contrato plurianual por licitação", "US$ 80–150 mil/ano por programa (estimativa de crop estimation ou extensão)", "Não (adicional)"),
 ("Comprador e certificação (EUDR)", f"RTRS paga US$ 2–4 a mais por tonelada{r(38)}; adequação à EUDR custa US$ 1,28–4,20/t{r(39)}; Cota Hilton ≈ US$ 17 mil/t{r(40)}", "Por tonelada ou por lote certificado", "US$ 0,50–1,00/t de grão; US$ 1–2 por cabeça certificada (estimativa)", "Não (adicional)"),
]
pr = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in pag)
doc1.append(f"""<div class='sec'><h1>3. Quem paga além do produtor</h1>
<p>A Help Farm gera um dado verificado da fazenda (condição da lavoura, do rebanho e das máquinas). O mesmo dado vale para seis pagadores diferentes. Abaixo, o que cada um já paga hoje e o preço indicado.</p>
<table><thead><tr><th style='width:15%'>Pagador</th><th style='width:33%'>O que já paga hoje</th><th style='width:16%'>Como paga</th><th style='width:26%'>Preço Help Farm indicado</th><th>No modelo?</th></tr></thead><tbody>{pr}</tbody></table>
<div class='box'><b>Leitura:</b> governo e certificação ainda não entram no caso base da planilha. Numa fazenda de grãos de 5 mil ha (≈ 15 mil t), a certificação a US$ 0,75/t somaria ≈ US$ 11 mil/ano, mais da metade da assinatura de grãos dessa fazenda (US$ 20 mil/ano na faixa C). É a principal alavanca para subir a receita sem subir o preço ao produtor.</div>
<div class='warn'><b class='h'>Atenção:</b> nenhum banco, seguradora ou cooperativa publica quanto paga por fornecedor de monitoramento (Agrotools, Serasa, TerraMagna, EOSDA). Os preços institucionais acima são estimativas a validar nas primeiras reuniões. A CMN 5.267 não diz quem paga o monitoramento: banco ou produtor.</div></div>""")

# 4. preço por país
bands = [("Assinatura da fazenda", "US$/fazenda/mês", [50, 60, 100], [50, 60, 100]),
 ("Pecuária de corte", "US$/cabeça/mês", [0.35, 0.45, 1.20], [0.5, 0.6, 1.0]),
 ("Pecuária de leite", "US$/vaca/mês", [3.0, 4.0, 5.0], [4.0, 4.8, 8.0]),
 ("Lavoura de grãos", "US$/ha/ano", [4, 6, 12], [2.5, 3, 5]),
 ("Alto valor (fruta, café, hortaliça)", "US$/ha/ano", [25, 30, 60], [25, 30, 50]),
 ("Máquinas, pivôs e bombas", "US$/ativo/mês", [20, 25, 40], [35, 42, 70]),
 ("Implantação (taxa única)", "US$/fazenda", [7500, 9000, 15000], [7500, 9000, 15000])]
def fv(v): return (f"{v:,.2f}" if v < 10 and v != int(v) else f"{v:,.0f}").replace(",", "X").replace(".", ",").replace("X", ".")
br_ = "".join(f"<tr><td><b>{a}</b><br><span class='note'>{u}</span></td>" + "".join(f"<td class='n'>{fv(o)} → <b>{fv(nw)}</b></td>" for o, nw in zip(old, new)) + "</tr>" for a, u, new, old in bands)
pc = ""
for p in C["paises"]:
    ad = (f"{p['adesao']:.3f}%".replace(".", ",") if p["adesao"] is not None else "—")
    pc += f"<tr><td><b>{p['pais']}</b></td><td>{p['faixa']}</td><td class='n'>{n0(p['receita'])}</td><td class='n'>{n0(p['margem'])} ({p['margem_pct']}%)</td><td class='n'>{n0(p['fixo'])}</td><td class='n'>{p['equilibrio']}</td><td class='n'>{n0(p['base']) if p['base'] else '—'}</td><td class='n'>{ad}</td></tr>"
doc1.append(f"""<div class='sec'><h1>4. Preço indicado por faixa e por país</h1>
<p>Faixa <b>C</b>: Paraguai, Argentina, Bolívia. Faixa <b>B</b>: Brasil, Uruguai, Chile, México, Colômbia. Faixa <b>A</b>: EUA, Canadá, Europa, Austrália e Nova Zelândia. Cada célula mostra o preço atual da planilha → o preço proposto.</p>
<table><thead><tr><th>Unidade cobrada</th><th class='n'>Faixa C</th><th class='n'>Faixa B</th><th class='n'>Faixa A</th></tr></thead><tbody>{br_}</tbody></table>
<p>Regra usada: o preço tem de ficar <b>abaixo do que o produtor já paga somando os fornecedores</b> (seção 1) e <b>acima do custo de servir</b> (sensor em comodato, conectividade, nuvem e equipe). Grãos subiu porque o satélite isolado já custa US$ 5–11/ha na Europa e a vistoria custa US$ 15–22/ha nos EUA. Corte, leite e máquinas desceram para ficar dentro das faixas publicadas.</p>
<h2>Equilíbrio por país</h2>
<p>Receita e margem por fazenda/mês no mix de fazendas do modelo (mista, grãos, leite, corte e alto valor), depois de royalty RAPP (10%) e marketing (8%). Custo fixo = estrutura da empresa + equipe de campo do país (+ unidade móvel no Paraguai). Na faixa A o custo variável foi multiplicado por 2,5.</p>
<table><thead><tr><th>País</th><th>Faixa</th><th class='n'>Receita/fazenda/mês (US$)</th><th class='n'>Margem/fazenda/mês</th><th class='n'>Custo fixo/mês</th><th class='n'>Fazendas no equilíbrio</th><th class='n'>Estabelecimentos no país</th><th class='n'>Adesão necessária</th></tr></thead><tbody>{pc}</tbody></table>
<p class='note'>Bases: Paraguai CAN 2022{r(57)}; Argentina CNA 2018{r(62)}; Brasil Censo Agro 2017{r(56)}; Uruguai CGA 2024{r(58)}; México 2022{r(67)}; Colômbia CNA 2014{r(68)}; EUA 2022{r(59)}; Espanha 2023{r(63)}; Portugal 2023{r(64)}; França 2023{r(65)}. A adesão é sobre todos os estabelecimentos; sobre as fazendas comerciais o percentual é maior (no Paraguai, {round(Pp['Paraguai']['equilibrio']/3490*100,1)}% das ~3.490 fazendas grandes). Equilíbrio operacional, sem amortizar o desenvolvimento da Fase 1.</p></div>""")

# 5. camada de energia do RAPP
def fu(v): return n0(v)
fn = [("Aprende a assinatura energética de cada ativo", "Garras de corrente e medidor nas bombas, pivôs, ordenha, câmaras frias e secadores. O RAPP aprende o kWh por m³ de água, por hectare irrigado, por litro de leite ou por tonelada seca, além da demanda, do fator de potência e do horário de uso."),
      ("Encontra o desperdício e corrige sem obra", "Demanda contratada acima do necessário, multa de reativos, bomba gasta, irrigação fora da janela de desconto e água aplicada sem o solo pedir. O diagnóstico do DIJA de 2001 achou 13% a 29% de economia só com isso" + r(112) + "; na Espanha, a Linkener promete até 20%" + r(82) + "."),
      ("Projeta a geração própria atividade por atividade", "Com a curva de carga medida, o RAPP separa o que compensa gerar: bombeamento diurno, ordenha e resfriamento, câmara fria, secagem. Dimensiona a usina solar (ou híbrida com diesel e bateria) para cada atividade, com o retorno calculado sobre a conta real, e não sobre uma média."),
      ("Monitora a usina e verifica a economia", "Depois de instalada, a usina vira mais um ativo do RAPP: geração esperada contra a realizada, falhas de inversor e sujeira. Todo mês, a economia é verificada pelo protocolo IPMVP (opção B, por medição isolada)" + r(94) + " e entra no relatório do produtor e do banco que financiou."),
      ("Mede a pegada de carbono por lote", "kWh, diesel e água por quilo produzido entram no certificado de origem ouro/prata/bronze. É o que varejistas e importadores pedem; o crédito de carbono em si vale pouco onde a rede já é limpa (Brasil, Paraguai)" + r(111) + ".")]
fpts = "".join(f"<div class='pt'><i>{i+1}</i><b>{a}.</b> {b}</div>" for i, (a, b) in enumerate(fn))
ge = range_chart("Custo de energia da irrigação — US$ por hectare irrigado por ano", [
 ("EUA · média do bombeamento", 153, 153, "≈ 153 (2023)", "m"),
 ("Brasil · pivô (2.700 kWh/ha)", 150, 150, "≈ 150 (estim.)", "m"),
 ("Brasil · perímetro FAPIJA (estim.)", 410, 410, "≈ 410", "e"),
 ("Argentina · olival (La Rioja)", 300, 850, "300 → 850", "m"),
 ("Paraguai · ANDE (2.700 kWh/ha)", 143, 143, "≈ 143 (estim., US$ 53/MWh)", "m"),
], (0, 0, ""), 900, "US$ por hectare irrigado por ano", f"Fontes: USDA{r(107)}, pivô{r(114)}, FAPIJA{r(111)}, La Rioja{r(32)}, ANDE{r(101)}. Choques de preço: Espanha +600% em 2022{r(108)}; EDIA (Portugal) €47 → €196/MWh{r(109)}.")
ge = ge.replace("Help Farm: </text>", "</text>")
cmp = [("Lindsay FieldNET Pivot Watch", "EUA", "Pressão e status do pivô; sem relatório de kWh", "US$ 440 com o 1º ano", "72,73"),
       ("Valley 365 + Solbras", "EUA / Brasil", "Diagnóstico de máquina; vende pivô solar e sistemas híbridos", "Não publicado; pivô solar paga em ≈ 2 anos contra diesel", "74,84,85"),
       ("Phytech (kit de bomba)", "Israel / EUA", "Pressão, vazão e liga/desliga; energia só pela conta de luz importada", "US$ 850–1.000 + US$ 200 pela integração da conta", "76"),
       ("Linkener", "Espanha", "Telemetria de consumo e potência contratada para regantes", "Mensalidade fixa (não publicada); até −20% na conta", "82"),
       ("Secure Meters Censeo", "Índia / global", "Eficiência de bombas (kWh por m³) em estações", "Não publicado", "78"),
       ("Lorentz (bombas solares)", "Alemanha", "Apps grátis, só para as próprias bombas, via Bluetooth", "Grátis", "77"),
       ("Way2 PowerHub (Auren)", "Brasil", "Medição de energia de 15 em 15 min para indústria e comércio", "Não publicado", "91,92"),
       ("Embrapii Rede Agrointeligente", "Brasil", "Pivô com gestão de energia em tempo real (em desenvolvimento)", "Modelo comercial em 2027", "93"),
       ("SolaQua / energia por assinatura", "Espanha / Brasil", "Usina sem investimento do produtor; PPA de 15–20 anos", "10–20% abaixo da tarifa", "87,89"),
       ("APEP (PG&E) / USDA REAP", "EUA", "Teste de bomba subsidiado; subsídio a solar e eficiência", "US$ 100/teste; até 50% do projeto", "79,80")]
ctab = "".join(f"<tr><td><b>{a}</b>{r(*map(int, e.split(',')))}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d, e in cmp)
ctab += "<tr class='hl'><td><b>Help Farm · RAPP Energia</b></td><td>Paraguai · Brasil · América do Sul</td><td>kWh por ativo + dado agronômico + projeto de geração + verificação da economia + pegada por lote</td><td>Medição incluída no ativo; diagnóstico, 30% da economia e US$/kWp</td></tr>"
pr = PRc
ptab = f"""<tr><td><b>Medição de energia por ativo</b><br><span class='note'>garra de corrente + alertas de demanda e reativos</span></td><td class='n' colspan='3'>incluída no preço do ativo (US$ 20 / 25 / 40 por mês)</td><td>Phytech cobra US$ 200 só para importar a conta{r(76)}</td></tr>
<tr><td><b>Diagnóstico e projeto de geração</b><br><span class='note'>60–90 dias de curva medida; taxa única por fazenda</span></td><td class='n'>{fu(pr['diag']['C'])}</td><td class='n'>{fu(pr['diag']['B'])}</td><td class='n'>{fu(pr['diag']['A'])}</td><td>APEP paga US$ 100 por teste de bomba{r(79)}; a REAP exige auditoria{r(80)}</td></tr>
<tr><td><b>Gestão com economia compartilhada</b><br><span class='note'>sem investimento do produtor; verificação IPMVP</span></td><td class='n' colspan='3'>30% da economia verificada, por 4 anos</td><td>Linkener: até −20% na conta{r(82)}; M&V custa 3–5% do projeto{r(94)}</td></tr>
<tr><td><b>…ou gestão por mensalidade</b><br><span class='note'>US$/fazenda/mês, para quem prefere valor fixo</span></td><td class='n'>{fu(pr['fixo']['C'])}</td><td class='n'>{fu(pr['fixo']['B'])}</td><td class='n'>{fu(pr['fixo']['A'])}</td><td>Linkener cobra mensalidade fixa{r(82)}</td></tr>
<tr><td><b>Originação do projeto solar</b><br><span class='note'>paga pela SPE ou pelo EPC parceiro, não pelo produtor</span></td><td class='n' colspan='3'>4% do investimento da usina</td><td>—</td></tr>
<tr><td><b>Monitoramento da usina + economia verificada</b><br><span class='note'>US$ por kWp instalado por ano</span></td><td class='n'>{pr['mv']['C']}</td><td class='n'>{pr['mv']['B']}</td><td class='n'>{pr['mv']['A']}</td><td>O&M no Brasil: ≈ R$ 100/sistema/mês, R$ 8 de software{r(90)}</td></tr>
<tr><td><b>Distrito de irrigação ou cooperativa</b><br><span class='note'>perímetro inteiro (ex.: FAPIJA)</span></td><td class='n' colspan='3'>diagnóstico ≈ US$ {fu(pr['perim_diag'])} + 30% da economia</td><td>FAPIJA: ≈ R$ 963 mil/ano sem usina{r(111)}</td></tr>"""
lab = [("Conta de energia/ano", "conta"), ("Economia sem obra (15%)", "gest"), ("Help Farm: 30% dessa economia", "hf_gest"),
       ("Usina solar (60% do consumo diurno), kWp", "kwp"), ("Investimento da usina", "capex"), ("Economia da usina/ano", "econ_solar"),
       ("Retorno da usina (anos)", "payback"), ("Help Farm: diagnóstico (uma vez)", "diag"), ("Help Farm: originação (uma vez, paga pela SPE/EPC)", "orig"),
       ("Help Farm: monitoramento da usina/ano", "mv"), ("Help Farm: média por ano (5 anos)", "hf_ano"), ("Ganho líquido do produtor/ano", "prod_liq"), ("Economia total sobre a conta", "pct_conta")]
def cell(k, v):
    if k == "payback": return str(v).replace(".", ",")
    if k == "pct_conta": return f"{v}%"
    if k == "kwp": return fu(v)
    return fu(v)
ftab = "".join(f"<tr{' class=hl' if k in ('hf_ano','prod_liq') else ''}><td>{a}</td>" + "".join(f"<td class='n'>{cell(k, F[b][k])}</td>" for b in "CBA") + "</tr>" for a, k in lab)
ftab += "<tr><td><b>Ganho do produtor ÷ o que paga à Help Farm pela energia</b></td>" + "".join(f"<td class='n'><b>{str(round(F[b]['prod_liq']/F[b]['hf_ano'],1)).replace('.',',')}×</b></td>" for b in "CBA") + "</tr>"
pay = [("Produtor irrigante, leiteiro, fruticultor", "Conta de luz e diesel: 30–50% do custo de quem irriga" + r(83,111), "Diagnóstico + 30% da economia ou mensalidade", "Sim"),
       ("Distrito de irrigação, perímetro, comunidade de regantes", "Conta do bombeamento coletivo; subsídio estadual no DIJA acaba em dez/2026" + r(111), "Contrato do perímetro (diagnóstico + 30%)", "Sim"),
       ("Cooperativa", "Coopercitrus já vende solar ao associado (parceria com a GSE)", "Licença B2B2F com a energia incluída", "Sim (licença)"),
       ("Banco e fundo (FNE Sol, Pronaf, crédito verde)", "FNE para renováveis a 7,5% a.a." + r(104) + "; precisa provar a geração e a economia do projeto financiado", "Relatório de economia verificada por contrato", "Não (adicional)"),
       ("SPE de geração / EPC parceiro", "Usina por PPA 10–20% abaixo da tarifa" + r(87,89) + "; precisa de cliente qualificado e de curva de carga", "Originação de 4% do investimento", "Sim"),
       ("Governo e programas", "USDA REAP (até 50% do projeto, exige auditoria)" + r(80) + "; PRTR na Espanha; PM-KUSUM na Índia" + r(110), "Auditoria e verificação por projeto", "Não (adicional)"),
       ("Comprador e certificação", "Pegada por quilo exigida por varejistas e importadores", "Dentro da certificação por tonelada", "Não (adicional)")]
paytab = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in pay)
eqt = "".join(f"<tr><td><b>{p['pais']}</b></td><td>{p['faixa']}</td><td class='n'>{fu(p['receita'])}</td><td class='n'>+{fu(p['add_r'])} ({str(p['pct']).replace('.',',')}%)</td><td class='n'>{p['eq0']}</td><td class='n'><b>{p['eq1']}</b></td></tr>" for p in EN["paises"])
doc1.append(f"""<div class='sec'><h1>5. Energia: a nova camada do RAPP</h1>
<p>O RAPP aprende a assinatura de funcionamento de cada ativo. A mesma lógica vale para a energia: o motor passa a entender <b>como, quando e para quê</b> a fazenda usa energia, propõe a geração própria que dá retorno em cada atividade e depois prova a economia. São cinco funções novas:</p>
<div class='pts'>{fpts}</div>
<h2>O tamanho do problema</h2>
<p>A irrigação consome ≈ 1.900 PJ por ano no mundo{r(106)}. Nos EUA, o bombeamento custa US$ 3,3 bi por ano{r(107)}; na Espanha, a energia chega a 50% do custo do regante{r(83)}; no Brasil, a geração distribuída rural já soma 5,6 GW, 13% do total{r(96)}, e 116.758 fazendas nos EUA têm solar{r(97)}. O produtor já compra solar; o que falta é saber <b>quanto, onde e se deu certo</b>.</p></div>
<div class='sec'>{ge}
<h2>Quem já vende energia para a fazenda, e quanto cobra</h2>
<table><thead><tr><th style='width:24%'>Oferta</th><th style='width:12%'>Origem</th><th>O que faz</th><th style='width:26%'>Preço</th></tr></thead><tbody>{ctab}</tbody></table>
<div class='box'><b>A brecha:</b> as plataformas de irrigação (Lindsay, Valley, Netafim, Phytech) medem água e pressão, mas nenhuma publica medição de kWh. Os medidores de energia (Linkener, Way2, Censeo) não sabem se a lavoura precisava daquela água. Quem vende solar não mede a fazenda antes nem verifica a economia depois. A Help Farm é a única a juntar as três coisas. O concorrente mais próximo é o projeto da Embrapii, que só chega ao mercado em 2027{r(93)}.</div></div>
<div class='sec'><h2 style='margin-top:0'>Preço proposto da camada de energia (US$)</h2>
<table><thead><tr><th style='width:30%'>Item</th><th class='n'>Faixa C</th><th class='n'>Faixa B</th><th class='n'>Faixa A</th><th style='width:28%'>Referência de mercado</th></tr></thead><tbody>{ptab}</tbody></table>
<p>Regra usada: <b>a medição sozinha quase não se vende</b> (Lorentz dá de graça; Phytech cobra US$ 200 uma vez){r(76,77)}. O valor está na economia provada. Por isso a medição entra no preço do ativo e a Help Farm cobra pelo diagnóstico, por uma parte da economia verificada e pelo monitoramento da usina. A usina em si fica fora do balanço da Help Farm, numa SPE de geração com o know-how Moulin du Soleil / Sollar Machine.</p>
<h2>A conta do produtor: fazenda irrigada de 500 ha de pivô (US$, estimativa)</h2>
<table><thead><tr><th>Item</th><th class='n'>C · Paraguai (US$ 60/MWh)</th><th class='n'>B · Brasil (US$ 75/MWh)</th><th class='n'>A · EUA/Ibéria (US$ 130/MWh)</th></tr></thead><tbody>{ftab}</tbody></table>
<p class='note'>Premissas: 2.700 kWh/ha/ano{r(114)}; usina a US$ 0,70/0,75/1,10 por Wp{r(105)}, 1.600–1.700 kWh/kWp/ano, O&M de US$ 8/MWh; a usina compensa contra a tarifa diurna (US$ 60/87/140 por MWh). No Paraguai a energia é barata e a usina leva 8 anos para se pagar: lá o produto é a gestão e a troca do diesel (pivô solar contra diesel paga em ≈ 2 anos{r(84)}; Chaco: La Betty e Chortitzer já geram{r(99,100)}).</p></div>
<div class='sec'><h2 style='margin-top:0'>Quem paga a camada de energia</h2>
<table><thead><tr><th style='width:22%'>Pagador</th><th>Por que paga</th><th style='width:24%'>Como cobrar</th><th style='width:11%'>No cálculo?</th></tr></thead><tbody>{paytab}</tbody></table>
<h2>Equilíbrio por país com a energia</h2>
<p>Receita adicional média por fazenda Help Farm/mês, supondo que a camada de energia seja contratada por 15% das fazendas na faixa C, 30% na B e 35% na A, e que 20–40% delas façam usina. Margem de contribuição da camada: 65% (engenheiro de energia, garras de corrente e verificação).</p>
<table><thead><tr><th>País</th><th>Faixa</th><th class='n'>Receita/fazenda/mês (US$)</th><th class='n'>+ energia (média)</th><th class='n'>Equilíbrio sem energia</th><th class='n'>Com energia</th></tr></thead><tbody>{eqt}</tbody></table>
<div class='dark'><h3>Veredito: é um plus aceitável?</h3>
<p><b>Sim, como módulo do Help Farm, não como empresa separada.</b> (1) Usa o mesmo sensor, a mesma visita da unidade móvel e o mesmo motor. (2) Transforma o preço em economia: o produtor ganha de 4 a 5 vezes o que paga pela camada. (3) Abre pagadores novos: perímetros, SPEs de geração e bancos de crédito verde. (4) Ninguém pesquisado faz o ciclo completo.</p>
<p style='margin:0'><b>Limites:</b> a receita é menor que a do monitoramento (≈ 8% a mais no Ano 5) e depende de fazendas irrigadas ou de leite; no Paraguai, com energia barata, vale pelo diesel e pela rede fraca; obra de usina fica com a SPE/EPC; os preços não foram validados com clientes. O piloto da FAPIJA é a prova que falta.</p></div></div>""")

# 5. efeito na planilha
pf = C["perfil"]
prof_rows = "".join(f"<tr><td><b>{p}</b></td>" + "".join(f"<td class='n'>{n0(pf[p][b]['antigo'])} → <b>{n0(pf[p][b]['novo'])}</b></td>" for b in "CBA") + "</tr>" for p in pf)
EF = [("Receita no Ano 5 — Paraguai (E2)", "6.677.822", "6.207.077"), ("EBITDA no Ano 5 — Paraguai (E2)", "3.133.262", "2.761.373"),
      ("Receita no Ano 5 — Brasil (E3)", "15.484.214", "14.850.960"), ("Receita no Ano 5 — Faixa A (E5)", "11.457.017", "13.962.771"),
      ("Receita em t7 — Paraguai + Brasil", "22.162.037", "21.058.037"), ("EBITDA em t7 — Paraguai + Brasil", "10.924.576", "10.052.416"),
      ("Valor da empresa na saída (EV)", "65.547.456", "60.314.496"), ("Pré-money justo hoje (TIR alvo)", "9.219.924", "7.520.863"),
      ("Equity necessário com todos os financiadores", "4.076.560", "4.525.467"), ("TIR do investidor de equity", "27,9%", "25,0%"),
      ("MOIC do investidor de equity", "4,5x", "3,9x")]
ef = "".join(f"<tr><td>{a}</td><td class='n'>{b}</td><td class='n'><b>{c}</b></td></tr>" for a, b, c in EF)
doc1.append(f"""<div class='sec'><h1>6. Efeito na planilha do investidor</h1>
<p>Os preços novos foram aplicados na aba Precos do modelo v2 e a planilha de financiadores foi recalculada. Receita por fazenda/mês, por perfil (US$, atual → novo):</p>
<table><thead><tr><th>Perfil de fazenda</th><th class='n'>Faixa C</th><th class='n'>Faixa B</th><th class='n'>Faixa A</th></tr></thead><tbody>{prof_rows}</tbody></table>
<p>Fazendas de grãos ganham (o preço por hectare estava abaixo do mercado); leite e corte perdem (estavam acima). Resultado consolidado, cenário Paraguai + Brasil:</p>
<table><thead><tr><th>Indicador (USD)</th><th class='n'>Tabela anterior</th><th class='n'>Preços de mercado</th></tr></thead><tbody>{ef}</tbody></table>
<h2>A camada de energia no Ano 5 (Paraguai + Brasil, estimativa fora da planilha)</h2>
<table><thead><tr><th>Linha</th><th class='n'>Paraguai</th><th class='n'>Brasil</th></tr></thead><tbody>
<tr><td>Fazendas com a camada de energia</td><td class='n'>{A5['py']['fazendas']}</td><td class='n'>{A5['br']['fazendas']}</td></tr>
<tr><td>Gestão: 30% da economia verificada</td><td class='n'>{n0(A5['py']['gestao'])}</td><td class='n'>{n0(A5['br']['gestao'])}</td></tr>
<tr><td>Diagnósticos no ano</td><td class='n'>{n0(A5['py']['diag'])}</td><td class='n'>{n0(A5['br']['diag'])}</td></tr>
<tr><td>Originação de usinas no ano (4%)</td><td class='n'>{n0(A5['py']['orig'])}</td><td class='n'>{n0(A5['br']['orig'])}</td></tr>
<tr><td>Monitoramento das usinas (US$/kWp)</td><td class='n'>{n0(A5['py']['mv'])}</td><td class='n'>{n0(A5['br']['mv'])}</td></tr>
<tr><td>Dois perímetros do porte da FAPIJA</td><td class='n' colspan='2'>{n0(A5['perimetros'])}</td></tr>
<tr class='hl'><td><b>Receita da camada de energia</b> ({str(A5['pct_receita']).replace('.',',')}% sobre US$ 21,1 mi)</td><td class='n' colspan='2'><b>{n0(A5['total'])}</b></td></tr>
<tr><td>EBITDA da camada (margem de 65%)</td><td class='n' colspan='2'>{n0(A5['ebitda'])}</td></tr>
<tr><td>Valor adicional da empresa na saída ({str(A5['mult']).replace('.',',')}× EBITDA, o múltiplo do modelo)</td><td class='n' colspan='2'>{n0(A5['ev_add'])}</td></tr>
<tr class='hl'><td><b>Pré-money justo: US$ 7,52 mi → </b></td><td class='n' colspan='2'><b>{n0(A5['pre_novo'])}</b></td></tr></tbody></table>
<div class='box'><b>Leitura para o investidor.</b> Com preços ancorados no mercado, o pré-money justo ficou em US$ 7,5 mi, abaixo dos US$ 9 mi negociados. A camada de energia sozinha leva a ≈ US$ {str(round(A5['pre_novo']/1e6,1)).replace('.',',')} mi. A certificação por tonelada (seção 3) ou um contrato de governo no Paraguai completam o caminho até os US$ 9 mi. Esta conta é mais conservadora que a do estudo FAPIJA (US$ 2,9 mi/ano): aqui a margem da venda de energia (PPA) fica na SPE de geração, fora da Help Farm. Para o grupo, a SPE somaria ≈ {str(EN['spe']['mwp']).replace('.',',')} MWp e US$ {str(round(EN['spe']['capex']/1e6,1)).replace('.',',')} mi de usinas até o Ano 5.</div></div>""")

# 6. oportunidade por país
S = [("Brasil", 3, 4, 3, 5, 4, 5, 5), ("Paraguai", 2, 3, 4, 4, 5, 2, 3), ("Uruguai", 3, 3, 4, 4, 4, 2, 2), ("EUA", 5, 4, 2, 3, 1, 5, 4),
     ("Argentina", 2, 3, 3, 3, 4, 4, 4), ("Portugal + Espanha", 4, 3, 3, 3, 3, 3, 5), ("Austrália", 4, 4, 2, 2, 1, 4, 4), ("Chile", 3, 3, 3, 2, 3, 2, 4),
     ("França", 4, 3, 2, 3, 1, 3, 3), ("Nova Zelândia", 4, 4, 2, 2, 1, 2, 2), ("Colômbia", 2, 2, 2, 2, 3, 3, 2), ("México", 2, 2, 2, 2, 2, 4, 4), ("Bolívia", 1, 2, 2, 2, 4, 2, 2)]
S.sort(key=lambda x: -sum(x[1:]))
cols = ["#2E1D10", "#3F7A22", "#5E9F3A", "#9BD06A", "#C9A36B", "#B5642F", "#FFB500"]
bars_rows = [(s[0], list(s[1:]), str(sum(s[1:]))) for s in S]
leg = "<div class='note' style='margin-top:4pt'>" + " · ".join(f"<span style='display:inline-block;width:8pt;height:8pt;background:{c};vertical-align:middle'></span> {t}" for c, t in zip(cols, ["Preço pago", "Pagador recorrente", "Canal de venda", "Exigência que obriga monitorar", "Proximidade", "Tamanho", "Dor de energia"])) + "</div>"
st = "".join(f"<tr><td class='n'>{i+1}</td><td><b>{s[0]}</b></td>" + "".join(f"<td class='n'>{v}</td>" for v in s[1:]) + f"<td class='n'><b>{sum(s[1:])}</b></td></tr>" for i, s in enumerate(S))
doc1.append(f"""<div class='sec'><h1>7. Oportunidade por país</h1>
<p>Cada país recebeu nota de 1 a 5 em sete critérios; o sétimo, novo, é a dor de energia na irrigação (custo, fim de subsídio, diesel e rede fraca), a partir da pesquisa (avaliação Help Farm, nov/2026). Quanto maior, melhor para entrar agora.</p>
{bars('Pontuação de oportunidade (máximo 35)', bars_rows, 35, leg)}
<table><thead><tr><th class='n'>#</th><th>País</th><th class='n'>Preço pago</th><th class='n'>Pagador recorrente</th><th class='n'>Canal</th><th class='n'>Exigência</th><th class='n'>Proximidade</th><th class='n'>Tamanho</th><th class='n'>Energia</th><th class='n'>Total</th></tr></thead><tbody>{st}</tbody></table>
<p class='note'>Exigência = regra que obriga alguém a monitorar a fazenda: crédito rural com sensoriamento (Brasil, CMN 5.267){r(25)}, EUDR para soja e carne exportadas à UE (Paraguai, Uruguai, Argentina){r(36,37)}, rastreabilidade bovina obrigatória (Paraguai, Uruguai, Argentina){r(18,19,20)}, monitoramento da PAC (Europa){r(33)}. Proximidade = idioma, distância e operação a partir do Paraguai.</p></div>""")

# 7. guia
G = [("Paraguai", "Cooperativas menonitas e de grãos (Colonias Unidas, Chortitzer, Fernheim, Neuland), frigoríficos exportadores, Fecoprod/Capeco (SISE-UE)", "Piloto com cooperativa (licença B2B2F) e certificação de lote para a EUDR; no Chaco, troca de diesel por solar nos pivôs"),
     ("Brasil", "Bancos e cooperativas de crédito (CMN 5.267), gestores de CPR, laticínios; distritos de irrigação (FAPIJA/DIJA, Maniçoba) e cooperativas que já vendem solar", "Produto de risco por contrato; leite primeiro, contra Cowmed; nos perímetros irrigados, entrar pela conta de luz"),
     ("Uruguai", "Seguradora estatal, grupos CREA, frigoríficos", "Rastreabilidade bovina do SNIG + seguro"),
     ("Argentina", "Grupos CREA, seguradoras de granizo, acopiadores", "Grãos por hectare; laudo remoto para seguro"),
     ("EUA", "Agrônomos independentes, revendas, Medicare… não: seguradoras de safra (RMA)", "Camada preditiva sobre dados de coleiras, pivôs e máquinas já instalados, via parceiro local"),
     ("Portugal + Espanha", "Cooperativas, comunidades de regantes, EDIA, IFAP/FEGA (monitoramento da PAC)", "Energia primeiro: diagnóstico e economia verificada para regantes; alto valor e irrigação"),
     ("Austrália e Nova Zelândia", "Pecuária extensiva e leite", "Integração com Halter, SenseHub e Ceres Tag: só a camada preditiva")]
G[4] = ("EUA", "Agrônomos independentes, revendas e seguradoras de safra", "Camada preditiva sobre dados de coleiras, pivôs e máquinas já instalados, via parceiro local")
gt = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in G)
doc1.append(f"""<div class='sec'><h1>8. Guia para a equipe de prospecção</h1>
<table><thead><tr><th style='width:16%'>Mercado</th><th>Quem procurar</th><th>Como entrar</th></tr></thead><tbody>{gt}</tbody></table>
<h2>O que vale para todos os mercados</h2>
<div class='pts'><div class='pt'><i>1</i>Medir no piloto do Paraguai a perda evitada por fazenda (safra, rebanho, máquina) e o custo real por visita da unidade móvel. É o número que sustenta preço e valuation.</div>
<div class='pt'><i>2</i>Manter a tabela por unidade (hectare, cabeça, máquina) em cada moeda, com o kit em comodato e a implantação cobrada à parte.</div>
<div class='pt'><i>3</i>Vender o mesmo dado a mais de um pagador: produtor, cooperativa, banco e seguradora na mesma fazenda.</div><div class='pt'><i>4</i>Em fazenda irrigada ou de leite, abrir a conversa pela conta de luz: pedir 12 faturas, medir 60 dias e voltar com a economia em reais.</div></div>
<div class='warn'><b class='h'>Limites desta pesquisa.</b> Muitos fornecedores não publicam preço; vários valores são antigos (2017–2021) ou de fonte secundária, como marcado. Preços institucionais (banco, seguradora, cooperativa, governo, certificação) são estimativas. Faltaram dados de base para Chile, Bolívia, Austrália e Nova Zelândia. Os preços da Help Farm ainda não foram validados com clientes.</div></div>""")

refs_html = "<div class='sec'><h1>Referências</h1><ol class='refs'>" + "".join(f"<li><b>{H.escape(a)}</b> — {u}</li>" for a, u in REFS) + "</ol></div>"
open("doc1.html", "w").write(page("".join(doc1) + refs_html))

# ============================================================== DOC 2
comp = [("Climate FieldView (Bayer)", "EUA", "Dados de lavoura e máquina", "C$ 499/ano por fazenda; >250 mi acres", 1, 41),
 ("John Deere Operations Center", "EUA", "Máquinas e lavoura", "Plataforma grátis; JDLink US$ 200/ano; 485 mi acres", 21, 42),
 ("Solinftec", "Brasil", "Lavoura, telemetria, robô", "Contratos de 5 anos; ≈ US$ 5/ha; 13 mi ha", 7, 43),
 ("Agrotools", "Brasil", "Risco socioambiental e de crédito", "Pago por trading, frigorífico e banco; 4,5 mi geo-ids", 44, 44),
 ("Halter", "Nova Zelândia", "Pecuária (coleira, cerca virtual)", "NZ$ 9,90/vaca/mês; >1 mi coleiras", 13, 45),
 ("SenseHub (MSD/Allflex)", "Global", "Leite (reprodução e saúde)", "US$ 1,5–3,9/vaca/mês; >2 mi vacas nos EUA", 14, 46),
 ("Cowmed", "Brasil", "Leite", "R$ 22–23/vaca/mês", 16, 16),
 ("CropX / Arable", "Israel / EUA", "Sensores de solo e clima", "US$ 300–5.000/ano por aparelho (secundária)", 70, 70),
 ("xarvio (BASF)", "Alemanha", "Doenças, mapas de aplicação", "€5–10/ha; ≈US$ 500/ano na Argentina", 3, 50),
 ("Auravant / Kilimo", "Argentina", "Software de lavoura; irrigação", "US$ 50–150 por plano; empresas pagam a irrigação", 47, 48),
 ("AgroPortal (NWF)", "Paraguai", "Rastreabilidade da pecuária", "Via frigorífico, sem custo ao produtor", 51, 51),
 ("Valley 365 + Solbras", "EUA / Brasil", "Pivôs; vende pivô solar e sistemas híbridos", "Sem kWh no software; pivô solar paga em ≈ 2 anos contra diesel", 84, 84),
 ("Phytech (kit de bomba)", "Israel / EUA", "Bomba: pressão, vazão, liga/desliga", "US$ 850–1.000; +US$ 200 para importar a conta de luz", 76, 76),
 ("Linkener", "Espanha", "Energia de regantes (potência, consumo)", "Mensalidade fixa; até −20% na conta; sem dado agronômico", 82, 82),
 ("Way2 PowerHub (Auren)", "Brasil", "Medição de energia na indústria", "Não publicado; não atende fazenda", 91, 91),
 ("Embrapii Rede Agrointeligente", "Brasil", "Pivô com gestão de energia", "Em desenvolvimento; comercial em 2027", 93, 93)]
ct = "".join(f"<tr><td><b>{a}</b>{r(s)}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d, s, _ in comp)
ct += "<tr class='hl'><td><b>Help Farm</b></td><td>Paraguai · Brasil · América do Sul</td><td>Lavoura + rebanho + máquinas + irrigação + energia, com assinatura por ativo e visita da unidade móvel</td><td>US$ 4–12/ha; US$ 0,35–1,20/cab.; US$ 3–5/vaca; US$ 20–40/máquina; energia: 30% da economia verificada; vários pagadores</td></tr>"
cards = [("Uma assinatura por ativo, em todos os domínios", "Halter e SenseHub aprendem o normal de cada animal; CropX, o de cada talhão; a Deere, o de cada máquina. Nenhum player pesquisado faz os quatro juntos. O motor RAPP compara cada talhão, animal e máquina com ele mesmo.", "Um contrato substitui quatro fornecedores."),
 ("Gente na fazenda, não só software", f"Só 20% dos estabelecimentos do Brasil recebem assistência técnica{r(56)}. A unidade móvel leva dois técnicos, drones e instrumentos, instala os sensores e calibra a assinatura de cada fazenda.", "Software sozinho deixa esse vazio: na Auravant, só 9% dos usuários pagam."),
 ("Vários pagadores para o mesmo dado", f"Agrotools recebe de bancos e tradings; Kilimo, de empresas; a Farmers Edge pertence a uma seguradora{r(44,48,49)}. A Help Farm cobra do produtor e vende o mesmo dado verificado a cooperativa, banco, seguradora e comprador.", "Menos risco de depender de um só cliente."),
 ("Preço dentro das faixas que já se pagam", "Grãos a US$ 4–12/ha fica entre o satélite (US$ 0,2–11) e o agrônomo (US$ 15–22 nos EUA). Leite a US$ 3–5/vaca fica entre SenseHub e Halter. Máquinas a US$ 20–40 fica entre JDLink e a telemetria pós-venda.", "Fácil de comparar numa proposta: ninguém precisa criar orçamento novo."),
 ("Exigências que obrigam alguém a monitorar", f"Crédito rural com sensoriamento no Brasil{r(25)}; EUDR para soja e carne exportadas à Europa{r(36)}; rastreabilidade bovina obrigatória no Paraguai, Uruguai e Argentina{r(18,19,20)}.", "O comprador já tem verba e prazo."),
 ("Certidão de nascimento do lote", f"O certificado de origem gravado em blockchain prova práticas e ausência de desmatamento desde 2020. A RTRS paga US$ 2–4 a mais por tonelada{r(38)}; a adequação à EUDR custa US$ 1,28–4,20/t{r(39)}.", "Nova receita por tonelada sem cobrar mais do produtor."),
 ("Terreno livre no Paraguai", f"No Paraguai só encontramos rastreabilidade via frigorífico (AgroPortal){r(51)}, sem monitoramento preditivo. Base: 291 mil propriedades{r(57)}, ~13 mi cabeças e ~3,6 mi ha de soja.", "Primeiro a chegar define o padrão com cooperativas e frigoríficos."),
 ("Agronomia e energia no mesmo dado", f"Lindsay, Valley, Netafim e Phytech medem água e pressão, mas não publicam medição de kWh{r(73,74,75,76)}. Linkener e Way2 medem energia, mas não sabem se a lavoura precisava da água{r(82,91)}. O RAPP sabe as duas coisas: corta o kWh que não vira produção.", "Economia de 15% sem obra numa fazenda irrigada (diagnóstico do DIJA: 13–29%)."),
 ("Do diagnóstico à economia verificada", f"Quem vende solar não mede a fazenda antes nem prova a economia depois. O RAPP mede a curva de carga, projeta a usina atividade por atividade (bombeamento, ordenha, frio, secagem), monitora a geração e verifica a economia pelo IPMVP{r(94)}.", "O produtor ganha 4–5× o que paga; o banco do crédito verde recebe a prova."),
 ("Equilíbrio com pouca adesão", "Em todos os países pesquisados, 37 a 63 fazendas pagando cobrem a operação local, já com a energia. No Paraguai, menos de 2% das fazendas grandes.", f"Perda evitada é grande: a seca de 2021/22 tirou 58% da soja paraguaia{r(53)}.")]
cd = "".join(f"<div class='card'><h3><em>{i+1:02d}</em>{a}</h3>{b}<div class='s'>{c}</div></div>" for i, (a, b, c) in enumerate(cards))
quick = [("Monitoramento preditivo por ativo", "Por campo", "Por animal", "Por máquina", "Não (risco)", "Sim, em todos"),
 ("Domínios", "Lavoura", "Leite ou corte", "Máquinas", "Crédito e socioambiental", "Lavoura, rebanho, máquinas, irrigação, energia"),
 ("Equipamento", "Do produtor", "Coleira do fornecedor", "Da máquina", "Nenhum (satélite)", "Kit em comodato + o que já existe"),
 ("Visita técnica", "Não", "Revenda", "Concessionária", "Não", "Unidade móvel com 2 técnicos"),
 ("Pagadores", "Produtor", "Produtor", "Produtor", "Banco, trading", "Produtor, cooperativa, banco, seguradora, comprador"),
 ("Energia (kWh, projeto de geração, economia verificada)", "Não", "Não", "Não", "Não", "Sim, as três"),
 ("Preço de referência", "US$ 0,2–11/ha", "US$ 1,5–5,7/vaca", "US$ 17–50/máq.", "Não público", "US$ 4–12/ha; 3–5/vaca; 20–40/máq.; 30% da economia")]
qt = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td><td><b>{f}</b></td></tr>" for a, b, c, d, e, f in quick)
doc2 = f"""<div class='sec first'><h1>1. O que os sistemas pesquisados fazem</h1>
<p>Players de monitoramento agro e de energia na fazenda e quanto cobram, a partir do Panorama de mercado e conceito de valor v2 (05/11/2026).</p>
<table><thead><tr><th style='width:24%'>Sistema</th><th>Sede</th><th>O que faz</th><th style='width:34%'>Modelo e preço</th></tr></thead><tbody>{ct}</tbody></table>
</div>
<div class='sec'><h1>2. Onde a Help Farm se diferencia</h1><div class='cards'>{cd[:cd.find("<div class='card'><h3><em>07")]}</div></div>
<div class='sec'><h1>2. Onde a Help Farm se diferencia (continuação)</h1><div class='cards'>{cd[cd.find("<div class='card'><h3><em>07"):]}</div></div>
<div class='sec'><h1>3. Comparação rápida</h1>
<table><thead><tr><th>Item</th><th>Satélite (FieldView, xarvio)</th><th>Coleira (Halter, SenseHub)</th><th>Telemetria (Deere)</th><th>Risco (Agrotools)</th><th>Help Farm</th></tr></thead><tbody>{qt}</tbody></table>
<div class='warn' style='font-size:8pt'><b class='h'>Onde os concorrentes estão à frente (cuidado nas reuniões)</b><ul>
<li><b>Escala de dados:</b> Deere tem 485 mi acres, FieldView mais de 250 mi, Solinftec 13 mi ha{r(41,42,43)}. A Help Farm começa com 5 fazendas-piloto.</li>
<li><b>Capital e distribuição:</b> Halter captou US$ 220 mi e vale US$ 2 bi; Solinftec, R$ 1,3 bi; Taranis, US$ 100 mi{r(45,43,71)}. Eles chegam pela revenda, concessionária e veterinário.</li>
<li><b>Produto validado:</b> SenseHub monitora mais de 2 mi vacas nos EUA{r(46)}. No leite, a Help Farm compete com sensores já instalados: melhor integrar do que substituir.</li>
<li><b>Custo de campo:</b> a Farmers Edge caiu cerca de 99% desde o IPO{r(49)}. A Help Farm precisa provar no piloto o custo por visita contra a receita por hectare.</li>
<li><b>Energia:</b> a Valley já vende pivô solar no Brasil (Solbras){r(84,85)} e a Embrapii lança gestão de energia no pivô em 2027{r(93)}. A janela para ocupar a posição é de 1 a 2 anos. Obra de usina não é negócio da Help Farm: fica com a SPE/EPC parceira.</li>
<li><b>Preços da Help Farm</b> ainda não foram validados com clientes. Apresentar como tabela de referência.</li></ul></div>
<div class='dark' style='font-size:8.4pt;padding:8pt 11pt'><h3>Em uma frase, por tipo de cliente</h3>
<p><b>Produtor:</b> satélite, sensores, agrônomo e alerta antes do problema num só contrato, por menos do que a soma dos fornecedores.</p>
<p><b>Cooperativa:</b> monitoramento de todos os associados com 20% de desconto e um painel da carteira inteira.</p>
<p><b>Banco:</b> o monitoramento que a CMN 5.267 exige, já feito, com a condição da lavoura e do rebanho que garante o crédito.</p>
<p><b>Seguradora:</b> alerta antes do sinistro e laudo remoto, por uma fração do prêmio.</p>
<p><b>Produtor irrigante:</b> a conta de luz cai de 15% a 45% e paga a assinatura; você só divide a economia que aparecer na fatura.</p>
<p><b>Distrito de irrigação:</b> diagnóstico do perímetro, usina dimensionada pela curva medida e economia verificada todo mês.</p>
<p style='margin:0'><b>Comprador:</b> cada lote com certidão de nascimento: origem, práticas e nível ouro, prata ou bronze.</p></div></div>"""
used = [1, 3, 7, 13, 14, 16, 18, 19, 20, 21, 25, 36, 38, 39, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 53, 56, 57, 70, 71, 73, 74, 75, 76, 82, 84, 85, 91, 93, 94]
refs2 = "<div class='sec'><h1>Referências</h1><p class='note'>Numeração igual à do documento Panorama de mercado e conceito de valor v2.</p><ol class='refs'>" + "".join(f"<li value='{i}'><b>{H.escape(REFS[i-1][0])}</b> — {REFS[i-1][1]}</li>" for i in used) + "</ol></div>"
open("doc2.html", "w").write(page(doc2 + refs2))

c1 = cover("Estudo de mercado · prospecção internacional · versão 2 com energia", "Quanto o mundo paga por <em>monitorar a fazenda</em> e pela energia que ela gasta",
           "Preços pagos por produtores, cooperativas, bancos, seguradoras, governos e compradores em 13 países, e a nova camada de energia do RAPP: diagnóstico, geração própria e economia verificada na irrigação.",
           [("13 países", "Américas, Europa e Oceania"), (f"{len(REFS)} fontes", "listas de preço, contratos, tabelas oficiais e censos"), (f"{F['B']['pct_conta']}% menos", "na conta de luz de uma fazenda irrigada (estimativa)")],
           "file:///home/claude/hfp2/c3.jpg")
c2 = cover("Guia da equipe de prospecção · novembro de 2026", "Por que a Help Farm ganha dos <em>sistemas que já existem</em>",
           "O que produtores e instituições pagam hoje por monitoramento agro e por energia na fazenda, o que a Help Farm faz diferente e onde os concorrentes ainda estão à frente. Versão 2, com a camada de energia do RAPP.",
           [("5 domínios", "lavoura, rebanho, máquinas, irrigação e energia numa só assinatura"), ("1 unidade móvel", "dois técnicos, drones e instrumentos na fazenda"), ("6 pagadores", "o mesmo dado vendido a quem já tem verba")],
           "file:///home/claude/hfp2/c2.jpg")
open("cover1.html", "w").write(c1); open("cover2.html", "w").write(c2)

HD = "<div style='font-family:Inter,Arial;font-size:7pt;color:#5E4A38;width:100%;padding:0 15mm;display:flex;justify-content:space-between'><span><b style='color:#2E1D10'>Help Farm</b> · {t}</span><span>Novembro de 2026</span></div>"
FT = "<div style='font-family:Inter,Arial;font-size:7pt;color:#5E4A38;width:100%;padding:0 15mm;display:flex;justify-content:space-between'><span>{f}</span><span>Página <span class='pageNumber'></span> de <span class='totalPages'></span></span></div>"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        for cv, body, out, t, f in [("cover1.html", "doc1.html", "HelpFarm_Panorama_Mercado_Conceito_de_Valor_v2.pdf", "Panorama de mercado e conceito de valor · v2", "Estudo para investidores e equipe de prospecção · helpcure.com.py/helpfarm"),
                                    ("cover2.html", "doc2.html", "HelpFarm_Diferenciais_Competitivos_v2.pdf", "Diferenciais competitivos v2 · Equipe de prospecção", "Uso interno da equipe comercial")]:
            await pg.goto(f"file:///home/claude/hfp2/{cv}"); await pg.wait_for_timeout(300); await pg.pdf(path="_c.pdf", format="A4", print_background=True)
            await pg.goto(f"file:///home/claude/hfp2/{body}"); await pg.wait_for_timeout(300)
            await pg.pdf(path="_b.pdf", format="A4", print_background=True, display_header_footer=True, header_template=HD.format(t=t), footer_template=FT.format(f=f), margin=dict(top="17mm", bottom="15mm", left="15mm", right="15mm"))
            w = PdfWriter()
            for x in ["_c.pdf", "_b.pdf"]:
                for q in PdfReader(x).pages: w.add_page(q)
            w.write(out); print(out, len(w.pages))
        await b.close()
asyncio.run(main())
