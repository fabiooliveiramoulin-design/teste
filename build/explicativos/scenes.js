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
};
