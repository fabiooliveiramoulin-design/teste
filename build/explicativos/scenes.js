// Cenas de cada vídeo: título manuscrito no topo + itens desenhados em ordem.
// Item = [svg, peso]; texto (class w) é escrito da esquerda para a direita.
const { I, T, K, G, GD, BR, AM, RD } = require("./icons");
const head = (txt, color = K) => [T(800, 115, txt, 74, color), 1.2];
const note = (x, y, txt, size = 40, color = K, a = "middle") => [T(x, y, txt, size, color, a), 0.6];

module.exports = {
  v1: [
    [head("A natureza decide o lucro"), [I.sun(280, 330, 1.3), 1], [I.cloud(560, 320, 1.3, true), 1], [I.bug(820, 340, 1.3), 1], [I.soil(1110, 340, 1.2), 1], [I.field(800, 600, 1.4), 1.4], [I.scale(1320, 560, 1.1), 1], [I.coin(1220, 600, 0.8), 0.5], note(1320, 720, "lucro ou prejuízo?", 44, RD)],
    [head("O problema aparece tarde demais", RD), [I.leaf(330, 470, 1.4), 1], note(330, 690, "folha manchada"), [I.cow(800, 470, 1.4), 1.2], note(800, 690, "animal parado"), [I.tractor(1260, 470, 1.3, true), 1.2], note(1260, 690, "máquina quebrada"), [I.clock(1480, 230, 0.9), 0.6]],
    [head("A Help Farm vai até a fazenda", GD), [I.motorhome(470, 480, 1.25), 1.6], [I.drone(520, 260, 1), 0.7], [I.sensor(1000, 500, 1.1), 0.6], [I.sensor(1130, 470, 1.1), 0.6], [I.sensor(1260, 500, 1.1), 0.6], note(1130, 650, "solo · lavoura · água · rebanho · máquinas", 40), [I.check(1450, 420, 1), 0.4]],
    [head("O RAPP aprende o normal", GD), [I.graph(800, 480, 1.7), 1.8], note(800, 330, "assinatura normal", 48, GD), note(330, 760, "talhão"), note(800, 760, "animal"), note(1270, 760, "máquina")],
    [head("O desvio vira alerta", RD), [I.graph(700, 480, 1.5, "drift"), 1.8], [I.bell(1340, 430, 1.3), 1], note(1340, 600, "dias antes", 56, RD)],
    [head("A pessoa certa age a tempo", GD), [I.monitor(800, 330, 1.1), 1], [I.headset(560, 400, 0.8), 0.5], note(560, 500, "central"), [I.arrow(760, 430, 380, 560), 0.4], [I.arrow(800, 430, 800, 560), 0.3], [I.arrow(840, 430, 1220, 560), 0.4], [I.person(330, 690, 0.9, G), 0.6], note(330, 810, "agrônomo"), [I.person(800, 690, 0.9, "#F2C94C"), 0.6], note(800, 810, "mecânico"), [I.person(1270, 690, 0.9, "#DCEEF7"), 0.6], note(1270, 810, "veterinário")],
    [[T(800, 400, "Help Farm", 140, GD), 1.4], [T(800, 540, "A sua fazenda avisa antes do problema.", 68, K), 1.4], [I.check(800, 680, 1.4), 0.5]],
  ],
  v2: [
    [head("A unidade móvel", GD), [I.motorhome(800, 520, 2), 2.2], note(800, 760, "motorhome 4x4 para estrada de terra", 48)],
    [head("Quem e o que vai a bordo"), [I.person(280, 520, 1.1, G), 0.7], [I.person(420, 520, 1.1, BR), 0.7], note(350, 700, "2 profissionais"), [I.drone(760, 450, 1.3), 0.8], note(760, 600, "drones"), [I.gear(1060, 450, 0.9), 0.6], note(1060, 600, "instrumentos"), [I.moto(1340, 480, 1), 0.8], note(1340, 600, "2 motos trail")],
    [head("Primeiro, os drones"), [I.map(800, 560, 1.7), 1.4], [I.drone(800, 260, 1.2), 0.7], [I.pin(620, 520, 1), 0.3], [I.pin(820, 600, 1), 0.3], [I.pin(960, 500, 1), 0.3], note(800, 800, "onde medir primeiro", 48, RD)],
    [head("Medição ponto a ponto"), [I.moto(330, 520, 1.3), 1], [I.soil(780, 440, 0.9), 0.6], [I.leaf(1000, 440, 0.7), 0.5], [I.cow(1240, 440, 0.8), 0.6], [I.tractor(780, 660, 0.7), 0.6], [I.pin(1060, 660, 1, G), 0.3], note(1240, 680, "GPS de precisão", 44, GD)],
    [head("A assinatura sobe por satélite", GD), [I.sensor(360, 560, 1.4), 0.6], [I.sensor(520, 580, 1.4), 0.6], [I.satellite(800, 260, 1.2), 0.9], [I.arrow(560, 470, 740, 320), 0.4], [I.arrow(880, 320, 1110, 450), 0.4], [I.monitor(1240, 540, 1), 0.8], note(1240, 700, "motor RAPP", 50, GD)],
    [head("Visita ou temporada"), [I.motorhome(470, 460, 1.1), 1.2], [I.arrow(700, 470, 860, 470), 0.3], note(470, 640, "mede e segue viagem"), [I.calendar(1200, 450, 1.3), 1], note(1200, 660, "fica a temporada inteira")],
  ],
  v3: [
    [head("Cada um tem o seu normal"), [I.field(330, 470, 1), 0.9], [I.cow(800, 450, 1.1), 0.9], [I.tractor(1260, 450, 1.1), 0.9], [T(330, 650, "~~~", 60, GD), 0.3], [T(800, 650, "~~~", 60, GD), 0.3], [T(1260, 650, "~~~", 60, GD), 0.3], note(800, 790, "essa é a assinatura", 56, GD)],
    [head("A faixa normal", GD), [I.graph(800, 500, 2), 2.2], note(800, 800, "medições de todos os dias")],
    [head("O desvio que o olho não vê", RD), [I.graph(720, 500, 1.6, "drift"), 1.6], [I.magnifier(1260, 520, 1.6), 0.8]],
    [head("Comparado com ele mesmo"), [I.barn(420, 480, 1.1), 0.8], [I.graph(420, 700, 0.6), 0.6], note(420, 340, "Fazenda A"), [I.barn(1180, 480, 1.1), 0.8], [I.graph(1180, 700, 0.6, "drift"), 0.6], note(1180, 340, "Fazenda B"), note(800, 520, "≠", 120, RD)],
    [head("Alerta antes do sintoma", GD), [I.bell(480, 480, 1.6), 1], [I.doc(1100, 480, 1.4), 1], note(1100, 720, "ação sugerida", 50, GD)],
    [head("Da indústria para o campo"), [I.gear(400, 460, 1.4), 1], note(400, 650, "turbinas e bombas"), [I.arrow(620, 460, 960, 460), 0.4], [I.barn(1200, 460, 1.2), 1], note(1200, 650, "a sua fazenda", 50, GD)],
  ],
  v4: [
    [head("De onde vem o que eu compro?"), [I.person(450, 520, 1.3), 0.8], [T(560, 380, "?", 120, RD), 0.3], [I.globe(1150, 480, 1.6), 1], note(1150, 680, "a Europa exige a prova", 46, RD)],
    [head("Sem desmatamento desde 2020", GD), [I.map(700, 520, 1.6), 1.4], [I.satellite(1300, 300, 1), 0.8], [I.check(1300, 560, 1.4), 0.5], note(1300, 680, "satélite desde 2020")],
    [head("Nota por critério"), [I.bars(500, 520, 1.4), 1.3], [I.medal(1000, 450, 1, AM, "ouro"), 0.8], [I.medal(1200, 450, 1, "#D3DAE0", "prata"), 0.8], [I.medal(1400, 450, 1, "#CD7F32", "bronze"), 0.8]],
    [head("Certificado gravado na blockchain"), [I.doc(330, 500, 1.3), 1], [I.chain(900, 500, 1.1), 1.4], [I.lock(1420, 500, 1.4), 0.6], note(900, 700, "ninguém consegue alterar", 48, RD)],
    [head("O comprador confere na hora", GD), [I.phone(600, 500, 1.6), 1.2], [I.check(1000, 420, 1.2), 0.4], note(1060, 520, "origem", 50, K, "start"), note(1060, 600, "práticas", 50, K, "start"), note(1060, 680, "nível", 50, K, "start")],
    [[T(800, 380, "Help Farm", 140, GD), 1.3], [I.medal(800, 560, 1, AM), 0.7], [T(800, 780, "Cada lote com certidão de nascimento.", 64), 1.3]],
  ],
  v6: [
    [head("A conta de luz das bombas", RD), [I.pump(420, 470, 1.6), 1], [I.bolt(700, 450, 1.3), 0.5], [I.coin(930, 430, 1.1), 0.4], [I.coin(1020, 500, 1.1), 0.4], [I.coin(1110, 430, 1.1), 0.4], note(800, 720, "pode passar de 1/3 do custo de produzir", 50, RD)],
    [head("Primeiro, medir", GD), [I.pump(350, 480, 1.2), 0.8], [I.sensor(470, 430, 0.9), 0.5], note(380, 660, "kWh de cada bomba"), [I.field(1150, 470, 1.1), 0.9], [I.drop(1150, 330, 1), 0.4], note(1150, 660, "água que a lavoura pede"), [I.graph(760, 470, 0.7), 0.8]],
    [head("De dia: sol direto na bomba", GD), [I.sun(300, 260, 1.2), 0.7], [I.panel(620, 470, 1.4), 1.2], [I.arrow(800, 480, 1000, 520), 0.3], [I.pump(1150, 520, 1.2), 0.7], [I.nobat(1300, 280, 1.2), 0.6], note(1300, 400, "sem bateria", 50, RD)],
    [head("O recalque: do rio para o alto"), [I.hill(900, 560, 2), 0.8], [I.river(340, 690, 1.3), 0.7], [I.pump(470, 610, 0.9), 0.5], [`<path class="s" style="stroke:#7FB4C9" d="M520 600 C700 580 820 340 1130 330"/>`, 0.6], [I.tank(1200, 330, 1.2), 0.8], [I.sun(260, 260, 0.9), 0.4], note(820, 820, "a bomba trabalha enquanto há sol", 46, GD)],
    [head("A água no alto é a bateria", GD), [I.tank(380, 400, 1.3), 0.8], [I.moon(300, 210, 1.3), 0.4], [I.cloud(520, 210, 1), 0.5], [I.arrow(520, 460, 900, 620), 0.4], note(700, 470, "gravidade", 44, GD), [I.pivot(1180, 660, 1.2), 1], note(1180, 800, "pivô irrigando à noite")],
    [head("Pago pela economia", GD), [I.nobat(330, 420, 1.1), 0.5], note(330, 540, "sem bateria"), [I.tractor(620, 440, 0.7, true), 0.5], note(620, 560, "sem diesel"), [I.monitor(1060, 430, 1.2), 0.9], note(1060, 610, "RAPP confere todo mês:", 44, GD), note(1060, 670, "kWh gerado · m³ bombeado", 44)],
    [[T(800, 380, "Help Farm", 140, GD), 1.3], [I.sun(560, 560, 0.8), 0.4], [I.tank(800, 560, 0.8), 0.4], [I.pivot(1060, 580, 0.6), 0.5], [T(800, 790, "O sol bombeia, a água espera, a conta cai.", 64), 1.4]],
  ],
  v5: [
    [head("Receita dos dois lados"), [I.scale(800, 520, 1.8), 1.4], [I.person(560, 470, 0.8, G), 0.5], [I.bank(1040, 470, 0.7), 0.5]],
    [head("Do produtor", GD), [I.person(350, 520, 1.3, G), 0.8], [I.coin(620, 440, 1), 0.4], [I.coin(700, 520, 1), 0.4], note(1100, 400, "taxa de implantação", 50), note(1100, 500, "assinatura por hectare,", 50), note(1100, 580, "por cabeça ou por máquina", 50)],
    [head("12 entidades ao redor da fazenda"), [I.barn(800, 500, 0.9), 0.8], ...[["vet", 0], ["mecânico", 30], ["sementes", 60], ["adubo", 90], ["defensivos", 120], ["agrônomo", 150], ["transporte", 180], ["seguradora", 210], ["governo", 240], ["banco", 270], ["comprador", 300], ["certificadora", 330]].map(([lab, a]) => { const r = (a - 90) * Math.PI / 180; return [I.node(800 + Math.cos(r) * 420, 500 + Math.sin(r) * 280, lab), 0.25]; })],
    [head("Bancos e seguradoras pagam por dado"), [I.barn(330, 520, 0.9), 0.7], [I.arrow(500, 500, 700, 500), 0.3], [I.monitor(850, 500, 0.8), 0.6], [I.bank(1220, 380, 0.8), 0.7], [I.shield(1220, 640, 0.9), 0.7], note(850, 680, "dado confiável", 46, GD)],
    [head("Cooperativas e tradings"), [I.barn(450, 500, 1.2), 0.9], note(450, 700, "licença anual"), [I.arrow(650, 500, 820, 500), 0.3], [I.person(960, 520, 0.7, G), 0.3], [I.person(1080, 520, 0.7, BR), 0.3], [I.person(1200, 520, 0.7, G), 0.3], [I.person(1320, 520, 0.7, BR), 0.3], note(1140, 700, "associados")],
    [head("Certificação de origem"), [I.medal(450, 480, 1.4, AM), 0.9], [I.doc(800, 480, 1), 0.7], [I.ton(1170, 500, 1.4), 0.8], note(800, 720, "receita por lote e por tonelada", 50, GD)],
    [head("Mais fontes, menos risco", GD), [I.grow(800, 520, 1.8), 1.8], note(800, 790, "quem investe participa desse crescimento", 50, GD)],
  ],
  v7: [
    [head("A fazenda negocia com a natureza"), [I.sun(260, 320, 1.1), 0.7], [I.cloud(520, 310, 1.2, true), 0.8], [I.bug(780, 330, 1.1), 0.7], [I.soil(1060, 340, 1), 0.7], [I.tractor(1340, 330, 0.9), 0.8], [I.field(800, 620, 1.5), 1.2], note(800, 800, "todos os dias, até o alimento chegar à mesa", 46)],
    [head("A perda aparece tarde demais", RD), [I.leaf(300, 460, 1.2), 0.8], [I.cow(620, 460, 1.1), 0.9], [I.tractor(950, 460, 1, true), 0.9], [I.arrow(1110, 460, 1240, 460), 0.3], [I.coin(1370, 440, 1.3), 0.5], note(1370, 560, "alimento", 44, RD), note(1370, 610, "mais caro", 44, RD), note(800, 760, "safra perdida encarece a mesa de todos", 50, RD)],
    [head("A Help Farm mede a fazenda inteira", GD), [I.satellite(260, 270, 0.9), 0.6], [I.sensor(250, 560, 1.1), 0.4], [I.sensor(360, 580, 1.1), 0.4], note(300, 720, "sensores e satélite"), [I.cloud(800, 300, 1.2), 0.7], [I.clock(800, 520, 0.8), 0.5], note(800, 660, "Analisador de Nuvens", 44, GD), note(800, 720, "em tempo real", 44, RD), [I.drone(1300, 270, 1), 0.6], [I.field(1300, 520, 0.9), 0.7], note(1300, 660, "Colheita e plantio", 44, GD), note(1300, 720, "6 vezes por hora", 44, RD)],
    [head("O motor: RAPP, desde 2010", GD), [I.gear(360, 470, 1.4), 1], note(360, 650, "2010 · turbinas e bombas"), note(360, 700, "do petróleo"), [I.arrow(620, 470, 960, 470), 0.4], [I.barn(1220, 460, 1.2), 1], note(1220, 650, "2026 · a fazenda", 46, GD)],
    [head("Cruza tudo e avisa antes", GD), [I.graph(680, 500, 1.5, "drift"), 1.6], [I.bell(1320, 450, 1.3), 0.8], note(1320, 620, "dias antes", 56, RD), note(680, 790, "talhão · animal · máquina", 46)],
    [head("Exclusivo no agronegócio", GD), [I.lock(400, 470, 1.4), 0.9], note(400, 650, "licença só da Help Farm"), [I.grow(1100, 500, 1.3), 1.2], note(1100, 700, "aprende a cada safra", 48, GD)],
    [head("Receita: o produtor paga", GD), [I.person(330, 520, 1.3, G), 0.8], [I.coin(600, 440, 1), 0.4], [I.coin(690, 520, 1), 0.4], note(1100, 400, "implantação", 54), note(1100, 500, "+ assinatura por hectare,", 50), note(1100, 580, "por cabeça ou por máquina", 50)],
    [head("Um alerta paga o ano"), [I.field(380, 500, 1.2), 1], note(380, 690, "fazenda de grãos · Brasil"), [I.bell(820, 470, 1.3), 0.7], note(820, 640, "1 alerta", 56, RD), [T(950, 480, "=", 90, K), 0.3], [I.calendar(1230, 470, 1.2), 0.8], note(1230, 640, "12 meses de Help Farm", 50, GD)],
    [head("Camada de energia do RAPP", GD), [I.sun(280, 280, 1), 0.5], [I.panel(470, 470, 1.1), 0.9], [I.pump(800, 480, 1.1), 0.8], [I.pivot(1150, 500, 0.9), 0.9], note(800, 760, "30% da economia verificada na conta", 52, GD)],
    [head("Vários pagadores, o mesmo dado"), [I.barn(800, 500, 0.9), 0.8], ...[["cooperativa", 0], ["banco", 72], ["seguradora", 144], ["comprador", 216], ["certificação", 288]].map(([lab, a]) => { const r = (a - 90) * Math.PI / 180; return [I.node(800 + Math.cos(r) * 400, 510 + Math.sin(r) * 270, lab), 0.35]; })],
    [head("Paraguai + Brasil"), [I.grow(520, 520, 1.6), 1.6], [T(1100, 450, "receita e resultado", 62, GD), 0.9], [T(1100, 540, "crescendo ano a ano", 62, GD), 0.9], note(1100, 640, "já descontado o royalty do RAPP", 42)],
    [head("Quanto vale no quinto ano"), [I.barn(400, 560, 0.9), 0.7], note(400, 720, "logo após a rodada"), [I.arrow(600, 520, 880, 520), 0.4], [I.barn(1150, 520, 1.6), 1], note(1150, 760, "≈ 5× o valor de hoje", 64, GD)],
    [head("A performance esperada", GD), [I.grow(420, 520, 1.4), 1.2], [T(1080, 440, "TIR esperada ≈ 27% ao ano", 62, GD), 1], [I.coin(940, 590, 0.8), 0.3], [T(1130, 610, "4,5× o capital", 66, K), 0.9]],
    [head("Paraguai prova, Brasil escala"), [I.map(560, 520, 1.4), 1.2], [I.pin(480, 520, 1), 0.3], [I.pin(600, 460, 1, G), 0.3], [I.motorhome(1180, 470, 0.9), 1], note(1180, 650, "5 fazendas-piloto"), note(1180, 700, "+ 1 cooperativa parceira")],
    [head("Um convite", GD), [I.person(380, 520, 1.3, BR), 0.8], note(380, 700, "você"), [I.arrow(560, 500, 760, 500), 0.4], [I.leaf(920, 480, 0.9), 0.5], [I.ton(1140, 500, 1), 0.6], [I.grow(1350, 480, 0.8), 0.6], note(1100, 720, "inovação na performance", 50, GD), note(1100, 780, "da produção de alimentos", 50, GD)],
    [[T(800, 360, "Help Farm", 140, GD), 1.3], [T(800, 500, "A sua fazenda avisa antes do problema.", 64), 1.3], [T(800, 640, "Área do investidor · fale com a gente", 50, BR), 1], [I.check(800, 760, 1.1), 0.4]],
  ],
};
