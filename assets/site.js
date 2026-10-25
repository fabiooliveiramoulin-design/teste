// Help Cure — idioma (PT/ES/EN), menu móvel e player de vídeo
(function () {
  var PT = {};
  document.querySelectorAll("[data-i]").forEach(function (el) { PT[el.dataset.i] = el.hasAttribute("data-html") ? el.innerHTML : el.textContent; });
  document.querySelectorAll("[data-alt]").forEach(function (el) { PT["alt:" + el.dataset.alt] = el.alt; });
  var T = window.HC_T || {}, cur = "pt";

  function setLang(l) {
    cur = l;
    var d = l === "pt" ? PT : (T[l] || {});
    document.querySelectorAll("[data-i]").forEach(function (el) {
      var v = d[el.dataset.i]; if (v == null) v = PT[el.dataset.i];
      if (el.hasAttribute("data-html")) el.innerHTML = v; else el.textContent = v;
    });
    document.querySelectorAll("[data-alt]").forEach(function (el) { var v = d["alt:" + el.dataset.alt] || PT["alt:" + el.dataset.alt]; if (v) el.alt = v; });
    document.documentElement.lang = { pt: "pt-BR", es: "es", en: "en" }[l];
    if (d._title) document.title = d._title; else if (PT._title) document.title = PT._title;
    document.querySelectorAll(".lang button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.l === l ? "true" : "false"); });
    document.querySelectorAll("a[data-inv]").forEach(function (a) { a.href = a.dataset.inv + "?lang=" + l; });
    try { localStorage.setItem("hc_lang", l); } catch (e) {}
    document.querySelectorAll(".video[data-ids]").forEach(function (v) { initVideo(v, l); });
    document.querySelectorAll("video[data-vbase]").forEach(function (v) {
      var b = v.dataset.vbase + "-" + l, src = b + ".mp4";
      if (v.dataset.cur === src) return;
      v.dataset.cur = src; v.poster = b + "-poster.jpg"; v.src = src; v.load();
    });
  }
  PT._title = document.title;

  // Vídeo: data-ids='{"pt":"ID","es":"ID","en":"ID"}', data-tabs="1" para mostrar abas de idioma
  var NAMES = { pt: "Português", es: "Español", en: "English" };
  var NOTE = { pt: { pt: "", es: "Vídeo em espanhol.", en: "Vídeo em inglês." }, es: { pt: "Video en portugués.", es: "", en: "Video en inglés." }, en: { pt: "Video in Portuguese.", es: "Video in Spanish.", en: "" } };
  function initVideo(box, lang) {
    var ids = JSON.parse(box.dataset.ids), tabs = box.querySelector(".vtabs"), pl = box.querySelector(".player"), note = box.querySelector(".vnote");
    function show(vl) {
      var id = ids[vl];
      pl.innerHTML = '<button type="button" class="poster" style="background-image:url(https://i.ytimg.com/vi/' + id + '/hqdefault.jpg)" aria-label="Play"><span><svg viewBox="0 0 24 24" fill="#05241C" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span></button>';
      pl.querySelector(".poster").onclick = function () {
        pl.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&modestbranding=1" title="Help Cure" allow="autoplay; fullscreen; picture-in-picture; encrypted-media" allowfullscreen></iframe>';
      };
      if (note) note.textContent = NOTE[lang][vl] || "";
      if (tabs) tabs.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-selected", b.dataset.v === vl ? "true" : "false"); });
    }
    if (tabs) {
      tabs.innerHTML = "";
      [lang].concat(["pt", "es", "en"].filter(function (x) { return x !== lang; })).forEach(function (l) {
        if (!ids[l]) return;
        var b = document.createElement("button"); b.type = "button"; b.role = "tab"; b.dataset.v = l; b.textContent = NAMES[l];
        b.onclick = function () { show(l); }; tabs.appendChild(b);
      });
    }
    show(ids[lang] ? lang : "pt");
  }

  document.querySelectorAll(".lang button").forEach(function (b) { b.addEventListener("click", function () { setLang(b.dataset.l); }); });
  var burger = document.querySelector(".burger");
  if (burger) burger.addEventListener("click", function () {
    var h = document.querySelector("header.top"); var o = h.classList.toggle("open"); burger.setAttribute("aria-expanded", o ? "true" : "false");
  });
  var start = "";
  try { start = new URLSearchParams(location.search).get("lang") || localStorage.getItem("hc_lang") || ""; } catch (e) {}
  if (!start) { var n = (navigator.language || "pt").slice(0, 2); start = n === "es" ? "es" : n === "en" ? "en" : "pt"; }
  if (!{ pt: 1, es: 1, en: 1 }[start]) start = "pt";
  setLang(start);
})();
