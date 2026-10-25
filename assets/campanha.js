// Help Cure Solidário — valores (assets/campanha.json) e formulário de interesse
(function () {
  function fmt(v, m) { try { return new Intl.NumberFormat(document.documentElement.lang || "pt-BR", { style: "currency", currency: m || "USD", maximumFractionDigits: 0 }).format(v); } catch (e) { return (m || "USD") + " " + v; } }
  function get(o, k) { return k.split(".").reduce(function (a, b) { return a == null ? a : a[b]; }, o); }
  var C = null;
  function paint() {
    if (!C) return;
    document.querySelectorAll("[data-camp]").forEach(function (el) {
      var v = get(C, el.dataset.camp);
      if (v == null) { el.classList.add("tbd"); return; }
      el.classList.remove("tbd");
      var s = el.querySelector("[data-i]"); if (s) s.removeAttribute("data-i");
      el.textContent = (el.dataset.camp.indexOf("niveis.") === 0 && el.dataset.camp !== "niveis.institucional" ? "" : "") + fmt(v, C.moeda) + (el.dataset.camp === "niveis.institucional" ? "+" : "");
    });
    var raised = C.arrecadado || 0, acc = 0;
    document.querySelectorAll("[data-meta]").forEach(function (card) {
      var goal = get(C, "metas." + card.dataset.meta), bar = card.querySelector(".bar i");
      if (!goal || !bar) return;
      var pct = Math.max(0, Math.min(100, (raised - acc) / goal * 100)); acc += goal;
      bar.style.width = pct + "%";
    });
  }

  // Marcadores por equipamento (célula / unidade móvel) — valores manuais em assets/campanha.json
  var EQ = { pt: { celula: "Célula", movel: "Unidade móvel", de: "de", ok: "Financiada ✓", pat: "Patrocinadores" },
             es: { celula: "Célula", movel: "Unidad móvil", de: "de", ok: "Financiada ✓", pat: "Patrocinadores" },
             en: { celula: "Care cell", movel: "Mobile unit", de: "of", ok: "Funded ✓", pat: "Sponsors" } };
  function paintEq() {
    var box = document.getElementById("equip"); if (!box || !C || !C.equipamentos) return;
    var l = (document.documentElement.lang || "pt").slice(0, 2); var t = EQ[l] || EQ.pt;
    box.innerHTML = "";
    C.equipamentos.forEach(function (e) {
      var a = e.arrecadado || 0, pct = e.meta ? Math.min(100, Math.round(a / e.meta * 100)) : 0, done = e.meta && a >= e.meta;
      var c = document.createElement("div"); c.className = "card meta eq" + (done ? " done" : "");
      var loc = (e.local && (e.local[l] || e.local.pt)) || "";
      var pats = (e.patrocinadores || []).filter(Boolean);
      c.innerHTML = '<div class="in"><h3></h3><p class="muted"></p><div class="mrow"><span></span><b></b></div><div class="bar" aria-hidden="true"><i></i></div>' + (pats.length ? '<p class="pats"></p>' : "") + "</div>";
      c.querySelector("h3").textContent = t[e.tipo] + " nº " + e.numero + (done ? " — " + t.ok : "");
      c.querySelector("p.muted").textContent = loc;
      c.querySelector(".mrow span").textContent = fmt(a, C.moeda) + " " + t.de + " " + fmt(e.meta, C.moeda);
      c.querySelector(".mrow b").textContent = pct + "%";
      if (pats.length) c.querySelector(".pats").textContent = t.pat + ": " + pats.join(", ");
      c.setAttribute("role", "group"); c.setAttribute("aria-label", c.querySelector("h3").textContent + ", " + pct + "%");
      box.appendChild(c);
      requestAnimationFrame(function () { c.querySelector(".bar i").style.width = pct + "%"; });
    });
  }
  document.querySelectorAll("[data-camp]").forEach(function (el) { el.classList.add("tbd"); });
  fetch("assets/campanha.json?t=" + Date.now()).then(function (r) { return r.json(); }).then(function (j) { C = j; paint(); paintEq(); }).catch(function () {});
  document.querySelectorAll(".lang button").forEach(function (b) { b.addEventListener("click", function () { setTimeout(function () { paint(); paintEq(); }, 0); }); });

  document.querySelectorAll("a[data-tipo]").forEach(function (a) { a.addEventListener("click", function () { var s = document.querySelector('#fcamp select[name="tipo"]'); if (s) s.value = a.dataset.tipo; }); });

  var f = document.getElementById("fcamp"); if (!f) return;
  var msg = f.querySelector(".msg");
  function say(k) { var m = f.querySelector('[data-m="' + k + '"]'); msg.textContent = m ? m.textContent : ""; msg.className = "msg " + (k === "ok" ? "ok" : "bad"); }
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    var d = {}; new FormData(f).forEach(function (v, k) { d[k] = String(v).trim(); });
    d.consent = f.consent.checked; d.idioma = (document.documentElement.lang || "pt").slice(0, 2);
    if (!d.nome || (!d.email && !d.whatsapp) || !d.consent) return say("bad");
    var btn = f.querySelector("button"); btn.disabled = true;
    fetch("/api/interesse", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(d) })
      .then(function (r) { if (!r.ok) throw 0; f.reset(); say("ok"); })
      .catch(function () { say("err"); })
      .finally(function () { btn.disabled = false; });
  });
})();
