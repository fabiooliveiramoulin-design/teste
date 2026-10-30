// Help Cure — motor do modelo final (30/10/2026), igual às abas Segmentos e Empresa de HelpCure_Equity_Lucros_Royalties.xlsx.
// Segmento: royalty RAPP por vida monitorada. Empresa: o investidor fundador paga Fase 1 + segmentos + reserva,
// recebe divisão de lucros (10% do EBITDA; rede de clínicas de 10% a 35%, para vender no máximo 30%; teto 5x a Fase 1, depois 1%) e um percentual da Help Cure.
(function (root) {
  function pv0(r, xs) { var s = 0; for (var i = 0; i < xs.length; i++) s += xs[i] / Math.pow(1 + r, i); return s; }
  function irr(xs) {
    var g = [-0.99, -0.9, -0.75, -0.5, -0.25, -0.1, 0, 0.1, 0.25, 0.5, 1, 2, 4, 8, 16, 50];
    for (var i = 0; i < g.length - 1; i++) {
      var a = g[i], b = g[i + 1], fa = pv0(a, xs), fb = pv0(b, xs);
      if (isFinite(fa) && isFinite(fb) && fa * fb <= 0) {
        for (var k = 0; k < 200; k++) { var m = (a + b) / 2, fm = pv0(m, xs); if (fa * fm <= 0) b = m; else { a = m; fa = fm; } }
        return (a + b) / 2;
      }
    }
    return null;
  }
  // Um segmento com k vezes as vidas do plano (Ano 0 a 5)
  function segmento(D, code, k) {
    var P = D.premissas, S = D.escopos[code];
    var tax = S.regime === "PY" ? P.taxPY : P.taxBR, wacc = S.regime === "PY" ? P.wPY : P.wBR;
    var teamm = S.teamb * Math.max(P.floor, Math.pow(k, S.elast)), integ = S.integ * (S.integk === 1 ? k : 1);
    var c = { vidas: [], receita: [], moulin: [], ebitda: [], fluxo: [], caixa: [] }, y;
    for (y = 0; y < 6; y++) {
      var L = k * S.vidas[y], R = k * S.receita[y], Mo = L * P.mvida * 12;
      var team = y === 0 ? teamm * S.m0 : teamm * 12 * Math.pow(1 + P.grow, y - 1);
      var opex = team + k * (S.servir[y] + S.op_celula[y] + S.op_movel[y]) + R * (P.mkt + P.infra) + Mo;
      var E = R - opex, F = E - Math.max(0, E) * tax - (k * S.capex[y] + (y === 0 ? integ : 0));
      c.vidas[y] = L; c.receita[y] = R; c.moulin[y] = Mo; c.ebitda[y] = E; c.fluxo[y] = F; c.caixa[y] = (y ? c.caixa[y - 1] : 0) + F;
    }
    var npv = 0; for (y = 1; y < 6; y++) npv += c.fluxo[y] / Math.pow(1 + wacc, y);
    var pb = null; for (y = 1; y <= 5; y++) if (c.caixa[y] >= 0) { pb = S.m0 / 12 + y - 1 + (-c.caixa[y - 1] / c.fluxo[y]); break; }
    var need = -Math.min(0, Math.min.apply(null, c.caixa)), t = irr(c.fluxo);
    return { curva: c, vpl: c.fluxo[0] + npv, tir: t === null ? 0 : t, payback: pb, captacao: need * P.safety };
  }
  // Empresa: segs = [[código, k, t em que começa o Ano 0]], ps = divisão de lucros ligada (true/false)
  // Clínicas (escopo com psmax): a divisão de lucros da rede de clínicas sobe de 10% em passos de 5 pontos, até psmax (35%),
  // e fica no menor percentual que deixa a participação vendida em até 30%. Os demais segmentos ficam em 10%.
  function empresa(D, segs, ps, ov) {
    if (ov === undefined && ps && segs.some(function (s) { return D.escopos[s[0]].psmax !== undefined; })) {
      var mx = Math.max.apply(null, segs.map(function (s) { return D.escopos[s[0]].psmax || 0; })), best;
      for (var q = D.premissas.ps; q <= mx + 1e-9; q += 0.05) { best = empresa(D, segs, ps, q); if (best.participacao <= 0.30) break; }
      return best;
    }
    var P = D.premissas, r = P.tir, f1 = P.f1cap, capv = P.pscap * f1, t;
    var E = [], F = [], R = [], Lv = [], Mo = [], X = [], capt = 0, segRes = [];
    for (t = 0; t < 8; t++) { E[t] = F[t] = R[t] = Lv[t] = Mo[t] = X[t] = 0; }
    segs.forEach(function (s) {
      var g = segmento(D, s[0], s[1]); segRes.push(g); capt += g.captacao;
      var sx = (D.escopos[s[0]].psmax !== undefined && ov !== undefined ? ov : P.ps) - P.ps; // divisão de lucros própria da rede de clínicas
      for (t = 0; t < 8; t++) {
        var y = t - s[2]; if (y < 0) continue; if (y > 5) y = 5;
        X[t] += sx * Math.max(0, g.curva.ebitda[y]);
        E[t] += g.curva.ebitda[y]; F[t] += g.curva.fluxo[y]; R[t] += g.curva.receita[y]; Lv[t] += g.curva.vidas[y]; Mo[t] += g.curva.moulin[y];
      }
    });
    var PS = [], cps = 0;
    for (t = 0; t < 8; t++) {
      var e = Math.max(0, E[t]);
      PS[t] = !ps ? 0 : cps >= capv ? P.psres * e : Math.min(Math.max(0, P.ps * e + X[t]), capv - cps); cps += PS[t];
    }
    var ticket = (f1 + capt) * (1 + P.res), ap = [f1 * P.tr[0], f1 * P.tr[1], f1 * P.tr[2] + ticket - f1];
    var f1y = { 1: -(P.dev * P.dsh + P.pil * P.psh + P.cg * P.csh), 2: -(P.dev * (1 - P.dsh) + P.pil * (1 - P.psh) + P.cg * (1 - P.csh)) };
    var corp = function (t) { return t >= 3 ? -P.corp * 12 * P.corpk * Math.pow(1 + P.grow, t - 3) : 0; };
    var buf = P.minm * P.corp * P.corpk, firm = [], div = [0, 0, 0], cash = [];
    for (t = 0; t < 8; t++) firm[t] = (f1y[t] || 0) + F[t] + corp(t) - PS[t];
    cash[0] = ap[0] + firm[0];
    for (t = 1; t < 8; t++) {
      if (t >= 3) div[t] = P.payout * Math.max(0, Math.min(firm[t], cash[t - 1] + firm[t] - buf));
      cash[t] = cash[t - 1] + (t <= 2 ? ap[t] : 0) + firm[t] - div[t];
    }
    var ev = Math.max(0, P.mult * (E[7] + corp(7) - PS[7])), eq = ev + cash[7], e7 = Math.max(0, E[7]), af = (1 - Math.pow(1 + r, -5)) / r;
    var tail = !ps ? 0 : cps >= capv ? P.psres * e7 / r : Math.min(Math.max(0, P.ps * e7 + X[7]) * af, capv - cps) + P.psres * e7 / r / Math.pow(1 + r, 5);
    var pvap = ap[0] + ap[1] / (1 + r) + ap[2] / Math.pow(1 + r, 2), pvps = tail / Math.pow(1 + r, 7), pveq = eq / Math.pow(1 + r, 7), sd = 0, sps = 0;
    for (t = 0; t < 8; t++) { pvps += PS[t] / Math.pow(1 + r, t); sps += PS[t]; }
    for (t = 3; t < 8; t++) { pveq += div[t] / Math.pow(1 + r, t); sd += div[t]; }
    var part = pveq <= 0 ? 9.99 : Math.min(9.99, Math.max(0, pvap - pvps) / pveq), em = Math.min(1, part);
    return { participacao: part, posmoney: pveq, premoney: pveq - Math.max(0, pvap - pvps), rodada: ticket, vpDivisao: pvps,
      receita7: R[7], ebitda7: E[7], vidas7: Lv[7], moulin: Mo[3] + Mo[4] + Mo[5] + Mo[6] + Mo[7], divisao: PS, tail: tail,
      multiplo: (sps + tail + em * (sd + eq)) / ticket, captacao: capt, segmentos: segRes, psClinicas: ov === undefined ? P.ps : ov };
  }
  var api = { segmento: segmento, empresa: empresa, irr: irr };
  if (typeof module !== "undefined") module.exports = api; else root.HCModelo = api;
})(this);
