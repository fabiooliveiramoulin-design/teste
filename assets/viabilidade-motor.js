// Help Cure — motor do simulador de vidas (mesmas fórmulas da aba Grade de HelpCure_Simulador_Vidas.xlsx).
// calc(D, codigo, vidasAno5) → resultado do projeto do escopo + rodada e valuation da Help Cure.
(function (root) {
  function npv(r, xs) { var s = 0; for (var i = 0; i < xs.length; i++) s += xs[i] / Math.pow(1 + r, i + 1); return s; }
  function pv0(r, xs) { var s = 0; for (var i = 0; i < xs.length; i++) s += xs[i] / Math.pow(1 + r, i); return s; }
  // TIR por bisseção em faixas: procura a primeira troca de sinal a partir de -99%
  function irr(xs) {
    var grid = [-0.99, -0.9, -0.75, -0.5, -0.25, -0.1, 0, 0.1, 0.25, 0.5, 1, 2, 4, 8, 16, 50];
    for (var g = 0; g < grid.length - 1; g++) {
      var a = grid[g], b = grid[g + 1], fa = pv0(a, xs), fb = pv0(b, xs);
      if (isFinite(fa) && isFinite(fb) && fa * fb <= 0) {
        for (var k = 0; k < 200; k++) { var m = (a + b) / 2, fm = pv0(m, xs); if (fa * fm <= 0) { b = m; fb = fm; } else { a = m; fa = fm; } }
        return (a + b) / 2;
      }
    }
    return null;
  }

  function calc(D, code, N) {
    var P = D.premissas, S = D.escopos[code];
    var k = N / S.nbase, inr = S.rodada === 1;
    var tax = S.regime === "PY" ? P.taxPY : P.taxBR, wacc = S.regime === "PY" ? P.wPY : P.wBR;
    var teamm = S.teamb * Math.max(P.floor, Math.pow(k, S.elast));
    var integ = S.integ * (S.integk === 1 ? k : 1);
    var y, lives = [], rev = [], ebitda = [], fcf = [], cum = [];
    for (y = 0; y < 6; y++) {
      lives[y] = k * S.vidas[y];
      rev[y] = k * S.receita[y];
      var team = y === 0 ? teamm * S.m0 : teamm * 12 * Math.pow(1 + P.grow, y - 1);
      var opex = team + k * (S.servir[y] + S.op_celula[y] + S.op_movel[y]) + rev[y] * (P.mkt + S.roy + P.infra);
      var capex = k * S.capex[y] + (y === 0 ? integ : 0);
      ebitda[y] = rev[y] - opex;
      fcf[y] = ebitda[y] - Math.max(0, ebitda[y]) * tax - capex;
      cum[y] = (y ? cum[y - 1] : 0) + fcf[y];
    }
    var vpl = fcf[0] + npv(wacc, fcf.slice(1));
    var tir = irr(fcf); if (tir === null) tir = 0;
    var payback = null;
    for (y = 1; y <= 5; y++) if (cum[y] >= 0) { payback = y - 1 + (-cum[y - 1] / fcf[y]); break; }
    var need = -Math.min(0, Math.min.apply(null, cum));
    var capt = need * P.safety;
    var ticket = inr ? (P.f1cap + capt) * (1 + P.res) : capt;
    var R = { vidas: N, k: k, curva: { vidas: lives, receita: rev, ebitda: ebitda, fluxo: fcf, caixa: cum },
      receita5: rev[5], ebitda5: ebitda[5], margem: rev[5] ? ebitda[5] / rev[5] : 0, vpl: vpl, tir: tir, payback: payback,
      necessidade: need, captacao: capt, ticket: ticket, rodada: inr };
    if (!inr) return R;

    // valuation da Help Cure (linha do tempo t0..t7: Fase 1 em t1–t2, Fase 2 de t2 em diante)
    var corp = function (t) { return -P.corp * 12 * P.corpk * Math.pow(1 + P.grow, t - 3); };
    var firm = [0, -(P.dev * P.dsh + P.pil * P.psh + P.cg * P.csh), -(P.dev * (1 - P.dsh) + P.pil * (1 - P.psh) + P.cg * (1 - P.csh)) + fcf[0]];
    for (var t = 3; t <= 7; t++) firm[t] = fcf[t - 2] + corp(t);
    var ap = [P.f1cap * P.tr[0], P.f1cap * P.tr[1], P.f1cap * P.tr[2] + (ticket - P.f1cap)];
    var buf = P.minm * P.corp * P.corpk, div = [0, 0, 0], cash = [ap[0] + firm[0]];
    for (t = 1; t <= 7; t++) {
      if (t >= 3) div[t] = P.payout * Math.max(0, Math.min(firm[t], cash[t - 1] + firm[t] - buf));
      cash[t] = cash[t - 1] + (t <= 2 ? ap[t] : 0) + firm[t] - div[t];
    }
    var ev = Math.max(0, P.mult * (ebitda[5] + corp(7))), eq = ev + cash[7], r = P.tir;
    var pvap = ap[0] + ap[1] / (1 + r) + ap[2] / Math.pow(1 + r, 2);
    var pveq = eq / Math.pow(1 + r, 7);
    for (t = 3; t <= 7; t++) pveq += div[t] / Math.pow(1 + r, t);
    var fair = pveq <= 0 ? 9.99 : Math.min(9.99, pvap / pveq);
    var e = P.eref, flow = [];
    for (t = 0; t <= 7; t++) flow[t] = e * div[t] - (t <= 2 ? ap[t] : 0) + (t === 7 ? e * eq : 0);
    var sdiv = 0; for (t = 3; t <= 7; t++) sdiv += div[t];
    R.posmoney = pveq; R.premoney = pveq - pvap; R.participacao = fair;
    R.tirInvRef = irr(flow); R.moicRef = e * (sdiv + eq) / ticket; R.menorCaixa = Math.min.apply(null, cash);
    R.evSaida = ev; R.equitySaida = eq; R.somaDividendos = sdiv;
    R.moicJusto = fair > 1 ? null : fair * (sdiv + eq) / ticket;
    return R;
  }
  var api = { calc: calc, irr: irr };
  if (typeof module !== "undefined") module.exports = api; else root.HCMotor = api;
})(this);
