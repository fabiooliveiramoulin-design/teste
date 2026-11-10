// Help Cure — site (servido do GitHub) + área do investidor.
// Acesso: código do prospect (ex.: 2SEA-XXXX) → cadastro do investidor (nome, e-mail, telefone) → conteúdo completo
// (vídeos + investir.html, cifrado no repositório) → botão "Quero investir".
// Prospects no KV LEADS, chave "prospect:<PREFIXO>" = {nome, codigo, emails[], ativo}.
// E-mails via Apps Script "HelpCure Mailer (site)" na conta fabio.moulin@helpcure.com.py (segredos MAIL_URL e MAIL_KEY), enviando como investidores@ ou campanha@; sem eles, fica só o registro no KV.
const RAW = "https://raw.githubusercontent.com/fabiooliveiramoulin-design/teste/main";
const TYPES = { pdf: "application/pdf", html: "text/html; charset=utf-8", css: "text/css; charset=utf-8", js: "application/javascript; charset=utf-8", svg: "image/svg+xml", webp: "image/webp", jpg: "image/jpeg", jpeg: "image/jpeg", png: "image/png", webmanifest: "application/manifest+json", json: "application/json", ico: "image/x-icon", mp4: "video/mp4", webm: "video/webm" };
const HC_MAIL = "investidores@helpcure.com.py";
// Cópia dos avisos de investidores para a equipe (03/11/2026: Mara).
const INV_COPIA = "gilmaratinoco@gmail.com";
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
    sub: "Digite o código de acesso que você recebeu de quem indicou a Help Cure.", ix: "A Área do Investidor reúne o material da primeira análise econômica da Help Cure: CAPEX, OPEX, estrutura de equity, rentabilidade projetada e o retorno esperado para quem investe. Por isso, o acesso é restrito a quem tem interesse em investir no projeto.", code: "Código de acesso", go: "Entrar", bad: "Código inválido. Confira e tente de novo.",
    ft: "Antes de começar", fs: "Para liberar o conteúdo completo, informe seus dados de contato.", nome: "Nome completo", email: "E-mail", tel: "WhatsApp (com código do país e DDD)",
    consent: "Autorizo a Help Cure e o parceiro que me indicou a usar estes dados para contato sobre o investimento, conforme a LGPD (Brasil) e a Lei 6534/2020 (Paraguai).",
    send: "Ver o conteúdo", need: "Preencha nome, e-mail válido e WhatsApp, e marque a autorização.",
    h: "Help Cure para investidores", p: "Os vídeos da plataforma e o plano completo: modelo de receita, viabilidade por segmento, divisão de lucros e rodada.",
    plan: "Ver o plano completo", soon: "Vídeo disponível em breve.", app: "Abrir o app do paciente", back: "Voltar ao site", out: "Sair", conf: "Material confidencial. Não compartilhe o código de acesso.",
    qt: "Gostou do que viu?", qs: "Clique abaixo e a nossa equipe entra em contato pelo e-mail ou telefone que você cadastrou.", quero: "Quero investir",
    obr: "Obrigado pelo interesse na nossa inovação!", obs: "Entraremos em contato pelo e-mail ou telefone cadastrado. Enviamos uma confirmação para {e}.", voltar: "Voltar ao conteúdo",
    nocode: "Não tenho código", rt: "Solicitar acesso", rx: "A Área do Investidor dá acesso ao plano de negócios e de investimento de cada segmento da saúde em que a Help Cure atua. Se você tem interesse em investir, podemos enviar um código de acesso a um amplo material de análise. Preencha o cadastro: entraremos em contato e liberaremos o seu código. Muito obrigado!",
    rconsent: "Autorizo a Help Cure a usar estes dados para contato sobre o investimento, conforme a LGPD (Brasil) e a Lei 6534/2020 (Paraguai).", rsend: "Enviar cadastro", rok: "Cadastro recebido. Muito obrigado!", roks: "Entraremos em contato e enviaremos o seu código de acesso. Mandamos uma confirmação para {e}.",
    r_subj: "Help Cure — recebemos o seu pedido de acesso", r_body: "Olá, {n}!\n\nRecebemos o seu pedido de acesso à Área do Investidor da Help Cure. Entraremos em contato e, em seguida, enviaremos o seu código de acesso ao material de análise.\n\nDados cadastrados:\nNome: {n}\nE-mail: {e}\nWhatsApp: {t}\n\nMuito obrigado!\nEquipe Help Cure\ninvestidores@helpcure.com.py · helpcure.com.py",
    c_subj: "Help Cure — seu código de acesso à Área do Investidor", c_body: "Olá, {n}!\n\nSeu acesso à Área do Investidor da Help Cure foi liberado.\n\nCódigo de acesso: {c}\nEntre em: {u}\n\nO material é confidencial. Por favor, não compartilhe o código.\n\nEquipe Help Cure\ninvestidores@helpcure.com.py · helpcure.com.py",
    m_subj: "Help Cure — obrigado pelo seu interesse", m_body: "Olá, {n}!\n\nObrigado pelo interesse na nossa inovação. Entraremos em contato pelo e-mail ou telefone cadastrado.\n\nDados cadastrados:\nNome: {n}\nE-mail: {e}\nWhatsApp: {t}\n\nEquipe Help Cure\ninvestidores@helpcure.com.py · helpcure.com.py" },
  es: { full: "Video completo", mods: "Por módulo", lg: { pt: "en portugués", es: "en español", en: "en inglés" }, t: "Área del inversionista",
    sub: "Ingrese el código de acceso que recibió de quien le recomendó Help Cure.", ix: "El Área del Inversionista reúne el material del primer análisis económico de Help Cure: CAPEX, OPEX, estructura de equity, rentabilidad proyectada y el retorno esperado para quien invierte. Por eso, el acceso está restringido a quienes tienen interés en invertir en el proyecto.", code: "Código de acceso", go: "Entrar", bad: "Código inválido. Verifique e intente de nuevo.",
    ft: "Antes de empezar", fs: "Para liberar el contenido completo, informe sus datos de contacto.", nome: "Nombre completo", email: "Correo electrónico", tel: "WhatsApp (con código de país)",
    consent: "Autorizo a Help Cure y al socio que me recomendó a usar estos datos para contactarme sobre la inversión, conforme a la Ley 6534/2020 (Paraguay) y la LGPD (Brasil).",
    send: "Ver el contenido", need: "Complete nombre, correo válido y WhatsApp, y marque la autorización.",
    h: "Help Cure para inversionistas", p: "Los videos de la plataforma y el plan completo: modelo de ingresos, viabilidad por segmento, participación en utilidades y ronda.",
    plan: "Ver el plan completo", soon: "Video disponible pronto.", app: "Abrir la app del paciente", back: "Volver al sitio", out: "Salir", conf: "Material confidencial. No comparta el código de acceso.",
    qt: "¿Le gustó lo que vio?", qs: "Haga clic abajo y nuestro equipo se pondrá en contacto por el correo o el teléfono que registró.", quero: "Quiero invertir",
    obr: "¡Gracias por su interés en nuestra innovación!", obs: "Nos pondremos en contacto por el correo electrónico o el teléfono registrado. Enviamos una confirmación a {e}.", voltar: "Volver al contenido",
    nocode: "No tengo código", rt: "Solicitar acceso", rx: "El Área del Inversionista da acceso al plan de negocios y de inversión de cada segmento de la salud en el que actúa Help Cure. Si le interesa invertir, podemos enviarle un código de acceso a un amplio material de análisis. Complete el registro: nos pondremos en contacto y liberaremos su código. ¡Muchas gracias!",
    rconsent: "Autorizo a Help Cure a usar estos datos para contactarme sobre la inversión, conforme a la Ley 6534/2020 (Paraguay) y la LGPD (Brasil).", rsend: "Enviar registro", rok: "Registro recibido. ¡Muchas gracias!", roks: "Nos pondremos en contacto y le enviaremos su código de acceso. Enviamos una confirmación a {e}.",
    r_subj: "Help Cure — recibimos su solicitud de acceso", r_body: "Hola, {n}:\n\nRecibimos su solicitud de acceso al Área del Inversionista de Help Cure. Nos pondremos en contacto y luego le enviaremos su código de acceso al material de análisis.\n\nDatos registrados:\nNombre: {n}\nCorreo: {e}\nWhatsApp: {t}\n\n¡Muchas gracias!\nEquipo Help Cure\ninvestidores@helpcure.com.py · helpcure.com.py",
    c_subj: "Help Cure — su código de acceso al Área del Inversionista", c_body: "Hola, {n}:\n\nSu acceso al Área del Inversionista de Help Cure fue liberado.\n\nCódigo de acceso: {c}\nIngrese en: {u}\n\nEl material es confidencial. Por favor, no comparta el código.\n\nEquipo Help Cure\ninvestidores@helpcure.com.py · helpcure.com.py",
    m_subj: "Help Cure — gracias por su interés", m_body: "Hola, {n}:\n\nGracias por su interés en nuestra innovación. Nos pondremos en contacto por el correo electrónico o el teléfono registrado.\n\nDatos registrados:\nNombre: {n}\nCorreo: {e}\nWhatsApp: {t}\n\nEquipo Help Cure\ninvestidores@helpcure.com.py · helpcure.com.py" },
  en: { full: "Full video", mods: "By module", lg: { pt: "in Portuguese", es: "in Spanish", en: "in English" }, t: "Investor area",
    sub: "Enter the access code you received from whoever referred you to Help Cure.", ix: "The Investor Area holds the material for Help Cure's first economic analysis: CAPEX, OPEX, equity structure, projected profitability and the expected return for investors. That is why access is restricted to those interested in investing in the project.", code: "Access code", go: "Enter", bad: "Invalid code. Please check and try again.",
    ft: "Before you start", fs: "To unlock the full content, please share your contact details.", nome: "Full name", email: "Email", tel: "WhatsApp (with country code)",
    consent: "I authorize Help Cure and the partner who referred me to use this data to contact me about the investment, under Brazil’s LGPD and Paraguay’s Law 6534/2020.",
    send: "See the content", need: "Please fill in your name, a valid email and WhatsApp, and tick the authorization.",
    h: "Help Cure for investors", p: "The platform videos and the full plan: revenue model, feasibility by segment, profit share and round.",
    plan: "See the full plan", soon: "Video coming soon.", app: "Open the patient app", back: "Back to the site", out: "Sign out", conf: "Confidential material. Do not share the access code.",
    qt: "Liked what you saw?", qs: "Click below and our team will contact you by the email or phone you registered.", quero: "I want to invest",
    obr: "Thank you for your interest in our innovation!", obs: "We will contact you by the email or phone you registered. A confirmation was sent to {e}.", voltar: "Back to the content",
    nocode: "I don't have a code", rt: "Request access", rx: "The Investor Area gives access to the business and investment plan for each healthcare segment Help Cure works in. If you are interested in investing, we can send you an access code to extensive analysis material. Fill in the form: we will get in touch and release your code. Thank you very much!",
    rconsent: "I authorize Help Cure to use this data to contact me about the investment, under Paraguay's Law 6534/2020 and Brazil's LGPD.", rsend: "Send", rok: "Request received. Thank you very much!", roks: "We will get in touch and send you your access code. We sent a confirmation to {e}.",
    r_subj: "Help Cure — we received your access request", r_body: "Hello {n},\n\nWe received your request to access the Help Cure Investor Area. We will get in touch and then send you your access code to the analysis material.\n\nYour details:\nName: {n}\nEmail: {e}\nWhatsApp: {t}\n\nThank you very much!\nHelp Cure team\ninvestidores@helpcure.com.py · helpcure.com.py",
    c_subj: "Help Cure — your Investor Area access code", c_body: "Hello {n},\n\nYour access to the Help Cure Investor Area has been released.\n\nAccess code: {c}\nGo to: {u}\n\nThe material is confidential. Please do not share the code.\n\nHelp Cure team\ninvestidores@helpcure.com.py · helpcure.com.py",
    m_subj: "Help Cure — thank you for your interest", m_body: "Hello, {n},\n\nThank you for your interest in our innovation. We will contact you by the email or phone you registered.\n\nRegistered details:\nName: {n}\nEmail: {e}\nWhatsApp: {t}\n\nHelp Cure team\ninvestidores@helpcure.com.py · helpcure.com.py" },
};
const NAMES = { pt: "Português", es: "Español", en: "English" };
const CAMP_MAIL = "campanha@helpcure.com.py";
const CAMP_MSG = {
  pt: { s: "Help Cure Solidário — recebemos o seu pré-cadastro", b: "Olá, {n}!\n\nObrigado por se interessar pela campanha Help Cure Solidário. Recebemos o seu pré-cadastro e vamos avisar você assim que a campanha abrir oficialmente, com as metas, os níveis de apoio e a forma de contribuir.\n\nEnquanto isso, conheça a campanha em https://helpcure.com.py/solidario.html\n\nSe não foi você que fez este cadastro, basta responder este e-mail e removemos os seus dados.\n\nEquipe Help Cure\ncampanha@helpcure.com.py · helpcure.com.py" },
  es: { s: "Help Cure Solidario — recibimos su preinscripción", b: "Hola, {n}:\n\nGracias por interesarse en la campaña Help Cure Solidario. Recibimos su preinscripción y le avisaremos cuando la campaña abra oficialmente, con las metas, los niveles de apoyo y la forma de contribuir.\n\nMientras tanto, conozca la campaña en https://helpcure.com.py/solidario.html\n\nSi usted no hizo esta inscripción, responda este correo y eliminaremos sus datos.\n\nEquipo Help Cure\ncampanha@helpcure.com.py · helpcure.com.py" },
  en: { s: "Help Cure Solidarity — we received your pre-registration", b: "Hello, {n},\n\nThank you for your interest in the Help Cure Solidarity campaign. We received your pre-registration and will let you know when the campaign officially opens, with the goals, support levels and how to contribute.\n\nIn the meantime, see the campaign at https://helpcure.com.py/solidario.html\n\nIf you did not sign up, just reply to this email and we will delete your data.\n\nHelp Cure team\ncampanha@helpcure.com.py · helpcure.com.py" },
};

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

const WA_MSG = { pt: "Olá! Tenho interesse em investir na Help Cure.", es: "¡Hola! Tengo interés en invertir en Help Cure.", en: "Hi! I am interested in investing in Help Cure." };
function waFab(lang) { const m = WA_MSG[lang] || WA_MSG.pt; return `<a href="https://wa.me/595982235441?text=${encodeURIComponent(m)}" target="_blank" rel="noopener" aria-label="WhatsApp Help Cure" title="WhatsApp Help Cure" style="position:fixed;right:calc(18px + env(safe-area-inset-right,0px));bottom:calc(18px + env(safe-area-inset-bottom,0px));z-index:50;width:56px;height:56px;border-radius:50%;background:#17B877;color:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,.25)"><svg width="30" height="30" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.1 5.1 0 0 0 1.1 2.7 11.6 11.6 0 0 0 4.4 3.9c1.6.7 2.3.7 3.1.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg></a>`; }
function page(lang, body, opts = {}) {
  const t = L[lang];
  const langs = ["pt", "es", "en"].map((l) => `<a href="?lang=${l}" ${l === lang ? 'aria-current="true"' : ""}>${l.toUpperCase()}</a>`).join("");
  return `<!doctype html><html lang="${lang === "pt" ? "pt-BR" : lang}" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="google" content="notranslate"><title>Help Cure — ${esc(t.t)}</title><link rel="icon" href="/img/icone.svg"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Lexend:wght@300;400;500&display=swap">
<style>:root{--brand:#0B3B36;--led:#17B877;--ink:#E9F3F0;--ink2:#BFD3CD}*{box-sizing:border-box}body{margin:0;min-height:100vh;background:#06201C;color:var(--ink);font:16px/1.6 Lexend,system-ui,sans-serif}
header{display:flex;align-items:center;gap:16px;max-width:1100px;margin:0 auto;padding:18px 20px}header a.logo{font:700 20px Sora,sans-serif;color:var(--ink);text-decoration:none}header a.logo b{color:var(--led)}
nav{margin-left:auto;display:flex;gap:4px;background:rgba(255,255,255,.08);border-radius:999px;padding:3px}nav a{color:var(--ink2);text-decoration:none;font:600 12px Sora,sans-serif;padding:7px 10px;border-radius:999px}nav a[aria-current]{background:var(--led);color:#05241C}
main{max-width:1100px;margin:0 auto;padding:24px 20px 64px}h1{font:700 clamp(28px,4vw,44px)/1.15 Sora,sans-serif;margin:8px 0 10px}p{margin:0;color:var(--ink2)}
.gate{max-width:460px;margin:6vh auto 0;background:#0B2E2A;border:1px solid #1E4A44;border-radius:18px;padding:32px}.gate h1{font-size:26px}.gate .ix{color:#E9F3F0;border-left:3px solid #1FC07A;padding-left:12px;margin:12px 0 18px;line-height:1.55}
label{display:block;font-size:14px;margin:18px 0 6px;color:var(--ink)}input[type=text],input[type=email],input[type=tel]{width:100%;min-height:48px;border-radius:12px;border:1px solid #2C5A53;background:#06201C;color:var(--ink);font:500 17px Lexend,sans-serif;padding:0 14px}input.code{letter-spacing:.08em;text-transform:uppercase}input:focus{outline:2px solid var(--led);outline-offset:1px}
.ck{display:flex;gap:10px;align-items:flex-start;font-size:13px;color:var(--ink2);margin-top:18px}.ck input{margin-top:4px;width:18px;height:18px;accent-color:var(--led);flex:none}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 22px;border-radius:999px;border:0;background:var(--led);color:#05241C;font:600 15px Sora,sans-serif;text-decoration:none;cursor:pointer}.btn.w{width:100%;margin-top:18px}.btn.g{background:transparent;color:var(--ink);border:1.5px solid #3C6A63}.btn.big{min-height:58px;font-size:18px;padding:0 34px}
.err{color:#FFB4A8;font-size:14px;margin-top:10px}
.tabs{display:flex;flex-wrap:wrap;gap:8px;margin:28px 0 16px}.tabs button{all:unset;cursor:pointer;padding:9px 16px;border-radius:999px;border:1px solid #2C5A53;font:600 14px Sora,sans-serif;color:var(--ink2)}.tabs button[aria-selected=true]{background:var(--led);border-color:var(--led);color:#05241C}
.player{aspect-ratio:16/9;border-radius:16px;overflow:hidden;background:#000 url(/img/hero.webp) center/cover;display:grid;place-items:center}.player iframe{width:100%;height:100%;border:0}.player span{background:rgba(6,32,28,.85);padding:12px 18px;border-radius:12px}
.h2{font:700 22px Sora,sans-serif;margin:40px 0 4px;color:var(--ink)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px;margin-top:16px}.sv{background:#0B2E2A;border:1px solid #1E4A44;border-radius:14px;overflow:hidden}.sv .f{aspect-ratio:16/9}.sv iframe{width:100%;height:100%;border:0;display:block}.sv b{display:block;padding:12px 14px 2px;font:600 15px Sora,sans-serif}.sv small{display:block;padding:0 14px 12px;color:#7FA39B}
.row{display:flex;flex-wrap:wrap;gap:12px;margin-top:24px}.conf{margin-top:32px;font-size:13px;color:#7FA39B}.quero{margin-top:48px;background:#0B2E2A;border:1px solid #1E4A44;border-radius:18px;padding:28px}</style></head>
<body><header><a class="logo" href="/" style="display:flex;align-items:center;gap:10px"><img src="/img/logo/helpcure-simbolo-animado-fundo-escuro.svg" alt="" aria-hidden="true" style="height:34px"><span style="letter-spacing:-.02em">Help<b>Cure</b></span></a><nav aria-label="Idioma">${langs}</nav></header><main>${body}</main>${waFab(lang)}</body></html>`;
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

  // Origem de marketing (?c=CANAL ou utm_source) para quem chega sem código de prospect.
  const oc = (url.searchParams.get("c") || url.searchParams.get("utm_source") || "").replace(/[^A-Za-z0-9_-]/g, "").slice(0, 30).toUpperCase();
  if (path === "/investidores/solicitar") return solicitar(req, env, url, lang, H, oc);
  if (path === "/investidores/liberar") return liberar(req, env, url);

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
        let lid = ""; // investidor direto: o cadastro já veio do pedido de acesso, não pede de novo
        if (pr.pedido) { const pd = await env.LEADS.get("pedido:" + pr.pedido, "json"); if (pd) { lid = pr.pedido; const ik = "inv:" + pref + ":" + lid; if (!(await env.LEADS.get(ik))) await env.LEADS.put(ik, JSON.stringify({ nome: pd.nome, email: pd.email, tel: pd.tel, prospect: pref, prospectNome: pr.nome, origem: pd.origem, idioma: lang, consent: true, quando: new Date().toISOString(), pais: pd.pais || "", eventos: [] })); } }
        return new Response(null, { status: 303, headers: { location: "/investidores/?lang=" + lang, "set-cookie": SC(await sign(env, { p: pref, l: lid }), 2592000) } });
      }
      error = t.bad;
    }
    return new Response(page(lang, `<div class="gate"><h1>${t.t}</h1><p class="ix">${t.ix}</p><p>${t.sub}</p><form method="post" action="/investidores/?lang=${lang}"><label for="code">${t.code}</label><input class="code" type="text" id="code" name="code" autocomplete="off" autocapitalize="characters" required placeholder="XXXX-XXXX">${error ? `<div class="err" role="alert">${error}</div>` : ""}<button class="btn w" type="submit">${t.go}</button></form><div class="row"><a class="btn g" href="/investidores/solicitar?lang=${lang}${oc ? "&c=" + oc : ""}">${t.nocode}</a><a class="btn g" href="/">${t.back}</a></div></div>`), { status: error ? 401 : 200, headers: H });
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
        rec.mailCadastro = await mail(env, { from: HC_MAIL, to: s.pr.emails.join(","), cc: HC_MAIL + "," + INV_COPIA, replyTo: v.email,
          subject: `Help Cure — novo investidor cadastrado (${s.pr.nome})`,
          text: `Um investidor indicado por ${s.pr.nome} se cadastrou na área do investidor da Help Cure.\n\nNome: ${v.nome}\nE-mail: ${v.email}\nWhatsApp: ${v.tel}\nConversar no WhatsApp: https://wa.me/${v.tel.replace(/\D/g, "")}\nIdioma: ${NAMES[lang]}\nPaís de acesso: ${rec.pais}\nData: ${rec.quando}\n\nO investidor autorizou o uso destes dados pela Help Cure e por ${s.pr.nome} para contato sobre o investimento.` });
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

  // 3) documentos do investidor (apresentação, resumo executivo e planilha por segmento, PT/ES/EN), cifrados em /priv/docs
  if (path.startsWith("/investidores/docs/")) {
    const name = decodeURIComponent(path.slice("/investidores/docs/".length));
    if (!/^HelpCure_[A-Za-z0-9_]+\.(pptx|docx|xlsx)$/.test(name)) return new Response("Not found", { status: 404 });
    const r = await fetch(RAW + "/priv/docs/" + name + ".enc", { cf: { cacheTtl: 300, cacheEverything: true } });
    if (!r.ok) return new Response("Not found", { status: 404 });
    const body = await decrypt(env, await r.text());
    try { const k = "inv:" + s.p + ":" + s.l; const rec = await env.LEADS.get(k, "json"); if (rec) { rec.eventos.push({ tipo: "download", doc: name, quando: new Date().toISOString() }); await env.LEADS.put(k, JSON.stringify(rec)); } } catch (e) {}
    const ct = { pptx: "application/vnd.openxmlformats-officedocument.presentationml.presentation", docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document", xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" }[name.split(".").pop()];
    return new Response(body, { headers: { "content-type": ct, "content-disposition": `attachment; filename="${name}"`, "cache-control": "private, no-store", "x-content-type-options": "nosniff" } });
  }

  // 3b) vídeo do investidor: cifrado em blocos de 1 MiB (cada um iv + AES-GCM) em /priv/video; servido por faixas (Range), lendo só os blocos pedidos
  if (path.startsWith("/investidores/video/")) {
    const name = decodeURIComponent(path.slice("/investidores/video/".length));
    if (!/^HelpCure_[A-Za-z0-9_]+\.mp4$/.test(name)) return new Response("Not found", { status: 404 });
    const src = RAW + "/priv/video/" + name + ".enc", CH = 1048576, REC = CH + 28;
    const m = /bytes=(\d*)-(\d*)/.exec(req.headers.get("range") || "");
    let a = m && m[1] !== "" ? Number(m[1]) : 0, b = m && m[1] !== "" && m[2] !== "" ? Number(m[2]) : Infinity;
    const ia = Math.floor(a / CH), ib = Math.min(Math.floor(Math.min(b, 1e15) / CH), ia + 1); // no máx. 2 blocos (2 MiB) por resposta
    const r = await fetch(src, { headers: { range: `bytes=${ia * REC}-${(ib + 1) * REC - 1}` } });
    let enc, total;
    if (r.status === 206) { enc = new Uint8Array(await r.arrayBuffer()); total = Number((r.headers.get("content-range") || "").split("/")[1]); }
    else if (r.ok) { const all = new Uint8Array(await r.arrayBuffer()); total = all.length; enc = all.slice(ia * REC, (ib + 1) * REC); }
    else if (r.status === 416) { const h = await fetch(src, { headers: { range: "bytes=0-0" } }); total = Number((h.headers.get("content-range") || "").split("/")[1]) || 0; enc = new Uint8Array(0); }
    else return new Response("Not found", { status: 404 });
    const n = total - 28 * Math.ceil(total / REC);
    if (!(a < n)) return new Response(null, { status: 416, headers: { "content-range": `bytes */${n}` } });
    b = Math.min(b, n - 1, (ib + 1) * CH - 1);
    const key = await crypto.subtle.importKey("raw", Uint8Array.from(atob(env.PRIV_KEY), (c) => c.charCodeAt(0)), { name: "AES-GCM" }, false, ["decrypt"]);
    const parts = [];
    for (let o = 0; o < enc.length; o += REC) { const rec = enc.subarray(o, Math.min(o + REC, enc.length)); parts.push(new Uint8Array(await crypto.subtle.decrypt({ name: "AES-GCM", iv: rec.subarray(0, 12) }, key, rec.subarray(12)))); }
    const plain = new Uint8Array(parts.reduce((x, y) => x + y.length, 0)); let off = 0; for (const q of parts) { plain.set(q, off); off += q.length; }
    if (a === 0) { try { const k = "inv:" + s.p + ":" + s.l; const rec = await env.LEADS.get(k, "json"); if (rec && !(rec.eventos || []).some((e) => e.tipo === "video" && e.doc === name)) { rec.eventos.push({ tipo: "video", doc: name, quando: new Date().toISOString() }); await env.LEADS.put(k, JSON.stringify(rec)); } } catch (e) {} }
    return new Response(plain.slice(a - ia * CH, b - ia * CH + 1), { status: 206, headers: { "content-type": "video/mp4", "accept-ranges": "bytes", "content-range": `bytes ${a}-${b}/${n}`, "content-length": String(b - a + 1), "cache-control": "private, no-store", "x-content-type-options": "nosniff" } });
  }

  // 4) "Quero investir"
  if (path === "/investidores/quero-investir") {
    const k = "inv:" + s.p + ":" + s.l; const rec = await env.LEADS.get(k, "json");
    if (!rec) return new Response(null, { status: 302, headers: { location: "/investidores/sair?lang=" + lang } });
    if (req.method === "POST") {
      const last = (rec.eventos || []).filter((e) => e.tipo === "quero-investir").pop();
      if (last && Date.now() - Date.parse(last.quando) < 600000) return new Response(null, { status: 303, headers: { location: "/investidores/quero-investir?lang=" + lang } }); // evita e-mails repetidos em 10 min
      const st = await mail(env, { from: HC_MAIL, to: rec.email, cc: [...s.pr.emails, HC_MAIL, INV_COPIA].join(","), replyTo: HC_MAIL, subject: t.m_subj,
        text: fill(t.m_body, { n: rec.nome, e: rec.email, t: rec.tel }) + `\n\n— Indicação: ${s.pr.nome}\nWhatsApp do investidor: https://wa.me/${String(rec.tel).replace(/\D/g, "")}` });
      rec.eventos.push({ tipo: "quero-investir", quando: new Date().toISOString(), mail: st });
      rec.queroInvestir = true; await env.LEADS.put(k, JSON.stringify(rec));
      return new Response(null, { status: 303, headers: { location: "/investidores/quero-investir?lang=" + lang } });
    }
    return new Response(page(lang, `<div class="gate"><h1>${t.obr}</h1><p>${fill(t.obs, { e: esc(rec.email) })}</p><div class="row"><a class="btn" href="/investidores/?lang=${lang}">${t.voltar}</a><a class="btn g" href="/">${t.back}</a></div></div>`), { headers: H });
  }

  // 5) conteúdo
  const order = [lang, ...["pt", "es", "en"].filter((l) => l !== lang)];
  const tabs = order.map((l, i) => `<button role="tab" aria-selected="${i === 0}" data-v="${VIDEOS[l]}">${NAMES[l]}</button>`).join("");
  return new Response(page(lang, `<h1>${t.h}</h1><p>${t.p}</p><div class="row"><a class="btn big" href="/investir.html">${t.plan}</a></div><h2 class="h2">${t.full}</h2><div class="tabs" role="tablist">${tabs}</div><div class="player" id="pl"></div><h2 class="h2">${t.mods}</h2><div class="grid">${SHORTS.map((v) => { const vl = v.id[lang] ? lang : "pt"; return `<div class="sv"><div class="f"><iframe src="https://www.youtube-nocookie.com/embed/${v.id[vl]}?rel=0&modestbranding=1" title="Help Cure — ${esc(v.n[lang])}" loading="lazy" allow="fullscreen; picture-in-picture; encrypted-media" allowfullscreen></iframe></div><b>${esc(v.n[lang])}</b><small>${t.lg[vl]}</small></div>`; }).join("")}</div>
${queroBox(lang)}
<div class="row"><a class="btn g" href="/app/">${t.app}</a><a class="btn g" href="/">${t.back}</a><a class="btn g" href="/investidores/sair?lang=${lang}">${t.out}</a></div><p class="conf">${t.conf}</p>
<script>var SOON=${JSON.stringify(t.soon)};function show(b){document.querySelectorAll('.tabs button').forEach(function(x){x.setAttribute('aria-selected',x===b)});var id=b.dataset.v,p=document.getElementById('pl');p.innerHTML=id&&id.charAt(0)=='/'?'<video controls playsinline preload="metadata" src="'+id+'" style="width:100%;height:100%;display:block;background:#06201C"></video>':id?'<iframe src="https://www.youtube-nocookie.com/embed/'+id+'?rel=0&modestbranding=1" title="Help Cure" allow="fullscreen; picture-in-picture; encrypted-media" allowfullscreen></iframe>':'<span>'+SOON+'</span>'}document.querySelectorAll('.tabs button').forEach(function(b){b.onclick=function(){show(b)}});show(document.querySelector('.tabs button'));</script>`), { headers: H });
}

// Lista de cadastros (CSV): /investidores/admin?key=ADMIN_KEY[&p=2SEA]
// Investidor sem código (marketing): pede acesso; investidores@ recebe o pedido com um link para liberar.
const RCH = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
function rnd(n) { const a = crypto.getRandomValues(new Uint8Array(n)); return Array.from(a, (x) => RCH[x % RCH.length]).join(""); }
async function solicitar(req, env, url, lang, H, oc) {
  const t = L[lang];
  let error = "", v = { nome: "", email: "", tel: "" };
  if (req.method === "POST") {
    const f = await req.formData(); const cut = (x, n) => String(f.get(x) || "").trim().slice(0, n);
    v = { nome: cut("nome", 120), email: cut("email", 160).toLowerCase(), tel: cut("tel", 40) };
    const origem = cut("c", 30).replace(/[^A-Za-z0-9_-]/g, "").toUpperCase() || "DIRETO";
    const ok = () => new Response(page(lang, `<div class="gate"><h1>${t.rok}</h1><p>${fill(t.roks, { e: esc(v.email) })}</p><div class="row"><a class="btn" href="/">${t.back}</a></div></div>`), { headers: H });
    if (cut("site", 10)) return ok(); // armadilha para robôs
    if (v.nome.length > 1 && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v.email) && v.tel.replace(/\D/g, "").length >= 8 && f.get("consent")) {
      const id = new Date().toISOString() + ":" + crypto.randomUUID().slice(0, 8);
      const rec = { ...v, origem, ref: (req.headers.get("referer") || "").slice(0, 200), idioma: lang, consent: true, quando: new Date().toISOString(), pais: (req.cf && req.cf.country) || "", status: "pendente" };
      const link = `${url.origin}/investidores/liberar?id=${encodeURIComponent(id)}&k=${await hmac(env.COOKIE_KEY, "lib:" + id)}`;
      rec.mailInterno = await mail(env, { from: HC_MAIL, to: HC_MAIL, cc: INV_COPIA, replyTo: v.email, subject: `Help Cure — pedido de acesso de investidor (${origem})`,
        text: `Novo pedido de acesso à Área do Investidor, sem código de prospect.\n\nNome: ${v.nome}\nE-mail: ${v.email}\nWhatsApp: ${v.tel}\nConversar no WhatsApp: https://wa.me/${v.tel.replace(/\D/g, "")}\nOrigem: ${origem}\nIdioma: ${NAMES[lang]}\nPaís (pelo acesso): ${rec.pais || "-"}\nData: ${rec.quando}\n\nPara liberar o acesso (gera um código exclusivo e envia ao investidor), abra:\n${link}\n\nSe não quiser liberar, basta ignorar este e-mail.` });
      rec.mailConf = await mail(env, { from: HC_MAIL, to: v.email, replyTo: HC_MAIL, subject: t.r_subj, text: fill(t.r_body, { n: v.nome, e: v.email, t: v.tel }) });
      await env.LEADS.put("pedido:" + id, JSON.stringify(rec));
      return ok();
    }
    error = t.need;
  }
  return new Response(page(lang, `<div class="gate"><h1>${t.rt}</h1><p>${t.rx}</p><form method="post" action="/investidores/solicitar?lang=${lang}"><input type="hidden" name="c" value="${esc(oc)}"><input type="text" name="site" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
<label for="nome">${t.nome}</label><input type="text" id="nome" name="nome" autocomplete="name" required value="${esc(v.nome)}">
<label for="email">${t.email}</label><input type="email" id="email" name="email" autocomplete="email" required value="${esc(v.email)}">
<label for="tel">${t.tel}</label><input type="tel" id="tel" name="tel" autocomplete="tel" required value="${esc(v.tel)}">
<label class="ck"><input type="checkbox" name="consent" value="1" required><span>${t.rconsent}</span></label>
${error ? `<div class="err" role="alert">${error}</div>` : ""}<button class="btn w" type="submit">${t.rsend}</button></form><div class="row"><a class="btn g" href="/investidores/?lang=${lang}">${t.code}</a><a class="btn g" href="/">${t.back}</a></div></div>`), { status: error ? 400 : 200, headers: H });
}
async function liberar(req, env, url) {
  const H = { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-frame-options": "DENY", "x-robots-tag": "noindex" };
  const id = url.searchParams.get("id") || "", k = url.searchParams.get("k") || "";
  if (!id || !k || !same(k, await hmac(env.COOKIE_KEY, "lib:" + id))) return new Response("Not found", { status: 404 });
  const rec = await env.LEADS.get("pedido:" + id, "json"); if (!rec) return new Response("Not found", { status: 404 });
  const P = (h) => new Response(page("pt", `<div class="gate">${h}</div>`), { headers: H });
  const dados = `<p>${esc(rec.nome)}<br>${esc(rec.email)}<br>WhatsApp: ${esc(rec.tel)}<br>Origem: ${esc(rec.origem)} · ${esc(rec.pais || "-")} · ${esc(rec.quando.slice(0, 10))}</p>`;
  if (rec.status === "liberado") return P(`<h1>Acesso já liberado</h1>${dados}<p>Código: <b>${esc(rec.codigo)}</b> (enviado em ${esc((rec.liberado || "").slice(0, 16).replace("T", " "))}).</p>`);
  if (req.method !== "POST") return P(`<h1>Liberar acesso do investidor</h1>${dados}<form method="post"><button class="btn w" type="submit">Liberar acesso e enviar o código</button></form>`);
  let pref; do { pref = "D" + rnd(4); } while (await env.LEADS.get("prospect:" + pref));
  const codigo = pref + "-" + rnd(4);
  await env.LEADS.put("prospect:" + pref, JSON.stringify({ nome: `Direto · ${rec.nome} (${rec.origem})`, codigo, emails: [HC_MAIL], ativo: true, criado: new Date().toISOString(), pedido: id }));
  const tl = L[rec.idioma] || L.pt;
  rec.status = "liberado"; rec.codigo = codigo; rec.liberado = new Date().toISOString();
  rec.mailCodigo = await mail(env, { from: HC_MAIL, to: rec.email, replyTo: HC_MAIL, subject: tl.c_subj, text: fill(tl.c_body, { n: rec.nome, c: codigo, u: `${url.origin}/investidores/?lang=${rec.idioma}` }) });
  await env.LEADS.put("pedido:" + id, JSON.stringify(rec));
  return P(`<h1>Acesso liberado</h1>${dados}<p>Código: <b>${esc(codigo)}</b><br>E-mail ao investidor: ${esc(rec.mailCodigo)}</p>`);
}

async function admin(req, env, url) {
  if (!env.ADMIN_KEY || !same(url.searchParams.get("key") || "", env.ADMIN_KEY)) return new Response("Not found", { status: 404 });
  const pref = (url.searchParams.get("p") || "").toUpperCase();
  const rows = [["data", "prospect", "nome", "email", "telefone", "idioma", "pais", "quero_investir", "email_cadastro", "email_quero", "documentos_baixados"]];
  let cur; do {
    const ls = await env.LEADS.list({ prefix: "inv:" + (pref ? pref + ":" : ""), cursor: cur }); cur = ls.list_complete ? null : ls.cursor;
    for (const k of ls.keys) { const r = await env.LEADS.get(k.name, "json"); if (!r) continue; const q = (r.eventos || []).filter((e) => e.tipo === "quero-investir");
      rows.push([r.quando, r.prospectNome || r.prospect, r.nome, r.email, r.tel, r.idioma, r.pais, q.length ? q[q.length - 1].quando : "", r.mailCadastro || "", q.length ? q[q.length - 1].mail : "", [...new Set((r.eventos || []).filter((e) => e.tipo === "download").map((e) => e.doc))].join(" | ")]); }
  } while (cur);
  const csv = "﻿" + rows.map((r) => r.map((c) => '"' + String(c).replace(/"/g, '""') + '"').join(";")).join("\r\n");
  return new Response(csv, { headers: { "content-type": "text/csv; charset=utf-8", "content-disposition": "attachment; filename=investidores_helpcure.csv", "cache-control": "no-store" } });
}

// Arquivos cifrados com PRIV_KEY2 (a partir de 03/11/2026) ou com a chave original PRIV_KEY.
async function decrypt(env, b64) {
  const raw = Uint8Array.from(atob(b64.trim()), (c) => c.charCodeAt(0));
  for (const kb of [env.PRIV_KEY2, env.PRIV_KEY]) {
    if (!kb) continue;
    try {
      const key = await crypto.subtle.importKey("raw", Uint8Array.from(atob(kb), (c) => c.charCodeAt(0)), { name: "AES-GCM" }, false, ["decrypt"]);
      return new Uint8Array(await crypto.subtle.decrypt({ name: "AES-GCM", iv: raw.slice(0, 12) }, key, raw.slice(12)));
    } catch (e) {}
  }
  throw new Error("decrypt");
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
    if (h.indexOf("wa.me/595982235441") < 0) h = h.replace(/<\/body>/i, waFab(lang) + "</body>");
    h = h.replace("<head>", '<head><meta name="robots" content="noindex,nofollow">');
    h = h.replace(/site\.css\?v=\d+/g, "site.css?v=8");
    h = h.replace(/<\/head>/i, '<style>a[href*="solidario"]{display:none!important}.eyebrow{font-size:clamp(14px,1.4vw,17px)!important;line-height:1.3!important;letter-spacing:.1em!important}h2{font-size:clamp(24px,3vw,34px)}</style></head>');
    body = new TextEncoder().encode(h);
  }
  return new Response(body, { headers: { "content-type": TYPES[ext], "cache-control": "private, no-store", "x-content-type-options": "nosniff" } });
}

// WhatsApp Cloud API (Meta) — webhook da Central de Entrada.
// GET: verificação da Meta (segredo WA_VERIFY). POST: mensagens recebidas → KV "wa:" + aviso por e-mail para contato@.
// Assinatura X-Hub-Signature-256 conferida quando o segredo WA_APP_SECRET existir.
async function whatsapp(req, env, url) {
  if (req.method === "GET") {
    if (url.searchParams.get("hub.mode") === "subscribe" && env.WA_VERIFY && same(url.searchParams.get("hub.verify_token") || "", env.WA_VERIFY))
      return new Response(url.searchParams.get("hub.challenge") || "", { headers: { "content-type": "text/plain" } });
    return new Response("Forbidden", { status: 403 });
  }
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405 });
  const body = await req.text();
  if (env.WA_APP_SECRET) {
    const k = await crypto.subtle.importKey("raw", new TextEncoder().encode(env.WA_APP_SECRET), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
    const sig = "sha256=" + [...new Uint8Array(await crypto.subtle.sign("HMAC", k, new TextEncoder().encode(body)))].map((b) => b.toString(16).padStart(2, "0")).join("");
    if (!same(req.headers.get("x-hub-signature-256") || "", sig)) return new Response("bad signature", { status: 401 });
  }
  let d; try { d = JSON.parse(body); } catch (e) { return new Response("ok"); }
  for (const en of d.entry || []) for (const ch of en.changes || []) {
    const v = ch.value || {}; const names = {}; (v.contacts || []).forEach((c) => { names[c.wa_id] = (c.profile && c.profile.name) || ""; });
    for (const m of v.messages || []) {
      const media = m.image || m.document || m.audio || m.video || m.sticker || null;
      const rec = { id: m.id, de: m.from, nome: names[m.from] || "", tipo: m.type, texto: (m.text && m.text.body) || (media && media.caption) || (m.button && m.button.text) || (m.interactive && JSON.stringify(m.interactive)) || "",
        midia: media ? { id: media.id, mime: media.mime_type || "", arquivo: media.filename || "" } : null, numero: (v.metadata && v.metadata.display_phone_number) || "", quando: new Date(Number(m.timestamp) * 1000 || Date.now()).toISOString() };
      await env.LEADS.put("wa:" + rec.quando + ":" + rec.id, JSON.stringify(rec), { metadata: { num: rec.de, nome: rec.nome.slice(0, 60), t: (rec.texto || (rec.midia ? "[anexo " + rec.tipo + "]" : "[" + rec.tipo + "]")).slice(0, 290), q: rec.quando } });
      rec.mail = await mail(env, { from: "contato@helpcure.com.py", to: "contato@helpcure.com.py", subject: `WhatsApp Help Cure — ${rec.nome || "+" + rec.de}`,
        text: `Mensagem recebida no WhatsApp da Help Cure (${rec.numero}).\n\nDe: ${rec.nome} (+${rec.de})\nTipo: ${rec.tipo}\n${rec.texto ? "Texto: " + rec.texto + "\n" : ""}${rec.midia ? "Anexo: " + (rec.midia.arquivo || rec.midia.mime) + " (id " + rec.midia.id + ")\n" : ""}Data: ${rec.quando}\n\nResponder: https://wa.me/${rec.de}` });
    }
    for (const st of v.statuses || []) { if (st.status === "failed") await env.LEADS.put("wa-erro:" + new Date().toISOString() + ":" + st.id, JSON.stringify(st)); }
  }
  return new Response("ok");
}

// Painel de atendimento do WhatsApp (Central de Entrada) — /painel
// Login por código (segredo PAINEL_KEY); sessão assinada com COOKIE_KEY.
// Lê as mensagens do KV ("wa:" recebidas, "wa-out:" enviadas, com metadata) e responde pela Cloud API (WA_TOKEN, WA_PHONE_ID).
async function painelSessao(req, env) {
  const c = cookie(req, "hc_painel"); if (!c || c.indexOf(".") < 0) return false;
  const [v, s] = c.split(".");
  if (!same(s, await hmac(env.COOKIE_KEY, "painel:" + v))) return false;
  return Number(v) > Date.now();
}
async function waLista(env) {
  const out = [];
  for (const pre of ["wa:", "wa-out:"]) {
    let cur; do {
      const ls = await env.LEADS.list({ prefix: pre, cursor: cur }); cur = ls.list_complete ? null : ls.cursor;
      for (const k of ls.keys) { const m = k.metadata || {}; out.push({ k: k.name, dir: pre === "wa:" ? "in" : "out", num: m.num || "", nome: m.nome || "", t: m.t || "", q: m.q || k.name.split(":").slice(1, 4).join(":") , st: m.st || "" }); }
    } while (cur);
  }
  return out.sort((a, b) => (a.q < b.q ? -1 : 1));
}
// ---- Help Farm: área do investidor (infra/hf-area.js) ----
// Help Farm — Área do investidor (/helpfarm/area-investidor), no mesmo modelo da área do Help Cure:
// código do prospect → cadastro do investidor → filme, vídeos explicativos e documentos cifrados → "Quero investir".
// Sem código: "Solicitar acesso" → investidores@ recebe link para liberar (gera código e envia ao investidor).
// KV LEADS com prefixos próprios: hfprospect:<PREF> = {nome, codigo, emails[], ativo}; hfinv:<PREF>:<id>; hfpedido:<id>.
// Segredos: COOKIE_KEY, HF_KEY (AES-256-GCM dos documentos em /priv/helpfarm), ADMIN_KEY; MAIL_URL/MAIL_KEY opcionais.
const HFA = "/helpfarm/area-investidor";
const HF_MAIL = "investidores@helpcure.com.py";
const HF_DOCS = [
  { f: "HelpFarm_Panorama_Mercado_Conceito_de_Valor_v3.pdf", g: "a", d: {"pt": "Mercado, conceito de valor, o motor RAPP desde 2010 e os cenários de valuation.", "es": "Mercado, concepto de valor, el motor RAPP desde 2010 y los escenarios de valuation.", "en": "Market, value concept, the RAPP engine since 2010 and valuation scenarios."}, n: { pt: "Panorama de mercado, RAPP e valuation (v3)", es: "Panorama de mercado, RAPP y valuation (v3)", en: "Market overview, RAPP and valuation (v3)" }, k: "PDF" },
  { f: "HelpFarm_Diferenciais_Competitivos_v3.pdf", g: "a", d: {"pt": "Por que a Help Farm não se copia: RAPP exclusivo no agro, unidade móvel e dispositivos.", "es": "Por qué Help Farm no se copia: RAPP exclusivo en el agro, unidad móvil y dispositivos.", "en": "Why Help Farm can't be copied: RAPP exclusive in agribusiness, mobile unit and devices."}, n: { pt: "Diferenciais competitivos e o motor RAPP (v3)", es: "Diferenciales competitivos y el motor RAPP (v3)", en: "Competitive edge and the RAPP engine (v3)" }, k: "PDF" },
  { f: "HelpFarm_Financiadores_Retorno_Valuation_v3.xlsx", g: "b", d: {"pt": "Fontes de capital, retorno do investidor, participação e valuation.", "es": "Fuentes de capital, retorno del inversionista, participación y valuation.", "en": "Funding sources, investor return, ownership and valuation."}, n: { pt: "Financiadores, retorno e valuation (v3)", es: "Financiadores, retorno y valuation (v3)", en: "Funders, returns and valuation (v3)" }, k: "Excel" },
  { f: "HelpFarm_Modelo_por_Abrangencia_v3_Rentabilidade.xlsx", g: "b", d: {"pt": "Preços, receitas por escopo (Paraguai, Brasil e mais), custos e royalty do RAPP.", "es": "Precios, ingresos por alcance (Paraguay, Brasil y más), costos y regalía de RAPP.", "en": "Pricing, revenue by scope (Paraguay, Brazil and beyond), costs and RAPP royalty."}, n: { pt: "Modelo de rentabilidade, preços e cenários (v3)", es: "Modelo de rentabilidad, precios y escenarios (v3)", en: "Profitability model, pricing and scenarios (v3)" }, k: "Excel" },
  { f: "HelpFarm_Dispositivos_RAPP.pdf", g: "c", d: {"pt": "O mapa dos dispositivos da fazenda ligados ao RAPP: o que cada um faz e como ajuda.", "es": "El mapa de los dispositivos del campo conectados a RAPP: qué hace cada uno y cómo ayuda.", "en": "The map of farm devices connected to RAPP: what each one does and how it helps."}, n: { pt: "Dispositivos Help Farm e o cérebro digital RAPP", es: "Dispositivos Help Farm y el cerebro digital RAPP", en: "Help Farm devices and the RAPP digital brain" }, k: "PDF" },
  { f: "HelpFarm_Analisador_de_Nuvens_Apresentacao.pdf", g: "c", d: {"pt": "A estação que vê a nuvem antes da chuva: origem, como funciona e ganhos para o produtor.", "es": "La estación que ve la nube antes de la lluvia: origen, cómo funciona y beneficios para el productor.", "en": "The station that sees the cloud before the rain: origin, how it works and grower benefits."}, n: { pt: "Analisador de Nuvens — apresentação", es: "Analizador de Nubes — presentación", en: "Cloud Analyser — overview" }, k: "PDF" },
  { f: "HelpFarm_Avaliador_Trabalho_Campo_Apresentacao.pdf", g: "c", d: {"pt": "Drone automático que acompanha colheita e plantio seis vezes por hora: como funciona e ganhos.", "es": "Dron automático que acompaña cosecha y siembra seis veces por hora: cómo funciona y beneficios.", "en": "Automatic drone that tracks harvest and planting six times an hour: how it works and benefits."}, n: { pt: "Avaliador de Trabalho em Campo — apresentação", es: "Evaluador de Trabajo en Campo — presentación", en: "Field Work Assessor — overview" }, k: "PDF" },
];
const HF_EXPL = [
  { k: "valor", pt: "Help Farm para investidores (2 min)", es: "Help Farm para inversionistas (2 min)", en: "Help Farm for investors (2 min)" },
  { k: "home", pt: "Como a Help Farm funciona", es: "Cómo funciona Help Farm", en: "How Help Farm works" },
  { k: "movel", pt: "Uma visita da unidade móvel", es: "Una visita de la unidad móvil", en: "A mobile-unit visit" },
  { k: "tec", pt: "O que é a assinatura de condição", es: "Qué es la firma de condición", en: "What a condition signature is" },
  { k: "cert", pt: "Do talhão ao QR code", es: "Del lote al código QR", en: "From field to QR code" },
  { k: "inv", pt: "Como a Help Farm gera receita", es: "Cómo genera ingresos Help Farm", en: "How Help Farm makes money" },
];
const HL = {
  pt: { v2: "Comece por aqui: a oportunidade em 2 minutos", k1b: "RAPP desde 2010", k1: "o motor de IA que cruza todas as medições da fazenda", k2b: "Exclusivo no agro", k2: "a licença do RAPP no agronegócio é só da Help Farm", k3b: "≈ 27% ao ano", k3: "TIR esperada para o investidor no caso base", k4b: "≈ 4,5× o capital", k4: "múltiplo esperado no cenário Paraguai + Brasil", kn: "Expectativas do modelo financeiro v3 (cenário Paraguai + Brasil), não garantia de retorno.", ga: "Comece por aqui", gb: "Números e valuation", gc: "Os dispositivos", gd: "Pesquisa de mercado e unidade móvel", t: "Área do investidor", ix: "A Área do Investidor reúne o material da rodada da Help Farm: panorama de mercado com o motor RAPP, modelo de rentabilidade e valuation, cadernos dos dispositivos, pesquisa em 16 países e os vídeos do projeto. O acesso é restrito a quem tem interesse em investir.", sub: "Digite o código de acesso que você recebeu.", code: "Código de acesso", go: "Entrar", bad: "Código inválido. Confira e tente de novo.",
    ft: "Antes de começar", fs: "Para liberar o conteúdo, informe seus dados de contato.", nome: "Nome completo", email: "E-mail", tel: "WhatsApp (com código do país e DDD)",
    consent: "Autorizo a Help Farm e quem me indicou a usar estes dados para contato sobre o investimento, conforme a LGPD (Brasil) e a Lei 6534/2020 (Paraguai).", send: "Ver o conteúdo", need: "Preencha nome, e-mail válido e WhatsApp, e marque a autorização.",
    h: "Help Farm para investidores", p: "A sua fazenda avisa antes do problema. Comece pelo vídeo de 2 minutos; depois, o filme, os documentos da rodada e os vídeos explicativos.", film: "O filme", expl: "Vídeos explicativos em desenho", soon: "em produção", docs: "Documentos", dl: "Baixar",
    back: "Voltar ao site", out: "Sair", conf: "Material confidencial. Não compartilhe o código de acesso.",
    qt: "Gostou do que viu?", qs: "Clique abaixo e a nossa equipe entra em contato pelo e-mail ou telefone que você cadastrou.", quero: "Quero investir",
    obr: "Obrigado pelo interesse!", obs: "Entraremos em contato pelo e-mail ou telefone cadastrado.", voltar: "Voltar ao conteúdo",
    nocode: "Não tenho código", rt: "Solicitar acesso", rx: "Preencha o cadastro: entraremos em contato e enviaremos o seu código de acesso ao material da Help Farm.", rconsent: "Autorizo a Help Farm a usar estes dados para contato sobre o investimento, conforme a LGPD (Brasil) e a Lei 6534/2020 (Paraguai).", rsend: "Enviar cadastro", rok: "Cadastro recebido. Muito obrigado!", roks: "Entraremos em contato e enviaremos o seu código de acesso.",
    c_subj: "Help Farm — seu código de acesso à Área do Investidor", c_body: "Olá, {n}!\n\nSeu acesso à Área do Investidor da Help Farm foi liberado.\n\nCódigo de acesso: {c}\nEntre em: {u}\n\nO material é confidencial. Por favor, não compartilhe o código.\n\nEquipe Help Farm",
    m_subj: "Help Farm — obrigado pelo seu interesse", m_body: "Olá, {n}!\n\nObrigado pelo interesse na Help Farm. Entraremos em contato pelo e-mail ou telefone cadastrado.\n\nEquipe Help Farm" },
  es: { v2: "Empiece aquí: la oportunidad en 2 minutos", k1b: "RAPP desde 2010", k1: "el motor de IA que cruza todas las mediciones del campo", k2b: "Exclusivo en el agro", k2: "la licencia de RAPP en el agronegocio es solo de Help Farm", k3b: "≈ 27% al año", k3: "TIR esperada para el inversionista en el caso base", k4b: "≈ 4,5× el capital", k4: "múltiplo esperado en el escenario Paraguay + Brasil", kn: "Expectativas del modelo financiero v3 (escenario Paraguay + Brasil), no garantía de retorno.", ga: "Empiece aquí", gb: "Números y valuation", gc: "Los dispositivos", gd: "Investigación de mercado y unidad móvil", t: "Área del inversionista", ix: "El Área del Inversionista reúne el material de la ronda de Help Farm: panorama de mercado con el motor RAPP, modelo de rentabilidad y valuation, cuadernos de los dispositivos, investigación en 16 países y los videos del proyecto. El acceso está restringido a quienes tienen interés en invertir.", sub: "Ingrese el código de acceso que recibió.", code: "Código de acceso", go: "Entrar", bad: "Código inválido. Verifique e intente de nuevo.",
    ft: "Antes de empezar", fs: "Para liberar el contenido, informe sus datos de contacto.", nome: "Nombre completo", email: "Correo electrónico", tel: "WhatsApp (con código de país)",
    consent: "Autorizo a Help Farm y a quien me recomendó a usar estos datos para contactarme sobre la inversión, conforme a la Ley 6534/2020 (Paraguay) y la LGPD (Brasil).", send: "Ver el contenido", need: "Complete nombre, correo válido y WhatsApp, y marque la autorización.",
    h: "Help Farm para inversionistas", p: "Su campo avisa antes del problema. Empiece por el video de 2 minutos; después, la película, los documentos de la ronda y los videos explicativos.", film: "La película", expl: "Videos explicativos en dibujo", soon: "en producción", docs: "Documentos", dl: "Descargar",
    back: "Volver al sitio", out: "Salir", conf: "Material confidencial. No comparta el código de acceso.",
    qt: "¿Le gustó lo que vio?", qs: "Haga clic abajo y nuestro equipo se pondrá en contacto por el correo o el teléfono que registró.", quero: "Quiero invertir",
    obr: "¡Gracias por su interés!", obs: "Nos pondremos en contacto por el correo o el teléfono registrado.", voltar: "Volver al contenido",
    nocode: "No tengo código", rt: "Solicitar acceso", rx: "Complete el registro: nos pondremos en contacto y le enviaremos su código de acceso al material de Help Farm.", rconsent: "Autorizo a Help Farm a usar estos datos para contactarme sobre la inversión, conforme a la Ley 6534/2020 (Paraguay) y la LGPD (Brasil).", rsend: "Enviar registro", rok: "Registro recibido. ¡Muchas gracias!", roks: "Nos pondremos en contacto y le enviaremos su código de acceso.",
    c_subj: "Help Farm — su código de acceso al Área del Inversionista", c_body: "Hola, {n}:\n\nSu acceso al Área del Inversionista de Help Farm fue liberado.\n\nCódigo de acceso: {c}\nIngrese en: {u}\n\nEl material es confidencial. Por favor, no comparta el código.\n\nEquipo Help Farm",
    m_subj: "Help Farm — gracias por su interés", m_body: "Hola, {n}:\n\nGracias por su interés en Help Farm. Nos pondremos en contacto por el correo o el teléfono registrado.\n\nEquipo Help Farm" },
  en: { v2: "Start here: the opportunity in 2 minutes", k1b: "RAPP since 2010", k1: "the AI engine that cross-checks every farm measurement", k2b: "Exclusive in agri", k2: "the RAPP licence in agribusiness belongs only to Help Farm", k3b: "≈ 27% a year", k3: "expected investor IRR in the base case", k4b: "≈ 4.5× capital", k4: "expected multiple in the Paraguay + Brazil scenario", kn: "Expectations from the v3 financial model (Paraguay + Brazil scenario), not a guarantee of return.", ga: "Start here", gb: "Numbers and valuation", gc: "The devices", gd: "Market research and mobile unit", t: "Investor area", ix: "The Investor Area holds the Help Farm round material: market overview with the RAPP engine, profitability and valuation model, device booklets, research across 16 countries and the project videos. Access is restricted to those interested in investing.", sub: "Enter the access code you received.", code: "Access code", go: "Enter", bad: "Invalid code. Please check and try again.",
    ft: "Before you start", fs: "To unlock the content, please enter your contact details.", nome: "Full name", email: "Email", tel: "WhatsApp (with country code)",
    consent: "I authorize Help Farm and whoever referred me to use this data to contact me about the investment, under Paraguay's Law 6534/2020 and Brazil's LGPD.", send: "See the content", need: "Enter your name, a valid email and WhatsApp, and tick the authorization.",
    h: "Help Farm for investors", p: "Your farm warns you before the problem. Start with the 2-minute video; then the film, the round documents and the explainer videos.", film: "The film", expl: "Hand-drawn explainer videos", soon: "in production", docs: "Documents", dl: "Download",
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
<style>html{background:#2E1D10}:root{--deep:#2E1D10;--card:#3A2516;--line:#5A3F28;--led:#7DB547;--ink:#F5EBDD;--ink2:#D9C6AC;--q:#A48C70}*{box-sizing:border-box}body{margin:0;min-height:100vh;background:radial-gradient(120% 80% at 80% 0%,#4A2F1B 0%,#2E1D10 60%) fixed;color:var(--ink);font:16px/1.6 Lexend,system-ui,sans-serif}
header{display:flex;align-items:center;gap:16px;max-width:1100px;margin:0 auto;padding:18px 20px}header a.logo{display:flex;align-items:center;gap:10px;font:700 20px Sora,sans-serif;color:var(--ink);text-decoration:none}header a.logo b{color:var(--led)}
nav{margin-left:auto;display:flex;gap:4px;background:rgba(255,255,255,.08);border-radius:999px;padding:3px}nav a{color:var(--ink2);text-decoration:none;font:600 12px Sora,sans-serif;padding:7px 10px;border-radius:999px}nav a[aria-current]{background:var(--led);color:#1E2A0E}
main{max-width:1100px;margin:0 auto;padding:24px 20px 64px}h1{font:700 clamp(28px,4vw,44px)/1.15 Sora,sans-serif;margin:8px 0 10px}p{margin:0;color:var(--ink2)}
.gate{max-width:470px;margin:5vh auto 0;background:var(--card);border:1px solid var(--line);border-radius:20px;padding:32px;box-shadow:0 30px 70px rgba(0,0,0,.35)}.gate h1{font-size:26px}.gate .ix{color:var(--ink);border-left:3px solid var(--led);padding-left:12px;margin:12px 0 18px}
label{display:block;font-size:14px;margin:18px 0 6px}input[type=text],input[type=email],input[type=tel]{width:100%;min-height:48px;border-radius:12px;border:1px solid var(--line);background:#24170C;color:var(--ink);font:500 17px Lexend,sans-serif;padding:0 14px}input.code{letter-spacing:.08em;text-transform:uppercase}input:focus{outline:2px solid var(--led);outline-offset:1px}
.ck{display:flex;gap:10px;align-items:flex-start;font-size:13px;color:var(--ink2);margin-top:18px}.ck input{margin-top:4px;width:18px;height:18px;accent-color:var(--led);flex:none}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 22px;border-radius:999px;border:0;background:var(--led);color:#1E2A0E;font:600 15px Sora,sans-serif;text-decoration:none;cursor:pointer}.btn.w{width:100%;margin-top:18px}.btn.g{background:transparent;color:var(--ink);border:1.5px solid var(--line)}.btn.big{min-height:58px;font-size:18px;padding:0 34px}
.err{color:#FFB4A8;font-size:14px;margin-top:10px}.row{display:flex;flex-wrap:wrap;gap:12px;margin-top:24px}
.h2{font:700 22px Sora,sans-serif;margin:40px 0 12px}.film{aspect-ratio:16/9;border-radius:18px;overflow:hidden;background:#000;box-shadow:0 30px 70px rgba(0,0,0,.45)}.film video{width:100%;height:100%;display:block}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}.feat{display:grid;grid-template-columns:1.35fr 1fr;gap:22px;align-items:center;margin-top:8px}.feat video{width:100%;aspect-ratio:16/9;border-radius:18px;display:block;background:#FBF8F1;box-shadow:0 30px 70px rgba(0,0,0,.45)}.kp{display:grid;grid-template-columns:1fr 1fr;gap:12px}.kp div{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px}.kp b{display:block;font:700 20px Sora,sans-serif;color:var(--led)}.kp span{font-size:13px;color:var(--ink2);line-height:1.4;display:block;margin-top:4px}.kn{font-size:12px;color:var(--q);margin-top:10px}.dg{font:600 13px Sora,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--led);margin:22px 0 8px}.doc small{display:block;color:var(--q);font-size:13px;margin-top:2px;line-height:1.4}.ex{background:var(--card);border:1px dashed #8A6A48;border-radius:14px;padding:16px}.ex b{display:block;font:600 15px Sora,sans-serif}.ex small{color:var(--q)}
.docs{display:grid;gap:10px}.doc{display:flex;align-items:center;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;color:var(--ink);text-decoration:none}.doc:hover{border-color:var(--led)}.doc i{font:700 11px Sora,sans-serif;font-style:normal;background:#4A2F1B;color:var(--led);padding:6px 8px;border-radius:8px}.doc span{flex:1;min-width:0}.doc em{font-style:normal;color:var(--led);font:600 14px Sora,sans-serif}
.quero{margin-top:48px;background:var(--card);border:1px solid var(--line);border-radius:20px;padding:28px}.conf{margin-top:32px;font-size:13px;color:var(--q)}@media(max-width:760px){.feat{grid-template-columns:1fr}.doc em{font-size:0}.doc em::after{content:'↓';font-size:18px}}</style></head>
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
        rec.mailInterno = await hfMail(env, { from: HF_MAIL, to: HF_MAIL, cc: "fabio.moulin@helpcure.com.py", replyTo: v.email, subject: "Help Farm — pedido de acesso de investidor", text: `Novo pedido de acesso à Área do Investidor da Help Farm.\n\nNome: ${v.nome}\nE-mail: ${v.email}\nWhatsApp: ${v.tel}\nIdioma: ${lang}\nPaís: ${rec.pais || "-"}\n\nPara liberar o acesso (gera um código e envia ao investidor), abra:\n${link}` });
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
        rec.mailCadastro = await hfMail(env, { from: HF_MAIL, to: s.pr.emails.join(","), cc: HF_MAIL + ",fabio.moulin@helpcure.com.py", replyTo: v.email, subject: `Help Farm — novo investidor cadastrado (${s.pr.nome})`, text: `Um investidor se cadastrou na área do investidor da Help Farm.\n\nNome: ${v.nome}\nE-mail: ${v.email}\nWhatsApp: ${v.tel}\nIndicação: ${s.pr.nome}\nIdioma: ${lang}\nPaís: ${rec.pais}` });
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
        const st = await hfMail(env, { from: HF_MAIL, to: rec.email, cc: [...s.pr.emails, HF_MAIL, "fabio.moulin@helpcure.com.py"].join(","), replyTo: HF_MAIL, subject: t.m_subj, text: hfFill(t.m_body, { n: rec.nome }) + `\n\n— Indicação: ${s.pr.nome}\nWhatsApp do investidor: https://wa.me/${String(rec.tel).replace(/\D/g, "")}` });
        rec.eventos.push({ tipo: "quero-investir", quando: new Date().toISOString(), mail: st }); await env.LEADS.put(ik, JSON.stringify(rec));
      }
      return go(A + "/quero-investir?lang=" + lang);
    }
    return R(`<div class="gate"><h1>${t.obr}</h1><p>${t.obs}</p><div class="row"><a class="btn" href="${A}/?lang=${lang}">${t.voltar}</a><a class="btn g" href="/helpfarm/">${t.back}</a></div></div>`);
  }

  const dl = (d) => `<a class="doc" href="${A}/docs/${encodeURIComponent(d.f)}"><i>${d.k}</i><span>${hfEsc(d.n[lang])}${d.d ? `<small>${hfEsc(d.d[lang])}</small>` : ""}</span><em>${t.dl} ↓</em></a>`;
  const docs = ["a", "b", "c"].map((g) => `<div class="dg">${t["g" + g]}</div><div class="docs">${HF_DOCS.filter((d) => d.g === g).map(dl).join("")}</div>`).join("");
  const fv = HF_EXPL[0], fvl = fv.langs && !fv.langs.includes(lang) ? fv.langs[0] : lang;
  const ex = HF_EXPL.slice(1).map((e) => { const vl = e.langs && !e.langs.includes(lang) ? e.langs[0] : lang; return `<div class="ex"><video controls playsinline preload="none" style="width:100%;aspect-ratio:16/9;border-radius:10px;display:block;margin-bottom:8px;background:#FBF8F1" poster="/helpfarm/video/expl-${e.k}-${vl}-poster.jpg" src="/helpfarm/video/expl-${e.k}-${vl}.mp4"></video><b>${hfEsc(e[lang])}</b><small>${vl.toUpperCase()}</small></div>`; }).join("");
  return R(`<h1>${t.h}</h1><p>${t.p}</p>
<h2 class="h2">${t.v2}</h2><div class="feat"><video controls playsinline preload="metadata" poster="/helpfarm/video/expl-${fv.k}-${fvl}-poster.jpg" src="/helpfarm/video/expl-${fv.k}-${fvl}.mp4"></video><div><div class="kp"><div><b>${t.k1b}</b><span>${t.k1}</span></div><div><b>${t.k2b}</b><span>${t.k2}</span></div><div><b>${t.k3b}</b><span>${t.k3}</span></div><div><b>${t.k4b}</b><span>${t.k4}</span></div></div><p class="kn">${t.kn}</p></div></div>
<h2 class="h2">${t.film}</h2><div class="film"><video controls playsinline preload="metadata" poster="/helpfarm/video/helpfarm-filme-${lang}-poster.jpg" src="/helpfarm/video/helpfarm-filme-${lang}.mp4"></video></div>
<h2 class="h2">${t.docs}</h2>${docs}
<h2 class="h2">${t.expl}</h2><div class="grid">${ex}</div>
<div class="quero"><h2 class="h2" style="margin-top:0">${t.qt}</h2><p>${t.qs}</p><form method="post" action="${A}/quero-investir?lang=${lang}" style="margin-top:18px"><button class="btn big" type="submit">${t.quero}</button></form></div>
<div class="row"><a class="btn g" href="/helpfarm/">${t.back}</a><a class="btn g" href="${A}/sair?lang=${lang}">${t.out}</a></div><p class="conf">${t.conf}</p>`);
}

// ---- Help Farm: gerencial do site (infra/hf-gerencial.js) ----
// Help Farm — Gerencial do site (/helpfarm/gerencial) e contador de visitas (/helpfarm/api/hit).
// Visitas: as páginas mandam um sinal (sendBeacon) com página, origem e se é visitante novo; o worker soma por dia
// no KV LEADS em "hfst:AAAA-MM-DD" = {v, u, nv, p:{}, c:{}, r:{}, d:{}, l:{}, play:{}}. Robôs sem JavaScript não contam.
// Acesso ao gerencial: código no segredo HF_GER; sessão assinada com COOKIE_KEY (90 dias).
const HFG = "/helpfarm/gerencial";
const HFG_PAGES = { "/helpfarm/": "Início", "/helpfarm/index.html": "Início", "/helpfarm/unidade-movel.html": "Unidade móvel", "/helpfarm/tecnologia.html": "Tecnologia", "/helpfarm/certificacao.html": "Certificação", "/helpfarm/investidores.html": "Investidores", "/helpfarm/lote-demo.html": "Lote demonstrativo", "/helpfarm/energia.html": "Energia" };
const HFG_VIDS = { "helpfarm-filme-pt": "Filme (3 min)", "expl-home-pt": "Como a Help Farm funciona", "expl-movel-pt": "Visita da unidade móvel", "expl-tec-pt": "Assinatura de condição", "expl-cert-pt": "Do talhão ao QR code", "expl-inv-pt": "Como gera receita", "expl-energia-pt": "Recalque solar sem bateria", "movel-corte": "Unidade móvel em corte" };
const HFG_CO = { BR: "Brasil", PY: "Paraguai", AR: "Argentina", UY: "Uruguai", US: "EUA", PT: "Portugal", ES: "Espanha", BO: "Bolívia", CL: "Chile", MX: "México", CO: "Colômbia", PE: "Peru", DE: "Alemanha", FR: "França", GB: "Reino Unido", CA: "Canadá", AU: "Austrália", NL: "Holanda", IT: "Itália", CN: "China", JP: "Japão" };
function hfgDay(ms) { return new Date(ms - 3 * 3600e3).toISOString().slice(0, 10); }
function hfgInc(o, k, n = 1) { if (!k) return; k = String(k).slice(0, 80); o[k] = (o[k] || 0) + n; }
async function hfgHit(req, env) {
  const ok = new Response(null, { status: 204, headers: { "cache-control": "no-store" } });
  if (req.method !== "POST") return ok;
  const ua = req.headers.get("user-agent") || "";
  if (/bot|crawl|spider|slurp|preview|headless|lighthouse|monitor/i.test(ua)) return ok;
  let b; try { b = JSON.parse(await req.text()); } catch (e) { return ok; }
  const path = String(b.p || "");
  if (!path.startsWith("/helpfarm/") || path.startsWith(HFG) || path.startsWith("/helpfarm/area-investidor")) return ok;
  const key = "hfst:" + hfgDay(Date.now());
  const st = (await env.LEADS.get(key, "json")) || { v: 0, u: 0, nv: 0, p: {}, c: {}, r: {}, d: {}, l: {}, play: {} };
  if (b.e === "play") { hfgInc(st.play, String(b.v || "").replace(/^.*\//, "").replace(/\.mp4.*$/, "")); }
  else {
    st.v++; if (b.u) st.u++; if (b.n) st.nv++;
    hfgInc(st.p, HFG_PAGES[path] || path.replace("/helpfarm/", ""));
    hfgInc(st.c, (req.cf && req.cf.country) || "??");
    let ref = "Direto"; try { if (b.r) { const h = new URL(b.r).hostname.replace(/^www\./, ""); if (!/helpcure\.com\.py$|workers\.dev$/.test(h)) ref = h; else ref = ""; } } catch (e) {}
    if (b.q) ref = "Campanha: " + String(b.q).slice(0, 40);
    hfgInc(st.r, ref);
    hfgInc(st.d, /mobi|android|iphone/i.test(ua) ? "Celular" : /ipad|tablet/i.test(ua) ? "Tablet" : "Computador");
    hfgInc(st.l, String(b.l || "pt").slice(0, 2));
  }
  await env.LEADS.put(key, JSON.stringify(st), { expirationTtl: 400 * 86400 });
  return ok;
}
async function hfgSess(req, env) {
  const c = hfCookie(req, "hf_ger"); if (!c || c.indexOf(".") < 0) return false;
  const [v, s] = c.split("."); return hfSame(s, await hfHmac(env.COOKIE_KEY, "hfger:" + v)) && Number(v) > Date.now();
}
function hfgEsc(s) { return hfEsc(s == null ? "" : s); }
function hfgTop(o, n = 8) { return Object.entries(o || {}).filter(([k]) => k).sort((a, b) => b[1] - a[1]).slice(0, n); }
function hfgBars(rows, fmt) {
  const max = Math.max(1, ...rows.map((r) => r[1]));
  return rows.length ? `<ul class="bars">${rows.map(([k, n]) => `<li><span>${hfgEsc(fmt ? fmt(k) : k)}</span><i style="--w:${Math.max(2, Math.round((n / max) * 100))}%"></i><b>${n}</b></li>`).join("")}</ul>` : `<p class="vazio">Sem dados no período.</p>`;
}
async function hfgList(env, prefix) {
  const out = []; let cur;
  do { const ls = await env.LEADS.list({ prefix, cursor: cur }); cur = ls.list_complete ? null : ls.cursor; for (const k of ls.keys) { const r = await env.LEADS.get(k.name, "json"); if (r) out.push([k.name, r]); } } while (cur);
  return out;
}
function hfgShell(body) {
  return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Gerencial — Help Farm</title>
<link rel="icon" href="/helpfarm/assets/hf-icone.svg" type="image/svg+xml">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Lexend:wght@400;500&display=swap">
<style>:root{--bg:#F7F1E7;--card:#FFFDF8;--ink:#2E1D10;--ink2:#6B5644;--line:#E6D9C4;--g:#5E9F3A;--g2:#3F7A22;--t:#B5642F}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 Lexend,system-ui,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:24px max(16px,env(safe-area-inset-left)) 48px}
header{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;margin-bottom:20px}
h1{font:700 26px Sora,sans-serif;margin:0}h1 small{display:block;font:400 14px Lexend;color:var(--ink2)}
h2{font:600 17px Sora,sans-serif;margin:0 0 12px}
.per a,.btn{display:inline-block;padding:7px 12px;border-radius:999px;border:1px solid var(--line);color:var(--ink);text-decoration:none;font-size:13px;background:var(--card)}
.per a.on{background:var(--g2);color:#fff;border-color:var(--g2)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:16px}
.k{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px 16px}.k b{display:block;font:700 28px Sora,sans-serif;color:var(--g2)}.k span{font-size:13px;color:var(--ink2)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px;min-width:0}
.bars{list-style:none;margin:0;padding:0;display:grid;gap:8px}.bars li{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,1.3fr) auto;gap:10px;align-items:center;font-size:14px}
.kv{list-style:none;margin:0;padding:0;display:grid;gap:8px}.kv li{display:flex;justify-content:space-between;gap:12px;font-size:14px}.kv b{font-variant-numeric:tabular-nums}
.bars span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.bars i{display:block;height:10px;border-radius:6px;background:linear-gradient(90deg,var(--g),var(--g2));width:var(--w)}.bars b{font-variant-numeric:tabular-nums}
.chart{overflow-x:auto}.chart svg{display:block;min-width:560px;width:100%;height:auto}
.vazio{color:var(--ink2);font-size:14px;margin:0}
table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;padding:8px 6px;border-bottom:1px solid var(--line);vertical-align:top}th{color:var(--ink2);font-weight:500}
.tbl{overflow-x:auto}.tag{display:inline-block;padding:2px 8px;border-radius:999px;background:#EAF3E2;color:var(--g2);font-size:12px}.tag.t{background:#F6E6D8;color:var(--t)}
.note{color:var(--ink2);font-size:13px;margin-top:18px}
form.login{max-width:360px;margin:12vh auto;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:24px;display:grid;gap:12px}
input{font:inherit;padding:10px 12px;border-radius:10px;border:1px solid var(--line)}button{font:600 15px Lexend;padding:11px;border:0;border-radius:10px;background:var(--g2);color:#fff;cursor:pointer}
.err{color:var(--t);font-size:14px;margin:0}</style></head><body><div class="wrap">${body}</div></body></html>`;
}
async function hfGerencial(req, env, url) {
  const H = { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-frame-options": "DENY", "x-robots-tag": "noindex" };
  const path = url.pathname.replace(/\/+$/, "") || HFG;
  if (path === HFG + "/login" && req.method === "POST") {
    const f = await req.formData();
    if (env.HF_GER && hfSame(String(f.get("codigo") || "").trim().toUpperCase(), String(env.HF_GER).toUpperCase())) {
      const v = String(Date.now() + 90 * 86400000);
      return new Response(null, { status: 303, headers: { location: HFG + "/", "set-cookie": `hf_ger=${v}.${await hfHmac(env.COOKIE_KEY, "hfger:" + v)}; Path=${HFG}; Max-Age=7776000; Secure; HttpOnly; SameSite=Strict` } });
    }
    return new Response(null, { status: 303, headers: { location: HFG + "/?erro=1" } });
  }
  if (path === HFG + "/sair") return new Response(null, { status: 303, headers: { location: HFG + "/", "set-cookie": `hf_ger=; Path=${HFG}; Max-Age=0; Secure; HttpOnly; SameSite=Strict` } });
  if (!(await hfgSess(req, env))) {
    return new Response(hfgShell(`<form class="login" method="post" action="${HFG}/login"><h1>Gerencial Help Farm<small>Acompanhamento do site</small></h1>${url.searchParams.get("erro") ? '<p class="err">Código inválido.</p>' : ""}<input name="codigo" placeholder="Código de acesso" autocomplete="off" required autofocus><button type="submit">Entrar</button></form>`), { headers: H });
  }
  const D = [7, 30, 90].includes(Number(url.searchParams.get("d"))) ? Number(url.searchParams.get("d")) : 30;
  const now = Date.now(); const days = []; for (let i = D - 1; i >= 0; i--) days.push(hfgDay(now - i * 86400e3));
  const sts = await Promise.all(days.map((d) => env.LEADS.get("hfst:" + d, "json")));
  const T = { v: 0, u: 0, nv: 0, p: {}, c: {}, r: {}, d: {}, l: {}, play: {} };
  sts.forEach((s) => { if (!s) return; T.v += s.v || 0; T.u += s.u || 0; T.nv += s.nv || 0; for (const k of ["p", "c", "r", "d", "l", "play"]) for (const [a, n] of Object.entries(s[k] || {})) hfgInc(T[k], a, n); });
  const series = sts.map((s) => [(s && s.v) || 0, (s && s.u) || 0]);
  const mx = Math.max(4, ...series.map((x) => x[0])); const W = 1000, Hh = 220, bw = W / D;
  const bars = series.map(([v, u], i) => { const h1 = (v / mx) * (Hh - 30), h2 = (u / mx) * (Hh - 30); return `<g><title>${days[i].slice(8)}/${days[i].slice(5, 7)}: ${v} visualizações, ${u} visitantes</title><rect x="${i * bw + bw * 0.12}" y="${Hh - 20 - h1}" width="${bw * 0.76}" height="${h1}" rx="3" fill="#CFE3BF"/><rect x="${i * bw + bw * 0.28}" y="${Hh - 20 - h2}" width="${bw * 0.44}" height="${h2}" rx="2" fill="#3F7A22"/></g>`; }).join("");
  const step = D <= 7 ? 1 : D <= 30 ? 5 : 15;
  const labels = days.map((d, i) => (i % step === 0 || i === D - 1 ? `<text x="${i * bw + bw / 2}" y="${Hh - 4}" font-size="12" text-anchor="middle" fill="#6B5644">${d.slice(8)}/${d.slice(5, 7)}</text>` : "")).join("");
  const svg = `<svg viewBox="0 0 ${W} ${Hh}" role="img" aria-label="Visitas por dia"><line x1="0" x2="${W}" y1="${Hh - 20}" y2="${Hh - 20}" stroke="#E6D9C4"/>${bars}${labels}<text x="4" y="14" font-size="12" fill="#6B5644">máx. ${mx}</text></svg>`;
  // área do investidor
  const [inv, ped, pro] = await Promise.all([hfgList(env, "hfinv:"), hfgList(env, "hfpedido:"), hfgList(env, "hfprospect:")]);
  const since = new Date(now - D * 86400e3).toISOString();
  const invP = inv.filter(([, r]) => (r.quando || "") >= since);
  const quer = inv.filter(([, r]) => (r.eventos || []).some((e) => e.tipo === "quero-investir")).length;
  const dl = {}; inv.forEach(([, r]) => (r.eventos || []).forEach((e) => { if (e.tipo === "download") hfgInc(dl, e.doc); }));
  const pend = ped.filter(([, r]) => r.status !== "liberado").length;
  const ultimos = inv.map(([, r]) => r).sort((a, b) => (b.quando || "").localeCompare(a.quando || "")).slice(0, 15);
  const tab = ultimos.length ? `<div class="tbl"><table><tr><th>Quando</th><th>Nome</th><th>Contato</th><th>Código</th><th>País</th><th>Ações</th></tr>${ultimos.map((r) => { const ev = r.eventos || []; const q = ev.some((e) => e.tipo === "quero-investir"); const nd = new Set(ev.filter((e) => e.tipo === "download").map((e) => e.doc)).size; return `<tr><td>${hfgEsc((r.quando || "").slice(0, 10).split("-").reverse().join("/"))}</td><td>${hfgEsc(r.nome)}</td><td>${hfgEsc(r.email)}<br>${hfgEsc(r.tel)}</td><td>${hfgEsc(r.prospectNome || r.prospect)}</td><td>${hfgEsc(r.pais)}</td><td>${q ? '<span class="tag t">quer investir</span> ' : ""}${nd ? `<span class="tag">${nd} doc.</span>` : ""}</td></tr>`; }).join("")}</table></div>` : `<p class="vazio">Nenhum investidor cadastrado ainda.</p>`;
  const per = [7, 30, 90].map((d) => `<a href="${HFG}/?d=${d}"${d === D ? ' class="on"' : ""}>${d} dias</a>`).join(" ");
  const body = `<header><h1>Gerencial Help Farm<small>Site helpcure.com.py/helpfarm · últimos ${D} dias · horário de Brasília</small></h1><nav class="per">${per} <a href="${HFG}/sair">Sair</a></nav></header>
<section class="kpis"><div class="k"><b>${T.v}</b><span>Páginas vistas</span></div><div class="k"><b>${T.u}</b><span>Visitantes (por dia)</span></div><div class="k"><b>${T.nv}</b><span>Visitantes novos</span></div><div class="k"><b>${Object.values(T.play).reduce((a, b) => a + b, 0)}</b><span>Vídeos iniciados</span></div><div class="k"><b>${invP.length}</b><span>Cadastros de investidor</span></div><div class="k"><b>${quer}</b><span>"Quero investir" (total)</span></div></section>
<div class="card" style="margin-bottom:14px"><h2>Visitas por dia</h2><div class="chart">${svg}</div><p class="vazio" style="margin-top:6px">Barra clara: páginas vistas · barra verde: visitantes.</p></div>
<div class="grid">
<div class="card"><h2>Páginas mais vistas</h2>${hfgBars(hfgTop(T.p))}</div>
<div class="card"><h2>Vídeos iniciados</h2>${hfgBars(hfgTop(T.play), (k) => HFG_VIDS[k] || k)}</div>
<div class="card"><h2>De onde vêm</h2>${hfgBars(hfgTop(T.r))}</div>
<div class="card"><h2>Países</h2>${hfgBars(hfgTop(T.c), (k) => HFG_CO[k] || k)}</div>
<div class="card"><h2>Aparelho</h2>${hfgBars(hfgTop(T.d))}</div>
<div class="card"><h2>Idioma escolhido</h2>${hfgBars(hfgTop(T.l), (k) => ({ pt: "Português", es: "Espanhol", en: "Inglês" })[k] || k)}</div>
<div class="card"><h2>Área do investidor</h2><ul class="kv"><li><span>Códigos ativos</span><b>${pro.filter(([, p]) => p.ativo).length}</b></li><li><span>Investidores cadastrados (total)</span><b>${inv.length}</b></li><li><span>Pedidos de acesso aguardando</span><b>${pend}</b></li><li><span>Pedidos de acesso (total)</span><b>${ped.length}</b></li></ul></div>
<div class="card"><h2>Documentos baixados</h2>${hfgBars(hfgTop(dl, 10), (k) => k.replace(/^HelpFarm_/, "").replace(/\.(pdf|xlsx)$/, "").replace(/_/g, " "))}</div>
</div>
<div class="card" style="margin-top:14px"><h2>Últimos investidores cadastrados</h2>${tab}</div>
<p class="note">Contagem própria do site: cada página aberta com JavaScript conta uma visualização; robôs não contam. Visitante = pessoa diferente no mesmo dia (pelo navegador). As visitas também entram no Metricool, na marca Help Cure, porque o Help Farm está no mesmo domínio.</p>`;
  return new Response(hfgShell(body), { headers: H });
}

async function painel(req, env, url) {
  const H = { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-frame-options": "DENY", "x-robots-tag": "noindex" };
  const J = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });
  const path = url.pathname.replace(/\/+$/, "") || "/painel";
  if (path === "/painel/login" && req.method === "POST") {
    const f = await req.formData();
    if (env.PAINEL_KEY && same(String(f.get("codigo") || "").trim(), env.PAINEL_KEY)) {
      const v = String(Date.now() + 30 * 86400000);
      return new Response(null, { status: 303, headers: { location: "/painel", "set-cookie": `hc_painel=${v}.${await hmac(env.COOKIE_KEY, "painel:" + v)}; Path=/painel; Max-Age=2592000; Secure; HttpOnly; SameSite=Strict` } });
    }
    return new Response(null, { status: 303, headers: { location: "/painel?erro=1" } });
  }
  if (path === "/painel/sair") return new Response(null, { status: 303, headers: { location: "/painel", "set-cookie": "hc_painel=; Path=/painel; Max-Age=0; Secure; HttpOnly; SameSite=Strict" } });
  const ok = await painelSessao(req, env);
  if (!ok) {
    if (path.startsWith("/painel/api/")) return J({ erro: "login" }, 401);
    return new Response(`<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Help Cure — Central</title><link rel="icon" href="/img/icone.svg"><style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#06201C;color:#E9F3F0;font:16px/1.5 system-ui,sans-serif}form{background:#0B2E2A;border:1px solid #1E4A44;border-radius:16px;padding:28px;width:min(360px,92vw)}h1{font-size:22px;margin:0 0 6px}p{color:#BFD3CD;margin:0 0 16px;font-size:14px}input{width:100%;box-sizing:border-box;min-height:46px;border-radius:10px;border:1px solid #2C5A53;background:#06201C;color:#E9F3F0;font-size:17px;padding:0 12px}button{width:100%;margin-top:14px;min-height:46px;border:0;border-radius:999px;background:#17B877;color:#05241C;font-weight:700;font-size:15px}.e{color:#FFB4A8;font-size:14px;margin-top:10px}</style></head><body><form method="post" action="/painel/login"><h1>Central Help Cure</h1><p>Atendimento do WhatsApp. Digite o código de acesso.</p><input type="password" name="codigo" autocomplete="current-password" required autofocus>${url.searchParams.get("erro") ? '<div class="e">Código inválido.</div>' : ""}<button type="submit">Entrar</button></form></body></html>`, { headers: H });
  }
  if (path === "/painel/api/diag") {
    const T = env.WA_TOKEN || env.wa_token; const G = "https://graph.facebook.com/v25.0/";
    const q = async (u) => { try { const r = await fetch(G + u, { headers: { authorization: "Bearer " + T } }); return await r.json(); } catch (e) { return { erro: String(e) }; } };
    const out = { tem_token: !!T, tamanho: T ? T.length : 0, phone_id: env.WA_PHONE_ID || null };
    out.me = await q("me?fields=id,name");
    out.permissoes = await q("me/permissions");
    out.numero = await q((env.WA_PHONE_ID || "x") + "?fields=id,display_phone_number,verified_name,quality_rating");
    out.waba = await q("1123012283531892?fields=id,name,currency,account_review_status");
    out.numero_teste_waba = await q("1122755736912374?fields=id,name");
    return new Response(JSON.stringify(out, null, 2), { headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
  }
  if (path === "/painel/api/conversas") {
    const all = await waLista(env); const conv = {};
    for (const m of all) { const c = conv[m.num] || (conv[m.num] = { num: m.num, nome: "", ult: "", q: "", lastIn: "", n: 0 }); if (m.dir === "in") { c.nome = m.nome || c.nome; c.lastIn = m.q; c.n++; } c.ult = (m.dir === "out" ? "Você: " : "") + m.t; c.q = m.q; }
    return J(Object.values(conv).filter((c) => c.num).sort((a, b) => (a.q < b.q ? 1 : -1)));
  }
  if (path === "/painel/api/conversa") {
    const n = (url.searchParams.get("n") || "").replace(/\D/g, "");
    const all = (await waLista(env)).filter((m) => m.num === n);
    for (const m of all) { if (m.t.length >= 290) { const v = await env.LEADS.get(m.k, "json"); if (v) m.t = v.texto || m.t; } }
    return J(all);
  }
  if (path === "/painel/api/enviar" && req.method === "POST") {
    let d; try { d = await req.json(); } catch (e) { return J({ erro: "dados" }, 400); }
    const para = String(d.para || "").replace(/\D/g, ""), texto = String(d.texto || "").trim().slice(0, 4000);
    if (!para || !texto) return J({ erro: "Escreva a mensagem." }, 400);
    if (!(env.WA_TOKEN || env.wa_token) || !env.WA_PHONE_ID) return J({ erro: "O envio ainda não está ligado (falta o token permanente do WhatsApp)." }, 503);
    const r = await fetch(`https://graph.facebook.com/v25.0/${env.WA_PHONE_ID}/messages`, { method: "POST", headers: { authorization: "Bearer " + (env.WA_TOKEN || env.wa_token), "content-type": "application/json" }, body: JSON.stringify({ messaging_product: "whatsapp", to: para, type: "text", text: { body: texto } }) });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) return J({ erro: (j.error && (j.error.error_user_msg || j.error.message)) || "Falha no envio (" + r.status + ")" }, 502);
    const id = (j.messages && j.messages[0] && j.messages[0].id) || crypto.randomUUID(), q = new Date().toISOString();
    await env.LEADS.put("wa-out:" + q + ":" + id, JSON.stringify({ id, para, texto, quando: q, por: "painel" }), { metadata: { num: para, t: texto.slice(0, 290), q, st: "enviada" } });
    return J({ ok: true });
  }
  return new Response(PAINEL_HTML, { headers: H });
}
const PAINEL_HTML = `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Central Help Cure — WhatsApp</title><link rel="icon" href="/img/icone.svg">
<style>:root{--bg:#06201C;--p:#0B2E2A;--l:#1E4A44;--ink:#E9F3F0;--mut:#9FBDB5;--led:#17B877;--in:#123B35;--out:#155E47}*{box-sizing:border-box}html,body{height:100%}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;display:flex;flex-direction:column}
header{display:flex;align-items:center;gap:12px;padding:10px 16px;border-bottom:1px solid var(--l)}header b{font-size:17px}header b i{font-style:normal;color:var(--led)}header span{color:var(--mut);font-size:13px}header a{margin-left:auto;color:var(--mut);font-size:13px}
main{flex:1;display:grid;grid-template-columns:minmax(240px,320px) 1fr;min-height:0}#lista{border-right:1px solid var(--l);overflow:auto}#lista button{all:unset;display:block;box-sizing:border-box;width:100%;padding:12px 16px;border-bottom:1px solid var(--l);cursor:pointer}#lista button[aria-current=true]{background:var(--p)}#lista button:focus-visible{outline:2px solid var(--led);outline-offset:-2px}#lista b{display:block}#lista small{display:block;color:var(--mut);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#chat{display:flex;flex-direction:column;min-height:0}#topo{padding:12px 16px;border-bottom:1px solid var(--l);display:flex;gap:10px;align-items:center}#topo button{display:none;all:unset;cursor:pointer;color:var(--led);font-weight:700}#msgs{flex:1;overflow:auto;padding:16px;display:flex;flex-direction:column;gap:8px}.m{max-width:78%;padding:8px 12px;border-radius:12px;white-space:pre-wrap;word-wrap:break-word}.m.in{background:var(--in);align-self:flex-start;border-top-left-radius:4px}.m.out{background:var(--out);align-self:flex-end;border-top-right-radius:4px}.m time{display:block;font-size:11px;color:var(--mut);margin-top:3px;text-align:right}
#aviso{padding:8px 16px;font-size:13px;color:#FFD9A0;background:#3A2D17;display:none}#form{display:flex;gap:8px;padding:10px 12px;border-top:1px solid var(--l)}#form textarea{flex:1;resize:none;min-height:44px;max-height:140px;border-radius:12px;border:1px solid #2C5A53;background:var(--bg);color:var(--ink);font:inherit;padding:10px 12px}#form button{border:0;border-radius:999px;background:var(--led);color:#05241C;font-weight:700;padding:0 18px;cursor:pointer}#form button:disabled{opacity:.5}
.vazio{margin:auto;color:var(--mut);text-align:center;padding:24px}
@media(max-width:720px){main{grid-template-columns:1fr}main.aberto #lista{display:none}main:not(.aberto) #chat{display:none}#topo button{display:inline}}</style></head><body>
<header><b>Help<i>Cure</i></b><span>Central · WhatsApp</span><a href="/painel/sair">Sair</a></header>
<main id="main"><nav id="lista" aria-label="Conversas"><div class="vazio">Carregando…</div></nav>
<section id="chat"><div id="topo"><button type="button" id="voltar" aria-label="Voltar às conversas">←</button><strong id="quem">Escolha uma conversa</strong></div><div id="msgs" aria-live="polite"><div class="vazio">As mensagens aparecem aqui.</div></div><div id="aviso"></div>
<form id="form"><textarea id="txt" rows="1" placeholder="Escreva a resposta…" aria-label="Mensagem"></textarea><button id="env" type="submit">Enviar</button></form></section></main>
<script>
var atual="",conv=[];function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function hora(q){var d=new Date(q);return isNaN(d)?"":d.toLocaleString("pt-BR",{day:"2-digit",month:"2-digit",hour:"2-digit",minute:"2-digit"})}
function fmt(n){return "+"+n}
async function j(u,o){var r=await fetch(u,o);if(r.status===401){location.href="/painel";throw 0}return r.json()}
async function lista(){conv=await j("/painel/api/conversas");var L=document.getElementById("lista");if(!conv.length){L.innerHTML='<div class="vazio">Nenhuma conversa ainda.</div>';return}
L.innerHTML=conv.map(function(c){return '<button type="button" data-n="'+c.num+'" aria-current="'+(c.num===atual)+'"><b>'+esc(c.nome||fmt(c.num))+'</b><small>'+esc(c.ult)+'</small><small>'+hora(c.q)+'</small></button>'}).join("");
L.querySelectorAll("button").forEach(function(b){b.onclick=function(){abrir(b.dataset.n)}})}
async function abrir(n){atual=n;document.getElementById("main").classList.add("aberto");var c=conv.find(function(x){return x.num===n})||{};document.getElementById("quem").textContent=(c.nome?c.nome+" · ":"")+fmt(n);
var ms=await j("/painel/api/conversa?n="+n),M=document.getElementById("msgs");M.innerHTML=ms.map(function(m){return '<div class="m '+m.dir+'">'+esc(m.t)+'<time>'+hora(m.q)+(m.dir==="out"?" · "+esc(m.st||""):"")+'</time></div>'}).join("")||'<div class="vazio">Sem mensagens.</div>';M.scrollTop=M.scrollHeight;
var ins=ms.filter(function(m){return m.dir==="in"}),ult=ins.length?new Date(ins[ins.length-1].q):null,A=document.getElementById("aviso");
if(!ult||Date.now()-ult>864e5){A.style.display="block";A.textContent="Fora da janela de 24 h: o WhatsApp só permite responder texto livre até 24 h depois da última mensagem do contato. Depois disso, é preciso um modelo aprovado."}else A.style.display="none";lista()}
document.getElementById("voltar").onclick=function(){document.getElementById("main").classList.remove("aberto")};
document.getElementById("form").onsubmit=async function(e){e.preventDefault();var t=document.getElementById("txt"),b=document.getElementById("env");if(!atual||!t.value.trim())return;b.disabled=true;
try{var r=await j("/painel/api/enviar",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({para:atual,texto:t.value})});if(r.erro){alertar(r.erro)}else{t.value="";abrir(atual)}}finally{b.disabled=false}};
function alertar(s){var A=document.getElementById("aviso");A.style.display="block";A.textContent=s}
document.getElementById("txt").addEventListener("keydown",function(e){if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();document.getElementById("form").requestSubmit()}});
lista();setInterval(function(){atual?abrir(atual):lista()},15000);
</script></body></html>`;

async function interesse(req, env) {
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405 });
  let d; try { d = await req.json(); } catch (e) { return new Response("bad", { status: 400 }); }
  const cut = (v, n) => String(v || "").trim().slice(0, n);
  const rec = { nome: cut(d.nome, 120), email: cut(d.email, 160), whatsapp: cut(d.whatsapp, 40), pais: cut(d.pais, 10), tipo: cut(d.tipo, 20), nivel: cut(d.nivel, 20), idioma: cut(d.idioma, 5), consent: d.consent === true, quando: new Date().toISOString(), cf_pais: (req.cf && req.cf.country) || "" };
  if (!rec.nome || (!rec.email && !rec.whatsapp) || !rec.consent) return new Response("bad", { status: 400 });
  const lg = ["pt", "es", "en"].includes(rec.idioma) ? rec.idioma : "pt";
  rec.mailInterno = await mail(env, { from: CAMP_MAIL, to: CAMP_MAIL, replyTo: rec.email || CAMP_MAIL,
    subject: `Help Cure Solidário — novo pré-cadastro (${rec.nome})`,
    text: `Novo pré-cadastro na campanha Help Cure Solidário.\n\nNome: ${rec.nome}\nE-mail: ${rec.email || "-"}\nWhatsApp: ${rec.whatsapp || "-"}\nPaís informado: ${rec.pais || "-"}\nTipo: ${rec.tipo || "-"}\nNível de interesse: ${rec.nivel || "-"}\nIdioma: ${NAMES[lg]}\nPaís de acesso: ${rec.cf_pais || "-"}\nData: ${rec.quando}\n\nO apoiador autorizou o uso destes dados para contato sobre a campanha.` });
  if (rec.email && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(rec.email)) {
    const m = CAMP_MSG[lg];
    rec.mailApoiador = await mail(env, { from: CAMP_MAIL, to: rec.email, replyTo: CAMP_MAIL, subject: m.s, text: m.b.replace(/\{n\}/g, rec.nome.split(" ")[0]) });
  }
  await env.LEADS.put("lead:" + rec.quando + ":" + crypto.randomUUID().slice(0, 8), JSON.stringify(rec));
  return new Response(JSON.stringify({ ok: true }), { headers: { "content-type": "application/json" } });
}

// ===== Help Cure Gestão online (03/11/2026) =====
// /gestao: app de gestão compartilhado. Login por código (segredo GESTAO_KEY), cookie hc_gestao (90 dias).
// HTML do app cifrado em /priv/gestao.html.enc no repositório (segredo GESTAO_AES, AES-GCM, iv nos 12 primeiros bytes); estado em "gestao:state" = {rev, S, quando}.
const GZ = { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-frame-options": "DENY", "x-robots-tag": "noindex" };
async function gestaoSessao(req, env) {
  const c = cookie(req, "hc_gestao"); if (!c || c.indexOf(".") < 0) return false;
  const [v, s] = c.split(".");
  if (!same(s, await hmac(env.COOKIE_KEY, "gestao:" + v))) return false;
  return Number(v) > Date.now();
}
async function gestao(req, env, url) {
  const J = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });
  const path = url.pathname.replace(/\/+$/, "") || "/gestao";
  if (path === "/gestao/login" && req.method === "POST") {
    const f = await req.formData();
    if (env.GESTAO_KEY && same(String(f.get("codigo") || "").trim(), env.GESTAO_KEY)) {
      const v = String(Date.now() + 90 * 86400000);
      return new Response(null, { status: 303, headers: { location: "/gestao", "set-cookie": `hc_gestao=${v}.${await hmac(env.COOKIE_KEY, "gestao:" + v)}; Path=/gestao; Max-Age=7776000; Secure; HttpOnly; SameSite=Strict` } });
    }
    return new Response(null, { status: 303, headers: { location: "/gestao?erro=1" } });
  }
  if (path === "/gestao/sair") return new Response(null, { status: 303, headers: { location: "/gestao", "set-cookie": "hc_gestao=; Path=/gestao; Max-Age=0; Secure; HttpOnly; SameSite=Strict" } });
  if (!(await gestaoSessao(req, env))) {
    if (path.startsWith("/gestao/api/")) return J({ erro: "login" }, 401);
    return new Response(`<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="HC Gestão"><title>Help Cure — Gestão</title><link rel="icon" href="/img/icone.svg"><link rel="apple-touch-icon" href="/img/icone.svg"><style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#06201C;color:#E9F3F0;font:16px/1.5 system-ui,sans-serif}form{background:#0B2E2A;border:1px solid #1E4A44;border-radius:16px;padding:28px;width:min(360px,92vw)}h1{font-size:22px;margin:0 0 6px}p{color:#BFD3CD;margin:0 0 16px;font-size:14px}input{width:100%;box-sizing:border-box;min-height:46px;border-radius:10px;border:1px solid #2C5A53;background:#06201C;color:#E9F3F0;font-size:17px;padding:0 12px}button{width:100%;margin-top:14px;min-height:46px;border:0;border-radius:999px;background:#17B877;color:#05241C;font-weight:700;font-size:15px}.e{color:#FFB4A8;font-size:14px;margin-top:10px}</style></head><body><form method="post" action="/gestao/login"><h1>Help Cure Gestão</h1><p>Código de acceso / Código de acesso</p><input type="password" name="codigo" autocomplete="current-password" required autofocus>${url.searchParams.get("erro") ? '<div class="e">Código inválido.</div>' : ""}<button type="submit">Entrar</button></form></body></html>`, { headers: GZ });
  }
  if (path === "/gestao/api/state") {
    if (req.method === "GET") { const st = await env.LEADS.get("gestao:state", "json"); return J(st || { rev: 0, S: null }); }
    if (req.method === "PUT") {
      let b; try { b = await req.json(); } catch (e) { return J({ erro: "json" }, 400); }
      if (!b || !b.S || !Array.isArray(b.S.tasks)) return J({ erro: "dados" }, 400);
      const cur = (await env.LEADS.get("gestao:state", "json")) || { rev: 0, S: null };
      if (Number(b.rev) !== Number(cur.rev)) return J({ erro: "conflito", ...cur }, 409);
      const nx = { rev: Number(cur.rev) + 1, S: b.S, quando: new Date().toISOString() };
      await env.LEADS.put("gestao:state", JSON.stringify(nx));
      return J({ ok: true, rev: nx.rev });
    }
    return J({ erro: "método" }, 405);
  }
  if (path === "/gestao") {
    let h = null;
    try {
      const r = await fetch(RAW + "/priv/gestao.html.enc", { cf: { cacheTtl: 60, cacheEverything: true } });
      if (r.ok) { const raw = Uint8Array.from(atob((await r.text()).trim()), (c) => c.charCodeAt(0));
        const key = await crypto.subtle.importKey("raw", Uint8Array.from(atob(env.GESTAO_AES), (c) => c.charCodeAt(0)), { name: "AES-GCM" }, false, ["decrypt"]);
        h = new TextDecoder().decode(await crypto.subtle.decrypt({ name: "AES-GCM", iv: raw.slice(0, 12) }, key, raw.slice(12))); }
    } catch (e) { h = null; }
    if (!h) return new Response("App não publicado.", { status: 503, headers: { "content-type": "text/plain; charset=utf-8" } });
    const st = (await env.LEADS.get("gestao:state", "json")) || { rev: 0, S: null };
    const boot = `<script>window.HC_ONLINE=1;window.HC_STATE=${JSON.stringify(st).replace(/</g, "\\u003c")};</script>`;
    return new Response(h.replace("<!--HC_BOOT-->", boot), { headers: GZ });
  }
  return new Response("Not found", { status: 404 });
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    let p = url.pathname;
    // Help Cure Solidário fora do ar até a análise jurídica (01/11/2026): página redireciona para o início e o formulário não grava.
    if (p === "/solidario.html" || p === "/solidario") return Response.redirect(url.origin + "/", 302);
    if (p === "/api/interesse") return new Response(JSON.stringify({ ok: false, erro: "campanha indisponível" }), { status: 410, headers: { "content-type": "application/json" } });
    if (p === "/api/whatsapp") return whatsapp(req, env, url);
    if (p === "/helpfarm/api/hit") return hfgHit(req, env);
    if (p === HFG || p.startsWith(HFG + "/")) return hfGerencial(req, env, url);
    if (p === HFA || p.startsWith(HFA + "/")) return hfArea(req, env, url, RAW);
    if (p === "/painel" || p.startsWith("/painel/")) return painel(req, env, url);
    if (p === "/gestao" || p.startsWith("/gestao/")) return gestao(req, env, url);
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
