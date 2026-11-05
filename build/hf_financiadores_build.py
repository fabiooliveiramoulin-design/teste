# Help Farm — prévia: receitas, financiadores, retorno e valuation (mesma lógica de valuation do Help Cure / modelo v2).
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.comments import Comment

SRC = "HelpFarm_Modelo_por_Abrangencia_v2_Rentabilidade.xlsx"
OUT = "HelpFarm_Financiadores_Retorno_Valuation_previa.xlsx"
src = openpyxl.load_workbook(SRC, data_only=True)

AR = "Arial"
F = lambda **k: Font(name=AR, size=k.pop("size", 10), **k)
BLUE, BLACK, GREEN = "0000FF", "000000", "008000"
HDR = PatternFill("solid", fgColor="4A2F1B")
SEC = PatternFill("solid", fgColor="EFE3CC")
KEY = PatternFill("solid", fgColor="FFFF00")
TOT = PatternFill("solid", fgColor="F6EBD7")
thin = Side(style="thin", color="CDB894")
USD = '$#,##0;($#,##0);"-"'
PCT = '0.0%;(0.0%);"-"'
MUL = '0.00"x"'
TC = ["t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7"]
COLS = [L(c) for c in range(3, 11)]  # C..J = t0..t7

wb = openpyxl.Workbook()


def sheet(name, title, sub, width=58):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = width
    ws.column_dimensions["B"].width = 16
    for c in COLS: ws.column_dimensions[c].width = 14
    ws["A1"] = title; ws["A1"].font = F(size=14, bold=True, color="2E1D10")
    ws["A2"] = sub; ws["A2"].font = F(size=9, italic=True, color="5E4A38")
    return ws


def sec(ws, r, text, heads=True):
    ws.cell(r, 1, text).font = F(bold=True, color="FFFFFF")
    for c in range(1, 11): ws.cell(r, c).fill = HDR
    if heads:
        for i, c in enumerate(COLS): x = ws[f"{c}{r}"]; x.value = TC[i]; x.font = F(bold=True, color="FFFFFF"); x.alignment = Alignment(horizontal="center")


def row(ws, r, label, vals=None, f=None, fmt=USD, kind="f", bold=False, fill=None, note=None):
    a = ws.cell(r, 1, label); a.font = F(bold=bold)
    for i, c in enumerate(COLS):
        cell = ws[f"{c}{r}"]
        if vals is not None: cell.value = vals[i]; cell.font = F(color=BLUE, bold=bold)
        elif f is not None: cell.value = f(c, i); cell.font = F(color=GREEN if kind == "x" else BLACK, bold=bold)
        cell.number_format = fmt
        if fill: cell.fill = fill
    if fill: a.fill = fill
    if note: ws.cell(r, 11, note).font = F(size=8, italic=True, color="8A745F")


def inp(ws, r, label, v, fmt=USD, note=None, key=False):
    ws.cell(r, 1, label).font = F()
    c = ws.cell(r, 2, v); c.font = F(color=BLUE); c.number_format = fmt
    if key: c.fill = KEY
    if note: ws.cell(r, 3, note).font = F(size=8, italic=True, color="8A745F")
    return f"$B${r}"


def calc(ws, r, label, formula, fmt=USD, bold=False, fill=None, link=False):
    a = ws.cell(r, 1, label); a.font = F(bold=bold)
    c = ws.cell(r, 2, formula); c.font = F(bold=bold, color=GREEN if link else BLACK); c.number_format = fmt
    if fill: a.fill = fill; c.fill = fill
    return f"$B${r}"


def esc(sh, r):  # Ano0..Ano5 -> t0..t7 (t2..t7)
    w = src[sh]; v = [w.cell(r, c).value or 0 for c in range(2, 8)]
    return [0, 0] + [round(x, 2) if isinstance(x, float) else x for x in v]


def rent(r):
    w = src["Rentabilidade_HelpFarm"]; return [round(w.cell(r, c).value or 0, 2) for c in range(2, 10)]


# ================================================================ Leia-me
ws = wb.active; ws.title = "Leia-me"; ws.sheet_view.showGridLines = False; ws.column_dimensions["A"].width = 120
lines = [
    ("HELP FARM — FINANCIADORES, RETORNO E VALUATION (PRÉVIA PARA A ÁREA DO INVESTIDOR)", 14, True),
    ("Valores em USD. Linha do tempo igual ao modelo v2 e ao valuation do Help Cure: t0 = fechamento; t1–t2 = Fase 1 (plataforma e piloto); a Fase 2 começa em t2 e o Ano 5 cai em t7.", 10, False),
    ("", 10, False),
    ("COMO USAR", 11, True),
    ("1. Aba Base: escolha o cenário (1 = Paraguai; 2 = Paraguai + Brasil). As séries vêm do modelo v2 (HelpFarm_Modelo_por_Abrangencia_v2_Rentabilidade.xlsx).", 10, False),
    ("2. Aba Financiamento: defina quanto cada tipo de financiador coloca e em que condições (células azuis). O investidor de equity cobre o que faltar.", 10, False),
    ("3. As abas Receitas, Fluxo, Valuation e Retornos recalculam sozinhas. A aba Resumo compara os financiadores lado a lado.", 10, False),
    ("", 10, False),
    ("QUEM PODE FINANCIAR E O QUE FINANCIA", 11, True),
    ("Investidor de equity (anjos, family office, fundo agtech): plataforma, piloto e estrutura — o risco tecnológico. Recebe participação e valor na saída.", 10, False),
    ("Banco comercial ou de fomento (dívida de equipamentos): os kits de sensores em comodato, que são ativos e geram assinatura. Recebe juros e amortização.", 10, False),
    ("Cooperativa ou trading (investidor estratégico): pré-compra de licenças para os associados e uma parcela pequena de equity. Recebe licenças com desconto, prioridade e participação.", 10, False),
    ("Seguradora ou banco de risco: pré-compra do produto de risco (índice de condição da fazenda). Recebe dados e menos sinistro na carteira monitorada.", 10, False),
    ("Multilateral ou fundo de impacto (BID Lab, IFC, fundos de clima): doação para o piloto de certificação e nota conversível. Recebe impacto medido e equity na conversão.", 10, False),
    ("", 10, False),
    ("CORES", 11, True),
    ("Azul = premissa editável · Preto = fórmula · Verde = vínculo com outra aba · Fundo amarelo = premissa-chave a validar.", 10, False),
    ("", 10, False),
    ("AVISO", 11, True),
    ("Prévia para conversa com investidores. Preços, custos, condições de cada financiador e ganhos de cooperativas e seguradoras são premissas em validação, não ofertas firmes nem promessa de retorno.", 10, False),
]
for i, (t, s, b) in enumerate(lines, 1):
    c = ws.cell(i, 1, t); c.font = F(size=s, bold=b, color="2E1D10" if b else "000000"); c.alignment = Alignment(wrap_text=True)

# ================================================================ Base
B = sheet("Base", "BASE — SÉRIES DO MODELO V2 (USD)", "Valores copiados do modelo v2 (abas E2_Paraguai, E3_Brasil e Rentabilidade_HelpFarm). Mude o cenário na célula amarela.")
inp(B, 4, "Cenário (1 = Paraguai; 2 = Paraguai + Brasil)", 2, "0", "Paraguai sozinho não paga a rodada no modelo v2; Paraguai + Brasil é o cenário recomendado", key=True)
calc(B, 5, "Inclui Brasil? (1 = sim)", "=IF($B$4=2,1,0)", "0")
lines_r = [(47, "Assinatura — fazendas mista"), (48, "Assinatura — fazendas grãos"), (49, "Assinatura — fazendas leite"), (50, "Assinatura — fazendas corte"), (51, "Assinatura — fazendas alto valor"),
           (52, "Implantação + parcela do kit paga na instalação"), (53, "Licenças B2B2F (cooperativas)"), (54, "Produto de risco (seguradoras e bancos)")]
r = 7; BASE = {}
for sh, tag in [("E2_Paraguai", "PY"), ("E3_Brasil", "BR")]:
    sec(B, r, f"{'PARAGUAI (E2)' if tag == 'PY' else 'BRASIL (E3)'} — receita, kits, EBITDA e fluxo do escopo"); r += 1
    for sr, lab in lines_r:
        row(B, r, lab, esc(sh, sr), note=f"{sh} linha {sr}"); BASE[(tag, sr)] = r; r += 1
    row(B, r, "Kits de campo em comodato (CAPEX)", esc(sh, 70), note=f"{sh} linha 70"); BASE[(tag, "kit")] = r; r += 1
    row(B, r, "EBITDA do escopo (já líquido de royalty RAPP)", esc(sh, 75), note=f"{sh} linha 75"); BASE[(tag, "ebitda")] = r; r += 1
    row(B, r, "Fluxo de caixa livre do escopo (inclui kits e imposto)", esc(sh, 78), note=f"{sh} linha 78"); BASE[(tag, "fcf")] = r; r += 2
sec(B, r, "EMPRESA — Fase 1 e estrutura corporativa"); r += 1
for rr, lab in [(18, "Desenvolvimento da plataforma"), (19, "Piloto (fazendas, unidade móvel, protótipos)"), (20, "Capital de giro (Fase 1)"), (22, "Estrutura corporativa após a Fase 1")]:
    row(B, r, lab, rent(rr), note=f"Rentabilidade_HelpFarm linha {rr}"); BASE[("emp", rr)] = r; r += 1

# ================================================================ Receitas
R = sheet("Receitas", "RECEITAS DA HELP FARM POR LINHA (USD)", "Paraguai + (Brasil × chave do cenário). Mostra de onde vem o dinheiro antes de qualquer financiamento.")
sec(R, 4, "RECEITA BRUTA")
rr = 5; RL = {}
for sr, lab in lines_r:
    row(R, rr, lab, f=lambda c, i, sr=sr: f"=Base!{c}{BASE[('PY', sr)]}+Base!$B$5*Base!{c}{BASE[('BR', sr)]}", kind="x"); RL[sr] = rr; rr += 1
row(R, rr, "RECEITA BRUTA TOTAL", f=lambda c, i: f"=SUM({c}5:{c}{rr-1})", bold=True, fill=TOT); RT = rr; rr += 2
sec(R, rr, "RECEITA POR TIPO DE PAGADOR"); rr += 1
row(R, rr, "Produtores (assinatura + implantação)", f=lambda c, i: f"=SUM({c}5:{c}10)"); rr += 1
row(R, rr, "Cooperativas e tradings (licenças B2B2F)", f=lambda c, i: f"={c}11"); rr += 1
row(R, rr, "Bancos e seguradoras (produto de risco)", f=lambda c, i: f"={c}12"); rr += 1
row(R, rr, "Participação de entidades na receita (%)", f=lambda c, i: f"=IF({c}{RT}=0,0,({c}{rr-2}+{c}{rr-1})/{c}{RT})", fmt=PCT); rr += 2
row(R, rr, "Crescimento da receita sobre o ano anterior", f=lambda c, i: "=0" if i == 0 else f"=IF({COLS[i-1]}{RT}=0,0,{c}{RT}/{COLS[i-1]}{RT}-1)", fmt=PCT); rr += 1
R.cell(rr + 1, 1, "Receita de certificação de origem e do ecossistema (bancos, seguradoras e compradores além do produto de risco) ainda não entra: é potencial adicional.").font = F(size=9, italic=True, color="5E4A38")

# ================================================================ Financiamento
FI = sheet("Financiamento", "FINANCIAMENTO — QUEM COLOCA O QUÊ (premissas)", "Células azuis editáveis. O investidor de equity cobre o que faltar para o caixa não ficar negativo.")
sec(FI, 4, "1. BANCO COMERCIAL OU DE FOMENTO — dívida dos kits em comodato", heads=False)
d_pct = inp(FI, 5, "Parcela dos kits financiada", 0.5, PCT, "só depois do piloto, com os contratos de 36 meses como garantia; a validar com o banco", key=True)
d_rate = inp(FI, 6, "Juros ao ano (USD)", 0.11, PCT, "faixa típica de linha de equipamento em dólar no Paraguai; a validar", key=True)
d_term = inp(FI, 7, "Prazo de amortização (anos, sobre o saldo)", 4, "0")
sec(FI, 9, "2. COOPERATIVA OU TRADING — investidor estratégico", heads=False)
c_pre = inp(FI, 10, "Pré-compra de licenças para associados (paga em t2)", 600000, USD, "consome licenças entre t3 e t7", key=True)
c_disc = inp(FI, 11, "Desconto concedido na pré-compra", 0.2, PCT)
c_eq = inp(FI, 12, "Equity estratégico (aporte em t2)", 400000, USD)
c_gain = inp(FI, 13, "Perdas evitadas por fazenda associada monitorada (USD/ano)", 4000, USD, "seca, praga, doença e quebra de máquina evitadas; a validar no piloto", key=True)
c_farms = inp(FI, 14, "Fazendas associadas monitoradas (média t3–t7)", 120, "0")
sec(FI, 16, "3. SEGURADORA OU BANCO DE RISCO — pré-compra do produto de risco", heads=False)
s_pre = inp(FI, 17, "Pré-compra de dados de risco (paga em t2)", 500000, USD, "consome o produto de risco entre t3 e t7", key=True)
s_ha = inp(FI, 18, "Hectares da carteira monitorada", 150000, "#,##0")
s_prem = inp(FI, 19, "Prêmio médio por hectare (USD/ano)", 18, USD)
s_red = inp(FI, 20, "Redução da sinistralidade na carteira monitorada (pontos de %)", 0.05, PCT, "5 pontos de loss ratio; a validar", key=True)
sec(FI, 22, "4. MULTILATERAL OU FUNDO DE IMPACTO", heads=False)
m_grant = inp(FI, 23, "Doação (não reembolsável) em t1 — piloto de certificação e EUDR", 250000, USD)
m_conv = inp(FI, 24, "Nota conversível em t1", 500000, USD)
m_disc = inp(FI, 25, "Desconto na conversão sobre o preço da rodada", 0.2, PCT)
sec(FI, 27, "5. INVESTIDOR DE EQUITY (anjos, family office, fundo agtech)", heads=False)
e_res = inp(FI, 28, "Reserva de segurança sobre a necessidade de caixa", 0.15, PCT)
e_tr = [inp(FI, 29, "Tranche em t0 (fechamento)", 0.35, PCT), inp(FI, 30, "Tranche em t1", 0.35, PCT), inp(FI, 31, "Tranche em t2", 0.3, PCT)]
calc(FI, 32, "Soma das tranches (deve dar 100%)", "=B29+B30+B31", PCT)
sec(FI, 34, "6. VALUATION", heads=False)
v_tir = inp(FI, 35, "TIR alvo do investidor de equity (taxa de desconto)", 0.25, PCT, "mesma do modelo v2 e do Help Cure")
v_mul = inp(FI, 36, "Múltiplo de saída EV/EBITDA em t7", 6, MUL, "mesmo do modelo v2")
v_pre = inp(FI, 37, "Pré-money negociado hoje (USD)", 9000000, USD, "compare com o pré-money justo na aba Valuation", key=True)

# ================================================================ Fluxo
X = sheet("Fluxo", "FLUXO DE CAIXA DA EMPRESA COM CADA FINANCIADOR (USD)", "A dívida paga os kits; cooperativa e seguradora antecipam receita; o equity cobre o restante.")
sec(X, 4, "A. OPERAÇÃO (antes de financiamento)")
row(X, 5, "Receita bruta", f=lambda c, i: f"=Receitas!{c}{RT}", kind="x")
row(X, 6, "Fluxo livre dos escopos (com kits e imposto)", f=lambda c, i: f"=Base!{c}{BASE[('PY','fcf')]}+Base!$B$5*Base!{c}{BASE[('BR','fcf')]}", kind="x")
row(X, 7, "(–) Fase 1: plataforma, piloto e capital de giro", f=lambda c, i: f"=Base!{c}{BASE[('emp',18)]}+Base!{c}{BASE[('emp',19)]}+Base!{c}{BASE[('emp',20)]}", kind="x")
row(X, 8, "(–) Estrutura corporativa", f=lambda c, i: f"=Base!{c}{BASE[('emp',22)]}", kind="x")
row(X, 9, "FLUXO LIVRE DA EMPRESA (sem financiamento)", f=lambda c, i: f"={c}6+{c}7+{c}8", bold=True, fill=TOT)
row(X, 10, "Kits em comodato no ano (CAPEX)", f=lambda c, i: f"=Base!{c}{BASE[('PY','kit')]}+Base!$B$5*Base!{c}{BASE[('BR','kit')]}", kind="x")
row(X, 11, "EBITDA da empresa (escopos − estrutura − Fase 1)", f=lambda c, i: f"=Base!{c}{BASE[('PY','ebitda')]}+Base!$B$5*Base!{c}{BASE[('BR','ebitda')]}+{c}7+{c}8", kind="x")
sec(X, 13, "B. DÍVIDA DOS KITS")
row(X, 14, "Desembolso do banco", f=lambda c, i: f"=Financiamento!{d_pct}*{c}10", kind="x")
row(X, 15, "Juros pagos", f=lambda c, i: "=0" if i == 0 else f"=-{COLS[i-1]}17*Financiamento!{d_rate}")
row(X, 16, "Amortização paga", f=lambda c, i: "=0" if i == 0 else f"=-{COLS[i-1]}17/Financiamento!{d_term}")
row(X, 17, "Saldo devedor (fim do ano)", f=lambda c, i: f"={c}14" if i == 0 else f"={COLS[i-1]}17+{c}14+{c}16")
sec(X, 19, "C. COOPERATIVA, SEGURADORA E MULTILATERAL")
pre_in = lambda val: (lambda c, i: f"=IF({i}=2,Financiamento!{val},0)")
use = lambda val: (lambda c, i: f"=IF(AND({i}>=3,{i}<=7),-Financiamento!{val}/5,0)")
row(X, 20, "Cooperativa: pré-compra de licenças (entra)", f=pre_in(c_pre), kind="x")
row(X, 21, "Cooperativa: licenças já pagas (receita que não entra de novo)", f=use(c_pre), kind="x")
row(X, 22, "Cooperativa: desconto sobre as licenças pré-pagas", f=lambda c, i: f"=IF(AND({i}>=3,{i}<=7),-Financiamento!{c_pre}*Financiamento!{c_disc}/(1-Financiamento!{c_disc})/5,0)", kind="x")
row(X, 23, "Cooperativa: equity estratégico", f=pre_in(c_eq), kind="x")
row(X, 24, "Seguradora: pré-compra do produto de risco (entra)", f=pre_in(s_pre), kind="x")
row(X, 25, "Seguradora: produto já pago (receita que não entra de novo)", f=use(s_pre), kind="x")
row(X, 26, "Multilateral: doação", f=lambda c, i: f"=IF({i}=1,Financiamento!{m_grant},0)", kind="x")
row(X, 27, "Multilateral: nota conversível", f=lambda c, i: f"=IF({i}=1,Financiamento!{m_conv},0)", kind="x")
sec(X, 29, "D. NECESSIDADE DE EQUITY E CAIXA")
row(X, 30, "Fluxo antes do investidor de equity", f=lambda c, i: f"={c}9+{c}14+{c}15+{c}16+SUM({c}20:{c}27)", bold=True)
row(X, 31, "Acumulado antes do equity", f=lambda c, i: f"={c}30" if i == 0 else f"={COLS[i-1]}31+{c}30")
X["A33"] = "Necessidade de equity (pior acumulado × (1 + reserva))"; X["A33"].font = F(bold=True)
X["B33"] = f"=MAX(0,-MIN(C31:J31))*(1+Financiamento!{e_res})"; X["B33"].number_format = USD; X["B33"].font = F(bold=True); X["B33"].fill = TOT
row(X, 34, "Aportes do investidor de equity", f=lambda c, i: f"=IF({i}=0,$B$33*Financiamento!$B$29,IF({i}=1,$B$33*Financiamento!$B$30,IF({i}=2,$B$33*Financiamento!$B$31,0)))")
row(X, 35, "CAIXA DA EMPRESA (acumulado, com todos)", f=lambda c, i: f"={c}31+SUM($C$34:{c}34)", bold=True, fill=TOT)
X["A36"] = "Menor saldo de caixa (≥ 0 = financiamento suficiente)"; X["B36"] = "=MIN(C35:J35)"; X["B36"].number_format = USD
X["A38"] = "Comparação: equity necessário sem nenhum outro financiador"; X["B38"] = "=MAX(0,-MIN(C40:J40))*(1+Financiamento!B28)"; X["B38"].number_format = USD
row(X, 40, "Memória: acumulado sem financiadores", f=lambda c, i: f"={c}9" if i == 0 else f"={COLS[i-1]}40+{c}9")
X["A39"] = "Redução do equity graças aos outros financiadores"; X["B39"] = "=IF(B38=0,0,1-B33/B38)"; X["B39"].number_format = PCT

# ================================================================ Valuation
V = sheet("Valuation", "VALUATION — MESMA LÓGICA DO HELP CURE (USD)", "Valor de saída em t7 = múltiplo × EBITDA; trazido a hoje pela TIR alvo do investidor.")
calc(V, 4, "EBITDA da empresa em t7", "=Fluxo!J11", link=True)
calc(V, 5, "Múltiplo EV/EBITDA", f"=Financiamento!{v_mul}", MUL, link=True)
calc(V, 6, "Valor da empresa na saída (EV)", "=B4*B5", bold=True)
calc(V, 7, "(+) Caixa em t7", "=Fluxo!J35", link=True)
calc(V, 8, "(–) Dívida dos kits em aberto em t7", "=-Fluxo!J17", link=True)
calc(V, 9, "VALOR DO EQUITY NA SAÍDA", "=B6+B7+B8", bold=True, fill=TOT)
calc(V, 10, "Receita em t7", "=Fluxo!J5", link=True)
calc(V, 11, "EV / receita em t7 (conferência)", "=IF(B10=0,0,B6/B10)", MUL)
V["A13"] = "VALOR JUSTO HOJE"; V["A13"].font = F(bold=True)
calc(V, 14, "Valor presente do equity de saída à TIR alvo (pós-money justo)", f"=B9/(1+Financiamento!{v_tir})^7", bold=True)
calc(V, 15, "Equity novo da rodada (investidor + cooperativa + conversível)", "=Fluxo!B33+Financiamento!B12+Financiamento!B24", link=True)
calc(V, 16, "Valor presente desse equity novo", f"=Fluxo!B33*(Financiamento!B29+Financiamento!B30/(1+Financiamento!{v_tir})+Financiamento!B31/(1+Financiamento!{v_tir})^2)+(Financiamento!B12+Financiamento!B24)/(1+Financiamento!{v_tir})^1.5")
calc(V, 17, "PRÉ-MONEY JUSTO (pós justo − equity novo a valor presente)", "=B14-B16", bold=True, fill=TOT)
calc(V, 18, "Participação justa de todo o equity novo", "=IF(B14<=0,0,B16/B14)", PCT, bold=True)
V["A20"] = "PREÇO NEGOCIADO"; V["A20"].font = F(bold=True)
calc(V, 21, "Pré-money negociado", f"=Financiamento!{v_pre}", link=True)
calc(V, 22, "Pós-money (pré + equity novo)", "=B21+B15")
calc(V, 23, "Participação do investidor de equity", "=Fluxo!B33/B22", PCT)
calc(V, 24, "Participação da cooperativa/trading", "=Financiamento!B12/B22", PCT)
calc(V, 25, "Participação da multilateral (conversível com desconto)", "=Financiamento!B24/(1-Financiamento!B25)/B22", PCT)
calc(V, 26, "Participação dos fundadores e da Moulin (RAPP)", "=1-B23-B24-B25", PCT, bold=True)
V["A28"] = "Leitura: se o pré-money negociado for maior que o pré-money justo, o investidor de equity fica abaixo da TIR alvo; se for menor, acima."
V["A28"].font = F(size=9, italic=True, color="5E4A38")

# ================================================================ Retornos
T = sheet("Retornos", "RETORNO DE CADA FINANCIADOR (USD)", "Fluxo do ponto de vista de quem financia: saídas negativas, entradas positivas.")
sec(T, 4, "1. INVESTIDOR DE EQUITY")
row(T, 5, "Aportes", f=lambda c, i: f"=-Fluxo!{c}34", kind="x")
row(T, 6, "Valor da participação na saída", f=lambda c, i: "=Valuation!B23*Valuation!B9" if i == 7 else "=0")
row(T, 7, "Fluxo do investidor de equity", f=lambda c, i: f"={c}5+{c}6", bold=True)
sec(T, 9, "2. BANCO (dívida dos kits)")
row(T, 10, "Desembolsos", f=lambda c, i: f"=-Fluxo!{c}14", kind="x")
row(T, 11, "Juros + amortização recebidos", f=lambda c, i: f"=-(Fluxo!{c}15+Fluxo!{c}16)", kind="x")
row(T, 12, "Saldo quitado na saída (t7)", f=lambda c, i: "=Fluxo!J17" if i == 7 else "=0", kind="x")
row(T, 13, "Fluxo do banco", f=lambda c, i: f"=SUM({c}10:{c}12)", bold=True)
sec(T, 15, "3. COOPERATIVA OU TRADING")
row(T, 16, "Pré-compra + equity", f=lambda c, i: f"=-(Fluxo!{c}20+Fluxo!{c}23)", kind="x")
row(T, 17, "Licenças recebidas a preço cheio", f=lambda c, i: f"=-(Fluxo!{c}21+Fluxo!{c}22)", kind="x")
row(T, 18, "Perdas evitadas nas fazendas associadas", f=lambda c, i: f"=IF(AND({i}>=3,{i}<=7),Financiamento!$B$13*Financiamento!$B$14,0)")
row(T, 19, "Valor da participação na saída", f=lambda c, i: "=Valuation!B24*Valuation!B9" if i == 7 else "=0")
row(T, 20, "Fluxo da cooperativa (financeiro + perdas evitadas)", f=lambda c, i: f"=SUM({c}16:{c}19)", bold=True)
row(T, 21, "Fluxo da cooperativa (só financeiro)", f=lambda c, i: f"={c}16+{c}17+{c}19")
sec(T, 23, "4. SEGURADORA OU BANCO DE RISCO")
row(T, 24, "Pré-compra do produto de risco", f=lambda c, i: f"=-Fluxo!{c}24", kind="x")
row(T, 25, "Sinistros evitados na carteira monitorada", f=lambda c, i: f"=IF(AND({i}>=3,{i}<=7),Financiamento!$B$18*Financiamento!$B$19*Financiamento!$B$20,0)")
row(T, 26, "Fluxo da seguradora", f=lambda c, i: f"={c}24+{c}25", bold=True)
sec(T, 28, "5. MULTILATERAL OU FUNDO DE IMPACTO (só a nota conversível)")
row(T, 29, "Nota conversível", f=lambda c, i: f"=-Fluxo!{c}27", kind="x")
row(T, 30, "Valor da participação convertida na saída", f=lambda c, i: "=Valuation!B25*Valuation!B9" if i == 7 else "=0")
row(T, 31, "Fluxo da multilateral", f=lambda c, i: f"={c}29+{c}30", bold=True)
sec(T, 33, "RESULTADO POR FINANCIADOR", heads=False)
heads = ["Financiador", "Coloca (USD)", "Recebe (USD)", "TIR", "Múltiplo (MOIC)"]
for j, h in enumerate(heads): c = T.cell(34, 1 + j, h); c.font = F(bold=True); c.fill = SEC
res = [("Investidor de equity", 7), ("Banco (dívida dos kits)", 13), ("Cooperativa/trading — com perdas evitadas", 20), ("Cooperativa/trading — só financeiro", 21), ("Seguradora", 26), ("Multilateral (conversível)", 31)]
for k, (n, rr) in enumerate(res):
    r0 = 35 + k
    T.cell(r0, 1, n).font = F()
    T.cell(r0, 2, f'=-SUMIF(C{rr}:J{rr},"<0")').number_format = USD
    T.cell(r0, 3, f'=SUMIF(C{rr}:J{rr},">0")').number_format = USD
    T.cell(r0, 4, f'=IFERROR(IRR(C{rr}:J{rr}),"n/d")').number_format = PCT
    T.cell(r0, 5, f"=IF(B{r0}=0,0,C{r0}/B{r0})").number_format = MUL
    for cc in range(2, 6): T.cell(r0, cc).font = F()

# ================================================================ Resumo
S = sheet("Resumo", "RESUMO — QUEM PODE FINANCIAR A HELP FARM E O QUE GANHA", "Prévia para a área do investidor. Valores em USD; premissas em validação.", width=36)
for c, w in zip("BCDEFGH", [30, 16, 16, 12, 12, 46, 2]): S.column_dimensions[c].width = w
hd = ["Financiador", "Instrumento", "Coloca", "Recebe", "TIR", "MOIC", "O que financia e por quê"]
for j, h in enumerate(hd): c = S.cell(4, 1 + j, h); c.font = F(bold=True, color="FFFFFF"); c.fill = HDR; c.alignment = Alignment(wrap_text=True)
rows = [
    ("Investidor de equity (anjos, family office, fundo agtech)", "Participação societária em 3 tranches", 35, "Plataforma, piloto e estrutura: o risco de tecnologia e de mercado."),
    ("Banco comercial ou de fomento", "Dívida de equipamentos", 36, "Kits de sensores em comodato: ativo que gera assinatura de 36 meses."),
    ("Cooperativa ou trading", "Pré-compra de licenças + equity", 37, "Monitoramento dos associados com desconto e prioridade; inclui perdas evitadas."),
    ("Seguradora ou banco de risco", "Pré-compra do produto de risco", 39, "Índice de condição da fazenda para precificar e reduzir sinistro."),
    ("Multilateral ou fundo de impacto", "Doação + nota conversível", 40, "Piloto de certificação de origem (EUDR) e impacto medido."),
]
for k, (n, ins, tr, why) in enumerate(rows):
    r0 = 5 + k
    vals = [n, ins, f"=Retornos!B{tr}", f"=Retornos!C{tr}", f"=Retornos!D{tr}", f"=Retornos!E{tr}", why]
    for j, v in enumerate(vals):
        c = S.cell(r0, 1 + j, v); c.font = F(color=GREEN if isinstance(v, str) and v.startswith("=") else BLACK); c.alignment = Alignment(wrap_text=True, vertical="top")
        if j in (2, 3): c.number_format = USD
        if j == 4: c.number_format = PCT
        if j == 5: c.number_format = MUL
    S.row_dimensions[r0].height = 42
S["A11"] = "RODADA"; S["A11"].font = F(bold=True)
items = [("Cenário (1 = Paraguai; 2 = Paraguai + Brasil)", "=Base!B4", "0"), ("Equity necessário com todos os financiadores", "=Fluxo!B33", USD), ("Equity necessário sem os outros financiadores", "=Fluxo!B38", USD),
         ("Redução do equity graças aos outros financiadores", "=Fluxo!B39", PCT), ("Receita em t7", "=Valuation!B10", USD), ("EBITDA em t7", "=Valuation!B4", USD), ("Valor da empresa na saída (EV)", "=Valuation!B6", USD),
         ("Pré-money justo hoje (à TIR alvo)", "=Valuation!B17", USD), ("Pré-money negociado (premissa)", "=Valuation!B21", USD), ("Participação do investidor de equity", "=Valuation!B23", PCT), ("Participação de fundadores e Moulin (RAPP)", "=Valuation!B26", PCT)]
for k, (lab, fml, fmt) in enumerate(items):
    S.cell(12 + k, 1, lab).font = F(); c = S.cell(12 + k, 2, fml); c.font = F(color=GREEN); c.number_format = fmt
S["A24"] = "Doação da multilateral não tem retorno financeiro: entra como impacto (fazendas monitoradas, hectares certificados sem desmatamento)."
S["A25"] = "Ganhos de cooperativa e seguradora (perdas e sinistros evitados) são premissas a validar no piloto do Paraguai."
for a in ("A24", "A25"): S[a].font = F(size=9, italic=True, color="5E4A38")

wb.move_sheet("Resumo", offset=-(len(wb.sheetnames) - 2))
for w in wb.worksheets: w.freeze_panes = None
wb.save(OUT); print("salvo", OUT)
