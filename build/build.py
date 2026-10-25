# Gera as páginas do site Help Cure (PT no HTML + ES/EN embutidos para a troca de idioma).
# Uso: python3 build/build.py   (a partir da raiz do repositório)
import json, html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FULL = {"pt": "tWPiFOwbaNw", "es": "pTT-sQGMW0U", "en": "2fYAVUm0ziI"}
SHORT = {
    "paciente": {"pt": "CR9zwnwG_Lg"},
    "hospital": {"pt": "DGMd9nJyOEg", "es": "zBIRuKMUgQo"},
    "celula": {"pt": "PGypaX2jzqk", "es": "SfoPAlmMvAk"},
    "movel": {"pt": "__HsnXBze2A"},
}


class Page:
    def __init__(self, depth):
        self.es, self.en, self.n = {}, {}, 0
        self.p = "../" * depth

    def t(self, pt, es, en, tag="span", cls="", raw=False, attrs=""):
        self.n += 1
        k = "k%d" % self.n
        self.es[k], self.en[k] = es, en
        h = ' data-html' if raw else ''
        c = ' class="%s"' % cls if cls else ''
        body = pt if raw else html.escape(pt)
        return '<%s data-i="%s"%s%s%s>%s</%s>' % (tag, k, h, c, attrs, body, tag)

    def alt(self, pt, es, en):
        self.n += 1
        k = "a%d" % self.n
        self.es["alt:" + k], self.en["alt:" + k] = es, en
        return 'alt="%s" data-alt="%s"' % (html.escape(pt), k)

    def title(self, pt, es, en):
        self.es["_title"], self.en["_title"] = es, en
        return pt


NAV = [("index.html", "Início", "Inicio", "Home"),
       ("solucoes/index.html", "Soluções", "Soluciones", "Solutions"),
       ("para-quem.html", "Para quem", "Para quién", "Who it’s for"),
       ("tecnologia.html", "Tecnologia", "Tecnología", "Technology"),
       ("solidario.html", "Solidário", "Solidario", "Solidarity")]


def shell(pg, path, title, body, desc):
    p = pg.p
    links = []
    for href, pt, es, en in NAV:
        cur = ' aria-current="page"' if path == href or (href.startswith("solucoes/") and path.startswith("solucoes/")) else ''
        links.append('<a href="%s%s"%s>%s</a>' % (p, href.replace("index.html", "") or "./", cur, pg.t(pt, es, en)))
    links.append('<a href="/investidores/" data-inv="/investidores/">%s</a>' % pg.t("Investidores", "Inversionistas", "Investors"))
    foot_sol = "".join('<a href="%ssolucoes/%s.html">%s</a>' % (p, s, pg.t(a, b, c)) for s, a, b, c in SOLS)
    head = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{p}img/hero.webp">
<link rel="icon" href="{p}img/icone.svg" type="image/svg+xml"><link rel="icon" href="{p}img/logo/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="{p}img/logo/helpcure-icone-app-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Lexend:wght@300;400;500;600&display=swap">
<link rel="stylesheet" href="{p}assets/site.css?v=3">
</head>
<body>
<header class="top">
  <div class="wrap nav">
    <a class="logo" href="{p}" aria-label="Help Cure"><img src="{p}img/logo/helpcure-simbolo-animado-fundo-escuro.svg" alt="" aria-hidden="true"><span style="letter-spacing:-.02em">Help<b>Cure</b></span></a>
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
    <div><a class="logo" href="{p}" style="color:#E9F3F0;display:flex"><img src="{p}img/logo/helpcure-simbolo-animado-fundo-escuro.svg" alt="" aria-hidden="true"><span style="letter-spacing:-.02em">Help<b>Cure</b></span></a>
      {pg.t("Monitoramento contínuo de saúde: cada paciente comparado com ele mesmo.", "Monitoreo continuo de salud: cada paciente comparado consigo mismo.", "Continuous health monitoring: every patient compared with themselves.", "p", attrs=' style="margin-top:10px;max-width:40ch"')}
      <p style="margin-top:12px">{pg.t("Contato", "Contacto", "Contact")}: <a href="mailto:contato@helpcure.com.py" style="display:inline">contato@helpcure.com.py</a></p></div>
    <div><h4>{pg.t("Soluções", "Soluciones", "Solutions")}</h4>{foot_sol}</div>
    <div><h4>{pg.t("Help Cure", "Help Cure", "Help Cure")}</h4>
      <a href="{p}para-quem.html">{pg.t("Para quem é", "Para quién es", "Who it’s for")}</a>
      <a href="{p}tecnologia.html">{pg.t("Tecnologia e segurança", "Tecnología y seguridad", "Technology and security")}</a>
      <a href="{p}solidario.html">{pg.t("Help Cure Solidário", "Help Cure Solidario", "Help Cure Solidarity")}</a>
      <a href="{p}app/">{pg.t("App do paciente", "App del paciente", "Patient app")}</a>
      <a href="/investidores/" data-inv="/investidores/">{pg.t("Área do investidor", "Área del inversionista", "Investor area")}</a></div>
    <div class="legal">© 2026 Help Cure · {pg.t("Plataforma em fase de piloto. Imagens dos vídeos são simulações com personagens fictícios.", "Plataforma en fase piloto. Las imágenes de los videos son simulaciones con personajes ficticios.", "Platform in pilot stage. Video images are simulations with fictional characters.")}</div>
  </div>
</footer>
<script>window.HC_T={json.dumps({"es": pg.es, "en": pg.en}, ensure_ascii=False)};</script>
<script src="{p}assets/site.js?v=3"></script>
</body>
</html>
'''
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(head + body + foot)


def video(pg, ids, tabs=False, dark=True):
    t = '<div class="vtabs" role="tablist"></div>' if tabs else ''
    return '<div class="video" data-ids=\'%s\'>%s<div class="player"></div><p class="vnote"></p></div>' % (json.dumps(ids), t)


def feats(pg, items):
    return '<ul class="feat">' + "".join('<li>%s</li>' % pg.t("<b>%s</b> — %s" % (a[0], a[1]), "<b>%s</b> — %s" % (b[0], b[1]), "<b>%s</b> — %s" % (c[0], c[1]), "span", raw=True) for a, b, c in items) + '</ul>'


SOLS = [("paciente", "Paciente e família", "Paciente y familia", "Patient and family"),
        ("hospital", "Hospital e clínica", "Hospital y clínica", "Hospital and clinic"),
        ("farmacia", "Farmácia", "Farmacia", "Pharmacy"),
        ("homecare", "Home care", "Atención domiciliaria", "Home care"),
        ("celula", "Célula de atendimento", "Célula de atención", "Care cell"),
        ("movel", "Unidade móvel", "Unidad móvil", "Mobile unit")]

SOL_CARD = {
    "paciente": ("acompanhamento", ("App, lembretes de remédio e resumo de emergência no bolso.", "App, recordatorios de medicamentos y resumen de emergencia en el bolsillo.", "App, medication reminders and an emergency summary in your pocket.")),
    "hospital": ("hospital", ("Sinais vitais direto no sistema e a família informada.", "Signos vitales directo al sistema y la familia informada.", "Vital signs straight into the system and the family kept informed.")),
    "farmacia": ("farmacia", ("Receita, dispensação e adesão ao tratamento no mesmo histórico.", "Receta, dispensación y adherencia al tratamiento en el mismo historial.", "Prescription, dispensing and adherence in one history.")),
    "homecare": ("estavel", ("O cuidado continua em casa depois da alta.", "El cuidado continúa en casa después del alta.", "Care continues at home after discharge.")),
    "celula": ("celula", ("Sala de 9 m² com triagem e teleconsulta, onde as pessoas estão.", "Sala de 9 m² con triaje y teleconsulta, donde están las personas.", "A 9 m² room with triage and teleconsultation, where people are.")),
    "movel": ("movel_toldo", ("Triagem e duas cabines de teleconsulta sobre rodas.", "Triaje y dos cabinas de teleconsulta sobre ruedas.", "Triage and two teleconsultation booths on wheels.")),
}


def sol_cards(pg, skip=None):
    out = []
    for s, a, b, c in SOLS:
        if s == skip:
            continue
        img, d = SOL_CARD[s]
        out.append('<a class="card" href="%ssolucoes/%s.html"><img src="%simg/%s.webp" alt="" loading="lazy"><div class="in">%s%s<span class="more">%s</span></div></a>' % (
            pg.p, s, pg.p, img, pg.t(a, b, c, "h3"), pg.t(d[0], d[1], d[2], "p"), pg.t("Saiba mais →", "Más información →", "Learn more →")))
    return "".join(out)


# ------------------------------------------------------------------ HOME
def home():
    pg = Page(0)
    T = pg.t
    title = pg.title("Help Cure — Ajuda a cuidar da sua saúde", "Help Cure — Ayuda a cuidar tu salud", "Help Cure — Helps you take care of your health")
    b = f'''
<div class="hero hv">
  <div class="wrap">
   <div class="hv-txt">
    {T("Saúde monitorada, todos os dias", "Salud monitoreada, todos los días", "Health monitored, every day", "span", "eyebrow")}
    {T("Cada paciente comparado <em>com ele mesmo</em>.", "Cada paciente comparado <em>consigo mismo</em>.", "Every patient compared <em>with themselves</em>.", "h1", raw=True)}
    {T("O Help Cure acompanha sinais vitais, medicamentos e histórico de cada pessoa e avisa quem cuida quando algo foge do padrão dela — não de uma média.", "Help Cure acompaña signos vitales, medicamentos e historial de cada persona y avisa a quien cuida cuando algo se aleja de su propio patrón — no de un promedio.", "Help Cure tracks each person’s vital signs, medication and history, and alerts caregivers when something drifts from that person’s own pattern — not from an average.", "p", "lead")}
    <div class="cta"><a class="btn primary" href="#video">{T("Assistir ao vídeo", "Ver el video", "Watch the video")}</a><a class="btn ghost" href="solucoes/">{T("Conhecer as soluções", "Conocer las soluciones", "Explore the solutions")}</a></div>
   </div>
   <div class="hv-media">
    <video autoplay muted loop playsinline preload="auto" poster="video/helpcure-anel-poster.jpg" aria-label="Animação Help Cure: anel inteligente monitora o coração e mãos digitais amparam quando o sinal sai do padrão">
     <source src="video/helpcure-anel-pulso.webm" type="video/webm">
     <source src="video/helpcure-anel-pulso-720.mp4" type="video/mp4" media="(max-width: 900px)">
     <source src="video/helpcure-anel-pulso.mp4" type="video/mp4">
    </video>
   </div>
  </div>
</div>

<section class="dark" id="video">
  <div class="wrap">
    <div class="head">
      {T("Em vídeo", "En video", "On video", "span", "eyebrow")}
      {T("Veja o Help Cure funcionando.", "Vea Help Cure en funcionamiento.", "See Help Cure in action.", "h2")}
      {T("Do pulso do paciente à central de monitoramento: a jornada completa, do consultório ao hospital, da farmácia à casa.", "Del pulso del paciente a la central de monitoreo: el recorrido completo, del consultorio al hospital, de la farmacia a la casa.", "From the patient’s wrist to the monitoring center: the full journey, from the doctor’s office to the hospital, from the pharmacy to the home.", "p", "muted")}
    </div>
    {video(pg, FULL, tabs=True)}
  </div>
</section>

<section>
  <div class="wrap split">
    <div>
      {T("O problema", "El problema", "The problem", "span", "eyebrow")}
      {T("Todo dia, milhares de pacientes precisam contar a própria história do zero.", "Cada día, miles de pacientes tienen que contar su historia desde cero.", "Every day, thousands of patients have to tell their story from scratch.", "h2")}
      {T("Exames ficam espalhados, a receita se perde, o remédio é esquecido e o sinal de alerta só aparece quando a pessoa já está no pronto-socorro.", "Los exámenes quedan dispersos, la receta se pierde, el remedio se olvida y la señal de alerta solo aparece cuando la persona ya está en urgencias.", "Test results are scattered, prescriptions get lost, doses are forgotten and the warning sign only shows up once the person is already in the emergency room.", "p", "muted", attrs=' style="margin-top:18px;font-size:18px"')}
      {T("O Help Cure junta essas informações num só lugar, acompanha o paciente entre uma consulta e outra e entrega à equipe de saúde um resumo pronto quando ela precisa.", "Help Cure reúne esa información en un solo lugar, acompaña al paciente entre una consulta y otra y entrega al equipo de salud un resumen listo cuando lo necesita.", "Help Cure brings that information together, follows the patient between appointments and gives the care team a ready summary when they need it.", "p", "muted", attrs=' style="font-size:18px"')}
    </div>
    <img src="img/paciente.webp" {pg.alt("Profissional de saúde medindo a pressão de uma paciente, com os dados no tablet", "Profesional de salud midiendo la presión de una paciente, con los datos en la tableta", "Health professional measuring a patient’s blood pressure, with the data on a tablet")} loading="lazy">
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <div class="head">
      {T("Como funciona", "Cómo funciona", "How it works", "span", "eyebrow")}
      {T("Do pulso do paciente à decisão de quem cuida.", "Del pulso del paciente a la decisión de quien cuida.", "From the patient’s wrist to the caregiver’s decision.", "h2")}
    </div>
    <div class="g g4 steps">
      <div class="step">{T("Coleta", "Captura", "Capture", "h3")}{T("Pulseira, relógio, cartão com chip ou o kit de triagem registram pressão, frequência cardíaca, oxigenação, temperatura e outros sinais. Receitas e diagnósticos entram por foto.", "Pulsera, reloj, tarjeta con chip o el kit de triaje registran presión, frecuencia cardíaca, oxigenación, temperatura y otras señales. Recetas y diagnósticos entran por foto.", "Band, watch, chip card or the triage kit record blood pressure, heart rate, oxygen, temperature and other signals. Prescriptions and diagnoses come in by photo.", "p")}</div>
      <div class="step">{T("Assinatura pessoal", "Firma personal", "Personal signature", "h3")}{T("O motor RAPP aprende o padrão de cada paciente e compara cada nova leitura com esse padrão, olhando desvio, tendência e a relação entre os sinais.", "El motor RAPP aprende el patrón de cada paciente y compara cada nueva lectura con ese patrón, mirando desvío, tendencia y la relación entre las señales.", "The RAPP engine learns each patient’s pattern and compares every new reading against it, looking at deviation, trend and how signals relate.", "p")}</div>
      <div class="step">{T("Central de monitoramento", "Central de monitoreo", "Monitoring center", "h3")}{T("Desvios viram alertas por nível de prioridade, com o histórico do paciente ao lado, para a equipe responsável decidir.", "Los desvíos se convierten en alertas por nivel de prioridad, con el historial del paciente al lado, para que el equipo responsable decida.", "Deviations become prioritized alerts, with the patient’s history alongside, for the responsible team to decide.", "p")}</div>
      <div class="step">{T("Cuidado", "Cuidado", "Care", "h3")}{T("Médico, farmácia, família e o próprio paciente recebem a informação certa, na hora certa, pelo app, pelo painel ou pelo WhatsApp.", "Médico, farmacia, familia y el propio paciente reciben la información correcta en el momento correcto, por la app, el panel o WhatsApp.", "Doctor, pharmacy, family and the patient get the right information at the right time, through the app, the dashboard or WhatsApp.", "p")}</div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head">
      {T("Soluções", "Soluciones", "Solutions", "span", "eyebrow")}
      {T("Uma plataforma, todos os pontos de cuidado.", "Una plataforma, todos los puntos de cuidado.", "One platform, every point of care.", "h2")}
      {T("Cada ponto de atendimento alimenta o mesmo histórico do paciente. Escolha uma solução para ver como ela funciona.", "Cada punto de atención alimenta el mismo historial del paciente. Elija una solución para ver cómo funciona.", "Every point of care feeds the same patient history. Pick a solution to see how it works.", "p", "muted")}
    </div>
    <div class="g g3">{sol_cards(pg)}</div>
  </div>
</section>

<section class="soft">
  <div class="wrap split rev">
    <div>
      {T("Tecnologia e segurança", "Tecnología y seguridad", "Technology and security", "span", "eyebrow")}
      {T("Dados clínicos tratados com o cuidado que exigem.", "Datos clínicos tratados con el cuidado que exigen.", "Clinical data handled with the care it demands.", "h2")}
      {T("Laudos com assinatura digital e carimbo do tempo, integração com o prontuário único público no padrão exigido e proteção de dados conforme a LGPD no Brasil e a lei de dados pessoais do Paraguai.", "Informes con firma digital y sello de tiempo, integración con el registro clínico único público en el estándar exigido y protección de datos conforme a la LGPD de Brasil y la ley de datos personales de Paraguay.", "Reports with digital signatures and timestamps, integration with the public unified health record in the required standard, and data protection under Brazil’s LGPD and Paraguay’s personal data law.", "p", "muted", attrs=' style="margin-top:16px;font-size:18px"')}
      <div class="cta"><a class="btn dark" href="tecnologia.html">{T("Ver a tecnologia", "Ver la tecnología", "See the technology")}</a></div>
    </div>
    <img src="img/central.webp" {pg.alt("Central de monitoramento Help Cure com sinais vitais em telas grandes", "Central de monitoreo Help Cure con signos vitales en pantallas grandes", "Help Cure monitoring center with vital signs on large screens")} loading="lazy">
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head">
      {T("Para quem é", "Para quién es", "Who it’s for", "span", "eyebrow")}
      {T("Quem ganha com o Help Cure.", "Quién gana con Help Cure.", "Who benefits from Help Cure.", "h2")}
    </div>
    <div class="g g3">
      <div class="card"><div class="in">{T("Pacientes e famílias", "Pacientes y familias", "Patients and families", "h3")}{T("Menos esquecimento, mais segurança e a família por perto, mesmo à distância.", "Menos olvidos, más seguridad y la familia cerca, incluso a distancia.", "Fewer missed doses, more safety and the family close by, even from afar.", "p")}</div></div>
      <div class="card"><div class="in">{T("Hospitais, clínicas e médicos", "Hospitales, clínicas y médicos", "Hospitals, clinics and doctors", "h3")}{T("O paciente chega com o histórico pronto e continua acompanhado depois da alta.", "El paciente llega con el historial listo y sigue acompañado después del alta.", "Patients arrive with their history ready and stay followed after discharge.", "p")}</div></div>
      <div class="card"><div class="in">{T("Governos e planos de saúde", "Gobiernos y planes de salud", "Governments and health plans", "h3")}{T("Prevenção no lugar de urgência: a população acompanhada todos os dias, com dados para decidir.", "Prevención en lugar de urgencia: la población acompañada todos los días, con datos para decidir.", "Prevention instead of emergencies: the population followed every day, with data to decide.", "p")}</div></div>
    </div>
    <div class="nextnav"><a class="btn line" href="para-quem.html">{T("Ver todos os públicos →", "Ver todos los públicos →", "See everyone it serves →")}</a></div>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="pilot camp">
      <img src="img/movel_fila.webp" alt="" loading="lazy">
      <div>
        {T("Help Cure Solidário", "Help Cure Solidario", "Help Cure Solidarity", "span", "eyebrow")}
        {T("Ajude a levar cuidado a quem mais precisa.", "Ayude a llevar cuidado a quien más lo necesita.", "Help bring care to those who need it most.", "h2")}
        {T("Nossa campanha financia unidades móveis com atendimento gratuito em comunidades carentes do Paraguai e do Brasil, e o desenvolvimento da plataforma. Quem apoia acompanha cada atendimento e pode receber o kit Help Cure em casa.", "Nuestra campaña financia unidades móviles con atención gratuita en comunidades vulnerables de Paraguay y Brasil, y el desarrollo de la plataforma. Quien apoya sigue cada atención y puede recibir el kit Help Cure en casa.", "Our campaign funds mobile units offering free care in underserved communities in Paraguay and Brazil, and the platform’s development. Supporters follow every visit and can receive the Help Cure kit at home.", "p")}
        <div class="cta"><a class="btn primary" href="solidario.html">{T("Conhecer a campanha", "Conocer la campaña", "See the campaign")}</a><a class="btn ghost" href="solidario.html#apoiar">{T("Quero apoiar", "Quiero apoyar", "I want to support")}</a></div>
      </div>
    </div>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="pilot">
      <img src="img/piloto.webp" alt="" loading="lazy">
      <div>
        {T("Próximo passo", "Próximo paso", "Next step", "span", "eyebrow")}
        {T("Piloto no Paraguai e no Brasil.", "Piloto en Paraguay y Brasil.", "Pilot in Paraguay and Brazil.", "h2")}
        {T("Estamos começando com um grupo de pacientes reais: receita por foto, lembretes pelo app e pelo WhatsApp e acompanhamento por uma central de monitoramento.", "Empezamos con un grupo de pacientes reales: receta por foto, recordatorios por la app y por WhatsApp y seguimiento desde una central de monitoreo.", "We are starting with a group of real patients: prescriptions by photo, reminders through the app and WhatsApp, and follow-up from a monitoring center.", "p")}
        <div class="cta"><a class="btn primary" href="app/">{T("Experimentar o app", "Probar la app", "Try the app")}</a><a class="btn ghost" href="/investidores/" data-inv="/investidores/">{T("Área do investidor", "Área del inversionista", "Investor area")}</a></div>
      </div>
    </div>
  </div>
</section>
'''
    shell(pg, "index.html", title, b, "Help Cure: monitoramento contínuo de saúde que compara cada paciente com ele mesmo. Soluções para pacientes, hospitais, farmácias, home care, célula de atendimento e unidade móvel.")


# ------------------------------------------------------------------ SOLUTIONS INDEX
def sol_index():
    pg = Page(1)
    T = pg.t
    title = pg.title("Soluções — Help Cure", "Soluciones — Help Cure", "Solutions — Help Cure")
    b = f'''
<div class="hero sub">
  <img src="../img/celula_universidade.webp" alt="">
  <div class="wrap">
    {T("Soluções", "Soluciones", "Solutions", "span", "eyebrow")}
    {T("O mesmo histórico em todos os pontos de cuidado.", "El mismo historial en todos los puntos de cuidado.", "The same history at every point of care.", "h1")}
    {T("Seis formas de levar o Help Cure até o paciente — do celular dele ao caminhão que chega aonde a estrada termina.", "Seis formas de llevar Help Cure hasta el paciente — desde su celular hasta el camión que llega adonde termina la ruta.", "Six ways to bring Help Cure to the patient — from their phone to the truck that reaches where the road ends.", "p", "lead")}
  </div>
</div>
<section>
  <div class="wrap">
    <div class="g g3">{sol_cards(pg)}</div>
    <div class="note">{T("Todas as soluções usam o mesmo motor (RAPP), a mesma central de monitoramento e o mesmo histórico do paciente. Um dado registrado na farmácia aparece para o médico no hospital.", "Todas las soluciones usan el mismo motor (RAPP), la misma central de monitoreo y el mismo historial del paciente. Un dato registrado en la farmacia aparece para el médico en el hospital.", "Every solution uses the same engine (RAPP), the same monitoring center and the same patient history. Data recorded at the pharmacy shows up for the doctor at the hospital.", "p")}</div>
  </div>
</section>
'''
    shell(pg, "solucoes/index.html", title, b, "As soluções Help Cure: paciente, hospital, farmácia, home care, célula de atendimento e unidade móvel.")


def sol_page(slug, d):
    pg = Page(1)
    T = pg.t
    name = [x for x in SOLS if x[0] == slug][0]
    title = pg.title(name[1] + " — Help Cure", name[2] + " — Help Cure", name[3] + " — Help Cure")
    vid = ""
    if slug in SHORT:
        vid = f'''<section class="dark"><div class="wrap"><div class="head">{T("Em vídeo", "En video", "On video", "span", "eyebrow")}{T(*d["vt"], tag="h2")}</div>{video(pg, SHORT[slug])}</div></section>'''
    steps = "".join('<div class="step">%s%s</div>' % (T(*s[0], tag="h3"), T(*s[1], tag="p")) for s in d["steps"])
    gal = "".join('<figure><img src="../img/%s.webp" %s loading="lazy"><figcaption>%s</figcaption></figure>' % (g[0], pg.alt(*g[1]), T(*g[1])) for g in d["gallery"])
    whos = "".join('<div class="card"><div class="in">%s%s</div></div>' % (T(*w[0], tag="h3"), T(*w[1], tag="p")) for w in d["who"])
    b = f'''
<div class="hero sub">
  <img src="../img/{d["hero"]}.webp" alt="">
  <div class="wrap">
    <p class="crumb"><a href="./">{T("Soluções", "Soluciones", "Solutions")}</a> / {T(name[1], name[2], name[3])}</p>
    {T(*d["h1"], tag="h1")}
    {T(*d["lead"], tag="p", cls="lead")}
  </div>
</div>
{vid}
<section>
  <div class="wrap">
    <div class="head">{T("Como funciona", "Cómo funciona", "How it works", "span", "eyebrow")}{T(*d["how"], tag="h2")}</div>
    <div class="g g{min(len(d["steps"]), 4)} steps">{steps}</div>
  </div>
</section>
<section class="soft">
  <div class="wrap">
    <div class="head">{T("Recursos", "Recursos", "Features", "span", "eyebrow")}{T(*d["ft"], tag="h2")}</div>
    {feats(pg, d["feats"])}
    <div class="gallery">{gal}</div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="head">{T("Para quem", "Para quién", "Who it’s for", "span", "eyebrow")}{T(*d["wt"], tag="h2")}</div>
    <div class="g g3">{whos}</div>
    {('<div class="note">%s</div>' % T(*d["note"], tag="p")) if d.get("note") else ""}
  </div>
</section>
<section class="soft">
  <div class="wrap">
    <div class="head">{T("Outras soluções", "Otras soluciones", "Other solutions", "span", "eyebrow")}{T("Tudo ligado ao mesmo histórico.", "Todo conectado al mismo historial.", "All connected to the same history.", "h2")}</div>
    <div class="g g3">{sol_cards(pg, skip=slug)}</div>
  </div>
</section>
'''
    shell(pg, "solucoes/%s.html" % slug, title, b, d["lead"][0])


def S(pt, es, en):
    return (pt, es, en)


SOLDATA = {
 "paciente": dict(
  hero="acompanhamento",
  h1=S("O cuidado que cabe no bolso do paciente.", "El cuidado que cabe en el bolsillo del paciente.", "Care that fits in the patient’s pocket."),
  lead=S("App e WhatsApp para lembrar os remédios, guardar o histórico e entregar um resumo de emergência quando o paciente não puder falar por si.", "App y WhatsApp para recordar los medicamentos, guardar el historial y entregar un resumen de emergencia cuando el paciente no pueda hablar por sí mismo.", "App and WhatsApp to remember medication, keep the history and hand over an emergency summary when the patient can’t speak for themselves."),
  vt=S("A jornada do paciente.", "El recorrido del paciente.", "The patient’s journey."),
  how=S("Da receita ao lembrete, sem digitar nada.", "De la receta al recordatorio, sin escribir nada.", "From prescription to reminder, without typing a thing."),
  steps=[(S("Foto da receita", "Foto de la receta", "Prescription photo"), S("O paciente fotografa a receita ou o diagnóstico pelo app ou envia pelo WhatsApp.", "El paciente fotografía la receta o el diagnóstico con la app o la envía por WhatsApp.", "The patient photographs the prescription or diagnosis in the app or sends it by WhatsApp.")),
         (S("Leitura e confirmação", "Lectura y confirmación", "Reading and confirmation"), S("A inteligência artificial lê medicamentos, doses e horários; o paciente confere e confirma a compra.", "La inteligencia artificial lee medicamentos, dosis y horarios; el paciente revisa y confirma la compra.", "AI reads medication, doses and times; the patient checks and confirms the purchase.")),
         (S("Lembretes", "Recordatorios", "Reminders"), S("Na hora de cada dose chega um lembrete com os botões “Tomei”, “Adiar” e “Não vou tomar”.", "A la hora de cada dosis llega un recordatorio con los botones “Tomé”, “Posponer” y “No la tomaré”.", "At each dose time a reminder arrives with “Taken”, “Snooze” and “Skip” buttons.")),
         (S("Acompanhamento", "Seguimiento", "Follow-up"), S("A adesão e os sinais do relógio ou da pulseira chegam à central, que avisa a família e o médico quando algo foge do padrão.", "La adherencia y las señales del reloj o la pulsera llegan a la central, que avisa a la familia y al médico cuando algo se sale del patrón.", "Adherence and signals from the watch or band reach the center, which alerts family and doctor when something drifts.")) ],
  ft=S("O que o paciente tem nas mãos.", "Lo que el paciente tiene en sus manos.", "What the patient gets."),
  feats=[(("Resumo de emergência", "QR code com medicamentos em uso, alergias, doenças e últimos diagnósticos para a equipe que atender."), ("Resumen de emergencia", "Código QR con medicamentos en uso, alergias, enfermedades y últimos diagnósticos para el equipo que atienda."), ("Emergency summary", "QR code with current medication, allergies, conditions and latest diagnoses for whoever provides care.")),
         (("Relógio e pulseira", "Leitura automática de batimentos, pressão, oxigenação e temperatura de wearables compatíveis."), ("Reloj y pulsera", "Lectura automática de pulso, presión, oxigenación y temperatura de wearables compatibles."), ("Watch and band", "Automatic heart rate, blood pressure, oxygen and temperature from compatible wearables.")),
         (("Cartão com chip", "Para quem não tem smartwatch: um cartão de baixo custo identifica o paciente no ponto de atendimento."), ("Tarjeta con chip", "Para quien no tiene reloj inteligente: una tarjeta de bajo costo identifica al paciente en el punto de atención."), ("Chip card", "For those without a smartwatch: a low-cost card identifies the patient at the point of care.")),
         (("WhatsApp ou app", "O paciente escolhe o canal. Funciona em português e espanhol."), ("WhatsApp o app", "El paciente elige el canal. Funciona en portugués y español."), ("WhatsApp or app", "The patient picks the channel. Works in Portuguese and Spanish.")),
         (("Família por perto", "Quem cuida recebe avisos de doses perdidas e alertas da central."), ("Familia cerca", "Quien cuida recibe avisos de dosis olvidadas y alertas de la central."), ("Family nearby", "Caregivers get notices of missed doses and alerts from the center.")),
         (("Histórico único", "Exames, receitas e medições no mesmo lugar, prontos para a próxima consulta."), ("Historial único", "Exámenes, recetas y mediciones en el mismo lugar, listos para la próxima consulta."), ("One history", "Tests, prescriptions and readings in one place, ready for the next appointment."))],
  gallery=[("emergencia", S("Resumo de emergência no tablet da equipe", "Resumen de emergencia en la tableta del equipo", "Emergency summary on the team’s tablet")),
           ("consulta_celular", S("Receita digital no histórico", "Receta digital en el historial", "Digital prescription in the history")),
           ("totem", S("Agenda e lembretes no celular", "Agenda y recordatorios en el celular", "Schedule and reminders on the phone"))],
  wt=S("Para quem toma remédio todo dia — e para quem cuida.", "Para quien toma medicamentos todos los días — y para quien cuida.", "For people on daily medication — and those who care for them."),
  who=[(S("Doenças crônicas", "Enfermedades crónicas", "Chronic conditions"), S("Hipertensão, diabetes e outros tratamentos contínuos.", "Hipertensión, diabetes y otros tratamientos continuos.", "Hypertension, diabetes and other ongoing treatments.")),
       (S("Idosos", "Adultos mayores", "Older adults"), S("Mais autonomia em casa, com a família informada.", "Más autonomía en casa, con la familia informada.", "More independence at home, with the family informed.")),
       (S("Cuidadores", "Cuidadores", "Caregivers"), S("Filhos e cuidadores acompanham sem precisar ligar a toda hora.", "Hijos y cuidadores acompañan sin tener que llamar a cada rato.", "Children and caregivers follow along without calling all the time."))],
  note=S("Experimente o app em modo demonstração: abra no celular e use “Adicionar à tela inicial” para instalar.", "Pruebe la app en modo demostración: ábrala en el celular y use “Agregar a la pantalla de inicio” para instalarla.", "Try the app in demo mode: open it on your phone and use “Add to Home Screen” to install it.")),
 "hospital": dict(
  hero="hospital",
  h1=S("O paciente chega com a história pronta.", "El paciente llega con su historia lista.", "Patients arrive with their story ready."),
  lead=S("Da recepção à alta: a pulseira identifica o paciente, os sinais entram direto no sistema e a família acompanha a internação.", "De la recepción al alta: la pulsera identifica al paciente, las señales entran directo al sistema y la familia acompaña la internación.", "From reception to discharge: the band identifies the patient, signals go straight into the system and the family follows the stay."),
  vt=S("Um dia no hospital com o Help Cure.", "Un día en el hospital con Help Cure.", "A day at the hospital with Help Cure."),
  how=S("Menos papel, menos redigitação, mais tempo com o paciente.", "Menos papel, menos redigitación, más tiempo con el paciente.", "Less paper, less re-typing, more time with the patient."),
  steps=[(S("Recepção", "Recepción", "Reception"), S("A leitura da pulseira ou do cartão abre o resumo do paciente: medicamentos, alergias e últimos diagnósticos.", "La lectura de la pulsera o la tarjeta abre el resumen del paciente: medicamentos, alergias y últimos diagnósticos.", "Scanning the band or card opens the patient summary: medication, allergies and latest diagnoses.")),
         (S("Triagem", "Triaje", "Triage"), S("Pressão, temperatura e oxigenação entram no sistema na hora, sem papel.", "Presión, temperatura y oxigenación entran al sistema al instante, sin papel.", "Blood pressure, temperature and oxygen enter the system instantly, paperless.")),
         (S("Internação", "Internación", "Admission"), S("O posto de enfermagem vê medicamentos e medições de cada leito; a enfermagem registra doses pelo tablet.", "El puesto de enfermería ve medicamentos y mediciones de cada cama; enfermería registra dosis en la tableta.", "The nursing station sees medication and readings for each bed; nurses log doses on a tablet.")),
         (S("Alta e continuidade", "Alta y continuidad", "Discharge and continuity"), S("O paciente vai para casa monitorado, e o médico recebe a indicação de estabilidade.", "El paciente va a casa monitoreado y el médico recibe la indicación de estabilidad.", "The patient goes home monitored, and the doctor receives a stability indicator."))],
  ft=S("O que muda na rotina da equipe.", "Lo que cambia en la rutina del equipo.", "What changes for the team."),
  feats=[(("Resumo de emergência", "Histórico essencial na tela em segundos, mesmo quando o paciente não pode falar."), ("Resumen de emergencia", "Historial esencial en pantalla en segundos, incluso cuando el paciente no puede hablar."), ("Emergency summary", "Essential history on screen in seconds, even when the patient can’t speak.")),
         (("Painel do posto", "Sinais e medicamentos de todos os leitos do andar, com alertas por prioridade."), ("Panel del puesto", "Señales y medicamentos de todas las camas del piso, con alertas por prioridad."), ("Station dashboard", "Signals and medication for every bed on the floor, with prioritized alerts.")),
         (("Família informada", "Quem cuida recebe atualizações da internação, sem ligar para o hospital."), ("Familia informada", "Quien cuida recibe novedades de la internación, sin llamar al hospital."), ("Family informed", "Caregivers get updates on the stay without calling the hospital.")),
         (("Visita médica com dados", "O médico vê a evolução comparada com o padrão do próprio paciente."), ("Visita médica con datos", "El médico ve la evolución comparada con el patrón del propio paciente."), ("Rounds with data", "The doctor sees progress compared with the patient’s own pattern.")),
         (("Integração", "API para enviar o prontuário ao sistema do hospital e ao prontuário único público."), ("Integración", "API para enviar la historia clínica al sistema del hospital y al registro único público."), ("Integration", "API to send the record to the hospital system and the public unified record.")),
         (("Laudos assinados", "Assinatura digital com carimbo do tempo nos documentos clínicos."), ("Informes firmados", "Firma digital con sello de tiempo en los documentos clínicos."), ("Signed reports", "Digital signature with timestamp on clinical documents."))],
  gallery=[("emergencia", S("Resumo de emergência na recepção", "Resumen de emergencia en la recepción", "Emergency summary at reception")),
           ("familia", S("Visita médica com o histórico na mão", "Visita médica con el historial a mano", "Rounds with the history at hand")),
           ("central", S("Central de monitoramento", "Central de monitoreo", "Monitoring center"))],
  wt=S("Para quem atende.", "Para quien atiende.", "For care providers."),
  who=[(S("Hospitais públicos e privados", "Hospitales públicos y privados", "Public and private hospitals"), S("Pronto-socorro, internação e alta com o mesmo histórico.", "Urgencias, internación y alta con el mismo historial.", "Emergency, admission and discharge with one history.")),
       (S("Clínicas e consultórios", "Clínicas y consultorios", "Clinics and practices"), S("O paciente chega com os dados entre uma consulta e outra.", "El paciente llega con los datos entre una consulta y otra.", "Patients arrive with data from between appointments.")),
       (S("Equipes de enfermagem", "Equipos de enfermería", "Nursing teams"), S("Registro de doses e sinais no tablet, sem redigitar.", "Registro de dosis y señales en la tableta, sin redigitar.", "Dose and signal logging on a tablet, no re-typing."))]),
 "farmacia": dict(
  hero="farmacia",
  h1=S("A farmácia como ponto de cuidado.", "La farmacia como punto de cuidado.", "The pharmacy as a point of care."),
  lead=S("Perto do paciente todos os dias: confere a receita, registra a dispensação, mede a pressão e ajuda o tratamento a não parar.", "Cerca del paciente todos los días: verifica la receta, registra la dispensación, mide la presión y ayuda a que el tratamiento no se interrumpa.", "Close to the patient every day: checks the prescription, records dispensing, measures blood pressure and helps keep treatment on track."),
  how=S("Receita, compra e acompanhamento no mesmo histórico.", "Receta, compra y seguimiento en el mismo historial.", "Prescription, purchase and follow-up in one history."),
  steps=[(S("Receita digital", "Receta digital", "Digital prescription"), S("O farmacêutico vê a receita do paciente no Help Cure.", "El farmacéutico ve la receta del paciente en Help Cure.", "The pharmacist sees the patient’s prescription in Help Cure.")),
         (S("Dispensação registrada", "Dispensación registrada", "Dispensing recorded"), S("A compra é confirmada e os lembretes de dose começam.", "La compra se confirma y comienzan los recordatorios de dosis.", "The purchase is confirmed and dose reminders begin.")),
         (S("Medição no balcão", "Medición en el mostrador", "Counter check"), S("Pressão e outros sinais medidos na farmácia entram no histórico.", "Presión y otras señales medidas en la farmacia entran al historial.", "Blood pressure and other signals measured at the pharmacy join the history.")),
         (S("Reposição", "Reposición", "Refill"), S("Quando o remédio está acabando, a farmácia pode oferecer a reposição.", "Cuando el remedio se está terminando, la farmacia puede ofrecer la reposición.", "When medication is running out, the pharmacy can offer a refill."))],
  ft=S("O que a farmácia ganha.", "Lo que gana la farmacia.", "What the pharmacy gains."),
  feats=[(("Adesão ao tratamento", "Lembretes e confirmação de doses reduzem o abandono do remédio."), ("Adherencia al tratamiento", "Recordatorios y confirmación de dosis reducen el abandono del medicamento."), ("Treatment adherence", "Reminders and dose confirmation reduce drop-off.")),
         (("Fidelização", "O paciente volta à farmácia que acompanha o tratamento dele."), ("Fidelización", "El paciente vuelve a la farmacia que acompaña su tratamiento."), ("Loyalty", "Patients return to the pharmacy that follows their treatment.")),
         (("Célula na farmácia", "A célula de atendimento pode ser instalada dentro da loja, com triagem e teleconsulta."), ("Célula en la farmacia", "La célula de atención puede instalarse dentro del local, con triaje y teleconsulta."), ("Cell in the pharmacy", "The care cell can be installed in-store, with triage and teleconsultation.")),
         (("Mesmo histórico", "O que é registrado na farmácia aparece para o médico e o hospital."), ("Mismo historial", "Lo registrado en la farmacia aparece para el médico y el hospital."), ("Same history", "What is recorded at the pharmacy shows up for the doctor and hospital."))],
  gallery=[("celula_farmacia", S("Célula de atendimento dentro da farmácia", "Célula de atención dentro de la farmacia", "Care cell inside the pharmacy")),
           ("consulta_celular", S("Receita digital", "Receta digital", "Digital prescription")),
           ("acompanhamento", S("Dose registrada em casa", "Dosis registrada en casa", "Dose logged at home"))],
  wt=S("Para quem dispensa e orienta.", "Para quien dispensa y orienta.", "For those who dispense and advise."),
  who=[(S("Redes de farmácias", "Cadenas de farmacias", "Pharmacy chains"), S("Serviço de cuidado como diferencial em todas as lojas.", "Servicio de cuidado como diferencial en todas las tiendas.", "Care services as a differentiator across stores.")),
       (S("Farmácias de bairro", "Farmacias de barrio", "Neighborhood pharmacies"), S("Relação próxima com o paciente, agora com dados.", "Relación cercana con el paciente, ahora con datos.", "A close patient relationship, now with data.")),
       (S("Farmacêuticos", "Farmacéuticos", "Pharmacists"), S("Orientação baseada no histórico e na adesão real.", "Orientación basada en el historial y la adherencia real.", "Guidance based on history and real adherence."))]),
 "homecare": dict(
  hero="estavel",
  h1=S("O cuidado não termina na alta.", "El cuidado no termina con el alta.", "Care doesn’t end at discharge."),
  lead=S("Em casa, o paciente continua monitorado. O médico recebe as medições com a indicação de estabilidade e a família fica tranquila.", "En casa, el paciente sigue monitoreado. El médico recibe las mediciones con la indicación de estabilidad y la familia queda tranquila.", "At home, the patient stays monitored. The doctor receives readings with a stability indicator, and the family has peace of mind."),
  how=S("Monitoramento contínuo, sem sair de casa.", "Monitoreo continuo, sin salir de casa.", "Continuous monitoring, without leaving home."),
  steps=[(S("Kit em casa", "Kit en casa", "Home kit"), S("Um celular Android como base, pulseira ou relógio e, se quiser, um assistente de voz para os lembretes.", "Un celular Android como base, pulsera o reloj y, si se desea, un asistente de voz para los recordatorios.", "An Android phone as a hub, a band or watch and, optionally, a voice assistant for reminders.")),
         (S("Leituras diárias", "Lecturas diarias", "Daily readings"), S("Os sinais vão para a central sem o paciente precisar digitar.", "Las señales van a la central sin que el paciente tenga que escribir.", "Signals go to the center without the patient typing anything.")),
         (S("Alerta e ação", "Alerta y acción", "Alert and action"), S("Se algo foge do padrão, a central avisa a equipe de home care, o médico e a família.", "Si algo se sale del patrón, la central avisa al equipo de atención domiciliaria, al médico y a la familia.", "If something drifts, the center alerts the home care team, doctor and family."))],
  ft=S("O que muda depois da alta.", "Lo que cambia después del alta.", "What changes after discharge."),
  feats=[(("Estabilidade visível", "O médico vê há quanto tempo o paciente está estável, sem visita."), ("Estabilidad visible", "El médico ve hace cuánto tiempo el paciente está estable, sin visita."), ("Visible stability", "The doctor sees how long the patient has been stable, without a visit.")),
         (("Menos reinternação", "Sinais de piora aparecem cedo, enquanto ainda dá para agir em casa."), ("Menos reinternación", "Las señales de empeoramiento aparecen temprano, cuando todavía se puede actuar en casa."), ("Fewer readmissions", "Signs of decline appear early, while action at home is still possible.")),
         (("Lembretes por voz", "Para quem tem dificuldade com o celular, os lembretes podem ser falados."), ("Recordatorios por voz", "Para quien tiene dificultad con el celular, los recordatorios pueden ser hablados."), ("Voice reminders", "For those who struggle with phones, reminders can be spoken.")),
         (("Equipe de home care", "Visitas planejadas pelos dados, não só pelo calendário."), ("Equipo domiciliario", "Visitas planificadas por los datos, no solo por el calendario."), ("Home care team", "Visits planned by data, not just by the calendar."))],
  gallery=[("acompanhamento", S("Lembrete por voz na cozinha", "Recordatorio por voz en la cocina", "Voice reminder in the kitchen")),
           ("estavel", S("Monitoramento em casa", "Monitoreo en casa", "Monitoring at home")),
           ("casa", S("A família por perto", "La familia cerca", "Family close by"))],
  wt=S("Para quem cuida em casa.", "Para quien cuida en casa.", "For those caring at home."),
  who=[(S("Empresas de home care", "Empresas de atención domiciliaria", "Home care companies"), S("Mais pacientes acompanhados com a mesma equipe.", "Más pacientes acompañados con el mismo equipo.", "More patients followed with the same team.")),
       (S("Hospitais", "Hospitales", "Hospitals"), S("Alta com segurança e continuidade do cuidado.", "Alta con seguridad y continuidad del cuidado.", "Safe discharge and continuity of care.")),
       (S("Famílias", "Familias", "Families"), S("Tranquilidade para quem mora longe.", "Tranquilidad para quien vive lejos.", "Peace of mind for those who live far away."))]),
 "celula": dict(
  hero="celula",
  h1=S("Uma sala de cuidado onde as pessoas estão.", "Una sala de cuidado donde están las personas.", "A care room where people already are."),
  lead=S("A célula Help Cure é uma sala de 3 × 3 m, desmontável, com totem de triagem e teleconsulta — para universidades, igrejas, indústrias, farmácias, órgãos públicos e academias.", "La célula Help Cure es una sala de 3 × 3 m, desmontable, con tótem de triaje y teleconsulta — para universidades, iglesias, industrias, farmacias, organismos públicos y gimnasios.", "The Help Cure cell is a demountable 3 × 3 m room with a triage kiosk and teleconsultation — for universities, churches, industry, pharmacies, public agencies and gyms."),
  vt=S("A célula em funcionamento.", "La célula en funcionamiento.", "The cell at work."),
  how=S("Triagem e consulta em poucos minutos.", "Triaje y consulta en pocos minutos.", "Triage and consultation in minutes."),
  steps=[(S("Check-in", "Registro", "Check-in"), S("Pulseira, cartão ou celular identificam o paciente na entrada.", "Pulsera, tarjeta o celular identifican al paciente en la entrada.", "Band, card or phone identify the patient at the door.")),
         (S("Triagem no totem", "Triaje en el tótem", "Kiosk triage"), S("Altura, peso, pressão e outros sinais medidos no totem e enviados na hora.", "Altura, peso, presión y otras señales medidas en el tótem y enviadas al instante.", "Height, weight, blood pressure and other signals measured at the kiosk and sent instantly.")),
         (S("Teleconsulta", "Teleconsulta", "Teleconsultation"), S("O médico atende pela tela grande, já com os dados da triagem; o vidro fica fosco durante a consulta.", "El médico atiende por la pantalla grande, ya con los datos del triaje; el vidrio se vuelve opaco durante la consulta.", "The doctor sees the patient on the big screen with triage data in hand; the glass turns frosted during the consultation.")),
         (S("Acompanhamento", "Seguimiento", "Follow-up"), S("Receita e plano de cuidado vão para o histórico e para o app do paciente.", "Receta y plan de cuidado van al historial y a la app del paciente.", "Prescription and care plan go to the history and the patient app."))],
  ft=S("Como é a célula.", "Cómo es la célula.", "What the cell is like."),
  feats=[(("3 × 3 m, 2,40 m de altura", "Estrutura desmontável em perfis de alumínio, montada em pouco espaço."), ("3 × 3 m, 2,40 m de altura", "Estructura desmontable en perfiles de aluminio, montada en poco espacio."), ("3 × 3 m, 2.40 m high", "Demountable aluminum-profile structure that fits a small footprint.")),
         (("Vidro inteligente", "As paredes de vidro ficam foscas durante a consulta, garantindo privacidade."), ("Vidrio inteligente", "Las paredes de vidrio se vuelven opacas durante la consulta, garantizando privacidad."), ("Smart glass", "Glass walls turn frosted during the consultation for privacy.")),
         (("Acessível", "Entrada de 1 m para cadeira de rodas e piso elevado com ar-condicionado."), ("Accesible", "Entrada de 1 m para silla de ruedas y piso elevado con aire acondicionado."), ("Accessible", "1 m wheelchair entrance and raised floor with air conditioning.")),
         (("Equipada", "Maca, mesa, duas cadeiras, TV grande para teleconsulta e totem de triagem."), ("Equipada", "Camilla, mesa, dos sillas, TV grande para teleconsulta y tótem de triaje."), ("Equipped", "Exam bed, desk, two chairs, large teleconsultation screen and triage kiosk.")),
         (("Em qualquer lugar", "Hospital, farmácia, indústria, universidade, igreja, academia ou órgão público."), ("En cualquier lugar", "Hospital, farmacia, industria, universidad, iglesia, gimnasio u organismo público."), ("Anywhere", "Hospital, pharmacy, factory, university, church, gym or public office.")),
         (("Ligada à central", "Tudo o que acontece na célula alimenta o histórico do paciente."), ("Conectada a la central", "Todo lo que ocurre en la célula alimenta el historial del paciente."), ("Connected to the center", "Everything that happens in the cell feeds the patient’s history."))],
  gallery=[("celula_universidade", S("Na universidade", "En la universidad", "At a university")),
           ("celula_industria", S("Na indústria", "En la industria", "In industry")),
           ("celula_farmacia", S("Na farmácia", "En la farmacia", "In a pharmacy"))],
  wt=S("Para quem quer levar saúde até as pessoas.", "Para quien quiere llevar salud a las personas.", "For those bringing healthcare to people."),
  who=[(S("Empresas e indústrias", "Empresas e industrias", "Companies and industry"), S("Check-up na entrada do turno e saúde ocupacional com dados.", "Chequeo al inicio del turno y salud ocupacional con datos.", "Shift-start check-ups and data-driven occupational health.")),
       (S("Universidades e igrejas", "Universidades e iglesias", "Universities and churches"), S("Atendimento para a comunidade, sem deslocamento.", "Atención para la comunidad, sin desplazamientos.", "Care for the community, no travel needed.")),
       (S("Órgãos públicos e academias", "Organismos públicos y gimnasios", "Public agencies and gyms"), S("Prevenção perto de onde as pessoas já estão.", "Prevención cerca de donde las personas ya están.", "Prevention close to where people already are."))]),
 "movel": dict(
  hero="movel_toldo",
  h1=S("O cuidado chega até onde a estrada termina.", "El cuidado llega hasta donde termina la ruta.", "Care reaches where the road ends."),
  lead=S("Um caminhão 4x4 com triagem e duas cabines de teleconsulta leva médico especialista a cidades distantes — e o acompanhamento continua depois, com a pulseira.", "Un camión 4x4 con triaje y dos cabinas de teleconsulta lleva médicos especialistas a ciudades distantes — y el seguimiento continúa después, con la pulsera.", "A 4x4 truck with triage and two teleconsultation booths brings specialist doctors to remote towns — and follow-up continues afterward with the band."),
  vt=S("A unidade móvel em ação.", "La unidad móvil en acción.", "The mobile unit in action."),
  how=S("Atendimento organizado, do agendamento à pulseira.", "Atención organizada, de la agenda a la pulsera.", "Organized care, from scheduling to the band."),
  steps=[(S("Visita agendada", "Visita agendada", "Scheduled visit"), S("A data é marcada com a prefeitura e os agentes de saúde; a vaga na praça já fica reservada.", "La fecha se acuerda con la municipalidad y los agentes de salud; el lugar en la plaza queda reservado.", "The date is set with the local government and health agents; the spot in the square is reserved.")),
         (S("Fila com senha", "Fila con número", "Numbered queue"), S("Cada pessoa já tem sua senha; o painel externo mostra só o número e o destino, nunca nomes.", "Cada persona ya tiene su número; el panel externo muestra solo el número y el destino, nunca nombres.", "Everyone already has a number; the outside screen shows only the number and destination, never names.")),
         (S("Triagem e consulta", "Triaje y consulta", "Triage and consultation"), S("Pressão, oxigênio, temperatura e glicemia medidos com o kit; duas cabines atendem ao mesmo tempo.", "Presión, oxígeno, temperatura y glucemia medidos con el kit; dos cabinas atienden al mismo tiempo.", "Blood pressure, oxygen, temperature and glucose measured with the kit; two booths run in parallel.")),
         (S("Pulseira e receita", "Pulsera y receta", "Band and prescription"), S("O paciente sai com a receita e a pulseira, e o médico acompanha de longe, todos os dias.", "El paciente sale con la receta y la pulsera, y el médico acompaña a distancia, todos los días.", "The patient leaves with a prescription and a band, and the doctor follows up remotely every day."))],
  ft=S("Como é a unidade.", "Cómo es la unidad.", "What the unit is like."),
  feats=[(("Acesso para todos", "Escada com corrimão e plataforma elevatória para cadeira de rodas."), ("Acceso para todos", "Escalera con pasamanos y plataforma elevadora para silla de ruedas."), ("Access for all", "Stairs with handrails and a wheelchair lift.")),
         (("Toldo e espera", "Toldo lateral cria a área de espera na sombra."), ("Toldo y espera", "Toldo lateral crea el área de espera a la sombra."), ("Awning and waiting area", "A side awning creates a shaded waiting area.")),
         (("Duas cabines", "Separadas por vidro, cada uma com tela para o médico por vídeo."), ("Dos cabinas", "Separadas por vidrio, cada una con pantalla para el médico por video."), ("Two booths", "Separated by glass, each with a screen for the video doctor.")),
         (("Privacidade", "Painel de senhas sem nomes e vidro fosco na altura do rosto."), ("Privacidad", "Panel de números sin nombres y vidrio opaco a la altura del rostro."), ("Privacy", "A number board with no names and frosted glass at face height.")),
         (("Fora da estrada", "Caminhão 4x4 para estradas de terra e longas distâncias."), ("Fuera de ruta", "Camión 4x4 para caminos de tierra y largas distancias."), ("Off-road", "4x4 truck for dirt roads and long distances.")),
         (("Continuidade", "Depois que o caminhão parte, a pulseira continua enviando os sinais."), ("Continuidad", "Después de que el camión parte, la pulsera sigue enviando las señales."), ("Continuity", "After the truck leaves, the band keeps sending signals."))],
  gallery=[("movel_fila", S("Plataforma para cadeira de rodas", "Plataforma para silla de ruedas", "Wheelchair lift")),
           ("movel_triagem", S("Triagem com o kit Help Cure", "Triaje con el kit Help Cure", "Triage with the Help Cure kit")),
           ("movel_toldo", S("Vaga reservada na praça", "Lugar reservado en la plaza", "Reserved spot in the square"))],
  wt=S("Para quem precisa chegar longe.", "Para quien necesita llegar lejos.", "For those who need to reach far."),
  who=[(S("Governos e secretarias de saúde", "Gobiernos y secretarías de salud", "Governments and health departments"), S("Especialistas em regiões sem hospital próximo.", "Especialistas en regiones sin hospital cercano.", "Specialists in regions without a nearby hospital.")),
       (S("Planos de saúde", "Planes de salud", "Health plans"), S("Cobertura real para beneficiários do interior.", "Cobertura real para beneficiarios del interior.", "Real coverage for members in rural areas.")),
       (S("Comunidades rurais", "Comunidades rurales", "Rural communities"), S("Consulta, receita e acompanhamento sem viajar horas.", "Consulta, receta y seguimiento sin viajar horas.", "Consultation, prescription and follow-up without hours of travel."))],
  note=S("Primeiro cenário: o Chaco paraguaio, onde o hospital mais próximo pode estar a horas de estrada.", "Primer escenario: el Chaco paraguayo, donde el hospital más cercano puede estar a horas de ruta.", "First scenario: the Paraguayan Chaco, where the nearest hospital can be hours away by road.")),
}


# ------------------------------------------------------------------ PARA QUEM
def para_quem():
    pg = Page(0)
    T = pg.t
    title = pg.title("Para quem é — Help Cure", "Para quién es — Help Cure", "Who it’s for — Help Cure")
    blocks = [
        ("acompanhamento", "solucoes/paciente.html", S("Pacientes e famílias", "Pacientes y familias", "Patients and families"),
         S("Menos esquecimento, mais segurança.", "Menos olvidos, más seguridad.", "Fewer missed doses, more safety."),
         S("Lembretes de remédio no app ou no WhatsApp, histórico sempre à mão e um resumo de emergência no celular. A família recebe avisos e acompanha de longe.", "Recordatorios de medicamentos en la app o en WhatsApp, historial siempre a mano y un resumen de emergencia en el celular. La familia recibe avisos y acompaña a distancia.", "Medication reminders in the app or on WhatsApp, history always at hand and an emergency summary on the phone. Family gets notices and follows from afar.")),
        ("hospital", "solucoes/hospital.html", S("Hospitais, clínicas e médicos", "Hospitales, clínicas y médicos", "Hospitals, clinics and doctors"),
         S("O paciente chega com a história pronta.", "El paciente llega con su historia lista.", "Patients arrive with their story ready."),
         S("Resumo de emergência na recepção, sinais vitais direto no sistema, família informada durante a internação e acompanhamento depois da alta.", "Resumen de emergencia en la recepción, signos vitales directo al sistema, familia informada durante la internación y seguimiento después del alta.", "Emergency summary at reception, vital signs straight into the system, family informed during the stay and follow-up after discharge.")),
        ("farmacia", "solucoes/farmacia.html", S("Farmácias", "Farmacias", "Pharmacies"),
         S("Um ponto de cuidado no caminho do paciente.", "Un punto de cuidado en el camino del paciente.", "A care point on the patient’s path."),
         S("Receita digital, dispensação registrada, medição no balcão e apoio à adesão. A célula de atendimento pode ficar dentro da loja.", "Receta digital, dispensación registrada, medición en el mostrador y apoyo a la adherencia. La célula de atención puede estar dentro del local.", "Digital prescriptions, recorded dispensing, counter checks and adherence support. The care cell can sit inside the store.")),
        ("central", None, S("Planos de saúde e operadoras", "Planes de salud y aseguradoras", "Health plans and insurers"),
         S("Prevenir em vez de só pagar a conta.", "Prevenir en lugar de solo pagar la cuenta.", "Prevent instead of just paying the bill."),
         S("Beneficiários acompanhados todos os dias, adesão ao tratamento medida e sinais de piora identificados antes da internação.", "Beneficiarios acompañados todos los días, adherencia al tratamiento medida y señales de empeoramiento identificadas antes de la internación.", "Members followed every day, treatment adherence measured and signs of decline spotted before hospitalization.")),
        ("movel_toldo", "solucoes/movel.html", S("Governos e saúde pública", "Gobiernos y salud pública", "Governments and public health"),
         S("A população acompanhada, com dados em tempo real.", "La población acompañada, con datos en tiempo real.", "The population followed, with real-time data."),
         S("Células em órgãos públicos, unidades móveis para regiões distantes e integração com o prontuário único público, no padrão exigido.", "Células en organismos públicos, unidades móviles para regiones distantes e integración con el registro clínico único público, en el estándar exigido.", "Cells in public offices, mobile units for remote regions and integration with the public unified record in the required standard.")),
        ("celula_industria", "solucoes/celula.html", S("Empresas, universidades e comunidades", "Empresas, universidades y comunidades", "Companies, universities and communities"),
         S("Saúde onde as pessoas já estão.", "Salud donde las personas ya están.", "Healthcare where people already are."),
         S("Check-up na entrada do turno, atendimento para alunos e fiéis, e prevenção em academias — com a célula Help Cure.", "Chequeo al inicio del turno, atención para alumnos y fieles, y prevención en gimnasios — con la célula Help Cure.", "Shift-start check-ups, care for students and congregations, and prevention in gyms — with the Help Cure cell.")),
    ]
    out = []
    for i, (img, href, h, t2, p) in enumerate(blocks):
        link = '<div class="cta"><a class="btn dark" href="%s">%s</a></div>' % (href, T("Ver a solução", "Ver la solución", "See the solution")) if href else ''
        out.append(f'''<section class="{'soft' if i % 2 else ''}"><div class="wrap split{' rev' if i % 2 else ''}"><div>{T(*h, tag="span", cls="eyebrow")}{T(*t2, tag="h2")}{T(*p, tag="p", cls="muted", attrs=' style="margin-top:16px;font-size:18px"')}{link}</div><img src="img/{img}.webp" alt="" loading="lazy"></div></section>''')
    b = f'''
<div class="hero sub">
  <img src="img/familia.webp" alt="">
  <div class="wrap">
    {T("Para quem é", "Para quién es", "Who it’s for", "span", "eyebrow")}
    {T("Cada pessoa da cadeia de cuidado ganha com o mesmo histórico.", "Cada persona de la cadena de cuidado gana con el mismo historial.", "Everyone in the chain of care gains from one shared history.", "h1")}
    {T("Do paciente ao governo, todos olham para os mesmos dados — cada um com o acesso que precisa.", "Del paciente al gobierno, todos miran los mismos datos — cada uno con el acceso que necesita.", "From patient to government, everyone sees the same data — each with the access they need.", "p", "lead")}
  </div>
</div>
{"".join(out)}
'''
    shell(pg, "para-quem.html", title, b, "Para quem é o Help Cure: pacientes, famílias, hospitais, farmácias, planos de saúde, governos e empresas.")


# ------------------------------------------------------------------ TECNOLOGIA
def tecnologia():
    pg = Page(0)
    T = pg.t
    title = pg.title("Tecnologia e segurança — Help Cure", "Tecnología y seguridad — Help Cure", "Technology and security — Help Cure")
    cards = [
        (S("Captura de sinais", "Captura de señales", "Signal capture"), S("Relógios e pulseiras compatíveis enviam os dados pelo celular do paciente. Para quem não tem wearable, cartão com chip e o kit de triagem das células e unidades móveis.", "Relojes y pulseras compatibles envían los datos por el celular del paciente. Para quien no tiene wearable, tarjeta con chip y el kit de triaje de las células y unidades móviles.", "Compatible watches and bands send data through the patient’s phone. For those without a wearable, a chip card and the triage kit in cells and mobile units.")),
        (S("Qualidade do dado", "Calidad del dato", "Data quality"), S("Antes de chegar ao motor clínico, cada leitura recebe uma nota de confiança: sensor desconectado, bateria fraca ou leitura fora do esperado são tratados como alerta técnico, não clínico.", "Antes de llegar al motor clínico, cada lectura recibe una nota de confianza: sensor desconectado, batería baja o lectura fuera de lo esperado se tratan como alerta técnica, no clínica.", "Before reaching the clinical engine, every reading gets a confidence score: a disconnected sensor, low battery or odd reading is handled as a technical alert, not a clinical one.")),
        (S("Motor RAPP", "Motor RAPP", "RAPP engine"), S("Compara cada paciente com o próprio padrão — a assinatura pessoal — olhando desvio, tendência e a correlação entre os sinais.", "Compara a cada paciente con su propio patrón — la firma personal — mirando desvío, tendencia y la correlación entre las señales.", "Compares each patient with their own pattern — the personal signature — looking at deviation, trend and correlation between signals.")),
        (S("Triagem por prioridade", "Triaje por prioridad", "Priority triage"), S("Os alertas são classificados por nível de gravidade, inspirados em escores clínicos reconhecidos, e cada nível define quem é avisado e como.", "Las alertas se clasifican por nivel de gravedad, inspiradas en puntajes clínicos reconocidos, y cada nivel define a quién se avisa y cómo.", "Alerts are ranked by severity, inspired by recognized clinical scores, and each level sets who is notified and how.")),
        (S("Resumo de emergência", "Resumen de emergencia", "Emergency summary"), S("QR code ou leitura por aproximação mostram medicamentos, alergias, doenças e últimos diagnósticos para a equipe de emergência.", "Código QR o lectura por proximidad muestran medicamentos, alergias, enfermedades y últimos diagnósticos para el equipo de emergencia.", "A QR code or tap-to-read shows medication, allergies, conditions and latest diagnoses to emergency teams.")),
        (S("Base clínica", "Base clínica", "Clinical base"), S("Doenças codificadas pela CID-11 e exames laboratoriais pelo padrão LOINC, com faixas de referência por sexo e idade, em português e espanhol.", "Enfermedades codificadas por la CIE-11 y exámenes de laboratorio por el estándar LOINC, con rangos de referencia por sexo y edad, en portugués y español.", "Conditions coded with ICD-11 and lab tests with LOINC, with reference ranges by sex and age, in Portuguese and Spanish.")),
    ]
    sec = [
        (S("Interoperabilidade", "Interoperabilidad", "Interoperability"), S("O Help Cure não substitui o prontuário único público: envia o prontuário do paciente por API, no padrão de dados exigido, e entrega um histórico mais completo porque acompanha o paciente todos os dias.", "Help Cure no reemplaza el registro clínico único público: envía la historia del paciente por API, en el estándar de datos exigido, y entrega un historial más completo porque acompaña al paciente todos los días.", "Help Cure doesn’t replace the public unified health record: it sends the patient record via API in the required data standard, and adds a richer history because it follows the patient daily.")),
        (S("Integridade dos documentos", "Integridad de los documentos", "Document integrity"), S("Laudos, resultados e relatórios enviados a órgãos públicos levam assinatura digital ICP-Brasil e carimbo do tempo. Opcionalmente, um código de verificação (hash) pode ser registrado em blockchain pública — o conteúdo clínico nunca vai para a blockchain.", "Informes, resultados y reportes enviados a organismos públicos llevan firma digital ICP-Brasil y sello de tiempo. Opcionalmente, un código de verificación (hash) puede registrarse en blockchain pública — el contenido clínico nunca va a la blockchain.", "Reports, results and documents sent to public agencies carry ICP-Brasil digital signatures and timestamps. Optionally, a verification hash can be anchored on a public blockchain — clinical content never goes on-chain.")),
        (S("Privacidade", "Privacidad", "Privacy"), S("Tratamento de dados conforme a LGPD no Brasil e a lei de proteção de dados pessoais do Paraguai. Cada perfil vê só o que precisa; painéis públicos, como o de senhas da unidade móvel, nunca mostram nomes.", "Tratamiento de datos conforme a la LGPD de Brasil y la ley de protección de datos personales de Paraguay. Cada perfil ve solo lo que necesita; los paneles públicos, como el de números de la unidad móvil, nunca muestran nombres.", "Data handled under Brazil’s LGPD and Paraguay’s personal data protection law. Each role sees only what it needs; public screens, like the mobile unit’s queue board, never show names.")),
        (S("Humano no comando", "Humano al mando", "Human in the loop"), S("O Help Cure organiza dados e prioriza alertas; a decisão clínica é sempre de um profissional de saúde. O enquadramento regulatório como software de saúde está em preparação no Brasil e no Paraguai.", "Help Cure organiza datos y prioriza alertas; la decisión clínica siempre es de un profesional de salud. El encuadre regulatorio como software de salud está en preparación en Brasil y Paraguay.", "Help Cure organizes data and prioritizes alerts; clinical decisions always belong to a health professional. Regulatory classification as health software is being prepared in Brazil and Paraguay.")),
    ]
    cs = "".join('<div class="card"><div class="in">%s%s</div></div>' % (T(*a, tag="h3"), T(*b2, tag="p")) for a, b2 in cards)
    ss = "".join('<div class="card"><div class="in">%s%s</div></div>' % (T(*a, tag="h3"), T(*b2, tag="p")) for a, b2 in sec)
    b = f'''
<div class="hero sub">
  <img src="img/assinatura.webp" alt="">
  <div class="wrap">
    {T("Tecnologia e segurança", "Tecnología y seguridad", "Technology and security", "span", "eyebrow")}
    {T("A assinatura de cada paciente, protegida.", "La firma de cada paciente, protegida.", "Each patient’s signature, protected.", "h1")}
    {T("No centro do Help Cure está o RAPP, motor de IA da MTS Moulin Tecnologia em Sistemas, que compara cada pessoa com o próprio padrão de saúde.", "En el centro de Help Cure está el RAPP, motor de IA de MTS Moulin Tecnologia em Sistemas, que compara a cada persona con su propio patrón de salud.", "At the heart of Help Cure is RAPP, the AI engine by MTS Moulin Tecnologia em Sistemas, which compares each person with their own health pattern.", "p", "lead")}
  </div>
</div>
<section>
  <div class="wrap">
    <div class="head">{T("Do sensor à decisão", "Del sensor a la decisión", "From sensor to decision", "span", "eyebrow")}{T("Como os dados viram cuidado.", "Cómo los datos se convierten en cuidado.", "How data becomes care.", "h2")}</div>
    <div class="g g3">{cs}</div>
  </div>
</section>
<section class="dark">
  <div class="wrap split">
    <div>
      {T("A assinatura de comportamento", "La firma de comportamiento", "The behavior signature", "span", "eyebrow")}
      {T("Normal para você, não para a média.", "Normal para usted, no para el promedio.", "Normal for you, not for the average.", "h2")}
      {T("Uma pressão de 14 por 9 pode ser rotina para uma pessoa e sinal de alerta para outra. O RAPP aprende o padrão de cada paciente ao longo dos dias e avisa quando ele muda — mesmo que o valor ainda esteja dentro da faixa “normal” da população.", "Una presión de 14 por 9 puede ser rutina para una persona y señal de alerta para otra. El RAPP aprende el patrón de cada paciente a lo largo de los días y avisa cuando cambia — aunque el valor todavía esté dentro del rango “normal” de la población.", "A blood pressure of 140/90 can be routine for one person and a warning sign for another. RAPP learns each patient’s pattern over days and alerts when it changes — even if the value is still within the population’s “normal” range.", "p", "muted", attrs=' style="margin-top:16px;font-size:18px"')}
    </div>
    <img src="img/central.webp" {pg.alt("Central de monitoramento com alertas", "Central de monitoreo con alertas", "Monitoring center with alerts")} loading="lazy">
  </div>
</section>
<section>
  <div class="wrap">
    <div class="head">{T("Segurança", "Seguridad", "Security", "span", "eyebrow")}{T("Confiança para pacientes, médicos e governos.", "Confianza para pacientes, médicos y gobiernos.", "Trust for patients, doctors and governments.", "h2")}</div>
    <div class="g g2">{ss}</div>
  </div>
</section>
'''
    shell(pg, "tecnologia.html", title, b, "A tecnologia do Help Cure: motor RAPP, captura de sinais, resumo de emergência, interoperabilidade, assinatura digital e privacidade.")


# ------------------------------------------------------------------ SOLIDÁRIO (campanha)
def solidario():
    pg = Page(0)
    T = pg.t
    title = pg.title("Help Cure Solidário — Campanha", "Help Cure Solidario — Campaña", "Help Cure Solidarity — Campaign")
    TBD = ("a definir", "a definir", "to be defined")

    def val(key):
        return '<b class="cv" data-camp="%s">%s</b>' % (key, T(*TBD))

    metas = [
        ("piloto", S("Etapa 1 — Piloto", "Etapa 1 — Piloto", "Stage 1 — Pilot"),
         S("Piloto com pacientes reais no ar, kits de teste e número oficial de WhatsApp.", "Piloto con pacientes reales en marcha, kits de prueba y número oficial de WhatsApp.", "Pilot with real patients running, test kits and an official WhatsApp number.")),
        ("movel1", S("Etapa 2 — Primeira unidade móvel", "Etapa 2 — Primera unidad móvil", "Stage 2 — First mobile unit"),
         S("Uma unidade móvel atendendo gratuitamente uma comunidade no Paraguai.", "Una unidad móvil atendiendo gratuitamente a una comunidad en Paraguay.", "One mobile unit providing free care to a community in Paraguay.")),
        ("expansao", S("Etapa 3 — Expansão", "Etapa 3 — Expansión", "Stage 3 — Expansion"),
         S("Segunda unidade no Brasil e pulseiras de monitoramento para os pacientes atendidos.", "Segunda unidad en Brasil y pulseras de monitoreo para los pacientes atendidos.", "A second unit in Brazil and monitoring bands for the patients served.")),
    ]
    metas_html = "".join(f'''<div class="card meta" data-meta="{k}"><div class="in">{T(*h, tag="h3")}{T(*d, tag="p")}
      <div class="mrow"><span>{T("Meta", "Meta", "Goal")}</span>{val("metas." + k)}</div>
      <div class="bar" aria-hidden="true"><i></i></div></div></div>''' for k, h, d in metas)

    niveis = [
        ("apoiador", S("Apoiador", "Apoyador", "Supporter"), S("Seu nome no mural de apoiadores e o relatório de impacto.", "Su nombre en el mural de apoyadores y el informe de impacto.", "Your name on the supporters’ wall and the impact report.")),
        ("padrinho", S("Padrinho", "Padrino", "Sponsor"), S("Tudo do Apoiador e você apadrinha um atendimento na unidade móvel.", "Todo lo del Apoyador y usted apadrina una atención en la unidad móvil.", "Everything in Supporter, plus you sponsor one visit at the mobile unit.")),
        ("guardiao", S("Guardião", "Guardián", "Guardian"), S("Kit Help Cure para casa com smartwatch e 12 meses de monitoramento gratuito.", "Kit Help Cure para casa con smartwatch y 12 meses de monitoreo gratuito.", "Help Cure home kit with smartwatch and 12 months of free monitoring.")),
        ("solidario", S("Guardião Solidário", "Guardián Solidario", "Solidarity Guardian"), S("Um kit para você e outro doado a uma família atendida pela campanha.", "Un kit para usted y otro donado a una familia atendida por la campaña.", "One kit for you and another donated to a family served by the campaign.")),
        ("institucional", S("Patrocinador institucional", "Patrocinador institucional", "Institutional sponsor"), S("Sua marca na unidade móvel e um relatório de impacto dedicado.", "Su marca en la unidad móvil y un informe de impacto dedicado.", "Your brand on the mobile unit and a dedicated impact report.")),
    ]
    niv_html = "".join(f'''<div class="card tier{' hl' if k == 'guardiao' else ''}"><div class="in">{T(*h, tag="h3")}<div class="price">{val("niveis." + k)}</div>{T(*d, tag="p")}</div></div>''' for k, h, d in niveis)

    b = f'''
<div class="hero sub">
  <img src="img/movel_triagem.webp" alt="">
  <div class="wrap">
    {T("Help Cure Solidário", "Help Cure Solidario", "Help Cure Solidarity", "span", "eyebrow")}
    {T("O cuidado que acompanha você — também para quem mais precisa.", "El cuidado que te acompaña — también para quien más lo necesita.", "Care that stays with you — also for those who need it most.", "h1")}
    {T("Uma campanha para levar unidades móveis com atendimento gratuito a comunidades carentes do Paraguai e do Brasil, e concluir o desenvolvimento da plataforma Help Cure.", "Una campaña para llevar unidades móviles con atención gratuita a comunidades vulnerables de Paraguay y Brasil, y completar el desarrollo de la plataforma Help Cure.", "A campaign to bring mobile units with free care to underserved communities in Paraguay and Brazil, and to complete the Help Cure platform.", "p", "lead")}
    <div class="cta"><a class="btn primary" href="#apoiar">{T("Quero apoiar", "Quiero apoyar", "I want to support")}</a><a class="btn ghost" href="#niveis">{T("Ver as recompensas", "Ver las recompensas", "See the rewards")}</a></div>
    <p class="status" data-camp-status>{T("Campanha em preparação: cadastre-se para ser avisado no lançamento.", "Campaña en preparación: regístrese para recibir aviso en el lanzamiento.", "Campaign in preparation: sign up to be notified at launch.")}</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="head">
      {T("Dois objetivos", "Dos objetivos", "Two goals", "span", "eyebrow")}
      {T("Cada contribuição gera cuidado hoje e uma plataforma melhor amanhã.", "Cada aporte genera cuidado hoy y una plataforma mejor mañana.", "Every contribution creates care today and a better platform tomorrow.", "h2")}
    </div>
    <div class="g g2">
      <div class="card"><img src="img/movel_fila.webp" alt="" loading="lazy"><div class="in">{T("Atendimento gratuito", "Atención gratuita", "Free care", "h3")}{T("Unidades móveis com triagem e teleconsulta visitam comunidades sem acesso à saúde. Cada pessoa atendida segue acompanhada à distância depois da visita.", "Unidades móviles con triaje y teleconsulta visitan comunidades sin acceso a la salud. Cada persona atendida sigue acompañada a distancia después de la visita.", "Mobile units with triage and teleconsultation visit communities without access to care. Everyone seen is followed remotely after the visit.", "p")}</div></div>
      <div class="card"><img src="img/central.webp" alt="" loading="lazy"><div class="in">{T("Desenvolvimento da plataforma", "Desarrollo de la plataforma", "Platform development", "h3")}{T("O atendimento real mostra o que funciona. Esses resultados aceleram o motor RAPP, o app do paciente e a central de monitoramento.", "La atención real muestra lo que funciona. Esos resultados aceleran el motor RAPP, la app del paciente y la central de monitoreo.", "Real-world care shows what works. Those results speed up the RAPP engine, the patient app and the monitoring center.", "p")}</div></div>
    </div>
  </div>
</section>

<section class="soft">
  <div class="wrap">
    <div class="head">
      {T("Metas", "Metas", "Goals", "span", "eyebrow")}
      {T("Metas por etapa: cada valor já vira um resultado visível.", "Metas por etapa: cada monto ya se convierte en un resultado visible.", "Stage goals: every amount turns into a visible result.", "h2")}
      <div class="total">{T("Arrecadado até agora", "Recaudado hasta ahora", "Raised so far")}: {val("arrecadado")}</div>
    </div>
    <div class="g g3">{metas_html}</div>
  </div>
</section>

<section id="niveis">
  <div class="wrap">
    <div class="head">
      {T("Recompensas", "Recompensas", "Rewards", "span", "eyebrow")}
      {T("Escolha como apoiar.", "Elija cómo apoyar.", "Choose how to support.", "h2")}
      {T("Os valores de cada nível serão publicados no lançamento. O monitoramento gratuito vale por 12 meses e segue os termos de uso e o consentimento do paciente.", "Los montos de cada nivel se publicarán en el lanzamiento. El monitoreo gratuito vale por 12 meses y sigue los términos de uso y el consentimiento del paciente.", "Each tier’s amount will be published at launch. Free monitoring lasts 12 months and follows the terms of use and patient consent.", "p", "muted")}
    </div>
    <div class="g g5">{niv_html}</div>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <div class="head">
      {T("Transparência", "Transparencia", "Transparency", "span", "eyebrow")}
      {T("Você acompanha cada real e cada atendimento.", "Usted sigue cada peso y cada atención.", "You can follow every dollar and every visit.", "h2")}
    </div>
    <div class="g g3 steps">
      <div class="step">{T("Fundação Help Cure", "Fundación Help Cure", "Help Cure Foundation", "h3")}{T("Entidade sem fins lucrativos no Paraguai que recebe as doações e opera as unidades móveis, com prestação de contas semestral.", "Entidad sin fines de lucro en Paraguay que recibe las donaciones y opera las unidades móviles, con rendición de cuentas semestral.", "A non-profit in Paraguay that receives donations and runs the mobile units, reporting every six months.", "p")}</div>
      <div class="step">{T("Painel público", "Panel público", "Public dashboard", "h3")}{T("Nesta página: valor arrecadado, gasto por destino e número de atendimentos, atualizados todo mês.", "En esta página: monto recaudado, gasto por destino y número de atenciones, actualizados cada mes.", "On this page: amount raised, spending by use and number of visits, updated monthly.", "p")}</div>
      <div class="step">{T("Cuidado com as pessoas", "Cuidado con las personas", "Care for people", "h3")}{T("Médico responsável em cada país, consentimento informado e proteção de dados. Ninguém é atendido sem saber como seus dados são usados.", "Médico responsable en cada país, consentimiento informado y protección de datos. Nadie es atendido sin saber cómo se usan sus datos.", "A responsible physician in each country, informed consent and data protection. No one is seen without knowing how their data is used.", "p")}</div>
    </div>
  </div>
</section>

<section class="soft">
  <div class="wrap split">
    <div>
      {T("Empresas e instituições", "Empresas e instituciones", "Companies and institutions", "span", "eyebrow")}
      {T("Patrocine uma unidade móvel.", "Patrocine una unidad móvil.", "Sponsor a mobile unit.", "h2")}
      {T("Indústrias, cooperativas, laboratórios, farmácias, igrejas e universidades podem levar a unidade a uma comunidade escolhida, com a marca na unidade e um relatório de impacto próprio.", "Industrias, cooperativas, laboratorios, farmacias, iglesias y universidades pueden llevar la unidad a una comunidad elegida, con su marca en la unidad y un informe de impacto propio.", "Industries, cooperatives, labs, pharmacies, churches and universities can bring the unit to a community of their choice, with their brand on the unit and a dedicated impact report.", "p", "muted", attrs=' style="margin-top:16px;font-size:18px"')}
      <div class="cta"><a class="btn dark" href="#apoiar" data-tipo="empresa">{T("Falar sobre patrocínio", "Hablar sobre patrocinio", "Talk about sponsorship")}</a></div>
    </div>
    <img src="img/movel_toldo.webp" alt="" loading="lazy">
  </div>
</section>

<section id="apoiar">
  <div class="wrap split">
    <div>
      {T("Quero apoiar", "Quiero apoyar", "I want to support", "span", "eyebrow")}
      {T("Cadastre-se e seja avisado no lançamento.", "Regístrese y reciba aviso en el lanzamiento.", "Sign up and be notified at launch.", "h2")}
      {T("Ainda não recebemos pagamentos. Assim que a fundação e a plataforma de doação estiverem prontas, você recebe o link e os valores de cada nível.", "Todavía no recibimos pagos. Cuando la fundación y la plataforma de donación estén listas, usted recibe el enlace y los montos de cada nivel.", "We are not taking payments yet. Once the foundation and donation platform are ready, you’ll get the link and each tier’s amount.", "p", "muted", attrs=' style="margin-top:16px;font-size:18px"')}
    </div>
    <form class="camp-form" id="fcamp" novalidate>
      <label>{T("Nome", "Nombre", "Name")}<input name="nome" required autocomplete="name"></label>
      <label>{T("E-mail", "Correo electrónico", "Email")}<input name="email" type="email" autocomplete="email"></label>
      <label>{T("WhatsApp (com código do país)", "WhatsApp (con código de país)", "WhatsApp (with country code)")}<input name="whatsapp" type="tel" autocomplete="tel" placeholder="+595 …"></label>
      <div class="two">
        <label>{T("País", "País", "Country")}<select name="pais"><option value="PY">Paraguay</option><option value="BR">Brasil</option><option value="OUTRO">{T("Outro", "Otro", "Other")}</option></select></label>
        <label>{T("Eu sou", "Soy", "I am")}<select name="tipo"><option value="cidadao">{T("Pessoa física", "Persona", "Individual")}</option><option value="empresa">{T("Empresa", "Empresa", "Company")}</option><option value="instituicao">{T("Instituição / ONG / igreja", "Institución / ONG / iglesia", "Institution / NGO / church")}</option><option value="voluntario">{T("Voluntário da saúde", "Voluntario de salud", "Health volunteer")}</option></select></label>
      </div>
      <label>{T("Nível de interesse", "Nivel de interés", "Tier of interest")}<select name="nivel"><option value="">—</option><option value="apoiador">{T("Apoiador", "Apoyador", "Supporter")}</option><option value="padrinho">{T("Padrinho", "Padrino", "Sponsor")}</option><option value="guardiao">{T("Guardião", "Guardián", "Guardian")}</option><option value="solidario">{T("Guardião Solidário", "Guardián Solidario", "Solidarity Guardian")}</option><option value="institucional">{T("Patrocinador institucional", "Patrocinador institucional", "Institutional sponsor")}</option></select></label>
      <label class="chk"><input type="checkbox" name="consent" required> {T("Aceito receber notícias da campanha por e-mail ou WhatsApp e posso cancelar a qualquer momento.", "Acepto recibir noticias de la campaña por correo o WhatsApp y puedo cancelar en cualquier momento.", "I agree to receive campaign news by email or WhatsApp and can opt out at any time.")}</label>
      <button class="btn primary" type="submit">{T("Quero ser avisado", "Quiero recibir aviso", "Notify me")}</button>
      <p class="msg" role="status" aria-live="polite"></p>
      <span hidden data-m="ok">{T("Obrigado! Você será avisado no lançamento.", "¡Gracias! Recibirá aviso en el lanzamiento.", "Thank you! We’ll let you know at launch.")}</span>
      <span hidden data-m="bad">{T("Preencha o nome, um contato (e-mail ou WhatsApp) e aceite receber notícias.", "Complete el nombre, un contacto (correo o WhatsApp) y acepte recibir noticias.", "Please fill in your name, a contact (email or WhatsApp) and accept updates.")}</span>
      <span hidden data-m="err">{T("Não foi possível enviar agora. Tente de novo em instantes.", "No fue posible enviar ahora. Intente de nuevo en unos instantes.", "Couldn’t send right now. Please try again shortly.")}</span>
    </form>
  </div>
</section>

<section class="soft">
  <div class="wrap">
    <div class="head">
      {T("Perguntas frequentes", "Preguntas frecuentes", "FAQ", "span", "eyebrow")}
      {T("Antes de apoiar.", "Antes de apoyar.", "Before you support.", "h2")}
    </div>
    <div class="faq">
      <details><summary>{T("Isto é um investimento?", "¿Esto es una inversión?", "Is this an investment?")}</summary>{T("Não. É uma doação com recompensas. Ela não dá participação na empresa, lucro ou retorno financeiro. Investidores têm uma área própria.", "No. Es una donación con recompensas. No da participación en la empresa, ganancias ni retorno financiero. Los inversionistas tienen un área propia.", "No. It’s a donation with rewards. It gives no stake in the company, profit or financial return. Investors have their own area.", "p")}</details>
      <details><summary>{T("Haverá um token Help Cure?", "¿Habrá un token Help Cure?", "Will there be a Help Cure token?")}</summary>{T("Numa segunda fase, a recompensa poderá ser emitida como token digital. Ele servirá apenas para registrar o apoio e liberar recompensas, sem promessa de valorização.", "En una segunda fase, la recompensa podrá emitirse como token digital. Solo servirá para registrar el apoyo y liberar recompensas, sin promesa de valorización.", "In a second phase, the reward may be issued as a digital token. It will only record support and unlock rewards, with no promise of appreciation.", "p")}</details>
      <details><summary>{T("Quem recebe o dinheiro?", "¿Quién recibe el dinero?", "Who receives the money?")}</summary>{T("As doações vão para a Fundação Help Cure, que opera as unidades móveis. A tecnologia é fornecida pela empresa Help Cure por contrato, com contas separadas.", "Las donaciones van a la Fundación Help Cure, que opera las unidades móviles. La tecnología la provee la empresa Help Cure por contrato, con cuentas separadas.", "Donations go to the Help Cure Foundation, which runs the mobile units. The technology is provided by the Help Cure company under contract, with separate accounts.", "p")}</details>
      <details><summary>{T("Como escolhem as comunidades?", "¿Cómo eligen las comunidades?", "How are communities chosen?")}</summary>{T("Em parceria com a rede pública local e organizações da comunidade, priorizando quem tem menos acesso à saúde.", "En alianza con la red pública local y organizaciones de la comunidad, priorizando a quienes tienen menos acceso a la salud.", "With local public health services and community organizations, prioritizing those with the least access to care.", "p")}</details>
    </div>
  </div>
</section>
<script src="assets/campanha.js?v=1"></script>
'''
    shell(pg, "solidario.html", title, b, "Help Cure Solidário: campanha para levar unidades móveis com atendimento gratuito a comunidades carentes do Paraguai e do Brasil.")


if __name__ == "__main__":
    home(); sol_index(); para_quem(); tecnologia(); solidario()
    for k, v in SOLDATA.items():
        sol_page(k, v)
    print("ok")
