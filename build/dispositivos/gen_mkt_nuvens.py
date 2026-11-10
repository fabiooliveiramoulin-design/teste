import asyncio
from common import *
src = open("/home/claude/hfm/gen_manual.py").read()
hist = src[src.find("# ---------------- histórico"):src.find("# ---------------- visão geral")]
pages = []; B = "file:///home/claude/hfm/"; L = "Analisador de Nuvens · apresentação"
exec(hist, {"pages": pages, "B": B, "foot": lambda n: foot(n, L)})
H = "file:///home/claude/hfm/img/"
p1 = cover(H + "hero.jpg", "Dispositivo exclusivo Help Farm", "Analisador<br>de <span style='color:#8FCB5A'>Nuvens</span>",
  "A estação que olha o céu da própria fazenda, compara com o satélite e confirma o alerta no celular do produtor em até 10 minutos.",
  [("≤ 10 min", "da nuvem vista ao alerta no celular"), ("180°", "o céu inteiro em cada foto"), ("3 fontes", "câmera, satélite e previsão concordando"), ("24 h", "funciona com energia solar própria")])
p3 = f"""<div class='pg'><div class='secband'></div><div class='pad'>
<span class='eyebrow'>Como funciona</span><h1>Do céu ao celular, sem alarme falso</h1>
<div class='grid2' style='grid-template-columns:1fr .9fr;align-items:center'>
<div><p>O Analisador de Nuvens fica num mastro na borda do talhão. A cada poucos minutos, fotografa o céu inteiro e mede a cobertura de nuvens, a direção e a velocidade com que elas andam.</p>
<p>A Help Farm <b>compara essa foto com a imagem de satélite e com a previsão do tempo</b>. Quando as três fontes concordam, o alerta é <b>confirmado visualmente</b> e chega ao produtor com a foto do céu. Ele não perde tempo com aviso que não se confirma.</p></div>
<img src='{B}r/montada.png' style='width:100%;max-height:105mm;object-fit:contain'></div>
<div class='flow'>
<div><b>1</b><h3>Vê</h3><span class='muted'>A câmera fotografa o céu inteiro, dia e noite.</span></div>
<div><b>2</b><h3>Compara</h3><span class='muted'>Cruza a foto com o satélite e a previsão.</span></div>
<div><b>3</b><h3>Confirma</h3><span class='muted'>O RAPP confirma quando as três fontes concordam.</span></div>
<div><b>4</b><h3>Avisa</h3><span class='muted'>Alerta com a foto no celular em até 10 minutos.</span></div></div>
<h2>O que o produtor ganha</h2>
<div class='ben'>
<div><b>Pulverização sem desperdício</b>Para a aplicação antes da chuva lavar o produto da folha.</div>
<div><b>Máquinas protegidas</b>Recolhe colhedoras, tratores e caminhões antes do temporal.</div>
<div><b>Colheita adiantada</b>Reforça a frente de colheita quando a chuva ainda está longe.</div>
<div><b>Irrigação inteligente</b>Desliga o pivô quando a chuva está chegando e economiza água e energia.</div>
<div><b>Granizo e vento forte</b>Aviso para proteger estufas, pomares e animais.</div>
<div><b>Histórico para o seguro</b>Foto e hora de cada evento guardadas, prova para seguradora e banco.</div></div>
</div>{foot(3, L)}</div>"""
p4 = f"""<div class='pg'><div class='secband'></div><div class='pad'>
<span class='eyebrow'>Integrado ao RAPP</span><h1>Um olho no céu ligado ao cérebro digital da fazenda</h1>
<img src='{H}hero.jpg' style='width:100%;height:92mm;object-fit:cover;border-radius:3.5mm'>
<p class='cap'>Imagem ilustrativa gerada por IA.</p>
<div class='rapp'><b class='t'>Tudo é controlado pelo RAPP</b>O Analisador não decide sozinho. Cada foto do céu vira um evento do <b>RAPP</b>, o motor de inteligência artificial construído desde 2010 e exclusivo da Help Farm no agronegócio. O RAPP cruza o céu com o satélite, a previsão, o <b>Avaliador de Trabalho em Campo</b> (dá para terminar o talhão antes da chuva?), as máquinas, a irrigação e o solo, decide quem avisar e guarda o histórico que deixa a previsão de cada fazenda mais precisa.</div>
<h2>Por que só a Help Farm tem</h2>
<div class='grid3'>
<div class='card'><h3>Nasceu na energia</h3><p class='muted' style='margin:0'>Desenvolvido primeiro para usinas solares que não podiam perder geração: precisão de minutos.</p></div>
<div class='card'><h3>Confirmação visual</h3><p class='muted' style='margin:0'>Não depende só da previsão: vê o céu da própria fazenda.</p></div>
<div class='card'><h3>Parte de um sistema</h3><p class='muted' style='margin:0'>Sozinho é uma câmera; ligado ao RAPP, decide o que fazer na fazenda.</p></div></div>
<p style='margin-top:6mm'><b>Help Farm</b> · A sua fazenda avisa antes do problema. · investidores@helpcure.com.py · helpcure.com.py/helpfarm</p>
</div>{foot(4, L)}</div>"""
asyncio.run(render(page(p1 + pages[0] + p3 + p4), "/home/claude/hfd/HelpFarm_Analisador_de_Nuvens_Apresentacao.pdf"))
