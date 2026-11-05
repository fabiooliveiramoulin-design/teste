# Módulo RAPP Energia no Help Farm — preços, economia do produtor e efeito no modelo (estimativas, nov/2026)
import json
C = json.load(open("calc.json")); FX = 5.40
o = {}
# Preço médio da energia paga por fazenda irrigante (US$/MWh, todos os encargos) — premissas por faixa
T = {"C": 60, "B": 75, "A": 130}          # C: ANDE ≈53 (PY), AR mais alto; B: Brasil c/ desconto noturno ≈70; A: EUA/Ibéria
DAY = {"C": 60, "B": 87, "A": 140}        # preço da energia diurna, contra a qual o solar compensa
YLD = {"C": 1650, "B": 1700, "A": 1600}   # kWh/kWp/ano
CAP = {"C": 0.70, "B": 0.75, "A": 1.10}   # US$/Wp instalado (BR R$3,5–5,5/Wp)
LCOE_OM = 8                                # O&M US$/MWh
# Preços propostos do módulo
PR = {"diag": {"C": 1500, "B": 2500, "A": 4000},          # diagnóstico + projeto de geração (por fazenda)
      "esco": 0.30, "anos": 4,                            # 30% da economia verificada, 4 anos
      "fixo": {"C": 120, "B": 200, "A": 350},             # alternativa: gestão por mensalidade fixa US$/fazenda/mês
      "orig": 0.04,                                       # taxa de originação do projeto solar (% do capex), paga pela SPE/EPC
      "mv": {"C": 4, "B": 6, "A": 9},                     # monitoramento da usina + verificação da economia, US$/kWp/ano
      "perim_diag": 28000, "perim_esco": 0.30}
o["precos"] = PR
# Fazenda irrigada típica: 500 ha de pivô, 2.700 kWh/ha
MWH = 500 * 2.7
far = {}
for b in "CBA":
    conta = MWH * T[b]
    gest = 0.15 * conta                       # economia sem investimento (15%)
    hf_gest = PR["esco"] * gest
    solar_mwh = MWH * 0.5 * 0.6               # 60% do consumo diurno (metade do total)
    kwp = solar_mwh * 1000 / YLD[b]; capex = kwp * 1000 * CAP[b]
    econ_solar = solar_mwh * (DAY[b] - LCOE_OM)
    payback = capex / econ_solar
    orig = PR["orig"] * capex; mv = PR["mv"][b] * kwp
    hf_ano = hf_gest + mv + (PR["diag"][b] + orig) / 5   # média anual em 5 anos
    prod_liq = gest - hf_gest + econ_solar - mv          # ganho do produtor/ano (após pagar o HF; usina já paga)
    far[b] = dict(conta=round(conta), gest=round(gest), hf_gest=round(hf_gest), kwp=round(kwp), capex=round(capex),
                  econ_solar=round(econ_solar), payback=round(payback, 1), orig=round(orig), mv=round(mv),
                  diag=PR["diag"][b], hf_ano=round(hf_ano), hf_mes=round(hf_ano / 12), prod_liq=round(prod_liq),
                  pct_conta=round((gest + econ_solar) / conta * 100))
o["fazenda"] = far
# Adoção entre as fazendas Help Farm (premissa): % com uso intensivo de energia (irrigação, leite, frio, secagem) e % que faz usina
AD = {"C": (0.15, 0.20), "B": (0.30, 0.40), "A": (0.35, 0.40)}
MG = 0.65   # margem de contribuição do módulo (engenheiro de energia, garras de corrente, M&V)
pais = []
for p in C["paises"]:
    b = p["faixa"]; ad, sol = AD[b]; f = far[b]
    hf_m = (f["hf_gest"] + (PR["diag"][b]) / 5 + sol * (f["mv"] + f["orig"] / 5)) / 12   # por fazenda aderente/mês
    add_r = ad * hf_m; add_m = add_r * MG
    eq = p["fixo"] / (p["margem"] + add_m)
    pais.append(dict(pais=p["pais"], faixa=b, receita=p["receita"], add_r=round(add_r), pct=round(add_r / p["receita"] * 100, 1),
                     eq0=p["equilibrio"], eq1=int(-(-eq // 1))))
o["paises"] = pais
# Ano 5, Paraguai + Brasil: 320 fazendas PY + 600 BR (mesma base do estudo FAPIJA)
y = {}
for b, n in (("C", 320), ("B", 600)):
    ad, sol = AD[b]; f = far[b]; k = n * ad
    y[b] = dict(fazendas=round(k), gestao=round(k * f["hf_gest"]), diag=round(k * PR["diag"][b] / 4),
                usinas=round(k * sol / 4), orig=round(k * sol / 4 * f["orig"]), mv=round(k * sol * f["mv"]))
per = 2 * (PR["perim_diag"] / 2 + PR["perim_esco"] * 3209573 / FX)   # 2 perímetros tipo FAPIJA (diagnóstico rateado + ESCO sem usina)
tot = sum(v[k] for v in y.values() for k in ("gestao", "diag", "orig", "mv")) + per
ebitda = tot * MG
core_rev, core_ebitda, ev, pre = 21058037, 10052416, 60314496, 7520863
mult = ev / core_ebitda; ratio = pre / ev
o["ano5"] = dict(py=y["C"], br=y["B"], perimetros=round(per), total=round(tot), pct_receita=round(tot / core_rev * 100, 1),
                 ebitda=round(ebitda), ev_add=round(ebitda * mult), pre_add=round(ebitda * mult * ratio),
                 pre_novo=round(pre + ebitda * mult * ratio), mult=round(mult, 1))
# Grupo (fora da Help Farm): SPE de geração, PPA com 15% de desconto
usinas_kwp = sum(y[b]["usinas"] * 4 * far[b]["kwp"] for b in y) / 4 * 4  # usinas acumuladas até o Ano 5 ≈ k*sol
o["spe"] = dict(mwp=round(sum(round(320 * .15 * .2) * far["C"]["kwp"] for _ in [0]) / 1000 + round(600 * .3 * .4) * far["B"]["kwp"] / 1000, 1),
                capex=round(round(320 * .15 * .2) * far["C"]["capex"] + round(600 * .3 * .4) * far["B"]["capex"]))
json.dump(o, open("calc_en.json", "w"), ensure_ascii=False, indent=1)
for k in ("fazenda", "paises", "ano5", "spe"): print(k, json.dumps(o[k], ensure_ascii=False))
