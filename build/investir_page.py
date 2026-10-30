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
         S("Clínicas e hospitais de porte médio para cima (a partir de cerca de 35 mil pacientes ativos): a plataforma e a implantação no sistema de cada clínica, sem dispositivos, sem célula de atendimento e sem unidade móvel. Se a clínica for a primeira a investir, paga a Fase 1 cheia e fica com a cota fundadora. Cada clínica monitora 2.000 vidas no Ano 5 (cerca de 3% de uma base de 67 mil pacientes), com crescimento de 10% ao ano; a rede cresce clínica a clínica, no Paraguai ou no Brasil, com os preços e impostos de cada país.",
           "Clínicas y hospitales de tamaño mediano en adelante (desde unos 35 mil pacientes activos): la plataforma y la implantación en el sistema de cada clínica, sin dispositivos, sin célula de atención y sin unidad móvil. Si la clínica es la primera en invertir, paga la Fase 1 completa y se queda con la cuota fundadora. Cada clínica monitorea 2.000 vidas en el Año 5 (cerca del 3% de una base de 67 mil pacientes), con crecimiento del 10% anual; la red crece clínica por clínica, en Paraguay o en Brasil, con los precios e impuestos de cada país.",
           "Mid-size and larger clinics and hospitals (from about 35,000 active patients): the platform and deployment into each clinic’s system, with no devices, no care cell and no mobile unit. If the clinic is the first to invest, it pays the full Phase 1 and takes the founder share. Each clinic monitors 2,000 lives in Year 5 (about 3% of a 67,000-patient base), growing 10% a year; the network grows clinic by clinic, in Paraguay or Brazil, with each country’s prices and taxes."),
         [(S("US$ 133 mil", "US$ 133 mil", "US$ 133k"), S("Receita por ano, por cliente", "Ingresos por año, por cliente", "Revenue per year, per client")),
          (S("73%", "73%", "73%"), TIR), (yrs("1,1"), PAY),
          (S("US$ 42 mil", "US$ 42 mil", "US$ 42k"), S("Captação por cliente", "Captación por cliente", "Funding per client"))],
         [(S("Mensalidade fixa", "Mensualidad fija", "Fixed monthly fee"), S("US$ 5.500 da instituição", "US$ 5.500 de la institución", "US$ 5,500 from the institution")),
          (S("Por paciente", "Por paciente", "Per patient"), S("pagos por usuário, governo ou plano (2.000 vidas por clínica no Ano 5)", "pagados por el usuario, el gobierno o el seguro (2.000 vidas por clínica en el Año 5)", "paid by the user, government or health plan (2,000 lives per clinic in Year 5)")),
          (S("Integração", "Integración", "Integration"), S("US$ 20 mil com o sistema da clínica (única despesa de capital)", "US$ 20 mil con el sistema de la clínica (único gasto de capital)", "US$ 20k with the clinic’s system (the only capital expense)"))],
         [(PRES, S("HelpCure na sua Clínica · Para o Médico", "HelpCure en su Clínica · Para el Médico", "HelpCure in your Clinic · For Doctors"), True),
          (RES, S("1 cliente-tipo", "1 cliente tipo", "1 typical client"), False),
          (PLAN, aba("E1"), True), (VID, VID35, False)]),
        ("e2", S("E2 · Plano de saúde", "E2 · Seguro de salud", "E2 · Health plan"),
         S("Uma operadora nacional (~3,5 mi de beneficiários, porte de Amil, Bradesco Saúde e SulAmérica). No Ano 5, metade dos candidatos usa o Help Cure: idosos com hipertensão ou diabetes e todas as crianças e adolescentes, com a pulseira com GPS para os pais — cerca de 545 mil vidas (15,6% da carteira). Diluído na carteira, o custo sobe a mensalidade média em 1,98%.",
           "Una aseguradora nacional (~3,5 M de beneficiarios, del tamaño de Amil, Bradesco Saúde y SulAmérica). En el Año 5, la mitad de los candidatos usa Help Cure: adultos mayores con hipertensión o diabetes y todos los niños y adolescentes, con la pulsera con GPS para los padres — unas 545 mil vidas (15,6% de la cartera). Diluido en la cartera, el costo sube la cuota media un 1,98%.",
           "A national health plan (~3.5M members, the size of Amil, Bradesco Saúde and SulAmérica). In Year 5, half of the candidates use Help Cure: older adults with hypertension or diabetes and all children and teenagers, with the GPS wristband for parents — about 545,000 lives (15.6% of members). Spread across all members, the cost raises the average premium by 1.98%."),
         [(S("US$ 97,7 mi", "US$ 97,7 M", "US$ 97.7M"), REC5), (S("186%", "186%", "186%"), TIR), (yrs("2,0"), PAY),
          (S("US$ 2,8 mi", "US$ 2,8 M", "US$ 2.8M"), CAP)],
         [(S("Por beneficiário", "Por beneficiario", "Per member"), S("monitorado por mês; fixo + variável por economia comprovada (modelo CASSI)", "monitoreado por mes; fijo + variable por ahorro comprobado (modelo CASSI)", "monitored per month; fixed + variable on proven savings (CASSI model)")),
          (S("Teto", "Techo", "Cap"), S("= economia do plano de saúde em internações e pronto-socorro evitados", "= ahorro del seguro de salud en internaciones y urgencias evitadas", "= the plan’s savings on avoided admissions and ER visits")),
          (S("Alta monitorada", "Alta monitoreada", "Monitored discharge"), S("por episódio", "por episodio", "per episode"))],
         [(PRES, S("Unimed-BH e CASSI", "Unimed-BH y CASSI", "Unimed-BH and CASSI"), True),
          (RES, S("Unimed-BH e CASSI", "Unimed-BH y CASSI", "Unimed-BH and CASSI"), True),
          (PLAN, aba("E2"), True),
          (VID, S("CASSI (pronto) · genérico a fazer", "CASSI (listo) · genérico por hacer", "CASSI (ready) · generic to do"), True)]),
        ("e3", S("E3 · Estado", "E3 · Estado", "E3 · State"),
         S("Secretaria estadual de saúde, planos, empresas e cidadãos de um estado. Volumes de mercado pela média dos estados em prospecção (RJ, SP, MG, BA, CE e PR): no Ano 5, 2% da população sem plano e 2,4% dos beneficiários de planos.",
           "Secretaría estatal de salud, seguros, empresas y ciudadanos de un estado. Volúmenes de mercado por el promedio de los estados en prospección (RJ, SP, MG, BA, CE y PR): en el Año 5, 2% de la población sin seguro y 2,4% de los beneficiarios de seguros.",
           "A state health department, plus health plans, employers and citizens of one state. Market volumes from the average of the states in prospection (RJ, SP, MG, BA, CE and PR): in Year 5, 2% of the population without a plan and 2.4% of health-plan members."),
         [(S("US$ 69,0 mi", "US$ 69,0 M", "US$ 69.0M"), REC5), (S("57%", "57%", "57%"), TIR), (yrs("4,0"), PAY),
          (S("US$ 4,7 mi", "US$ 4,7 M", "US$ 4.7M"), CAP)],
         [(S("Governo", "Gobierno", "Government"), S("por cidadão coberto no atendimento móvel + contrato anual por célula pública", "por ciudadano cubierto en la atención móvil + contrato anual por célula pública", "per citizen covered by mobile care + annual contract per public cell")),
          (S("Planos, empresas e academias", "Seguros, empresas y gimnasios", "Plans, employers and gyms"), S("por pessoa e por célula instalada", "por persona y por célula instalada", "per person and per installed cell")),
          (S("Royalty RAPP", "Royalty RAPP", "RAPP royalty"), S("por vida monitorada; só o investimento local no estado", "por vida monitoreada; solo la inversión local en el estado", "per monitored life; only the local investment in the state"))],
         [(PRES, S("Bahia · Ceará · Ecossistema", "Bahía · Ceará · Ecosistema", "Bahia · Ceará · Ecosystem"), True),
          (RES, S("Bahia e Ceará (a alinhar)", "Bahía y Ceará (por alinear)", "Bahia and Ceará (to align)"), True),
          (PLAN, aba("E3"), True), (VID, VID35, False)]),
        ("e4", S("E4 · Paraguai", "E4 · Paraguay", "E4 · Paraguay"),
         S("O país-piloto da Fase 2: a plataforma já existe, então só entram os custos de aplicação no Paraguai. Volumes de mercado: 6,1 mi de habitantes (censo 2022), cerca de 7% com seguro privado; no Ano 5, 2% da população sem seguro e 2,4% dos segurados.",
           "El país piloto de la Fase 2: la plataforma ya existe, así que solo entran los costos de aplicación en Paraguay. Volúmenes de mercado: 6,1 M de habitantes (censo 2022), cerca del 7% con seguro privado; en el Año 5, 2% de la población sin seguro y 2,4% de los asegurados.",
           "Phase 2’s pilot country: the platform already exists, so only the costs of deploying in Paraguay come in. Market volumes: 6.1M people (2022 census), about 7% privately insured; in Year 5, 2% of the uninsured population and 2.4% of the insured."),
         [(S("US$ 19,9 mi", "US$ 19,9 M", "US$ 19.9M"), REC5),
          (S("> 100%", "> 100%", "> 100%"), S("TIR (plataforma paga na Fase 1)", "TIR (plataforma pagada en la Fase 1)", "IRR (platform paid in Phase 1)")),
          (yrs("1,8"), PAY),
          (S("US$ 0,35 mi", "US$ 0,35 M", "US$ 0.35M"), S("Captação (+ Fase 1)", "Captación (+ Fase 1)", "Funding (+ Phase 1)"))],
         [(S("Por pessoa/mês", "Por persona/mes", "Per person/month"), S("usuário US$ 9,90 · governo US$ 10 · plano US$ 12 · empregador US$ 3", "usuario US$ 9,90 · gobierno US$ 10 · seguro US$ 12 · empleador US$ 3", "user US$ 9.90 · government US$ 10 · plan US$ 12 · employer US$ 3")),
          (S("Células e unidades móveis", "Células y unidades móviles", "Cells and mobile units"), S("por entidade e por região de saúde", "por entidad y por región sanitaria", "per entity and per health region")),
          (S("Royalty RAPP", "Royalty RAPP", "RAPP royalty"), S("US$ 0,60 por vida monitorada por mês, como nos demais segmentos", "US$ 0,60 por vida monitoreada por mes, como en los demás segmentos", "US$ 0.60 per monitored life per month, as in the other segments"))],
         [(PRES, S("Plano de Negócios Paraguai (a atualizar)", "Plan de Negocios Paraguay (por actualizar)", "Paraguay Business Plan (to update)"), True),
          (RES, S("ES/PT", "ES/PT", "ES/PT"), True),
          (PLAN, aba("E4"), True), (VID, VID35, False)]),
        ("e5", S("E5 · Brasil", "E5 · Brasil", "E5 · Brazil"),
         S("Camada nacional de monitoramento integrada à RNDS e aos programas do Ministério da Saúde, mais planos e cidadãos. Volumes de mercado: no Ano 5, 2% dos 160 mi de brasileiros sem plano e 2,4% dos 53 mi de beneficiários — o potencial com todos os estados aderindo.",
           "Capa nacional de monitoreo integrada a la RNDS y a los programas del Ministerio de Salud de Brasil, más seguros y ciudadanos. Volúmenes de mercado: en el Año 5, 2% de los 160 M de brasileños sin seguro y 2,4% de los 53 M de beneficiarios — el potencial con todos los estados adhiriendo.",
           "A national monitoring layer integrated with Brazil’s RNDS and Ministry of Health programs, plus health plans and citizens. Market volumes: in Year 5, 2% of the 160M Brazilians without a plan and 2.4% of the 53M plan members — the potential with every state joining."),
         [(S("US$ 658 mi", "US$ 658 M", "US$ 658M"), REC5), (S("85%", "85%", "85%"), TIR), (yrs("3,8"), PAY),
          (S("US$ 30,1 mi", "US$ 30,1 M", "US$ 30.1M"), CAP)],
         [(S("Governo", "Gobierno", "Government"), S("per capita por cidadão coberto, no espírito do PMAE", "per cápita por ciudadano cubierto, en la línea del PMAE", "per capita per covered citizen, in the spirit of PMAE")),
          (S("Planos", "Seguros", "Health plans"), S("via integração RNDS–ANS", "vía integración RNDS–ANS", "via RNDS–ANS integration")),
          (S("Certificação RNDS/FHIR", "Certificación RNDS/FHIR", "RNDS/FHIR certification"), S("no Ano 0; royalty RAPP por vida", "en el Año 0; royalty RAPP por vida", "in Year 0; RAPP royalty per life"))],
         [(PRES, S("Brasil Vital Grid · Ministério", "Brasil Vital Grid · Ministerio", "Brasil Vital Grid · Ministry"), True),
          (RES, S("Ministério da Saúde (a alinhar)", "Ministerio de Salud (por alinear)", "Ministry of Health (to align)"), True),
          (PLAN, aba("E5"), True), (VID, VID35, False)]),
    ]

    def viab(code):
        clin = code == "E1"
        if clin:
            code = "E1PY"
        lab = S("Vidas monitoradas no Ano 5 (2.000 por clínica)", "Vidas monitoreadas en el Año 5 (2.000 por clínica)", "Lives monitored in Year 5 (2,000 per clinic)") if clin else \
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
                  ("vpdiv", S("Valor da divisão de lucros ao fundador", "Valor de la participación en utilidades del fundador", "Value of the founder’s profit share")),
                  ("participacao", S("% da Help Cure a vender (com divisão de lucros)", "% de Help Cure a vender (con participación en utilidades)", "% of Help Cure to sell (with profit share)")),
                  ("semdiv", S("% a vender sem divisão de lucros", "% a vender sin participación en utilidades", "% to sell without profit share"))]
            val = '<div class="vrow">' + "".join('<div><b data-o="%s">—</b>%s</div>' % (o, T(*l)) for o, l in v4) + '</div>'
        pais = ('<div class="vpais" role="group" aria-label="País">'
                '<button type="button" data-p="E1PY" aria-pressed="true">%s</button><button type="button" data-p="E1BR" aria-pressed="false">%s</button>'
                '%s</div>' % (T("Paraguai", "Paraguay", "Paraguay"), T("Brasil", "Brasil", "Brazil"),
                              T("Preços e impostos de cada país · Fase 1 cheia (US$ 4,8 mi), com divisão de lucros ao fundador",
                                "Precios e impuestos de cada país · Fase 1 completa (US$ 4,8 M), con participación en utilidades del fundador",
                                "Each country’s prices and taxes · full Phase 1 (US$ 4.8M), with the founder’s profit share", cls="vpn"))) if clin else ""
        return f'''<div class="viab" data-esc="{code}">
  {pais}
  <div class="vbar">
    <div class="vsl">
      <div class="vtop">{T(*lab, cls="vlab")}<b class="vn" data-o="vidas">—</b><span class="vd" data-o="delta"></span></div>
      <input type="range" min="0" max="0" step="1" value="0" aria-label="{html.escape(lab[0])}">
      <div class="vends"><span data-o="min"></span><button class="vreset" type="button">{T("Voltar à referência", "Volver a la referencia", "Back to the reference")}</button><span data-o="max"></span></div>
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
        (S("Royalty RAPP: US$ 0,60 por vida", "Royalty RAPP: US$ 0,60 por vida", "RAPP royalty: US$ 0.60 per life"), S("Por vida monitorada por mês, pago à Moulin, detentora do motor RAPP. Equivale a 4–5% da receita nos segmentos de escala.", "Por vida monitoreada por mes, pagado a Moulin, titular del motor RAPP. Equivale al 4–5% de los ingresos en los segmentos de escala.", "Per monitored life per month, paid to Moulin, owner of the RAPP engine. About 4–5% of revenue in the scale segments.")),
        (S("Investidor fundador: lucro + equity", "Inversionista fundador: utilidades + equity", "Founder investor: profit + equity"), S("Quem financia a Fase 1 recebe 10% do lucro (EBITDA) da rede e um percentual da Help Cure, negociado pelo valuation.", "Quien financia la Fase 1 recibe el 10% de las utilidades (EBITDA) de la red y un porcentaje de Help Cure, negociado por el valuation.", "Whoever funds Phase 1 receives 10% of the network’s profit (EBITDA) and a stake in Help Cure, negotiated on the valuation.")),
    ]
    mc = "".join('<div class="card"><div class="in">%s%s</div></div>' % (T(*a, tag="h3"), T(*b, tag="p")) for a, b in modelo)

    rows = [
        (S("Cota fundadora — Fase 1 (24 meses)", "Cuota fundadora — Fase 1 (24 meses)", "Founder share — Phase 1 (24 months)"), S("10% do lucro de toda a rede por 10 anos + equity", "10% de las utilidades de toda la red por 10 años + equity", "10% of the whole network’s profit for 10 years + equity"), S("4,8 mi em 3 tranches", "4,8 M en 3 tramos", "4.8M in 3 tranches")),
        (S("Rede de clínicas (Paraguai ou Brasil)", "Red de clínicas (Paraguay o Brasil)", "Clinic network (Paraguay or Brazil)"), S("Fase 1 + E1 + reserva", "Fase 1 + E1 + reserva", "Phase 1 + E1 + reserve"), S("6,9 mi (30 clínicas) a 7,7 mi (50)", "6,9 M (30 clínicas) a 7,7 M (50)", "6.9M (30 clinics) to 7.7M (50)")),
        (S("Investidor no Paraguai", "Inversionista en Paraguay", "Investor in Paraguay"), S("Fase 1 + E4 + reserva", "Fase 1 + E4 + reserva", "Phase 1 + E4 + reserve"), S("5,9 mi", "5,9 M", "5.9M")),
        (S("Investidor regional no Brasil", "Inversionista regional en Brasil", "Regional investor in Brazil"), S("Fase 1 + E2 + E3 + reserva", "Fase 1 + E2 + E3 + reserva", "Phase 1 + E2 + E3 + reserve"), S("14,1 mi", "14,1 M", "14.1M")),
        (S("Parceiro nacional no Brasil", "Socio nacional en Brasil", "National partner in Brazil"), S("Fase 1 + E5 + reserva", "Fase 1 + E5 + reserva", "Phase 1 + E5 + reserve"), S("40,0 mi", "40,0 M", "40.0M")),
        (S("Investidor global", "Inversionista global", "Global investor"), S("Fase 1 + E4 + E5 + 2 planos de saúde + reserva", "Fase 1 + E4 + E5 + 2 seguros de salud + reserva", "Phase 1 + E4 + E5 + 2 health plans + reserve"), S("≈ 46,9 mi, em tranches", "≈ 46,9 M, en tramos", "≈ 46.9M, in tranches")),
    ]
    tr = "".join("<tr><td>%s</td><td>%s</td><td class=\"n\">%s</td></tr>" % (T(*a), T(*b), T(*c)) for a, b, c in rows)

    b = f'''
<div class="hero sub">
  <img src="img/central.webp" alt="">
  <div class="wrap">
    {T("Investidores", "Inversionistas", "Investors", "span", "eyebrow")}
    {T("Uma plataforma, cinco escopos de implantação.", "Una plataforma, cinco alcances de implantación.", "One platform, five deployment scopes.", "h1")}
    {T("O Help Cure é pago por pessoa monitorada, todo mês. O investidor escolhe a abrangência: uma clínica, um plano de saúde, um estado ou um país. Receita, retorno e captação variam com o escopo; a plataforma é a mesma.", "Help Cure se paga por persona monitoreada, cada mes. El inversionista elige el alcance: una clínica, un seguro de salud, un estado o un país. Ingresos, retorno y captación varían con el alcance; la plataforma es la misma.", "Help Cure is paid per monitored person, every month. The investor chooses the reach: a clinic, a health plan, a state or a country. Revenue, return and funding vary with the scope; the platform is the same.", "p", "lead")}
    {kpis([(S("10% do lucro", "10% de las utilidades", "10% of profit"), S("da rede ao investidor fundador, além do equity", "de la red al inversionista fundador, además del equity", "of the network to the founder investor, plus equity")),
           (S("US$ 0,60", "US$ 0,60", "US$ 0.60"), S("Royalty RAPP por vida monitorada por mês", "Royalty RAPP por vida monitoreada por mes", "RAPP royalty per monitored life per month")),
           (S("US$ 4,8 mi", "US$ 4,8 M", "US$ 4.8M"), S("Fase 1: desenvolvimento, piloto e 24 meses da empresa", "Fase 1: desarrollo, piloto y 24 meses de la empresa", "Phase 1: development, pilot and 24 months of the company")),
           (S("1% a 46%", "1% a 46%", "1% to 46%"), S("Da Help Cure a vender ao fundador, conforme o segmento", "De Help Cure a vender al fundador, según el segmento", "Of Help Cure to sell to the founder, by segment"))])}
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
    <div class="head">{T("A plataforma", "La plataforma", "The platform", "span", "eyebrow")}{T("Duas fases: desenvolver uma vez, aplicar por escopo.", "Dos fases: desarrollar una vez, aplicar por alcance.", "Two phases: build once, deploy by scope.", "h2")}{T("<b>Fase 1</b> (Paraguai, 24 meses): plataforma, piloto (com uma unidade móvel protótipo) e manutenção da empresa, pagos uma vez — US$ 4,8 mi em três tranches por marcos. <b>Fase 2</b>: cada escopo de aplicação carrega só o que é dele — dispositivos, células, unidades móveis, equipe adicional e infraestrutura — e paga o royalty RAPP: US$ 0,60 por vida monitorada por mês.", "<b>Fase 1</b> (Paraguay, 24 meses): plataforma, piloto (con una unidad móvil prototipo) y mantenimiento de la empresa, pagados una sola vez — US$ 4,8 M en tres tramos por hitos. <b>Fase 2</b>: cada alcance de aplicación lleva solo lo suyo — dispositivos, células, unidades móviles, equipo adicional e infraestructura — y paga el royalty RAPP: US$ 0,60 por vida monitoreada por mes.", "<b>Phase 1</b> (Paraguay, 24 months): platform, pilot (with one prototype mobile unit) and company upkeep, paid once — US$ 4.8M in three milestone tranches. <b>Phase 2</b>: each deployment scope carries only its own costs — devices, cells, mobile units, extra staff and infrastructure — and pays the RAPP royalty: US$ 0.60 per monitored life per month.", "p", raw=True)}</div>
    <div class="g g4">{mc}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head">{T("Viabilidade por segmento", "Viabilidad por segmento", "Feasibility by segment", "span", "eyebrow")}{T("Escolha o segmento e mova a barra de vidas.", "Elija el segmento y mueva la barra de vidas.", "Pick a segment and move the lives slider.", "h2")}{T("A barra começa nas vidas calculadas (estimativas de mercado), pode descer para cenários mais conservadores e anda em passos de 2 mil na clínica (uma clínica a mais por passo), 20 mil no plano de saúde, no estado e no Paraguai e 100 mil no Brasil. VPL, TIR, payback, captação, valuation e o percentual da Help Cure a vender recalculam na hora. Em cada segmento o investidor é o fundador: paga a Fase 1 (fixa), o segmento e a reserva, recebe 10% do lucro e o percentual da empresa.", "La barra empieza en las vidas calculadas (estimaciones de mercado), puede bajar a escenarios más conservadores y avanza en pasos de 2 mil en la clínica (una clínica más por paso), 20 mil en el seguro de salud, el estado y Paraguay y 100 mil en Brasil. VAN, TIR, payback, captación, valuation y el porcentaje de Help Cure a vender se recalculan al instante. En cada segmento el inversionista es el fundador: paga la Fase 1 (fija), el segmento y la reserva, y recibe el 10% de las utilidades y el porcentaje de la empresa.", "The slider starts at the estimated lives (market estimates), can go down to more conservative cases and moves in steps of 2,000 for the clinic (one more clinic per step), 20,000 for the health plan, the state and Paraguay and 100,000 for Brazil. NPV, IRR, payback, funding, valuation and the share of Help Cure to sell recalculate instantly. In each segment the investor is the founder: pays Phase 1 (fixed), the segment and the reserve, and receives 10% of profit plus the stake.", "p")}</div>
    <div class="ctabs" role="tablist">{"".join(tabs)}</div>{"".join(cases)}
    {T("Como calculamos: o mesmo motor da planilha de equity do Help Cure (out/2026). VPL a 20% a.a. O percentual a vender é o que dá ao investidor exatamente 25% a.a., somando divisão de lucros, dividendos (50% do caixa livre) e saída no ano 7 a 6× o EBITDA. A divisão de lucros é de 10% do EBITDA positivo por 10 anos; ao chegar a 5× a Fase 1, cai para 1%. A rodada inclui a Fase 1 (US$ 4,8 mi) e 15% de reserva. Todo segmento tem pelo menos 8 meses de desenvolvimento antes da primeira receita; o payback conta desde o início. Acima das vidas calculadas, a curva é extrapolada na mesma proporção.", "Cómo calculamos: el mismo motor de la planilla de equity de Help Cure (oct/2026). VAN al 20% anual. El porcentaje a vender es el que da al inversionista exactamente 25% anual, sumando participación en utilidades, dividendos (50% de la caja libre) y salida en el año 7 a 6× el EBITDA. La participación es del 10% del EBITDA positivo por 10 años; al llegar a 5× la Fase 1, baja al 1%. La ronda incluye la Fase 1 (US$ 4,8 M) y 15% de reserva. Todo segmento tiene al menos 8 meses de desarrollo antes del primer ingreso; el payback se cuenta desde el inicio. Por encima de las vidas calculadas, la curva se extrapola en la misma proporción.", "How we calculate: the same engine as Help Cure’s equity spreadsheet (Oct 2026). NPV at 20% a year. The share to sell is the one that gives the investor exactly 25% a year, adding profit share, dividends (50% of free cash) and exit in year 7 at 6× EBITDA. The profit share is 10% of positive EBITDA for 10 years; once it reaches 5× Phase 1, it drops to 1%. The round includes Phase 1 (US$ 4.8M) and a 15% reserve. Every segment has at least 8 months of development before its first revenue; payback counts from the start. Above the estimated lives, the curve is extrapolated in the same proportion.", "p", "vnote2", attrs=' style="margin-top:22px;font-size:13.5px"')}
  </div>
</section>

<section class="soft" id="fundador">
  <div class="wrap">
    <div class="head">{T("Divisão de lucros", "Participación en utilidades", "Profit share", "span", "eyebrow")}{T("O fundador ganha com toda a rede, e vende-se menos da empresa.", "El fundador gana con toda la red, y se vende menos de la empresa.", "The founder earns on the whole network, and less of the company is sold.", "h2")}{T("A Fase 1 é paga uma única vez. A primeira entidade que financiar — um plano de saúde, um governo, um investidor ou uma rede de clínicas — vira sócia da Help Cure e recebe 10% do lucro de todos os segmentos que entrarem depois. Quanto mais a rede cresce, menor o percentual da empresa que precisa ser vendido.", "La Fase 1 se paga una sola vez. La primera entidad que la financie — un seguro de salud, un gobierno, un inversionista o una red de clínicas — se vuelve socia de Help Cure y recibe el 10% de las utilidades de todos los segmentos que entren después. Cuanto más crece la red, menor el porcentaje de la empresa que hay que vender.", "Phase 1 is paid only once. The first entity to fund it — a health plan, a government, an investor or a clinic network — becomes a Help Cure shareholder and receives 10% of the profit of every segment that joins afterwards. The more the network grows, the smaller the stake that has to be sold.", "p")}</div>
    <div class="g g4 frules">
      <div class="card"><div class="in">{T("US$ 4,8 mi, uma vez", "US$ 4,8 M, una vez", "US$ 4.8M, once", "h3")}{T("Fase 1: desenvolvimento, piloto e 24 meses da empresa, em três tranches ligadas a marcos.", "Fase 1: desarrollo, piloto y 24 meses de la empresa, en tres tramos ligados a hitos.", "Phase 1: development, pilot and 24 months of the company, in three milestone tranches.", "p")}</div></div>
      <div class="card"><div class="in">{T("10% do lucro da rede", "10% de las utilidades de la red", "10% of network profit", "h3")}{T("Do EBITDA positivo de todos os segmentos, por 10 anos a partir da primeira receita.", "Del EBITDA positivo de todos los segmentos, por 10 años desde el primer ingreso.", "Of every segment’s positive EBITDA, for 10 years from the first revenue.", "p")}</div></div>
      <div class="card"><div class="in">{T("Teto de 5×", "Techo de 5×", "5× cap", "h3")}{T("Ao receber 5 vezes a Fase 1, a participação cai para 1% e fica assim.", "Al recibir 5 veces la Fase 1, la participación baja al 1% y queda así.", "Once it has received 5 times Phase 1, the share drops to 1% and stays there.", "p")}</div></div>
      <div class="card"><div class="in">{T("E sócio da empresa", "Y socio de la empresa", "And a shareholder", "h3")}{T("O percentual da Help Cure é negociado pelo valuation e fecha a TIR de 25% a.a.", "El porcentaje de Help Cure se negocia por el valuation y cierra la TIR del 25% anual.", "The Help Cure stake is negotiated on the valuation and closes the 25% annual IRR.", "p")}</div></div>
    </div>
    <div class="fund" aria-live="polite">
      <h3 style="margin:34px 0 0">{T("Até onde a rede chega?", "¿Hasta dónde llega la red?", "How far does the network go?")}</h3>
      <div class="ctabs fcen" role="tablist">
        <button role="tab" aria-selected="true" data-f="R1">{T("Paraguai + plano de saúde", "Paraguay + seguro de salud", "Paraguay + health plan")}</button>
        <button role="tab" aria-selected="false" data-f="R2">{T("+ um estado", "+ un estado", "+ a state")}</button>
        <button role="tab" aria-selected="false" data-f="R3">{T("Paraguai, Brasil, estado e 2 planos", "Paraguay, Brasil, estado y 2 seguros", "Paraguay, Brazil, a state and 2 plans")}</button>
        <button role="tab" aria-selected="false" data-f="R4">{T("Rede de clínicas fundadora + Paraguai, plano e estado", "Red de clínicas fundadora + Paraguay, seguro y estado", "Founder clinic network + Paraguay, plan and state")}</button>
      </div>
      <p class="vst" data-f="msg"></p>
      <div class="kpis vk">
        <div class="kpi"><b data-f="e">—</b>{T("% da Help Cure a vender", "% de Help Cure a vender", "% of Help Cure to sell")}</div>
        <div class="kpi"><b data-f="pre">—</b>{T("Valuation pré-money", "Valuation pre-money", "Pre-money valuation")}</div>
        <div class="kpi"><b data-f="rod">—</b>{T("Rodada (Fase 1 + segmentos + reserva)", "Ronda (Fase 1 + segmentos + reserva)", "Round (Phase 1 + segments + reserve)")}</div>
      </div>
      <div class="vrow">
        <div><b data-f="vpd">—</b>{T("Valor da divisão de lucros ao fundador", "Valor de la participación en utilidades", "Value of the profit share")}</div>
        <div><b data-f="e0">—</b>{T("% a vender sem divisão de lucros", "% a vender sin participación", "% to sell without profit share")}</div>
        <div><b data-f="rec">—</b>{T("Receita da rede no ano 7", "Ingresos de la red en el año 7", "Network revenue in year 7")}</div>
        <div><b data-f="mult">—</b>{T("Múltiplo do investidor", "Múltiplo del inversionista", "Investor multiple")}</div>
      </div>
      <div class="vchart">
        <div class="vch-h">{T("Divisão de lucros recebida pelo fundador, por ano desde a assinatura", "Participación en utilidades recibida por el fundador, por año desde la firma", "Profit share received by the founder, per year from signing", "h3")}</div>
        <div class="vsvg fsvg"></div><div class="vtip ftip" role="status"></div>
        <details><summary>{T("Ver em tabela", "Ver en tabla", "View as table")}</summary><div class="tw"><table class="t ftab"></table></div></details>
      </div>
      {T("Segmentos entram em sequência (Ano 0 em t2, t3 ou t4), com as vidas do plano de cada um; a rede de clínicas tem 30 clínicas de porte médio (60 mil vidas). A divisão de lucros depois do ano 7 entra pelo valor presente. Estrutura de equity, divisão de lucros e royalty a validar com advogado e tributarista no Paraguai e no Brasil antes de qualquer oferta.", "Los segmentos entran en secuencia (Año 0 en t2, t3 o t4), con las vidas del plan de cada uno; la red de clínicas tiene 30 clínicas medianas (60 mil vidas). La participación después del año 7 entra por su valor presente. Estructura de equity, participación en utilidades y royalty a validar con abogado y asesor tributario en Paraguay y Brasil antes de cualquier oferta.", "Segments come in sequence (Year 0 at t2, t3 or t4), with each plan’s lives; the clinic network has 30 mid-size clinics (60,000 lives). The profit share after year 7 enters at present value. Equity, profit-share and royalty structure to be validated with legal and tax advisors in Paraguay and Brazil before any offer.", "p", "vnote2", attrs=' style="margin-top:18px;font-size:13.5px"')}
    </div>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <div class="head">{T("Captação", "Captación", "Funding", "span", "eyebrow")}{T("Rodada, valuation e quanto vender, por perfil de investidor.", "Ronda, valuation y cuánto vender, por perfil de inversionista.", "Round, valuation and how much to sell, by investor profile.", "h2")}{T("Toda rodada começa pela Fase 1 (US$ 4,8 mi). A rodada = Fase 1 + captação dos segmentos (caixa até o equilíbrio, com 30% de folga) + 15% de reserva, liberada em tranches ligadas a marcos. O percentual a vender já considera a divisão de lucros de 10% ao fundador.", "Toda ronda empieza por la Fase 1 (US$ 4,8 M). La ronda = Fase 1 + captación de los segmentos (caja hasta el equilibrio, con 30% de margen) + 15% de reserva, liberada en tramos ligados a hitos. El porcentaje a vender ya considera la participación del 10% en utilidades del fundador.", "Every round starts with Phase 1 (US$ 4.8M). The round = Phase 1 + segment funding (cash to break even, with a 30% buffer) + 15% reserve, released in milestone-linked tranches. The share to sell already reflects the founder’s 10% profit share.", "p", "muted")}</div>
    <div class="tw"><table class="t" style="color:#E9F3F0">
      <thead><tr><th>{T("Perfil do investidor fundador", "Perfil del inversionista fundador", "Founder investor profile")}</th><th style="text-align:right">{T("Rodada (US$)", "Ronda (US$)", "Round (US$)")}</th><th style="text-align:right">{T("Pré-money (US$)", "Pre-money (US$)", "Pre-money (US$)")}</th><th style="text-align:right">{T("% da Help Cure a vender", "% de Help Cure a vender", "% of Help Cure to sell")}</th></tr></thead>
      <tbody id="captab"></tbody></table></div>
    {T("Projeções do modelo financeiro do Help Cure (out/2026), com premissas de planejamento e preços a validar com os primeiros clientes. Não são resultados realizados nem garantia de retorno. Estrutura tributária e societária a validar por assessores antes de qualquer rodada.", "Proyecciones del modelo financiero de Help Cure (oct/2026), con premisas de planificación y precios a validar con los primeros clientes. No son resultados realizados ni garantía de retorno. Estructura tributaria y societaria a validar por asesores antes de cualquier ronda.", "Projections from Help Cure’s financial model (Oct 2026), with planning assumptions and prices to be validated with the first clients. They are not actual results or a guarantee of return. Tax and corporate structure to be validated by advisors before any round.", "p", "muted", attrs=' style="margin-top:24px;font-size:14px"')}
    <p style="margin-top:20px"><a class="btn primary" href="mailto:investidores@helpcure.com.py">{T("Falar com a equipe", "Hablar con el equipo", "Talk to the team")}</a></p>
  </div>
</section>
<script src="assets/viabilidade-dados.js?v=6"></script><script src="assets/modelo-motor.js?v=1"></script><script src="assets/viabilidade.js?v=5" defer></script><script src="assets/rede.js?v=3" defer></script>
<script>
document.querySelectorAll('.ctabs:not(.fcen) button').forEach(function(b){{b.onclick=function(){{document.querySelectorAll('.ctabs:not(.fcen) button').forEach(function(x){{x.setAttribute('aria-selected',x===b)}});document.querySelectorAll('.case').forEach(function(c){{c.classList.toggle('on',c.id==='c-'+b.dataset.c)}})}}}});
</script>
'''
    shell(pg, "investir.html", title, b,
          "Investir no Help Cure: modelo de receita por pessoa monitorada, duas fases de investimento e cinco escopos de implantação, da clínica ao país.",
          extra_head='\n<meta name="robots" content="noindex,nofollow">\n<style>\n' + INV_CSS + '</style>')
