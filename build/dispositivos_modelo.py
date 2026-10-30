# Dispositivos no modelo (decisão de 30/10/2026): cada pessoa monitorada recebe a sua pulseira ou smartwatch
# (crianças do plano: pulseira com GPS 4G) e 10% dos adultos recebem o kit Help Cure Casa. O pagador paga o
# dispositivo dentro do pacote: entra como receita e como custo, ao preço de lote (20% abaixo do mercado).
# Marketing: "cada monitorado recebe o seu — ou pode usar o próprio smartwatch para a leitura" (BYOD só reduz os dois lados).
# A clínica (E1) não recebe dispositivos. Mesma lógica da planilha HelpCure_Dispositivos_por_Segmento.xlsx.
DESC = 0.20
PRECO_MERCADO = {"adulto": 50.0, "infantil": 67.0}
KIT_CUSTO, KIT_PCT = 180.0, 0.10
VIDA_UTIL = {"adulto": 3, "infantil": 2, "kit": 4}


def serie(S, kids_share=0.0):
    v = S["vidas"]; n = len(v)
    parque = {"adulto": [x * (1 - kids_share) for x in v], "infantil": [x * kids_share for x in v],
              "kit": [x * (1 - kids_share) * KIT_PCT for x in v]}
    preco = {"adulto": PRECO_MERCADO["adulto"] * (1 - DESC), "infantil": PRECO_MERCADO["infantil"] * (1 - DESC), "kit": KIT_CUSTO}
    out = [0.0] * n
    for t, p in parque.items():
        for y in range(1, n):
            out[y] += (max(0.0, p[y] - p[y - 1]) + p[y - 1] / VIDA_UTIL[t]) * preco[t]
    return out


def aplica_disp(esc):
    for code, S in esc.items():
        if "disp" in S:
            continue
        if code.startswith("E1"):
            S["disp"] = [0.0] * len(S["vidas"]); continue
        kids = S["mercado"]["criancas"] / S["mercado"]["vidas_ano5"] if code == "E2" else 0.0
        d = serie(S, kids)
        S["receita"] = [a + b for a, b in zip(S["receita"], d)]
        S["servir"] = [a + b for a, b in zip(S["servir"], d)]
        S["disp"] = d
    return esc
