# Gera o site Help Farm em /helpfarm (PT no HTML + ES/EN embutidos para a troca de idioma).
# Uso: python3 build/build_helpfarm.py   (a partir da raiz do repositório)
# Reaproveita assets/site.css e assets/site.js do repositório; ajustes próprios em helpfarm/assets/hf.css.
import json, html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "helpfarm")


class Page:
    def __init__(self):
        self.es, self.en, self.n = {}, {}, 0

    def t(self, pt, es, en, tag="span", cls="", raw=False, attrs=""):
        self.n += 1
        k = "f%d" % self.n
        self.es[k], self.en[k] = es, en
        h = ' data-html' if raw else ''
        c = ' class="%s"' % cls if cls else ''
        body = pt if raw else html.escape(pt)
        return '<%s data-i="%s"%s%s%s>%s</%s>' % (tag, k, h, c, attrs, body, tag)

    def title(self, pt, es, en):
        self.es["_title"], self.en["_title"] = es, en
        return pt


NAV = [("index.html", "Início", "Inicio", "Home"),
       ("unidade-movel.html", "Unidade móvel", "Unidad móvil", "Mobile unit"),
       ("tecnologia.html", "Tecnologia", "Tecnología", "Technology"),
       ("certificacao.html", "Certificação", "Certificación", "Certification"),
       ("investidores.html", "Investidores", "Inversionistas", "Investors")]

LOGO = '''<svg class="hf-mark" viewBox="0 0 40 40" aria-hidden="true"><rect x="1" y="1" width="38" height="38" rx="10" fill="#4A2F1B" stroke="#5E9F3A" stroke-opacity=".35"/>
<path d="M7 29c6-3 20-3 26 0M7 24c6-3 20-3 26 0" fill="none" stroke="#C9A36B" stroke-width="2" stroke-linecap="round" opacity=".7"/>
<path d="M8 19l6-1 4-6 4 9 4-4 6 0" fill="none" stroke="#8FCB5A" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="32" cy="17" r="2.6" fill="#FFB500"/></svg>'''


def shell(pg, path, title, body, desc, extra=""):
    links = []
    for href, pt, es, en in NAV:
        cur = ' aria-current="page"' if path == href else ''
        links.append('<a href="%s"%s>%s</a>' % ("./" if href == "index.html" else href, cur, pg.t(pt, es, en)))
    head = f'''<!doctype html>
<html lang="pt-BR" translate="no" class="notranslate">
<head>
<meta charset="utf-8">
<meta name="google" content="notranslate">
<meta name="robots" content="noindex">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<link rel="icon" href="assets/hf-icone.svg" type="image/svg+xml">
<meta property="og:image" content="https://helpcure.com.py/helpfarm/img/movel-fazenda.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Lexend:wght@300;400;500;600&display=swap">
<link rel="stylesheet" href="../assets/site.css?v=8">
<link rel="stylesheet" href="assets/hf.css?v=5">
</head>
<body class="hf">
<header class="top">
  <div class="wrap nav">
    <a class="logo" href="./" aria-label="Help Farm">{LOGO}<span style="letter-spacing:-.02em">Help<b>Farm</b></span></a>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    <nav class="menu" aria-label="Menu">{"".join(links)}</nav>
    <div class="lang" role="group" aria-label="Idioma / Language">
      <button type="button" data-l="pt" aria-pressed="true">PT</button><button type="button" data-l="es" aria-pressed="false">ES</button><button type="button" data-l="en" aria-pressed="false">EN</button>
    </div>
  </div>
</header>
<main>
'''
    foot = f'''</main>
<footer>
  <div class="wrap">
    <div><a class="logo" href="./" style="color:#E9F3F0;display:flex">{LOGO}<span style="letter-spacing:-.02em">Help<b>Farm</b></span></a>
      {pg.t("Monitoramento preditivo de fazendas: cada talhão, animal e máquina comparado com ele mesmo.", "Monitoreo predictivo de establecimientos: cada lote, animal y máquina comparado consigo mismo.", "Predictive farm monitoring: every field, animal and machine compared with itself.", "p", attrs=' style="margin-top:10px;max-width:40ch"')}
      <p style="margin-top:12px">{pg.t("Contato", "Contacto", "Contact")}: <a href="mailto:investidores@helpcure.com.py?subject=Help%20Farm" style="display:inline">investidores@helpcure.com.py</a></p></div>
    <div><h4>Help Farm</h4>
      <a href="unidade-movel.html">{pg.t("Unidade móvel de medição", "Unidad móvil de medición", "Mobile measuring unit")}</a>
      <a href="tecnologia.html">{pg.t("Motor RAPP e o que medimos", "Motor RAPP y qué medimos", "RAPP engine and what we measure")}</a>
      <a href="certificacao.html">{pg.t("Certificação de origem", "Certificación de origen", "Origin certification")}</a>
      <a href="investidores.html">{pg.t("Investidores", "Inversionistas", "Investors")}</a></div>
    <div><h4>{pg.t("Tecnologia", "Tecnología", "Technology")}</h4>
      {pg.t("Motor RAPP, desenvolvido pela Moulin", "Motor RAPP, desarrollado por Moulin", "RAPP engine, developed by Moulin", "p")}</div>
    <div class="legal">© 2026 Help Farm · {pg.t("Projeto em fase de desenvolvimento. Ilustrações esquemáticas; configuração final da unidade móvel e dos instrumentos a definir.", "Proyecto en fase de desarrollo. Ilustraciones esquemáticas; configuración final de la unidad móvil y de los instrumentos a definir.", "Project in development. Schematic illustrations; final configuration of the mobile unit and the instruments to be defined.")}</div>
  </div>
</footer>
<script>window.HC_T={json.dumps({"es": pg.es, "en": pg.en}, ensure_ascii=False)};</script>
<script src="../assets/site.js?v=4"></script>
{extra}
</body>
</html>
'''
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, path), "w", encoding="utf-8").write(head + body + foot)


def feats(pg, items):
    return '<ul class="feat">' + "".join('<li>%s</li>' % pg.t("<b>%s</b> — %s" % (a[0], a[1]), "<b>%s</b> — %s" % (b[0], b[1]), "<b>%s</b> — %s" % (c[0], c[1]), "span", raw=True) for a, b, c in items) + '</ul>'


def card(pg, a, b, c, href=None, more=None, img=None):
    pic = '<div class="pic"><img src="img/f/%s.webp" alt="" loading="lazy"></div>' % img if img else ""
    inner = pic + '<div class="in">%s%s%s</div>' % (pg.t(a[0], b[0], c[0], "h3"), pg.t(a[1], b[1], c[1], "p"),
                                              ('<span class="more">%s →</span>' % pg.t(*more)) if more else "")
    return ('<a class="card" href="%s">%s</a>' % (href, inner)) if href else '<div class="card">%s</div>' % inner


def stl(pg, x, y, pt, es, en, cls="lb", anchor="start"):
    return pg.t(pt, es, en, "text", attrs=' x="%s" y="%s" class="%s" text-anchor="%s"' % (x, y, cls, anchor))


# ------------------------------------------------------------------ ilustrações
def svg_signature(pg):
    return f'''<svg class="sig" viewBox="0 0 560 300" role="img" aria-label="Assinatura basal e desvio">
<defs><linearGradient id="band" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#5E9F3A" stop-opacity=".22"/><stop offset="1" stop-color="#5E9F3A" stop-opacity=".05"/></linearGradient></defs>
<rect x="0" y="0" width="560" height="300" rx="20" fill="#2E1D10"/>
<g stroke="#4E3520" stroke-width="1">{"".join('<line x1="40" x2="530" y1="%d" y2="%d"/>' % (y, y) for y in (60, 110, 160, 210, 250))}</g>
<path d="M40 150 C110 120 150 175 220 150 S330 120 380 148" fill="none" stroke="url(#band)" stroke-width="46" stroke-linecap="round"/>
<path d="M40 150 C110 120 150 175 220 150 S330 120 380 148" fill="none" stroke="#8FCB5A" stroke-width="3"/>
<path d="M380 148 C420 160 445 190 470 215 S510 245 528 252" fill="none" stroke="#FFB500" stroke-width="3" stroke-dasharray="7 5"/>
<circle cx="430" cy="172" r="7" fill="#FFB500"/><circle cx="430" cy="172" r="15" fill="none" stroke="#FFB500" stroke-opacity=".5"/>
{stl(pg, 46, 40, "Assinatura basal do talhão, do animal ou da máquina", "Firma basal del lote, del animal o de la máquina", "Baseline signature of the field, animal or machine", "lb lw")}
{stl(pg, 412, 200, "desvio detectado", "desvío detectado", "deviation detected", "lb lo", "end")}
{stl(pg, 528, 280, "problema (se nada for feito)", "problema (si no se actúa)", "failure (if nothing is done)", "lb lm", "end")}
{stl(pg, 46, 280, "faixa normal aprendida pelo RAPP", "rango normal aprendido por el RAPP", "normal range learned by RAPP", "lb lg")}
</svg>'''


def svg_movel(pg):
    # motorhome 4x4 de 7,75 m sobre chassi de caminhão leve, em corte lateral (frente à direita)
    return f'''<svg class="draw" viewBox="0 0 1000 440" role="img" aria-label="Unidade móvel Help Farm em corte">
<rect width="1000" height="440" rx="22" fill="#F7F1E7"/>
<line x1="20" x2="980" y1="378" y2="378" stroke="#CDBB9F" stroke-width="2"/>
<!-- teto: painel solar, antena e ar -->
<g>{"".join('<rect x="%d" y="104" width="78" height="14" rx="2" fill="#123B6B" stroke="#0B2747"/>' % x for x in (176, 260, 344, 428, 512))}
{"".join('<line x1="%d" x2="%d" y1="104" y2="118" stroke="#4E7BB0" stroke-width="1"/>' % (x, x) for x in range(196, 590, 20))}</g>
<rect x="606" y="96" width="50" height="9" rx="3" fill="#E9EEF0" stroke="#9A8570"/><rect x="627" y="105" width="8" height="15" fill="#9A8570"/>
<!-- toldo recolhido -->
<rect x="170" y="126" width="470" height="8" rx="4" fill="#CDBB9F"/>
<!-- carroceria + capuchino -->
<path d="M150 120 L690 120 Q704 120 704 134 L704 332 L150 332 Q136 332 136 318 L136 134 Q136 120 150 120 Z" fill="#FFFFFF" stroke="#4A2F1B" stroke-width="4"/>
<!-- cabine de caminhão leve 4x4 -->
<path d="M712 150 L858 150 Q878 150 882 170 L898 248 L912 260 L912 320 Q912 332 900 332 L712 332 Z" fill="#F4EEE4" stroke="#4A2F1B" stroke-width="4"/>
<path d="M726 164 L852 164 L868 234 L726 234 Z" fill="#CFE3B4" opacity=".9"/>
<rect x="712" y="132" width="150" height="10" rx="3" fill="#9A8570"/>
<rect x="890" y="282" width="22" height="10" rx="3" fill="#FFB500"/>
<rect x="896" y="298" width="18" height="30" rx="3" fill="#9A8570"/>
<!-- divisórias internas -->
<g stroke="#4A2F1B" stroke-width="2"><line x1="322" x2="322" y1="124" y2="330"/><line x1="410" x2="410" y1="124" y2="330"/><line x1="470" x2="470" y1="124" y2="330"/></g>
<!-- dormitório traseiro com beliche -->
<rect x="148" y="214" width="166" height="12" rx="3" fill="#4A2F1B"/><rect x="148" y="304" width="166" height="12" rx="3" fill="#4A2F1B"/>
<rect x="152" y="199" width="158" height="15" rx="6" fill="#CFE3B4"/><rect x="152" y="289" width="158" height="15" rx="6" fill="#CFE3B4"/>
<rect x="190" y="146" width="80" height="34" rx="6" fill="#DCEEF7" stroke="#6E5644"/>
<!-- banheiro com box -->
<rect x="332" y="262" width="30" height="40" rx="8" fill="#E4D7C4" stroke="#6E5644"/><rect x="370" y="140" width="32" height="170" rx="4" fill="#DCEEF7" stroke="#6E5644"/>
<path d="M386 150 l0 14" stroke="#6E5644" stroke-width="3"/>
<!-- porta de entrada -->
<rect x="420" y="150" width="40" height="176" rx="6" fill="#F7F1E7" stroke="#6E5644" stroke-dasharray="5 4"/>
<rect x="426" y="166" width="28" height="44" rx="4" fill="#DCEEF7"/>
<!-- bancada de medição (antiga sala) -->
<rect x="480" y="258" width="212" height="12" fill="#6E5644"/>
<rect x="488" y="222" width="42" height="34" rx="4" fill="#5E9F3A"/><rect x="536" y="226" width="34" height="30" rx="4" fill="#FFB500"/><rect x="576" y="216" width="28" height="40" rx="4" fill="#6E5644"/><rect x="610" y="228" width="40" height="28" rx="4" fill="#5E9F3A" opacity=".7"/>
<rect x="656" y="200" width="32" height="56" rx="4" fill="#EFE4D2" stroke="#6E5644"/>
<rect x="488" y="276" width="200" height="48" rx="6" fill="#EFE4D2" stroke="#6E5644"/>
<rect x="490" y="150" width="200" height="40" rx="6" fill="#EFE4D2" stroke="#6E5644"/>
<g fill="#4A2F1B"><circle cx="514" cy="170" r="8"/><circle cx="548" cy="170" r="8"/><rect x="518" y="166" width="26" height="8"/>
<circle cx="582" cy="170" r="8"/><circle cx="616" cy="170" r="8"/><rect x="586" y="166" width="26" height="8"/></g>
<!-- rack traseiro com 2 motos trail -->
<rect x="18" y="306" width="122" height="9" rx="2" fill="#6E5644"/><rect x="128" y="290" width="12" height="24" fill="#6E5644"/>
<g opacity=".45" transform="translate(10,-10)"><g fill="none" stroke="#2A1C10" stroke-width="7"><circle cx="40" cy="289" r="15"/><circle cx="120" cy="289" r="15"/></g><path d="M40 289 L60 268 L98 268 L120 289" fill="none" stroke="#6E5644" stroke-width="5"/></g>
<g fill="none" stroke="#2A1C10" stroke-width="7"><circle cx="40" cy="289" r="15"/><circle cx="120" cy="289" r="15"/></g>
<rect x="60" y="272" width="26" height="18" rx="3" fill="#6E5644"/>
<path d="M40 289 L62 268 L94 264 L120 289" fill="none" stroke="#4A2F1B" stroke-width="5" stroke-linejoin="round"/>
<path d="M66 264 Q78 252 96 256 L102 264 Z" fill="#FFB500"/>
<path d="M50 262 L86 260" stroke="#2A1C10" stroke-width="6" stroke-linecap="round"/>
<path d="M106 268 L98 246 M92 244 L108 246" stroke="#2A1C10" stroke-width="4" stroke-linecap="round"/>
<path d="M98 246 L120 289" stroke="#9A8570" stroke-width="4"/>
<!-- rodas: rodado duplo traseiro e dianteira -->
<g fill="#2A1C10"><circle cx="262" cy="340" r="40"/><circle cx="800" cy="340" r="40"/></g>
<g fill="#CDBB9F"><circle cx="262" cy="340" r="15"/><circle cx="800" cy="340" r="15"/></g>
<!-- rótulos -->
<line x1="215" y1="102" x2="215" y2="62" stroke="#5E9F3A" stroke-width="1.5"/>
{stl(pg, 176, 54, "Painel solar + baterias de lítio", "Panel solar + baterías de litio", "Solar panel + lithium batteries", "lb")}
{stl(pg, 690, 82, "Antena satelital (internet em qualquer lugar)", "Antena satelital (internet en cualquier lugar)", "Satellite antenna (internet anywhere)", "lb", "end")}
{stl(pg, 655, 175, "Drones", "Drones", "Drones", "ls", "middle")}
{stl(pg, 586, 210, "Instrumentos portáteis", "Instrumentos portátiles", "Portable instruments", "ls", "middle")}
{stl(pg, 588, 306, "Sensores para instalar", "Sensores a instalar", "Sensors to install", "ls", "middle")}
{stl(pg, 440, 346, "Entrada", "Entrada", "Door", "ls", "middle")}
{stl(pg, 366, 346, "Banheiro", "Baño", "Bathroom", "ls", "middle")}
{stl(pg, 232, 252, "Dormitório com beliche", "Dormitorio con litera", "Bunk-bed sleeping area", "ls", "middle")}
{stl(pg, 80, 236, "2 motos trail", "2 motos trail", "2 trail bikes", "lb", "middle")}
{stl(pg, 262, 412, "Pneus de uso misto (terra e asfalto)", "Neumáticos de uso mixto (tierra y asfalto)", "All-terrain tyres", "lb", "middle")}
{stl(pg, 806, 412, "Chassi de caminhão leve 4x4", "Chasis de camión liviano 4x4", "4x4 light-truck chassis", "lb", "middle")}
{stl(pg, 590, 144, "Bancada de medição (no lugar da sala)", "Mesada de medición (en lugar del living)", "Measuring bench (replaces the lounge)", "ls", "middle")}
</svg>'''


# ------------------------------------------------------------------ páginas
def home():
    pg = Page()
    title = pg.title("Help Farm — a sua fazenda avisa antes do problema",
                     "Help Farm — su establecimiento avisa antes del problema",
                     "Help Farm — your farm warns before the problem")
    domains = [
        (("Solo", "Umidade em perfil, compactação, pH, condutividade e nutrientes."), ("Suelo", "Humedad en perfil, compactación, pH, conductividad y nutrientes."), ("Soil", "Moisture by depth, compaction, pH, conductivity and nutrients.")),
        (("Lavoura", "Índices de vigor por satélite e drone, pragas e doenças."), ("Cultivo", "Índices de vigor por satélite y dron, plagas y enfermedades."), ("Crops", "Vigour indices from satellite and drone, pests and disease.")),
        (("Clima", "Estação local, risco de geada, seca e chuva forte."), ("Clima", "Estación local, riesgo de helada, sequía y lluvia fuerte."), ("Weather", "Local station, frost, drought and heavy-rain risk.")),
        (("Gado", "Peso, temperatura, ruminação, água e comportamento do rebanho."), ("Ganado", "Peso, temperatura, rumia, agua y comportamiento del rodeo."), ("Livestock", "Weight, temperature, rumination, water and herd behaviour.")),
        (("Máquinas", "Vibração, corrente e falhas de tratores, pivôs e bombas."), ("Máquinas", "Vibración, corriente y fallas de tractores, pivotes y bombas."), ("Machines", "Vibration, current and faults of tractors, pivots and pumps.")),
    ]
    steps = [
        (("Diagnóstico remoto", "Antes da visita, o histórico de satélite e de clima da fazenda mostra onde olhar primeiro."), ("Diagnóstico remoto", "Antes de la visita, el historial satelital y climático del establecimiento muestra dónde mirar primero."), ("Remote diagnosis", "Before the visit, the farm’s satellite and weather history shows where to look first.")),
        (("A unidade móvel chega", "Dois profissionais ficam instalados na fazenda, com drones, instrumentos portáteis e duas motos para percorrer talhões e pastos."), ("Llega la unidad móvil", "Dos profesionales se instalan en el establecimiento, con drones, instrumentos portátiles y dos motos para recorrer lotes y potreros."), ("The mobile unit arrives", "Two professionals stay on the farm with drones, portable instruments and two bikes to cover fields and pastures.")),
        (("Medição completa", "Solo, planta, água, clima, rebanho e máquinas são medidos e georreferenciados; os sensores fixos ficam instalados."), ("Medición completa", "Suelo, planta, agua, clima, rodeo y máquinas se miden y georreferencian; los sensores fijos quedan instalados."), ("Full measurement", "Soil, plants, water, weather, herd and machines are measured and geo-referenced; fixed sensors stay in place.")),
        (("Assinatura e alertas", "O motor RAPP aprende o normal de cada talhão, animal e máquina e avisa quando algo começa a sair do padrão."), ("Firma y alertas", "El motor RAPP aprende lo normal de cada lote, animal y máquina y avisa cuando algo empieza a salir del patrón."), ("Signature and alerts", "The RAPP engine learns what is normal for each field, animal and machine and warns when something starts to drift.")),
    ]
    imgs = ["solo", "pragas", "geada", "gado", "pivo"]
    body = f'''
<div class="hero hv">
  <div class="wrap">
    <div>
      {pg.t("Help Farm · motor RAPP", "Help Farm · motor RAPP", "Help Farm · RAPP engine", "span", "eyebrow")}
      {pg.t("A sua fazenda <em>avisa antes</em> do problema.", "Su establecimiento <em>avisa antes</em> del problema.", "Your farm <em>warns before</em> the problem.", "h1", raw=True)}
      {pg.t("Medimos solo, lavoura, clima, gado e máquinas, aprendemos a assinatura normal de cada um e disparamos a ação antes da perda — a mesma inteligência de manutenção preditiva usada em turbinas de plataforma de petróleo, agora no campo.", "Medimos suelo, cultivo, clima, ganado y máquinas, aprendemos la firma normal de cada uno y disparamos la acción antes de la pérdida — la misma inteligencia de mantenimiento predictivo usada en turbinas de plataformas petroleras, ahora en el campo.", "We measure soil, crops, weather, livestock and machines, learn each one’s normal signature and trigger action before the loss — the same predictive-maintenance intelligence used on offshore oil turbines, now in the field.", "p", "lead")}
      <div class="cta"><a class="btn primary" href="unidade-movel.html">{pg.t("Conheça a unidade móvel", "Conozca la unidad móvil", "See the mobile unit")}</a><a class="btn ghost" href="investidores.html">{pg.t("Para investidores", "Para inversionistas", "For investors")}</a></div>
    </div>
    <div class="hv-media sigbox">{svg_signature(pg)}</div>
  </div>
</div>
{film(pg)}

<section>
  <div class="wrap">
    <div class="head">{pg.t("O que medimos", "Qué medimos", "What we measure", "span", "eyebrow")}{pg.t("Cinco frentes, um só histórico da fazenda.", "Cinco frentes, un solo historial del establecimiento.", "Five fronts, one farm history.", "h2")}
    {pg.t("Cada medição entra na mesma linha do tempo. É o cruzamento entre elas — chuva com solo, solo com planta, calor com rebanho, máquina com safra — que permite prever.", "Cada medición entra en la misma línea de tiempo. Es el cruce entre ellas — lluvia con suelo, suelo con planta, calor con rodeo, máquina con cosecha — lo que permite predecir.", "Every measurement goes on the same timeline. Crossing them — rain with soil, soil with plants, heat with herd, machines with harvest — is what makes prediction possible.", "p", "muted")}</div>
    <div class="g g5 photocards">{"".join(card(pg, a, b, c, img=imgs[i]) for i, (a, b, c) in enumerate(domains))}</div>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <div class="head">{pg.t("Como funciona", "Cómo funciona", "How it works", "span", "eyebrow")}{pg.t("Do diagnóstico ao alerta, em quatro passos.", "Del diagnóstico a la alerta, en cuatro pasos.", "From diagnosis to alert, in four steps.", "h2")}</div>
    <div class="g g4 steps">{"".join('<div class="step">%s%s</div>' % (pg.t(a[0], b[0], c[0], "h3"), pg.t(a[1], b[1], c[1], "p")) for a, b, c in steps)}</div>
    {explainer(pg, "home", ("Como a Help Farm funciona", "Cómo funciona Help Farm", "How Help Farm works"), "≈ 90 s", [
        ("A fazenda negocia com a natureza: clima, pragas e solo decidem o lucro", "El establecimiento negocia con la naturaleza: clima, plagas y suelo deciden la ganancia", "The farm bargains with nature: weather, pests and soil decide the profit"),
        ("A unidade móvel mede tudo e deixa sensores trabalhando", "La unidad móvil mide todo y deja sensores trabajando", "The mobile unit measures everything and leaves sensors working"),
        ("O RAPP aprende a assinatura normal de cada talhão, animal e máquina", "El RAPP aprende la firma normal de cada lote, animal y máquina", "RAPP learns the normal signature of each field, animal and machine"),
        ("O desvio aparece dias antes da perda e vira alerta", "El desvío aparece días antes de la pérdida y se vuelve alerta", "The deviation shows up days before the loss and becomes an alert"),
        ("A equipe certa age a tempo: agrônomo, veterinário, mecânico", "El equipo correcto actúa a tiempo: agrónomo, veterinario, mecánico", "The right team acts in time: agronomist, vet, mechanic")])}
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head">{pg.t("Estrutura de campo", "Estructura de campo", "Field structure", "span", "eyebrow")}{pg.t("Os profissionais vão até a fazenda — e ficam o tempo que for preciso.", "Los profesionales van hasta el establecimiento — y se quedan el tiempo que haga falta.", "The professionals go to the farm — and stay as long as needed.", "h2")}</div>
    <figure class="photo"><a href="unidade-movel.html"><img src="img/movel-fazenda.webp" srcset="img/movel-fazenda-960.webp 960w, img/movel-fazenda.webp 1568w" sizes="(max-width:1180px) 100vw, 1140px" alt="Unidade móvel Help Farm numa fazenda" loading="lazy"></a><figcaption>{pg.t("Imagem conceitual da unidade móvel: motorhome 4x4 com painel solar, antena satelital, drone, bancada externa e duas motos trail.", "Imagen conceptual de la unidad móvil: motorhome 4x4 con panel solar, antena satelital, dron, mesada exterior y dos motos trail.", "Concept image of the mobile unit: 4x4 motorhome with solar panel, satellite antenna, drone, outdoor bench and two trail bikes.")}</figcaption></figure>
    <div class="split" style="margin-top:28px;align-items:start">
      <div>{pg.t("Unidade móvel de medição", "Unidad móvil de medición", "Mobile measuring unit", "h3")}{pg.t("Um motorhome 4x4 de 7,75 m sobre chassi de caminhão leve com instrumentos, drones, dormitório, banheiro, energia solar, antena satelital e duas motos trail.", "Un motorhome 4x4 de 7,75 m sobre chasis de camión liviano con instrumentos, drones, dormitorio, baño, energía solar, antena satelital y dos motos trail.", "A 7.75 m 4x4 motorhome on a light-truck chassis with instruments, drones, sleeping area, bathroom, solar power, satellite antenna and two trail bikes.", "p", "muted", attrs=' style="margin-top:10px"')}</div>
      <div>{pg.t("Visita ou temporada", "Visita o temporada", "Visit or season", "h3")}{pg.t("Numa visita, mede, instala os sensores e segue para a próxima fazenda. Nas fazendas que precisam de acompanhamento contínuo, fica estacionada por temporada — plantio, colheita ou estação de monta — com a dupla morando a bordo.", "En una visita, mide, instala los sensores y sigue al próximo establecimiento. En los que necesitan acompañamiento continuo, se queda estacionada por temporada — siembra, cosecha o servicio — con la dupla viviendo a bordo.", "On a visit, it measures, installs the sensors and moves on to the next farm. Where a farm needs continuous follow-up, it stays parked for a season — planting, harvest or breeding — with the pair living on board.", "p", "muted", attrs=' style="margin-top:10px"')}
      <div class="cta" style="margin-top:18px"><a class="btn dark" href="unidade-movel.html">{pg.t("Ver a unidade móvel", "Ver la unidad móvil", "See the mobile unit")} →</a></div></div>
    </div>
  </div>
</section>

{cert_band(pg)}

<section class="soft">
  <div class="wrap split">
    <div>
      {pg.t("Por que agora", "Por qué ahora", "Why now", "span", "eyebrow")}
      {pg.t("O sensor já é barato. Falta quem avise antes.", "El sensor ya es barato. Falta quien avise antes.", "Sensors are already cheap. What is missing is an early warning.", "h2")}
      {pg.t("Governos da região compram brincos eletrônicos por menos de um dólar e a rastreabilidade do rebanho virou obrigatória no Paraguai, no Brasil e na Argentina. Imagens de satélite são gratuitas a cada cinco dias. O que o produtor ainda não tem é uma inteligência que junte tudo isso e diga, com dias de antecedência, onde vai dar problema.", "Los gobiernos de la región compran caravanas electrónicas por menos de un dólar y la trazabilidad del rodeo se volvió obligatoria en Paraguay, Brasil y Argentina. Las imágenes satelitales son gratuitas cada cinco días. Lo que el productor aún no tiene es una inteligencia que junte todo eso y diga, con días de anticipación, dónde habrá un problema.", "Governments in the region buy electronic ear tags for under a dollar and herd traceability is now mandatory in Paraguay, Brazil and Argentina. Satellite images are free every five days. What producers still lack is an intelligence that brings it all together and says, days in advance, where trouble is coming.", "p", "muted")}
    </div>
    <div class="kpis">
      <div class="kpi"><b>2–7</b>{pg.t("dias de antecedência na detecção de doenças do gado, em estudos publicados", "días de anticipación en la detección de enfermedades del ganado, en estudios publicados", "days of early warning for cattle disease, in published studies", "span")}</div>
      <div class="kpi"><b>13</b>{pg.t("dias antes do sintoma visível: doença foliar detectada por imagem multiespectral", "días antes del síntoma visible: enfermedad foliar detectada por imagen multiespectral", "days before visible symptoms: leaf disease detected by multispectral imaging", "span")}</div>
      <div class="kpi"><b>12,8 mi</b>{pg.t("cabeças de gado no Paraguai, primeiro mercado", "cabezas de ganado en Paraguay, primer mercado", "head of cattle in Paraguay, first market", "span")}</div>
      <div class="kpi"><b>3,7 mi ha</b>{pg.t("de soja no Paraguai na safra 2025/26", "de soja en Paraguay en la zafra 2025/26", "of soybeans in Paraguay in the 2025/26 season", "span")}</div>
    </div>
  </div>
</section>
'''
    shell(pg, "index.html", title, body, "Help Farm: monitoramento preditivo de solo, lavoura, clima, gado e máquinas com o motor RAPP.")


def movel():
    pg = Page()
    title = pg.title("Unidade móvel — Help Farm", "Unidad móvil — Help Farm", "Mobile unit — Help Farm")
    kit = [
        (("Solo", "penetrômetro digital (compactação), sonda TDR portátil (umidade), medidor de pH, condutividade e temperatura, espectrômetro NIR portátil (matéria orgânica e nutrientes) e trado para amostras georreferenciadas"),
         ("Suelo", "penetrómetro digital (compactación), sonda TDR portátil (humedad), medidor de pH, conductividad y temperatura, espectrómetro NIR portátil (materia orgánica y nutrientes) y barreno para muestras georreferenciadas"),
         ("Soil", "digital penetrometer (compaction), portable TDR probe (moisture), pH, conductivity and temperature meter, portable NIR spectrometer (organic matter and nutrients) and auger for geo-referenced samples")),
        (("Lavoura", "drone multiespectral (vigor e estresse), drone de mapeamento (ortofoto e relevo), medidor de clorofila, câmera termográfica e refratômetro"),
         ("Cultivo", "dron multiespectral (vigor y estrés), dron de mapeo (ortofoto y relieve), medidor de clorofila, cámara termográfica y refractómetro"),
         ("Crops", "multispectral drone (vigour and stress), mapping drone (orthophoto and terrain), chlorophyll meter, thermal camera and refractometer")),
        (("Clima e água", "estação meteorológica portátil, sensor de molhamento foliar, pluviômetros e sonda multiparâmetro para bebedouros, açudes e poços"),
         ("Clima y agua", "estación meteorológica portátil, sensor de mojado foliar, pluviómetros y sonda multiparámetro para bebederos, tajamares y pozos"),
         ("Weather and water", "portable weather station, leaf-wetness sensor, rain gauges and multi-parameter probe for troughs, ponds and wells")),
        (("Gado", "leitor de brinco eletrônico, balança portátil, termômetro infravermelho e bolus para os animais sentinela"),
         ("Ganado", "lector de caravana electrónica, balanza portátil, termómetro infrarrojo y bolos para los animales centinela"),
         ("Livestock", "electronic ear-tag reader, portable scale, infrared thermometer and boluses for sentinel animals")),
        (("Máquinas", "analisador de vibração portátil, pinça amperimétrica e leitor do barramento CAN/ISOBUS de tratores e colheitadeiras"),
         ("Máquinas", "analizador de vibración portátil, pinza amperimétrica y lector del bus CAN/ISOBUS de tractores y cosechadoras"),
         ("Machines", "portable vibration analyser, clamp meter and CAN/ISOBUS bus reader for tractors and harvesters")),
        (("Posição", "receptor GNSS RTK para que cada ponto medido volte ao mesmo lugar na próxima visita"),
         ("Posición", "receptor GNSS RTK para que cada punto medido vuelva al mismo lugar en la próxima visita"),
         ("Position", "GNSS RTK receiver so every measured point is revisited at exactly the same spot")),
    ]
    ficha = [
        (("Base", "motorhome 4x4 de 7,75 m sobre chassi de caminhão leve 4x4, já fabricado em série no Brasil, para estrada de terra"), ("Base", "motorhome 4x4 de 7,75 m sobre chasis de camión liviano 4x4, ya fabricado en serie en Brasil, para caminos de tierra"), ("Base", "7.75 m 4x4 motorhome on a 4x4 light-truck chassis, already built in series in Brazil, for dirt roads")),
        (("Acomodação", "de 6 lugares de passeio para 2 profissionais em beliche; o espaço liberado vira laboratório"), ("Alojamiento", "de 6 plazas de paseo a 2 profesionales en litera; el espacio liberado se vuelve laboratorio"), ("Sleeping", "from 6 leisure berths to 2 staff in bunk beds; the space freed becomes the lab")),
        (("Sala", "a sala com mesa dá lugar à bancada de medição, com instrumentos, drones e geladeira de amostras"), ("Living", "el living con mesa da lugar a la mesada de medición, con instrumentos, drones y heladera de muestras"), ("Lounge", "the dinette becomes the measuring bench, with instruments, drones and a sample fridge")),
        (("Banheiro e água", "banheiro com chuveiro; caixas de 500 L de água limpa, 200 L de servida e 100 L de detritos (modelo de série)"), ("Baño y agua", "baño con ducha; tanques de 500 L de agua limpia, 200 L de grises y 100 L de residuos (modelo de serie)"), ("Bathroom and water", "bathroom with shower; 500 L fresh, 200 L grey and 100 L waste tanks (series model)")),
        (("Energia", "painel solar com controlador e bateria estacionária de série, mais baterias de lítio e inversor na adaptação"), ("Energía", "panel solar con controlador y batería estacionaria de serie, más baterías de litio e inversor en la adaptación"), ("Power", "series solar panel, charge controller and stationary battery, plus lithium batteries and inverter added")),
        (("Internet", "antena satelital no teto, para subir os dados no mesmo dia"), ("Internet", "antena satelital en el techo, para subir los datos el mismo día"), ("Internet", "rooftop satellite antenna to upload data the same day")),
        (("Traseira", "suporte de motos de série, reforçado para levar 2 motos trail simples"), ("Trasera", "soporte de motos de serie, reforzado para llevar 2 motos trail simples"), ("Rear", "series motorbike mount, reinforced to carry 2 simple trail bikes")),
        (("Apoio externo", "cozinha e chuveiro externos de série e toldo para montar a bancada de campo ao lado do veículo"), ("Apoyo exterior", "cocina y ducha exteriores de serie y toldo para armar la mesada de campo junto al vehículo"), ("Outdoor support", "series outdoor kitchen and shower, plus awning to set up the field bench beside the vehicle")),
    ]
    res = [
        (("Dois profissionais instalados", "Um agrônomo e um técnico (ou veterinário) ficam na fazenda durante a campanha de medição, sem depender de hotel na cidade."), ("Dos profesionales instalados", "Un agrónomo y un técnico (o veterinario) se quedan en el establecimiento durante la campaña de medición, sin depender de hotel en la ciudad."), ("Two professionals on site", "An agronomist and a technician (or vet) stay on the farm during the measuring campaign, with no need for a hotel in town.")),
        (("Dormitório e banheiro", "Beliche para dois, banheiro com chuveiro, caixa d’água de 500 L e ar-condicionado."), ("Dormitorio y baño", "Litera para dos, baño con ducha, tanque de agua y climatización."), ("Sleeping area and bathroom", "Bunk bed for two, bathroom with shower, water tank and climate control.")),
        (("Energia própria", "Painel solar no teto com baterias de lítio para instrumentos, drones e a vida a bordo."), ("Energía propia", "Panel solar en el techo con baterías de litio para instrumentos, drones y la vida a bordo."), ("Own power", "Rooftop solar panel with lithium batteries for instruments, drones and life on board.")),
        (("Conectada em qualquer lugar", "Antena satelital no teto: os dados sobem para o motor RAPP no mesmo dia."), ("Conectada en cualquier lugar", "Antena satelital en el techo: los datos suben al motor RAPP el mismo día."), ("Connected anywhere", "Rooftop satellite antenna: data reaches the RAPP engine the same day.")),
        (("Duas motos trail", "No suporte traseiro, para chegar a talhões, pastos e aguadas onde o motorhome não entra."), ("Dos motos trail", "En el soporte trasero, para llegar a lotes, potreros y aguadas donde el motorhome no entra."), ("Two trail bikes", "On the rear rack, to reach fields, pastures and water points the motorhome cannot.")),
        (("Visita ou temporada", "Numa visita, mede e instala os sensores; nas fazendas que precisam de acompanhamento contínuo, fica estacionada a temporada inteira."), ("Visita o temporada", "En una visita, mide e instala los sensores; en los establecimientos que necesitan acompañamiento continuo, se queda estacionada toda la temporada."), ("Visit or season", "On a visit it measures and installs sensors; on farms needing continuous follow-up it stays parked for the whole season.")),
        (("Drones a bordo", "Voos multiespectrais e de mapeamento no primeiro dia; a mesma rota se repete nas visitas seguintes."), ("Drones a bordo", "Vuelos multiespectrales y de mapeo el primer día; la misma ruta se repite en las visitas siguientes."), ("Drones on board", "Multispectral and mapping flights on day one; the same route is repeated on later visits.")),
    ]
    body = f'''
<div class="hero sub hfphoto">
  <img src="img/movel-fazenda.webp" alt="" fetchpriority="high">
  <div class="wrap">
    <p class="crumb"><a href="./">Help Farm</a> / {pg.t("Unidade móvel", "Unidad móvil", "Mobile unit")}</p>
    {pg.t("O laboratório de campo que dorme na fazenda.", "El laboratorio de campo que duerme en el establecimiento.", "The field lab that sleeps on the farm.", "h1")}
    {pg.t("Um motorhome 4x4 de 7,75 m sobre chassi de caminhão leve leva dois profissionais, drones e instrumentos portáteis até a fazenda. Eles ficam instalados o tempo necessário para medir todas as variáveis, deixam os sensores fixos funcionando e criam a assinatura de referência de cada talhão, rebanho e máquina.", "Un motorhome 4x4 de 7,75 m sobre chasis de camión liviano lleva dos profesionales, drones e instrumentos portátiles hasta el establecimiento. Se quedan el tiempo necesario para medir todas las variables, dejan los sensores fijos funcionando y crean la firma de referencia de cada lote, rodeo y máquina.", "A 7.75 m 4x4 motorhome on a light-truck chassis takes two professionals, drones and portable instruments to the farm. They stay as long as needed to measure every variable, leave the fixed sensors running and build the reference signature of each field, herd and machine.", "p", "lead")}
  </div>
</div>
<section>
  <div class="wrap">
    <div class="head">{pg.t("Em corte (esquema)", "En corte (esquema)", "Cutaway (schematic)", "span", "eyebrow")}{pg.t("Tudo cabe num motorhome.", "Todo cabe en un motorhome.", "It all fits in a motorhome.", "h2")}</div>
    <div class="figure">{svg_movel(pg)}</div>
    {feats(pg, res)}
    {explainer(pg, "movel", ("Uma visita da unidade móvel", "Una visita de la unidad móvil", "A mobile-unit visit"), "≈ 60 s", [
        ("O motorhome chega pela estrada de terra com a dupla, drones e motos", "El motorhome llega por el camino de tierra con la dupla, drones y motos", "The motorhome arrives by dirt road with the pair, drones and bikes"),
        ("Drones voam a fazenda e marcam os pontos a medir", "Los drones vuelan el establecimiento y marcan los puntos a medir", "Drones fly the farm and mark the points to measure"),
        ("De moto, solo, planta, água, rebanho e máquinas são medidos", "En moto se miden suelo, planta, agua, rodeo y máquinas", "On the bikes, soil, plants, water, herd and machines are measured"),
        ("Sensores ficam instalados e a primeira assinatura sobe por satélite", "Los sensores quedan instalados y la primera firma sube por satélite", "Sensors stay in place and the first signature goes up via satellite")])}
  </div>
</section>
<section class="soft">
  <div class="wrap">
    <div class="head">{pg.t("No campo", "En el campo", "In the field", "span", "eyebrow")}{pg.t("A unidade móvel em ação.", "La unidad móvil en acción.", "The mobile unit in action.", "h2")}</div>
    <div class="gallery">
      <figure class="g-big"><img src="img/f/movel-estrada.webp" alt="Unidade móvel Help Farm chegando à fazenda" loading="lazy"><figcaption>{pg.t("Chegada à fazenda, com drone em voo.", "Llegada al establecimiento, con dron en vuelo.", "Arriving at the farm, drone in flight.")}</figcaption></figure>
      <figure><img src="img/f/tecnicos-2.webp" alt="" loading="lazy"><figcaption>{pg.t("Bancada de medição e drones a bordo.", "Mesada de medición y drones a bordo.", "Measuring bench and drones on board.")}</figcaption></figure>
      <figure><img src="img/f/tecnicos.webp" alt="" loading="lazy"><figcaption>{pg.t("A dupla em contato com a central.", "La dupla en contacto con la central.", "The pair in touch with the control centre.")}</figcaption></figure>
      <figure><img src="img/f/produtor.webp" alt="" loading="lazy"><figcaption>{pg.t("O produtor acompanha pelo tablet.", "El productor sigue todo en la tableta.", "The farmer follows on a tablet.")}</figcaption></figure>
    </div>
    {pg.t("Imagens conceituais geradas para o filme institucional.", "Imágenes conceptuales generadas para la película institucional.", "Concept images made for the corporate film.", "p", "note", attrs=' style="margin-top:18px"')}
  </div>
</section>
<section>
  <div class="wrap">
    <div class="head">{pg.t("Ficha da unidade", "Ficha de la unidad", "Unit specification", "span", "eyebrow")}{pg.t("Um motorhome de série, adaptado para medir.", "Un motorhome de serie, adaptado para medir.", "A series motorhome, adapted to measure.", "h2")}
    {pg.t("Partir de um modelo que já é fabricado reduz prazo e custo: o veículo vem pronto para morar, e a adaptação fica só no que é de medição.", "Partir de un modelo que ya se fabrica reduce plazo y costo: el vehículo viene listo para vivir, y la adaptación queda solo en lo que es de medición.", "Starting from a model already in production cuts time and cost: the vehicle comes ready to live in, and the conversion covers only the measuring parts.", "p", "muted")}</div>
    {feats(pg, ficha)}
  </div>
</section>
<section class="soft">
  <div class="wrap">
    <div class="head">{pg.t("Instrumentos portáteis", "Instrumentos portátiles", "Portable instruments", "span", "eyebrow")}{pg.t("O kit de medição inicial.", "El kit de medición inicial.", "The initial measuring kit.", "h2")}
    {pg.t("Proposta de partida, a validar com a equipe técnica. Começamos com instrumentos portáteis; o que se mostrar mais útil vira sensor fixo na fazenda.", "Propuesta de partida, a validar con el equipo técnico. Empezamos con instrumentos portátiles; lo que resulte más útil pasa a ser sensor fijo en el establecimiento.", "Starting proposal, to be validated with the technical team. We start with portable instruments; whatever proves most useful becomes a fixed sensor on the farm.", "p", "muted")}</div>
    {feats(pg, kit)}
  </div>
</section>
<section>
  <div class="wrap">
    <div class="head">{pg.t("Uma visita", "Una visita", "One visit", "span", "eyebrow")}{pg.t("O que acontece na fazenda.", "Qué pasa en el establecimiento.", "What happens on the farm.", "h2")}</div>
    <div class="g g4 steps">
      <div class="step">{pg.t("Chegada e voo", "Llegada y vuelo", "Arrival and flight", "h3")}{pg.t("Base montada, drones voam a fazenda inteira e o mapa de vigor sai no mesmo dia.", "Base montada, los drones vuelan todo el establecimiento y el mapa de vigor sale el mismo día.", "Base set up, drones fly the whole farm and the vigour map is ready the same day.", "p")}</div>
      <div class="step">{pg.t("Pontos de medição", "Puntos de medición", "Measuring points", "h3")}{pg.t("De moto, a dupla mede solo, planta e água nos pontos escolhidos pelo mapa e marca cada um com GPS de precisão.", "En moto, la dupla mide suelo, planta y agua en los puntos elegidos por el mapa y marca cada uno con GPS de precisión.", "On the bikes, the pair measures soil, plants and water at map-chosen points and tags each with precision GPS.", "p")}</div>
      <div class="step">{pg.t("Rebanho e máquinas", "Rodeo y máquinas", "Herd and machines", "h3")}{pg.t("Pesagem e leitura dos brincos, bolus nos animais sentinela, vibração e corrente de pivôs, bombas e tratores.", "Pesaje y lectura de caravanas, bolos en los animales centinela, vibración y corriente de pivotes, bombas y tractores.", "Weighing and ear-tag reading, boluses in sentinel animals, vibration and current of pivots, pumps and tractors.", "p")}</div>
      <div class="step">{pg.t("Sensores e assinatura", "Sensores y firma", "Sensors and signature", "h3")}{pg.t("Gateway e sensores fixos instalados; o RAPP recebe a primeira assinatura basal e passa a vigiar a fazenda.", "Gateway y sensores fijos instalados; el RAPP recibe la primera firma basal y pasa a vigilar el establecimiento.", "Gateway and fixed sensors installed; RAPP gets the first baseline signature and starts watching the farm.", "p")}</div>
    </div>
    <div class="nextnav"><a class="btn dark" href="tecnologia.html">{pg.t("Ver como o RAPP usa as medições", "Ver cómo el RAPP usa las mediciones", "See how RAPP uses the measurements")} →</a></div>
  </div>
</section>
'''
    shell(pg, "unidade-movel.html", title, body, "Motorhome 4x4 com instrumentos, drones, dormitório, banheiro, energia solar, antena satelital e duas motos trail.")


def tecnologia():
    pg = Page()
    title = pg.title("Tecnologia — Help Farm", "Tecnología — Help Farm", "Technology — Help Farm")
    rows = [
        (("Solo", "Solo", "Soil"), ("Umidade por profundidade, condutividade, temperatura, chuva", "Humedad por profundidad, conductividad, temperatura, lluvia", "Moisture by depth, conductivity, temperature, rain"), ("Secagem mais rápida que o normal; camada funda sem recarga; condutividade subindo", "Secado más rápido de lo normal; capa profunda sin recarga; conductividad en aumento", "Faster-than-normal drying; deep layer not recharging; rising conductivity"), ("Ajuste de irrigação, subsolagem, compra de corretivo", "Ajuste de riego, subsolado, compra de enmienda", "Irrigation adjustment, subsoiling, buying soil amendment")),
        (("Lavoura", "Cultivo", "Crops"), ("Vigor por satélite e drone, molhamento foliar, armadilhas de pragas", "Vigor por satélite y dron, mojado foliar, trampas de plagas", "Vigour from satellite and drone, leaf wetness, pest traps"), ("Vigor abaixo da curva esperada e dos vizinhos; praga acima do nível de controle", "Vigor por debajo de la curva esperada y de los vecinos; plaga por encima del umbral", "Vigour below the expected curve and neighbours; pests above threshold"), ("Vistoria guiada por GPS, reserva de defensivo, pulverizador agendado", "Recorrida guiada por GPS, reserva de fitosanitario, pulverizadora agendada", "GPS-guided scouting, crop-protection reserved, sprayer booked")),
        (("Clima", "Clima", "Weather"), ("Estação local, previsão numérica, zoneamento de risco", "Estación local, pronóstico numérico, zonificación de riesgo", "Local station, numerical forecast, risk zoning"), ("Queda rápida de temperatura com céu limpo (geada); déficit de água acima do histórico", "Caída rápida de temperatura con cielo despejado (helada); déficit hídrico por encima del histórico", "Fast temperature drop under clear sky (frost); water deficit above history"), ("Proteção contra geada, replanejamento, aviso ao seguro", "Protección contra helada, replanificación, aviso al seguro", "Frost protection, re-planning, insurer notified")),
        (("Gado", "Ganado", "Livestock"), ("Peso, temperatura, ruminação, água, índice de calor", "Peso, temperatura, rumia, agua, índice de calor", "Weight, temperature, rumination, water, heat index"), ("Ruminação caindo; febre acima da média do animal; menos tempo no cocho", "Rumia en baja; fiebre por encima del promedio del animal; menos tiempo en el comedero", "Rumination falling; fever above the animal’s average; less time at the feeder"), ("Separar o animal, reservar medicamento, chamar o veterinário", "Apartar el animal, reservar medicamento, llamar al veterinario", "Pull the animal, reserve medication, call the vet")),
        (("Máquinas", "Máquinas", "Machines"), ("Vibração, corrente do motor, pressão hidráulica, códigos CAN", "Vibración, corriente del motor, presión hidráulica, códigos CAN", "Vibration, motor current, hydraulic pressure, CAN codes"), ("Vibração crescendo na frequência de defeito; corrente do pivô subindo com a mesma velocidade", "Vibración creciente en la frecuencia de falla; corriente del pivote en alza a la misma velocidad", "Vibration growing at the fault frequency; pivot current rising at the same speed"), ("Ordem de serviço e peça comprada antes da safra", "Orden de servicio y repuesto comprado antes de la cosecha", "Work order and part bought before harvest")),
    ]
    th = "".join(pg.t(*h, "th") for h in [("Frente", "Frente", "Front"), ("O que entra", "Qué entra", "Inputs"), ("Desvio que antecede o problema", "Desvío que anticipa el problema", "Deviation that precedes the problem"), ("Ação disparada", "Acción disparada", "Action triggered")])
    trs = "".join("<tr>%s</tr>" % "".join(pg.t(*c, "td") for c in r) for r in rows)
    body = f'''
<div class="hero sub hfsub">
  <div class="wrap">
    <p class="crumb"><a href="./">Help Farm</a> / {pg.t("Tecnologia", "Tecnología", "Technology")}</p>
    {pg.t("O motor RAPP: cada ativo comparado com ele mesmo.", "El motor RAPP: cada activo comparado consigo mismo.", "The RAPP engine: every asset compared with itself.", "h1")}
    {pg.t("Criado para turbinas, bombas e compressores de plataforma de petróleo, o RAPP aprende o funcionamento normal de um equipamento e detecta o desvio que leva à falha. Na fazenda, o “equipamento” é o talhão, o animal e a máquina.", "Creado para turbinas, bombas y compresores de plataformas petroleras, el RAPP aprende el funcionamiento normal de un equipo y detecta el desvío que lleva a la falla. En el establecimiento, el “equipo” es el lote, el animal y la máquina.", "Built for offshore oil turbines, pumps and compressors, RAPP learns how a piece of equipment normally behaves and detects the deviation that leads to failure. On the farm, the “equipment” is the field, the animal and the machine.", "p", "lead")}
  </div>
</div>
<section>
  <div class="wrap">
    <div class="head">{pg.t("Assinatura de condição", "Firma de condición", "Condition signature", "span", "eyebrow")}{pg.t("Entradas, basal, desvio, ação.", "Entradas, basal, desvío, acción.", "Inputs, baseline, deviation, action.", "h2")}</div>
    <div class="tablewrap"><table class="hft"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>
    {explainer(pg, "tec", ("O que é a assinatura de condição", "Qué es la firma de condición", "What a condition signature is"), "≈ 75 s", [
        ("Cada talhão, animal e máquina tem um jeito normal de funcionar", "Cada lote, animal y máquina tiene una forma normal de funcionar", "Every field, animal and machine has a normal way of behaving"),
        ("O RAPP desenha essa faixa normal a partir das medições", "El RAPP dibuja ese rango normal a partir de las mediciones", "RAPP draws that normal band from the measurements"),
        ("Um desvio pequeno, que o olho não vê, sai da faixa", "Un desvío pequeño, que el ojo no ve, sale del rango", "A small deviation the eye cannot see leaves the band"),
        ("O alerta chega antes do sintoma, com a ação sugerida", "La alerta llega antes del síntoma, con la acción sugerida", "The alert arrives before the symptom, with the suggested action")])}
  </div>
</section>
<section class="soft">
  <div class="wrap split">
    <div class="duo"><img src="img/f/centro-2.webp" alt="Central de monitoramento Help Farm" loading="lazy"><img src="img/f/tecnicos.webp" alt="" loading="lazy"></div>
    <div>
      {pg.t("Central de monitoramento", "Central de monitoreo", "Monitoring centre", "span", "eyebrow")}
      {pg.t("Técnicos recebem os sinais da terra, dia e noite.", "Técnicos reciben las señales de la tierra, día y noche.", "Technicians receive the signals of the land, day and night.", "h2")}
      {pg.t("No backoffice, especialistas acompanham os alertas do RAPP e falam com a dupla da unidade móvel e com o produtor. Quem decide é sempre uma pessoa: o RAPP recomenda, a central confirma e aciona quem precisa agir.", "En el backoffice, especialistas siguen las alertas del RAPP y hablan con la dupla de la unidad móvil y con el productor. Quien decide es siempre una persona: el RAPP recomienda, la central confirma y activa a quien debe actuar.", "In the back office, specialists follow RAPP alerts and talk to the mobile-unit pair and the farmer. A person always decides: RAPP recommends, the centre confirms and calls whoever needs to act.", "p", "muted", attrs=' style="margin-top:14px"')}
    </div>
  </div>
</section>
<section class="dark">
  <div class="wrap">
    <div class="head">{pg.t("Arquitetura de campo", "Arquitectura de campo", "Field architecture", "span", "eyebrow")}{pg.t("O alerta sai mesmo sem internet.", "La alerta sale incluso sin internet.", "Alerts go out even without internet.", "h2")}</div>
    <div class="g g4 steps">
      <div class="step">{pg.t("Sensores", "Sensores", "Sensors", "h3")}{pg.t("Sondas, estações, bolus e sensores de vibração enviam dados por rádio de longo alcance (LoRaWAN), sem mensalidade de operadora.", "Sondas, estaciones, bolos y sensores de vibración envían datos por radio de largo alcance (LoRaWAN), sin abono de operadora.", "Probes, stations, boluses and vibration sensors send data over long-range radio (LoRaWAN), with no carrier fees.", "p")}</div>
      <div class="step">{pg.t("Gateway na fazenda", "Gateway en el establecimiento", "Farm gateway", "h3")}{pg.t("Um computador de borda roda o RAPP no próprio local e dispara o alerta na hora.", "Una computadora de borde corre el RAPP en el lugar y dispara la alerta en el momento.", "An edge computer runs RAPP on site and fires the alert immediately.", "p")}</div>
      <div class="step">{pg.t("Satélite e nuvem", "Satélite y nube", "Satellite and cloud", "h3")}{pg.t("Antena satelital ou 4G sobe os dados para a nuvem, onde o modelo aprende com todas as fazendas.", "Antena satelital o 4G sube los datos a la nube, donde el modelo aprende con todos los establecimientos.", "Satellite antenna or 4G sends data to the cloud, where the model learns from every farm.", "p")}</div>
      <div class="step">{pg.t("Quem age", "Quién actúa", "Who acts", "h3")}{pg.t("Produtor, técnico da cooperativa, veterinário, fornecedor e seguradora recebem o que lhes cabe.", "Productor, técnico de la cooperativa, veterinario, proveedor y aseguradora reciben lo que les corresponde.", "Producer, cooperative technician, vet, supplier and insurer each get what concerns them.", "p")}</div>
    </div>
    {pg.t("Os dados pertencem ao produtor. A Help Farm usa dados agregados e anônimos para melhorar o modelo, com isso escrito em contrato.", "Los datos pertenecen al productor. Help Farm usa datos agregados y anónimos para mejorar el modelo, con eso escrito en contrato.", "The data belongs to the producer. Help Farm uses aggregated, anonymous data to improve the model, as stated in the contract.", "p", "note darknote")}
  </div>
</section>
'''
    shell(pg, "tecnologia.html", title, body, "Motor RAPP de assinatura de condição aplicado a solo, lavoura, clima, gado e máquinas.")


def investidores():
    pg = Page()
    title = pg.title("Investidores — Help Farm", "Inversionistas — Help Farm", "Investors — Help Farm")
    layers = [
        (("Implantação", "Taxa única por fazenda: medição completa pela unidade móvel, instalação dos sensores e calibração da assinatura."), ("Implantación", "Tasa única por establecimiento: medición completa por la unidad móvil, instalación de sensores y calibración de la firma."), ("Onboarding", "One-off fee per farm: full measurement by the mobile unit, sensor installation and signature calibration.")),
        (("Assinatura por unidade", "Mensal por cabeça, por vaca, por hectare ou por máquina, com o equipamento em comodato e contrato de 36 meses."), ("Suscripción por unidad", "Mensual por cabeza, por vaca, por hectárea o por máquina, con el equipo en comodato y contrato de 36 meses."), ("Per-unit subscription", "Monthly per head, per cow, per hectare or per machine, with equipment on loan and a 36-month contract.")),
        (("Cooperativas", "Licença anual para cooperativas, laticínios e tradings levarem a Help Farm aos associados."), ("Cooperativas", "Licencia anual para cooperativas, lácteas y tradings llevar Help Farm a sus asociados."), ("Cooperatives", "Annual licence for cooperatives, dairies and traders to bring Help Farm to their members.")),
        (("Temporada de campo", "A unidade móvel fica na fazenda durante plantio, colheita ou estação de monta, com a dupla de profissionais a bordo."), ("Temporada de campo", "La unidad móvil se queda en el establecimiento durante siembra, cosecha o servicio, con la dupla de profesionales a bordo."), ("Field season", "The mobile unit stays on the farm through planting, harvest or breeding season, with the two professionals on board.")),
        (("Risco para bancos e seguradoras", "Índice de condição da fazenda e do rebanho para crédito rural e seguro agrícola."), ("Riesgo para bancos y aseguradoras", "Índice de condición del establecimiento y del rodeo para crédito rural y seguro agrícola."), ("Risk for banks and insurers", "Farm and herd condition index for rural credit and crop insurance.")),
    ]
    body = f'''
<div class="hero sub hfsub">
  <div class="wrap">
    <p class="crumb"><a href="./">Help Farm</a> / {pg.t("Investidores", "Inversionistas", "Investors")}</p>
    {pg.t("Um motor já desenhado, um mercado que já paga por animal e por hectare.", "Un motor ya diseñado, un mercado que ya paga por animal y por hectárea.", "An engine already designed, a market that already pays per animal and per hectare.", "h1")}
    {pg.t("A Help Farm roda sobre o motor RAPP, desenvolvido pela Moulin para manutenção preditiva industrial. O primeiro mercado é o Paraguai, onde o grupo já tem empresa e operação; o Brasil vem em seguida, para escala.", "Help Farm funciona con el motor RAPP, desarrollado por Moulin para mantenimiento predictivo industrial. El primer mercado es Paraguay, donde el grupo ya tiene empresa y operación; Brasil viene después, para escala.", "Help Farm runs on the RAPP engine, developed by Moulin for industrial predictive maintenance. The first market is Paraguay, where the group already has a company and operations; Brazil follows for scale.", "p", "lead")}
  </div>
</div>
<section>
  <div class="wrap">
    <div class="head">{pg.t("Mercado", "Mercado", "Market", "span", "eyebrow")}{pg.t("Quem já paga por monitoramento hoje.", "Quién ya paga por monitoreo hoy.", "Who already pays for monitoring today.", "h2")}</div>
    <div class="kpis k4">
      <div class="kpi"><b>US$ 4–10</b>{pg.t("por vaca/mês pagos hoje por colares e bolus de monitoramento (Brasil, Nova Zelândia, Europa)", "por vaca/mes pagados hoy por collares y bolos de monitoreo (Brasil, Nueva Zelanda, Europa)", "per cow/month paid today for monitoring collars and boluses (Brazil, New Zealand, Europe)", "span")}</div>
      <div class="kpi"><b>US$ 5/acre</b>{pg.t("cobrados pela maior fabricante de máquinas por uma única função de IA na lavoura", "cobrados por el mayor fabricante de máquinas por una sola función de IA en el cultivo", "charged by the largest machinery maker for a single AI crop feature", "span")}</div>
      <div class="kpi"><b>&lt; US$ 1</b>{pg.t("por brinco eletrônico comprado por governos — o sensor virou commodity, o alerta não", "por caravana electrónica comprada por gobiernos — el sensor es commodity, la alerta no", "per electronic ear tag bought by governments — sensors are a commodity, alerts are not", "span")}</div>
      <div class="kpi"><b>16</b>{pg.t("países pesquisados, com contratos públicos e preços privados conferidos", "países investigados, con contratos públicos y precios privados verificados", "countries researched, with public contracts and private prices checked", "span")}</div>
    </div>
  </div>
</section>
<section class="soft">
  <div class="wrap">
    <div class="head">{pg.t("Modelo de receita", "Modelo de ingresos", "Revenue model", "span", "eyebrow")}{pg.t("Receita recorrente por unidade monitorada.", "Ingreso recurrente por unidad monitoreada.", "Recurring revenue per monitored unit.", "h2")}
    {pg.t("O modelo segue o que deu certo no setor — cobrar por animal, hectare ou máquina, com o equipamento dentro da assinatura — e evita o que quebrou empresas: áreas gratuitas em massa e venda de dado genérico.", "El modelo sigue lo que funcionó en el sector — cobrar por animal, hectárea o máquina, con el equipo dentro de la suscripción — y evita lo que quebró empresas: áreas gratuitas masivas y venta de datos genéricos.", "The model follows what worked in the sector — charging per animal, hectare or machine, with equipment inside the subscription — and avoids what broke companies: mass free acreage and selling generic data.", "p", "muted")}</div>
    <div class="g g5">{"".join(card(pg, a, b, c) for a, b, c in layers)}</div>
  </div>
</section>
<section>
  <div class="wrap">
    {explainer(pg, "inv", ("Como a Help Farm gera receita", "Cómo genera ingresos Help Farm", "How Help Farm makes money"), "≈ 90 s", [
        ("O produtor paga a implantação e a assinatura por hectare, cabeça ou máquina", "El productor paga la implantación y la suscripción por hectárea, cabeza o máquina", "The farmer pays onboarding and a subscription per hectare, head or machine"),
        ("Ao redor da fazenda vivem 12 entidades que dependem da saúde dela", "Alrededor del establecimiento viven 12 entidades que dependen de su salud", "Around the farm live 12 entities that depend on its health"),
        ("Bancos, seguradoras e compradores pagam por dado confiável da fazenda", "Bancos, aseguradoras y compradores pagan por datos confiables del establecimiento", "Banks, insurers and buyers pay for reliable farm data"),
        ("A certificação de origem gera receita por lote e por tonelada", "La certificación de origen genera ingresos por lote y por tonelada", "Origin certification earns revenue per lot and per tonne")])}
  </div>
</section>
<section class="invarea">
  <div class="wrap split">
    <div>
      {pg.t("Área do investidor", "Área del inversionista", "Investor area", "span", "eyebrow")}
      {pg.t("O material completo da rodada, com acesso por código.", "El material completo de la ronda, con acceso por código.", "The full round material, with code access.", "h2")}
      {pg.t("Pesquisa de mercado em 16 países, modelo de rentabilidade por abrangência, kit da unidade móvel, o filme e os vídeos explicativos. O acesso é restrito a quem tem interesse em investir.", "Investigación de mercado en 16 países, modelo de rentabilidad por alcance, kit de la unidad móvil, la película y los videos explicativos. El acceso está restringido a quienes tienen interés en invertir.", "Market research across 16 countries, profitability model by scope, mobile-unit kit, the film and the explainer videos. Access is restricted to those interested in investing.", "p", "muted", attrs=' style="margin-top:14px"')}
      <div class="cta"><a class="btn primary" href="/helpfarm/area-investidor/">{pg.t("Entrar com código", "Entrar con código", "Enter with code")}</a><a class="btn dark" href="/helpfarm/area-investidor/solicitar">{pg.t("Solicitar acesso", "Solicitar acceso", "Request access")}</a></div>
    </div>
    <img class="invimg" src="img/f/assinatura.webp" alt="" loading="lazy">
  </div>
</section>
<section class="dark">
  <div class="wrap">
    <div class="head">{pg.t("Sequência de entrada", "Secuencia de entrada", "Go-to-market sequence", "span", "eyebrow")}{pg.t("Paraguai prova, Brasil escala.", "Paraguay prueba, Brasil escala.", "Paraguay proves, Brazil scales.", "h2")}</div>
    <div class="g g3 steps">
      <div class="step">{pg.t("Piloto no Paraguai", "Piloto en Paraguay", "Pilot in Paraguay", "h3")}{pg.t("Cinco fazendas com a unidade móvel e uma cooperativa parceira: provar um alerta antecipado documentado em cada frente.", "Cinco establecimientos con la unidad móvil y una cooperativa socia: probar una alerta anticipada documentada en cada frente.", "Five farms with the mobile unit and a partner cooperative: prove one documented early alert on each front.", "p")}</div>
      <div class="step">{pg.t("Brasil e Cone Sul", "Brasil y Cono Sur", "Brazil and Southern Cone", "h3")}{pg.t("Leite e gado de corte primeiro, com a rastreabilidade obrigatória; depois grãos. Seguradoras e bancos entram com o produto de risco.", "Leche y ganado de carne primero, con la trazabilidad obligatoria; después granos. Aseguradoras y bancos entran con el producto de riesgo.", "Dairy and beef first, riding mandatory traceability; then grains. Insurers and banks join with the risk product.", "p")}</div>
      <div class="step">{pg.t("Mercados maduros", "Mercados maduros", "Mature markets", "h3")}{pg.t("Estados Unidos, Oceania e Europa com parceiro local, como camada preditiva sobre dados de equipamentos já instalados.", "Estados Unidos, Oceanía y Europa con socio local, como capa predictiva sobre datos de equipos ya instalados.", "United States, Oceania and Europe with a local partner, as a predictive layer over data from equipment already in place.", "p")}</div>
    </div>
    <div class="cta"><a class="btn primary" href="/helpfarm/area-investidor/solicitar">{pg.t("Pedir o material completo", "Pedir el material completo", "Request the full material")}</a></div>
    {pg.t("Pesquisa de mercado em 16 países, modelo por abrangência e cenários de rodada disponíveis mediante solicitação. Números de preço e custo da Help Farm são premissas em validação.", "Investigación de mercado en 16 países, modelo por alcance y escenarios de ronda disponibles a pedido. Precios y costos de Help Farm son supuestos en validación.", "Market research across 16 countries, scope model and round scenarios available on request. Help Farm price and cost figures are assumptions under validation.", "p", "note darknote")}
  </div>
</section>
'''
    shell(pg, "investidores.html", title, body, "Help Farm para investidores: mercado, modelo de receita e sequência de entrada.")


from hf_cert import cert_band, certificacao, lote_demo  # noqa: E402
from hf_media import film, explainer  # noqa: E402

if __name__ == "__main__":
    home(); movel(); tecnologia(); investidores(); certificacao(); lote_demo()
    print("ok")
