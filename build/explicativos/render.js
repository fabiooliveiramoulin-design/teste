// Renderiza vídeos de quadro branco: cada cena vira um mp4 (1280x720, 30 fps) desenhado a traço com caneta.
// Uso: node render.js v1 [cenaInicial] [--still]   (durations.json: {v1:[s,...]})
const { chromium } = require("playwright");
const { spawn } = require("child_process");
const fs = require("fs");
const SC = require("./scenes");
const LANG = (process.argv.find((a) => a.startsWith("--lang=")) || "--lang=pt").slice(7);
const DUR = JSON.parse(fs.readFileSync(__dirname + (LANG === "pt" ? "/durations.json" : `/durations_${LANG}.json`)));
const LBL = require("./i18n.json").labels; const LI = { es: 0, en: 1 }[LANG];
const tr = (s) => (LI === undefined ? s : s.replace(/>([^<>]+)<\/text>/g, (m, t) => (LBL[t] ? ">" + LBL[t][LI].replace(/&/g, "&amp;") + "</text>" : m)));
const vid = process.argv[2], only = process.argv[3] !== undefined && !process.argv[3].startsWith("--") ? +process.argv[3] : null, still = process.argv.includes("--still");
const VD = LANG === "pt" ? vid : vid + "_" + LANG;
const FPS = 30, W = 1280, H = 720, LEAD = 0.35, TAIL = 0.9;
const font = "file://" + __dirname + "/node_modules/@fontsource/caveat/files/caveat-latin-700-normal.woff2";

const html = (items) => `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Hand;src:url(${font}) format("woff2");font-weight:700}
html,body{margin:0;width:${W}px;height:${H}px;overflow:hidden;background:#FBF8F1}
svg{width:${W}px;height:${H}px;display:block}
.s{fill:none;stroke:#1E1A16;stroke-width:var(--sw,5);stroke-linecap:round;stroke-linejoin:round}
.s.red{stroke:#C4512B}
text.w{font-family:Hand,cursive;font-weight:700}
</style></head><body><svg id="sv" viewBox="0 0 1600 900">
<defs><filter id="paper"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 .55 0 0 0 0 .5 0 0 0 0 .4 0 0 0 .05 0"/></filter></defs>
<rect width="1600" height="900" fill="#FBF8F1"/><rect width="1600" height="900" filter="url(#paper)"/>
<g transform="translate(1520,850)" opacity=".9"><text x="0" y="0" font-family="Hand" font-weight="700" font-size="34" fill="#3F7A22" text-anchor="end">Help Farm</text></g>
${items.map(([svgS], i) => `<g class="it" data-i="${i}">${tr(svgS)}</g>`).join("")}
<g id="pen" style="display:none"><g transform="rotate(30)"><rect x="-9" y="-150" width="18" height="120" rx="6" fill="#2B2B2B"/><rect x="-9" y="-150" width="18" height="34" rx="6" fill="#3F7A22"/><path d="M-9 -30 L9 -30 L4 -6 L-4 -6 Z" fill="#555"/><path d="M-4 -6 L4 -6 L0 2 Z" fill="#1E1A16"/>
<path d="M14 -120 C40 -118 60 -95 58 -60 C56 -40 40 -36 30 -40 L12 -46 C2 -60 2 -100 14 -120 Z" fill="#E9C9A6" stroke="#B88E6A" stroke-width="2"/></g></g>
</svg>
<script>
const W=[...document.querySelectorAll('.it')].map(g=>{const parts=[];g.querySelectorAll('.s, text.w').forEach(el=>{
  if(el.tagName==='text'){const bb=el.getBBox();const id='c'+Math.random().toString(36).slice(2);const NS='http://www.w3.org/2000/svg';
    const cp=document.createElementNS(NS,'clipPath');cp.id=id;const r=document.createElementNS(NS,'rect');r.setAttribute('x',bb.x-4);r.setAttribute('y',bb.y-10);r.setAttribute('height',bb.height+20);r.setAttribute('width',0);cp.appendChild(r);document.querySelector('defs').appendChild(cp);el.setAttribute('clip-path','url(#'+id+')');
    parts.push({el,txt:true,r,bb,len:bb.width*1.2});}
  else{const len=el.getTotalLength();el.style.strokeDasharray=len+' '+len;el.style.strokeDashoffset=len;const f=el.dataset.fill;if(f){el.style.fill=f;el.style.fillOpacity=0;}parts.push({el,len});}});
  return parts;});
const pen=document.getElementById('pen');
window.setSched=(sch)=>{window.S=sch;};
function tipOf(p,k){const el=p.el;if(p.txt){return [p.bb.x+p.bb.width*k,p.bb.y+p.bb.height*0.75];}
  const pt=el.getPointAtLength(p.len*k);const m=el.getCTM(),sv=document.getElementById('sv').getScreenCTM();const q=new DOMPoint(pt.x,pt.y).matrixTransform(m).matrixTransform(sv.inverse());return [q.x,q.y];}
window.setT=(t)=>{let tip=null;
  S.forEach((s,i)=>{const parts=W[i];const tot=parts.reduce((a,p)=>a+p.len,0)||1;const k=Math.max(0,Math.min(1,(t-s.a)/(s.b-s.a)));let acc=0;
    parts.forEach(p=>{const k0=acc/tot,k1=(acc+p.len)/tot;acc+=p.len;const kk=Math.max(0,Math.min(1,(k-k0)/((k1-k0)||1)));
      if(p.txt)p.r.setAttribute('width',(p.bb.width+8)*kk);else{p.el.style.strokeDashoffset=p.len*(1-kk);if(p.el.dataset.fill)p.el.style.fillOpacity=Math.max(0,(kk-0.85)/0.15)*0.95;}
      if(kk>0&&kk<1&&k<1)tip=tipOf(p,kk);});});
  if(tip){pen.style.display='';pen.setAttribute('transform','translate('+tip[0]+','+tip[1]+')');}else pen.style.display='none';};
</script></body></html>`;

(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: W, height: H } });
  const scenes = SC[vid];
  fs.mkdirSync(`${__dirname}/out/${VD}`, { recursive: true });
  for (let si = 0; si < scenes.length; si++) {
    if (only !== null && si !== only) continue;
    const items = scenes[si], dur = DUR[vid][si] + LEAD + TAIL;
    fs.writeFileSync(`${__dirname}/out/scene_${VD}.html`, html(items)); await pg.goto("file://" + __dirname + `/out/scene_${VD}.html`, { waitUntil: "load" });
    await pg.evaluate(() => document.fonts.ready);
    // agenda: desenha entre 0.25 s e 82% da cena, proporcional ao peso
    const tw = items.reduce((a, it) => a + it[1], 0), t0 = 0.25, t1 = Math.max(2.5, dur * 0.82);
    let acc = 0; const sch = items.map((it) => { const a = t0 + (t1 - t0) * acc / tw; acc += it[1]; return { a, b: t0 + (t1 - t0) * acc / tw }; });
    await pg.evaluate((s) => { window.setSched(s); window.reinit && window.reinit(); }, sch);
    if (still) { for (const f of [0.45, 0.85, 1.0]) { await pg.evaluate((t) => setT(t), t1 * f); await pg.screenshot({ path: `${__dirname}/out/${VD}/still_${si}_${Math.round(f * 100)}.jpg`, type: "jpeg", quality: 90 }); } continue; }
    const N = Math.round(dur * FPS), tmp = `${__dirname}/out/${VD}/s${si}.tmp.mp4`;
    const ff = spawn("ffmpeg", ["-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", String(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", String(FPS), tmp]);
    for (let f = 0; f < N; f++) {
      await pg.evaluate((t) => setT(t), f / FPS);
      const buf = await pg.screenshot({ type: "jpeg", quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
    }
    ff.stdin.end(); await new Promise((r, j) => ff.on("close", (c) => (c === 0 ? r() : j(new Error("ffmpeg " + c)))));
    fs.renameSync(tmp, `${__dirname}/out/${VD}/s${si}.mp4`); console.log(vid, si, dur.toFixed(2), N);
  }
  await b.close();
})();
