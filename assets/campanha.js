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
  document.querySelectorAll("[data-camp]").forEach(function (el) { el.classList.add("tbd"); });
  fetch("assets/campanha.json?t=" + Date.now()).then(function (r) { return r.json(); }).then(function (j) { C = j; paint(); }).catch(function () {});
  document.querySelectorAll(".lang button").forEach(function (b) { b.addEventListener("click", function () { setTimeout(paint, 0); }); });

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
