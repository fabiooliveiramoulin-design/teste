// Help Farm — Gerencial do site (/helpfarm/gerencial) e contador de visitas (/helpfarm/api/hit).
// Visitas: as páginas mandam um sinal (sendBeacon) com página, origem e se é visitante novo; o worker soma por dia
// no KV LEADS em "hfst:AAAA-MM-DD" = {v, u, nv, p:{}, c:{}, r:{}, d:{}, l:{}, play:{}}. Robôs sem JavaScript não contam.
// Acesso ao gerencial: código no segredo HF_GER; sessão assinada com COOKIE_KEY (90 dias).
const HFG = "/helpfarm/gerencial";
const HFG_PAGES = { "/helpfarm/": "Início", "/helpfarm/index.html": "Início", "/helpfarm/unidade-movel.html": "Unidade móvel", "/helpfarm/tecnologia.html": "Tecnologia", "/helpfarm/certificacao.html": "Certificação", "/helpfarm/investidores.html": "Investidores", "/helpfarm/lote-demo.html": "Lote demonstrativo" };
const HFG_VIDS = { "helpfarm-filme-pt": "Filme (3 min)", "expl-home-pt": "Como a Help Farm funciona", "expl-movel-pt": "Visita da unidade móvel", "expl-tec-pt": "Assinatura de condição", "expl-cert-pt": "Do talhão ao QR code", "expl-inv-pt": "Como gera receita", "movel-corte": "Unidade móvel em corte" };
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
