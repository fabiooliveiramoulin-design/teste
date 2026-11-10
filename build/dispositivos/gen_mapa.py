import asyncio, math
from common import *
CAT = {"s": ("#2F6E9E", "Solo, água e clima"), "l": ("#5E9F3A", "Lavoura"), "r": ("#B5642F", "Rebanho"), "m": ("#8A5A00", "Máquinas, irrigação e energia"), "c": ("#5E4A38", "Conectividade")}
# nome, cat, função, ajuda, exemplos
D = [
 ("Analisador de Nuvens", "HF1", "Vê as nuvens chegando e confirma com o satélite", "Alerta de chuva, granizo e tempestade em até 10 min: dá tempo de parar a pulverização, recolher máquinas ou adiantar a colheita", "Exclusivo Help Farm"),
 ("Estação meteorológica", "s", "Mede chuva, vento, temperatura e umidade no local", "Aviso de geada e escolha da janela certa para pulverizar", "Davis Vantage Pro2, METER ATMOS 41"),
 ("Imagens de satélite", "s", "Mostram o vigor de cada talhão a cada poucos dias", "Acha manchas de falha antes de o olho ver", "Sentinel-2, Planet"),
 ("Sonda de umidade do solo", "s", "Mede a água em várias profundidades", "Irrigar na hora certa, sem desperdiçar água e energia", "Sentek Drill & Drop, METER TEROS"),
 ("Sensor de nível de água", "s", "Mede o nível de caixas, represas e bebedouros", "Gado nunca fica sem água; vazamento aparece na hora", "Sensores LoRaWAN de nível"),
 ("Monitor de pivô", "m", "Informa posição, pressão e se o pivô parou", "Pivô parado avisa na hora, sem perder dias de irrigação", "Lindsay FieldNET Pivot Watch, Valley 365"),
 ("Sensor de vibração em motores e bombas", "m", "Mede vibração e temperatura do equipamento", "Conserta antes de quebrar, fora da safra", "Dragino LHT65N-VIB, Khomp"),
 ("Medidor de energia", "m", "Mede o consumo de cada máquina, bomba e pivô", "Corta desperdício e mostra onde vale gerar energia solar", "Garras de corrente com rádio"),
 ("Avaliador de Trabalho em Campo", "HF2", "Drone automático fotografa a colheita e o plantio 6 vezes por hora", "Mostra área feita, ritmo, paradas e hora de término: a logística acompanha o campo em tempo real", "Exclusivo Help Farm"),
 ("Telemetria das máquinas", "m", "Lê horas, consumo e códigos de falha dos tratores e colhedoras", "Manutenção no momento certo e frota bem usada", "John Deere JDLink, CNH AFS Connect"),
 ("Gateway da fazenda", "c", "Recebe os sensores por rádio e roda o RAPP no local", "O alerta sai mesmo sem internet", "Gateways LoRaWAN com computador de borda"),
 ("Balança de passagem", "r", "Pesa o animal quando ele vai beber água", "Ganho de peso diário sem tirar o gado do pasto", "Balanças automáticas de bebedouro"),
 ("Bolus ruminal", "r", "Mede a temperatura interna e o consumo de água do animal", "Febre aparece antes do sintoma", "smaXtec"),
 ("Coleira ou brinco inteligente", "r", "Mede ruminação, atividade e cio", "Animal doente ou no cio é visto no mesmo dia", "MSD SenseHub, CowManager"),
 ("Armadilha inteligente de pragas", "l", "Fotografa e conta os insetos capturados", "Aplica defensivo só quando a praga passa do limite", "Trapview"),
 ("Drone de mapeamento", "l", "Faz mapas de vigor detalhados do talhão", "Mostra onde corrigir e onde a lavoura falha", "DJI Mavic 3 Multispectral"),
]
W, H = 297, 210; cx, cy, rx, ry = 148.5, 113, 113, 64
svg = [f"<svg viewBox='0 0 {W} {H}' style='position:absolute;inset:0;width:297mm;height:210mm'>"]
order_xy = [(148.5, 40), (237, 40)] + [(257, y) for y in (65, 89, 113, 137, 161)] + [(237, 186), (148.5, 186), (60, 186)] + [(40, y) for y in (161, 137, 113, 89, 65)] + [(60, 40)]
pos = order_xy
for (x, y) in pos: svg.append(f"<line x1='{cx}' y1='{cy}' x2='{x:.1f}' y2='{y:.1f}' stroke='#C9A36B' stroke-width='.45' stroke-dasharray='1.4 1.2'/>")
svg.append(f"<circle cx='{cx}' cy='{cy}' r='33' fill='#F6EFE3'/><circle cx='{cx}' cy='{cy}' r='27' fill='#2E1D10'/><circle cx='{cx}' cy='{cy}' r='27' fill='none' stroke='#8FCB5A' stroke-width='1'/>")
svg.append(f"<text x='{cx}' y='{cy-2}' text-anchor='middle' font-family='Inter Display,Inter' font-weight='800' font-size='13' fill='#8FCB5A'>RAPP</text><text x='{cx}' y='{cy+5}' text-anchor='middle' font-size='3.4' fill='#F4EBDD' font-weight='600'>o cérebro digital</text><text x='{cx}' y='{cy+9.5}' text-anchor='middle' font-size='3.1' fill='#C9B79C'>da fazenda · desde 2010</text>")
svg.append("</svg>")
boxes = ""
for (x, y), (n, c, *_r) in zip(pos, D):
    w, h = 50, 13
    if c == "HF1": st = "background:#3F7A22;color:#fff;border:0;box-shadow:0 1.5mm 4mm rgba(63,122,34,.35)"; tag = "<i style='display:block;font-style:normal;font-size:6pt;letter-spacing:.12em;color:#D7F0C0;font-weight:700'>EXCLUSIVO HELP FARM</i>"
    elif c == "HF2": st = "background:#FFB500;color:#2E1D10;border:0;box-shadow:0 1.5mm 4mm rgba(255,181,0,.35)"; tag = "<i style='display:block;font-style:normal;font-size:6pt;letter-spacing:.12em;color:#6B4600;font-weight:700'>EXCLUSIVO HELP FARM</i>"
    else: st = f"background:#fff;border:.5mm solid #E2D3BA;border-left:2.2mm solid {CAT[c][0]}"; tag = ""
    boxes += f"<div style='position:absolute;left:{x-w/2:.1f}mm;top:{y-h/2:.1f}mm;width:{w}mm;min-height:{h}mm;{st};border-radius:2.5mm;padding:1.6mm 2.4mm;display:flex;flex-direction:column;justify-content:center;font-size:8.2pt;font-weight:700;line-height:1.15'>{tag}{n}</div>"
leg = "".join(f"<span style='display:inline-flex;align-items:center;gap:1.4mm;margin-right:5mm'><i style='width:3mm;height:3mm;border-radius:.6mm;background:{v[0]}'></i>{v[1]}</span>" for v in CAT.values())
p1 = f"""<div class='pg' style='width:297mm;height:210mm'><div class='secband'></div>
<div style='position:absolute;left:14mm;top:10mm;right:14mm;display:flex;justify-content:space-between;align-items:flex-start'>
<div><span class='eyebrow'>Os dispositivos Help Farm</span><div style='font-family:"Inter Display",Inter;font-size:20pt;font-weight:800;line-height:1.05;letter-spacing:-.015em'>Muitos sensores, um único cérebro digital: o RAPP</div></div>
<div style='margin-top:2mm'>{wordmark(14, False)}</div></div>
{''.join(svg)}{boxes}
<div style='position:absolute;left:14mm;bottom:7mm;right:14mm;display:flex;justify-content:space-between;font-size:7.4pt;color:#5E4A38'><div>{leg}</div><div>Verde e amarelo: dispositivos exclusivos Help Farm</div></div></div>"""
rows = ""
for n, c, f, a, e in D:
    hf = c.startswith("HF")
    col = "#3F7A22" if c == "HF1" else "#B98400" if c == "HF2" else CAT[c][0]
    rows += f"<tr{' style=\"background:#F6EFE3\"' if hf else ''}><td><span style='display:inline-block;width:2.4mm;height:2.4mm;border-radius:.5mm;background:{col};margin-right:1.6mm'></span><b>{n}</b></td><td>{f}</td><td>{a}</td><td class='muted'>{'<b style=\"color:'+col+'\">'+e+'</b>' if hf else e}</td></tr>"
p2 = f"""<div class='pg' style='width:297mm;height:210mm'><div class='secband'></div><div style='padding:13mm 14mm 0'>
<span class='eyebrow'>O que cada dispositivo faz</span><h1 style='font-size:18pt'>A função em poucas palavras e o ganho para a fazenda</h1>
<table style='font-size:7.6pt' class='tb'><thead><tr><th style='width:56mm'>Dispositivo</th><th style='width:66mm'>O que faz</th><th>Como ajuda a fazenda</th><th style='width:48mm'>Exemplos no mercado</th></tr></thead><tbody>{rows}</tbody></table>
<p class='note' style='margin-top:2.5mm'>Os exemplos são equipamentos que já existem e são vendidos hoje; servem de referência e não indicam parceria. A Help Farm escolhe o conjunto de cada fazenda conforme a atividade e não depende de uma marca.</p></div>
<div class='foot' style='left:14mm;right:14mm'>{wordmark(8.5, False)}<span>Dispositivos Help Farm · tudo controlado pelo RAPP</span><span>2</span></div></div>"""
CR = [("Nuvem chegando + colheita pela metade", "Analisador de Nuvens + Avaliador de Trabalho em Campo", "O RAPP calcula se dá para terminar o talhão antes da chuva e avisa para reforçar ou recolher as máquinas."),
      ("Solo secando + energia mais cara", "Sonda de umidade + estação + medidor de energia", "Irriga só o necessário e no horário em que a energia custa menos."),
      ("Animal comendo e bebendo menos", "Coleira + bolus + balança + nível de água", "Separa o animal e chama o veterinário antes da febre virar perda."),
      ("Motor vibrando diferente", "Sensor de vibração + telemetria + monitor de pivô", "A peça é comprada e trocada antes da safra, sem parar a irrigação."),
      ("Praga passando do limite", "Armadilha inteligente + satélite + drone de mapeamento", "Aplica só no talhão afetado, na janela de vento certa da estação.")]
cr = "".join(f"<div class='card'><h3 style='color:#3F7A22'>{a}</h3><p class='muted' style='font-size:7.6pt;margin:0 0 1.5mm'><b>{b}</b></p><p style='margin:0;font-size:8.2pt'>{c}</p></div>" for a, b, c in CR)
p3 = f"""<div class='pg' style='width:297mm;height:210mm'><div class='secband'></div><div style='padding:13mm 14mm 0'>
<span class='eyebrow'>Um único cérebro digital</span><h1 style='font-size:18pt'>Cada sensor sozinho é um número. O RAPP transforma tudo em decisão.</h1>
<p style='max-width:250mm'>Todos os dispositivos da fazenda, os de mercado e os exclusivos Help Farm, enviam as medições para o <b>RAPP</b>, o motor de inteligência artificial construído desde 2010. Ele aprende o normal de cada talhão, animal e máquina, cruza as medições entre si e avisa antes do problema, já com a ação recomendada. No agronegócio, a licença do RAPP é exclusiva da Help Farm.</p>
<h2>Exemplos de cruzamentos que só o RAPP faz</h2>
<div style='display:grid;grid-template-columns:repeat(5,1fr);gap:3mm'>{cr}</div>
<div style='display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:5mm'>
<div style='display:grid;grid-template-columns:50mm 1fr;gap:4mm;align-items:center;background:#3F7A22;color:#fff;border-radius:3.5mm;padding:3mm'><img src='file:///home/claude/hfm/img/hero.jpg' style='width:50mm;height:34mm;object-fit:cover;border-radius:2.5mm'><div><b style='font-size:11pt'>Analisador de Nuvens</b><br><span style='font-size:8.3pt'>Exclusivo Help Farm. Nasceu para usinas solares que não podiam perder energia; na fazenda, confirma a nuvem com o satélite e avisa em até 10 minutos.</span></div></div>
<div style='display:grid;grid-template-columns:50mm 1fr;gap:4mm;align-items:center;background:#FFB500;color:#2E1D10;border-radius:3.5mm;padding:3mm'><img src='file:///home/claude/hfa/drone.jpg' style='width:50mm;height:34mm;object-fit:cover;border-radius:2.5mm'><div><b style='font-size:11pt'>Avaliador de Trabalho em Campo</b><br><span style='font-size:8.3pt'>Exclusivo Help Farm. Drone automático que sai da unidade móvel e acompanha a colheita e o plantio seis vezes por hora.</span></div></div></div>
<p class='note' style='margin-top:2mm'>Imagens dos dispositivos exclusivos: ilustrativas, geradas por IA.</p></div>
<div class='foot' style='left:14mm;right:14mm'>{wordmark(8.5, False)}<span>Dispositivos Help Farm · tudo controlado pelo RAPP</span><span>3</span></div></div>"""
asyncio.run(render(page(p1 + p2 + p3).replace("</style>", ".tb td{padding:.75mm 2mm;line-height:1.3}</style>").replace("@page{size:A4;margin:0}", "@page{size:297mm 210mm;margin:0}"), "/home/claude/hfd/HelpFarm_Dispositivos_RAPP.pdf", True))
