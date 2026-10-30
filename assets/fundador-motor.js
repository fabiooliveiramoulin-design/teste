// Help Cure — cota fundadora: quem financia a Fase 1 recebe royalty sobre a receita de toda a rede.
// Regras (30/10/2026): 5% da receita de todas as entidades por 10 anos a partir da primeira receita;
// ao receber 5x a Fase 1, cai para 1% e fica. Valor residual: 1% ao fim do prazo, perpetuidade à TIR alvo (4x).
(function (root) {
  var REGRA = { taxa: 0.05, anos: 10, teto: 5, residual: 0.01 };
  // Cenários de expansão: [segmento, vidas (null = calculado no plano), ano t em que começa o Ano 0 do segmento]
  var CEN = [
    { id: "clin", seg: [["E1PY", 60000, 2]] }, // 30 clínicas de 2.000 vidas
    { id: "py", seg: [["E4", null, 2]] },
    { id: "pyp", seg: [["E4", null, 2], ["E2", null, 3]] },
    { id: "pype", seg: [["E4", null, 2], ["E2", null, 3], ["E3", null, 3]] },
    { id: "glob", seg: [["E4", null, 2], ["E2", null, 3], ["E2", null, 4], ["E3", null, 3], ["E5", null, 4]] }
  ];
  function calc(D, M, cen) {
    var P = D.premissas, I = P.f1cap, H = 2 + REGRA.anos, R = [], t, k;
    for (t = 0; t <= H; t++) R[t] = 0;
    cen.seg.forEach(function (s) {
      var c = M.calc(D, s[0], s[1] || D.escopos[s[0]].nbase).curva.receita;
      for (t = s[2]; t <= H; t++) { k = t - s[2]; R[t] += c[Math.min(k, 5)]; } // após o Ano 5, receita estável
    });
    var roy = [], fl = [], acum = 0, tetoAno = null;
    for (t = 0; t <= H; t++) {
      var taxa = acum >= REGRA.teto * I ? REGRA.residual : REGRA.taxa, v = taxa * R[t];
      if (taxa === REGRA.taxa && acum + v > REGRA.teto * I) { v = REGRA.teto * I - acum + REGRA.residual * (R[t] - (REGRA.teto * I - acum) / REGRA.taxa); tetoAno = t; }
      acum += v; roy[t] = v;
      fl[t] = v - (t <= 2 ? I * P.tr[t] : 0);
    }
    var resid = REGRA.residual * R[H] / P.tir; // perpetuidade do 1% residual
    var fT = fl.slice(); fT[H] += resid;
    var cum = 0, pb = null;
    for (t = 0; t <= H; t++) { cum += fl[t]; if (pb === null && t > 2 && cum >= 0) pb = t - 1 + (-(cum - fl[t]) / fl[t]); }
    return { aporte: I, royalties: roy, receitaRede: R, recebido10: acum, multiplo: acum / I, tir: M.irr(fT), payback: pb, tetoAno: tetoAno, residual: resid, H: H };
  }
  var api = { REGRA: REGRA, CEN: CEN, calc: calc };
  if (typeof module !== "undefined") module.exports = api; else root.HCFundador = api;
})(this);
