# Preço indicado por pagador e país, margem, equilíbrio e adesão — Help Farm (nov/2026)
import json
# preços novos por faixa (US$)  [C, B, A]
P = {
 "fazenda":  ([50, 60, 100],   "mês", "fazenda"),
 "corte":    ([0.35, 0.45, 1.20], "mês", "cabeça"),
 "leite":    ([3.0, 4.0, 5.0], "mês", "vaca"),
 "graos":    ([4.0, 6.0, 12.0], "ano", "ha"),
 "alto":     ([25, 30, 60],    "ano", "ha"),
 "maq":      ([20, 25, 40],    "mês", "ativo"),
}
OLD = {"fazenda":[50,60,100],"corte":[0.5,0.6,1.0],"leite":[4,4.8,8],"graos":[2.5,3,5],"alto":[25,30,50],"maq":[35,42,70]}
VAR = {"fazenda":0,"corte":0.08,"leite":0.70,"graos":0.40/12,"alto":1.5/12,"maq":6}   # custo variável por mês por unidade
GW = 120  # conectividade por gateway/mês
PROF = {  # unidades por fazenda: fazenda, corte, leite, graos ha, alto ha, maq, gateways
 "Mista":[1,1000,0,2000,0,10,1], "Grãos":[1,0,0,5000,0,6,2], "Leite":[1,0,300,0,0,3,1], "Corte":[1,5000,0,0,0,3,2], "Alto valor":[1,0,0,0,200,2,1]}
MIX = {"Mista":96,"Grãos":80,"Leite":48,"Corte":80,"Alto valor":16}  # E2 Paraguai ano 5
K = ["fazenda","corte","leite","graos","alto","maq"]
def rev(prof,b,tab):
    u=PROF[prof]; return sum((tab[k][b] if isinstance(tab[k],list) else tab[k][0][b])/(12 if (P[k][1]=="ano") else 1)*u[i] for i,k in enumerate(K))
def var(prof):
    u=PROF[prof]; return sum(VAR[k]*u[i] for i,k in enumerate(K))+GW*u[6]
out={"perfil":{}}
for b,bn in enumerate("CBA"):
    for p in PROF:
        r_new=rev(p,b,{k:P[k][0] for k in K}); r_old=rev(p,b,OLD); v=var(p)
        out["perfil"].setdefault(p,{})[bn]=dict(novo=round(r_new,1),antigo=round(r_old,1),var=round(v,1))
def mix(b,tab):
    w=sum(MIX.values()); return sum(rev(p,b,tab)*MIX[p] for p in MIX)/w
vmix=sum(var(p)*MIX[p] for p in MIX)/sum(MIX.values())
out["mix"]={bn:dict(novo=round(mix(b,{k:P[k][0] for k in K}),1),antigo=round(mix(b,OLD),1),var=round(vmix,1)) for b,bn in enumerate("CBA")}
# países: faixa, estrutura fixa (US$/mês), base de fazendas (total; fonte), base-alvo comercial (estimativa)
C=[
 ("Paraguai","C",29000,291497,"CAN 2022",3490,"fazendas grandes que produzem ~61% (modelo v2)"),
 ("Argentina","C",29000,250881,"CNA 2018",None,None),
 ("Bolívia","C",29000,None,None,None,None),
 ("Brasil","B",40000,5070000,"Censo Agro 2017",None,None),
 ("Uruguai","B",29000,41918,"CGA 2024",None,None),
 ("Chile","B",29000,None,None,None,None),
 ("México","B",29000,4600000,"Censo Agropecuario 2022",None,None),
 ("Colômbia","B",29000,2700000,"CNA 2014",None,None),
 ("EUA","A",80000,1900000,"Census of Agriculture 2022",None,None),
 ("Portugal + Espanha","A",80000,261500+784141,"INE PT 2023 + INE ES 2023",None,None),
 ("França","A",80000,349600,"Agreste 2023",None,None),
 ("Austrália","A",80000,None,None,None,None),
 ("Nova Zelândia","A",80000,None,None,None,None),
]
rows=[]
TEAM={"Paraguai":18000+4150,"Argentina":20000,"Bolívia":20000,"Brasil":35000,"Uruguai":20000,"Chile":20000,"México":25000,"Colômbia":20000}
for n,b,fix,base,src,alvo,alvo_src in C:
    bi="CBA".index(b); m=mix(bi,{k:P[k][0] for k in K}); vv=vmix*(2.5 if b=="A" else 1); mg=m*(1-0.18)-vv
    fix=fix+TEAM.get(n,40000)
    be=fix/mg
    rows.append(dict(pais=n,faixa=b,fixo=fix,var=round(vv),receita=round(m),margem=round(mg),margem_pct=round(mg/m*100),equilibrio=round(be),base=base,fonte=src,adesao=(round(be/base*100,3) if base else None),alvo=alvo))
out["paises"]=rows
json.dump(out,open("calc.json","w"),ensure_ascii=False,indent=1)
print(json.dumps(out["mix"],indent=0)); 
for r in rows: print(r)
for p,v in out["perfil"].items(): print(p,v)
