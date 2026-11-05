// Help Farm — Área do investidor (/helpfarm/area-investidor), no mesmo modelo da área do Help Cure:
// código do prospect → cadastro do investidor → filme, vídeos explicativos e documentos cifrados → "Quero investir".
// Sem código: "Solicitar acesso" → investidores@ recebe link para liberar (gera código e envia ao investidor).
// KV LEADS com prefixos próprios: hfprospect:<PREF> = {nome, codigo, emails[], ativo}; hfinv:<PREF>:<id>; hfpedido:<id>.
// Segredos: COOKIE_KEY, HF_KEY (AES-256-GCM dos documentos em /priv/helpfarm), ADMIN_KEY; MAIL_URL/MAIL_KEY opcionais.
const HFA = "/helpfarm/area-investidor";
const HF_MAIL = "investidores@helpcure.com.py";
const HF_DOCS = [
  { f: "HelpFarm_Financiadores_Retorno_Valuation_previa.xlsx", n: { pt: "Financiadores, retorno e valuation (prévia)", es: "Financiadores, retorno y valuation (borrador)", en: "Funders, returns and valuation (draft)" }, k: "Excel" },
  { f: "HelpFarm_Pesquisa_Mercado_v2_16_paises.pdf", n: { pt: "Pesquisa de mercado v2 — 16 países", es: "Investigación de mercado v2 — 16 países", en: "Market research v2 — 16 countries" }, k: "PDF" },
  { f: "HelpFarm_Pesquisa_Mercado_v1_Cone_Sul.pdf", n: { pt: "Pesquisa de mercado v1 — Cone Sul", es: "Investigación de mercado v1 — Cono Sur", en: "Market research v1 — Southern Cone" }, k: "PDF" },
  { f: "HelpFarm_Modelo_Rentabilidade_v2.xlsx", n: { pt: "Modelo de rentabilidade por abrangência", es: "Modelo de rentabilidad por alcance", en: "Profitability model by scope" }, k: "Excel" },
  { f: "HelpFarm_Equipamentos_Unidade_Movel.xlsx", n: { pt: "Equipamentos da unidade móvel", es: "Equipos de la unidad móvil", en: "Mobile-unit equipment" }, k: "Excel" },
];
const HF_EXPL = [
  { k: "home", pt: "Como a Help Farm funciona", es: "Cómo funciona Help Farm", en: "How Help Farm works" },
  { k: "movel", pt: "Uma visita da unidade móvel", es: "Una visita de la unidad móvil", en: "A mobile-unit visit" },
  { k: "tec", pt: "O que é a assinatura de condição", es: "Qué es la firma de condición", en: "What a condition signature is" },
  { k: "cert", pt: "Do talhão ao QR code", es: "Del lote al código QR", en: "From field to QR code" },
  { k: "inv", pt: "Como a Help Farm gera receita", es: "Cómo genera ingresos Help Farm", en: "How Help Farm makes money" },
];
const HL = {
  pt: { t: "Área do investidor", ix: "A Área do Investidor reúne o material da rodada da Help Farm: pesquisa de mercado em 16 países, modelo de rentabilidade, unidade móvel e os vídeos do projeto. O acesso é restrito a quem tem interesse em investir.", sub: "Digite o código de acesso que você recebeu.", code: "Código de acesso", go: "Entrar", bad: "Código inválido. Confira e tente de novo.",
    ft: "Antes de começar", fs: "Para liberar o conteúdo, informe seus dados de contato.", nome: "Nome completo", email: "E-mail", tel: "WhatsApp (com código do país e DDD)",
    consent: "Autorizo a Help Farm e quem me indicou a usar estes dados para contato sobre o investimento, conforme a LGPD (Brasil) e a Lei 6534/2020 (Paraguai).", send: "Ver o conteúdo", need: "Preencha nome, e-mail válido e WhatsApp, e marque a autorização.",
    h: "Help Farm para investidores", p: "O filme, os vídeos explicativos e os documentos da rodada.", film: "O filme", expl: "Vídeos explicativos em desenho", soon: "em produção", docs: "Documentos", dl: "Baixar",
    back: "Voltar ao site", out: "Sair", conf: "Material confidencial. Não compartilhe o código de acesso.",
    qt: "Gostou do que viu?", qs: "Clique abaixo e a nossa equipe entra em contato pelo e-mail ou telefone que você cadastrou.", quero: "Quero investir",
    obr: "Obrigado pelo interesse!", obs: "Entraremos em contato pelo e-mail ou telefone cadastrado.", voltar: "Voltar ao conteúdo",
    nocode: "Não tenho código", rt: "Solicitar acesso", rx: "Preencha o cadastro: entraremos em contato e enviaremos o seu código de acesso ao material da Help Farm.", rconsent: "Autorizo a Help Farm a usar estes dados para contato sobre o investimento, conforme a LGPD (Brasil) e a Lei 6534/2020 (Paraguai).", rsend: "Enviar cadastro", rok: "Cadastro recebido. Muito obrigado!", roks: "Entraremos em contato e enviaremos o seu código de acesso.",
    c_subj: "Help Farm — seu código de acesso à Área do Investidor", c_body: "Olá, {n}!\n\nSeu acesso à Área do Investidor da Help Farm foi liberado.\n\nCódigo de acesso: {c}\nEntre em: {u}\n\nO material é confidencial. Por favor, não compartilhe o código.\n\nEquipe Help Farm",
    m_subj: "Help Farm — obrigado pelo seu interesse", m_body: "Olá, {n}!\n\nObrigado pelo interesse na Help Farm. Entraremos em contato pelo e-mail ou telefone cadastrado.\n\nEquipe Help Farm" },
  es: { t: "Área del inversionista", ix: "El Área del Inversionista reúne el material de la ronda de Help Farm: investigación de mercado en 16 países, modelo de rentabilidad, unidad móvil y los videos del proyecto. El acceso está restringido a quienes tienen interés en invertir.", sub: "Ingrese el código de acceso que recibió.", code: "Código de acceso", go: "Entrar", bad: "Código inválido. Verifique e intente de nuevo.",
    ft: "Antes de empezar", fs: "Para liberar el contenido, informe sus datos de contacto.", nome: "Nombre completo", email: "Correo electrónico", tel: "WhatsApp (con código de país)",
    consent: "Autorizo a Help Farm y a quien me recomendó a usar estos datos para contactarme sobre la inversión, conforme a la Ley 6534/2020 (Paraguay) y la LGPD (Brasil).", send: "Ver el contenido", need: "Complete nombre, correo válido y WhatsApp, y marque la autorización.",
    h: "Help Farm para inversionistas", p: "La película, los videos explicativos y los documentos de la ronda.", film: "La película", expl: "Videos explicativos en dibujo", soon: "en producción", docs: "Documentos", dl: "Descargar",
    back: "Volver al sitio", out: "Salir", conf: "Material confidencial. No comparta el código de acceso.",
    qt: "¿Le gustó lo que vio?", qs: "Haga clic abajo y nuestro equipo se pondrá en contacto por el correo o el teléfono que registró.", quero: "Quiero invertir",
    obr: "¡Gracias por su interés!", obs: "Nos pondremos en contacto por el correo o el teléfono registrado.", voltar: "Volver al contenido",
    nocode: "No tengo código", rt: "Solicitar acceso", rx: "Complete el registro: nos pondremos en contacto y le enviaremos su código de acceso al material de Help Farm.", rconsent: "Autorizo a Help Farm a usar estos datos para contactarme sobre la inversión, conforme a la Ley 6534/2020 (Paraguay) y la LGPD (Brasil).", rsend: "Enviar registro", rok: "Registro recibido. ¡Muchas gracias!", roks: "Nos pondremos en contacto y le enviaremos su código de acceso.",
    c_subj: "Help Farm — su código de acceso al Área del Inversionista", c_body: "Hola, {n}:\n\nSu acceso al Área del Inversionista de Help Farm fue liberado.\n\nCódigo de acceso: {c}\nIngrese en: {u}\n\nEl material es confidencial. Por favor, no comparta el código.\n\nEquipo Help Farm",
    m_subj: "Help Farm — gracias por su interés", m_body: "Hola, {n}:\n\nGracias por su interés en Help Farm. Nos pondremos en contacto por el correo o el teléfono registrado.\n\nEquipo Help Farm" },
  en: { t: "Investor area", ix: "The Investor Area holds the Help Farm round material: market research across 16 countries, profitability model, mobile unit and the project videos. Access is restricted to those interested in investing.", sub: "Enter the access code you received.", code: "Access code", go: "Enter", bad: "Invalid code. Please check and try again.",
    ft: "Before you start", fs: "To unlock the content, please enter your contact details.", nome: "Full name", email: "Email", tel: "WhatsApp (with country code)",
    consent: "I authorize Help Farm and whoever referred me to use this data to contact me about the investment, under Paraguay's Law 6534/2020 and Brazil's LGPD.", send: "See the content", need: "Enter your name, a valid email and WhatsApp, and tick the authorization.",
    h: "Help Farm for investors", p: "The film, the explainer videos and the round documents.", film: "The film", expl: "Hand-drawn explainer videos", soon: "in production", docs: "Documents", dl: "Download",
    back: "Back to the site", out: "Sign out", conf: "Confidential material. Do not share the access code.",
    qt: "Liked what you saw?", qs: "Click below and our team will contact you by the email or phone you registered.", quero: "I want to invest",
    obr: "Thank you for your interest!", obs: "We will contact you by the email or phone you registered.", voltar: "Back to the content",
    nocode: "I don't have a code", rt: "Request access", rx: "Fill in the form: we will get in touch and send you your access code to the Help Farm material.", rconsent: "I authorize Help Farm to use this data to contact me about the investment, under Paraguay's Law 6534/2020 and Brazil's LGPD.", rsend: "Send", rok: "Request received. Thank you very much!", roks: "We will get in touch and send you your access code.",
    c_subj: "Help Farm — your Investor Area access code", c_body: "Hello {n},\n\nYour access to the Help Farm Investor Area has been released.\n\nAccess code: {c}\nGo to: {u}\n\nThe material is confidential. Please do not share the code.\n\nHelp Farm team",
    m_subj: "Help Farm — thank you for your interest", m_body: "Hello {n},\n\nThank you for your interest in Help Farm. We will contact you by the email or phone you registered.\n\nHelp Farm team" },
};

async function hfHmac(key, msg) {
  const k = await crypto.subtle.importKey("raw", new TextEncoder().encode(key), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return [...new Uint8Array(await crypto.subtle.sign("HMAC", k, new TextEncoder().encode(msg)))].map((b) => b.toString(16).padStart(2, "0")).join("");
}
function hfSame(a, b) { if (a.length !== b.length) return false; let r = 0; for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i); return r === 0; }
function hfCookie(req, name) { const m = (req.headers.get("cookie") || "").match(new RegExp("(?:^|; )" + name + "=([^;]+)")); return m ? decodeURIComponent(m[1]) : ""; }
function hfEsc(s) { return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]); }
function hfFill(s, o) { return s.replace(/\{(\w)\}/g, (_, k) => o[k] || ""); }
const hfB64 = (s) => btoa(unescape(encodeURIComponent(s))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const hfUnB64 = (s) => decodeURIComponent(escape(atob(s.replace(/-/g, "+").replace(/_/g, "/"))));
const HF_CH = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
function hfRnd(n) { return Array.from(crypto.getRandomValues(new Uint8Array(n)), (x) => HF_CH[x % HF_CH.length]).join(""); }
async function hfMail(env, msg) {
  if (!env.MAIL_URL || !env.MAIL_KEY) return "sem-config";
  try { const r = await fetch(env.MAIL_URL, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ key: env.MAIL_KEY, ...msg }) }); const t = await r.text(); return /"ok":\s*true/.test(t) ? "enviado" : "erro:" + t.slice(0, 120); } catch (e) { return "erro:" + String(e).slice(0, 120); }
}
async function hfProspect(env, pref) { if (!pref) return null; const p = await env.LEADS.get("hfprospect:" + pref, "json"); return p && p.ativo ? p : null; }
async function hfSign(env, o) { const v = hfB64(JSON.stringify(o)); return v + "." + (await hfHmac(env.COOKIE_KEY, "hfsess:" + v)); }
async function hfSession(req, env) {
  const c = hfCookie(req, "hf_sess"); if (!c || c.indexOf(".") < 0) return null;
  const [v, s] = c.split("."); if (!hfSame(s, await hfHmac(env.COOKIE_KEY, "hfsess:" + v))) return null;
  let o; try { o = JSON.parse(hfUnB64(v)); } catch (e) { return null; }
  const pr = await hfProspect(env, o.p); return pr ? { ...o, pr } : null;
}
const hfSC = (v, age) => `hf_sess=${encodeURIComponent(v)}; Path=${HFA}; Max-Age=${age}; Secure; HttpOnly; SameSite=Lax`;
async function hfDecrypt(env, b64) {
  const raw = Uint8Array.from(atob(b64.trim()), (c) => c.charCodeAt(0));
  const key = await crypto.subtle.importKey("raw", Uint8Array.from(atob(env.HF_KEY), (c) => c.charCodeAt(0)), { name: "AES-GCM" }, false, ["decrypt"]);
  return new Uint8Array(await crypto.subtle.decrypt({ name: "AES-GCM", iv: raw.slice(0, 12) }, key, raw.slice(12)));
}

function hfPage(lang, body) {
  const t = HL[lang];
  const langs = ["pt", "es", "en"].map((l) => `<a href="?lang=${l}" ${l === lang ? 'aria-current="true"' : ""}>${l.toUpperCase()}</a>`).join("");
  return `<!doctype html><html lang="${lang === "pt" ? "pt-BR" : lang}" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Help Farm — ${hfEsc(t.t)}</title><link rel="icon" href="/helpfarm/assets/hf-icone.svg" type="image/svg+xml"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Lexend:wght@300;400;500&display=swap">
<style>:root{--deep:#2E1D10;--card:#3A2516;--line:#5A3F28;--led:#7DB547;--ink:#F5EBDD;--ink2:#D9C6AC;--q:#A48C70}*{box-sizing:border-box}body{margin:0;min-height:100vh;background:radial-gradient(120% 80% at 80% 0%,#4A2F1B 0%,#2E1D10 60%) fixed;color:var(--ink);font:16px/1.6 Lexend,system-ui,sans-serif}
header{display:flex;align-items:center;gap:16px;max-width:1100px;margin:0 auto;padding:18px 20px}header a.logo{display:flex;align-items:center;gap:10px;font:700 20px Sora,sans-serif;color:var(--ink);text-decoration:none}header a.logo b{color:var(--led)}
nav{margin-left:auto;display:flex;gap:4px;background:rgba(255,255,255,.08);border-radius:999px;padding:3px}nav a{color:var(--ink2);text-decoration:none;font:600 12px Sora,sans-serif;padding:7px 10px;border-radius:999px}nav a[aria-current]{background:var(--led);color:#1E2A0E}
main{max-width:1100px;margin:0 auto;padding:24px 20px 64px}h1{font:700 clamp(28px,4vw,44px)/1.15 Sora,sans-serif;margin:8px 0 10px}p{margin:0;color:var(--ink2)}
.gate{max-width:470px;margin:5vh auto 0;background:var(--card);border:1px solid var(--line);border-radius:20px;padding:32px;box-shadow:0 30px 70px rgba(0,0,0,.35)}.gate h1{font-size:26px}.gate .ix{color:var(--ink);border-left:3px solid var(--led);padding-left:12px;margin:12px 0 18px}
label{display:block;font-size:14px;margin:18px 0 6px}input[type=text],input[type=email],input[type=tel]{width:100%;min-height:48px;border-radius:12px;border:1px solid var(--line);background:#24170C;color:var(--ink);font:500 17px Lexend,sans-serif;padding:0 14px}input.code{letter-spacing:.08em;text-transform:uppercase}input:focus{outline:2px solid var(--led);outline-offset:1px}
.ck{display:flex;gap:10px;align-items:flex-start;font-size:13px;color:var(--ink2);margin-top:18px}.ck input{margin-top:4px;width:18px;height:18px;accent-color:var(--led);flex:none}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 22px;border-radius:999px;border:0;background:var(--led);color:#1E2A0E;font:600 15px Sora,sans-serif;text-decoration:none;cursor:pointer}.btn.w{width:100%;margin-top:18px}.btn.g{background:transparent;color:var(--ink);border:1.5px solid var(--line)}.btn.big{min-height:58px;font-size:18px;padding:0 34px}
.err{color:#FFB4A8;font-size:14px;margin-top:10px}.row{display:flex;flex-wrap:wrap;gap:12px;margin-top:24px}
.h2{font:700 22px Sora,sans-serif;margin:40px 0 12px}.film{aspect-ratio:16/9;border-radius:18px;overflow:hidden;background:#000;box-shadow:0 30px 70px rgba(0,0,0,.45)}.film video{width:100%;height:100%;display:block}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px}.ex{background:var(--card);border:1px dashed #8A6A48;border-radius:14px;padding:16px}.ex b{display:block;font:600 15px Sora,sans-serif}.ex small{color:var(--q)}
.docs{display:grid;gap:10px}.doc{display:flex;align-items:center;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;color:var(--ink);text-decoration:none}.doc:hover{border-color:var(--led)}.doc i{font:700 11px Sora,sans-serif;font-style:normal;background:#4A2F1B;color:var(--led);padding:6px 8px;border-radius:8px}.doc span{flex:1}.doc em{font-style:normal;color:var(--led);font:600 14px Sora,sans-serif}
.quero{margin-top:48px;background:var(--card);border:1px solid var(--line);border-radius:20px;padding:28px}.conf{margin-top:32px;font-size:13px;color:var(--q)}</style></head>
<body><header><a class="logo" href="/helpfarm/"><img src="/helpfarm/assets/hf-icone.svg" alt="" style="height:34px"><span style="letter-spacing:-.02em">Help<b>Farm</b></span></a><nav aria-label="Idioma">${langs}</nav></header><main>${body}</main></body></html>`;
}

async function hfArea(req, env, url, RAW) {
  let lang = url.searchParams.get("lang") || hfCookie(req, "hc_lang") || "pt"; if (!HL[lang]) lang = "pt";
  const t = HL[lang], A = HFA;
  const H = { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-frame-options": "DENY", "set-cookie": `hc_lang=${lang}; Path=/; Max-Age=31536000; Secure; SameSite=Lax` };
  const path = url.pathname.replace(/\/+$/, "") || A;
  const R = (body, st = 200) => new Response(hfPage(lang, body), { status: st, headers: H });
  const go = (loc, ck) => new Response(null, { status: 303, headers: ck ? { location: loc, "set-cookie": ck } : { location: loc } });
  const form = (action, fields, consent, btn, error, extra) => `<form method="post" action="${action}">${extra || ""}${fields}<label class="ck"><input type="checkbox" name="consent" value="1" required><span>${consent}</span></label>${error ? `<div class="err" role="alert">${error}</div>` : ""}<button class="btn w" type="submit">${btn}</button></form>`;
  const contact = (v) => `<label for="nome">${t.nome}</label><input type="text" id="nome" name="nome" autocomplete="name" required value="${hfEsc(v.nome)}"><label for="email">${t.email}</label><input type="email" id="email" name="email" autocomplete="email" required value="${hfEsc(v.email)}"><label for="tel">${t.tel}</label><input type="tel" id="tel" name="tel" autocomplete="tel" required value="${hfEsc(v.tel)}">`;
  const readContact = async () => { const f = await req.formData(); const cut = (x, n) => String(f.get(x) || "").trim().slice(0, n); const v = { nome: cut("nome", 120), email: cut("email", 160).toLowerCase(), tel: cut("tel", 40) }; return { f, v, ok: v.nome.length > 1 && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v.email) && v.tel.replace(/\D/g, "").length >= 8 && f.get("consent") }; };

  if (path === A + "/sair") return new Response(null, { status: 302, headers: { location: A + "/?lang=" + lang, "set-cookie": hfSC("", 0) } });

  if (path === A + "/admin") {
    if (!env.ADMIN_KEY || !hfSame(url.searchParams.get("key") || "", env.ADMIN_KEY)) return new Response("Not found", { status: 404 });
    // criar prospect: &novo=NOME&p=PREF  → devolve o código
    if (url.searchParams.get("novo")) {
      const pref = (url.searchParams.get("p") || "H" + hfRnd(4)).toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 8), codigo = pref + "-" + hfRnd(4);
      await env.LEADS.put("hfprospect:" + pref, JSON.stringify({ nome: url.searchParams.get("novo").slice(0, 80), codigo, emails: [HF_MAIL], ativo: true, criado: new Date().toISOString() }));
      return new Response(JSON.stringify({ prefixo: pref, codigo }), { headers: { "content-type": "application/json" } });
    }
    const rows = [["data", "prospect", "nome", "email", "telefone", "idioma", "pais", "quero_investir", "documentos"]];
    let cur; do { const ls = await env.LEADS.list({ prefix: "hfinv:", cursor: cur }); cur = ls.list_complete ? null : ls.cursor;
      for (const k of ls.keys) { const r = await env.LEADS.get(k.name, "json"); if (!r) continue; rows.push([r.quando, r.prospectNome, r.nome, r.email, r.tel, r.idioma, r.pais, (r.eventos || []).some((e) => e.tipo === "quero-investir") ? "sim" : "", [...new Set((r.eventos || []).filter((e) => e.tipo === "download").map((e) => e.doc))].join(" | ")]); } } while (cur);
    return new Response("﻿" + rows.map((r) => r.map((c) => '"' + String(c || "").replace(/"/g, '""') + '"').join(";")).join("\r\n"), { headers: { "content-type": "text/csv; charset=utf-8", "content-disposition": "attachment; filename=investidores_helpfarm.csv", "cache-control": "no-store" } });
  }

  if (path === A + "/solicitar") {
    let error = "", v = { nome: "", email: "", tel: "" };
    if (req.method === "POST") {
      const c = await readContact(); v = c.v;
      if (String(c.f.get("site") || "")) return R(`<div class="gate"><h1>${t.rok}</h1><p>${t.roks}</p></div>`);
      if (c.ok) {
        const id = new Date().toISOString() + ":" + crypto.randomUUID().slice(0, 8);
        const rec = { ...v, idioma: lang, consent: true, quando: new Date().toISOString(), pais: (req.cf && req.cf.country) || "", status: "pendente" };
        const link = `${url.origin}${A}/liberar?id=${encodeURIComponent(id)}&k=${await hfHmac(env.COOKIE_KEY, "hflib:" + id)}`;
        rec.mailInterno = await hfMail(env, { from: HF_MAIL, to: HF_MAIL, replyTo: v.email, subject: "Help Farm — pedido de acesso de investidor", text: `Novo pedido de acesso à Área do Investidor da Help Farm.\n\nNome: ${v.nome}\nE-mail: ${v.email}\nWhatsApp: ${v.tel}\nIdioma: ${lang}\nPaís: ${rec.pais || "-"}\n\nPara liberar o acesso (gera um código e envia ao investidor), abra:\n${link}` });
        rec.link = link; await env.LEADS.put("hfpedido:" + id, JSON.stringify(rec));
        return R(`<div class="gate"><h1>${t.rok}</h1><p>${t.roks}</p><div class="row"><a class="btn" href="/helpfarm/">${t.back}</a></div></div>`);
      }
      error = t.need;
    }
    return R(`<div class="gate"><h1>${t.rt}</h1><p>${t.rx}</p>${form(`${A}/solicitar?lang=${lang}`, contact(v), t.rconsent, t.rsend, error, '<input type="text" name="site" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">')}<div class="row"><a class="btn g" href="${A}/?lang=${lang}">${t.code}</a><a class="btn g" href="/helpfarm/">${t.back}</a></div></div>`, error ? 400 : 200);
  }

  if (path === A + "/liberar") {
    const id = url.searchParams.get("id") || "", k = url.searchParams.get("k") || "";
    if (!id || !k || !hfSame(k, await hfHmac(env.COOKIE_KEY, "hflib:" + id))) return new Response("Not found", { status: 404 });
    const rec = await env.LEADS.get("hfpedido:" + id, "json"); if (!rec) return new Response("Not found", { status: 404 });
    const dados = `<p>${hfEsc(rec.nome)}<br>${hfEsc(rec.email)}<br>WhatsApp: ${hfEsc(rec.tel)}</p>`;
    if (rec.status === "liberado") return R(`<div class="gate"><h1>Acesso já liberado</h1>${dados}<p>Código: <b>${hfEsc(rec.codigo)}</b></p></div>`);
    if (req.method !== "POST") return R(`<div class="gate"><h1>Liberar acesso do investidor</h1>${dados}<form method="post"><button class="btn w" type="submit">Liberar acesso e enviar o código</button></form></div>`);
    let pref; do { pref = "F" + hfRnd(4); } while (await env.LEADS.get("hfprospect:" + pref));
    const codigo = pref + "-" + hfRnd(4), tl = HL[rec.idioma] || HL.pt;
    await env.LEADS.put("hfprospect:" + pref, JSON.stringify({ nome: "Direto · " + rec.nome, codigo, emails: [HF_MAIL], ativo: true, criado: new Date().toISOString(), pedido: id }));
    rec.status = "liberado"; rec.codigo = codigo; rec.mailCodigo = await hfMail(env, { from: HF_MAIL, to: rec.email, replyTo: HF_MAIL, subject: tl.c_subj, text: hfFill(tl.c_body, { n: rec.nome, c: codigo, u: `${url.origin}${A}/?lang=${rec.idioma}` }) });
    await env.LEADS.put("hfpedido:" + id, JSON.stringify(rec));
    return R(`<div class="gate"><h1>Acesso liberado</h1>${dados}<p>Código: <b>${hfEsc(codigo)}</b><br>E-mail ao investidor: ${hfEsc(rec.mailCodigo)}</p></div>`);
  }

  const s = await hfSession(req, env);
  if (!s) {
    let error = "";
    if (req.method === "POST" && path === A) {
      const f = await req.formData(); const code = String(f.get("code") || "").trim().toUpperCase().replace(/\s+/g, ""); const pref = code.split("-")[0];
      const pr = /^[A-Z0-9]{2,8}$/.test(pref) ? await hfProspect(env, pref) : null;
      if (pr && hfSame(code, String(pr.codigo).toUpperCase())) {
        let lid = "";
        if (pr.pedido) { const pd = await env.LEADS.get("hfpedido:" + pr.pedido, "json"); if (pd) { lid = pr.pedido; const ik = "hfinv:" + pref + ":" + lid; if (!(await env.LEADS.get(ik))) await env.LEADS.put(ik, JSON.stringify({ nome: pd.nome, email: pd.email, tel: pd.tel, prospect: pref, prospectNome: pr.nome, idioma: lang, consent: true, quando: new Date().toISOString(), pais: pd.pais || "", eventos: [] })); } }
        return go(A + "/?lang=" + lang, hfSC(await hfSign(env, { p: pref, l: lid }), 2592000));
      }
      error = t.bad;
    }
    return R(`<div class="gate"><h1>${t.t}</h1><p class="ix">${t.ix}</p><p>${t.sub}</p><form method="post" action="${A}/?lang=${lang}"><label for="code">${t.code}</label><input class="code" type="text" id="code" name="code" autocomplete="off" autocapitalize="characters" required placeholder="XXXX-XXXX">${error ? `<div class="err" role="alert">${error}</div>` : ""}<button class="btn w" type="submit">${t.go}</button></form><div class="row"><a class="btn g" href="${A}/solicitar?lang=${lang}">${t.nocode}</a><a class="btn g" href="/helpfarm/">${t.back}</a></div></div>`, error ? 401 : 200);
  }

  if (!s.l) {
    let error = "", v = { nome: "", email: "", tel: "" };
    if (req.method === "POST" && path === A + "/cadastro") {
      const c = await readContact(); v = c.v;
      if (c.ok) {
        const id = new Date().toISOString() + ":" + crypto.randomUUID().slice(0, 8);
        const rec = { ...v, prospect: s.p, prospectNome: s.pr.nome, idioma: lang, consent: true, quando: new Date().toISOString(), pais: (req.cf && req.cf.country) || "", eventos: [] };
        rec.mailCadastro = await hfMail(env, { from: HF_MAIL, to: s.pr.emails.join(","), cc: HF_MAIL, replyTo: v.email, subject: `Help Farm — novo investidor cadastrado (${s.pr.nome})`, text: `Um investidor se cadastrou na área do investidor da Help Farm.\n\nNome: ${v.nome}\nE-mail: ${v.email}\nWhatsApp: ${v.tel}\nIndicação: ${s.pr.nome}\nIdioma: ${lang}\nPaís: ${rec.pais}` });
        await env.LEADS.put("hfinv:" + s.p + ":" + id, JSON.stringify(rec));
        return go(A + "/?lang=" + lang, hfSC(await hfSign(env, { p: s.p, l: id }), 2592000));
      }
      error = t.need;
    }
    return R(`<div class="gate"><h1>${t.ft}</h1><p>${t.fs}</p>${form(`${A}/cadastro?lang=${lang}`, contact(v), t.consent, t.send, error)}<div class="row"><a class="btn g" href="${A}/sair?lang=${lang}">${t.out}</a></div></div>`, error ? 400 : 200);
  }

  const ik = "hfinv:" + s.p + ":" + s.l;
  if (path.startsWith(A + "/docs/")) {
    const name = decodeURIComponent(path.slice((A + "/docs/").length));
    if (!HF_DOCS.some((d) => d.f === name)) return new Response("Not found", { status: 404 });
    const r = await fetch(RAW + "/priv/helpfarm/" + name + ".enc", { cf: { cacheTtl: 300, cacheEverything: true } });
    if (!r.ok) return new Response("Not found", { status: 404 });
    const body = await hfDecrypt(env, await r.text());
    try { const rec = await env.LEADS.get(ik, "json"); if (rec) { rec.eventos.push({ tipo: "download", doc: name, quando: new Date().toISOString() }); await env.LEADS.put(ik, JSON.stringify(rec)); } } catch (e) {}
    const ct = { pdf: "application/pdf", xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" }[name.split(".").pop()];
    return new Response(body, { headers: { "content-type": ct, "content-disposition": `attachment; filename="${name}"`, "cache-control": "private, no-store", "x-content-type-options": "nosniff" } });
  }

  if (path === A + "/quero-investir") {
    const rec = await env.LEADS.get(ik, "json");
    if (!rec) return new Response(null, { status: 302, headers: { location: A + "/sair?lang=" + lang } });
    if (req.method === "POST") {
      const last = (rec.eventos || []).filter((e) => e.tipo === "quero-investir").pop();
      if (!last || Date.now() - Date.parse(last.quando) > 600000) {
        const st = await hfMail(env, { from: HF_MAIL, to: rec.email, cc: [...s.pr.emails, HF_MAIL].join(","), replyTo: HF_MAIL, subject: t.m_subj, text: hfFill(t.m_body, { n: rec.nome }) + `\n\n— Indicação: ${s.pr.nome}\nWhatsApp do investidor: https://wa.me/${String(rec.tel).replace(/\D/g, "")}` });
        rec.eventos.push({ tipo: "quero-investir", quando: new Date().toISOString(), mail: st }); await env.LEADS.put(ik, JSON.stringify(rec));
      }
      return go(A + "/quero-investir?lang=" + lang);
    }
    return R(`<div class="gate"><h1>${t.obr}</h1><p>${t.obs}</p><div class="row"><a class="btn" href="${A}/?lang=${lang}">${t.voltar}</a><a class="btn g" href="/helpfarm/">${t.back}</a></div></div>`);
  }

  const docs = HF_DOCS.map((d) => `<a class="doc" href="${A}/docs/${encodeURIComponent(d.f)}"><i>${d.k}</i><span>${hfEsc(d.n[lang])}</span><em>${t.dl} ↓</em></a>`).join("");
  const ex = HF_EXPL.map((e) => `<div class="ex"><video controls playsinline preload="none" style="width:100%;aspect-ratio:16/9;border-radius:10px;display:block;margin-bottom:8px;background:#FBF8F1" poster="/helpfarm/video/expl-${e.k}-${lang}-poster.jpg" src="/helpfarm/video/expl-${e.k}-${lang}.mp4"></video><b>${hfEsc(e[lang])}</b><small>${lang.toUpperCase()}</small></div>`).join("");
  return R(`<h1>${t.h}</h1><p>${t.p}</p>
<h2 class="h2">${t.film}</h2><div class="film"><video controls playsinline preload="metadata" poster="/helpfarm/video/helpfarm-filme-${lang}-poster.jpg" src="/helpfarm/video/helpfarm-filme-${lang}.mp4"></video></div>
<h2 class="h2">${t.docs}</h2><div class="docs">${docs}</div>
<h2 class="h2">${t.expl}</h2><div class="grid">${ex}</div>
<div class="quero"><h2 class="h2" style="margin-top:0">${t.qt}</h2><p>${t.qs}</p><form method="post" action="${A}/quero-investir?lang=${lang}" style="margin-top:18px"><button class="btn big" type="submit">${t.quero}</button></form></div>
<div class="row"><a class="btn g" href="/helpfarm/">${t.back}</a><a class="btn g" href="${A}/sair?lang=${lang}">${t.out}</a></div><p class="conf">${t.conf}</p>`);
}

const RAW = "https://raw.githubusercontent.com/fabiooliveiramoulin-design/teste/helpfarm-v3";
const TYPES = { pdf: "application/pdf", html: "text/html; charset=utf-8", css: "text/css; charset=utf-8", js: "application/javascript; charset=utf-8", svg: "image/svg+xml", webp: "image/webp", jpg: "image/jpeg", png: "image/png", json: "application/json", mp4: "video/mp4" };
export default {
  async fetch(req, env) {
    const url = new URL(req.url); let p = url.pathname;
    if (p === "/" ) return Response.redirect(url.origin + "/helpfarm/", 302);
    if (p === HFA || p.startsWith(HFA + "/")) return hfArea(req, env, url, RAW);
    if (p.startsWith("/priv/") || p.includes("..")) return new Response("Not found", { status: 404 });
    if (p.endsWith("/")) p += "index.html"; else if (!/\.[a-z0-9]+$/i.test(p)) return Response.redirect(url.origin + p + "/" + url.search, 301);
    const r = await fetch(RAW + p, { cf: { cacheTtl: 60, cacheEverything: true } });
    if (!r.ok) return new Response("Not found", { status: 404 });
    const ext = p.split(".").pop().toLowerCase();
    if (ext === "mp4") {
      const buf = await r.arrayBuffer(); const n = buf.byteLength; const vh = { "content-type": "video/mp4", "accept-ranges": "bytes", "cache-control": "public, max-age=3600" };
      const m = /bytes=(\d*)-(\d*)/.exec(req.headers.get("range") || "");
      if (m) { let a = m[1] === "" ? Math.max(0, n - Number(m[2])) : Number(m[1]); let b = m[1] !== "" && m[2] !== "" ? Math.min(Number(m[2]), n - 1) : n - 1; if (a >= n || a > b) return new Response(null, { status: 416, headers: { "content-range": `bytes */${n}` } }); return new Response(buf.slice(a, b + 1), { status: 206, headers: { ...vh, "content-range": `bytes ${a}-${b}/${n}`, "content-length": String(b - a + 1) } }); }
      return new Response(buf, { headers: { ...vh, "content-length": String(n) } });
    }
    const h = { "content-type": TYPES[ext] || "application/octet-stream", "cache-control": "public, max-age=60" };
    if (ext === "html") h["x-robots-tag"] = "noindex";
    return new Response(r.body, { headers: h });
  },
};
