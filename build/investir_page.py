# Página do investidor (investir.html) — PT/ES/EN. Importada por build.py.
# Números: modelo HelpCure_Modelo_por_Abrangencia (out/2026). Ao mudar o modelo, atualize aqui.
import os, html

INV_CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "investir.css"), encoding="utf-8").read()


def build(Page, shell, S):
    pg = Page(0)
    T = pg.t
    title = pg.title("Investir no Help Cure", "Invertir en Help Cure", "Invest in Help Cure")

    def kpis(items, hero=False):
        return '<div class="kpis">' + "".join(
            '<div class="kpi">%s%s</div>' % (T(*v, tag="b"), T(*l)) for v, l in items) + '</div>'

    # ---- escopos: (id, aba, texto, kpis, receita, docs)
    OK = S("Pronto", "Listo", "Ready")
    TODO = S("A enviar", "Por enviar", "Coming")
    REC5 = S("Receita no Ano 5", "Ingresos en el Año 5", "Year 5 revenue")
    TIR = S("TIR", "TIR", "IRR")
    PAY = S("Payback", "Payback", "Payback")
    CAP = S("Captação", "Captación", "Funding")
    PRES = S("Apresentação", "Presentación", "Presentation")
    RES = S("Resumo executivo", "Resumen ejecutivo", "Executive summary")
    PLAN = S("Planilha", "Planilla", "Spreadsheet")
    VID = S("Vídeo", "Video", "Video")
    VID35 = S("3–5 min, narrado", "3–5 min, narrado", "3–5 min, narrated")

    def aba(e):
        return S("Aba %s do modelo único" % e, "Pestaña %s del modelo único" % e, "Tab %s of the single model" % e)

    def yrs(pt):
        return S(pt + " anos", pt + " años", pt.replace(",", ".") + " years")

    ESC = [
        ("e1", S("E1 · Clínica", "E1 · Clínica", "E1 · Clinic"),
         S("Projeto enxuto para redes de clínicas e hospitais: só o desenvolvimento da plataforma, a implantação no sistema de cada clínica e 24 meses de manutenção da empresa. Sem dispositivos, sem célula de atendimento e sem unidade móvel. Cresce por clínica replicada (500 pacientes cada), no Paraguai ou no Brasil, com os preços e impostos de cada país.",
           "Proyecto reducido para redes de clínicas y hospitales: solo el desarrollo de la plataforma, la implantación en el sistema de cada clínica y 24 meses de mantenimiento de la empresa. Sin dispositivos, sin célula de atención y sin unidad móvil. Crece clínica por clínica (500 pacientes cada una), en Paraguay o en Brasil, con los precios e impuestos de cada país.",
           "A lean project for clinic and hospital networks: only platform development, deployment into each clinic’s system and 24 months of company upkeep. No devices, no care cell and no mobile unit. It grows clinic by clinic (500 patients each), in Paraguay or Brazil, with each country’s prices and taxes."),
         [(S("US$ 133 mil", "US$ 133 mil", "US$ 133k"), S("Receita por ano, por cliente", "Ingresos por año, por cliente", "Revenue per year, per client")),
          (S("73%", "73%", "73%"), TIR), (yrs("1,1"), PAY),
          (S("US$ 42 mil", "US$ 42 mil", "US$ 42k"), S("Captação por cliente", "Captación por cliente", "Funding per client"))],
         [(S("Mensalidade fixa", "Mensualidad fija", "Fixed monthly fee"), S("US$ 5.500 da instituição", "US$ 5.500 de la institución", "US$ 5,500 from the institution")),
          (S("Por paciente", "Por paciente", "Per patient"), S("pagos por usuário, governo ou plano (500 pacientes)", "pagados por el usuario, el gobierno o el seguro (500 pacientes)", "paid by the user, government or health plan (500 patients)")),
          (S("Integração", "Integración", "Integration"), S("US$ 20 mil com o sistema da clínica (única despesa de capital)", "US$ 20 mil con el sistema de la clínica (único gasto de capital)", "US$ 20k with the clinic’s system (the only capital expense)"))],
         [(PRES, S("HelpCure na sua Clínica · Para o Médico", "HelpCure en su Clínica · Para el Médico", "HelpCure in your Clinic · For Doctors"), True),
          (RES, S("1 cliente-tipo", "1 cliente tipo", "1 typical client"), False),
          (PLAN, aba("E1"), True), (VID, VID35, False)]),
        ("e2", S("E2 · Plano de saúde", "E2 · Seguro de salud", "E2 · Health plan"),
         S("Um plano de saúde regional: de 1.500 a 40.000 beneficiários crônicos monitorados, com a equipe clínica do próprio cliente. Casos Unimed-BH e CASSI.",
           "Un seguro de salud regional: de 1.500 a 40.000 beneficiarios crónicos monitoreados, con el equipo clínico del propio cliente. Casos Unimed-BH y CASSI.",
           "A regional health plan: 1,500 to 40,000 chronic members monitored, with the client’s own clinical team. Unimed-BH and CASSI cases."),
         [(S("US$ 7,2 mi", "US$ 7,2 M", "US$ 7.2M"), REC5), (S("64%", "64%", "64%"), TIR), (yrs("2,6"), PAY),
          (S("US$ 0,85 mi", "US$ 0,85 M", "US$ 0.85M"), CAP)],
         [(S("Por beneficiário", "Por beneficiario", "Per member"), S("monitorado por mês; fixo + variável por economia comprovada (modelo CASSI)", "monitoreado por mes; fijo + variable por ahorro comprobado (modelo CASSI)", "monitored per month; fixed + variable on proven savings (CASSI model)")),
          (S("Teto", "Techo", "Cap"), S("= economia do plano de saúde em internações e pronto-socorro evitados", "= ahorro del seguro de salud en internaciones y urgencias evitadas", "= the plan’s savings on avoided admissions and ER visits")),
          (S("Alta monitorada", "Alta monitoreada", "Monitored discharge"), S("por episódio", "por episodio", "per episode"))],
         [(PRES, S("Unimed-BH e CASSI", "Unimed-BH y CASSI", "Unimed-BH and CASSI"), True),
          (RES, S("Unimed-BH e CASSI", "Unimed-BH y CASSI", "Unimed-BH and CASSI"), True),
          (PLAN, aba("E2"), True),
          (VID, S("CASSI (pronto) · genérico a fazer", "CASSI (listo) · genérico por hacer", "CASSI (ready) · generic to do"), True)]),
        ("e3", S("E3 · Estado", "E3 · Estado", "E3 · State"),
         S("Secretaria estadual de saúde, planos, empresas e cidadãos de um estado. Volumes do estudo da Bahia (14,9 mi de habitantes); aplicável ao Ceará.",
           "Secretaría estatal de salud, seguros, empresas y ciudadanos de un estado. Volúmenes del estudio de Bahía (14,9 M de habitantes); aplicable a Ceará.",
           "A state health department, plus health plans, employers and citizens of one state. Volumes from the Bahia study (14.9M people); applicable to Ceará."),
         [(S("US$ 20,0 mi", "US$ 20,0 M", "US$ 20.0M"), REC5), (S("20%", "20%", "20%"), TIR), (yrs("4,3"), PAY),
          (S("US$ 2,4 mi", "US$ 2,4 M", "US$ 2.4M"), CAP)],
         [(S("Governo", "Gobierno", "Government"), S("por cidadão coberto no atendimento móvel + contrato anual por célula pública", "por ciudadano cubierto en la atención móvil + contrato anual por célula pública", "per citizen covered by mobile care + annual contract per public cell")),
          (S("Planos, empresas e academias", "Seguros, empresas y gimnasios", "Plans, employers and gyms"), S("por pessoa e por célula instalada", "por persona y por célula instalada", "per person and per installed cell")),
          (S("Royalty", "Royalty", "Royalty"), S("do motor de análise; só o investimento local no estado", "del motor de análisis; solo la inversión local en el estado", "on the analysis engine; only the local investment in the state"))],
         [(PRES, S("Bahia · Ceará · Ecossistema", "Bahía · Ceará · Ecosistema", "Bahia · Ceará · Ecosystem"), True),
          (RES, S("Bahia e Ceará (a alinhar)", "Bahía y Ceará (por alinear)", "Bahia and Ceará (to align)"), True),
          (PLAN, aba("E3"), True), (VID, VID35, False)]),
        ("e4", S("E4 · Paraguai", "E4 · Paraguay", "E4 · Paraguay"),
         S("O país-piloto da Fase 2: a plataforma já existe, então só entram os custos de aplicação no Paraguai. É o laboratório que gera a evidência para os outros escopos.",
           "El país piloto de la Fase 2: la plataforma ya existe, así que solo entran los costos de aplicación en Paraguay. Es el laboratorio que genera la evidencia para los demás alcances.",
           "Phase 2’s pilot country: the platform already exists, so only the costs of deploying in Paraguay come in. It is the lab that produces the evidence for the other scopes."),
         [(S("US$ 13,5 mi", "US$ 13,5 M", "US$ 13.5M"), REC5),
          (S("> 100%", "> 100%", "> 100%"), S("TIR (plataforma paga na Fase 1)", "TIR (plataforma pagada en la Fase 1)", "IRR (platform paid in Phase 1)")),
          (yrs("1,4"), PAY),
          (S("US$ 0,36 mi", "US$ 0,36 M", "US$ 0.36M"), S("Captação (+ Fase 1)", "Captación (+ Fase 1)", "Funding (+ Phase 1)"))],
         [(S("Por pessoa/mês", "Por persona/mes", "Per person/month"), S("usuário US$ 9,90 · governo US$ 10 · plano US$ 12 · empregador US$ 3", "usuario US$ 9,90 · gobierno US$ 10 · seguro US$ 12 · empleador US$ 3", "user US$ 9.90 · government US$ 10 · plan US$ 12 · employer US$ 3")),
          (S("Células e unidades móveis", "Células y unidades móviles", "Cells and mobile units"), S("por entidade e por região de saúde", "por entidad y por región sanitaria", "per entity and per health region")),
          (S("Royalty", "Royalty", "Royalty"), S("de 10% sobre a receita, como nos demais escopos", "del 10% sobre los ingresos, como en los demás alcances", "of 10% of revenue, as in the other scopes"))],
         [(PRES, S("Plano de Negócios Paraguai (a atualizar)", "Plan de Negocios Paraguay (por actualizar)", "Paraguay Business Plan (to update)"), True),
          (RES, S("ES/PT", "ES/PT", "ES/PT"), True),
          (PLAN, aba("E4"), True), (VID, VID35, False)]),
        ("e5", S("E5 · Brasil", "E5 · Brasil", "E5 · Brazil"),
         S("Camada nacional de monitoramento integrada à RNDS e aos programas do Ministério da Saúde, mais planos e cidadãos. Volumes do estudo nacional.",
           "Capa nacional de monitoreo integrada a la RNDS y a los programas del Ministerio de Salud de Brasil, más seguros y ciudadanos. Volúmenes del estudio nacional.",
           "A national monitoring layer integrated with Brazil’s RNDS and Ministry of Health programs, plus health plans and citizens. Volumes from the national study."),
         [(S("US$ 96,3 mi", "US$ 96,3 M", "US$ 96.3M"), REC5), (S("40%", "40%", "40%"), TIR), (yrs("3,8"), PAY),
          (S("US$ 8,7 mi", "US$ 8,7 M", "US$ 8.7M"), CAP)],
         [(S("Governo", "Gobierno", "Government"), S("per capita por cidadão coberto, no espírito do PMAE", "per cápita por ciudadano cubierto, en la línea del PMAE", "per capita per covered citizen, in the spirit of PMAE")),
          (S("Planos", "Seguros", "Health plans"), S("via integração RNDS–ANS", "vía integración RNDS–ANS", "via RNDS–ANS integration")),
          (S("Certificação RNDS/FHIR", "Certificación RNDS/FHIR", "RNDS/FHIR certification"), S("no Ano 0; royalty do motor de análise", "en el Año 0; royalty del motor de análisis", "in Year 0; royalty on the analysis engine"))],
         [(PRES, S("Brasil Vital Grid · Ministério", "Brasil Vital Grid · Ministerio", "Brasil Vital Grid · Ministry"), True),
          (RES, S("Ministério da Saúde (a alinhar)", "Ministerio de Salud (por alinear)", "Ministry of Health (to align)"), True),
          (PLAN, aba("E5"), True), (VID, VID35, False)]),
    ]

    def viab(code):
        clin = code == "E1"
        if clin:
            code = "E1PY"
        lab = S("Pacientes no Ano 5 (clínicas replicadas)", "Pacientes en el Año 5 (clínicas replicadas)", "Patients in Year 5 (replicated clinics)") if clin else \
            S("Vidas monitoradas no Ano 5", "Vidas monitoreadas en el Año 5", "Lives monitored in Year 5")
        k6 = [("vpl", S("VPL do projeto", "VAN del proyecto", "Project NPV")), ("tir", S("TIR do projeto", "TIR del proyecto", "Project IRR")),
              ("payback", S("Payback", "Payback", "Payback")), ("receita5", S("Receita no Ano 5", "Ingresos en el Año 5", "Year 5 revenue")),
              ("ebitda5", S("EBITDA no Ano 5", "EBITDA en el Año 5", "Year 5 EBITDA")), ("captacao", S("Captação do segmento", "Captación del segmento", "Segment funding"))]
        kp6 = '<div class="kpis vk">' + "".join('<div class="kpi"><b data-o="%s">—</b>%s</div>' % (o, T(*l)) for o, l in k6) + '</div>'
        if False:
            val = T("A clínica usa a plataforma pronta: não paga célula nem unidade móvel e não entra na rodada da Fase 1. Por isso o que vale aqui é o resultado do projeto, por clínica replicada.",
                    "La clínica usa la plataforma lista: no paga célula ni unidad móvil y no entra en la ronda de la Fase 1. Por eso lo que vale aquí es el resultado del proyecto, por clínica replicada.",
                    "The clinic uses the ready platform: it pays for no cell or mobile unit and is not part of the Phase 1 round. So what counts here is the project result, per replicated clinic.", "p", "vnote2")
        else:
            v4 = [("ticket", S("Rodada (Fase 1 + segmento + reserva)", "Ronda (Fase 1 + segmento + reserva)", "Round (Phase 1 + segment + reserve)")),
                  ("posmoney", S("Pós-money", "Post-money", "Post-money")),
                  ("participacao", S("Participação justa para TIR de 25%", "Participación justa para TIR del 25%", "Fair stake for a 25% IRR")),
                  ("moic", S("Múltiplo do investidor (MOIC)", "Múltiplo del inversionista (MOIC)", "Investor multiple (MOIC)"))]
            val = '<div class="vrow">' + "".join('<div><b data-o="%s">—</b>%s</div>' % (o, T(*l)) for o, l in v4) + '</div>'
        pais = ('<div class="vpais" role="group" aria-label="País">'
                '<button type="button" data-p="E1PY" aria-pressed="true">%s</button><button type="button" data-p="E1BR" aria-pressed="false">%s</button>'
                '%s</div>' % (T("Paraguai", "Paraguay", "Paraguay"), T("Brasil", "Brasil", "Brazil"),
                              T("Fase 1 enxuta: US$ 3,7 mi (desenvolvimento + 24 meses de empresa, com 30% de folga)",
                                "Fase 1 reducida: US$ 3,7 M (desarrollo + 24 meses de empresa, con 30% de margen)",
                                "Lean Phase 1: US$ 3.7M (development + 24 months of company, with a 30% buffer)", cls="vpn"))) if clin else ""
        return f'''<div class="viab" data-esc="{code}">
  {pais}
  <div class="vbar">
    <div class="vsl">
      <div class="vtop">{T(*lab, cls="vlab")}<b class="vn" data-o="vidas">—</b><span class="vd" data-o="delta"></span></div>
      <input type="range" min="0" max="0" step="1" value="0" aria-label="{html.escape(lab[0])}">
      <div class="vends"><span data-o="min"></span><button class="vreset" type="button">{T("Voltar ao calculado", "Volver a lo calculado", "Back to the estimate")}</button><span data-o="max"></span></div>
    </div>
    <div class="vval" aria-live="polite"><span class="vlab" data-o="vallab"></span><b data-o="val">—</b><span class="vsub" data-o="valsub"></span></div>
  </div>
  <p class="vst" data-o="status"></p>
  {kp6}
  {val}
  <div class="vchart">
    <div class="vch-h">{T("Receita e EBITDA por ano", "Ingresos y EBITDA por año", "Revenue and EBITDA by year", "h3")}<div class="vleg"><span><i class="sw r"></i>{T("Receita", "Ingresos", "Revenue")}</span><span><i class="sw e"></i>{T("EBITDA", "EBITDA", "EBITDA")}</span></div></div>
    <div class="vsvg"></div><div class="vtip" role="status"></div>
    <details><summary>{T("Ver em tabela", "Ver en tabla", "View as table")}</summary><div class="tw"><table class="t vtab"></table></div></details>
  </div>
</div>'''

    tabs, cases = [], []
    for i, (cid, lab, txt, kp, rev, docs) in enumerate(ESC):
        tabs.append('<button role="tab" aria-selected="%s" data-c="%s">%s</button>' % ("true" if i == 0 else "false", cid, T(*lab)))
        revs = "".join("<li>%s %s</li>" % (T(*a, tag="b"), T(*b)) for a, b in rev)
        ds = "".join('<div class="doc%s">%s%s<br><span class="tag%s">%s</span></div>' % (
            " ok" if ok else "", T(*a, tag="b"), T(*b), " ok" if ok else "", T(*(OK if ok else TODO))) for a, b, ok in docs)
        cases.append('<div class="case%s" id="c-%s">%s%s%s<ul class="rev">%s</ul><div class="docs">%s</div></div>' % (
            " on" if i == 0 else "", cid, T(*txt, tag="p", cls="lead", attrs=' style="max-width:70ch"'), viab(cid.upper()),
            T("Como gera receita", "Cómo genera ingresos", "How it makes money", "h3", attrs=' style="margin-top:26px"'), revs, ds))

    modelo = [
        (S("Por pessoa monitorada", "Por persona monitoreada", "Per monitored person"), S("Mensalidade por paciente, paga pelo governo, plano, empregador ou pelo próprio usuário. É a maior parte da receita.", "Mensualidad por paciente, pagada por el gobierno, el seguro, el empleador o el propio usuario. Es la mayor parte de los ingresos.", "A monthly fee per patient, paid by the government, health plan, employer or the user. It is most of the revenue.")),
        (S("Implantação e integração", "Implantación e integración", "Setup and integration"), S("Setup e conexão com prontuários e sistemas públicos no padrão exigido, com assinatura mensal por entidade.", "Setup y conexión con historias clínicas y sistemas públicos en el estándar exigido, con suscripción mensual por entidad.", "Setup and connection to health records and public systems in the required standard, with a monthly subscription per entity.")),
        (S("Infraestrutura como serviço", "Infraestructura como servicio", "Infrastructure as a service"), S("Células de atendimento, unidades móveis e kits residenciais, cobrados em contrato anual.", "Células de atención, unidades móviles y kits domiciliarios, cobrados en contrato anual.", "Care cells, mobile units and home kits, billed under annual contracts.")),
        (S("Royalty do motor de análise", "Royalty del motor de análisis", "Analysis engine royalty"), S("10% da receita de cada escopo remunera a detentora do motor de análise e predição.", "El 10% de los ingresos de cada alcance remunera a la titular del motor de análisis y predicción.", "10% of each scope’s revenue pays the owner of the analysis and prediction engine.")),
    ]
    mc = "".join('<div class="card"><div class="in">%s%s</div></div>' % (T(*a, tag="h3"), T(*b, tag="p")) for a, b in modelo)

    rows = [
        (S("Fase 1 — desenvolvimento, piloto e empresa (24 meses)", "Fase 1 — desarrollo, piloto y empresa (24 meses)", "Phase 1 — development, pilot and company (24 months)"), S("Base de qualquer rodada", "Base de cualquier ronda", "Basis of any round"), S("4,8 mi em 3 tranches", "4,8 M en 3 tramos", "4.8M in 3 tranches")),
        (S("Rede de clínicas (Paraguai ou Brasil)", "Red de clínicas (Paraguay o Brasil)", "Clinic network (Paraguay or Brazil)"), S("Fase 1 enxuta + E1 + reserva", "Fase 1 reducida + E1 + reserva", "Lean Phase 1 + E1 + reserve"), S("4,3 mi (1 clínica) a 7,7 mi (100)", "4,3 M (1 clínica) a 7,7 M (100)", "4.3M (1 clinic) to 7.7M (100)")),
        (S("Investidor no Paraguai", "Inversionista en Paraguay", "Investor in Paraguay"), S("Fase 1 + E4 + reserva", "Fase 1 + E4 + reserva", "Phase 1 + E4 + reserve"), S("5,9 mi", "5,9 M", "5.9M")),
        (S("Investidor regional no Brasil", "Inversionista regional en Brasil", "Regional investor in Brazil"), S("Fase 1 + E2 + E3 + reserva", "Fase 1 + E2 + E3 + reserva", "Phase 1 + E2 + E3 + reserve"), S("9,2 mi", "9,2 M", "9.2M")),
        (S("Parceiro nacional no Brasil", "Socio nacional en Brasil", "National partner in Brazil"), S("Fase 1 + E5 + reserva", "Fase 1 + E5 + reserva", "Phase 1 + E5 + reserve"), S("15,5 mi", "15,5 M", "15.5M")),
        (S("Investidor global", "Inversionista global", "Global investor"), S("Fase 1 + E4 + E5 + 2 planos de saúde + reserva", "Fase 1 + E4 + E5 + 2 seguros de salud + reserva", "Phase 1 + E4 + E5 + 2 health plans + reserve"), S("≈ 17,9 mi, em tranches", "≈ 17,9 M, en tramos", "≈ 17.9M, in tranches")),
    ]
    tr = "".join("<tr><td>%s</td><td>%s</td><td class=\"n\">%s</td></tr>" % (T(*a), T(*b), T(*c)) for a, b, c in rows)

    b = f'''
<div class="hero sub">
  <img src="img/central.webp" alt="">
  <div class="wrap">
    {T("Investidores", "Inversionistas", "Investors", "span", "eyebrow")}
    {T("Uma plataforma, cinco escopos de implantação.", "Una plataforma, cinco alcances de implantación.", "One platform, five deployment scopes.", "h1")}
    {T("O Help Cure é pago por pessoa monitorada, todo mês. O investidor escolhe a abrangência: uma clínica, um plano de saúde, um estado ou um país. Receita, retorno e captação variam com o escopo; a plataforma é a mesma.", "Help Cure se paga por persona monitoreada, cada mes. El inversionista elige el alcance: una clínica, un seguro de salud, un estado o un país. Ingresos, retorno y captación varían con el alcance; la plataforma es la misma.", "Help Cure is paid per monitored person, every month. The investor chooses the reach: a clinic, a health plan, a state or a country. Revenue, return and funding vary with the scope; the platform is the same.", "p", "lead")}
    {kpis([(S("US$ 12–20", "US$ 12–20", "US$ 12–20"), S("Receita por pessoa monitorada por mês", "Ingreso por persona monitoreada por mes", "Revenue per monitored person per month")),
           (S("45–57%", "45–57%", "45–57%"), S("Margem EBITDA no Ano 5", "Margen EBITDA en el Año 5", "EBITDA margin in Year 5")),
           (S("US$ 4,8 mi", "US$ 4,8 M", "US$ 4.8M"), S("Fase 1: desenvolvimento, piloto e 24 meses da empresa", "Fase 1: desarrollo, piloto y 24 meses de la empresa", "Phase 1: development, pilot and 24 months of the company")),
           (S("US$ 42 mil a 8,7 mi", "US$ 42 mil a 8,7 M", "US$ 42k to 8.7M"), S("Fase 2: captação por escopo de aplicação", "Fase 2: captación por alcance de aplicación", "Phase 2: funding per deployment scope"))])}
  </div>
</div>

<section>
  <div class="wrap">
    <div class="head">{T("Apresentação", "Presentación", "Presentation", "span", "eyebrow")}{T("Em 10 minutos, o Help Cure para investidores.", "En 10 minutos, Help Cure para inversionistas.", "Help Cure for investors, in 10 minutes.", "h2")}{T("Vídeo narrado com a plataforma, o modelo de receita e um minuto por escopo. Enquanto ele fica pronto, veja como o Help Cure funciona em cada ponto de cuidado.", "Video narrado con la plataforma, el modelo de ingresos y un minuto por alcance. Mientras está listo, vea cómo funciona Help Cure en cada punto de atención.", "A narrated video with the platform, the revenue model and one minute per scope. Until it’s ready, see how Help Cure works at each point of care.", "p")}</div>
    <div class="player" style="margin-top:28px;aspect-ratio:16/9;border-radius:18px;background:#06201C url(img/hero.webp) center/cover;display:grid;place-items:center">{T("Vídeo do investidor em produção", "Video del inversionista en producción", "Investor video in production", attrs=' style="background:rgba(6,32,28,.85);color:#E9F3F0;padding:12px 18px;border-radius:12px"')}</div>
    <p style="margin-top:14px"><a class="btn line" href="/investidores/" data-inv="/investidores/">{T("Ver os vídeos por módulo", "Ver los videos por módulo", "Watch the videos by module")}</a></p>
  </div>
</section>

<section class="soft">
  <div class="wrap">
    <div class="head">{T("A plataforma", "La plataforma", "The platform", "span", "eyebrow")}{T("Duas fases: desenvolver uma vez, aplicar por escopo.", "Dos fases: desarrollar una vez, aplicar por alcance.", "Two phases: build once, deploy by scope.", "h2")}{T("<b>Fase 1</b> (Paraguai, 24 meses): plataforma, piloto (com uma unidade móvel protótipo) e manutenção da empresa, pagos uma vez — US$ 4,8 mi em três tranches por marcos. <b>Fase 2</b>: cada escopo de aplicação carrega só o que é dele — dispositivos, células, unidades móveis, equipe adicional e infraestrutura — e paga royalty sobre a receita pelo motor de análise.", "<b>Fase 1</b> (Paraguay, 24 meses): plataforma, piloto (con una unidad móvil prototipo) y mantenimiento de la empresa, pagados una sola vez — US$ 4,8 M en tres tramos por hitos. <b>Fase 2</b>: cada alcance de aplicación lleva solo lo suyo — dispositivos, células, unidades móviles, equipo adicional e infraestructura — y paga royalty sobre los ingresos por el motor de análisis.", "<b>Phase 1</b> (Paraguay, 24 months): platform, pilot (with one prototype mobile unit) and company upkeep, paid once — US$ 4.8M in three milestone tranches. <b>Phase 2</b>: each deployment scope carries only its own costs — devices, cells, mobile units, extra staff and infrastructure — and pays a revenue royalty for the analysis engine.", "p", raw=True)}</div>
    <div class="g g4">{mc}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head">{T("Viabilidade por segmento", "Viabilidad por segmento", "Feasibility by segment", "span", "eyebrow")}{T("Escolha o segmento e mova a barra de vidas.", "Elija el segmento y mueva la barra de vidas.", "Pick a segment and move the lives slider.", "h2")}{T("A barra começa nas vidas calculadas no plano de cada segmento e soma passos de 5 mil (clínica e plano de saúde) ou 20 mil (estado e país). VPL, TIR, payback, captação e o valuation da Help Cure recalculam na hora. Em todos os segmentos a rodada inclui a Fase 1 (desenvolvimento), que é fixa; na clínica, uma Fase 1 enxuta, sem dispositivos, célula nem unidade móvel.", "La barra empieza en las vidas calculadas en el plan de cada segmento y suma pasos de 5 mil (clínica y seguro de salud) o 20 mil (estado y país). VAN, TIR, payback, captación y el valuation de Help Cure se recalculan al instante. En todos los segmentos la ronda incluye la Fase 1 (desarrollo), que es fija; en la clínica, una Fase 1 reducida, sin dispositivos, célula ni unidad móvil.", "The slider starts at the lives estimated in each segment’s plan and adds steps of 5,000 (clinic and health plan) or 20,000 (state and country). NPV, IRR, payback, funding and Help Cure’s valuation recalculate instantly. In every segment the round includes Phase 1 (development), which is fixed; for the clinic, a lean Phase 1 with no devices, cell or mobile unit.", "p")}</div>
    <div class="ctabs" role="tablist">{"".join(tabs)}</div>{"".join(cases)}
    {T("Como calculamos: mesmo motor do simulador de vidas do plano de negócios (out/2026). VPL a 20% a.a.; valuation por fluxo descontado à TIR de 25% exigida pelo investidor, com saída no ano 7 a 6× o EBITDA e dividendos de 50% do caixa livre. A rodada de cada segmento inclui a Fase 1 (US$ 4,8 mi; na clínica, a enxuta de US$ 3,7 mi) e 15% de reserva. Na clínica, o suporte ganha escala com o número de clínicas, como nos demais segmentos. Todo segmento tem pelo menos 8 meses de desenvolvimento e implantação antes da primeira receita, e o payback conta desde o início desse período. Acima das vidas calculadas, a curva é extrapolada na mesma proporção, sem teste de capacidade de mercado.", "Cómo calculamos: el mismo motor del simulador de vidas del plan de negocios (oct/2026). VAN al 20% anual; valuation por flujo descontado a la TIR del 25% exigida por el inversionista, con salida en el año 7 a 6× el EBITDA y dividendos del 50% de la caja libre. La ronda de cada segmento incluye la Fase 1 (US$ 4,8 M; en la clínica, la reducida de US$ 3,7 M) y 15% de reserva. En la clínica, el soporte gana escala con el número de clínicas, como en los demás segmentos. Todo segmento tiene al menos 8 meses de desarrollo e implantación antes del primer ingreso, y el payback se cuenta desde el inicio de ese período. Por encima de las vidas calculadas, la curva se extrapola en la misma proporción, sin prueba de capacidad de mercado.", "How we calculate: the same engine as the business plan’s lives simulator (Oct 2026). NPV at 20% a year; valuation by discounted cash flow at the investor’s required 25% IRR, with exit in year 7 at 6× EBITDA and 50% of free cash paid as dividends. Each segment’s round includes Phase 1 (US$ 4.8M; for the clinic, the lean US$ 3.7M one) and a 15% reserve. For the clinic, support scales with the number of clinics, as in the other segments. Every segment has at least 8 months of development and deployment before its first revenue, and payback is counted from the start of that period. Above the estimated lives, the curve is extrapolated in the same proportion, with no market-capacity test.", "p", "vnote2", attrs=' style="margin-top:22px;font-size:13.5px"')}
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <div class="head">{T("Captação", "Captación", "Funding", "span", "eyebrow")}{T("Quanto entra depende de quais escopos o investidor financia.", "Cuánto entra depende de qué alcances financia el inversionista.", "How much comes in depends on which scopes the investor funds.", "h2")}{T("Toda rodada começa pela Fase 1 (US$ 4,8 mi). A captação de cada escopo é o caixa necessário até o ponto de equilíbrio, com 30% de folga. A rodada = Fase 1 + escopos financiados + 15% de reserva, liberada em tranches ligadas a marcos.", "Toda ronda empieza por la Fase 1 (US$ 4,8 M). La captación de cada alcance es la caja necesaria hasta el punto de equilibrio, con 30% de margen. La ronda = Fase 1 + alcances financiados + 15% de reserva, liberada en tramos ligados a hitos.", "Every round starts with Phase 1 (US$ 4.8M). Each scope’s funding is the cash needed to break even, with a 30% buffer. The round = Phase 1 + funded scopes + 15% reserve, released in milestone-linked tranches.", "p", "muted")}</div>
    <div class="tw"><table class="t" style="color:#E9F3F0">
      <thead><tr><th>{T("Perfil do investidor", "Perfil del inversionista", "Investor profile")}</th><th>{T("Escopos", "Alcances", "Scopes")}</th><th style="text-align:right">{T("Captação (US$)", "Captación (US$)", "Funding (US$)")}</th></tr></thead>
      <tbody>{tr}</tbody></table></div>
    {T("Projeções do modelo financeiro do Help Cure (out/2026), com premissas de planejamento e preços a validar com os primeiros clientes. Não são resultados realizados nem garantia de retorno. Estrutura tributária e societária a validar por assessores antes de qualquer rodada.", "Proyecciones del modelo financiero de Help Cure (oct/2026), con premisas de planificación y precios a validar con los primeros clientes. No son resultados realizados ni garantía de retorno. Estructura tributaria y societaria a validar por asesores antes de cualquier ronda.", "Projections from Help Cure’s financial model (Oct 2026), with planning assumptions and prices to be validated with the first clients. They are not actual results or a guarantee of return. Tax and corporate structure to be validated by advisors before any round.", "p", "muted", attrs=' style="margin-top:24px;font-size:14px"')}
    <p style="margin-top:20px"><a class="btn primary" href="mailto:investidores@helpcure.com.py">{T("Falar com a equipe", "Hablar con el equipo", "Talk to the team")}</a></p>
  </div>
</section>
<script src="assets/viabilidade-dados.js?v=1"></script><script src="assets/viabilidade-motor.js?v=1"></script><script src="assets/viabilidade.js?v=1" defer></script>
<script>
document.querySelectorAll('.ctabs button').forEach(function(b){{b.onclick=function(){{document.querySelectorAll('.ctabs button').forEach(function(x){{x.setAttribute('aria-selected',x===b)}});document.querySelectorAll('.case').forEach(function(c){{c.classList.toggle('on',c.id==='c-'+b.dataset.c)}})}}}});
</script>
'''
    shell(pg, "investir.html", title, b,
          "Investir no Help Cure: modelo de receita por pessoa monitorada, duas fases de investimento e cinco escopos de implantação, da clínica ao país.",
          extra_head='\n<meta name="robots" content="noindex,nofollow">\n<style>\n' + INV_CSS + '</style>')
