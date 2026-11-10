import asyncio
from common import *
L = "Avaliador de Trabalho em Campo · apresentação"; A = "file:///home/claude/hfa/"; S = "file:///home/claude/teste/helpfarm/img/"
from PIL import Image
for n in ("movel-drone", "movel-fazenda"):
    Image.open(f"/home/claude/teste/helpfarm/img/{'f/' if n=='movel-drone' else ''}{n}.webp").convert("RGB").save(f"/home/claude/hfd/{n}.jpg", quality=88)
D = "file:///home/claude/hfd/"
p1 = cover(A + "drone.jpg", "Dispositivo exclusivo Help Farm", "Avaliador de<br>Trabalho <span style='color:#8FCB5A'>em Campo</span>",
  "O drone automático que sai da unidade móvel e acompanha a colheita e o plantio seis vezes por hora, mostrando quanto já foi feito, o ritmo e a hora de terminar.",
  [("6× por hora", "um voo a cada 10 minutos"), ("Automático", "decola e pousa sozinho no teto da unidade móvel"), ("ha e ha/h", "área feita e ritmo de trabalho"), ("Tempo real", "paradas e previsão de término")])
p2 = f"""<div class='pg'><div class='secband'></div><div class='pad'>
<span class='eyebrow'>O problema</span><h1>Na safra, quem está longe do talhão não sabe como a colheita está indo</h1>
<p>O dono, o gerente, a logística dos caminhões e o armazém dependem de ligações e de estimativas. Uma parada de meia hora, uma colhedora mais lenta ou um talhão que vai terminar depois da chuva só aparecem quando já é tarde para reagir.</p>
<h2>A solução</h2>
<div class='grid2' style='align-items:center'>
<div><p>O <b>Avaliador de Trabalho em Campo</b> é um drone automático que fica numa base no teto da unidade móvel Help Farm. <b>A cada 10 minutos</b> ele decola, fotografa o talhão do mesmo ponto e volta sozinho. Ninguém precisa pilotar.</p>
<p>A Help Farm compara as fotos e mostra, em tempo real, a área já colhida ou plantada, quanto falta, o ritmo em hectares por hora, o tempo parado e a hora prevista para terminar.</p></div>
<img src='{D}movel-drone.jpg' style='width:100%;height:62mm;object-fit:cover;border-radius:3mm'></div>
<div class='flow'>
<div><b>1</b><h3>Voa</h3><span class='muted'>Decola da unidade móvel a cada 10 minutos.</span></div>
<div><b>2</b><h3>Fotografa</h3><span class='muted'>Sempre do mesmo ponto, para comparar.</span></div>
<div><b>3</b><h3>Mede</h3><span class='muted'>Área feita, ritmo, paradas e término.</span></div>
<div><b>4</b><h3>Avisa</h3><span class='muted'>Painel e alerta para quem decide.</span></div></div>
<img src='{D}painel.jpg' style='width:100%;border-radius:3mm;margin-top:2mm;border:.6pt solid #E2D3BA'>
<p class='cap'>Painel de acompanhamento: área colhida, ritmo, paradas e previsão de término (dados de simulação).</p>
</div>{foot(2, L)}</div>"""
p3 = f"""<div class='pg'><div class='secband'></div><div class='pad'>
<span class='eyebrow'>O que a fazenda ganha</span><h1>A safra acompanhada de 10 em 10 minutos</h1>
<div class='ben'>
<div><b>Logística no ritmo do campo</b>Caminhões e armazém chamados na hora certa, sem fila e sem espera.</div>
<div><b>Paradas vistas na hora</b>Quebra, atolamento ou falta de caminhão aparecem no mesmo voo.</div>
<div><b>Colheita antes da chuva</b>Com o Analisador de Nuvens, o RAPP diz se dá para terminar o talhão antes do temporal.</div>
<div><b>Plantio na janela certa</b>Mostra se o plantio vai caber na janela de umidade do solo.</div>
<div><b>Prestação de serviço medida</b>Área feita por máquina e por equipe, base para pagar terceiros com justiça.</div>
<div><b>Prova para banco e seguro</b>Registro com foto e hora de cada etapa da safra.</div></div>
<h2>Controle na mão, na unidade móvel</h2>
<div class='grid2' style='align-items:center'>
<img src='{A}maleta.jpg' style='width:100%;height:70mm;object-fit:cover;border-radius:3mm'>
<div><p>Na unidade móvel, a <b>Maleta de Controle Help Farm</b> reúne as telas do acompanhamento: o técnico vê o mapa do talhão, o andamento e os alertas sem precisar de um piloto de drone. O operador acompanha sentado; o voo é automático.</p><p class='cap'>Imagens ilustrativas geradas por IA.</p></div></div>
</div>{foot(3, L)}</div>"""
p4 = f"""<div class='pg'><div class='secband'></div><div class='pad'>
<span class='eyebrow'>Integrado ao RAPP</span><h1>Um olhar do alto ligado ao cérebro digital da fazenda</h1>
<img src='{D}movel-fazenda.jpg' style='width:100%;height:92mm;object-fit:cover;border-radius:3.5mm'>
<p class='cap'>Unidade móvel Help Farm. Imagem ilustrativa gerada por IA.</p>
<div class='rapp'><b class='t'>Tudo é controlado pelo RAPP</b>Cada voo vira um evento do <b>RAPP</b>, o motor de inteligência artificial construído desde 2010 e exclusivo da Help Farm no agronegócio. O RAPP cruza o andamento da colheita com o <b>Analisador de Nuvens</b>, a telemetria das máquinas, o solo e a logística, e avisa o que fazer: reforçar a frente, chamar caminhões ou recolher as máquinas antes da chuva.</div>
<h2>Por que só a Help Farm tem</h2>
<div class='grid3'>
<div class='card'><h3>Sem piloto</h3><p class='muted' style='margin:0'>Voo automático a partir da unidade móvel, seis vezes por hora.</p></div>
<div class='card'><h3>Mede, não só filma</h3><p class='muted' style='margin:0'>Transforma as fotos em hectares, ritmo, paradas e hora de término.</p></div>
<div class='card'><h3>Parte de um sistema</h3><p class='muted' style='margin:0'>Sozinho é um drone; ligado ao RAPP, orienta a safra inteira.</p></div></div>
<p style='margin-top:6mm'><b>Help Farm</b> · A sua fazenda avisa antes do problema. · investidores@helpcure.com.py · helpcure.com.py/helpfarm</p>
</div>{foot(4, L)}</div>"""
asyncio.run(render(page(p1 + p2 + p3 + p4), "/home/claude/hfd/HelpFarm_Avaliador_Trabalho_Campo_Apresentacao.pdf"))
