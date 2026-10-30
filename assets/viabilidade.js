// Help Cure — viabilidade por segmento na página do investidor (barra de vidas + indicadores + valuation).
// Dados: assets/viabilidade-dados.js · Motor: assets/modelo-motor.js (mesmas fórmulas da planilha HelpCure_Equity_Lucros_Royalties).
(function () {
  var D = window.HC_VIAB, M = window.HCModelo;
  if (!D || !M) return;
  // Um segmento sozinho: o investidor dele é o fundador (Fase 1 + segmento + reserva), com divisão de lucros
  function calc(code, N) {
    var k = N / D.escopos[code].nbase, g = M.segmento(D, code, k), c = M.empresa(D, [[code, k, 2]], true), s0 = M.empresa(D, [[code, k, 2]], false);
    return { vidas: N, rodada: true, curva: g.curva, receita5: g.curva.receita[5], ebitda5: g.curva.ebitda[5], margem: g.curva.receita[5] ? g.curva.ebitda[5] / g.curva.receita[5] : 0,
      vpl: g.vpl, tir: g.tir, payback: g.payback, captacao: g.captacao, ticket: c.rodada, posmoney: c.posmoney, premoney: c.premoney,
      participacao: c.participacao, participacaoSem: s0.participacao, vpDivisao: c.vpDivisao };
  }
  var P = D.premissas;

  var TX = {
    pt: { mil: "mil", mi: "mi", bi: "bi", anos: "anos", ano: "Ano", mais5: "mais de 5 anos", sobre: "acima da referência", abaixo: "abaixo da referência", calc: "valor de referência",
      val: "Valuation da Help Cure (pré-money)", valE1: "Valor do projeto (VPL)", valsub: "valor da empresa antes do aporte, a 25% a.a.", valsubE1: "por clínica replicada, a 20% a.a.",
      neg: "não sustenta a rodada", margem: "margem", rec: "Receita", ebit: "EBITDA", vidas: "Vidas", caixa: "Caixa acumulado",
      ok: "Rodada viável: {p} da Help Cure entrega 25% a.a. ao investidor.",
      alto: "Rodada possível, mas cara: o investidor precisa de {p} da Help Cure para ter 25% a.a.",
      inv: "Nesta escala, nem 100% da Help Cure entrega 25% a.a. ao investidor.",
      ate: " Com {n}, a participação cai para {p}.", un: "vidas", cli: "vidas ({c} clínicas)", nunca: " Nem no máximo da barra a participação fica abaixo do limite.",
      e1ok: "Projeto viável por clínica: VPL positivo e payback de {pb}.", e1no: "Nesta escala o projeto não se paga em 5 anos.",
      vpln: "VPL negativo: nesta escala o segmento não cobre a sua estrutura fixa." },
    es: { mil: "mil", mi: "M", bi: "mil M", anos: "años", ano: "Año", mais5: "más de 5 años", sobre: "por encima de la referencia", abaixo: "por debajo de la referencia", calc: "valor de referencia",
      val: "Valuation de Help Cure (pre-money)", valE1: "Valor del proyecto (VAN)", valsub: "valor de la empresa antes del aporte, al 25% anual", valsubE1: "por clínica replicada, al 20% anual",
      neg: "no sostiene la ronda", margem: "margen", rec: "Ingresos", ebit: "EBITDA", vidas: "Vidas", caixa: "Caja acumulada",
      ok: "Ronda viable: el {p} de Help Cure entrega 25% anual al inversionista.",
      alto: "Ronda posible, pero cara: el inversionista necesita el {p} de Help Cure para obtener 25% anual.",
      inv: "En esta escala, ni el 100% de Help Cure entrega 25% anual al inversionista.",
      ate: " Con {n}, la participación baja al {p}.", un: "vidas", cli: "vidas ({c} clínicas)", nunca: " Ni en el máximo de la barra la participación queda por debajo del límite.",
      e1ok: "Proyecto viable por clínica: VAN positivo y payback de {pb}.", e1no: "En esta escala el proyecto no se paga en 5 años.",
      vpln: "VAN negativo: en esta escala el segmento no cubre su estructura fija." },
    en: { mil: "k", mi: "M", bi: "B", anos: "years", ano: "Year", mais5: "over 5 years", sobre: "above the reference", abaixo: "below the reference", calc: "reference value",
      val: "Help Cure valuation (pre-money)", valE1: "Project value (NPV)", valsub: "company value before the investment, at 25% a year", valsubE1: "per replicated clinic, at 20% a year",
      neg: "does not support the round", margem: "margin", rec: "Revenue", ebit: "EBITDA", vidas: "Lives", caixa: "Cumulative cash",
      ok: "Viable round: {p} of Help Cure delivers 25% a year to the investor.",
      alto: "Possible but expensive round: the investor needs {p} of Help Cure for 25% a year.",
      inv: "At this scale, not even 100% of Help Cure delivers 25% a year to the investor.",
      ate: " With {n}, the stake drops to {p}.", un: "lives", cli: "lives ({c} clinics)", nunca: " Even at the top of the slider the stake stays above the limit.",
      e1ok: "Viable project per clinic: positive NPV and payback of {pb}.", e1no: "At this scale the project does not pay back within 5 years.",
      vpln: "Negative NPV: at this scale the segment does not cover its fixed structure." }
  };
  function lang() { var l = (document.documentElement.lang || "pt").slice(0, 2); return TX[l] ? l : "pt"; }
  function dec(x, d, l) { var s = x.toFixed(d); return l === "en" ? s : s.replace(".", ","); }
  function int(x, l) { return Math.round(x).toLocaleString(l === "en" ? "en-US" : "de-DE"); }
  function usd(v, l) {
    var t = TX[l], a = Math.abs(v), s = v < 0 ? "−" : "", n;
    if (a >= 1e9) n = dec(a / 1e9, 1, l) + (l === "en" ? "" : " ") + t.bi;
    else if (a >= 1e6) n = dec(a / 1e6, a >= 1e8 ? 0 : 1, l) + (l === "en" ? "" : " ") + t.mi;
    else if (a >= 1e3) n = int(a / 1e3, l) + (l === "en" ? "" : " ") + t.mil;
    else n = int(a, l);
    return s + "US$ " + n;
  }
  function pct(x, l) { if (x === null || x === undefined) return "—"; if (Math.abs(x) >= 10) return (x > 0 ? "> " : "") + "1.000%".replace(".", l === "en" ? "," : "."); return (x < 0 ? "−" : "") + dec(Math.abs(x) * 100, Math.abs(x) < 0.1 ? 1 : 0, l) + "%"; }
  function yrs(x, l) { return x === null ? TX[l].mais5 : dec(x, 1, l) + " " + TX[l].anos; }
  function fill(s, o) { return s.replace(/\{(\w+)\}/g, function (_, k) { return o[k]; }); }

  // valores da barra: o calculado no plano + passos (5 mil ou 20 mil) até o máximo do segmento
  // valores da barra: passos fechados do mínimo ao máximo, com o valor calculado no plano incluído (a barra começa nele)
  function steps(S) {
    var v = [], x = Math.min(S.min, S.nbase);
    for (; x < S.nbase; x += S.passo) v.push(x);
    v.push(S.nbase); x = Math.ceil((S.nbase + 1) / S.passo) * S.passo;
    for (; x <= S.max; x += S.passo) v.push(x);
    if (v[v.length - 1] < S.max) v.push(S.max);
    return v;
  }

  var boxes = [];
  function load(b, code) {
    b.code = code; b.S = D.escopos[code];
    b.st = steps(b.S); b.R = b.st.map(function (n) { return calc(code, n); });
    b.i0 = b.st.indexOf(b.S.nbase); b.i = b.i0; b.inp.max = b.st.length - 1; b.inp.value = b.i0;
  }
  document.querySelectorAll(".viab[data-esc]").forEach(function (el) {
    if (!D.escopos[el.dataset.esc]) return;
    var b = { el: el, inp: el.querySelector("input[type=range]") };
    load(b, el.dataset.esc);
    b.inp.addEventListener("input", function () { b.i = +b.inp.value; paint(b); });
    el.querySelector(".vreset").addEventListener("click", function () { b.i = b.i0; b.inp.value = b.i0; paint(b); });
    // seletor de país (clínica: Paraguai ou Brasil, com preços e impostos de cada um)
    el.querySelectorAll(".vpais button[data-p]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        el.querySelectorAll(".vpais button[data-p]").forEach(function (x) { x.setAttribute("aria-pressed", x === btn ? "true" : "false"); });
        load(b, btn.dataset.p); paint(b);
      });
    });
    boxes.push(b);
  });

  function o(b, k) { return b.el.querySelector('[data-o="' + k + '"]'); }
  function set(b, k, v) { var e = o(b, k); if (e) e.textContent = v; }

  function paint(b) {
    var l = lang(), t = TX[l], r = b.R[b.i], e1 = !r.rodada;
    set(b, "vidas", int(r.vidas, l));
    set(b, "delta", b.i === b.i0 ? t.calc : r.vidas > b.S.nbase ? "+" + int(r.vidas - b.S.nbase, l) + " " + t.sobre : "−" + int(b.S.nbase - r.vidas, l) + " " + t.abaixo);
    set(b, "min", int(b.st[0], l)); set(b, "max", int(b.st[b.st.length - 1], l));
    b.inp.setAttribute("aria-valuetext", int(r.vidas, l));
    b.el.querySelector(".vreset").hidden = b.i === b.i0;
    // indicadores do projeto
    set(b, "vpl", usd(r.vpl, l)); set(b, "tir", pct(r.tir, l)); set(b, "payback", yrs(r.payback, l));
    set(b, "receita5", usd(r.receita5, l)); set(b, "ebitda5", usd(r.ebitda5, l) + " · " + pct(r.margem, l)); set(b, "captacao", usd(r.captacao, l));
    o(b, "vpl").classList.toggle("neg", r.vpl < 0);
    // valuation no fim da barra
    if (e1) {
      set(b, "vallab", t.valE1); set(b, "val", usd(r.vpl, l)); set(b, "valsub", t.valsubE1);
      set(b, "status", r.payback !== null && r.vpl > 0 ? fill(t.e1ok, { pb: yrs(r.payback, l) }) : t.e1no);
    } else {
      set(b, "vallab", t.val);
      set(b, "val", r.premoney > 0 ? usd(r.premoney, l) : t.neg); o(b, "val").classList.toggle("txt", !(r.premoney > 0));
      set(b, "valsub", r.premoney > 0 ? t.valsub : "");
      set(b, "ticket", usd(r.ticket, l)); set(b, "posmoney", usd(r.posmoney, l));
      set(b, "participacao", r.participacao > 1 ? "> 100%" : pct(r.participacao, l)); set(b, "semdiv", r.participacaoSem > 1 ? "> 100%" : pct(r.participacaoSem, l)); set(b, "vpdiv", usd(r.vpDivisao, l));
      var lim = b.code.indexOf("E1") === 0 ? 0.3 : 0.4; // rede de clínicas fundadora: no máximo 30%
      var msg = r.participacao <= lim ? fill(t.ok, { p: pct(r.participacao, l) }) : r.participacao <= 1 ? fill(t.alto, { p: pct(r.participacao, l) }) : t.inv;
      if (r.participacao > lim) {
        var j = -1; for (var q = b.i + 1; q < b.R.length; q++) if (b.R[q].participacao <= lim) { j = q; break; }
        msg += j >= 0 ? fill(t.ate, { n: int(b.R[j].vidas, l) + " " + (b.code.indexOf("E1") === 0 ? fill(t.cli, { c: int(b.R[j].vidas / b.S.nbase, l) }) : t.un), p: pct(b.R[j].participacao, l) }) : t.nunca;
      }
      if (r.vpl < 0) msg = t.vpln + " " + msg;
      set(b, "status", msg);
      o(b, "status").className = "vst " + (r.participacao <= lim && r.vpl >= 0 ? "good" : r.participacao <= 1 ? "warn" : "bad");
    }
    if (e1) o(b, "status").className = "vst " + (r.vpl > 0 ? "good" : "bad");
    chart(b, r, l);
  }
  // gráfico de barras: receita e EBITDA por ano (escala fixa no máximo da barra)
  var NS = "http://www.w3.org/2000/svg";
  function chart(b, r, l) {
    var box = b.el.querySelector(".vsvg"), W = box.clientWidth; if (!W) return;
    var t = TX[l], H = 230, padL = W < 500 ? 48 : 64, padR = 8, padT = 10, padB = 28, n = 6;
    var hi = Math.max.apply(null, r.curva.receita.concat(r.curva.ebitda)) * 1.08, lo = Math.min(0, Math.min.apply(null, r.curva.ebitda) * 1.15);
    var tk = niceTicks(lo, hi, 4); hi = Math.max(hi, tk[tk.length - 1]); lo = Math.min(lo, tk[0]); var span = hi - lo || 1;
    var Y = function (v) { return padT + (hi - v) / span * (H - padT - padB); };
    var gw = (W - padL - padR) / n, bw = Math.max(6, Math.min(26, gw / 3.2)), gap = 2;
    var s = '<svg viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H + '" role="img" aria-label="' + t.rec + " / " + t.ebit + '">';
    // grade recessiva
    var ticks = tk;
    ticks.forEach(function (v) { var y = Y(v); s += '<line x1="' + padL + '" x2="' + (W - padR) + '" y1="' + y + '" y2="' + y + '" class="' + (v === 0 ? "z" : "g") + '"/><text x="' + (padL - 8) + '" y="' + (y + 4) + '" text-anchor="end">' + usd(v, l).replace("US$ ", "").replace(/[.,]0(?=\D|$)/, "") + "</text>"; });
    function bar(x, v, cls) {
      var y0 = Y(0), y1 = Y(v), h = Math.abs(y1 - y0); if (h < 0.5) return "";
      var rr = Math.min(4, h, bw / 2), up = v >= 0, top = up ? y1 : y0, bot = up ? y0 : y1;
      var d = up ? "M" + x + "," + bot + "V" + (top + rr) + "Q" + x + "," + top + " " + (x + rr) + "," + top + "H" + (x + bw - rr) + "Q" + (x + bw) + "," + top + " " + (x + bw) + "," + (top + rr) + "V" + bot + "Z"
                 : "M" + x + "," + top + "V" + (bot - rr) + "Q" + x + "," + bot + " " + (x + rr) + "," + bot + "H" + (x + bw - rr) + "Q" + (x + bw) + "," + bot + " " + (x + bw) + "," + (bot - rr) + "V" + top + "Z";
      return '<path class="' + cls + '" d="' + d + '"/>';
    }
    for (var i = 0; i < n; i++) {
      var cx = padL + gw * i + gw / 2;
      s += bar(cx - bw - gap / 2, r.curva.receita[i], "br") + bar(cx + gap / 2, r.curva.ebitda[i], "be");
      s += '<text x="' + cx + '" y="' + (H - 8) + '" text-anchor="middle">' + (gw > 56 ? t.ano + " " : (i ? "" : t.ano.charAt(0) + " ")) + i + "</text>";
      s += '<rect class="hit" data-y="' + i + '" x="' + (padL + gw * i) + '" y="' + padT + '" width="' + gw + '" height="' + (H - padT - padB) + '"/>';
    }
    box.innerHTML = s + "</svg>";
    var tip = b.el.querySelector(".vtip");
    box.querySelectorAll(".hit").forEach(function (h) {
      function show() {
        var y = +h.dataset.y;
        tip.innerHTML = "<b>" + t.ano + " " + y + "</b><span><i class='sw r'></i>" + t.rec + ": " + usd(r.curva.receita[y], l) + "</span><span><i class='sw e'></i>" + t.ebit + ": " + usd(r.curva.ebitda[y], l) + "</span><span>" + t.vidas + ": " + int(r.curva.vidas[y], l) + "</span>";
        tip.style.left = (16 + Math.min(W - 190, Math.max(0, +h.getAttribute("x") + gw / 2 - 95))) + "px"; tip.classList.add("on");
        box.querySelectorAll(".hit").forEach(function (x) { x.classList.toggle("on", x === h); });
      }
      h.addEventListener("mouseenter", show); h.addEventListener("click", show);
    });
    box.addEventListener("mouseleave", function () { tip.classList.remove("on"); box.querySelectorAll(".hit").forEach(function (x) { x.classList.remove("on"); }); });
    // tabela equivalente
    var tb = "<thead><tr><th></th>" + [0, 1, 2, 3, 4, 5].map(function (y) { return '<th style="text-align:right">' + t.ano + " " + y + "</th>"; }).join("") + "</tr></thead><tbody>";
    [[t.vidas, "vidas", int], [t.rec, "receita", usd], [t.ebit, "ebitda", usd], [t.caixa, "caixa", usd]].forEach(function (row) {
      tb += "<tr><td>" + row[0] + "</td>" + r.curva[row[1]].map(function (v) { return '<td class="n">' + row[2](v, l) + "</td>"; }).join("") + "</tr>";
    });
    b.el.querySelector(".vtab").innerHTML = tb + "</tbody>";
  }
  function niceTicks(lo, hi, k) {
    var raw = (hi - lo) / k, p = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / p;
    var step = (m > 5 ? 10 : m > 2 ? 5 : m > 1 ? 2 : 1) * p, out = [];
    for (var v = Math.ceil(lo / step) * step; v <= hi + 1e-9; v += step) out.push(Math.abs(v) < 1e-9 ? 0 : v);
    return out;
  }

  function all() { boxes.forEach(paint); }
  all();
  new MutationObserver(all).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
  document.querySelectorAll(".ctabs button").forEach(function (x) { x.addEventListener("click", function () { setTimeout(all, 0); }); });
  var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(all, 120); });
})();
