const { chromium } = require('playwright');
const fs=require('fs');
const P=[['p1_clima',7.5],['p2_umidade',8.0],['p3_pragas',4.0],['p4_solo',11.0],['p5_gado',8.3]];
const FPS=25;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:960,height:1080}});
for(const [n,d] of P){
  const dir='/home/claude/video/i18n/'+process.argv[2]+'/anim/'+n; fs.mkdirSync(dir,{recursive:true});
  await p.goto('file:///home/claude/video/i18n/'+process.argv[2]+'/charts/'+n+'.html');
  await p.evaluate(()=>{
    const svg=document.querySelector('.card svg');svg.style.overflow='visible';const RADAR=location.href.includes('p4_solo');const NS='http://www.w3.org/2000/svg';
    const W=+svg.getAttribute('width'),H=+svg.getAttribute('height');
    const defs=document.createElementNS(NS,'defs');const cp=document.createElementNS(NS,'clipPath');cp.id='rv';
    const r=document.createElementNS(NS,'rect');r.setAttribute('x',0);r.setAttribute('y',-50);r.setAttribute('height',H+100);r.setAttribute('width',0);
    cp.appendChild(r);defs.appendChild(cp);svg.insertBefore(defs,svg.firstChild);
    const data=[];svg.querySelectorAll('path,rect,circle,polygon,polyline').forEach(e=>{if(e.closest('defs'))return;const bb=e.getBBox();if(e.tagName=='rect'&&bb.width<=20&&bb.height<=20)return;
 if(RADAR){const st=(e.getAttribute('stroke')||'')+(e.getAttribute('fill')||'');if(/8FCB5A|FFB500/i.test(st))data.push(e);}else e.setAttribute('clip-path','url(#rv)')});
 let cx=0,cy=0;if(RADAR){const bb=data[0].getBBox();cx=bb.x+bb.width/2;cy=bb.y+bb.height/2;}
    // scanning line
    const sl=document.createElementNS(NS,'line');sl.setAttribute('y1',0);sl.setAttribute('y2',H);sl.setAttribute('stroke','#8FCB5A');sl.setAttribute('stroke-opacity','.55');sl.setAttribute('stroke-width','2');svg.appendChild(sl);
    const k=document.querySelector('.kpis'),a=document.querySelector('.alert');
    window.setT=(t)=>{const e=x=>x<0?0:x>1?1:x;const s=e(t/0.7);const ease=1-Math.pow(1-s,2);
      if(RADAR){r.setAttribute('width',W);sl.setAttribute('stroke-opacity','0');data.forEach((d,i)=>{const q=e((s-i*0.25)/0.75);const qe=1-Math.pow(1-q,3);d.setAttribute('transform',`translate(${cx} ${cy}) scale(${Math.max(qe,0.001)}) translate(${-cx} ${-cy})`);d.style.opacity=q>0?1:0;});}
 else{r.setAttribute('width',W*ease);sl.setAttribute('x1',W*ease);sl.setAttribute('x2',W*ease);sl.setAttribute('stroke-opacity',s<1?'.55':'0');}
      k.style.opacity=e((t-0.25)/0.15);
      const ap=e((t-0.62)/0.1);a.style.opacity=ap;a.style.transform=`translateY(${(1-ap)*24}px)`;
      a.style.boxShadow=t>0.72?`0 0 ${18+14*Math.sin(t*40)}px rgba(255,181,0,.35)`:'none';};
  });
  const N=Math.round(d*FPS);
  for(let i=0;i<N;i++){await p.evaluate(t=>window.setT(t),i/(N-1));await p.screenshot({path:`${dir}/f${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
  console.log(n,N);
}
await b.close();})();
