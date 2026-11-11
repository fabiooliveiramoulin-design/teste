import asyncio
from common import *
L = "Avaliador de Trabalho em Campo · apresentação"; A = "file:///home/claude/hfa/"; S = "file:///home/claude/teste/helpfarm/img/"
from PIL import Image
for n in ("movel-drone", "movel-fazenda"):
    Image.open(f"/home/claude/teste/helpfarm/img/{'f/' if n=='movel-drone' else ''}{n}.webp").convert("RGB").save(f"/home/claude/hfd/{n}.jpg", quality=88)
D = "file:///home/claude/hfd/"
p1 = cover(A + "drone.jpg", "Dispositivo exclusivo Help Farm", "Avaliador de<br>Trabalho <span style='color:#8FCB5A'>em Campo</span>",
  "O drone automático de dois turnos: de dia acompanha a colheita e o plantio seis vezes por hora; à noite faz a ronda de segurança da fazenda com câmera térmica.",
  [("6× por hora", "um voo a cada 10 minutos na safra"), ("Automático", "decola e pousa sozinho, sem piloto"), ("24 horas", "de dia produção, à noite vigilância"), ("Tempo real", "andamento, paradas e alertas")])
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
SVG = """<svg viewBox='0 0 180 74' style='width:100%;height:auto;display:block;border-radius:3mm;margin-top:2mm'>
<defs><linearGradient id='dsk' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#BFE3F5'/><stop offset='1' stop-color='#EAF6FB'/></linearGradient>
<linearGradient id='nsk' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#0F1A33'/><stop offset='1' stop-color='#22345C'/></linearGradient>
<radialGradient id='heat'><stop offset='0' stop-color='#FFF4B0'/><stop offset='.45' stop-color='#FF9A1F'/><stop offset='1' stop-color='#C2261B' stop-opacity='0'/></radialGradient></defs>
<rect x='0' y='0' width='90' height='74' fill='url(#dsk)'/><circle cx='14' cy='12' r='6' fill='#FFC62E'/>
<g stroke='#FFC62E' stroke-width='.8'><line x1='14' y1='2' x2='14' y2='4'/><line x1='4' y1='12' x2='6' y2='12'/><line x1='22' y1='12' x2='24' y2='12'/><line x1='7' y1='5' x2='8.4' y2='6.4'/><line x1='21' y1='5' x2='19.6' y2='6.4'/></g>
<polygon points='0,44 90,38 90,74 0,74' fill='#D9B867'/>
<polygon points='0,52 90,45 90,74 0,74' fill='#7FB34A'/>
<g stroke='#6A9A3B' stroke-width='.5'><line x1='0' y1='58' x2='90' y2='51'/><line x1='0' y1='64' x2='90' y2='57'/><line x1='0' y1='70' x2='90' y2='63'/></g>
<g stroke='#C9A54E' stroke-width='.5'><line x1='0' y1='47' x2='90' y2='41'/></g>
<rect x='52' y='43' width='12' height='5' rx='1' fill='#3F7A22'/><rect x='60' y='40' width='5' height='4' fill='#2E5A18'/><circle cx='55' cy='49' r='1.6' fill='#2E1D10'/><circle cx='62' cy='49' r='1.6' fill='#2E1D10'/>
<rect x='8' y='54' width='20' height='8' rx='1.2' fill='#F4EBDD' stroke='#8B6A43' stroke-width='.4'/><rect x='14' y='51.6' width='8' height='2.4' fill='#8B6A43'/>
<path d='M18 51 C 30 20, 60 18, 72 30 S 60 46, 40 40' fill='none' stroke='#2E1D10' stroke-width='.5' stroke-dasharray='1.4 1'/>
<g transform='translate(66,22)'><rect x='-3' y='-.8' width='6' height='1.6' rx='.6' fill='#2E1D10'/><line x1='-5' y1='-1.6' x2='5' y2='-1.6' stroke='#2E1D10' stroke-width='.5'/><polygon points='-1,1 1,1 6,18 -6,18' fill='#FFB500' opacity='.25'/></g>
<rect x='3' y='3' rx='1.5' width='34' height='6.5' fill='#fff' opacity='.9' transform='translate(28,0)'/><text x='45' y='7.6' text-anchor='middle' font-size='3.6' font-weight='700' fill='#2E1D10'>DIA · PRODUÇÃO</text>
<text x='18' y='66.5' text-anchor='middle' font-size='2.4' fill='#2E1D10'>unidade móvel</text>
<rect x='90' y='0' width='90' height='74' fill='url(#nsk)'/><circle cx='166' cy='11' r='5' fill='#F1EEDC'/><circle cx='168.5' cy='9.6' r='4.4' fill='#14213F'/>
<g fill='#fff' opacity='.8'><circle cx='100' cy='8' r='.4'/><circle cx='112' cy='14' r='.35'/><circle cx='128' cy='6' r='.4'/><circle cx='146' cy='17' r='.35'/><circle cx='156' cy='5' r='.3'/><circle cx='176' cy='22' r='.35'/></g>
<polygon points='90,48 180,44 180,74 90,74' fill='#1B2A1E'/>
<polygon points='98,46 112,40 126,46' fill='#3A3328'/><rect x='100' y='46' width='24' height='10' fill='#4A4033'/><rect x='109' y='50' width='5' height='6' fill='#F2C14E' opacity='.8'/>
<rect x='132' y='42' width='18' height='12' fill='#3C4A57'/><polygon points='131,42 141,37 151,42' fill='#2E3A45'/>
<rect x='155' y='45' width='8' height='9' rx='3' fill='#56626E'/>
<g stroke='#7A6A4F' stroke-width='.5'><line x1='92' y1='62' x2='178' y2='58'/><line x1='92' y1='65' x2='178' y2='61'/></g><g fill='#7A6A4F'><rect x='96' y='59.5' width='.8' height='6'/><rect x='116' y='58.6' width='.8' height='6'/><rect x='136' y='57.7' width='.8' height='6'/><rect x='156' y='56.8' width='.8' height='6'/><rect x='176' y='55.9' width='.8' height='6'/></g>
<g fill='#8C7A5E' opacity='.8'><ellipse cx='104' cy='69' rx='2.4' ry='1.2'/><ellipse cx='110' cy='70' rx='2.4' ry='1.2'/><ellipse cx='117' cy='68.8' rx='2.4' ry='1.2'/></g>
<g transform='translate(150,24)'><rect x='-3' y='-.8' width='6' height='1.6' rx='.6' fill='#E9EEF6'/><line x1='-5' y1='-1.6' x2='5' y2='-1.6' stroke='#E9EEF6' stroke-width='.5'/><circle cx='0' cy='1.3' r='.7' fill='#FF5A3C'/><polygon points='-1,1.6 1,1.6 14,30 -6,30' fill='#FF8A3C' opacity='.18'/></g>
<circle cx='158' cy='52' r='5' fill='url(#heat)'/><rect x='157.2' y='48.6' width='1.6' height='4.6' rx='.8' fill='#FFE38A'/><circle cx='158' cy='47.6' r='1' fill='#FFE38A'/>
<rect x='155' y='36' width='23' height='5' rx='1' fill='#C2261B'/><text x='166.5' y='39.4' text-anchor='middle' font-size='2.3' font-weight='700' fill='#fff'>pessoa detectada</text>
<path d='M120 54 C 125 30, 140 22, 150 24' fill='none' stroke='#E9EEF6' stroke-width='.45' stroke-dasharray='1.4 1' opacity='.8'/>
<rect x='118' y='3' rx='1.5' width='34' height='6.5' fill='#14213F' stroke='#8FA9D6' stroke-width='.3'/><text x='135' y='7.6' text-anchor='middle' font-size='3.6' font-weight='700' fill='#E9EEF6'>NOITE · VIGILÂNCIA</text>
<text x='112' y='60' text-anchor='middle' font-size='2.3' fill='#C9D3E6'>sede</text><text x='141' y='57' text-anchor='middle' font-size='2.3' fill='#C9D3E6'>galpão</text><text x='159' y='57.6' text-anchor='middle' font-size='2.3' fill='#C9D3E6'>diesel</text><text x='110.5' y='73' text-anchor='middle' font-size='2.3' fill='#C9D3E6'>curral</text>
<line x1='90' y1='0' x2='90' y2='74' stroke='#fff' stroke-width='.6'/></svg>
<p class='cap'>Ilustração esquemática do drone de dois turnos.</p>"""
p4n = f"""<div class='pg'><div class='secband'></div><div class='pad'>
<span class='eyebrow'>Drone de dois turnos</span><h1>De dia mede a produção. À noite vigia a fazenda.</h1>
<p>O mesmo drone trabalha 24 horas. Quando a colheita ou o plantio param no fim do dia, ele troca de função: passa a fazer rondas de segurança com <b>câmera térmica</b>, que enxerga pessoas, veículos, animais e fogo no escuro total. Um único equipamento, duas funções e o custo dividido entre produção e segurança.</p>
{SVG}
<div class='grid2' style='gap:4mm;margin-top:3mm'>
<div class='card' style='border-top:1.2mm solid #FFB500'><h3>☀ Turno do dia · produção</h3><p class='muted' style='margin:0'>Voo a cada 10 minutos sobre o talhão em operação: área colhida ou plantada, ritmo, paradas e hora prevista de término.</p></div>
<div class='card' style='border-top:1.2mm solid #2F4A7A'><h3>☾ Turno da noite · vigilância</h3><p class='muted' style='margin:0'>Rondas programadas pela sede, galpão de insumos, tanque de combustível, maquinário, cercas e currais.</p></div></div>
<h2>Quando algo acontece de madrugada</h2>
<div class='flow'>
<div><b>1</b><h3>Dispara</h3><span class='muted'>Porteira aberta, cerca elétrica ou sensor de movimento.</span></div>
<div><b>2</b><h3>Decola</h3><span class='muted'>O drone sai sozinho da base e vai direto ao ponto.</span></div>
<div><b>3</b><h3>Confirma</h3><span class='muted'>A câmera térmica mostra se é pessoa, veículo, gado solto ou fogo.</span></div>
<div><b>4</b><h3>Avisa</h3><span class='muted'>Foto e localização no celular do produtor e do vigia.</span></div></div>
<div class='ben' style='margin-top:3mm'>
<div><b>Menos furto de gado e de insumos</b>Movimento estranho em curral, galpão ou tanque é visto na hora, não na manhã seguinte.</div>
<div><b>Fogo visto cedo</b>Foco de calor em pastagem ou palhada aparece no primeiro voo.</div>
<div><b>Gado no lugar</b>Animais fora do pasto ou cerca rompida aparecem na ronda.</div>
<div><b>Ronda sem expor pessoas</b>O vigia confere pelo celular antes de sair no escuro.</div></div>
<p class='note' style='margin-top:3mm'>Voos noturnos e automáticos seguem as autorizações das autoridades de aviação civil de cada país (DINAC no Paraguai; ANAC e DECEA no Brasil). No piloto, a operação começa em área delimitada da fazenda com responsável acompanhando à distância.</p>
</div>{foot(4, L)}</div>"""
p4 = f"""<div class='pg'><div class='secband'></div><div class='pad'>
<span class='eyebrow'>Integrado ao RAPP</span><h1>Um olhar do alto ligado ao cérebro digital da fazenda</h1>
<img src='{D}movel-fazenda.jpg' style='width:100%;height:92mm;object-fit:cover;border-radius:3.5mm'>
<p class='cap'>Unidade móvel Help Farm. Imagem ilustrativa gerada por IA.</p>
<div class='rapp'><b class='t'>Tudo é controlado pelo RAPP</b>Cada voo vira um evento do <b>RAPP</b>, o motor de inteligência artificial construído desde 2010 e exclusivo da Help Farm no agronegócio. O RAPP cruza o andamento da colheita com o <b>Analisador de Nuvens</b>, a telemetria das máquinas, o solo e a logística, e avisa o que fazer: reforçar a frente, chamar caminhões ou recolher as máquinas antes da chuva. À noite, é o RAPP que programa as rondas, decide quando o drone decola após um alarme, confere se o vento e a chuva permitem o voo e aprende o que é normal em cada canto da fazenda.</div>
<h2>Por que só a Help Farm tem</h2>
<div class='grid3'>
<div class='card'><h3>Sem piloto, 24 horas</h3><p class='muted' style='margin:0'>Voo automático: produção de dia, vigilância à noite. Funciona com drones de marcas diferentes.</p></div>
<div class='card'><h3>Mede, não só filma</h3><p class='muted' style='margin:0'>Transforma as fotos em hectares, ritmo, paradas e hora de término.</p></div>
<div class='card'><h3>Parte de um sistema</h3><p class='muted' style='margin:0'>Sozinho é um drone; ligado ao RAPP, orienta a safra inteira.</p></div></div>
<p style='margin-top:6mm'><b>Help Farm</b> · A sua fazenda avisa antes do problema. · investidores@helpcure.com.py · helpcure.com.py/helpfarm</p>
</div>{foot(5, L)}</div>"""
asyncio.run(render(page(p1 + p2 + p3 + p4n + p4), "/home/claude/hfd/HelpFarm_Avaliador_Trabalho_Campo_Apresentacao.pdf"))
