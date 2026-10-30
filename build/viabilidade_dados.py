# Lê HelpCure_Simulador_Vidas.xlsx (já recalculada) e gera assets/viabilidade-dados.js para a página do investidor.
# Uso: python3 build/viabilidade_dados.py <HelpCure_Simulador_Vidas.xlsx>
import json, sys, os, datetime
from openpyxl import load_workbook

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
wb = load_workbook(sys.argv[1], data_only=True)
b, p = wb["Base_Escopos"], wb["Premissas"]
TIERS = ["PY", "BR base", "BR alto", "BR realista"]
CODES = ["E1", "E2", "E3", "E4", "E5"]
REV0, SRV0, COP0, UOP0, CPX0, LIV0 = 70, 93, 101, 109, 117, 125   # layout fixo do build_simulador_vidas.py
row = lambda r: [b.cell(r, c).value or 0 for c in range(2, 8)]
P = lambda a: p[a].value

esc = {}
for i, code in enumerate(CODES):
    r = 5 + i
    v = [b.cell(r, c).value for c in range(1, 19)]
    tier = v[8]
    esc[code] = {
        "nbase": v[2], "m0": v[3], "teamb": v[4], "integ": v[5], "roy": v[6], "regime": v[7], "tabela": tier,
        "passo": v[11], "min": v[12], "max": v[13], "celula": v[14], "rodada": v[15], "elast": v[16], "integk": v[17],
        "vidas": row(LIV0 + i), "receita": row(REV0 + i * 4 + TIERS.index(tier)),
        "servir": row(SRV0 + i), "op_celula": row(COP0 + i), "op_movel": row(UOP0 + i), "capex": row(CPX0 + i),
    }
prem = {
    "mkt": P("B15"), "grow": P("B16"), "safety": P("B17"), "taxPY": P("B18"), "taxBR": P("B19"), "wPY": P("B20"), "wBR": P("B21"),
    "floor": P("B23"), "infra": P("B24"), "dev": P("B27"), "pil": P("B28"), "cg": P("B29"), "corp": P("B30"), "f1cap": P("B31"),
    "tr": [P("B32"), P("B33"), P("B34")], "tir": P("B37"), "mult": P("B38"), "corpk": P("B39"), "res": P("B40"), "payout": P("B41"),
    "minm": P("B42"), "eref": P("B43"), "dsh": P("B44"), "psh": P("B45"), "csh": P("B46"),
}
out = {"fonte": "HelpCure_Simulador_Vidas.xlsx", "gerado": datetime.date.today().isoformat(), "premissas": prem, "escopos": esc}
dst = os.path.join(ROOT, "assets", "viabilidade-dados.js")
open(dst, "w", encoding="utf-8").write("// Gerado por build/viabilidade_dados.py a partir do simulador de vidas. Não editar à mão.\nwindow.HC_VIAB=" + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n")
print("ok", dst, os.path.getsize(dst), "bytes")
