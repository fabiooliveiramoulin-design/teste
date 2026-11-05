// Gera legendas, gráficos animados, mosaico e tela final traduzidos: node build_i18n_gfx.js es|en
const { chromium } = require("playwright"); const fs = require("fs");
const L = process.argv[2], I = { es: 0, en: 1 }[L], J = require("./i18n_film.json"), V = "/home/claude/video", O = `${V}/i18n/${L}`;
fs.mkdirSync(`${O}/lt`, { recursive: true }); fs.mkdirSync(`${O}/charts`, { recursive: true });
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const [k, v] of Object.entries(J.lt)) {
    await p.setContent(`<html><body style="margin:0;background:transparent"><div style="position:absolute;left:96px;bottom:110px;display:flex;align-items:center;gap:22px;padding:22px 34px 22px 26px;border-radius:18px;background:rgba(46,29,16,.82);border:1.5px solid rgba(143,203,90,.55);font-family:Inter,Arial,sans-serif;color:#F5EBDD;font-size:40px;font-weight:600;box-shadow:0 10px 40px rgba(0,0,0,.35);max-width:1650px"><div style="width:10px;height:54px;border-radius:5px;background:linear-gradient(#8FCB5A,#C9A36B);flex:none"></div>${esc(v[I])}</div></body></html>`);
    await p.screenshot({ path: `${O}/lt/${k}.png`, omitBackground: true });
  }
  // gráficos: troca textos nos nós de texto
  for (const n of ["p1_clima", "p2_umidade", "p3_pragas", "p4_solo", "p5_gado"]) {
    await p.goto(`file://${V}/charts/${n}.html`);
    const miss = await p.evaluate((C) => { const m = []; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let x; while ((x = w.nextNode())) { const s = x.nodeValue.trim(); if (!s) continue; if (C[s]) x.nodeValue = x.nodeValue.replace(s, C[s]); else if (/[a-zà-ú]{3}/i.test(s) && !/^(Help|Farm|animal 2314|N|P|K|pH)$/.test(s)) m.push(s); } return m; }, Object.fromEntries(Object.entries(J.charts).map(([k, v]) => [k, v[I]])));
    if (miss.length) console.log("faltando", n, miss);
    const html = await p.content(); fs.writeFileSync(`${O}/charts/${n}.html`, html.replace(/(src|href)="(?!https?:|data:|file:)([^"]+)"/g, `$1="file://${V}/charts/$2"`));
  }
  // tela final
  let fin = fs.readFileSync(`${V}/frames/final.html`, "utf8"); for (const [k, v] of Object.entries(J.final)) fin = fin.replace(k, v[I]);
  fin = fin.replace('src="../img/', `src="file://${V}/img/`); fs.writeFileSync(`${O}/final.html`, fin);
  await p.goto(`file://${O}/final.html`); await p.waitForTimeout(300); await p.screenshot({ path: `${O}/14_final.jpg`, type: "jpeg", quality: 93 });
  // mosaico: 4 imagens com rótulo
  const Q = [["13a_soja_py", "Paraguai · soja"], ["13b_milho_eua", "Estados Unidos · milho"], ["13c_cafe_br", "Brasil · café"], ["13d_gado_br", "Brasil · gado"]];
  await p.setContent(`<html><body style="margin:0;width:1920px;height:1080px;display:grid;grid-template-columns:960px 960px;grid-template-rows:540px 540px;background:#2E1D10;font-family:Inter,Arial,sans-serif">${Q.map(([f, t]) => `<div style="position:relative;overflow:hidden;border:2px solid #2E1D10"><img src="file://${V}/img/${f}.jpg" style="width:100%;height:100%;object-fit:cover"><span style="position:absolute;left:28px;bottom:26px;background:rgba(46,29,16,.82);color:#F5EBDD;font-size:32px;font-weight:600;padding:8px 18px;border-radius:12px">${esc(J.mosaic[t][I])}</span></div>`).join("")}</body></html>`);
  await p.waitForTimeout(400); await p.screenshot({ path: `${O}/13_culturas.jpg`, type: "jpeg", quality: 93 });
  await b.close(); console.log("ok", L);
})();
