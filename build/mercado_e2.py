# Plano de saúde (E2) por estimativa de mercado (30/10/2026) — estudo "Help Cure — Aderência nos planos de saúde (BR e PY)".
# Referência: operadora nacional média (~3,5 mi de beneficiários, como Amil/Bradesco/SulAmérica).
# Vidas no Ano 5 = 50% dos candidatos: idosos 60+ com hipertensão ou diabetes (15,3% × 55%) + todas as crianças e
# adolescentes de 0 a 18 anos com a pulseira com GPS (22,7%) — cenário B, aprovado pelo Fábio. ≈ 15,6% da carteira.
# Custo diluído na carteira: +1,98% na mensalidade média (R$ 72,80 por usuário/mês sobre R$ 571).
# Fontes: IESS NAB 114 (dez/2025), PNS 2019, CQCS/O Globo (abr/2026).
E2_BENEF = 3_500_000
E2_P60, E2_CRON60, E2_KIDS, E2_ADES = 0.153, 0.55, 0.227, 0.5
E2_PASSO = 20000


def e2_vidas():
    return round(E2_BENEF * (E2_P60 * E2_CRON60 + E2_KIDS) * E2_ADES)


def aplica_e2(S):
    """Escala o E2 do plano original (só pagador plano; células proporcionais) para o volume de mercado.
    Todas as séries são lineares nas vidas e nas entidades, então basta multiplicar por kt; a equipe cresce com kt^elast."""
    if "mercado" in S:          # já aplicado
        return S
    nb = e2_vidas(); kt = nb / S["nbase"]
    for key in ("vidas", "receita", "servir", "op_celula", "op_movel", "capex"):
        S[key] = [x * kt for x in S[key]]
    S.update({"nbase": nb, "teamb": S["teamb"] * kt ** S["elast"], "passo": E2_PASSO, "min": E2_PASSO,
              "max": max(S["max"], 3 * nb), "mercado": {"vidas_ano5": nb, "fator_vs_plano": kt,
              "beneficiarios": E2_BENEF, "criancas": round(E2_BENEF * E2_KIDS * E2_ADES)}})
    return S
