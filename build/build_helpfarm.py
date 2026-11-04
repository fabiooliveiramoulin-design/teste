# Gera o site Help Farm em /helpfarm (PT no HTML + ES/EN embutidos para a troca de idioma).
# Uso: python3 build/build_helpfarm.py   (a partir da raiz do repositório)
# Reaproveita assets/site.css e assets/site.js do Help Cure; ajustes próprios em helpfarm/assets/hf.css.
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
       ("celula.html", "Célula", "Célula", "Field cell"),
       ("tecnologia.html", "Tecnologia", "Tecnología", "Technology"),
       ("investidores.html", "Investidores", "Inversionistas", "Investors")]

LOGO = '''<svg class="hf-mark" viewBox="0 0 40 40" aria-hidden="true"><rect x="1" y="1" width="38" height="38" rx="10" fill="#0E4A3F" stroke="#17B877" stroke-opacity=".35"/>
<path d="M7 29c6-3 20-3 26 0M7 24c6-3 20-3 26 0" fill="none" stroke="#17B877" stroke-width="2" stroke-linecap="round" opacity=".55"/>
<path d="M8 19l6-1 4-6 4 9 4-4 6 0" fill="none" stroke="#3EE39A" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="32" cy="17" r="2.6" fill="#FFB500"/></svg>'''


def shell(pg, path, title, body, desc):
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Lexend:wght@300;400;500;600&display=swap">
<link rel="stylesheet" href="../assets/site.css?v=8">
<link rel="stylesheet" href="assets/hf.css?v=1">
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
      <a href="celula.html">{pg.t("Célula de campo", "Célula de campo", "Field cell")}</a>
      <a href="tecnologia.html">{pg.t("Motor RAPP e o que medimos", "Motor RAPP y qué medimos", "RAPP engine and what we measure")}</a>
      <a href="investidores.html">{pg.t("Investidores", "Inversionistas", "Investors")}</a></div>
    <div><h4>{pg.t("Grupo", "Grupo", "Group")}</h4>
      <a href="../">{pg.t("Help Cure — saúde", "Help Cure — salud", "Help Cure — health")}</a></div>
    <div class="legal">© 2026 Help Farm · {pg.t("Projeto em fase de desenvolvimento. Ilustrações esquemáticas; configuração final da unidade móvel, da célula e dos instrumentos a definir.", "Proyecto en fase de desarrollo. Ilustraciones esquemáticas; configuración final de la unidad móvil, la célula y los instrumentos a definir.", "Project in development. Schematic illustrations; final configuration of the mobile unit, the cell and the instruments to be defined.")}</div>
  </div>
</footer>
<script>window.HC_T={json.dumps({"es": pg.es, "en": pg.en}, ensure_ascii=False)};</script>
<script src="../assets/site.js?v=4"></script>
</body>
</html>
'''
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, path), "w", encoding="utf-8").write(head + body + foot)


def feats(pg, items):
    return '<ul class="feat">' + "".join('<li>%s</li>' % pg.t("<b>%s</b> — %s" % (a[0], a[1]), "<b>%s</b> — %s" % (b[0], b[1]), "<b>%s</b> — %s" % (c[0], c[1]), "span", raw=True) for a, b, c in items) + '</ul>'


def card(pg, a, b, c, href=None, more=None):
    inner = '<div class="in">%s%s%s</div>' % (pg.t(a[0], b[0], c[0], "h3"), pg.t(a[1], b[1], c[1], "p"),
                                              ('<span class="more">%s →</span>' % pg.t(*more)) if more else "")
    return ('<a class="card" href="%s">%s</a>' % (href, inner)) if href else '<div class="card">%s</div>' % inner


def stl(pg, x, y, pt, es, en, cls="lb", anchor="start"):
    return pg.t(pt, es, en, "text", attrs=' x="%s" y="%s" class="%s" text-anchor="%s"' % (x, y, cls, anchor))


# ------------------------------------------------------------------ ilustrações
def svg_signature(pg):
    return f'''<svg class="sig" viewBox="0 0 560 300" role="img" aria-label="Assinatura basal e desvio">
<defs><linearGradient id="band" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#17B877" stop-opacity=".22"/><stop offset="1" stop-color="#17B877" stop-opacity=".05"/></linearGradient></defs>
<rect x="0" y="0" width="560" height="300" rx="20" fill="#06201C"/>
<g stroke="#1F4A42" stroke-width="1">{"".join('<line x1="40" x2="530" y1="%d" y2="%d"/>' % (y, y) for y in (60, 110, 160, 210, 250))}</g>
<path d="M40 150 C110 120 150 175 220 150 S330 120 380 148" fill="none" stroke="url(#band)" stroke-width="46" stroke-linecap="round"/>
<path d="M40 150 C110 120 150 175 220 150 S330 120 380 148" fill="none" stroke="#3EE39A" stroke-width="3"/>
<path d="M380 148 C420 160 445 190 470 215 S510 245 528 252" fill="none" stroke="#FFB500" stroke-width="3" stroke-dasharray="7 5"/>
<circle cx="430" cy="172" r="7" fill="#FFB500"/><circle cx="430" cy="172" r="15" fill="none" stroke="#FFB500" stroke-opacity=".5"/>
{stl(pg, 46, 40, "Assinatura basal do talhão, do animal ou da máquina", "Firma basal del lote, del animal o de la máquina", "Baseline signature of the field, animal or machine", "lb lw")}
{stl(pg, 412, 200, "desvio detectado", "desvío detectado", "deviation detected", "lb lo", "end")}
{stl(pg, 528, 280, "problema (se nada for feito)", "problema (si no se actúa)", "failure (if nothing is done)", "lb lm", "end")}
{stl(pg, 46, 280, "faixa normal aprendida pelo RAPP", "rango normal aprendido por el RAPP", "normal range learned by RAPP", "lb lg")}
</svg>'''


def svg_movel(pg):
    # motorhome 4x4 em corte lateral
    return f'''<svg class="draw" viewBox="0 0 1000 430" role="img" aria-label="Unidade móvel Help Farm em corte">
<rect width="1000" height="430" rx="22" fill="#F1F6F4"/>
<line x1="20" x2="980" y1="372" y2="372" stroke="#B9CBC5" stroke-width="2"/>
<!-- painel solar e antena -->
<g>{"".join('<rect x="%d" y="88" width="88" height="16" rx="2" fill="#123B6B" stroke="#0B2747"/>' % x for x in (262, 356, 450, 544, 638))}
{"".join('<line x1="%d" x2="%d" y1="88" y2="104" stroke="#4E7BB0" stroke-width="1"/>' % (x, x) for x in range(284, 726, 22))}</g>
<rect x="752" y="78" width="54" height="10" rx="3" fill="#E9EEF0" stroke="#7C8E89"/><rect x="775" y="88" width="8" height="18" fill="#7C8E89"/>
<!-- cabine -->
<path d="M60 330 L60 220 Q62 176 110 170 L205 166 L205 330 Z" fill="#0B3B36"/>
<path d="M78 222 Q82 190 116 186 L190 184 L190 232 L78 236 Z" fill="#9FD9C6" opacity=".85"/>
<!-- carroceria em corte -->
<rect x="205" y="106" width="620" height="226" rx="14" fill="#FFFFFF" stroke="#0B3B36" stroke-width="4"/>
<line x1="440" x2="440" y1="110" y2="330" stroke="#0B3B36" stroke-width="2"/>
<line x1="540" x2="540" y1="110" y2="330" stroke="#0B3B36" stroke-width="2"/>
<!-- bancada de instrumentos e drones -->
<rect x="222" y="246" width="200" height="12" fill="#465A55"/>
<rect x="232" y="210" width="44" height="34" rx="4" fill="#17B877"/><rect x="284" y="214" width="36" height="30" rx="4" fill="#FFB500"/><rect x="328" y="206" width="30" height="38" rx="4" fill="#465A55"/><rect x="366" y="216" width="46" height="28" rx="4" fill="#17B877" opacity=".7"/>
<rect x="232" y="130" width="180" height="56" rx="6" fill="#E9F1EE" stroke="#465A55"/>
<g fill="#0B3B36"><circle cx="262" cy="158" r="9"/><circle cx="300" cy="158" r="9"/><rect x="266" y="154" width="30" height="8"/>
<circle cx="350" cy="158" r="9"/><circle cx="388" cy="158" r="9"/><rect x="354" y="154" width="30" height="8"/></g>
<rect x="232" y="266" width="180" height="56" rx="6" fill="#E9F1EE" stroke="#465A55"/>
<!-- banheiro -->
<rect x="456" y="226" width="34" height="40" rx="8" fill="#D3DFDB" stroke="#465A55"/><rect x="500" y="130" width="28" height="180" rx="4" fill="#DCEEF7" stroke="#465A55"/>
<path d="M514 140 l0 14" stroke="#465A55" stroke-width="3"/>
<!-- dormitório com beliche -->
<rect x="556" y="190" width="250" height="14" rx="3" fill="#0B3B36"/><rect x="556" y="292" width="250" height="14" rx="3" fill="#0B3B36"/>
<rect x="562" y="174" width="238" height="16" rx="6" fill="#9FD9C6"/><rect x="562" y="276" width="238" height="16" rx="6" fill="#9FD9C6"/>
<rect x="600" y="122" width="70" height="40" rx="6" fill="#DCEEF7" stroke="#465A55"/>
<!-- rack traseiro com 2 motos trail -->
<rect x="826" y="300" width="138" height="9" rx="2" fill="#465A55"/><rect x="826" y="262" width="8" height="46" fill="#465A55"/>
<g opacity=".45" transform="translate(12,-10)">
<g fill="none" stroke="#0E1F1C" stroke-width="7"><circle cx="852" cy="283" r="15"/><circle cx="936" cy="283" r="15"/></g>
<path d="M852 283 L872 262 L912 262 L936 283" fill="none" stroke="#465A55" stroke-width="5"/>
</g>
<g fill="none" stroke="#0E1F1C" stroke-width="7"><circle cx="852" cy="283" r="15"/><circle cx="936" cy="283" r="15"/></g>
<rect x="872" y="266" width="26" height="18" rx="3" fill="#465A55"/>
<path d="M852 283 L874 262 L906 258 L936 283" fill="none" stroke="#0B3B36" stroke-width="5" stroke-linejoin="round"/>
<path d="M878 258 Q890 246 908 250 L914 258 Z" fill="#FFB500"/>
<path d="M862 256 L898 254" stroke="#0E1F1C" stroke-width="6" stroke-linecap="round"/>
<path d="M922 262 L914 240 M908 238 L924 240" stroke="#0E1F1C" stroke-width="4" stroke-linecap="round"/>
<path d="M914 240 L936 283" stroke="#7C8E89" stroke-width="4"/>
<!-- rodas -->
<g fill="#0E1F1C"><circle cx="140" cy="340" r="36"/><circle cx="640" cy="340" r="36"/><circle cx="742" cy="340" r="36"/></g>
<g fill="#B9CBC5"><circle cx="140" cy="340" r="13"/><circle cx="640" cy="340" r="13"/><circle cx="742" cy="340" r="13"/></g>
<!-- rótulos -->
<line x1="306" y1="86" x2="306" y2="46" stroke="#17B877" stroke-width="1.5"/>
{stl(pg, 262, 38, "Painel solar + baterias de lítio", "Panel solar + baterías de litio", "Solar panel + lithium batteries", "lb")}
{stl(pg, 806, 66, "Antena satelital (internet em qualquer lugar)", "Antena satelital (internet en cualquier lugar)", "Satellite antenna (internet anywhere)", "lb", "end")}
{stl(pg, 236, 124, "Drones em case", "Drones en estuche", "Drones in cases", "ls")}
{stl(pg, 236, 202, "Instrumentos portáteis", "Instrumentos portátiles", "Portable instruments", "ls")}
{stl(pg, 240, 300, "Sensores para instalar", "Sensores a instalar", "Sensors to install", "ls")}
{stl(pg, 490, 324, "Banheiro", "Baño", "Bathroom", "ls", "middle")}
{stl(pg, 680, 236, "Dormitório com beliche (2 profissionais)", "Dormitorio con litera (2 profesionales)", "Bunk-bed sleeping area (2 staff)", "ls", "middle")}
{stl(pg, 895, 226, "2 motos trail", "2 motos trail", "2 trail bikes", "lb", "middle")}
{stl(pg, 133, 404, "Chassi 4x4", "Chasis 4x4", "4x4 chassis", "lb", "middle")}
{stl(pg, 690, 404, "Tração e altura para estrada de terra", "Tracción y altura para camino de tierra", "Traction and clearance for dirt roads", "lb", "middle")}
</svg>'''


def svg_celula(pg):
    # contêiner 12 m em corte lateral
    cor = "".join('<line x1="%d" x2="%d" y1="116" y2="300" stroke="#0B3B36" stroke-opacity=".08" stroke-width="6"/>' % (x, x) for x in range(70, 960, 26))
    return f'''<svg class="draw" viewBox="0 0 1000 400" role="img" aria-label="Célula de campo Help Farm em corte">
<rect width="1000" height="400" rx="22" fill="#F1F6F4"/>
<line x1="20" x2="980" y1="338" y2="338" stroke="#B9CBC5" stroke-width="2"/>
<g>{"".join('<rect x="%d" y="96" width="96" height="14" rx="2" fill="#123B6B" stroke="#0B2747"/>' % x for x in (90, 192, 294, 396, 498, 600))}</g>
<rect x="760" y="84" width="54" height="10" rx="3" fill="#E9EEF0" stroke="#7C8E89"/><rect x="783" y="94" width="8" height="18" fill="#7C8E89"/>
<rect x="50" y="112" width="900" height="192" rx="6" fill="#FFFFFF" stroke="#0B3B36" stroke-width="4"/>
<g stroke="#0B3B36" stroke-width="2">{"".join('<line x1="%d" x2="%d" y1="114" y2="302"/>' % (x, x) for x in (270, 360, 480, 740))}</g>
<!-- dormitório: 2 beliches -->
<rect x="66" y="196" width="190" height="10" fill="#0B3B36"/><rect x="66" y="282" width="190" height="10" fill="#0B3B36"/>
<rect x="70" y="182" width="182" height="14" rx="5" fill="#9FD9C6"/><rect x="70" y="268" width="182" height="14" rx="5" fill="#9FD9C6"/>
<rect x="110" y="146" width="90" height="36" rx="5" fill="#DCEEF7" stroke="#465A55"/>
<!-- banheiro -->
<rect x="282" y="248" width="30" height="36" rx="8" fill="#D3DFDB" stroke="#465A55"/><rect x="322" y="134" width="26" height="150" rx="4" fill="#DCEEF7" stroke="#465A55"/>
<!-- cozinha -->
<rect x="372" y="230" width="96" height="54" fill="#E9F1EE" stroke="#465A55"/><rect x="384" y="146" width="70" height="36" rx="5" fill="#DCEEF7" stroke="#465A55"/>
<!-- laboratório de campo -->
<rect x="494" y="238" width="232" height="12" fill="#465A55"/>
<rect x="504" y="204" width="40" height="32" rx="4" fill="#17B877"/><rect x="552" y="208" width="32" height="28" rx="4" fill="#FFB500"/><rect x="592" y="198" width="28" height="38" rx="4" fill="#465A55"/><rect x="628" y="210" width="44" height="26" rx="4" fill="#17B877" opacity=".7"/>
<rect x="680" y="196" width="40" height="88" rx="4" fill="#E9F1EE" stroke="#465A55"/>
<rect x="520" y="146" width="90" height="36" rx="5" fill="#DCEEF7" stroke="#465A55"/><rect x="626" y="146" width="90" height="36" rx="5" fill="#DCEEF7" stroke="#465A55"/>
<!-- escritório / central -->
<rect x="760" y="232" width="170" height="12" fill="#465A55"/><rect x="782" y="196" width="54" height="34" rx="3" fill="#0B3B36"/><rect x="848" y="196" width="54" height="34" rx="3" fill="#0B3B36"/>
<path d="M792 222 l10 -8 8 6 10 -12 8 6" fill="none" stroke="#3EE39A" stroke-width="2"/>
<rect x="792" y="146" width="110" height="36" rx="5" fill="#DCEEF7" stroke="#465A55"/>
<!-- sapatas -->
<g fill="#7C8E89">{"".join('<rect x="%d" y="304" width="34" height="34"/>' % x for x in (60, 330, 620, 906))}</g>
<!-- rótulos -->
{stl(pg, 395, 84, "Painel solar + baterias", "Panel solar + baterías", "Solar panel + batteries", "lb", "middle")}
{stl(pg, 787, 72, "Antena satelital", "Antena satelital", "Satellite antenna", "lb", "middle")}
{stl(pg, 160, 134, "Dormitório (2 beliches)", "Dormitorio (2 literas)", "Sleeping area (2 bunk beds)", "ls", "middle")}
{stl(pg, 315, 134, "Banheiro", "Baño", "Bathroom", "ls", "middle")}
{stl(pg, 420, 134, "Cozinha", "Cocina", "Kitchen", "ls", "middle")}
{stl(pg, 610, 134, "Laboratório de campo", "Laboratorio de campo", "Field lab", "ls", "middle")}
{stl(pg, 845, 134, "Escritório e central", "Oficina y central", "Office and control desk", "ls", "middle")}
{stl(pg, 500, 380, "Contêiner de 12 m (40 pés) com janelas, transportado por caminhão e implantado sobre sapatas", "Contenedor de 12 m (40 pies) con ventanas, transportado en camión e instalado sobre zapatas", "12 m (40 ft) container with windows, trucked in and set on footings", "lb", "middle")}
</svg>'''


# ------------------------------------------------------------------ páginas
def home():
    pg = Page()
    title = pg.title("Help Farm — a fazenda que avisa antes do problema",
                     "Help Farm — el establecimiento que avisa antes del problema",
                     "Help Farm — the farm that warns before the problem")
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
    body = f'''
<div class="hero hv">
  <div class="wrap">
    <div>
      {pg.t("Help Farm · motor RAPP", "Help Farm · motor RAPP", "Help Farm · RAPP engine", "span", "eyebrow")}
      {pg.t("A fazenda que <em>avisa antes</em> do problema.", "El establecimiento que <em>avisa antes</em> del problema.", "The farm that <em>warns before</em> the problem.", "h1", raw=True)}
      {pg.t("Medimos solo, lavoura, clima, gado e máquinas, aprendemos a assinatura normal de cada um e disparamos a ação antes da perda — a mesma inteligência de manutenção preditiva usada em turbinas de plataforma de petróleo, agora no campo.", "Medimos suelo, cultivo, clima, ganado y máquinas, aprendemos la firma normal de cada uno y disparamos la acción antes de la pérdida — la misma inteligencia de mantenimiento predictivo usada en turbinas de plataformas petroleras, ahora en el campo.", "We measure soil, crops, weather, livestock and machines, learn each one’s normal signature and trigger action before the loss — the same predictive-maintenance intelligence used on offshore oil turbines, now in the field.", "p", "lead")}
      <div class="cta"><a class="btn primary" href="unidade-movel.html">{pg.t("Conheça a unidade móvel", "Conozca la unidad móvil", "See the mobile unit")}</a><a class="btn ghost" href="investidores.html">{pg.t("Para investidores", "Para inversionistas", "For investors")}</a></div>
    </div>
    <div class="hv-media sigbox">{svg_signature(pg)}</div>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="head">{pg.t("O que medimos", "Qué medimos", "What we measure", "span", "eyebrow")}{pg.t("Cinco frentes, um só histórico da fazenda.", "Cinco frentes, un solo historial del establecimiento.", "Five fronts, one farm history.", "h2")}
    {pg.t("Cada medição entra na mesma linha do tempo. É o cruzamento entre elas — chuva com solo, solo com planta, calor com rebanho, máquina com safra — que permite prever.", "Cada medición entra en la misma línea de tiempo. Es el cruce entre ellas — lluvia con suelo, suelo con planta, calor con rodeo, máquina con cosecha — lo que permite predecir.", "Every measurement goes on the same timeline. Crossing them — rain with soil, soil with plants, heat with herd, machines with harvest — is what makes prediction possible.", "p", "muted")}</div>
    <div class="g g5">{"".join(card(pg, a, b, c) for a, b, c in domains)}</div>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <div class="head">{pg.t("Como funciona", "Cómo funciona", "How it works", "span", "eyebrow")}{pg.t("Do diagnóstico ao alerta, no mesmo método do Help Cure.", "Del diagnóstico a la alerta, con el mismo método de Help Cure.", "From diagnosis to alert, with the same method as Help Cure.", "h2")}</div>
    <div class="g g4 steps">{"".join('<div class="step">%s%s</div>' % (pg.t(a[0], b[0], c[0], "h3"), pg.t(a[1], b[1], c[1], "p")) for a, b, c in steps)}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head">{pg.t("Estrutura de campo", "Estructura de campo", "Field structure", "span", "eyebrow")}{pg.t("Duas formas de levar os profissionais até a fazenda.", "Dos formas de llevar a los profesionales hasta el establecimiento.", "Two ways to bring the professionals to the farm.", "h2")}</div>
    <div class="g g2">
      <a class="card" href="unidade-movel.html"><div class="pic">{svg_movel(pg)}</div><div class="in">{pg.t("Unidade móvel de medição", "Unidad móvil de medición", "Mobile measuring unit", "h3")}{pg.t("Um motorhome 4x4 com instrumentos, drones, dormitório, banheiro, energia solar, antena satelital e duas motos trail. Vai, mede, instala os sensores e segue para a próxima fazenda.", "Un motorhome 4x4 con instrumentos, drones, dormitorio, baño, energía solar, antena satelital y dos motos trail. Va, mide, instala los sensores y sigue al próximo establecimiento.", "A 4x4 motorhome with instruments, drones, sleeping area, bathroom, solar power, satellite antenna and two trail bikes. It goes, measures, installs the sensors and moves on to the next farm.", "p")}<span class="more">{pg.t("Ver a unidade", "Ver la unidad", "See the unit")} →</span></div></a>
      <a class="card" href="celula.html"><div class="pic">{svg_celula(pg)}</div><div class="in">{pg.t("Célula de campo", "Célula de campo", "Field cell", "h3")}{pg.t("Um contêiner de 12 m com dormitório, banheiro, janelas e laboratório, implantado nas fazendas e cooperativas que precisam de profissionais residentes.", "Un contenedor de 12 m con dormitorio, baño, ventanas y laboratorio, instalado en los establecimientos y cooperativas que necesitan profesionales residentes.", "A 12 m container with sleeping area, bathroom, windows and lab, set up on farms and cooperatives that need resident professionals.", "p")}<span class="more">{pg.t("Ver a célula", "Ver la célula", "See the cell")} →</span></div></a>
    </div>
  </div>
</section>

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
    res = [
        (("Dois profissionais instalados", "Um agrônomo e um técnico (ou veterinário) ficam na fazenda durante a campanha de medição, sem depender de hotel na cidade."), ("Dos profesionales instalados", "Un agrónomo y un técnico (o veterinario) se quedan en el establecimiento durante la campaña de medición, sin depender de hotel en la ciudad."), ("Two professionals on site", "An agronomist and a technician (or vet) stay on the farm during the measuring campaign, with no need for a hotel in town.")),
        (("Dormitório e banheiro", "Beliche para dois, banheiro com chuveiro, caixa d’água e climatização."), ("Dormitorio y baño", "Litera para dos, baño con ducha, tanque de agua y climatización."), ("Sleeping area and bathroom", "Bunk bed for two, bathroom with shower, water tank and climate control.")),
        (("Energia própria", "Painel solar no teto com baterias de lítio para instrumentos, drones e a vida a bordo."), ("Energía propia", "Panel solar en el techo con baterías de litio para instrumentos, drones y la vida a bordo."), ("Own power", "Rooftop solar panel with lithium batteries for instruments, drones and life on board.")),
        (("Conectada em qualquer lugar", "Antena satelital no teto: os dados sobem para o motor RAPP no mesmo dia."), ("Conectada en cualquier lugar", "Antena satelital en el techo: los datos suben al motor RAPP el mismo día."), ("Connected anywhere", "Rooftop satellite antenna: data reaches the RAPP engine the same day.")),
        (("Duas motos trail", "No suporte traseiro, para chegar a talhões, pastos e aguadas onde o motorhome não entra."), ("Dos motos trail", "En el soporte trasero, para llegar a lotes, potreros y aguadas donde el motorhome no entra."), ("Two trail bikes", "On the rear rack, to reach fields, pastures and water points the motorhome cannot.")),
        (("Drones a bordo", "Voos multiespectrais e de mapeamento no primeiro dia; a mesma rota se repete nas visitas seguintes."), ("Drones a bordo", "Vuelos multiespectrales y de mapeo el primer día; la misma ruta se repite en las visitas siguientes."), ("Drones on board", "Multispectral and mapping flights on day one; the same route is repeated on later visits.")),
    ]
    body = f'''
<div class="hero sub hfsub">
  <div class="wrap">
    <p class="crumb"><a href="./">Help Farm</a> / {pg.t("Unidade móvel", "Unidad móvil", "Mobile unit")}</p>
    {pg.t("O laboratório de campo que dorme na fazenda.", "El laboratorio de campo que duerme en el establecimiento.", "The field lab that sleeps on the farm.", "h1")}
    {pg.t("Um motorhome 4x4 leva dois profissionais, drones e instrumentos portáteis até a fazenda. Eles ficam instalados o tempo necessário para medir todas as variáveis, deixam os sensores fixos funcionando e criam a assinatura de referência de cada talhão, rebanho e máquina.", "Un motorhome 4x4 lleva dos profesionales, drones e instrumentos portátiles hasta el establecimiento. Se quedan el tiempo necesario para medir todas las variables, dejan los sensores fijos funcionando y crean la firma de referencia de cada lote, rodeo y máquina.", "A 4x4 motorhome takes two professionals, drones and portable instruments to the farm. They stay as long as needed to measure every variable, leave the fixed sensors running and build the reference signature of each field, herd and machine.", "p", "lead")}
  </div>
</div>
<section>
  <div class="wrap">
    <div class="head">{pg.t("Em corte", "En corte", "Cutaway", "span", "eyebrow")}{pg.t("Tudo cabe num motorhome.", "Todo cabe en un motorhome.", "It all fits in a motorhome.", "h2")}</div>
    <div class="figure">{svg_movel(pg)}</div>
    {feats(pg, res)}
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
    <div class="nextnav"><a class="btn dark" href="celula.html">{pg.t("Ver a célula de campo", "Ver la célula de campo", "See the field cell")} →</a></div>
  </div>
</section>
'''
    shell(pg, "unidade-movel.html", title, body, "Motorhome 4x4 com instrumentos, drones, dormitório, banheiro, energia solar, antena satelital e duas motos trail.")


def celula():
    pg = Page()
    title = pg.title("Célula de campo — Help Farm", "Célula de campo — Help Farm", "Field cell — Help Farm")
    res = [
        (("Profissionais residentes", "Para fazendas grandes e cooperativas que precisam de agrônomo e técnico todos os dias, não só na visita."), ("Profesionales residentes", "Para establecimientos grandes y cooperativas que necesitan agrónomo y técnico todos los días, no solo en la visita."), ("Resident professionals", "For large farms and cooperatives that need an agronomist and technician every day, not just on visits.")),
        (("Moradia digna", "Dormitório com dois beliches, banheiro, cozinha e janelas — o profissional fica bem e fica mais tempo."), ("Vivienda digna", "Dormitorio con dos literas, baño, cocina y ventanas — el profesional está bien y se queda más tiempo."), ("Decent quarters", "Sleeping area with two bunk beds, bathroom, kitchen and windows — staff are comfortable and stay longer.")),
        (("Laboratório de campo", "Bancada, geladeira de amostras e instrumentos para análises rápidas sem mandar tudo para a cidade."), ("Laboratorio de campo", "Mesada, heladera de muestras e instrumentos para análisis rápidos sin mandar todo a la ciudad."), ("Field lab", "Bench, sample fridge and instruments for quick analysis without shipping everything to town.")),
        (("Central de monitoramento", "Telas com os alertas do RAPP da fazenda — ou de todas as fazendas da cooperativa na região."), ("Central de monitoreo", "Pantallas con las alertas del RAPP del establecimiento — o de todos los establecimientos de la cooperativa en la zona."), ("Monitoring desk", "Screens with the farm’s RAPP alerts — or those of every cooperative farm in the region.")),
        (("Energia e internet próprias", "Painel solar com baterias e antena satelital no teto."), ("Energía e internet propias", "Panel solar con baterías y antena satelital en el techo."), ("Own power and internet", "Solar panel with batteries and a satellite antenna on the roof.")),
        (("Implantação rápida", "Chega montada de caminhão e é assentada sobre sapatas; se a operação mudar, a célula muda junto."), ("Instalación rápida", "Llega armada en camión y se asienta sobre zapatas; si la operación cambia, la célula se muda también."), ("Fast set-up", "Arrives pre-built on a truck and sits on footings; if operations change, the cell moves too.")),
    ]
    body = f'''
<div class="hero sub hfsub">
  <div class="wrap">
    <p class="crumb"><a href="./">Help Farm</a> / {pg.t("Célula de campo", "Célula de campo", "Field cell")}</p>
    {pg.t("Uma base permanente onde a fazenda precisa de gente.", "Una base permanente donde el establecimiento necesita gente.", "A permanent base where the farm needs people.", "h1")}
    {pg.t("A célula é um contêiner de 12 metros com dormitório, banheiro, janelas, cozinha, laboratório e central de monitoramento. É transportada e implantada nas fazendas e cooperativas que precisam de profissionais Help Farm o ano todo.", "La célula es un contenedor de 12 metros con dormitorio, baño, ventanas, cocina, laboratorio y central de monitoreo. Se transporta e instala en los establecimientos y cooperativas que necesitan profesionales Help Farm todo el año.", "The cell is a 12-metre container with sleeping area, bathroom, windows, kitchen, lab and monitoring desk. It is trucked in and set up on farms and cooperatives that need Help Farm professionals all year round.", "p", "lead")}
  </div>
</div>
<section>
  <div class="wrap">
    <div class="head">{pg.t("Em corte", "En corte", "Cutaway", "span", "eyebrow")}{pg.t("Contêiner de 12 m, cinco ambientes.", "Contenedor de 12 m, cinco ambientes.", "12 m container, five spaces.", "h2")}</div>
    <div class="figure">{svg_celula(pg)}</div>
    {feats(pg, res)}
  </div>
</section>
<section class="soft">
  <div class="wrap">
    <div class="head">{pg.t("Unidade móvel ou célula?", "¿Unidad móvil o célula?", "Mobile unit or cell?", "span", "eyebrow")}{pg.t("Cada fazenda recebe a estrutura de que precisa.", "Cada establecimiento recibe la estructura que necesita.", "Each farm gets the structure it needs.", "h2")}</div>
    <div class="g g2">
      {card(pg, ("Unidade móvel", "Visitas de medição e instalação em várias fazendas por mês. Ideal para produtores médios e para abrir uma região nova."), ("Unidad móvil", "Visitas de medición e instalación en varios establecimientos por mes. Ideal para productores medianos y para abrir una zona nueva."), ("Mobile unit", "Measuring and installation visits to several farms a month. Ideal for mid-size producers and for opening a new region."), "unidade-movel.html", ("Ver a unidade", "Ver la unidad", "See the unit"))}
      {card(pg, ("Célula de campo", "Presença permanente numa fazenda grande ou num polo de cooperativa, com laboratório e central para atender todas as propriedades ao redor."), ("Célula de campo", "Presencia permanente en un establecimiento grande o en un polo de cooperativa, con laboratorio y central para atender a todas las propiedades cercanas."), ("Field cell", "Permanent presence on a large farm or at a cooperative hub, with a lab and control desk serving every property around it."))}
    </div>
  </div>
</section>
'''
    shell(pg, "celula.html", title, body, "Contêiner de 12 m com dormitório, banheiro, janelas, laboratório e central, implantado nas fazendas.")


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
        (("Célula de campo", "Contrato de presença permanente para fazendas grandes e polos de cooperativa."), ("Célula de campo", "Contrato de presencia permanente para establecimientos grandes y polos de cooperativa."), ("Field cell", "Permanent-presence contract for large farms and cooperative hubs.")),
        (("Risco para bancos e seguradoras", "Índice de condição da fazenda e do rebanho para crédito rural e seguro agrícola."), ("Riesgo para bancos y aseguradoras", "Índice de condición del establecimiento y del rodeo para crédito rural y seguro agrícola."), ("Risk for banks and insurers", "Farm and herd condition index for rural credit and crop insurance.")),
    ]
    body = f'''
<div class="hero sub hfsub">
  <div class="wrap">
    <p class="crumb"><a href="./">Help Farm</a> / {pg.t("Investidores", "Inversionistas", "Investors")}</p>
    {pg.t("Um motor já desenhado, um mercado que já paga por animal e por hectare.", "Un motor ya diseñado, un mercado que ya paga por animal y por hectárea.", "An engine already designed, a market that already pays per animal and per hectare.", "h1")}
    {pg.t("A Help Farm usa o mesmo motor RAPP e a mesma base de desenvolvimento do Help Cure. O primeiro mercado é o Paraguai, onde o grupo já tem empresa e operação; o Brasil vem em seguida, para escala.", "Help Farm usa el mismo motor RAPP y la misma base de desarrollo de Help Cure. El primer mercado es Paraguay, donde el grupo ya tiene empresa y operación; Brasil viene después, para escala.", "Help Farm runs on the same RAPP engine and development base as Help Cure. The first market is Paraguay, where the group already has a company and operations; Brazil follows for scale.", "p", "lead")}
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
<section class="dark">
  <div class="wrap">
    <div class="head">{pg.t("Sequência de entrada", "Secuencia de entrada", "Go-to-market sequence", "span", "eyebrow")}{pg.t("Paraguai prova, Brasil escala.", "Paraguay prueba, Brasil escala.", "Paraguay proves, Brazil scales.", "h2")}</div>
    <div class="g g3 steps">
      <div class="step">{pg.t("Piloto no Paraguai", "Piloto en Paraguay", "Pilot in Paraguay", "h3")}{pg.t("Cinco fazendas com a unidade móvel e uma cooperativa parceira: provar um alerta antecipado documentado em cada frente.", "Cinco establecimientos con la unidad móvil y una cooperativa socia: probar una alerta anticipada documentada en cada frente.", "Five farms with the mobile unit and a partner cooperative: prove one documented early alert on each front.", "p")}</div>
      <div class="step">{pg.t("Brasil e Cone Sul", "Brasil y Cono Sur", "Brazil and Southern Cone", "h3")}{pg.t("Leite e gado de corte primeiro, com a rastreabilidade obrigatória; depois grãos. Seguradoras e bancos entram com o produto de risco.", "Leche y ganado de carne primero, con la trazabilidad obligatoria; después granos. Aseguradoras y bancos entran con el producto de riesgo.", "Dairy and beef first, riding mandatory traceability; then grains. Insurers and banks join with the risk product.", "p")}</div>
      <div class="step">{pg.t("Mercados maduros", "Mercados maduros", "Mature markets", "h3")}{pg.t("Estados Unidos, Oceania e Europa com parceiro local, como camada preditiva sobre dados de equipamentos já instalados.", "Estados Unidos, Oceanía y Europa con socio local, como capa predictiva sobre datos de equipos ya instalados.", "United States, Oceania and Europe with a local partner, as a predictive layer over data from equipment already in place.", "p")}</div>
    </div>
    <div class="cta"><a class="btn primary" href="mailto:investidores@helpcure.com.py?subject=Help%20Farm%20-%20material%20do%20investidor">{pg.t("Pedir o material completo", "Pedir el material completo", "Request the full material")}</a><a class="btn ghost" href="../">{pg.t("Conhecer o Help Cure", "Conocer Help Cure", "See Help Cure")}</a></div>
    {pg.t("Pesquisa de mercado em 16 países, modelo por abrangência e cenários de rodada disponíveis mediante solicitação. Números de preço e custo da Help Farm são premissas em validação.", "Investigación de mercado en 16 países, modelo por alcance y escenarios de ronda disponibles a pedido. Precios y costos de Help Farm son supuestos en validación.", "Market research across 16 countries, scope model and round scenarios available on request. Help Farm price and cost figures are assumptions under validation.", "p", "note darknote")}
  </div>
</section>
'''
    shell(pg, "investidores.html", title, body, "Help Farm para investidores: mercado, modelo de receita e sequência de entrada.")


if __name__ == "__main__":
    home(); movel(); celula(); tecnologia(); investidores()
    print("ok")
