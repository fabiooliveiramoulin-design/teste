// Help Farm — mapa interativo de certificação (ouro / prata / bronze / em adequação)
(function () {
  var root = document.getElementById("cmap");
  if (!root) return;

  var CRIT = [
    { k: "des", pt: "Livre de desmatamento (pós-2020)", es: "Libre de deforestación (pos-2020)", en: "Deforestation-free (post-2020)", s: { pt: "Desmatamento", es: "Deforestación", en: "Deforestation" } },
    { k: "ras", pt: "Rastreabilidade do lote", es: "Trazabilidad del lote", en: "Lot traceability", s: { pt: "Rastreio", es: "Trazabilidad", en: "Traceability" } },
    { k: "sol", pt: "Saúde do solo e carbono", es: "Salud del suelo y carbono", en: "Soil health and carbon", s: { pt: "Solo e carbono", es: "Suelo y carbono", en: "Soil & carbon" } },
    { k: "ins", pt: "Uso racional de insumos", es: "Uso racional de insumos", en: "Rational input use", s: { pt: "Insumos", es: "Insumos", en: "Inputs" } },
    { k: "agu", pt: "Água e clima", es: "Agua y clima", en: "Water and climate", s: { pt: "Água", es: "Agua", en: "Water" } },
    { k: "san", pt: "Sanidade e bem-estar", es: "Sanidad y bienestar", en: "Health and welfare", s: { pt: "Sanidade", es: "Sanidad", en: "Health" } }
  ];
  var CROP = {
    soy: { pt: "Soja e milho", es: "Soja y maíz", en: "Soybeans and corn" },
    soyw: { pt: "Soja e trigo", es: "Soja y trigo", en: "Soybeans and wheat" },
    corn: { pt: "Milho", es: "Maíz", en: "Corn" },
    beef: { pt: "Pecuária de corte", es: "Ganadería de carne", en: "Beef cattle" },
    dairy: { pt: "Leite", es: "Leche", en: "Dairy" }
  };
  var F = {
    be: { n: "Fazenda Boa Esperança", c: "soy", ha: 2850, s: [100, 98, 92, 90, 91, 94], demo: true },
    tr: { n: "Fazenda Três Rios", c: "soy", ha: 4100, s: [100, 96, 90, 88, 92, 90] },
    la: { n: "Tambo Los Álamos", c: "dairy", ha: 620, s: [100, 99, 88, 91, 93, 96] },
    sc: { n: "Estancia Santa Clara", c: "beef", ha: 5400, s: [100, 92, 74, 80, 78, 85] },
    pr: { n: "Fazenda Primavera", c: "corn", ha: 1900, s: [100, 88, 79, 72, 81, 77] },
    iv: { n: "Fazenda Itá Verá", c: "soy", ha: 3300, s: [100, 90, 70, 76, 74, 80] },
    sm: { n: "Granja San Miguel", c: "soyw", ha: 1450, s: [100, 84, 62, 58, 70, 66] },
    lp: { n: "Estancia La Paloma", c: "beef", ha: 3800, s: [100, 81, 55, 64, 60, 72] },
    yp: { n: "Estancia Yvy Porã", c: "beef", ha: 2600, s: [100, 80, 58, 61, 66, 63] },
    na: { n: "Fazenda Nova Aurora", c: "soy", ha: 2200, s: [0, 70, 65, 60, 72, 68], block: true }
  };
  var LV = {
    ouro: { pt: "Ouro", es: "Oro", en: "Gold", col: "#E2B53C", ink: "#7A5A06" },
    prata: { pt: "Prata", es: "Plata", en: "Silver", col: "#BCC5CD", ink: "#4E5A64" },
    bronze: { pt: "Bronze", es: "Bronce", en: "Bronze", col: "#C98446", ink: "#6B3A12" },
    adq: { pt: "Em adequação", es: "En adecuación", en: "In progress", col: "#D6CBBB", ink: "#8A3A22" }
  };
  var SC = [ // escala por critério
    { min: 90, col: "#3F7A22", pt: "90% ou mais", es: "90% o más", en: "90% or more" },
    { min: 75, col: "#7DB547", pt: "75–89%", es: "75–89%", en: "75–89%" },
    { min: 60, col: "#F2B53A", pt: "60–74%", es: "60–74%", en: "60–74%" },
    { min: 0, col: "#C4512B", pt: "abaixo de 60%", es: "menos de 60%", en: "below 60%" }
  ];
  var TX = {
    level: { pt: "Nível", es: "Nivel", en: "Level" },
    farms: { pt: "fazendas", es: "establecimientos", en: "farms" },
    certified: { pt: "ha certificados", es: "ha certificadas", en: "certified ha" },
    overall: { pt: "aderência geral", es: "adherencia general", en: "overall adherence" },
    tolv: { pt: "Para chegar a", es: "Para llegar a", en: "To reach" },
    raise: { pt: "subir", es: "subir", en: "raise" },
    to: { pt: "para", es: "a", en: "to" },
    avg: { pt: "e a média para", es: "y el promedio a", en: "and the average to" },
    top: { pt: "Nível máximo. Manter as notas na próxima safra.", es: "Nivel máximo. Mantener las notas en la próxima zafra.", en: "Top level. Keep the scores next season." },
    block: { pt: "Bloqueada: área de 18 ha aberta em 2022, detectada por satélite. Plano de recuperação acompanhado pela Help Farm; sem certificado até a regularização.", es: "Bloqueado: área de 18 ha abierta en 2022, detectada por satélite. Plan de recuperación acompañado por Help Farm; sin certificado hasta la regularización.", en: "Blocked: an 18 ha area cleared in 2022, detected by satellite. Recovery plan monitored by Help Farm; no certificate until resolved." },
    lot: { pt: "Ver o certificado de um lote", es: "Ver el certificado de un lote", en: "See a lot certificate" },
    nolot: { pt: "Certificados de lote desta fazenda: em breve na demonstração.", es: "Certificados de lote de este establecimiento: pronto en la demostración.", en: "Lot certificates for this farm: coming soon in the demo." },
    filter: { pt: "Toque para filtrar", es: "Toque para filtrar", en: "Tap to filter" },
    by: { pt: "Camada", es: "Capa", en: "Layer" },
    cleared: { pt: "Área aberta após 2020", es: "Área abierta después de 2020", en: "Area cleared after 2020" },
    reserve: { pt: "Reserva e mata ciliar", es: "Reserva y bosque ribereño", en: "Reserve and riverside forest" }
  };

  function L() { var l = (document.documentElement.lang || "pt").slice(0, 2); return l === "es" || l === "en" ? l : "pt"; }
  function avg(s) { return Math.round(s.reduce(function (a, b) { return a + b; }, 0) / s.length * 10) / 10; }
  function level(f) {
    var a = avg(f.s), mn = Math.min.apply(null, f.s);
    if (f.s[0] < 100 || f.s[1] < 80 || a < 60) return "adq";
    if (a >= 90 && mn >= 80) return "ouro";
    if (a >= 75 && mn >= 60) return "prata";
    return "bronze";
  }
  function scol(v) { for (var i = 0; i < SC.length; i++) if (v >= SC[i].min) return SC[i]; return SC[3]; }
  function fmt(n) { return n.toLocaleString(L() === "en" ? "en-US" : "es-PY"); }
  function pct(n) { var s = (Math.round(n * 10) / 10).toString(); return (L() === "en" ? s : s.replace(".", ",")) + "%"; }

  Object.keys(F).forEach(function (id) { F[id].lv = level(F[id]); F[id].a = avg(F[id].s); });

  var mode = -1, sel = "be", filt = null;
  var svg = root.querySelector("svg"), tip = document.getElementById("ctip");
  var modes = document.getElementById("cmodes"), legend = document.getElementById("clegend"), panel = document.getElementById("cpanel"), stats = document.getElementById("cstats");

  function paint() {
    root.querySelectorAll(".farm").forEach(function (g) {
      var f = F[g.dataset.id], base = g.querySelector(".base"), dot = g.querySelector(".dot");
      var c = mode < 0 ? LV[f.lv].col : scol(f.s[mode]).col;
      base.setAttribute("fill", c); dot.setAttribute("fill", c);
      g.classList.toggle("sel", g.dataset.id === sel);
      var hide = filt && (mode < 0 ? f.lv !== filt : scol(f.s[mode]).min !== filt);
      g.classList.toggle("dim", !!hide);
      g.classList.toggle("adq", f.lv === "adq");
    });
  }

  function renderModes() {
    var l = L(), h = '<span class="cm-l">' + TX.by[l] + ':</span><button type="button" data-m="-1">' + TX.level[l] + "</button>";
    CRIT.forEach(function (c, i) { h += '<button type="button" data-m="' + i + '">' + c.s[l] + "</button>"; });
    modes.innerHTML = h;
    modes.querySelectorAll("button").forEach(function (b) {
      b.setAttribute("aria-pressed", +b.dataset.m === mode ? "true" : "false");
      b.onclick = function () { mode = +b.dataset.m; filt = null; renderAll(); };
    });
  }

  function renderLegend() {
    var l = L(), h = "";
    if (mode < 0) {
      ["ouro", "prata", "bronze", "adq"].forEach(function (k) {
        var n = Object.keys(F).filter(function (id) { return F[id].lv === k; }).length;
        h += '<button type="button" data-f="' + k + '" class="lg' + (filt === k ? " on" : "") + '"><i style="background:' + LV[k].col + '"></i>' + LV[k][l] + " <em>" + n + "</em></button>";
      });
    } else {
      SC.forEach(function (s) { h += '<button type="button" data-f="' + s.min + '" class="lg' + (filt === s.min ? " on" : "") + '"><i style="background:' + s.col + '"></i>' + s[l] + "</button>"; });
    }
    h += '<span class="lgx"><i class="fx"></i>' + TX.reserve[l] + '</span><span class="lgx"><i class="cx"></i>' + TX.cleared[l] + "</span>";
    legend.innerHTML = h;
    legend.querySelectorAll("button").forEach(function (b) {
      b.title = TX.filter[l];
      b.onclick = function () { var v = mode < 0 ? b.dataset.f : +b.dataset.f; filt = filt === v ? null : v; renderAll(); };
    });
  }

  function renderStats() {
    var l = L(), ids = Object.keys(F), cnt = { ouro: 0, prata: 0, bronze: 0, adq: 0 }, ha = 0;
    ids.forEach(function (id) { cnt[F[id].lv]++; if (F[id].lv !== "adq") ha += F[id].ha; });
    stats.innerHTML = "<b>" + ids.length + "</b> " + TX.farms[l] + ' <span class="sep"></span><b>' + fmt(ha) + "</b> " + TX.certified[l];
  }

  function renderPanel() {
    var l = L(), f = F[sel], lv = f.lv;
    var md = lv === "adq" ? '<div class="nomedal">!</div>' : document.getElementById("md-" + lv).innerHTML;
    var bars = CRIT.map(function (c, i) {
      var v = f.s[i], sc = scol(v);
      return '<div class="bar' + (mode === i ? " hl" : "") + '"><div class="bl">' + c[l] + '</div><div class="bt"><i style="width:' + Math.max(v, 2) + "%;background:" + sc.col + '"></i></div><b>' + v + "%</b></div>";
    }).join("");
    var next = "";
    if (lv === "adq") next = '<p class="pnote bad">' + TX.block[l] + "</p>";
    else if (lv === "ouro") next = '<p class="pnote">' + TX.top[l] + "</p>";
    else {
      var tgt = lv === "bronze" ? "prata" : "ouro", mn = tgt === "ouro" ? 80 : 60, av = tgt === "ouro" ? 90 : 75;
      var low = CRIT.map(function (c, i) { return f.s[i] < mn ? c[l] + " (" + f.s[i] + "%)" : null; }).filter(Boolean);
      var parts = [];
      if (low.length) parts.push(TX.raise[l] + " " + low.join(", ") + " " + TX.to[l] + " " + mn + "%");
      if (f.a < av) parts.push((low.length ? TX.avg[l] : TX.raise[l] + " " + TX.overall[l] + " " + TX.to[l]) + " " + av + "%");
      next = '<p class="pnote"><b>' + TX.tolv[l] + " " + LV[tgt][l] + ":</b> " + parts.join(" ") + ".</p>";
    }
    var cta = f.demo ? '<a class="btn primary" href="lote-demo.html">' + TX.lot[l] + " →</a>" : '<p class="pfoot">' + TX.nolot[l] + "</p>";
    panel.innerHTML = '<div class="phead"><div class="pmedal">' + md + '</div><div><h3>' + f.n + '</h3><p class="pmeta">' + CROP[f.c][l] + " · " + fmt(f.ha) + ' ha</p><span class="ptag t-' + lv + '">' + LV[lv][l] + "</span></div></div>" +
      '<div class="pscore"><b>' + pct(f.a) + "</b><span>" + TX.overall[l] + "</span></div>" +
      '<div class="bars">' + bars + "</div>" + next + cta;
  }

  function renderAll() { paint(); renderModes(); renderLegend(); renderStats(); renderPanel(); }

  root.querySelectorAll(".farm").forEach(function (g) {
    var id = g.dataset.id;
    function pick() { sel = id; renderAll(); if (window.innerWidth < 960) panel.scrollIntoView({ behavior: "smooth", block: "nearest" }); }
    g.addEventListener("click", pick);
    g.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(); } });
    g.addEventListener("mousemove", function (e) {
      var l = L(), f = F[id], r = root.querySelector(".cmap-stage").getBoundingClientRect();
      var v = mode < 0 ? LV[f.lv][l] + " · " + pct(f.a) : CRIT[mode].s[l] + " · " + f.s[mode] + "%";
      tip.innerHTML = "<b>" + f.n + "</b><span>" + v + "</span>";
      tip.hidden = false;
      var x = e.clientX - r.left + 14, y = e.clientY - r.top + 14;
      if (x > r.width - 230) x = e.clientX - r.left - 230;
      tip.style.left = x + "px"; tip.style.top = y + "px";
    });
    g.addEventListener("mouseleave", function () { tip.hidden = true; });
  });

  new MutationObserver(renderAll).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
  renderAll();
})();
