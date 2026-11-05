# Energia própria — caso FAPIJA/DIJA e efeito no Help Farm (estimativas, nov/2026)
import json
FX=5.40
o={}
# Produção 2024 (planilha Resumo_2024)
o["prod"]={"perenes":(1444.52,81525603.27),"temporarias":(4548.25,52377150.84),"adjacentes":(616.5,77690118.46),"total":(6609.27,211592872.57)}
o["top"]=[("Banana prata catarina",1128.81,42389749.21),("Banana Del Monte (adjacente)",309.5,40401717),("Banana Grand Nine Banesa (adjacente)",307,37288401.46),("Capim (leite e animais)",68,21520351.72),("Soja",1800,16226124.44),("Milho silagem",1612.5,15917146.84),("Pitaya",54,8613600),("Banana pacovan",100.25,5958454.38),("Milho verde",422.5,5938000),("Milho semente",268.75,5288516),("Feijão",93.75,4719749.56)]
# Cenários de consumo (kWh/ha/ano) sobre a área irrigável de 5.658 ha (estudo 2014)
A=5658
sc={"baixo":4000,"base":5300,"alto":6700}
tarifa={"dia":0.47,"desconto":0.06,"ponta":1.90}   # R$/kWh com impostos (estim.)
mix={"dia":0.50,"desconto":0.47,"ponta":0.03}
dem_kw=5400+4000; dem_rs=20.82*1.25  # R$/kW·mês com impostos (estim.)
res={}
for k,kwh in sc.items():
    E=A*kwh
    en=sum(E*mix[p]*tarifa[p] for p in mix)
    dm=dem_kw*dem_rs*12
    tot=en+dm
    res[k]=dict(mwh=round(E/1000),energia=round(en),demanda=round(dm),total=round(tot),rs_ha=round(tot/A),pct_vbp=round(tot/211592872.57*100,1))
o["conta"]=res
B=res["base"]; E=A*sc["base"]
# Alavancas (sobre o cenário base)
lev={}
en=B["energia"]; dm=B["demanda"]; mwh=E/1000
x=0.13*(en+dm); lev["Demanda contratada, reativos e motores (diagnóstico 2001: −13%)"]=x; en*=0.87; dm*=0.87; mwh*=0.87
x=0.10*en; lev["Manejo da irrigação com sensores Help Farm (energia de bombeamento −10%)"]=x; en*=0.90; mwh*=0.90
x=0.18*en*0.55; lev["Mercado livre na estação principal (Cogerh: −17% a −24%; usado 18%)"]=x; en-=x
mwh_dia=mwh*mix["dia"]; solar_mwh=mwh_dia*0.8
kwp=solar_mwh*1000/1800; capex=kwp*1000*4.5; om=capex*0.015
solar_saving=solar_mwh*1000*(tarifa["dia"]-0.07)
lev["Usina solar cobrindo 80% do consumo diurno restante"]=solar_saving-om
o["alavancas"]={k:round(v) for k,v in lev.items()}
o["solar"]=dict(mwp=round(kwp/1000,1),capex=round(capex),economia_liq=round(solar_saving-om),payback=round(capex/(solar_saving-om),1),mwh=round(solar_mwh))
tot_sav=sum(lev.values()); sem_solar=tot_sav-(solar_saving-om)
o["economia_total"]=dict(rs=round(tot_sav),pct=round(tot_sav/B["total"]*100),sem_solar=round(sem_solar),pct_sem_solar=round(sem_solar/B["total"]*100))
# Modelo de negócio Help Farm Energia para a FAPIJA
esco=0.30*sem_solar   # 30% da economia sem capex, 5 anos
ppa_desc=0.15; lcoe=0.27
ppa_margin=o["solar"]["mwh"]*1000*((tarifa["dia"]-0.07)*(1-ppa_desc)-lcoe)
o["hf_fapija"]=dict(diagnostico=150000, esco_ano=round(esco), ppa_margem_ano=round(ppa_margin), epc_margem=round(capex*0.12),
  cliente_ppa_economia=round(o["solar"]["mwh"]*1000*(tarifa["dia"]-0.07)*ppa_desc))
# Fazenda irrigada típica (500 ha de pivô)
fha=500; fk=fha*2700; fcost=fk*(0.5*0.47+0.47*0.06+0.03*1.9)+250*dem_rs*12
fs=0.20*fcost
sub=(500*6+0)+(60*12)+(25*12*6)   # US$/ano: grãos faixa B + assinatura + 6 ativos
o["fazenda"]=dict(mwh=fk/1000,conta_rs=round(fcost),conta_us=round(fcost/FX),economia_us=round(fs/FX),assinatura_us=sub,esco_hf_us=round(0.3*fs/FX))
# Efeito no modelo do investidor (Ano 5, PY+BR): fazendas 320 PY + 600 BR
irr=600*0.30+320*0.10
esco_rev=irr*o["fazenda"]["esco_hf_us"]
ppa_farms=irr*0.30; ppa_rev=ppa_farms*(0.5*1800*1000*((0.47-0.07)*(1-0.15)-0.27))/FX   # 0,5 MWp por fazenda
per=2*o["hf_fapija"]["ppa_margem_ano"]/FX + 2*o["hf_fapija"]["esco_ano"]/FX
diag=irr*0.5*3000 + 2*150000/FX
o["upside"]=dict(fazendas_irrigadas=round(irr),esco=round(esco_rev),ppa=round(ppa_rev),perimetros=round(per),diagnosticos=round(diag),total=round(esco_rev+ppa_rev+per+diag))
json.dump(o,open("calc.json","w"),ensure_ascii=False,indent=1)
for k in ["conta","alavancas","solar","economia_total","hf_fapija","fazenda","upside"]: print(k,o[k])
