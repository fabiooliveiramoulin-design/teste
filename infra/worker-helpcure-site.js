// Help Cure — site (servido do GitHub) + área do investidor.
// Acesso: código do prospect (ex.: 2SEA-XXXX) → cadastro do investidor (nome, e-mail, telefone) → conteúdo completo
// (vídeos + investir.html, cifrado no repositório) → botão "Quero investir".
// Prospects no KV LEADS, chave "prospect:<PREFIXO>" = {nome, codigo, emails[], ativo}.
// E-mails via Apps Script do Google Workspace (segredos MAIL_URL e MAIL_KEY); sem eles, fica só o registro no KV.
const RAW = "https://raw.githubusercontent.com/fabiooliveiramoulin-design/teste/main";
const TYPES = { html: "text/html; charset=utf-8", css: "text/css; charset=utf-8", js: "application/javascript; charset=utf-8", svg: "image/svg+xml", webp: "image/webp", jpg: "image/jpeg", jpeg: "image/jpeg", png: "image/png", webmanifest: "application/manifest+json", json: "application/json", ico: "image/x-icon", mp4: "video/mp4", webm: "video/webm" };
const HC_MAIL = "investidores@helpcure.com.py";
// Páginas e scripts da área do investidor: só existem cifrados em /priv no repositório.
const PRIV = { "/investir.html": "investir.html", "/assets/viabilidade-dados.js": "assets__viabilidade-dados.js", "/assets/modelo-motor.js": "assets__modelo-motor.js", "/assets/viabilidade.js": "assets__viabilidade.js", "/assets/rede.js": "assets__rede.js" };
const VIDEOS = { pt: "tWPiFOwbaNw", es: "pTT-sQGMW0U", en: "2fYAVUm0ziI" };
const SHORTS = [
  { id: { pt: "CR9zwnwG_Lg", es: "2hfLJ0W2Y1s", en: "" }, d: "2:48", n: { pt: "Paciente", es: "Paciente", en: "Patient" } },
  { id: { pt: "DGMd9nJyOEg", es: "zBIRuKMUgQo", en: "" }, d: "2:46", n: { pt: "Hospital", es: "Hospital", en: "Hospital" } },
  { id: { pt: "PGypaX2jzqk", es: "SfoPAlmMvAk", en: "" }, d: "2:14", n: { pt: "Célula de atendimento", es: "Célula de atención", en: "Care cell" } },
  { id: { pt: "u_Oz8Sv924g", es: "Jut4FUUfuO4", en: "9X3sDuNgOQ0" }, d: "", n: { pt: "Unidade móvel", es: "Unidad móvil", en: "Mobile unit" } },
];

const L = {
  pt: { full: "Vídeo completo", mods: "Por módulo", lg: { pt: "em português", es: "em espanhol", en: "em inglês" }, t: "Área do investidor",
    sub: "Digite o código de acesso que você recebeu de quem indicou a Help Cure.", code: "Código de acesso", go: "Entrar", bad: "Código inválido. Confira e tente de novo.",
    ft: "Antes de começar", fs: "Para liberar o conteúdo completo, informe seus dados de contato.", nome: "Nome completo", email: "E-mail", tel: "Telefone (com DDD / código do país)",
    consent: "Autorizo a Help Cure e o parceiro que me indicou a usar estes dados para contato sobre o investimento, conforme a LGPD (Brasil) e a Lei 6534/2020 (Paraguai).",
    send: "Ver o conteúdo", need: "Preencha nome, e-mail válido e telefone, e marque a autorização.",
    h: "Help Cure para investidores", p: "Os vídeos da plataforma e o plano completo: modelo de receita, viabilidade por segmento, divisão de lucros e rodada.",
    plan: "Ver o plano completo", soon: "Vídeo disponível em breve.", app: "Abrir o app do paciente", back: "Voltar ao site", out: "Sair", conf: "Material confidencial. Não compartilhe o código de acesso.",
    qt: "Gostou do que viu?", qs: "Clique abaixo e a nossa equipe entra em contato pelo e-mail ou telefone que você cadastrou.", quero: "Quero investir",
    obr: "Obrigado pelo interesse na nossa inovação!", obs: "Entraremos em contato pelo e-mail ou telefone cadastrado. Enviamos uma confirmação para {e}.", voltar: "Voltar ao conteúdo",
    m_subj: "Help Cure — obrigado pelo seu interesse", m_body: "Olá, {n}!\n\nObrigado pelo interesse na nossa inovação. Entraremos em contato pelo e-mail ou telefone cadastrado.\n\nDados cadastrados:\nNome: {n}\nE-mail: {e}\nTelefone: {t}\n\nEquipe Help Cure\ninvestidores@helpcure.com.py · helpcure.com.py" },
  es: { full: "Video completo", mods: "Por módulo", lg: { pt: "en portugués", es: "en español", en: "en inglés" }, t: "Área del inversionista",
    sub: "Ingrese el código de acceso que recibió de quien le recomendó Help Cure.", code: "Código de acceso", go: "Entrar", bad: "Código inválido. Verifique e intente de nuevo.",
    ft: "Antes de empezar", fs: "Para liberar el contenido completo, informe sus datos de contacto.", nome: "Nombre completo", email: "Correo electrónico", tel: "Teléfono (con código de país)",
    consent: "Autorizo a Help Cure y al socio que me recomendó a usar estos datos para contactarme sobre la inversión, conforme a la Ley 6534/2020 (Paraguay) y la LGPD (Brasil).",
    send: "Ver el contenido", need: "Complete nombre, correo válido y teléfono, y marque la autorización.",
    h: "Help Cure para inversionistas", p: "Los videos de la plataforma y el plan completo: modelo de ingresos, viabilidad por segmento, participación en utilidades y ronda.",
    plan: "Ver el plan completo", soon: "Video disponible pronto.", app: "Abrir la app del paciente", back: "Volver al sitio", out: "Salir", conf: "Material confidencial. No comparta el código de acceso.",
    qt: "¿Le gustó lo que vio?", qs: "Haga clic abajo y nuestro equipo se pondrá en contacto por el correo o el teléfono que registró.", quero: "Quiero invertir",
    obr: "¡Gracias por su interés en nuestra innovación!", obs: "Nos pondremos en contacto por el correo electrónico o el teléfono registrado. Enviamos una confirmación a {e}.", voltar: "Volver al contenido",
    m_subj: "Help Cure — gracias por su interés", m_body: "Hola, {n}:\n\nGracias por su interés en nuestra innovación. Nos pondremos en contacto por el correo electrónico o el teléfono registrado.\n\nDatos registrados:\nNombre: {n}\nCorreo: {e}\nTeléfono: {t}\n\nEquipo Help Cure\ninvestidores@helpcure.com.py · helpcure.com.py" },
  en: { full: "Full video", mods: "By module", lg: { pt: "in Portuguese", es: "in Spanish", en: "in English" }, t: "Investor area",
    sub: "Enter the access code you received from whoever referred you to Help Cure.", code: "Access code", go: "Enter", bad: "Invalid code. Please check and try again.",
    ft: "Before you start", fs: "To unlock the full content, please share your contact details.", nome: "Full name", email: "Email", tel: "Phone (with country code)",
    consent: "I authorize Help Cure and the partner who referred me to use this data to contact me about the investment, under Brazil’s LGPD and Paraguay’s Law 6534/2020.",
    send: "See the content", need: "Please fill in your name, a valid email and phone, and tick the authorization.",
    h: "Help Cure for investors", p: "The platform videos and the full plan: revenue model, feasibility by segment, profit share and round.",
    plan: "See the full plan", soon: "Video coming soon.", app: "Open the patient app", back: "Back to the site", out: "Sign out", conf: "Confidential material. Do not share the access code.",
    qt: "Liked what you saw?", qs: "Click below and our team will contact you by the email or phone you registered.", quero: "I want to invest",
    obr: "Thank you for your interest in our innovation!", obs: "We will contact you by the email or phone you registered. A confirmation was sent to {e}.", voltar: "Back to the content",
    m_subj: "Help Cure — thank you for your interest", m_body: "Hello, {n},\n\nThank you for your interest in our innovation. We will contact you by the email or phone you registered.\n\nRegistered details:\nName: {n}\nEmail: {e}\nPhone: {t}\n\nHelp Cure team\ninvestidores@helpcure.com.py · helpcure.com.py" },
};
const NAMES = { pt: "Português", es: "Español", en: "English" };

async function hmac(key, msg) {
  const k = await crypto.subtle.importKey("raw", new TextEncoder().encode(key), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const s = await crypto.subtle.sign("HMAC", k, new TextEncoder().encode(msg));
  return [...new Uint8Array(s)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
function same(a, b) { if (a.length !== b.length) return false; let r = 0; for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i); return r === 0; }
function cookie(req, name) { const m = (req.headers.get("cookie") || "").match(new RegExp("(?:^|; )" + name + "=([^;]+)")); return m ? decodeURIComponent(m[1]) : ""; }
function esc(s) { return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]); }
function fill(s, o) { return s.replace(/\{(\w)\}/g, (_, k) => o[k] || ""); }
const b64u = (s) => btoa(unescape(encodeURIComponent(s))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const ub64u = (s) => decodeURIComponent(escape(atob(s.replace(/-/g, "+").replace(/_/g, "/"))));

// sessão assinada: {p: prefixo do prospect, l: id do cadastro (vazio antes do formulário)}
async function sign(env, obj) { const v = b64u(JSON.stringify(obj)); return v + "." + (await hmac(env.COOKIE_KEY, "sess:" + v)); }
async function session(req, env) {
  const c = cookie(req, "hc_sess"); if (!c || c.indexOf(".") < 0) return null;
  const [v, s] = c.split("."); if (!same(s, await hmac(env.COOKIE_KEY, "sess:" + v))) return null;
  let o; try { o = JSON.parse(ub64u(v)); } catch (e) { return null; }
  const pr = await prospect(env, o.p); if (!pr) return null; // prospect bloqueado ou removido: perde o acesso
  return { ...o, pr };
}
async function prospect(env, pref) { if (!pref) return null; const p = await env.LEADS.get("prospect:" + pref, "json"); return p && p.ativo ? p : null; }
const SC = (v, age) => `hc_sess=${encodeURIComponent(v)}; Path=/; Max-Age=${age}; Secure; HttpOnly; SameSite=Lax`;

async function mail(env, msg) {
  if (!env.MAIL_URL || !env.MAIL_KEY) return "sem-config";
  try {
    const r = await fetch(env.MAIL_URL, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ key: env.MAIL_KEY, ...msg }) });
    const t = await r.text(); return /"ok":\s*true/.test(t) ? "enviado" : "erro:" + t.slice(0, 120);
  } catch (e) { return "erro:" + String(e).slice(0, 120); }
}

function page(lang, body, opts = {}) {
  const t = L[lang];
  const langs = ["pt", "es", "en"].map((l) => `<a href="?lang=${l}" ${l === lang ? 'aria-current="true"' : ""}>${l.toUpperCase()}</a>`).join("");
  return `<!doctype html><html lang="${lang === "pt" ? "pt-BR" : lang}" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="google" content="notranslate"><title>Help Cure — ${esc(t.t)}</title><link rel="icon" href="/img/icone.svg"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Lexend:wght@300;400;500&display=swap">
<style>:root{--brand:#0B3B36;--led:#17B877;--ink:#E9F3F0;--ink2:#BFD3CD}*{box-sizing:border-box}body{margin:0;min-height:100vh;background:#06201C;color:var(--ink);font:16px/1.6 Lexend,system-ui,sans-serif}
header{display:flex;align-items:center;gap:16px;max-width:1100px;margin:0 auto;padding:18px 20px}header a.logo{font:700 20px Sora,sans-serif;color:var(--ink);text-decoration:none}header a.logo b{color:var(--led)}
nav{margin-left:auto;display:flex;gap:4px;background:rgba(255,255,255,.08);border-radius:999px;padding:3px}nav a{color:var(--ink2);text-decoration:none;font:600 12px Sora,sans-serif;padding:7px 10px;border-radius:999px}nav a[aria-current]{background:var(--led);color:#05241C}
main{max-width:1100px;margin:0 auto;padding:24px 20px 64px}h1{font:700 clamp(28px,4vw,44px)/1.15 Sora,sans-serif;margin:8px 0 10px}p{margin:0;color:var(--ink2)}
.gate{max-width:460px;margin:6vh auto 0;background:#0B2E2A;border:1px solid #1E4A44;border-radius:18px;padding:32px}.gate h1{font-size:26px}
label{display:block;font-size:14px;margin:18px 0 6px;color:var(--ink)}input[type=text],input[type=email],input[type=tel]{width:100%;min-height:48px;border-radius:12px;border:1px solid #2C5A53;background:#06201C;color:var(--ink);font:500 17px Lexend,sans-serif;padding:0 14px}input.code{letter-spacing:.08em;text-transform:uppercase}input:focus{outline:2px solid var(--led);outline-offset:1px}
.ck{display:flex;gap:10px;align-items:flex-start;font-size:13px;color:var(--ink2);margin-top:18px}.ck input{margin-top:4px;width:18px;height:18px;accent-color:var(--led);flex:none}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 22px;border-radius:999px;border:0;background:var(--led);color:#05241C;font:600 15px Sora,sans-serif;text-decoration:none;cursor:pointer}.btn.w{width:100%;margin-top:18px}.btn.g{background:transparent;color:var(--ink);border:1.5px solid #3C6A63}.btn.big{min-height:58px;font-size:18px;padding:0 34px}
.err{color:#FFB4A8;font-size:14px;margin-top:10px}
.tabs{display:flex;flex-wrap:wrap;gap:8px;margin:28px 0 16px}.tabs button{all:unset;cursor:pointer;padding:9px 16px;border-radius:999px;border:1px solid #2C5A53;font:600 14px Sora,sans-serif;color:var(--ink2)}.tabs button[aria-selected=true]{background:var(--led);border-color:var(--led);color:#05241C}
.player{aspect-ratio:16/9;border-radius:16px;overflow:hidden;background:#000 url(/img/hero.webp) center/cover;display:grid;place-items:center}.player iframe{width:100%;height:100%;border:0}.player span{background:rgba(6,32,28,.85);padding:12px 18px;border-radius:12px}
.h2{font:700 22px Sora,sans-serif;margin:40px 0 4px;color:var(--ink)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px;margin-top:16px}.sv{background:#0B2E2A;border:1px solid #1E4A44;border-radius:14px;overflow:hidden}.sv .f{aspect-ratio:16/9}.sv iframe{width:100%;height:100%;border:0;display:block}.sv b{display:block;padding:12px 14px 2px;font:600 15px Sora,sans-serif}.sv small{display:block;padding:0 14px 12px;color:#7FA39B}
.row{display:flex;flex-wrap:wrap;gap:12px;margin-top:24px}.conf{margin-top:32px;font-size:13px;color:#7FA39B}.quero{margin-top:48px;background:#0B2E2A;border:1px solid #1E4A44;border-radius:18px;padding:28px}</style></head>
<body><header><a class="logo" href="/" style="display:flex;align-items:center;gap:10px"><img src="/img/logo/helpcure-simbolo-animado-fundo-escuro.svg" alt="" aria-hidden="true" style="height:34px"><span style="letter-spacing:-.02em">Help<b>Cure</b></span></a><nav aria-label="Idioma">${langs}</nav></header><main>${body}</main></body></html>`;
}

function queroBox(lang) {
  const t = L[lang];
  return `<div class="quero"><h2 class="h2" style="margin-top:0">${t.qt}</h2><p>${t.qs}</p><form method="post" action="/investidores/quero-investir?lang=${lang}" style="margin-top:18px"><button class="btn big" type="submit">${t.quero}</button></form></div>`;
}

async function investors(req, env, url) {
  let lang = url.searchParams.get("lang") || cookie(req, "hc_lang") || "pt";
  if (!L[lang]) lang = "pt";
  const t = L[lang];
  const H = { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-frame-options": "DENY", "set-cookie": `hc_lang=${lang}; Path=/; Max-Age=31536000; Secure; SameSite=Lax` };
  const path = url.pathname.replace(/\/+$/, "") || "/investidores";

  if (path === "/investidores/sair") return new Response(null, { status: 302, headers: { location: "/investidores/?lang=" + lang, "set-cookie": SC("", 0) } });
  if (path === "/investidores/admin") return admin(req, env, url);

  const s = await session(req, env);

  // 1) código do prospect
  if (!s) {
    let error = "";
    if (req.method === "POST" && path === "/investidores") {
      const f = await req.formData();
      const code = String(f.get("code") || "").trim().toUpperCase().replace(/\s+/g, "");
      const pref = code.split("-")[0];
      const pr = /^[A-Z0-9]{2,8}$/.test(pref) ? await prospect(env, pref) : null;
      if (pr && same(code, String(pr.codigo).toUpperCase())) {
        return new Response(null, { status: 303, headers: { location: "/investidores/?lang=" + lang, "set-cookie": SC(await sign(env, { p: pref, l: "" }), 2592000) } });
      }
      error = t.bad;
    }
    return new Response(page(lang, `<div class="gate"><h1>${t.t}</h1><p>${t.sub}</p><form method="post" action="/investidores/?lang=${lang}"><label for="code">${t.code}</label><input class="code" type="text" id="code" name="code" autocomplete="off" autocapitalize="characters" required placeholder="XXXX-XXXX">${error ? `<div class="err" role="alert">${error}</div>` : ""}<button class="btn w" type="submit">${t.go}</button></form><div class="row"><a class="btn g" href="/">${t.back}</a></div></div>`), { status: error ? 401 : 200, headers: H });
  }

  // 2) cadastro do investidor
  if (!s.l) {
    let error = "", v = { nome: "", email: "", tel: "" };
    if (req.method === "POST" && path === "/investidores/cadastro") {
      const f = await req.formData(); const cut = (x, n) => String(f.get(x) || "").trim().slice(0, n);
      v = { nome: cut("nome", 120), email: cut("email", 160).toLowerCase(), tel: cut("tel", 40) };
      if (v.nome.length > 1 && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v.email) && v.tel.replace(/\D/g, "").length >= 8 && f.get("consent")) {
        const id = new Date().toISOString() + ":" + crypto.randomUUID().slice(0, 8);
        const rec = { ...v, prospect: s.p, prospectNome: s.pr.nome, idioma: lang, consent: true, quando: new Date().toISOString(), pais: (req.cf && req.cf.country) || "", eventos: [] };
        rec.mailCadastro = await mail(env, { to: s.pr.emails.join(","), cc: HC_MAIL, replyTo: v.email,
          subject: `Help Cure — novo investidor cadastrado (${s.pr.nome})`,
          text: `Um investidor indicado por ${s.pr.nome} se cadastrou na área do investidor da Help Cure.\n\nNome: ${v.nome}\nE-mail: ${v.email}\nTelefone: ${v.tel}\nIdioma: ${NAMES[lang]}\nPaís de acesso: ${rec.pais}\nData: ${rec.quando}\n\nO investidor autorizou o uso destes dados pela Help Cure e por ${s.pr.nome} para contato sobre o investimento.` });
        await env.LEADS.put("inv:" + s.p + ":" + id, JSON.stringify(rec));
        return new Response(null, { status: 303, headers: { location: "/investidores/?lang=" + lang, "set-cookie": SC(await sign(env, { p: s.p, l: id }), 2592000) } });
      }
      error = t.need;
    }
    return new Response(page(lang, `<div class="gate"><h1>${t.ft}</h1><p>${t.fs}</p><form method="post" action="/investidores/cadastro?lang=${lang}">
<label for="nome">${t.nome}</label><input type="text" id="nome" name="nome" autocomplete="name" required value="${esc(v.nome)}">
<label for="email">${t.email}</label><input type="email" id="email" name="email" autocomplete="email" required value="${esc(v.email)}">
<label for="tel">${t.tel}</label><input type="tel" id="tel" name="tel" autocomplete="tel" required value="${esc(v.tel)}">
<label class="ck"><input type="checkbox" name="consent" value="1" required><span>${t.consent}</span></label>
${error ? `<div class="err" role="alert">${error}</div>` : ""}<button class="btn w" type="submit">${t.send}</button></form><div class="row"><a class="btn g" href="/investidores/sair?lang=${lang}">${t.out}</a></div></div>`), { status: error ? 400 : 200, headers: H });
  }

  // 3) "Quero investir"
  if (path === "/investidores/quero-investir") {
    const k = "inv:" + s.p + ":" + s.l; const rec = await env.LEADS.get(k, "json");
    if (!rec) return new Response(null, { status: 302, headers: { location: "/investidores/sair?lang=" + lang } });
    if (req.method === "POST") {
      const last = (rec.eventos || []).filter((e) => e.tipo === "quero-investir").pop();
      if (last && Date.now() - Date.parse(last.quando) < 600000) return new Response(null, { status: 303, headers: { location: "/investidores/quero-investir?lang=" + lang } }); // evita e-mails repetidos em 10 min
      const st = await mail(env, { to: rec.email, cc: [...s.pr.emails, HC_MAIL].join(","), replyTo: HC_MAIL, subject: t.m_subj,
        text: fill(t.m_body, { n: rec.nome, e: rec.email, t: rec.tel }) + `\n\n— Indicação: ${s.pr.nome}` });
      rec.eventos.push({ tipo: "quero-investir", quando: new Date().toISOString(), mail: st });
      rec.queroInvestir = true; await env.LEADS.put(k, JSON.stringify(rec));
      return new Response(null, { status: 303, headers: { location: "/investidores/quero-investir?lang=" + lang } });
    }
    return new Response(page(lang, `<div class="gate"><h1>${t.obr}</h1><p>${fill(t.obs, { e: esc(rec.email) })}</p><div class="row"><a class="btn" href="/investidores/?lang=${lang}">${t.voltar}</a><a class="btn g" href="/">${t.back}</a></div></div>`), { headers: H });
  }

  // 4) conteúdo
  const order = [lang, ...["pt", "es", "en"].filter((l) => l !== lang)];
  const tabs = order.map((l, i) => `<button role="tab" aria-selected="${i === 0}" data-v="${VIDEOS[l]}">${NAMES[l]}</button>`).join("");
  return new Response(page(lang, `<h1>${t.h}</h1><p>${t.p}</p><div class="row"><a class="btn big" href="/investir.html">${t.plan}</a></div><h2 class="h2">${t.full}</h2><div class="tabs" role="tablist">${tabs}</div><div class="player" id="pl"></div><h2 class="h2">${t.mods}</h2><div class="grid">${SHORTS.map((v) => { const vl = v.id[lang] ? lang : "pt"; return `<div class="sv"><div class="f"><iframe src="https://www.youtube-nocookie.com/embed/${v.id[vl]}?rel=0&modestbranding=1" title="Help Cure — ${esc(v.n[lang])}" loading="lazy" allow="fullscreen; picture-in-picture; encrypted-media" allowfullscreen></iframe></div><b>${esc(v.n[lang])}</b><small>${t.lg[vl]}</small></div>`; }).join("")}</div>
${queroBox(lang)}
<div class="row"><a class="btn g" href="/app/">${t.app}</a><a class="btn g" href="/">${t.back}</a><a class="btn g" href="/investidores/sair?lang=${lang}">${t.out}</a></div><p class="conf">${t.conf}</p>
<script>var SOON=${JSON.stringify(t.soon)};function show(b){document.querySelectorAll('.tabs button').forEach(function(x){x.setAttribute('aria-selected',x===b)});var id=b.dataset.v,p=document.getElementById('pl');p.innerHTML=id?'<iframe src="https://www.youtube-nocookie.com/embed/'+id+'?rel=0&modestbranding=1" title="Help Cure" allow="fullscreen; picture-in-picture; encrypted-media" allowfullscreen></iframe>':'<span>'+SOON+'</span>'}document.querySelectorAll('.tabs button').forEach(function(b){b.onclick=function(){show(b)}});show(document.querySelector('.tabs button'));</script>`), { headers: H });
}

// Lista de cadastros (CSV): /investidores/admin?key=ADMIN_KEY[&p=2SEA]
async function admin(req, env, url) {
  if (!env.ADMIN_KEY || !same(url.searchParams.get("key") || "", env.ADMIN_KEY)) return new Response("Not found", { status: 404 });
  const pref = (url.searchParams.get("p") || "").toUpperCase();
  const rows = [["data", "prospect", "nome", "email", "telefone", "idioma", "pais", "quero_investir", "email_cadastro", "email_quero"]];
  let cur; do {
    const ls = await env.LEADS.list({ prefix: "inv:" + (pref ? pref + ":" : ""), cursor: cur }); cur = ls.list_complete ? null : ls.cursor;
    for (const k of ls.keys) { const r = await env.LEADS.get(k.name, "json"); if (!r) continue; const q = (r.eventos || []).filter((e) => e.tipo === "quero-investir");
      rows.push([r.quando, r.prospectNome || r.prospect, r.nome, r.email, r.tel, r.idioma, r.pais, q.length ? q[q.length - 1].quando : "", r.mailCadastro || "", q.length ? q[q.length - 1].mail : ""]); }
  } while (cur);
  const csv = "﻿" + rows.map((r) => r.map((c) => '"' + String(c).replace(/"/g, '""') + '"').join(";")).join("\r\n");
  return new Response(csv, { headers: { "content-type": "text/csv; charset=utf-8", "content-disposition": "attachment; filename=investidores_helpcure.csv", "cache-control": "no-store" } });
}

async function decrypt(env, b64) {
  const raw = Uint8Array.from(atob(b64.trim()), (c) => c.charCodeAt(0));
  const key = await crypto.subtle.importKey("raw", Uint8Array.from(atob(env.PRIV_KEY), (c) => c.charCodeAt(0)), { name: "AES-GCM" }, false, ["decrypt"]);
  return new Uint8Array(await crypto.subtle.decrypt({ name: "AES-GCM", iv: raw.slice(0, 12) }, key, raw.slice(12)));
}

async function privado(req, env, url, p) {
  const s = await session(req, env);
  if (!s || !s.l) return new Response(null, { status: 302, headers: { location: "/investidores/" } });
  const r = await fetch(RAW + "/priv/" + PRIV[p] + ".enc", { cf: { cacheTtl: 300, cacheEverything: true } });
  if (!r.ok) return new Response("Not found", { status: 404 });
  let body = await decrypt(env, await r.text());
  const ext = p.split(".").pop();
  if (ext === "html") {
    let lang = cookie(req, "hc_lang"); if (!L[lang]) lang = "pt";
    let h = new TextDecoder().decode(body);
    // botão "Quero investir" no fim da página e "Sair" no rodapé
    const box = `<section class="dark" id="quero-investir"><div class="wrap" style="text-align:center"><h2 style="margin:0 0 10px">${["pt", "es", "en"].map((l) => `<span lang="${l}" class="lq lq-${l}">${L[l].qt}</span>`).join("")}</h2><p style="max-width:60ch;margin:0 auto 22px">${["pt", "es", "en"].map((l) => `<span class="lq lq-${l}">${L[l].qs}</span>`).join("")}</p><form method="post" action="/investidores/quero-investir" onsubmit="this.action='/investidores/quero-investir?lang='+(document.documentElement.lang||'pt').slice(0,2)"><button class="btn primary" type="submit" style="font-size:18px;padding:16px 34px">${["pt", "es", "en"].map((l) => `<span class="lq lq-${l}">${L[l].quero}</span>`).join("")}</button></form><p style="margin-top:18px;font-size:13px"><a href="/investidores/" style="color:inherit">${["pt", "es", "en"].map((l) => `<span class="lq lq-${l}">${L[l].h}</span>`).join("")}</a> · <a href="/investidores/sair" style="color:inherit">${["pt", "es", "en"].map((l) => `<span class="lq lq-${l}">${L[l].out}</span>`).join("")}</a></p></div></section>
<style>.lq{display:none}html[lang^=pt] .lq-pt,html[lang=es] .lq-es,html[lang^=en] .lq-en{display:inline}</style>`;
    h = h.replace(/<footer/i, box + "<footer");
    if (h.indexOf('id="quero-investir"') < 0) h = h.replace(/<\/body>/i, box + "</body>");
    h = h.replace("<head>", '<head><meta name="robots" content="noindex,nofollow">');
    body = new TextEncoder().encode(h);
  }
  return new Response(body, { headers: { "content-type": TYPES[ext], "cache-control": "private, no-store", "x-content-type-options": "nosniff" } });
}

async function interesse(req, env) {
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405 });
  let d; try { d = await req.json(); } catch (e) { return new Response("bad", { status: 400 }); }
  const cut = (v, n) => String(v || "").trim().slice(0, n);
  const rec = { nome: cut(d.nome, 120), email: cut(d.email, 160), whatsapp: cut(d.whatsapp, 40), pais: cut(d.pais, 10), tipo: cut(d.tipo, 20), nivel: cut(d.nivel, 20), idioma: cut(d.idioma, 5), consent: d.consent === true, quando: new Date().toISOString(), cf_pais: (req.cf && req.cf.country) || "" };
  if (!rec.nome || (!rec.email && !rec.whatsapp) || !rec.consent) return new Response("bad", { status: 400 });
  await env.LEADS.put("lead:" + rec.quando + ":" + crypto.randomUUID().slice(0, 8), JSON.stringify(rec));
  return new Response(JSON.stringify({ ok: true }), { headers: { "content-type": "application/json" } });
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    let p = url.pathname;
    if (p === "/api/interesse") return interesse(req, env);
    if (p === "/investidores" || p.startsWith("/investidores/")) return investors(req, env, url);
    if (PRIV[p]) return privado(req, env, url, p);
    if (p.startsWith("/priv/")) return new Response("Not found", { status: 404 });
    if (p.includes("..")) return new Response("Bad request", { status: 400 });
    if (p.endsWith("/")) p += "index.html";
    else if (!/\.[a-z0-9]+$/i.test(p)) return Response.redirect(url.origin + p + "/" + url.search, 301);
    const r = await fetch(RAW + p, { cf: { cacheTtl: 300, cacheEverything: true } });
    if (!r.ok) return new Response("Página não encontrada / Página no encontrada / Page not found", { status: 404, headers: { "content-type": "text/plain; charset=utf-8" } });
    const ext = p.split(".").pop().toLowerCase();
    if (ext === "mp4" || ext === "webm") {
      const buf = await r.arrayBuffer(); const n = buf.byteLength;
      const vh = { "content-type": TYPES[ext], "accept-ranges": "bytes", "cache-control": "public, max-age=86400", "x-content-type-options": "nosniff" };
      const m = /bytes=(\d*)-(\d*)/.exec(req.headers.get("range") || "");
      if (m) {
        let a = m[1] === "" ? Math.max(0, n - Number(m[2])) : Number(m[1]);
        let b = m[1] !== "" && m[2] !== "" ? Math.min(Number(m[2]), n - 1) : n - 1;
        if (a >= n || a > b) return new Response(null, { status: 416, headers: { "content-range": `bytes */${n}` } });
        return new Response(buf.slice(a, b + 1), { status: 206, headers: { ...vh, "content-range": `bytes ${a}-${b}/${n}`, "content-length": String(b - a + 1) } });
      }
      return new Response(buf, { headers: { ...vh, "content-length": String(n) } });
    }
    return new Response(r.body, { headers: { "content-type": TYPES[ext] || "application/octet-stream", "cache-control": "public, max-age=300", "x-content-type-options": "nosniff" } });
  },
};
