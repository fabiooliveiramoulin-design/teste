# Help Farm — certificação de origem: faixa da home, página com mapa interativo (ouro/prata/bronze)
# e demonstração de um lote certificado com verificação de integridade (SHA-256) no navegador.
# Chamado por build_helpfarm.py (usa Page/shell de lá, via __main__).
import hashlib, html, io, json, sys

import qrcode
import qrcode.image.svg


def B():
    return sys.modules["__main__"]


SITE = "https://helpcure.com.py/helpfarm/"

# ------------------------------------------------------------------ medalha
MET = {
    "ouro": ("#FFF3C4", "#F2C94C", "#B8860B", "#7A5A06"),
    "prata": ("#FFFFFF", "#D3DAE0", "#8A97A3", "#55616C"),
    "bronze": ("#F8D3AE", "#CD7F32", "#8B4A1C", "#5E3011"),
}
WORD = {"ouro": ("OURO", "ORO", "GOLD"), "prata": ("PRATA", "PLATA", "SILVER"), "bronze": ("BRONZE", "BRONCE", "BRONZE")}


def medal(level, uid, word=True, cls="medal", pg=None):
    a, b, c, d = MET[level]
    at = f' x="60" y="104" text-anchor="middle" font-family="Sora,sans-serif" font-weight="700" font-size="11" letter-spacing="2" fill="{d}"'
    if not word:
        txt = ""
    elif pg is not None:
        txt = pg.t(*WORD[level], "text", attrs=at)
    else:
        txt = f'<text{at}>{WORD[level][0]}</text>'

    return f'''<svg class="{cls}" viewBox="0 0 120 150" aria-hidden="true">
<defs><linearGradient id="m{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset=".45" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></linearGradient>
<linearGradient id="r{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A2F1B"/><stop offset="1" stop-color="#2E1D10"/></linearGradient></defs>
<path d="M38 96 L24 146 L42 136 L52 150 L62 104 Z" fill="url(#r{uid})"/><path d="M82 96 L96 146 L78 136 L68 150 L58 104 Z" fill="#5E9F3A"/>
<circle cx="60" cy="64" r="52" fill="url(#m{uid})"/>
<circle cx="60" cy="64" r="43" fill="none" stroke="{d}" stroke-opacity=".45" stroke-width="1.5" stroke-dasharray="2 3"/>
<circle cx="60" cy="64" r="52" fill="none" stroke="{c}" stroke-width="2"/>
<path d="M60 34c14 6 20 18 16 32-14 2-24-6-26-20 2-6 6-10 10-12z" fill="{d}" fill-opacity=".85"/>
<path d="M52 66c6-8 14-14 22-18" fill="none" stroke="{a}" stroke-width="2" stroke-linecap="round"/>
<path d="M44 74l9 9 19-21" fill="none" stroke="{d}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
{txt}</svg>'''


# ------------------------------------------------------------------ faixa da home
def cert_band(pg):
    return f'''<section class="certband">
  <div class="wrap split">
    <div class="medals">{medal("prata", "hb1", pg=pg)}{medal("ouro", "hb2", cls="medal big", pg=pg)}{medal("bronze", "hb3", pg=pg)}</div>
    <div>
      {pg.t("Certificação de origem", "Certificación de origen", "Origin certification", "span", "eyebrow")}
      {pg.t("Cada lote com certidão de nascimento.", "Cada lote con partida de nacimiento.", "Every lot with a birth certificate.", "h2")}
      {pg.t("Do talhão ao comprador: área georreferenciada, prova de que não houve desmatamento, práticas medidas pelo RAPP e um selo ouro, prata ou bronze que qualquer comprador confere pelo QR code.", "Del lote al comprador: área georreferenciada, prueba de que no hubo deforestación, prácticas medidas por el RAPP y un sello oro, plata o bronce que cualquier comprador verifica por código QR.", "From field to buyer: geo-referenced area, proof of no deforestation, practices measured by RAPP and a gold, silver or bronze seal any buyer can check by QR code.", "p", "muted", attrs=' style="margin-top:14px"')}
      <div class="cta"><a class="btn primary" href="certificacao.html#mapa">{pg.t("Ver o mapa de certificação", "Ver el mapa de certificación", "See the certification map")}</a><a class="btn dark" href="lote-demo.html">{pg.t("Ver um lote certificado", "Ver un lote certificado", "See a certified lot")}</a></div>
    </div>
  </div>
</section>'''


# ------------------------------------------------------------------ mapa (SVG estático; interação em cert-map.js)
FARMS = [
    # id, nome, pontos, pino (x,y), tipo (crop|pasture)
    ("be", "Fazenda Boa Esperança", "40,40 250,30 280,150 200,228 50,215", (150, 128), "crop"),
    ("tr", "Fazenda Três Rios", "290,30 520,25 540,140 420,200 300,170", (410, 100), "crop"),
    ("sc", "Estancia Santa Clara", "560,25 820,20 780,128 690,186 572,150", (680, 92), "pasture"),
    ("pr", "Fazenda Primavera", "40,250 210,262 240,380 120,432 30,400", (130, 340), "crop"),
    ("iv", "Fazenda Itá Verá", "244,215 420,226 450,320 370,395 265,360", (348, 300), "crop"),
    ("na", "Fazenda Nova Aurora", "440,205 560,172 640,214 572,282 470,308", (536, 240), "crop"),
    ("la", "Tambo Los Álamos", "900,168 990,150 990,292 862,302 822,232", (912, 236), "pasture"),
    ("sm", "Granja San Miguel", "690,272 840,262 862,380 720,420 652,350", (760, 340), "crop"),
    ("lp", "Estancia La Paloma", "520,440 700,446 742,560 562,604 478,540", (612, 518), "pasture"),
    ("yp", "Estancia Yvy Porã", "760,442 870,402 986,332 990,584 800,604 748,520", (874, 500), "pasture"),
]


def map_svg():
    farms = []
    for fid, name, pts, (px, py), kind in FARMS:
        pat = "url(#rows)" if kind == "crop" else "url(#graze)"
        lw = len(name) * 8.6 + 26
        farms.append(f'''<g class="farm" data-id="{fid}" tabindex="0" role="button" aria-label="{html.escape(name)}">
<polygon class="base" points="{pts}"/><polygon class="tex" points="{pts}" fill="{pat}"/><polygon class="sheen" points="{pts}" fill="url(#sheen)"/>
<polygon class="edge" points="{pts}"/>
<g class="pin" transform="translate({px},{py})"><circle class="halo" r="22"/><circle class="dot" r="12"/><path d="M-5 0l3.5 3.5 6.5-7" fill="none" stroke="#2E1D10" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="ck"/>
<rect class="chip" x="{-lw/2:.0f}" y="18" width="{lw:.0f}" height="27" rx="13.5"/><text class="nm" y="37" text-anchor="middle">{html.escape(name)}</text></g>
</g>''')
    return f'''<svg viewBox="0 0 1000 620" role="img" aria-label="Mapa demonstrativo de fazendas certificadas">
<defs>
<pattern id="rows" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(28)"><rect width="10" height="10" fill="none"/><line x1="0" y1="0" x2="0" y2="10" stroke="#2E1D10" stroke-opacity=".22" stroke-width="2.2"/></pattern>
<pattern id="graze" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="1.6" fill="#2E1D10" fill-opacity=".22"/><circle cx="11" cy="10" r="1.2" fill="#2E1D10" fill-opacity=".16"/></pattern>
<pattern id="forest" width="18" height="18" patternUnits="userSpaceOnUse"><rect width="18" height="18" fill="#557A3A"/><circle cx="5" cy="6" r="5" fill="#46692F"/><circle cx="14" cy="13" r="5.5" fill="#3D5F28"/><circle cx="14" cy="3" r="3" fill="#62893F"/></pattern>
<pattern id="cleared" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#E8B9A6"/><line x1="0" y1="0" x2="0" y2="8" stroke="#B4412A" stroke-width="3"/></pattern>
<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".38"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#2E1D10" stop-opacity=".18"/></linearGradient>
<radialGradient id="land" cx=".4" cy=".35" r=".9"><stop offset="0" stop-color="#F3E7D2"/><stop offset="1" stop-color="#DCC8A6"/></radialGradient>
<filter id="lift" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#2E1D10" flood-opacity=".35"/></filter>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .18 0 0 0 0 .11 0 0 0 0 .06 0 0 0 .07 0"/></filter>
</defs>
<rect width="1000" height="620" fill="url(#land)"/>
<rect width="1000" height="620" filter="url(#grain)"/>
<g fill="none" stroke="#C9B48F" stroke-opacity=".55" stroke-width="1.2">
<path d="M-10 120 C 180 90 300 160 520 120 S 860 60 1010 100"/><path d="M-10 300 C 160 270 300 340 470 300 S 760 230 1010 250"/><path d="M-10 470 C 200 440 330 500 520 470 S 820 420 1010 450"/></g>
<path d="M1010 36 C 950 70 900 110 860 130 S 770 182 700 212 S 610 262 580 300 S 520 372 470 410 S 380 476 300 503 S 120 548 -10 576" fill="none" stroke="#6E9A4F" stroke-opacity=".55" stroke-width="44" stroke-linecap="round"/>
<path d="M1010 36 C 950 70 900 110 860 130 S 770 182 700 212 S 610 262 580 300 S 520 372 470 410 S 380 476 300 503 S 120 548 -10 576" fill="none" stroke="url(#forest)" stroke-width="30" stroke-linecap="round" opacity=".9"/>
<path d="M1010 36 C 950 70 900 110 860 130 S 770 182 700 212 S 610 262 580 300 S 520 372 470 410 S 380 476 300 503 S 120 548 -10 576" fill="none" stroke="#7FB4C9" stroke-width="12" stroke-linecap="round"/>
<path d="M1010 36 C 950 70 900 110 860 130 S 770 182 700 212 S 610 262 580 300 S 520 372 470 410 S 380 476 300 503 S 120 548 -10 576" fill="none" stroke="#B9DCE8" stroke-width="3" stroke-linecap="round" stroke-dasharray="18 26" opacity=".8"/>
<polygon points="20,520 180,500 260,560 120,612 10,600" fill="url(#forest)" opacity=".95"/>
<polygon points="250,232 236,250 262,262" fill="url(#forest)"/>
<path d="M0 238 C 120 246 200 244 238 238 S 400 206 440 204 S 560 168 610 162 S 760 146 840 150 S 960 142 1010 138" fill="none" stroke="#F7EEDD" stroke-width="7" stroke-linecap="round"/>
<path d="M0 238 C 120 246 200 244 238 238 S 400 206 440 204 S 560 168 610 162 S 760 146 840 150 S 960 142 1010 138" fill="none" stroke="#B89F78" stroke-width="1.5" stroke-dasharray="7 6"/>
{"".join(farms)}
<g class="cleared"><polygon points="566,224 612,218 596,262 560,256" fill="url(#cleared)" stroke="#B4412A" stroke-width="2"/></g>
<g class="compass" transform="translate(958,580)"><circle r="22" fill="#F7EEDD" stroke="#B89F78"/><path d="M0 -15 L5 2 L0 -2 L-5 2 Z" fill="#4A2F1B"/><text y="15" text-anchor="middle" font-size="10" font-weight="700" fill="#4A2F1B">N</text></g>
<g transform="translate(24,594)"><rect x="-10" y="-22" width="142" height="36" rx="8" fill="#F7EEDD" fill-opacity=".92"/><rect width="120" height="6" fill="#4A2F1B"/><rect width="60" height="6" fill="#F7EEDD" stroke="#4A2F1B"/><text y="-6" font-size="12" fill="#4A2F1B">0</text><text x="120" y="-6" font-size="12" fill="#4A2F1B" text-anchor="end">5 km</text></g>
</svg>'''


def certificacao():
    pg = B().Page()
    title = pg.title("Certificação de origem — Help Farm", "Certificación de origen — Help Farm", "Origin certification — Help Farm")
    steps = [
        (("Medimos a fazenda", "A unidade móvel e os sensores georreferenciam a área e medem solo, lavoura, água, rebanho e máquinas."), ("Medimos el establecimiento", "La unidad móvil y los sensores georreferencian el área y miden suelo, cultivo, agua, rodeo y máquinas."), ("We measure the farm", "The mobile unit and sensors geo-reference the area and measure soil, crops, water, herd and machines.")),
        (("O RAPP confere", "Cada critério é comparado com a assinatura da própria fazenda e recebe uma nota de aderência."), ("El RAPP verifica", "Cada criterio se compara con la firma del propio establecimiento y recibe una nota de adherencia."), ("RAPP checks", "Each criterion is compared with the farm’s own signature and gets an adherence score.")),
        (("Emitimos o certificado", "Cada lote recebe um registro único, com a impressão digital dos dados gravada em blockchain."), ("Emitimos el certificado", "Cada lote recibe un registro único, con la huella digital de los datos grabada en blockchain."), ("We issue the certificate", "Each lot gets a unique record, with the data’s fingerprint written to a blockchain.")),
        (("O comprador verifica", "Pelo QR code, vê origem, práticas e nível, e confere que nada foi alterado."), ("El comprador verifica", "Por el código QR ve origen, prácticas y nivel, y comprueba que nada fue alterado."), ("The buyer verifies", "Through the QR code they see origin, practices and level, and confirm nothing was changed.")),
    ]
    levels = [
        ("bronze", ("Bronze", "Bronce", "Bronze"), ("Origem comprovada", "Origen comprobado", "Proven origin"),
         [("Livre de desmatamento após 31/12/2020", "Libre de deforestación después del 31/12/2020", "Deforestation-free after 31/12/2020"),
          ("Área georreferenciada e lote rastreado", "Área georreferenciada y lote rastreado", "Geo-referenced area and traced lot"),
          ("Aderência geral de 60% ou mais", "Adherencia general de 60% o más", "Overall adherence of 60% or more")]),
        ("prata", ("Prata", "Plata", "Silver"), ("Fazenda monitorada", "Establecimiento monitoreado", "Monitored farm"),
         [("Tudo do bronze", "Todo lo del bronce", "Everything in bronze"),
          ("Monitoramento RAPP por pelo menos uma safra", "Monitoreo RAPP durante al menos una zafra", "RAPP monitoring for at least one season"),
          ("Nenhum critério abaixo de 60%; média de 75% ou mais", "Ningún criterio por debajo de 60%; promedio de 75% o más", "No criterion below 60%; average of 75% or more")]),
        ("ouro", ("Ouro", "Oro", "Gold"), ("Excelência medida", "Excelencia medida", "Measured excellence"),
         [("Tudo da prata", "Todo lo de la plata", "Everything in silver"),
          ("Carbono do solo medido e histórico de 3 safras", "Carbono del suelo medido e historial de 3 zafras", "Measured soil carbon and a 3-season history"),
          ("Nenhum critério abaixo de 80%; média de 90% ou mais", "Ningún criterio por debajo de 80%; promedio de 90% o más", "No criterion below 80%; average of 90% or more")]),
    ]
    lv = []
    for key, nm, sub, reqs in levels:
        lis = "".join("<li>%s</li>" % pg.t(*r) for r in reqs)
        lv.append(f'<div class="lvl lvl-{key}">{medal(key, "lv" + key, pg=pg)}<div>{pg.t(*nm, "h3")}{pg.t(*sub, "p", "lsub")}<ul>{lis}</ul></div></div>')
    proves = [
        (("Onde", "polígono da área com coordenadas, como exige a regra europeia contra desmatamento"), ("Dónde", "polígono del área con coordenadas, como exige la regla europea contra la deforestación"), ("Where", "area polygon with coordinates, as the EU deforestation rule requires")),
        (("Sem desmatamento", "comparação com imagens de satélite desde 31/12/2020"), ("Sin deforestación", "comparación con imágenes satelitales desde el 31/12/2020"), ("No deforestation", "comparison with satellite imagery since 31/12/2020")),
        (("Como foi produzido", "solo, insumos, água e sanidade medidos pelo RAPP, com nota por critério"), ("Cómo se produjo", "suelo, insumos, agua y sanidad medidos por el RAPP, con nota por criterio"), ("How it was produced", "soil, inputs, water and health measured by RAPP, scored per criterion")),
        (("Quanto e com que qualidade", "volume, umidade e qualidade confirmados na entrega ao armazém"), ("Cuánto y con qué calidad", "volumen, humedad y calidad confirmados en la entrega al acopio"), ("How much and what quality", "volume, moisture and quality confirmed on delivery to storage")),
    ]
    faq = [
        (("Preciso entender de cripto?", "Não. Produtor e comprador veem o certificado e o QR code; o registro em blockchain funciona por trás."), ("¿Necesito entender de cripto?", "No. Productor y comprador ven el certificado y el código QR; el registro en blockchain funciona por detrás."), ("Do I need to understand crypto?", "No. Producers and buyers see the certificate and the QR code; the blockchain record works behind the scenes.")),
        (("Quem é dono dos dados?", "O produtor. Só a impressão digital dos dados fica pública; os dados completos ficam protegidos e cada compartilhamento depende da autorização dele."), ("¿Quién es dueño de los datos?", "El productor. Solo la huella digital de los datos es pública; los datos completos quedan protegidos y cada intercambio depende de su autorización."), ("Who owns the data?", "The producer. Only the data’s fingerprint is public; the full data stays protected and every share requires their permission.")),
        (("O certificado é um investimento?", "Não. Ele prova origem e práticas de produção; não é vendido como ativo financeiro e não promete rendimento."), ("¿El certificado es una inversión?", "No. Prueba origen y prácticas de producción; no se vende como activo financiero y no promete rendimiento."), ("Is the certificate an investment?", "No. It proves origin and production practices; it is not sold as a financial asset and promises no return.")),
        (("Como uma fazenda sobe de nível?", "O RAPP mostra quais critérios estão abaixo do mínimo e o que fazer; a reavaliação acontece a cada safra."), ("¿Cómo sube de nivel un establecimiento?", "El RAPP muestra qué criterios están por debajo del mínimo y qué hacer; la reevaluación ocurre en cada zafra."), ("How does a farm move up a level?", "RAPP shows which criteria are below the minimum and what to do; the farm is re-assessed every season.")),
        (("Serve para a regra europeia contra desmatamento?", "O certificado reúne os dados que a regra pede — coordenadas da área e prova de que não houve desmatamento após 2020 — para o comprador usar na diligência dele."), ("¿Sirve para la regla europea contra la deforestación?", "El certificado reúne los datos que pide la regla — coordenadas del área y prueba de que no hubo deforestación después de 2020 — para que el comprador los use en su diligencia."), ("Does it help with the EU deforestation rule?", "The certificate gathers the data the rule asks for — area coordinates and proof of no deforestation after 2020 — for the buyer to use in their due diligence.")),
    ]
    faqh = "".join('<details class="faq">%s%s</details>' % (pg.t(a[0], b[0], c[0], "summary"), pg.t(a[1], b[1], c[1], "p")) for a, b, c in faq)
    body = f'''
<div class="hero sub hfsub certhero">
  <div class="wrap">
    <div>
      <p class="crumb"><a href="./">Help Farm</a> / {pg.t("Certificação", "Certificación", "Certification")}</p>
      {pg.t("Cada lote com certidão de nascimento.", "Cada lote con partida de nacimiento.", "Every lot with a birth certificate.", "h1")}
      {pg.t("O certificado Help Farm mostra de onde veio o produto, como ele foi produzido e em que nível a fazenda está — ouro, prata ou bronze. O comprador confere tudo pelo QR code, e o registro não pode ser alterado depois.", "El certificado Help Farm muestra de dónde vino el producto, cómo se produjo y en qué nivel está el establecimiento — oro, plata o bronce. El comprador verifica todo por código QR, y el registro no puede alterarse después.", "The Help Farm certificate shows where the product came from, how it was produced and which level the farm is at — gold, silver or bronze. Buyers check everything via QR code, and the record cannot be changed afterwards.", "p", "lead")}
      <div class="cta"><a class="btn primary" href="#mapa">{pg.t("Explorar o mapa", "Explorar el mapa", "Explore the map")}</a><a class="btn ghost" href="lote-demo.html">{pg.t("Ver um lote certificado", "Ver un lote certificado", "See a certified lot")}</a></div>
    </div>
    <div class="medals hero-medals">{medal("prata", "hm1", pg=pg)}{medal("ouro", "hm2", cls="medal big", pg=pg)}{medal("bronze", "hm3", pg=pg)}</div>
  </div>
</div>

<section class="dark">
  <div class="wrap">
    <div class="head">{pg.t("Como funciona", "Cómo funciona", "How it works", "span", "eyebrow")}{pg.t("Da medição ao QR code em quatro passos.", "De la medición al código QR en cuatro pasos.", "From measurement to QR code in four steps.", "h2")}</div>
    <div class="g g4 steps">{"".join('<div class="step">%s%s</div>' % (pg.t(a[0], b[0], c[0], "h3"), pg.t(a[1], b[1], c[1], "p")) for a, b, c in steps)}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head">{pg.t("Níveis", "Niveles", "Levels", "span", "eyebrow")}{pg.t("Três níveis, medidos — não declarados.", "Tres niveles, medidos — no declarados.", "Three levels, measured — not self-declared.", "h2")}
    {pg.t("O nível sai da nota de aderência calculada pelo RAPP em seis critérios. Uma fazenda que não cumpre um requisito obrigatório fica “em adequação”, com plano de ação acompanhado.", "El nivel sale de la nota de adherencia calculada por el RAPP en seis criterios. Un establecimiento que no cumple un requisito obligatorio queda “en adecuación”, con plan de acción acompañado.", "The level comes from the adherence score RAPP calculates across six criteria. A farm that misses a mandatory requirement is marked “in progress”, with a monitored action plan.", "p", "muted")}</div>
    <div class="lvls">{"".join(lv)}</div>
  </div>
</section>

<section class="soft" id="mapa">
  <div class="wrap">
    <div class="head">{pg.t("Mapa interativo", "Mapa interactivo", "Interactive map", "span", "eyebrow")}{pg.t("Veja a aderência de cada fazenda.", "Vea la adherencia de cada establecimiento.", "See each farm’s adherence.", "h2")}
    {pg.t("Toque numa fazenda para ver as notas. Troque a camada para ver a região por critério — e note a Fazenda Nova Aurora, bloqueada por uma área aberta depois de 2020.", "Toque un establecimiento para ver las notas. Cambie la capa para ver la región por criterio — y observe el establecimiento Nova Aurora, bloqueado por un área abierta después de 2020.", "Tap a farm to see its scores. Switch the layer to view the region by criterion — and notice Nova Aurora farm, blocked by an area cleared after 2020.", "p", "muted")}</div>
    <div class="cmap" id="cmap">
      <div class="cmap-main">
        <div class="cmodes" id="cmodes" role="toolbar"></div>
        <div class="cmap-stage">
          <div class="cbar"><div class="cstats" id="cstats"></div><div class="cdemo">{pg.t("Demonstração · fazendas e notas fictícias", "Demostración · establecimientos y notas ficticios", "Demo · fictional farms and scores")}</div></div>
          <div class="cscroll">{map_svg()}</div>
          <div class="ctip" id="ctip" hidden></div>
        </div>
        <div class="clegend" id="clegend"></div>
      </div>
      <aside class="cpanel" id="cpanel" aria-live="polite"></aside>
    </div>
    <template id="md-ouro">{medal("ouro", "tpo", word=False)}</template><template id="md-prata">{medal("prata", "tpp", word=False)}</template><template id="md-bronze">{medal("bronze", "tpb", word=False)}</template>
  </div>
</section>

<section>
  <div class="wrap split" style="align-items:start">
    <div>
      {pg.t("O que o certificado prova", "Qué prueba el certificado", "What the certificate proves", "span", "eyebrow")}
      {pg.t("Origem, prática e quantidade — no mesmo documento.", "Origen, práctica y cantidad — en el mismo documento.", "Origin, practice and quantity — in one document.", "h2")}
      {B().feats(pg, proves)}
    </div>
    <div class="whychain">
      {pg.t("Por que blockchain", "Por qué blockchain", "Why blockchain", "span", "eyebrow")}
      {pg.t("Um registro que ninguém consegue mudar depois — nem a Help Farm.", "Un registro que nadie puede cambiar después — ni Help Farm.", "A record nobody can change afterwards — not even Help Farm.", "h3")}
      {pg.t("Só a impressão digital dos dados (o hash) fica gravada na blockchain; os dados completos ficam protegidos. Se alguém mudar um único número do certificado, a impressão digital deixa de bater e a verificação acusa na hora.", "Solo la huella digital de los datos (el hash) queda grabada en la blockchain; los datos completos quedan protegidos. Si alguien cambia un solo número del certificado, la huella deja de coincidir y la verificación lo detecta al instante.", "Only the data’s fingerprint (the hash) is written to the blockchain; the full data stays protected. If anyone changes a single number on the certificate, the fingerprint no longer matches and verification flags it instantly.", "p", "muted", attrs=' style="margin-top:12px"')}
      <a class="btn dark" href="lote-demo.html#verificar" style="margin-top:18px">{pg.t("Testar a verificação num lote", "Probar la verificación en un lote", "Try verification on a lot")} →</a>
    </div>
  </div>
</section>

<section class="soft">
  <div class="wrap narrow">
    <div class="head">{pg.t("Perguntas frequentes", "Preguntas frecuentes", "FAQ", "span", "eyebrow")}{pg.t("Simples para o produtor, confiável para o comprador.", "Simple para el productor, confiable para el comprador.", "Simple for producers, reliable for buyers.", "h2")}</div>
    {faqh}
    {pg.t("Critérios, limites e níveis são uma proposta em validação com produtores, compradores e certificadoras. O mapa usa fazendas e notas fictícias.", "Criterios, límites y niveles son una propuesta en validación con productores, compradores y certificadoras. El mapa usa establecimientos y notas ficticios.", "Criteria, thresholds and levels are a proposal being validated with producers, buyers and certifiers. The map uses fictional farms and scores.", "p", "note", attrs=' style="margin-top:24px"')}
  </div>
</section>
'''
    B().shell(pg, "certificacao.html", title, body, "Certificação de origem Help Farm: níveis ouro, prata e bronze, mapa interativo de aderência e verificação por QR code.",
              extra='<script src="assets/cert-map.js?v=1"></script>')


# ------------------------------------------------------------------ lote demonstrativo
LOT = {
    "lote": "HF-PY-2027-000184",
    "produto": "Soja (grão)",
    "fazenda": "Fazenda Boa Esperança (demonstração)",
    "talhao": "Talhão 7",
    "area_ha": 412.6,
    "safra": "2026/27",
    "poligono": [[-25.4312, -54.9821], [-25.4298, -54.9644], [-25.4419, -54.9618], [-25.4447, -54.9779], [-25.4378, -54.9842]],
    "livre_desmatamento_desde": "2020-12-31",
    "volume_t": 1240.5,
    "umidade_pct": 13.1,
    "impurezas_pct": 0.8,
    "proteina_pct": 37.9,
    "aderencia": {"desmatamento": 100, "rastreabilidade": 98, "solo_carbono": 92, "insumos": 90, "agua_clima": 91, "sanidade": 94},
    "nivel": "Ouro",
    "emitido_em": "2027-04-18",
    "verificador": "Help Farm · motor RAPP",
}


def canon(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def qr_svg(url):
    q = qrcode.QRCode(border=1, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(url); q.make(fit=True)
    m = q.get_matrix(); n = len(m)
    d = "".join("M%d %dh1v1h-1z" % (x, y) for y, row in enumerate(m) for x, v in enumerate(row) if v)
    return f'<svg class="qr" viewBox="0 0 {n} {n}" shape-rendering="crispEdges" aria-label="QR code"><rect width="{n}" height="{n}" fill="#fff"/><path d="{d}" fill="#2E1D10"/></svg>'


def plot_svg(pg):
    # talhão 7 em planta: polígono, reserva e mata ciliar, pontos de medição
    return '''<svg class="plot" viewBox="0 0 520 360" role="img" aria-label="Talhão 7 em planta">
<defs><pattern id="pr" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(28)"><line x1="0" y1="0" x2="0" y2="9" stroke="#2E1D10" stroke-opacity=".2" stroke-width="2"/></pattern>
<pattern id="pf" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="#557A3A"/><circle cx="4" cy="5" r="4.5" fill="#46692F"/><circle cx="12" cy="12" r="5" fill="#3D5F28"/></pattern>
<linearGradient id="pg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F7DE86"/><stop offset="1" stop-color="#D9A93A"/></linearGradient></defs>
<rect width="520" height="360" rx="18" fill="#EFE3CC"/>
<g stroke="#D8C6A6" stroke-width="1">''' + "".join('<line x1="%d" y1="0" x2="%d" y2="360"/>' % (x, x) for x in range(40, 520, 40)) + "".join('<line x1="0" y1="%d" x2="520" y2="%d"/>' % (y, y) for y in range(40, 360, 40)) + '''</g>
<path d="M-10 330 C 120 300 260 340 530 300" fill="none" stroke="#6E9A4F" stroke-opacity=".6" stroke-width="40"/><path d="M-10 330 C 120 300 260 340 530 300" fill="none" stroke="#7FB4C9" stroke-width="9"/>
<polygon points="380,40 470,52 480,150 400,140" fill="url(#pf)"/>
<polygon points="80,60 360,44 392,190 330,270 110,262 60,170" fill="url(#pg)" stroke="#8B6508" stroke-width="3"/>
<polygon points="80,60 360,44 392,190 330,270 110,262 60,170" fill="url(#pr)"/>
<polygon points="210,150 262,140 270,190 222,196" fill="#B4412A" fill-opacity=".18" stroke="#B4412A" stroke-dasharray="4 3"/>
''' + "".join('<g transform="translate(%d,%d)"><circle r="7" fill="#FFF" stroke="#2E1D10" stroke-width="2"/><circle r="2.5" fill="#2E1D10"/></g>' % p for p in [(120, 110), (200, 90), (300, 80), (340, 170), (150, 200), (250, 230), (110, 160)]) + '''
<g font-family="Lexend,sans-serif" font-size="13" fill="#2E1D10">' + pg.t("Talhão 7 · 412,6 ha", "Lote 7 · 412,6 ha", "Field 7 · 412.6 ha", "text", attrs=' x="96" y="86" font-weight="600"') + pg.t("Reserva", "Reserva", "Reserve", "text", attrs=' x="404" y="170"') + '<text x="276" y="212">38 ha</text></g>
<g transform="translate(24,336)"><rect width="100" height="5" fill="#2E1D10"/><rect width="50" height="5" fill="#F7EEDD" stroke="#2E1D10"/><text x="100" y="-6" font-size="11" fill="#2E1D10" text-anchor="end">1 km</text></g>
</svg>'''


def lote_demo():
    pg = B().Page()
    title = pg.title("Lote certificado (demonstração) — Help Farm", "Lote certificado (demostración) — Help Farm", "Certified lot (demo) — Help Farm")
    digest = hashlib.sha256(canon(LOT).encode("utf-8")).hexdigest()
    tx = "0x" + hashlib.sha256(("tx" + digest).encode()).hexdigest()
    contract = "0x" + hashlib.sha256(b"helpfarm-cert-demo").hexdigest()[:40]
    crit = [("desmatamento", "Livre de desmatamento", "Libre de deforestación", "Deforestation-free"),
            ("rastreabilidade", "Rastreabilidade", "Trazabilidad", "Traceability"),
            ("solo_carbono", "Solo e carbono", "Suelo y carbono", "Soil and carbon"),
            ("insumos", "Uso racional de insumos", "Uso racional de insumos", "Rational input use"),
            ("agua_clima", "Água e clima", "Agua y clima", "Water and climate"),
            ("sanidade", "Sanidade da lavoura", "Sanidad del cultivo", "Crop health")]
    bars = "".join(f'<div class="bar"><div class="bl">{pg.t(pt, es, en)}</div><div class="bt"><i style="width:{LOT["aderencia"][k]}%"></i></div><b>{LOT["aderencia"][k]}%</b></div>' for k, pt, es, en in crit)
    tl = [
        ("12/09/2026", ("Unidade móvel mede o talhão: solo em 7 pontos, voo multiespectral", "La unidad móvil mide el lote: suelo en 7 puntos, vuelo multiespectral", "Mobile unit measures the field: soil at 7 points, multispectral flight")),
        ("03/10/2026", ("Plantio registrado; semente e dose de adubo por zona", "Siembra registrada; semilla y dosis de fertilizante por zona", "Planting recorded; seed and fertiliser rate by zone")),
        ("20/12/2026", ("Alerta de ferrugem: aplicação só em 38 ha, onde o RAPP indicou", "Alerta de roya: aplicación solo en 38 ha, donde indicó el RAPP", "Rust alert: spraying only on 38 ha, where RAPP pointed")),
        ("28/03/2027", ("Colheita: 1.240,5 t", "Cosecha: 1.240,5 t", "Harvest: 1,240.5 t")),
        ("02/04/2027", ("Entrada no armazém: umidade 13,1%, impurezas 0,8%", "Ingreso al acopio: humedad 13,1%, impurezas 0,8%", "Into storage: 13.1% moisture, 0.8% impurities")),
        ("18/04/2027", ("Certificado emitido e registrado em blockchain", "Certificado emitido y registrado en blockchain", "Certificate issued and recorded on blockchain")),
    ]
    tlh = "".join(f'<li><time>{d}</time>{pg.t(*t)}</li>' for d, t in tl)
    url = SITE + "lote-demo.html"
    body = f'''
<div class="demo-ribbon">{pg.t("DEMONSTRAÇÃO — dados fictícios, registro simulado em rede de teste", "DEMOSTRACIÓN — datos ficticios, registro simulado en red de prueba", "DEMO — fictional data, record simulated on a test network")}</div>
<div class="hero sub hfsub lothero">
  <div class="wrap">
    <p class="crumb"><a href="./">Help Farm</a> / <a href="certificacao.html">{pg.t("Certificação", "Certificación", "Certification")}</a> / {LOT["lote"]}</p>
    <div class="certcard">
      <div class="cc-medal">{medal("ouro", "lot", cls="medal big", pg=pg)}<span class="cc-ok">✓ {pg.t("Verificado", "Verificado", "Verified")}</span></div>
      <div class="cc-body">
        {pg.t("Certificado de origem Help Farm", "Certificado de origen Help Farm", "Help Farm origin certificate", "span", "eyebrow")}
        {pg.t("Soja em grão · 1.240,5 t", "Soja en grano · 1.240,5 t", "Soybeans (grain) · 1,240.5 t", "h1")}
        <dl class="cc-grid">
          <div><dt>{pg.t("Lote", "Lote", "Lot")}</dt><dd>{LOT["lote"]}</dd></div>
          <div><dt>{pg.t("Fazenda", "Establecimiento", "Farm")}</dt><dd>Fazenda Boa Esperança</dd></div>
          <div><dt>{pg.t("Talhão e área", "Lote y área", "Field and area")}</dt><dd>{pg.t("Talhão 7 · 412,6 ha", "Lote 7 · 412,6 ha", "Field 7 · 412.6 ha")}</dd></div>
          <div><dt>{pg.t("Safra", "Zafra", "Season")}</dt><dd>2026/27</dd></div>
          <div><dt>{pg.t("Nível", "Nivel", "Level")}</dt><dd class="gold">{pg.t("Ouro · aderência 94%", "Oro · adherencia 94%", "Gold · 94% adherence")}</dd></div>
          <div><dt>{pg.t("Emitido em", "Emitido el", "Issued on")}</dt><dd>18/04/2027</dd></div>
        </dl>
      </div>
      <div class="cc-qr">{qr_svg(url)}<small>{pg.t("Aponte a câmera para conferir", "Apunte la cámara para verificar", "Point your camera to verify")}</small></div>
    </div>
  </div>
</div>

<section>
  <div class="wrap split" style="align-items:start">
    <div>
      {pg.t("Onde foi produzido", "Dónde se produjo", "Where it was produced", "span", "eyebrow")}
      {pg.t("Área georreferenciada, sem desmatamento desde 2020.", "Área georreferenciada, sin deforestación desde 2020.", "Geo-referenced area, no deforestation since 2020.", "h2")}
      <div class="figure" style="margin-top:20px">{plot_svg(pg)}</div>
      <p class="muted" style="font-size:14px;margin-top:10px">{pg.t("Polígono do talhão, reserva vizinha e mata ciliar preservadas; em vermelho tracejado, os 38 ha onde houve aplicação contra ferrugem. Pontos brancos: medições de solo da unidade móvel.", "Polígono del lote, reserva vecina y bosque ribereño preservados; en rojo punteado, las 38 ha donde hubo aplicación contra roya. Puntos blancos: mediciones de suelo de la unidad móvil.", "Field polygon, neighbouring reserve and riverside forest preserved; dashed red marks the 38 ha sprayed against rust. White dots: mobile-unit soil measurements.")}</p>
    </div>
    <div>
      {pg.t("Como foi produzido", "Cómo se produjo", "How it was produced", "span", "eyebrow")}
      {pg.t("Aderência por critério.", "Adherencia por criterio.", "Adherence by criterion.", "h2")}
      <div class="bars big">{bars}</div>
      <div class="qual">
        <div><b>13,1%</b>{pg.t("umidade", "humedad", "moisture")}</div><div><b>0,8%</b>{pg.t("impurezas", "impurezas", "impurities")}</div><div><b>37,9%</b>{pg.t("proteína", "proteína", "protein")}</div>
      </div>
    </div>
  </div>
</section>

<section class="soft">
  <div class="wrap narrow">
    <div class="head">{pg.t("Histórico do lote", "Historial del lote", "Lot history", "span", "eyebrow")}{pg.t("Da medição ao armazém.", "De la medición al acopio.", "From measurement to storage.", "h2")}</div>
    <ol class="tline">{tlh}</ol>
  </div>
</section>

<section class="dark" id="verificar">
  <div class="wrap">
    <div class="head">{pg.t("Registro em blockchain", "Registro en blockchain", "Blockchain record", "span", "eyebrow")}{pg.t("Confira que nada foi alterado.", "Compruebe que nada fue alterado.", "Check that nothing was changed.", "h2")}
    {pg.t("O botão recalcula, aqui no seu navegador, a impressão digital (SHA-256) dos dados deste certificado e compara com a que foi gravada. Depois, simule uma adulteração: basta mudar 10 toneladas para a impressão digital deixar de bater.", "El botón recalcula, aquí en su navegador, la huella digital (SHA-256) de los datos de este certificado y la compara con la grabada. Después, simule una adulteración: basta cambiar 10 toneladas para que la huella deje de coincidir.", "The button recalculates, right here in your browser, the fingerprint (SHA-256) of this certificate’s data and compares it with the recorded one. Then simulate tampering: changing just 10 tonnes makes the fingerprint stop matching.", "p")}</div>
    <div class="chain">
      <dl>
        <div><dt>{pg.t("Rede", "Red", "Network")}</dt><dd>{pg.t("Polygon Amoy (rede de teste) — simulado", "Polygon Amoy (red de prueba) — simulado", "Polygon Amoy (test network) — simulated")}</dd></div>
        <div><dt>{pg.t("Contrato", "Contrato", "Contract")}</dt><dd class="mono">{contract}</dd></div>
        <div><dt>Token</dt><dd class="mono">#184 · ERC-721</dd></div>
        <div><dt>{pg.t("Transação", "Transacción", "Transaction")}</dt><dd class="mono">{tx[:22]}…{tx[-8:]}</dd></div>
        <div><dt>{pg.t("Impressão digital gravada", "Huella digital grabada", "Recorded fingerprint")}</dt><dd class="mono" id="hrec">{digest}</dd></div>
        <div><dt>{pg.t("Impressão digital calculada agora", "Huella digital calculada ahora", "Fingerprint calculated now")}</dt><dd class="mono" id="hnow">—</dd></div>
      </dl>
      <div class="vbtns"><button class="btn primary" type="button" id="vbtn">{pg.t("Verificar integridade", "Verificar integridad", "Verify integrity")}</button><button class="btn ghost" type="button" id="tbtn">{pg.t("Simular adulteração (+10 t)", "Simular adulteración (+10 t)", "Simulate tampering (+10 t)")}</button></div>
      <div class="vres" id="vres" aria-live="polite"></div>
      <span hidden id="m-ok">{pg.t("Confere. O certificado é o mesmo que foi registrado.", "Coincide. El certificado es el mismo que se registró.", "Match. The certificate is the same one that was recorded.")}</span>
      <span hidden id="m-bad">{pg.t("Não confere. Alguém alterou o volume para 1.250,5 t — a verificação acusa na hora.", "No coincide. Alguien cambió el volumen a 1.250,5 t — la verificación lo detecta al instante.", "No match. Someone changed the volume to 1,250.5 t — verification flags it instantly.")}</span>
    </div>
    <script type="application/json" id="lotdata">{canon(LOT)}</script>
  </div>
</section>
'''
    js = r'''<script>
(function(){
  var data=JSON.parse(document.getElementById('lotdata').textContent);
  function canon(o){if(Array.isArray(o))return '['+o.map(canon).join(',')+']';if(o&&typeof o==='object')return '{'+Object.keys(o).sort().map(function(k){return JSON.stringify(k)+':'+canon(o[k]);}).join(',')+'}';return JSON.stringify(o);}
  function sha(s){return crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)).then(function(b){return Array.from(new Uint8Array(b)).map(function(x){return x.toString(16).padStart(2,'0');}).join('');});}
  var rec=document.getElementById('hrec').textContent.trim(),now=document.getElementById('hnow'),res=document.getElementById('vres');
  function run(obj,tamper){now.textContent='…';res.className='vres';res.textContent='';
    sha(canon(obj)).then(function(h){now.textContent=h;var ok=h===rec;now.className='mono '+(ok?'ok':'bad');
      res.className='vres '+(ok?'ok':'bad');res.textContent=(ok?'✓ ':'✗ ')+document.getElementById(ok?'m-ok':'m-bad').textContent;});}
  document.getElementById('vbtn').onclick=function(){run(data);};
  document.getElementById('tbtn').onclick=function(){var t=JSON.parse(JSON.stringify(data));t.volume_t=1250.5;run(t,true);};
})();
</script>'''
    B().shell(pg, "lote-demo.html", title, body, "Demonstração de um lote de soja com certificado de origem Help Farm nível ouro e verificação de integridade.", extra=js)
