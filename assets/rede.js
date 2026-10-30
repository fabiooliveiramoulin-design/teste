// Help Cure — divisão de lucros na rede (seção #fundador) e tabela de captação, com o motor final (assets/modelo-motor.js).
(function () {
  var D = window.HC_VIAB, M = window.HCModelo;
  if (!D || !M) return;
  var REDE = {
    R1: [["E4", 1, 2], ["E2", 1, 3]],
    R2: [["E4", 1, 2], ["E2", 1, 3], ["E3", 1, 3]],
    R3: [["E4", 1, 2], ["E2", 1, 3], ["E2", 1, 4], ["E3", 1, 3], ["E5", 1, 4]],
    R4: [["E1PY", 30, 2], ["E4", 1, 3], ["E2", 1, 3], ["E3", 1, 4]]
  };
  var TX = {
    pt: { mil: "mil", mi: "mi", ano: "Ano", nf: "não fecha", div: "Divisão de lucros", rede: "EBITDA da rede", acum: "Acumulado",
      ok: "Com essa rede, basta vender {e} da Help Cure ao fundador: com a divisão de lucros ele tem 25% a.a.", alto: "Com essa rede, o fundador precisa de {e} da Help Cure para ter 25% a.a.", no: "Essa rede ainda não sustenta a rodada.",
      linhas: [["Rede de clínicas de porte médio — 30 clínicas (Paraguai)", [["E1PY", 30, 2]]], ["Rede de clínicas de porte médio — 50 clínicas (Paraguai)", [["E1PY", 50, 2]]],
        ["Plano de saúde (40 mil vidas)", [["E2", 1, 2]]], ["Estado brasileiro (média de RJ, SP, MG, BA, CE e PR)", [["E3", 1, 2]]], ["País: Paraguai", [["E4", 1, 2]]], ["País: Brasil", [["E5", 1, 2]]],
        ["Rede: Paraguai + plano de saúde", REDE.R1], ["Rede: Paraguai + plano + estado", REDE.R2], ["Rede: Paraguai, Brasil, estado e 2 planos", REDE.R3], ["Rede: clínicas fundadoras + Paraguai, plano e estado", REDE.R4]] },
    es: { mil: "mil", mi: "M", ano: "Año", nf: "no cierra", div: "Participación en utilidades", rede: "EBITDA de la red", acum: "Acumulado",
      ok: "Con esta red, basta vender el {e} de Help Cure al fundador: con la participación en utilidades obtiene 25% anual.", alto: "Con esta red, el fundador necesita el {e} de Help Cure para obtener 25% anual.", no: "Esta red todavía no sostiene la ronda.",
      linhas: [["Red de clínicas medianas — 30 clínicas (Paraguay)", [["E1PY", 30, 2]]], ["Red de clínicas medianas — 50 clínicas (Paraguay)", [["E1PY", 50, 2]]],
        ["Seguro de salud (40 mil vidas)", [["E2", 1, 2]]], ["Estado brasileño (promedio de RJ, SP, MG, BA, CE y PR)", [["E3", 1, 2]]], ["País: Paraguay", [["E4", 1, 2]]], ["País: Brasil", [["E5", 1, 2]]],
        ["Red: Paraguay + seguro de salud", REDE.R1], ["Red: Paraguay + seguro + estado", REDE.R2], ["Red: Paraguay, Brasil, estado y 2 seguros", REDE.R3], ["Red: clínicas fundadoras + Paraguay, seguro y estado", REDE.R4]] },
    en: { mil: "k", mi: "M", ano: "Year", nf: "does not close", div: "Profit share", rede: "Network EBITDA", acum: "Cumulative",
      ok: "With this network, selling {e} of Help Cure to the founder is enough: with the profit share it earns 25% a year.", alto: "With this network, the founder needs {e} of Help Cure to earn 25% a year.", no: "This network does not yet support the round.",
      linhas: [["Mid-size clinic network — 30 clinics (Paraguay)", [["E1PY", 30, 2]]], ["Mid-size clinic network — 50 clinics (Paraguay)", [["E1PY", 50, 2]]],
        ["Health plan (40,000 lives)", [["E2", 1, 2]]], ["Brazilian state (average of RJ, SP, MG, BA, CE and PR)", [["E3", 1, 2]]], ["Country: Paraguay", [["E4", 1, 2]]], ["Country: Brazil", [["E5", 1, 2]]],
        ["Network: Paraguay + health plan", REDE.R1], ["Network: Paraguay + plan + state", REDE.R2], ["Network: Paraguay, Brazil, state and 2 plans", REDE.R3], ["Network: founder clinics + Paraguay, plan and state", REDE.R4]] }
  };
  function lang() { var l = (document.documentElement.lang || "pt").slice(0, 2); return TX[l] ? l : "pt"; }
  function dec(x, d, l) { var s = x.toFixed(d); return l === "en" ? s : s.replace(".", ","); }
  function usd(v, l) { var t = TX[l], a = Math.abs(v), s = v < 0 ? "−" : "", sp = l === "en" ? "" : " ";
    var n = a >= 1e6 ? dec(a / 1e6, 1, l) + sp + t.mi : a >= 1e3 ? Math.round(a / 1e3) + sp + t.mil : String(Math.round(a)); return s + "US$ " + n; }
  function pct(x, l) { return dec(x * 100, x < 0.1 ? 1 : 0, l) + "%"; }
  function part(x, l) { return x > 1 ? TX[l].nf : pct(x, l); }
  function fill(s, o) { return s.replace(/\{(\w+)\}/g, function (_, k) { return o[k]; }); }

  // ---- tabela de captação
  function tabela() {
    var tb = document.getElementById("captab"); if (!tb) return;
    var l = lang();
    tb.innerHTML = TX[l].linhas.map(function (ln) {
      var r = M.empresa(D, ln[1], true);
      return "<tr><td>" + ln[0] + "</td><td class='n'>" + usd(r.rodada, l).replace("US$ ", "") + "</td><td class='n'>" + (r.premoney > 0 ? usd(r.premoney, l).replace("US$ ", "") : "—") + "</td><td class='n'><b>" + part(r.participacao, l) + "</b></td></tr>";
    }).join("");
  }

  // ---- seção de rede
  var box = document.querySelector(".fund"), cur = "R1";
  function q(k) { return box.querySelector('[data-f="' + k + '"]'); }
  function paint() {
    if (!box) return;
    var l = lang(), t = TX[l], r = M.empresa(D, REDE[cur], true), r0 = M.empresa(D, REDE[cur], false);
    q("e").textContent = part(r.participacao, l);
    q("pre").textContent = r.premoney > 0 ? usd(r.premoney, l) : "—";
    q("rod").textContent = usd(r.rodada, l);
    q("vpd").textContent = usd(r.vpDivisao, l);
    q("e0").textContent = part(r0.participacao, l);
    q("rec").textContent = usd(r.receita7, l);
    q("mult").textContent = dec(r.multiplo, 1, l) + "×";
    var m = q("msg"); m.textContent = r.participacao <= 0.4 ? fill(t.ok, { e: pct(r.participacao, l) }) : r.participacao <= 1 ? fill(t.alto, { e: pct(r.participacao, l) }) : t.no;
    m.className = "vst " + (r.participacao <= 0.4 ? "good" : r.participacao <= 1 ? "warn" : "bad");
    chart(r, l);
  }
  function chart(r, l) {
    var el = box.querySelector(".fsvg"), W = el.clientWidth; if (!W) return;
    var t = TX[l], H = 220, padL = W < 500 ? 44 : 60, padR = 8, padT = 10, padB = 28, ys = [1, 2, 3, 4, 5, 6, 7], v = r.divisao;
    var hi = Math.max.apply(null, v) * 1.1 || 1, raw = hi / 4, p = Math.pow(10, Math.floor(Math.log10(raw))), mm = raw / p;
    var step = (mm > 5 ? 10 : mm > 2 ? 5 : mm > 1 ? 2 : 1) * p; hi = Math.ceil(hi / step) * step;
    var Y = function (x) { return padT + (hi - x) / hi * (H - padT - padB); };
    var gw = (W - padL - padR) / ys.length, bw = Math.max(6, Math.min(34, gw * 0.5));
    var s = '<svg viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H + '" role="img" aria-label="' + t.div + '">';
    for (var x = 0; x <= hi + 1e-9; x += step) s += '<line x1="' + padL + '" x2="' + (W - padR) + '" y1="' + Y(x) + '" y2="' + Y(x) + '" class="' + (x === 0 ? "z" : "g") + '"/><text x="' + (padL - 8) + '" y="' + (Y(x) + 4) + '" text-anchor="end">' + usd(x, l).replace("US$ ", "").replace(/[.,]0(?=\D|$)/, "") + "</text>";
    ys.forEach(function (yy, i) {
      var x0 = padL + gw * i + (gw - bw) / 2, top = Y(v[yy]), bot = Y(0), h = bot - top, rr = Math.min(4, h, bw / 2);
      if (h > 0.5) s += '<path class="br" d="M' + x0 + "," + bot + "V" + (top + rr) + "Q" + x0 + "," + top + " " + (x0 + rr) + "," + top + "H" + (x0 + bw - rr) + "Q" + (x0 + bw) + "," + top + " " + (x0 + bw) + "," + (top + rr) + "V" + bot + 'Z"/>';
      s += '<text x="' + (padL + gw * i + gw / 2) + '" y="' + (H - 8) + '" text-anchor="middle">' + (gw > 56 ? t.ano + " " : "") + yy + "</text>";
      s += '<rect class="hit" data-y="' + yy + '" x="' + (padL + gw * i) + '" y="' + padT + '" width="' + gw + '" height="' + (H - padT - padB) + '"/>';
    });
    el.innerHTML = s + "</svg>";
    var tip = box.querySelector(".ftip"), acc = [], a = 0;
    for (var k = 0; k < 8; k++) { a += v[k]; acc[k] = a; }
    el.querySelectorAll(".hit").forEach(function (h) {
      function show() { var yy = +h.dataset.y;
        tip.innerHTML = "<b>" + t.ano + " " + yy + "</b><span><i class='sw e'></i>" + t.div + ": " + usd(v[yy], l) + "</span><span>" + t.acum + ": " + usd(acc[yy], l) + "</span>";
        tip.style.left = (16 + Math.min(W - 190, Math.max(0, +h.getAttribute("x") + gw / 2 - 95))) + "px"; tip.classList.add("on");
        el.querySelectorAll(".hit").forEach(function (z) { z.classList.toggle("on", z === h); }); }
      h.addEventListener("mouseenter", show); h.addEventListener("click", show);
    });
    el.addEventListener("mouseleave", function () { tip.classList.remove("on"); el.querySelectorAll(".hit").forEach(function (z) { z.classList.remove("on"); }); });
    box.querySelector(".ftab").innerHTML = "<thead><tr><th>" + t.ano + "</th><th style='text-align:right'>" + t.div + "</th><th style='text-align:right'>" + t.acum + "</th></tr></thead><tbody>" +
      ys.map(function (yy) { return "<tr><td>" + yy + "</td><td class='n'>" + usd(v[yy], l) + "</td><td class='n'>" + usd(acc[yy], l) + "</td></tr>"; }).join("") + "</tbody>";
  }
  if (box) box.querySelectorAll(".fcen button").forEach(function (b) {
    b.addEventListener("click", function () {
      cur = b.dataset.f;
      box.querySelectorAll(".fcen button").forEach(function (x) { x.setAttribute("aria-selected", x === b ? "true" : "false"); });
      paint();
    });
  });
  function all() { tabela(); paint(); }
  all();
  new MutationObserver(all).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
  var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(paint, 120); });
})();
