// Help Cure — cota fundadora na página do investidor (seletor de cenário, indicadores e gráfico por ano).
(function () {
  var D = window.HC_VIAB, M = window.HCMotor, F = window.HCFundador, box = document.querySelector(".fund");
  if (!D || !M || !F || !box) return;
  var TX = {
    pt: { mil: "mil", mi: "mi", anos: "anos", ano: "Ano", nunca: "mais de 10 anos", roy: "Royalty", rede: "Receita da rede", acum: "Acumulado",
      teto: " Chega ao teto de 5× no ano {a}; depois recebe 1% para sempre.", semteto: " Não chega ao teto de 5× em 10 anos.",
      bom: "Com essa rede, o fundador tem {t} ao ano e recebe {m}× o investimento em 10 anos.", fraco: "Só com essa rede, o retorno do fundador é de {t} ao ano: a cota vale pela expansão do Help Cure.",
      mult: "{m}× o investimento" },
    es: { mil: "mil", mi: "M", anos: "años", ano: "Año", nunca: "más de 10 años", roy: "Royalty", rede: "Ingresos de la red", acum: "Acumulado",
      teto: " Llega al techo de 5× en el año {a}; después recibe 1% para siempre.", semteto: " No llega al techo de 5× en 10 años.",
      bom: "Con esta red, el fundador obtiene {t} anual y recibe {m}× la inversión en 10 años.", fraco: "Solo con esta red, el retorno del fundador es de {t} anual: la cuota vale por la expansión de Help Cure.",
      mult: "{m}× la inversión" },
    en: { mil: "k", mi: "M", anos: "years", ano: "Year", nunca: "over 10 years", roy: "Royalty", rede: "Network revenue", acum: "Cumulative",
      teto: " It reaches the 5× cap in year {a}; after that it earns 1% forever.", semteto: " It does not reach the 5× cap within 10 years.",
      bom: "With this network, the founder earns {t} a year and receives {m}× the investment in 10 years.", fraco: "With this network alone, the founder earns {t} a year: the share is worth it because of Help Cure’s expansion.",
      mult: "{m}× the investment" }
  };
  function lang() { var l = (document.documentElement.lang || "pt").slice(0, 2); return TX[l] ? l : "pt"; }
  function dec(x, d, l) { var s = x.toFixed(d); return l === "en" ? s : s.replace(".", ","); }
  function usd(v, l) { var t = TX[l], a = Math.abs(v), s = v < 0 ? "−" : "", sp = l === "en" ? "" : " ";
    var n = a >= 1e6 ? dec(a / 1e6, 1, l) + sp + t.mi : a >= 1e3 ? Math.round(a / 1e3) + sp + t.mil : String(Math.round(a)); return s + "US$ " + n; }
  function pct(x, l) { return x === null ? "—" : (x < 0 ? "−" : "") + dec(Math.abs(x) * 100, 0, l) + "%"; }
  function fill(s, o) { return s.replace(/\{(\w+)\}/g, function (_, k) { return o[k]; }); }
  function q(k) { return box.querySelector('[data-f="' + k + '"]'); }

  var cur = "clin";
  function paint() {
    var l = lang(), t = TX[l], cen = F.CEN.filter(function (c) { return c.id === cur; })[0], r = F.calc(D, M, cen);
    q("tir").textContent = pct(r.tir, l);
    q("rec").textContent = usd(r.recebido10, l) + " · " + dec(r.multiplo, 1, l) + "×";
    q("pb").textContent = r.payback === null ? t.nunca : dec(r.payback, 1, l) + " " + t.anos;
    var msg = fill(r.tir >= D.premissas.tir ? t.bom : t.fraco, { t: pct(r.tir, l), m: dec(r.multiplo, 1, l) });
    msg += r.tetoAno !== null ? fill(t.teto, { a: r.tetoAno }) : t.semteto;
    var m = q("msg"); m.textContent = msg; m.className = "vst " + (r.tir >= D.premissas.tir ? "good" : r.tir >= 0.12 ? "warn" : "bad");
    chart(r, l);
  }
  var NS = "http://www.w3.org/2000/svg";
  function chart(r, l) {
    var el = box.querySelector(".fsvg"), W = el.clientWidth; if (!W) return;
    var t = TX[l], H = 220, padL = W < 500 ? 44 : 60, padR = 8, padT = 10, padB = 28, ys = [];
    for (var y = 1; y <= r.H; y++) ys.push(y);
    var hi = Math.max.apply(null, r.royalties) * 1.1 || 1, raw = hi / 4, p = Math.pow(10, Math.floor(Math.log10(raw))), mm = raw / p;
    var step = (mm > 5 ? 10 : mm > 2 ? 5 : mm > 1 ? 2 : 1) * p; hi = Math.ceil(hi / step) * step;
    var Y = function (v) { return padT + (hi - v) / hi * (H - padT - padB); };
    var gw = (W - padL - padR) / ys.length, bw = Math.max(6, Math.min(30, gw * 0.55));
    var s = '<svg viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H + '" role="img" aria-label="' + t.roy + '">';
    for (var v = 0; v <= hi + 1e-9; v += step) s += '<line x1="' + padL + '" x2="' + (W - padR) + '" y1="' + Y(v) + '" y2="' + Y(v) + '" class="' + (v === 0 ? "z" : "g") + '"/><text x="' + (padL - 8) + '" y="' + (Y(v) + 4) + '" text-anchor="end">' + usd(v, l).replace("US$ ", "").replace(/[.,]0(?=\D|$)/, "") + "</text>";
    ys.forEach(function (yy, i) {
      var x = padL + gw * i + (gw - bw) / 2, val = r.royalties[yy], top = Y(val), bot = Y(0), h = bot - top, rr = Math.min(4, h, bw / 2);
      if (h > 0.5) s += '<path class="br" d="M' + x + "," + bot + "V" + (top + rr) + "Q" + x + "," + top + " " + (x + rr) + "," + top + "H" + (x + bw - rr) + "Q" + (x + bw) + "," + top + " " + (x + bw) + "," + (top + rr) + "V" + bot + 'Z"/>';
      if (gw > 34 || yy % 2 === 0) s += '<text x="' + (padL + gw * i + gw / 2) + '" y="' + (H - 8) + '" text-anchor="middle">' + (gw > 56 ? t.ano + " " : "") + yy + "</text>";
      s += '<rect class="hit" data-y="' + yy + '" x="' + (padL + gw * i) + '" y="' + padT + '" width="' + gw + '" height="' + (H - padT - padB) + '"/>';
    });
    el.innerHTML = s + "</svg>";
    var tip = box.querySelector(".ftip"), acc = [], a = 0;
    for (var k = 0; k <= r.H; k++) { a += r.royalties[k]; acc[k] = a; }
    el.querySelectorAll(".hit").forEach(function (h) {
      function show() { var yy = +h.dataset.y;
        tip.innerHTML = "<b>" + t.ano + " " + yy + "</b><span><i class='sw e'></i>" + t.roy + ": " + usd(r.royalties[yy], l) + "</span><span>" + t.rede + ": " + usd(r.receitaRede[yy], l) + "</span><span>" + t.acum + ": " + usd(acc[yy], l) + "</span>";
        tip.style.left = (16 + Math.min(W - 190, Math.max(0, +h.getAttribute("x") + gw / 2 - 95))) + "px"; tip.classList.add("on");
        el.querySelectorAll(".hit").forEach(function (x) { x.classList.toggle("on", x === h); }); }
      h.addEventListener("mouseenter", show); h.addEventListener("click", show);
    });
    el.addEventListener("mouseleave", function () { tip.classList.remove("on"); el.querySelectorAll(".hit").forEach(function (x) { x.classList.remove("on"); }); });
    var tb = "<thead><tr><th>" + t.ano + "</th><th style='text-align:right'>" + t.rede + "</th><th style='text-align:right'>" + t.roy + "</th><th style='text-align:right'>" + t.acum + "</th></tr></thead><tbody>";
    ys.forEach(function (yy) { tb += "<tr><td>" + yy + "</td><td class='n'>" + usd(r.receitaRede[yy], l) + "</td><td class='n'>" + usd(r.royalties[yy], l) + "</td><td class='n'>" + usd(acc[yy], l) + "</td></tr>"; });
    box.querySelector(".ftab").innerHTML = tb + "</tbody>";
  }
  box.querySelectorAll(".fcen button").forEach(function (b) {
    b.addEventListener("click", function () {
      cur = b.dataset.f;
      box.querySelectorAll(".fcen button").forEach(function (x) { x.setAttribute("aria-selected", x === b ? "true" : "false"); });
      paint();
    });
  });
  paint();
  new MutationObserver(paint).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
  var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(paint, 120); });
})();
