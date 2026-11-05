import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter as L

wb = openpyxl.Workbook()
wb.remove(wb.active)
DARK = "0B3B36"
F_T = Font(name="Arial", size=13, bold=True, color="FFFFFF")
FILL_T = PatternFill("solid", fgColor=DARK)
F_H = Font(name="Arial", size=10, bold=True, color=DARK)
F_B = Font(name="Arial", size=10, bold=True)
F_N = Font(name="Arial", size=10)
F_IN = Font(name="Arial", size=10, color="0000FF")
F_LK = Font(name="Arial", size=10, color="008000")
F_NOTE = Font(name="Arial", size=9, italic=True, color="5B6B67")
FILL_IN = PatternFill("solid", fgColor="FFFF00")
FILL_TOT = PatternFill("solid", fgColor="E9F1EE")
FILL_HDR = PatternFill("solid", fgColor="D5E5E0")
USD = '\\$#,##0;"($"#,##0\\);\\-'
USD2 = '\\$#,##0.00;"($"#,##0.00\\);\\-'
NUM = '#,##0;\\(#,##0\\);\\-'
PCT = '0.0%;\\(0.0%\\);\\-'
YEARS = ["Ano 0", "Ano 1", "Ano 2", "Ano 3", "Ano 4", "Ano 5"]
COLS = "BCDEFG"

def sheet(name, title, sub, widths=(60, 15, 15, 15, 15, 15, 15, 15, 15, 15)):
    ws = wb.create_sheet(name)
    for i, w in enumerate(widths):
        ws.column_dimensions[L(i + 1)].width = w
    ws["A1"] = title; ws["A1"].font = F_T
    for c in range(1, len(widths) + 1):
        ws.cell(1, c).fill = FILL_T
    if sub:
        ws["A2"] = sub; ws["A2"].font = F_NOTE
        ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=min(len(widths), 8))
        ws.row_dimensions[2].height = 42
    ws.sheet_view.showGridLines = False
    return ws

def put(ws, ref, v, kind="f", fmt=None, bold=False, note=None):
    c = ws[ref]; c.value = v
    if kind == "in":
        c.font = F_IN; c.fill = FILL_IN
    elif kind == "lk":
        c.font = F_LK
    elif kind == "lbl":
        c.font = F_B if bold else F_N
    else:
        c.font = F_B if bold else F_N
    if fmt: c.number_format = fmt
    if note: c.comment = Comment(note, "Help Farm")
    return c

def hdr(ws, r, text, labels=None, start=2):
    put(ws, f"A{r}", text).font = F_H
    if labels:
        for i, t in enumerate(labels):
            c = ws.cell(r, start + i, t); c.font = F_H; c.fill = FILL_HDR
            c.alignment = Alignment(horizontal="center", wrap_text=True)
        ws.cell(r, 1).fill = FILL_HDR

def tot(ws, r, cols):
    ws.cell(r, 1).font = F_B
    for c in cols:
        ws[f"{c}{r}"].font = F_B; ws[f"{c}{r}"].fill = FILL_TOT
    ws.cell(r, 1).fill = FILL_TOT

# =====================================================================
# Leia-me
# =====================================================================
ws = sheet("Leia-me", "HELP FARM — MODELO POR ABRANGÊNCIA DE IMPLANTAÇÃO (RENTABILIDADE)", None, (130,))
lines = [
    ("Um único modelo em duas fases, no mesmo formato do modelo Help Cure. FASE 1 — Desenvolvimento (Paraguai, empresa Help Farm): plataforma, piloto e manutenção da empresa com 24 meses de capital de giro. FASE 2 — Aplicação: cinco escopos de abrangência (E1–E5) que só carregam custos incrementais (kits de campo em comodato, equipe adicional, unidade móvel, instalação, certificação). Valores em USD.", F_N),
    ("", F_N),
    ("Premissas desta versão (pedido de 03/11/2026)", F_H),
    ("• Entidade principal = FAZENDA. Cada escopo informa quantas fazendas ativas há em cada perfil (mista, grãos, leite, corte, alto valor). Cooperativas entram como licença B2B2F; seguradoras e bancos como contratos do produto de risco.", F_N),
    ("• Desenvolvimento (aba F1_Desenvolvimento, bloco A) com os MESMOS valores do Help Cure (US$ 2,47 mi com contingência). Os itens foram descritos para o agro, mas os números são idênticos.", F_N),
    ("• Uma unidade móvel de campo (mesmo CAPEX e OPEX da unidade móvel do Help Cure). Ela é comprada no piloto da Fase 1 e passa a operar no escopo Paraguai (E2). Nenhum escopo compra outra unidade enquanto a premissa ficar em 1.", F_N),
    ("• Sem células de atendimento nesta versão. Onde não há unidade móvel, a instalação é feita pela equipe de campo (custo por fazenda nova, aba Precos).", F_N),
    ("", F_N),
    ("Como usar", F_H),
    ("1. A aba Precos guarda a tabela de preços por faixa de país (C = Paraguai, Argentina, América Central; B = Brasil, Uruguai, México; A = EUA, Canadá, Oceania, Europa do norte), os custos variáveis, os kits de campo por unidade e os cinco perfis de fazenda. Mude ali e todos os escopos mudam.", F_N),
    ("2. Cada aba E1–E5 é um escopo. Células azuis com fundo amarelo são as premissas editáveis (faixa, regime, equipe, fazendas por perfil, cooperativas, contratos de risco, unidade móvel, royalty, comissão de parceiro).", F_N),
    ("3. A aba Resumo compara os cinco escopos (receita, EBITDA, TIR, VPL, payback, necessidade de caixa e captação) e monta a rodada: marque 1 nos escopos financiados.", F_N),
    ("4. A aba Rentabilidade_HelpFarm consolida Fase 1 + escopos marcados numa linha do tempo de 7 anos: fluxo de caixa da empresa, TIR e VPL do projeto, payback, valor de saída, valor da empresa hoje, participação justa para o investidor e sensibilidade de 10% a 40%.", F_N),
    ("5. Regra de coerência (igual ao Help Cure): o desenvolvimento é pago UMA vez, na Fase 1. Nenhum escopo da Fase 2 carrega custo de plataforma; cada um paga royalty sobre a receita (remuneração do motor RAPP, que fica na detentora) e só o investimento local.", F_N),
    ("6. Captação sugerida = pior saldo de caixa acumulado × fator de segurança (aba Precos).", F_N),
    ("", F_N),
    ("Legenda de cores", F_H),
    ("Azul com fundo amarelo = premissa editável · Preto = fórmula · Verde = ligação com outra aba · Verde-claro = totais", F_N),
    ("", F_N),
    ("Origem das premissas", F_H),
    ("Preços por unidade e faixas de país: Help Farm — Pesquisa de mercado RAPP-Agro v2 (02/11/2026), camadas A–E; referências de mercado verificadas: CowMed R$ 22–23/vaca/mês, Halter a partir de NZ$ 9,90/vaca/mês, SenseHub NZ$ 2,55–4,41, smaXtec €2,50 + bolus €35, Taranis US$ 1,50–2/ha/ano, xarvio ~€10/ha/ano, John Deere See & Spray US$ 5/acre, Cropin ~US$ 50 mil/ano por cliente empresarial.", F_N),
    ("Custos de kit: estação US$ 1.500 (Davis, faixa US$ 500–1.500), sonda de solo US$ 150, gateway LoRaWAN + edge US$ 800 cada, bolus ~US$ 45 (smaXtec €35), balança de passagem US$ 3.500, kit de vibração/corrente US$ 400 — premissas MTS a cotar.", F_N),
    ("Fase 1 (desenvolvimento, capital de giro) e unidade móvel (CAPEX US$ 234.652; OPEX US$ 4.150/mês): copiados do modelo HelpCure_Modelo_por_Abrangencia_v2_Precos_Estudo.xlsx. Volumes de fazendas por escopo: premissas MTS a validar com a equipe comercial.", F_N),
]
for i, (t, f) in enumerate(lines, start=2):
    c = ws.cell(i, 1, t); c.font = f; c.alignment = Alignment(wrap_text=True, vertical="top")

# =====================================================================
# Precos
# =====================================================================
P = sheet("Precos", "PREÇOS POR FAIXA DE PAÍS, CUSTOS UNITÁRIOS E PERFIS DE FAZENDA (USD)", None,
          (52, 13, 13, 13, 13, 13, 12, 16, 16, 60))
hdr(P, 3, "A. Preço por unidade monitorada, por faixa de país")
labels = ["C", "B", "A", "Unidade", "Base", "Divisor p/ mês", "Custo variável (mesma base)", "Kit em comodato (USD/unid.)", "Fonte / referência"]
hdr(P, 4, "Item  (faixa C = PY, AR, Am. Central · B = BR, UY, MX · A = EUA, CA, AU, NZ, UE norte)", labels)
P.row_dimensions[4].height = 40
units = [
    ("Assinatura da fazenda (plataforma, painel, alertas)", 50, 60, 100, "fazenda", "mês", 1, 0, 0, "FieldView C$ 499/ano; Agworld A$ 1.695–3.995/ano (pesquisa nov/2026)"),
    ("Pecuária de corte (brinco oficial + balança + bolus sentinela)", 0.35, 0.45, 1.20, "cabeça", "mês", 1, 0.08, 3, "Kit: bolus em 5% do rebanho × US$ 60. Ref.: brinco SENACSA US$ 0,95 pago pelo Estado; Smart Paddock A$ 2/mês; cerca virtual US$ 1,5–4/mês + colar"),
    ("Pecuária de leite (bolus ou colar em comodato)", 3.0, 4.0, 5.0, "vaca", "mês", 1, 0.70, 45, "Cowmed R$ 22–23/vaca/mês (~US$ 4); SenseHub IE €3,50; Halter NZ$ 9,90 (~US$ 5,7)"),
    ("Lavoura de grãos (satélite + solo + clima)", 4.0, 6.0, 12.0, "hectare", "ano", 12, 0.40, 4.2, "Kit: estação US$ 1.500 a cada 500 ha + sonda US$ 150 a cada 125 ha. Ref.: OneSoil €5–6/ha; vistoria EUA US$ 15–22/ha; Solinftec ~US$ 5/ha"),
    ("Alto valor (fruta, café, hortaliça)", 25, 30, 60, "hectare", "ano", 12, 1.50, 15, "Kit: sonda US$ 150 a cada 10 ha. Ref.: Manna até US$ 5/ha/mês; sensores US$ 30–250/ha/ano"),
    ("Máquinas, pivôs e bombas (vibração + corrente + CAN)", 20, 25, 40, "ativo", "mês", 1, 6, 400, "Ref.: JDLink US$ 200/ano; telemetria US$ 27–50/mês; bomba A$ 15/mês; pivô ~US$ 440/ano"),
    ("Gateway LoRaWAN + edge RAPP + conectividade (Starlink/4G)", 0, 0, 0, "gateway", "mês", 1, 120, 1600, "2 gateways × US$ 800; conectividade US$ 120/mês"),
    ("Balança de passagem (pecuária de corte)", 0, 0, 0, "balança", "mês", 1, 0, 3500, "Premissa MTS a cotar"),
    ("Estação meteorológica adicional (alto valor)", 0, 0, 0, "estação", "mês", 1, 0, 1500, "Davis Vantage Pro2 US$ 1.455"),
]
for i, u in enumerate(units):
    r = 5 + i
    put(P, f"A{r}", u[0], "lbl")
    for j, col in enumerate("BCD"):
        put(P, f"{col}{r}", u[1 + j], "in", USD2)
    put(P, f"E{r}", u[4], "lbl"); put(P, f"F{r}", u[5], "lbl")
    put(P, f"G{r}", u[6], "in", "0")
    put(P, f"H{r}", u[7], "in", USD2)
    put(P, f"I{r}", u[8], "in", USD2)
    put(P, f"J{r}", u[9], "lbl").font = F_NOTE

hdr(P, 15, "B. Outras receitas por faixa")
hdr(P, 16, "Item", ["C", "B", "A"])
others = [
    (17, "Implantação por fazenda nova (taxa única, USD)", 7500, 9000, 15000, USD, "Visita da unidade móvel, drone, gateway e calibração. Ref.: grid de solo US$ 8–25/ha por coleta; smaXtec instalação €800 + base €4–5,5 mil"),
    (18, "Licença B2B2F por cooperativa / laticínio / trading (USD/ano)", 30000, 36000, 60000, USD, "Cropin ~US$ 50 mil/ano por cliente; pilotos US$ 10–40 mil"),
    (19, "Produto de risco — contrato com seguradora ou banco (USD/ano)", 50000, 60000, 100000, USD, "≈ US$ 1/ha/ano sobre 50 mil ha. Ref.: CMN 5.267/2025 obriga sensoriamento no crédito >300 ha; prêmio PSR ~US$ 93/ha (1–3% = US$ 1–3/ha); laudo Proagro R$ 330"),
]
for r, a, c1, c2, c3, fm, src in others:
    put(P, f"A{r}", a, "lbl")
    for col, v in zip("BCD", (c1, c2, c3)):
        put(P, f"{col}{r}", v, "in", fm)
    put(P, f"J{r}", src, "lbl").font = F_NOTE
put(P, "A20", "Desconto nas unidades para fazendas contratadas via cooperativa", "lbl")
put(P, "B20", 0.20, "in", PCT)
put(P, "J20", "Cooperativa fatura o associado (modelo Farm Source / SenseHub)", "lbl").font = F_NOTE

hdr(P, 22, "C. Perfis de fazenda — unidades monitoradas por fazenda")
PROF = ["Mista", "Grãos", "Leite", "Corte", "Alto valor"]
hdr(P, 23, "Unidade  (as linhas seguem a ordem da tabela A)", PROF)
prof_units = [
    ("Assinatura da fazenda", [1, 1, 1, 1, 1]),
    ("Cabeças de corte", [1000, 0, 0, 5000, 0]),
    ("Vacas de leite", [0, 0, 300, 0, 0]),
    ("Hectares de grãos", [2000, 5000, 0, 0, 0]),
    ("Hectares de alto valor", [0, 0, 0, 0, 200]),
    ("Máquinas, pivôs e bombas", [10, 6, 3, 3, 2]),
    ("Gateways", [1, 2, 1, 2, 1]),
    ("Balanças de passagem", [1, 0, 0, 1, 0]),
    ("Estações meteorológicas adicionais", [0, 0, 0, 0, 1]),
]
for i, (a, vals) in enumerate(prof_units):
    r = 24 + i
    put(P, f"A{r}", a, "lbl")
    for j, v in enumerate(vals):
        put(P, f"{'BCDEF'[j]}{r}", v, "in", NUM)
# computed rows 34..38
hdr(P, 33, "Resultado por fazenda (USD/mês)", PROF)
calc = [(34, "Receita por fazenda/mês — faixa C", "$B$5:$B$13"),
        (35, "Receita por fazenda/mês — faixa B", "$C$5:$C$13"),
        (36, "Receita por fazenda/mês — faixa A", "$D$5:$D$13")]
for r, a, rng in calc:
    put(P, f"A{r}", a, "lbl")
    for col in "BCDEF":
        put(P, f"{col}{r}", f"=SUMPRODUCT({rng}/$G$5:$G$13,{col}$24:{col}$32)", "f", USD)
put(P, "A37", "Custo variável por fazenda/mês", "lbl")
put(P, "A38", "Kit de campo em comodato por fazenda (CAPEX)", "lbl")
put(P, "A39", "Margem por fazenda/mês — faixa C", "lbl")
for col in "BCDEF":
    put(P, f"{col}37", f"=SUMPRODUCT($H$5:$H$13/$G$5:$G$13,{col}$24:{col}$32)", "f", USD)
    put(P, f"{col}38", f"=SUMPRODUCT($I$5:$I$13,{col}$24:{col}$32)", "f", USD)
    put(P, f"{col}39", f"=IF({col}34=0,0,({col}34-{col}37)/{col}34)", "f", PCT)
# faixa code helper for MATCH
put(P, "G33", "Faixa", "lbl").font = F_H
for r, code in zip((34, 35, 36), "CBA"):
    put(P, f"G{r}", code, "lbl")
put(P, "J34", "Fazenda mista-tipo: 2.000 ha + 1.000 cab corte + 10 máquinas (pesquisa v2: US$ 1.317/mês, kit US$ 20.500)", "lbl").font = F_NOTE

hdr(P, 41, "D. Custos unitários e parâmetros")
params = [
    (42, "Unidade móvel completa — CAPEX (motorhome 4x4 + adaptação + 2 motos trail + instrumentos portáteis e drones)", 230000, USD, "Premissa do usuário, 04/11/2026: ~US$ 230 mil. Instrumentos e drones ≈ US$ 54–60 mil (HelpFarm_Equipamentos_Unidade_Movel.xlsx); restante para motorhome, adaptação e motos"),
    (43, "Unidade móvel — OPEX mensal (combustível, manutenção, seguro, Starlink, calibração)", 4150, USD, "Mesmo valor do Help Cure; inclui ~US$ 450/mês de recorrentes dos instrumentos"),
    (44, "Instalação por fazenda nova — equipe de campo (USD, pago pela Help Farm)", 1500, USD, "Premissa MTS: deslocamento + 2 técnicos × 3 dias"),
    (45, "Marketing e vendas (% da receita)", 0.08, PCT, "Igual ao Help Cure"),
    (46, "Crescimento anual do custo da equipe", 0.08, PCT, "Igual ao Help Cure"),
    (47, "Fator de segurança sobre a necessidade de caixa (captação)", 1.3, "0.00", "Igual ao Help Cure"),
    (48, "Imposto sobre EBITDA positivo — PY (IRE)", 0.10, PCT, ""),
    (49, "Imposto sobre EBITDA positivo — BR / outros (Lucro Real, proxy)", 0.34, PCT, "Usado como proxy conservador para AR, UY, EUA e AU"),
    (50, "WACC — PY", 0.20, PCT, ""),
    (51, "WACC — BR / outros", 0.20, PCT, ""),
]
for r, a, v, fm, src in params:
    put(P, f"A{r}", a, "lbl"); put(P, f"B{r}", v, "in", fm)
    put(P, f"J{r}", src, "lbl").font = F_NOTE
P.freeze_panes = "B5"

# =====================================================================
# F1_Desenvolvimento
# =====================================================================
F = sheet("F1_Desenvolvimento", "FASE 1 — DESENVOLVIMENTO E MANUTENÇÃO DA EMPRESA (PARAGUAI, HELP FARM) — USD",
          "Valores do desenvolvimento IGUAIS aos do Help Cure (orçamento MTS 29/10/2026), por instrução do usuário; descrições adaptadas ao agro. Faixas baixa/alta; o modelo usa o ponto médio. Piloto sem célula, com 1 unidade móvel de campo. Nenhum escopo da Fase 2 repete estes custos.",
          (78, 14, 14, 15, 60))
hdr(F, 4, "A. Desenvolvimento da plataforma (24 meses)")
hdr(F, 5, "Item", ["Baixa", "Alta", "Ponto médio", "Base"])
dev = [
    ("Plataforma central: cadastro de fazendas, talhões, rebanhos e ativos; identidade, consentimento e propriedade do dado; APIs", 280000, 420000, "Mesmo valor do Help Cure (núcleo multi-entidade)"),
    ("Aplicativos: produtor e capataz (Android/iOS), painel do técnico/veterinário, painel da cooperativa, central de monitoramento (web)", 320000, 480000, "Mesmo valor do Help Cure (4 produtos de interface)"),
    ("Ingestão de dispositivos: LoRaWAN, brinco oficial (SENACSA/SISBOV), bolus/colar, estações, sondas, CAN/ISOBUS, APIs de máquinas", 150000, 250000, "Mesmo valor do Help Cure"),
    ("Motor RAPP de análise e predição: assinatura basal de talhão, animal e máquina; séries temporais; desvios; NDVI/NDRE Sentinel-2", 280000, 420000, "Licença de uso da detentora remunerada por royalty na Fase 2"),
    ("Interoperabilidade: SENACSA/SIAP, SISBOV/PNIB, ZARC, seguradoras e bancos (índice de risco), John Deere/FieldView APIs", 150000, 240000, "Mesmo valor do Help Cure"),
    ("Software de campo e da unidade móvel: instalação de kits, operação offline com sincronização, console de campo", 90000, 150000, "Mesmo valor do Help Cure (equivalente ao software das células e unidades)"),
    ("Engenharia da unidade móvel de campo: projeto do contêiner 20 pés, energia, conectividade (satélite/4G), drone e kit de instalação", 40000, 80000, "Mesmo valor do Help Cure"),
    ("Qualidade do dado e observabilidade (AIOps): nota de confiança, alertas técnicos, autorremediação", 70000, 110000, "Mesmo valor do Help Cure"),
    ("Segurança, LGPD / Lei 7593/2025 PY, testes de invasão, homologação ANATEL dos rádios", 120000, 200000, "Mesmo valor do Help Cure (no agro substitui o dossiê SaMD)"),
    ("QA, validação com o piloto (5 fazendas) e métricas agronômicas e veterinárias", 90000, 160000, "Mesmo valor do Help Cure"),
    ("Gestão de produto, UX e design", 90000, 150000, "1 PM + 1 designer por 24 meses, parcial"),
    ("Infraestrutura de nuvem e ferramentas de desenvolvimento (24 meses)", 60000, 96000, "US$ 2,5–4 mil/mês"),
]
for i, (a, lo, hi, src) in enumerate(dev):
    r = 6 + i
    put(F, f"A{r}", a, "lbl"); F[f"A{r}"].alignment = Alignment(wrap_text=True)
    put(F, f"B{r}", lo, "in", USD); put(F, f"C{r}", hi, "in", USD)
    put(F, f"D{r}", f"=(B{r}+C{r})/2", "f", USD)
    put(F, f"E{r}", src, "lbl").font = F_NOTE
put(F, "A18", "Subtotal desenvolvimento", "lbl")
for col in "BCD":
    put(F, f"{col}18", f"=SUM({col}6:{col}17)", "f", USD)
tot(F, 18, "BCD")
put(F, "A19", "Contingência sobre o desenvolvimento", "lbl"); put(F, "B19", 0.10, "in", PCT)
put(F, "A20", "TOTAL DESENVOLVIMENTO (ponto médio + contingência)", "lbl")
put(F, "D20", "=D18*(1+B19)", "f", USD); tot(F, 20, "D")

hdr(F, 22, "B. Piloto (5 fazendas, sem célula, 1 unidade móvel)")
put(F, "A23", "Fazendas-piloto (coluna B) × kit de campo da fazenda mista-tipo", "lbl")
put(F, "B23", 5, "in", NUM)
put(F, "D23", "=B23*Precos!$B$38", "lk", USD)
put(F, "E23", "kit mista-tipo da aba Precos (comodato no piloto)", "lbl").font = F_NOTE
put(F, "A24", "1 unidade móvel completa (motorhome 4x4 adaptado + 2 motos trail + instrumentos e drones) — passa a operar no escopo E2", "lbl")
put(F, "D24", "=Precos!$B$42", "lk", USD)
put(F, "E24", "mesmo custo do Help Cure (aba Precos)", "lbl").font = F_NOTE
put(F, "A25", "Protótipos: drone multiespectral, balança portátil, bancada de vibração, bolus de teste", "lbl")
put(F, "D25", 40000, "in", USD)
put(F, "E25", "estimativa MTS (mesmo valor dos protótipos do Help Cure)", "lbl").font = F_NOTE
put(F, "A26", "Operação do piloto: unidade móvel + custo variável das fazendas (meses em campo → coluna B)", "lbl")
put(F, "B26", 18, "in", NUM)
put(F, "D26", "=(Precos!$B$43+B23*Precos!$B$37)*B26", "lk", USD)
put(F, "E26", "OPEX da unidade móvel + custo variável da fazenda mista-tipo", "lbl").font = F_NOTE
put(F, "A27", "TOTAL PILOTO", "lbl"); put(F, "D27", "=SUM(D23:D26)", "f", USD); tot(F, 27, "D")

hdr(F, 29, "C. Manutenção da empresa no Paraguai — capital de giro")
cg = [(30, "Pessoal da empresa (USD/mês)", 20000), (31, "Escritório, contabilidade, jurídico, seguros (USD/mês)", 4000),
      (32, "Marketing, site, campanha e comercial (USD/mês)", 3000), (33, "Viagens e representação (USD/mês)", 2000)]
for r, a, v in cg:
    put(F, f"A{r}", a, "lbl"); put(F, f"B{r}", v, "in", USD)
put(F, "E30", "Mesmos valores do Help Cure (estimativa do Fábio, 29/10/2026)", "lbl").font = F_NOTE
put(F, "A34", "Meses de capital de giro reservados", "lbl"); put(F, "B34", 24, "in", NUM)
put(F, "A35", "TOTAL CAPITAL DE GIRO (24 meses)", "lbl"); put(F, "D35", "=SUM(B30:B33)*B34", "f", USD); tot(F, 35, "D")

hdr(F, 37, "D. Captação da Fase 1")
put(F, "A38", "Desenvolvimento + piloto + capital de giro", "lbl"); put(F, "D38", "=D20+D27+D35", "f", USD)
put(F, "A39", "Fator de segurança (aba Precos)", "lbl"); put(F, "D39", "=Precos!$B$47", "lk", "0.00")
put(F, "A40", "CAPTAÇÃO SUGERIDA — FASE 1", "lbl"); put(F, "D40", "=D38*D39", "f", USD); tot(F, 40, "D")
hdr(F, 42, "Tranches sugeridas (ligadas a marcos)", ["%", "", "USD", "Quando"])
tr = [(43, "Tranche 1 — início: equipe, arquitetura, apps do piloto, projeto da unidade móvel", 0.35, "mês 1"),
      (44, "Tranche 2 — 5 fazendas-piloto com kit instalado; motor RAPP v1 com basal; unidade móvel montada", 0.35, "mês 8"),
      (45, "Tranche 3 — 1º alerta antecipado documentado por domínio; 1ª cooperativa contratada; homologação ANATEL protocolada", 0.30, "mês 16")]
for r, a, p, q in tr:
    put(F, f"A{r}", a, "lbl"); F[f"A{r}"].alignment = Alignment(wrap_text=True)
    put(F, f"B{r}", p, "in", PCT); put(F, f"D{r}", f"=B{r}*$D$40", "f", USD); put(F, f"E{r}", q, "lbl")

# =====================================================================
# Scope sheets
# =====================================================================
scopes = [
    dict(sh="E1_Cooperativa", title="E1 · Cooperativa paraguaia (B2B2F, 1 cooperativa)",
         sub="Uma cooperativa (ex.: Colonias Unidas, Chortitzer, Fernheim, Neuland, Pirapó) licencia a plataforma e leva o RAPP aos associados. A plataforma já existe (Fase 1). Instalação pela equipe de campo; a unidade móvel opera no escopo E2.",
         faixa="C", reg="PY", meses=3, equipe=6000, ti=0.03, integ=0, roy=0.10, parc=0, coop_pct=1.0, implant=1, um_exist=0,
         farms={"Mista": [0, 3, 8, 12, 15, 18], "Grãos": [0, 2, 5, 8, 10, 12], "Leite": [0, 2, 5, 8, 10, 12],
                "Corte": [0, 3, 7, 12, 15, 18], "Alto valor": [0, 0, 0, 0, 0, 0]},
         coops=[0, 1, 1, 1, 1, 1], risk=[0, 0, 0, 0, 0, 0], um=[0, 0, 0, 0, 0, 0]),
    dict(sh="E2_Paraguai", title="E2 · País: Paraguai (piloto-país)",
         sub="Piloto-país da Fase 2: produtores diretos + cooperativas (B2B2F) + produto de risco para seguradoras e bancos (Mapfre PY, AFD). Opera a unidade móvel comprada no piloto da Fase 1. Base-alvo ~3.490 fazendas grandes (3% dos 116.224 donos de gado produzem 61%).",
         faixa="C", reg="PY", meses=6, equipe=18000, ti=0.03, integ=0, roy=0.10, parc=0, coop_pct=0.4, implant=1, um_exist=1,
         farms={"Mista": [0, 9, 24, 45, 69, 96], "Grãos": [0, 8, 20, 38, 58, 80], "Leite": [0, 5, 12, 22, 34, 48],
                "Corte": [0, 7, 20, 37, 57, 80], "Alto valor": [0, 1, 4, 8, 12, 16]},
         coops=[0, 1, 2, 3, 4, 5], risk=[0, 0, 1, 2, 2, 3], um=[1, 1, 1, 1, 1, 1]),
    dict(sh="E3_Brasil", title="E3 · País: Brasil (faixa B, após homologação ANATEL)",
         sub="Escala no Brasil: leite e corte primeiro (PNIB 2027–2032), depois grãos. Concorre com CowMed (leite) somando máquinas e lavoura. Sem unidade móvel: instalação pela equipe de campo. CAPEX de certificação ANATEL/LGPD no Ano 0.",
         faixa="B", reg="BR", meses=6, equipe=35000, ti=0.03, integ=120000, roy=0.10, parc=0, coop_pct=0.4, implant=1, um_exist=0,
         farms={"Mista": [0, 4, 16, 40, 75, 120], "Grãos": [0, 3, 12, 30, 55, 90], "Leite": [0, 7, 28, 70, 135, 210],
                "Corte": [0, 5, 20, 50, 95, 150], "Alto valor": [0, 1, 4, 10, 20, 30]},
         coops=[0, 1, 3, 5, 8, 10], risk=[0, 0, 1, 2, 3, 4], um=[0, 0, 0, 0, 0, 0]),
    dict(sh="E4_ConeSul", title="E4 · Cone Sul: Uruguai + Argentina (faixa C, cobrança em US$)",
         sub="Rastreabilidade bovina obrigatória e base RFID estatal (SNIG, SENASA). Entrada com seguradora (BSE ~70% do seguro agrícola no UY) e grupos CREA. Imposto pelo proxy BR. Sem unidade móvel.",
         faixa="C", reg="BR", meses=6, equipe=20000, ti=0.03, integ=40000, roy=0.10, parc=0, coop_pct=0.3, implant=1, um_exist=0,
         farms={"Mista": [0, 3, 12, 27, 45, 66], "Grãos": [0, 3, 10, 22, 37, 55], "Leite": [0, 1, 6, 14, 23, 33],
                "Corte": [0, 3, 12, 27, 45, 66], "Alto valor": [0, 0, 0, 0, 0, 0]},
         coops=[0, 0, 1, 2, 3, 3], risk=[0, 1, 1, 2, 2, 3], um=[0, 0, 0, 0, 0, 0]),
    dict(sh="E5_FaixaA", title="E5 · Faixa A: EUA / Austrália via parceiro local",
         sub="Camada preditiva sobre dados de coleiras, pivôs e máquinas já instalados (APIs), com revenda ou integrador local que fica com comissão. Kit pode ser vendido com reembolso NRCS/EQIP nos EUA. Certificação FCC/ISED no Ano 0. Imposto pelo proxy BR.",
         faixa="A", reg="BR", meses=9, equipe=40000, ti=0.03, integ=150000, roy=0.10, parc=0.25, coop_pct=0.2, implant=1, um_exist=0,
         farms={"Mista": [0, 2, 8, 20, 36, 56], "Grãos": [0, 3, 12, 30, 54, 84], "Leite": [0, 4, 15, 38, 68, 105],
                "Corte": [0, 1, 5, 12, 22, 35], "Alto valor": [0, 0, 0, 0, 0, 0]},
         coops=[0, 0, 1, 1, 2, 2], risk=[0, 0, 0, 1, 1, 2], um=[0, 0, 0, 0, 0, 0]),
]

def build_scope(s):
    ws = sheet(s["sh"], s["title"], s["sub"])
    hdr(ws, 4, "PREMISSAS DO ESCOPO")
    prem = [
        (5, "Faixa de preço (C / B / A — aba Precos)", s["faixa"], None),
        (6, "Regime tributário (PY / BR)", s["reg"], None),
        (7, "Meses de implantação no Ano 0", s["meses"], NUM),
        (8, "Equipe ADICIONAL da Fase 2 — custo mensal (Ano 0 e 1)", s["equipe"], USD),
        (9, "Infraestrutura de TI adicional (nuvem, satélite, licenças) — % da receita", s["ti"], PCT),
        (10, "CAPEX de integração / certificação local (Ano 0)", s["integ"], USD),
        (11, "Royalty da plataforma RAPP (% da receita)", s["roy"], PCT),
        (12, "Comissão de parceiro / revenda local (% da receita)", s["parc"], PCT),
        (13, "% das fazendas contratadas via cooperativa (recebem o desconto B2B2F)", s["coop_pct"], PCT),
        (14, "Cobra taxa de implantação por fazenda nova? (1 = sim, 0 = não)", s["implant"], NUM),
        (15, "Unidades móveis já existentes, vindas da Fase 1 (sem novo CAPEX)", s["um_exist"], NUM),
    ]
    for r, a, v, fm in prem:
        put(ws, f"A{r}", a, "lbl"); put(ws, f"B{r}", v, "in", fm)
    hdr(ws, 16, "Fazendas ativas (média do ano) por perfil", YEARS)
    for i, p in enumerate(PROF):
        r = 17 + i
        put(ws, f"A{r}", p, "lbl")
        for j, col in enumerate(COLS):
            put(ws, f"{col}{r}", s["farms"][p][j], "in", NUM)
    put(ws, "A22", "Total de fazendas ativas", "lbl")
    for col in COLS:
        put(ws, f"{col}22", f"=SUM({col}17:{col}21)", "f", NUM)
    tot(ws, 22, COLS)
    for r, a, key in [(23, "Cooperativas com licença B2B2F (acumulado)", "coops"),
                      (24, "Contratos do produto de risco — seguradoras e bancos (acumulado)", "risk"),
                      (25, "Unidades móveis em operação (acumulado)", "um")]:
        put(ws, f"A{r}", a, "lbl")
        for j, col in enumerate(COLS):
            put(ws, f"{col}{r}", s[key][j], "in", NUM)

    hdr(ws, 27, "Valores por fazenda — faixa escolhida (aba Precos)", ["Receita/mês", "Custo variável/mês", "Kit em comodato"])
    for i, p in enumerate(PROF):
        r = 28 + i
        pc = "BCDEF"[i]
        put(ws, f"A{r}", p, "lbl")
        put(ws, f"B{r}", f"=INDEX(Precos!$B$34:$F$36,MATCH($B$5,Precos!$G$34:$G$36,0),{i+1})", "lk", USD)
        put(ws, f"C{r}", f"=Precos!{pc}$37", "lk", USD)
        put(ws, f"D{r}", f"=Precos!{pc}$38", "lk", USD)
    other = [(33, "Implantação por fazenda nova (USD)", 17), (34, "Licença B2B2F (USD/ano por cooperativa)", 18),
             (35, "Produto de risco (USD/ano por contrato)", 19)]
    for r, a, pr in other:
        put(ws, f"A{r}", a, "lbl")
        put(ws, f"B{r}", f"=INDEX(Precos!$B${pr}:$D${pr},MATCH($B$5,Precos!$B$4:$D$4,0))", "lk", USD)
    put(ws, "A36", "Desconto B2B2F nas unidades", "lbl"); put(ws, "B36", "=Precos!$B$20", "lk", PCT)
    put(ws, "A37", "% do kit pago na instalação pelo cliente ou financiado por banco/cooperativa (alavanca; Help Cure usa 70% na célula)", "lbl")
    put(ws, "B37", s.get("kitpct", 0), "in", PCT)

    hdr(ws, 38, "Fazendas novas no ano (para kit, implantação e instalação)", YEARS)
    for i, p in enumerate(PROF):
        r = 39 + i; src = 17 + i
        put(ws, f"A{r}", p, "lbl")
        for j, col in enumerate(COLS):
            prev = "0" if j == 0 else f"{COLS[j-1]}{src}"
            put(ws, f"{col}{r}", f"=MAX(0,{col}{src}-{prev})", "f", NUM)
    put(ws, "A44", "Total de fazendas novas", "lbl")
    for col in COLS:
        put(ws, f"{col}44", f"=SUM({col}39:{col}43)", "f", NUM)
    tot(ws, 44, COLS)

    hdr(ws, 46, "RECEITA (USD)", YEARS)
    for i, p in enumerate(PROF):
        r = 47 + i
        put(ws, f"A{r}", f"Receita — fazendas {p.lower()}", "lbl")
        for col in COLS:
            put(ws, f"{col}{r}", f"={col}{17+i}*$B${28+i}*12*(1-$B$13*$B$36)", "f", USD)
    put(ws, "A52", "Receita — taxa de implantação + parcela do kit paga na instalação", "lbl")
    put(ws, "A53", "Receita — licenças B2B2F (cooperativas)", "lbl")
    put(ws, "A54", "Receita — produto de risco (seguradoras e bancos)", "lbl")
    put(ws, "A55", "RECEITA BRUTA TOTAL", "lbl")
    for col in COLS:
        put(ws, f"{col}52", f"={col}44*$B$33*$B$14+SUMPRODUCT({col}39:{col}43,$D$28:$D$32)*$B$37", "f", USD)
        put(ws, f"{col}53", f"={col}23*$B$34", "f", USD)
        put(ws, f"{col}54", f"={col}24*$B$35", "f", USD)
        put(ws, f"{col}55", f"=SUM({col}47:{col}54)", "f", USD)
    tot(ws, 55, COLS)

    hdr(ws, 57, "OPEX (USD)", YEARS)
    lab = [(58, "Equipe adicional"), (59, "Custo de servir (conectividade, nuvem, satélite, suporte) por fazenda"),
           (60, "Instalação das fazendas novas (equipe de campo)"), (61, "Operação da unidade móvel"),
           (62, "Marketing e vendas"), (63, "Royalty da plataforma RAPP"), (64, "Comissão de parceiro local"),
           (65, "Infraestrutura de TI adicional"), (66, "OPEX TOTAL")]
    for r, a in lab:
        put(ws, f"A{r}", a, "lbl")
    for j, col in enumerate(COLS):
        if j == 0:
            put(ws, "B58", "=$B$8*$B$7", "f", USD)
        else:
            put(ws, f"{col}58", f"=$B$8*12*(1+Precos!$B$46)^({j-1})", "f", USD)
        put(ws, f"{col}59", f"=SUMPRODUCT({col}17:{col}21,$C$28:$C$32)*12", "f", USD)
        put(ws, f"{col}60", f"={col}44*Precos!$B$44", "f", USD)
        put(ws, f"{col}61", f"={col}25*Precos!$B$43*12", "f", USD)
        put(ws, f"{col}62", f"={col}55*Precos!$B$45", "f", USD)
        put(ws, f"{col}63", f"={col}55*$B$11", "f", USD)
        put(ws, f"{col}64", f"={col}55*$B$12", "f", USD)
        put(ws, f"{col}65", f"={col}55*$B$9", "f", USD)
        put(ws, f"{col}66", f"=SUM({col}58:{col}65)", "f", USD)
    tot(ws, 66, COLS)

    hdr(ws, 68, "CAPEX (USD)", YEARS)
    put(ws, "A69", "Integração / certificação local (Ano 0)", "lbl")
    put(ws, "A70", "Kits de campo em comodato (fazendas novas × kit do perfil)", "lbl")
    put(ws, "A71", "Unidades móveis novas (além das vindas da Fase 1)", "lbl")
    put(ws, "A72", "CAPEX TOTAL", "lbl")
    for j, col in enumerate(COLS):
        put(ws, f"{col}69", "=$B$10" if j == 0 else 0, "f" if j == 0 else "in", USD)
        put(ws, f"{col}70", f"=SUMPRODUCT({col}39:{col}43,$D$28:$D$32)", "f", USD)
        if j == 0:
            put(ws, "B71", "=MAX(0,B25-$B$15)*Precos!$B$42", "f", USD)
        else:
            put(ws, f"{col}71", f"=MAX(0,{col}25-MAX({COLS[j-1]}25,$B$15))*Precos!$B$42", "f", USD)
        put(ws, f"{col}72", f"=SUM({col}69:{col}71)", "f", USD)
    tot(ws, 72, COLS)

    hdr(ws, 74, "RESULTADO E FLUXO DE CAIXA (USD)", YEARS)
    for r, a in [(75, "EBITDA"), (76, "Margem EBITDA"), (77, "(–) Imposto sobre EBITDA positivo"),
                 (78, "FLUXO DE CAIXA LIVRE"), (79, "Caixa acumulado")]:
        put(ws, f"A{r}", a, "lbl")
    for j, col in enumerate(COLS):
        put(ws, f"{col}75", f"={col}55-{col}66", "f", USD)
        put(ws, f"{col}76", f"=IF({col}55=0,0,{col}75/{col}55)", "f", PCT)
        put(ws, f"{col}77", f'=-MAX(0,{col}75)*IF($B$6="PY",Precos!$B$48,Precos!$B$49)', "f", USD)
        put(ws, f"{col}78", f"={col}75+{col}77-{col}72", "f", USD)
        put(ws, f"{col}79", "=B78" if j == 0 else f"={COLS[j-1]}79+{col}78", "f", USD)
    tot(ws, 75, COLS); tot(ws, 78, COLS)

    hdr(ws, 81, "INDICADORES (Ano 0–5)")
    ind = [
        (82, "VPL", '=B78+NPV(IF($B$6="PY",Precos!$B$50,Precos!$B$51),C78:G78)', USD),
        (83, "TIR", '=IFERROR(IRR(B78:G78,0.1),IFERROR(IRR(B78:G78,-0.3),"n/d"))', PCT),
        (84, "Payback (anos a partir do Ano 0)", '=IFERROR(MATCH(TRUE(),INDEX(C79:G79>=0,0),0)-1+(-INDEX(B79:G79,MATCH(TRUE(),INDEX(C79:G79>=0,0),0))/INDEX(C78:G78,MATCH(TRUE(),INDEX(C79:G79>=0,0),0))),">5")', "0.0"),
        (85, "Necessidade de caixa (pior saldo acumulado)", "=-MIN(0,MIN(B79:G79))", USD),
        (86, "CAPTAÇÃO SUGERIDA (necessidade × fator de segurança)", "=B85*Precos!$B$47", USD),
        (87, "Receita no Ano 5", "=G55", USD),
        (88, "EBITDA no Ano 5", "=G75", USD),
        (89, "Margem EBITDA no Ano 5", "=G76", PCT),
        (90, "Fazendas ativas no Ano 5", "=G22", NUM),
        (91, "Receita por fazenda por ano (Ano 5)", "=IF(G22=0,0,G55/G22)", USD),
        (92, "Investimento total em 5 anos (CAPEX)", "=SUM(B72:G72)", USD),
        (93, "Equipe adicional em 5 anos", "=SUM(B58:G58)", USD),
        (94, "Primeiro ano com EBITDA positivo", '=IFERROR(INDEX($B$16:$G$16,MATCH(TRUE(),INDEX(B75:G75>0,0),0)),"após Ano 5")', None),
    ]
    for r, a, f, fm in ind:
        put(ws, f"A{r}", a, "lbl", bold=(r in (82, 83, 86)))
        put(ws, f"B{r}", f, "f", fm, bold=(r in (82, 83, 86)))
    ws.freeze_panes = "B5"

for s in scopes:
    build_scope(s)

# =====================================================================
# Resumo
# =====================================================================
R = sheet("Resumo", "RESUMO — FASE 1 + OS CINCO ESCOPOS DA FASE 2 (USD)",
          "Mesmas premissas de preço e custo (aba Precos). Mude um escopo na aba dele e esta tabela acompanha.",
          (60, 19, 19, 19, 19, 19, 4))
names = ["Cooperativa PY (B2B2F)", "País: Paraguai (piloto-país)", "País: Brasil", "Cone Sul: UY + AR", "Faixa A: EUA / Austrália"]
hdr(R, 4, "Escopo", names)
R.row_dimensions[4].height = 30
rows = [(5, "Faixa de preço", "B5", None), (6, "Fazendas ativas no Ano 5", "$B$90", NUM),
        (7, "Receita no Ano 5", "$B$87", USD), (8, "EBITDA no Ano 5", "$B$88", USD),
        (9, "Margem EBITDA no Ano 5", "$B$89", PCT), (10, "Receita por fazenda por ano (Ano 5)", "$B$91", USD),
        (11, "Investimento total em 5 anos (CAPEX)", "$B$92", USD), (12, "VPL", "$B$82", USD),
        (13, "TIR", "$B$83", PCT), (14, "Payback (anos a partir do Ano 0)", "$B$84", "0.0"),
        (15, "Necessidade de caixa (pior saldo acumulado)", "$B$85", USD),
        (16, "CAPTAÇÃO SUGERIDA (necessidade × fator de segurança)", "$B$86", USD),
        (17, "Primeiro ano com EBITDA positivo", "$B$94", None)]
for r, a, ref, fm in rows:
    put(R, f"A{r}", a, "lbl", bold=(r in (13, 16)))
    for i, s in enumerate(scopes):
        put(R, f"{'BCDEF'[i]}{r}", f"={s['sh']}!{ref}", "lk", fm)
hdr(R, 19, "Receita por ano (USD)")
for j, y in enumerate(YEARS[1:], start=1):
    r = 19 + j
    put(R, f"A{r}", y, "lbl")
    for i, s in enumerate(scopes):
        put(R, f"{'BCDEF'[i]}{r}", f"={s['sh']}!{COLS[j]}55", "lk", USD)
hdr(R, 26, "EBITDA por ano (USD)")
for j, y in enumerate(YEARS[1:], start=1):
    r = 26 + j
    put(R, f"A{r}", y, "lbl")
    for i, s in enumerate(scopes):
        put(R, f"{'BCDEF'[i]}{r}", f"={s['sh']}!{COLS[j]}75", "lk", USD)

hdr(R, 33, "FASE 1 — Desenvolvimento (Paraguai)")
put(R, "A34", "Desenvolvimento da plataforma (com contingência) — igual ao Help Cure", "lbl"); put(R, "B34", "=F1_Desenvolvimento!$D$20", "lk", USD)
put(R, "A35", "Piloto (5 fazendas, 1 unidade móvel, protótipos)", "lbl"); put(R, "B35", "=F1_Desenvolvimento!$D$27", "lk", USD)
put(R, "A36", "Capital de giro da empresa (24 meses)", "lbl"); put(R, "B36", "=F1_Desenvolvimento!$D$35", "lk", USD)
put(R, "A37", "CAPTAÇÃO SUGERIDA — FASE 1", "lbl"); put(R, "B37", "=F1_Desenvolvimento!$D$40", "lk", USD); tot(R, 37, "B")

hdr(R, 39, "MONTAGEM DA RODADA — marque 1 nos escopos que o investidor financia", ["Marcar (1/0)", "Captação do escopo"])
put(R, "A40", "Fase 1 (sempre incluída)", "lbl"); put(R, "C40", "=F1_Desenvolvimento!$D$40", "lk", USD)
flags = [0, 1, 0, 0, 0]
for i, s in enumerate(scopes):
    r = 41 + i
    put(R, f"A{r}", f"E{i+1} · {names[i]}", "lbl")
    put(R, f"B{r}", flags[i], "in", NUM)
    put(R, f"C{r}", f"=B{r}*{s['sh']}!$B$86", "f", USD)
put(R, "A46", "Reserva de expansão (% sobre a soma)", "lbl"); put(R, "B46", 0.15, "in", PCT)
put(R, "A47", "CAPTAÇÃO TOTAL DA RODADA", "lbl"); put(R, "C47", "=(C40+SUM(C41:C45))*(1+B46)", "f", USD); tot(R, 47, "C")
put(R, "A48", "Atenção: E1 é um subconjunto do Paraguai. Não marque E1 e E2 juntos (as fazendas da cooperativa já estão no E2).", "lbl").font = F_NOTE
hdr(R, 50, "Leitura")
for k, t in enumerate([
    "A Fase 1 é paga uma vez e não se repete em nenhum escopo. Os escopos da Fase 2 só carregam custos incrementais e pagam royalty sobre a receita.",
    "Captação sugerida = o que precisa entrar antes do caixa virar, com 30% de folga. É o número a pedir a um investidor daquele escopo.",
    "A rentabilidade da empresa inteira (Fase 1 + escopos marcados) está na aba Rentabilidade_HelpFarm.",
]):
    put(R, f"A{51+k}", t, "lbl")

# =====================================================================
# Rentabilidade_HelpFarm
# =====================================================================
V = sheet("Rentabilidade_HelpFarm", "RENTABILIDADE DA HELP FARM — FASE 1 + ESCOPOS MARCADOS NO RESUMO (USD)",
          "Linha do tempo: t0 = fechamento; t1 e t2 = anos 1 e 2 da Fase 1; o Ano 0 da Fase 2 começa em t2 (ligado ao 1º contrato), de modo que o Ano 5 cai em t7. Mesma lógica do valuation do Help Cure, sem quadro societário.",
          (64, 15, 15, 15, 15, 15, 15, 15, 15, 12))
hdr(V, 4, "1. PREMISSAS")
vp = [(5, "Retorno exigido pelo investidor (TIR alvo = taxa de desconto)", 0.25, PCT),
      (6, "Múltiplo de saída EV/EBITDA aplicado ao EBITDA de t7", 6, "0.0x"),
      (7, "Estrutura corporativa mantida após a Fase 1 (% do custo mensal da Fase 1)", 1, PCT),
      (8, "Fase 1 · parcela do desenvolvimento gasta no ano 1", 0.5, PCT),
      (9, "Fase 1 · parcela do piloto gasta no ano 1", 0.4, PCT),
      (10, "Fase 1 · parcela do capital de giro gasta no ano 1", 0.5, PCT),
      (13, "Participação de referência do investidor", 0.2, PCT)]
for r, a, v, fm in vp:
    put(V, f"A{r}", a, "lbl"); put(V, f"B{r}", v, "in", fm)
put(V, "A11", "Reserva de expansão sobre a rodada (aba Resumo)", "lbl"); put(V, "B11", "=Resumo!$B$46", "lk", PCT)
put(V, "A12", "Tranches da Fase 1: fechamento · ano 1 · ano 2", "lbl")
for col, ref in zip("BCD", ("B43", "B44", "B45")):
    put(V, f"{col}12", f"=F1_Desenvolvimento!${ref[0]}${ref[1:]}", "lk", PCT)

T = list("BCDEFGHI")
hdr(V, 15, "2. FLUXO DE CAIXA DA EMPRESA", [f"t{i}" for i in range(8)])
put(V, "A16", "t (anos desde o fechamento)", "lbl")
for i, col in enumerate(T):
    put(V, f"{col}16", i, "f", "0")
put(V, "A17", "Ano da Fase 2", "lbl")
for i, col in enumerate(T):
    put(V, f"{col}17", "Fase 1" if i < 2 else f"Ano {i-2}", "lbl")
put(V, "A18", "(–) Desenvolvimento da plataforma", "lbl")
put(V, "A19", "(–) Piloto (fazendas, unidade móvel, protótipos)", "lbl")
put(V, "A20", "(–) Capital de giro da empresa (Fase 1)", "lbl")
put(V, "A21", "(+) Fluxo de caixa livre dos escopos marcados (já líquido de royalty)", "lbl")
put(V, "A22", "(–) Estrutura corporativa e evolução da plataforma (após a Fase 1)", "lbl")
put(V, "A23", "FLUXO DE CAIXA LIVRE DA EMPRESA", "lbl")
put(V, "A24", "Fluxo acumulado (sem aportes)", "lbl")
for i, col in enumerate(T):
    put(V, f"{col}18", {1: "=-F1_Desenvolvimento!$D$20*$B$8", 2: "=-F1_Desenvolvimento!$D$20*(1-$B$8)"}.get(i, 0), "lk" if i in (1, 2) else "f", USD)
    put(V, f"{col}19", {1: "=-F1_Desenvolvimento!$D$27*$B$9", 2: "=-F1_Desenvolvimento!$D$27*(1-$B$9)"}.get(i, 0), "lk" if i in (1, 2) else "f", USD)
    put(V, f"{col}20", {1: "=-F1_Desenvolvimento!$D$35*$B$10", 2: "=-F1_Desenvolvimento!$D$35*(1-$B$10)"}.get(i, 0), "lk" if i in (1, 2) else "f", USD)
    if i >= 2:
        sc = COLS[i - 2]
        f = "=" + "+".join(f"Resumo!$B${41+k}*{s['sh']}!{sc}78" for k, s in enumerate(scopes))
        put(V, f"{col}21", f, "lk", USD)
    else:
        put(V, f"{col}21", 0, "f", USD)
    if i >= 3:
        put(V, f"{col}22", f"=-SUM(F1_Desenvolvimento!$B$30:$B$33)*12*$B$7*(1+Precos!$B$46)^({i}-3)", "lk", USD)
    else:
        put(V, f"{col}22", 0, "f", USD)
    put(V, f"{col}23", f"=SUM({col}18:{col}22)", "f", USD)
    put(V, f"{col}24", f"={col}23" if i == 0 else f"={T[i-1]}24+{col}23", "f", USD)
tot(V, 23, T)
put(V, "A25", "Aportes do investidor (tranches da Fase 1 + captação dos escopos em t2)", "lbl")
put(V, "A26", "Caixa da empresa (acumulado, com aportes)", "lbl")
for i, col in enumerate(T):
    if i == 0: f = "=$B$30*$B$12"
    elif i == 1: f = "=$B$30*$C$12"
    elif i == 2: f = "=$B$30*$D$12+($B$32-$B$30)"
    else: f = 0
    put(V, f"{col}25", f, "f", USD)
    put(V, f"{col}26", f"={col}25+{col}23" if i == 0 else f"={T[i-1]}26+{col}25+{col}23", "f", USD)

hdr(V, 28, "3. CAPTAÇÃO, VALOR E RENTABILIDADE")
res = [
    (30, "Captação da Fase 1 (aba F1_Desenvolvimento)", "=F1_Desenvolvimento!$D$40", USD, "lk"),
    (31, "Captação dos escopos marcados (aba Resumo)", "=SUM(Resumo!$C$41:$C$45)", USD, "lk"),
    (32, "CAPTAÇÃO TOTAL DA RODADA (com reserva)", "=(B30+B31)*(1+$B$11)", USD, "f"),
    (33, "Receita em t7 (Ano 5 dos escopos marcados)", "=" + "+".join(f"Resumo!$B${41+k}*{s['sh']}!$G$55" for k, s in enumerate(scopes)), USD, "lk"),
    (34, "EBITDA da Help Farm em t7 (escopos − estrutura corporativa)", "=" + "+".join(f"Resumo!$B${41+k}*{s['sh']}!$G$75" for k, s in enumerate(scopes)) + "+I22", USD, "lk"),
    (35, "Valor de saída (EV = múltiplo × EBITDA de t7)", "=MAX(0,$B$6*B34)", USD, "f"),
    (36, "Equity value na saída (EV + caixa em t7)", "=B35+I26", USD, "f"),
    (37, "TIR DO PROJETO (fluxo da empresa + valor de saída em t7)", '=IFERROR(IRR(B45:I45,0.1),IFERROR(IRR(B45:I45,-0.3),"n/d"))', PCT, "f"),
    (38, "VPL do projeto à TIR alvo", "=B45+NPV($B$5,C45:I45)", USD, "f"),
    (39, "Payback do fluxo da empresa sem valor de saída (anos desde o fechamento)", '=IFERROR(MATCH(TRUE(),INDEX(C24:I24>=0,0),0),"após t7")', "0", "f"),
    (40, "Menor saldo de caixa com aportes (≥ 0 = captação suficiente)", "=MIN(B26:I26)", USD, "f"),
    (41, "Valor presente dos aportes (à TIR alvo)", "=SUMPRODUCT(B25:I25/(1+$B$5)^B16:I16)", USD, "f"),
    (42, "Valor da empresa hoje — pós-money (VP do equity de saída)", "=B36/(1+$B$5)^I16", USD, "f"),
    (43, "PARTICIPAÇÃO JUSTA para o investidor atingir a TIR alvo", '=IF(B42<=0,"n/d",B41/B42)', PCT, "f"),
]
for r, a, f, fm, k in res:
    put(V, f"A{r}", a, "lbl", bold=(r in (32, 37, 43)))
    put(V, f"B{r}", f, k, fm, bold=(r in (32, 37, 43)))
put(V, "A45", "Fluxo do projeto com valor de saída (base da TIR do projeto)", "lbl")
for i, col in enumerate(T):
    put(V, f"{col}45", f"={col}23" + ("+$B$35" if i == 7 else ""), "f", USD)

hdr(V, 47, "4. SENSIBILIDADE DA PARTICIPAÇÃO DO INVESTIDOR: 10% A 40%")
pcts = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]
PC = list("BCDEFGH")
put(V, "A48", "Participação do investidor na Help Farm", "lbl")
for c, p in zip(PC, pcts):
    put(V, f"{c}48", p, "in", PCT)
sens = [(49, "Ticket da rodada (captação total)", "=$B$32", USD),
        (50, "Pós-money implícito (ticket ÷ participação)", "={c}49/{c}48", USD),
        (51, "Pré-money implícito (pós − ticket)", "={c}50-{c}49", USD),
        (52, "Valor da participação na saída (t7)", "={c}48*$B$36", USD),
        (53, "MOIC (valor na saída ÷ ticket)", "=IF({c}49=0,0,{c}52/{c}49)", "0.00x"),
        (54, "TIR do investidor", None, PCT),
        (55, "Leitura frente à TIR alvo", None, None)]
for r, a, f, fm in sens:
    put(V, f"A{r}", a, "lbl")
    for k, c in enumerate(PC):
        if r == 54:
            put(V, f"{c}{r}", f'=IFERROR(IRR($B${60+k}:$I${60+k},0.1),IFERROR(IRR($B${60+k}:$I${60+k},-0.3),"n/d"))', "f", fm)
        elif r == 55:
            put(V, f"{c}{r}", f'=IF(ISNUMBER({c}54),IF({c}54>=$B$5,"atinge a TIR alvo","abaixo da TIR alvo"),"n/d")', "f")
        else:
            put(V, f"{c}{r}", f.format(c=c), "f", fm)
hdr(V, 58, "Memória: fluxo do investidor por participação", [f"t{i}" for i in range(8)])
for k, (c, p) in enumerate(zip(PC, pcts)):
    r = 60 + k
    put(V, f"A{r}", f"Participação de {int(p*100)}%", "lbl")
    for i, col in enumerate(T):
        f = f"=-{col}$25" + (f"+{c}$48*$B$36" if i == 7 else "")
        put(V, f"{col}{r}", f, "f", USD)

hdr(V, 68, "5. COMO LER E O QUE FOI ASSUMIDO")
for k, t in enumerate([
    "TIR do projeto = retorno da empresa inteira: gasta a Fase 1 em t1–t2, recebe o caixa dos escopos marcados a partir de t2, paga a estrutura corporativa a partir de t3 e vale o múltiplo × EBITDA em t7.",
    "Participação justa = parte da empresa que faz o investidor receber exatamente a TIR alvo sobre os aportes, só com o valor de saída (sem dividendos).",
    "A Help Farm consolida os escopos. O royalty dos escopos é receita da detentora do motor RAPP e não volta ao caixa da Help Farm neste cálculo (conservador).",
    "Desenvolvimento, capital de giro e unidade móvel iguais ao Help Cure. Se o motor RAPP e a plataforma forem compartilhados com o Help Cure, o custo da Fase 1 cai e a rentabilidade sobe — não considerado aqui.",
]):
    put(V, f"A{69+k}", t, "lbl")


hdr(V, 75, "6. CENÁRIOS DE RODADA — compare perfis de investidor (pesos editáveis)")
PRF = ["Paraguai (E2)", "Paraguai + Brasil", "Mercosul (PY + BR + Cone Sul)", "Global (PY + BR + Cone Sul + Faixa A)"]
W = [[0,1,0,0,0],[0,1,1,0,0],[0,1,1,1,0],[0,1,1,1,1]]
PCOL = list("BCDE")
hdr(V, 76, "Escopo  (peso de cada escopo na rodada)", PRF)
V.row_dimensions[76].height = 30
for k, s_ in enumerate(scopes):
    r = 77 + k
    put(V, f"A{r}", f"E{k+1} · {names[k]}", "lbl")
    for p, c in enumerate(PCOL):
        put(V, f"{c}{r}", W[p][k], "in", NUM)
hdr(V, 83, "Resultado do cenário", PRF)
MB = 100
lbls = [(84,"Captação total da rodada (com reserva)",USD),(85,"Receita em t7",USD),(86,"EBITDA da Help Farm em t7",USD),
        (87,"Valor de saída (EV)",USD),(88,"TIR DO PROJETO",PCT),(89,"VPL do projeto à TIR alvo",USD),
        (90,"Menor saldo de caixa com aportes",USD),(91,"Payback do fluxo da empresa (anos desde o fechamento)","0"),
        (92,"PARTICIPAÇÃO JUSTA para a TIR alvo",PCT)]
for r,a,fm in lbls:
    put(V, f"A{r}", a, "lbl", bold=(r in (88,92)))
for p, c in enumerate(PCOL):
    b = MB + p*7
    wcol = c
    put(V, f"A{b}", f"Memória — {PRF[p]}: FCF dos escopos", "lbl").font = F_H
    put(V, f"A{b+1}", "  FCF da empresa", "lbl"); put(V, f"A{b+2}", "  FCF com valor de saída em t7", "lbl")
    put(V, f"A{b+3}", "  Aportes", "lbl"); put(V, f"A{b+4}", "  Caixa acumulado com aportes", "lbl"); put(V, f"A{b+5}", "  Fluxo acumulado sem aportes", "lbl")
    capt = f"(F1_Desenvolvimento!$D$40+" + "+".join(f"${wcol}${77+k}*{s_['sh']}!$B$86" for k, s_ in enumerate(scopes)) + ")*(1+$B$11)"
    ebitda = "+".join(f"${wcol}${77+k}*{s_['sh']}!$G$75" for k, s_ in enumerate(scopes)) + "+$I$22"
    put(V, f"{c}84", "="+capt, "f", USD)
    put(V, f"{c}85", "="+"+".join(f"${wcol}${77+k}*{s_['sh']}!$G$55" for k, s_ in enumerate(scopes)), "f", USD)
    put(V, f"{c}86", "="+ebitda, "f", USD)
    put(V, f"{c}87", f"=MAX(0,$B$6*{c}86)", "f", USD)
    for i, col in enumerate(T):
        if i >= 2:
            sc = COLS[i-2]
            put(V, f"{col}{b}", "="+"+".join(f"${wcol}${77+k}*{s_['sh']}!{sc}78" for k, s_ in enumerate(scopes)), "f", USD)
        else:
            put(V, f"{col}{b}", 0, "f", USD)
        put(V, f"{col}{b+1}", f"={col}$18+{col}$19+{col}$20+{col}{b}+{col}$22", "f", USD)
        put(V, f"{col}{b+2}", f"={col}{b+1}" + (f"+{c}$87" if i == 7 else ""), "f", USD)
        if i == 0: ap = f"=F1_Desenvolvimento!$D$40*$B$12"
        elif i == 1: ap = f"=F1_Desenvolvimento!$D$40*$C$12"
        elif i == 2: ap = f"=F1_Desenvolvimento!$D$40*$D$12+({c}$84-F1_Desenvolvimento!$D$40)"
        else: ap = 0
        put(V, f"{col}{b+3}", ap, "f", USD)
        put(V, f"{col}{b+4}", f"={col}{b+3}+{col}{b+1}" if i == 0 else f"={T[i-1]}{b+4}+{col}{b+3}+{col}{b+1}", "f", USD)
        put(V, f"{col}{b+5}", f"={col}{b+1}" if i == 0 else f"={T[i-1]}{b+5}+{col}{b+1}", "f", USD)
    put(V, f"{c}88", f'=IFERROR(IRR(B{b+2}:I{b+2},0.1),IFERROR(IRR(B{b+2}:I{b+2},-0.3),"n/d"))', "f", PCT, bold=True)
    put(V, f"{c}89", f"=B{b+2}+NPV($B$5,C{b+2}:I{b+2})", "f", USD)
    put(V, f"{c}90", f"=MIN(B{b+4}:I{b+4})", "f", USD)
    put(V, f"{c}91", f'=IFERROR(MATCH(TRUE(),INDEX(C{b+5}:I{b+5}>=0,0),0),"após t7")', "f", "0")
    put(V, f"{c}92", f'=IFERROR(SUMPRODUCT(B{b+3}:I{b+3}/(1+$B$5)^$B$16:$I$16)/(({c}87+I{b+4})/(1+$B$5)^$I$16),"n/d")', "f", PCT, bold=True)
put(V, "A94", "Participação justa acima de 100% = nem a empresa inteira entrega a TIR alvo naquele cenário; abaixo de 40% = rodada viável para o investidor.", "lbl").font = F_NOTE

wb.move_sheet("Resumo", offset=-(len(wb.sheetnames) - 3))
order = ["Leia-me", "F1_Desenvolvimento", "Resumo", "Precos"] + [s["sh"] for s in scopes] + ["Rentabilidade_HelpFarm"]
wb._sheets = [wb[n] for n in order]
for w in wb.worksheets:
    w.sheet_properties.tabColor = DARK if w.title in ("Resumo", "Rentabilidade_HelpFarm") else "00BA30"
wb.save("HelpFarm_Modelo_por_Abrangencia_v2_Rentabilidade.xlsx")
print("saved")
