# 5. camada de energia do RAPP
def fu(v): return n0(v)
fn = [("Aprende a assinatura energética de cada ativo", "Garras de corrente e medidor nas bombas, pivôs, ordenha, câmaras frias e secadores. O RAPP aprende o kWh por m³ de água, por hectare irrigado, por litro de leite ou por tonelada seca, além da demanda, do fator de potência e do horário de uso."),
      ("Encontra o desperdício e corrige sem obra", "Demanda contratada acima do necessário, multa de reativos, bomba gasta, irrigação fora da janela de desconto e água aplicada sem o solo pedir. O diagnóstico do DIJA de 2001 achou 13% a 29% de economia só com isso" + r(112) + "; na Espanha, a Linkener promete até 20%" + r(82) + "."),
      ("Projeta a geração própria atividade por atividade", "Com a curva de carga medida, o RAPP separa o que compensa gerar: bombeamento diurno, ordenha e resfriamento, câmara fria, secagem. Dimensiona a usina solar (ou híbrida com diesel e bateria) para cada atividade, com o retorno calculado sobre a conta real, e não sobre uma média."),
      ("Monitora a usina e verifica a economia", "Depois de instalada, a usina vira mais um ativo do RAPP: geração esperada contra a realizada, falhas de inversor e sujeira. Todo mês, a economia é verificada pelo protocolo IPMVP (opção B, por medição isolada)" + r(94) + " e entra no relatório do produtor e do banco que financiou."),
      ("Mede a pegada de carbono por lote", "kWh, diesel e água por quilo produzido entram no certificado de origem ouro/prata/bronze. É o que varejistas e importadores pedem; o crédito de carbono em si vale pouco onde a rede já é limpa (Brasil, Paraguai)" + r(111) + ".")]
fpts = "".join(f"<div class='pt'><i>{i+1}</i><b>{a}.</b> {b}</div>" for i, (a, b) in enumerate(fn))
ge = range_chart("Custo de energia da irrigação — US$ por hectare irrigado por ano", [
 ("EUA · média do bombeamento", 153, 153, "≈ 153 (2023)", "m"),
 ("Brasil · pivô (2.700 kWh/ha)", 150, 150, "≈ 150 (estim.)", "m"),
 ("Brasil · perímetro FAPIJA (estim.)", 410, 410, "≈ 410", "e"),
 ("Argentina · olival (La Rioja)", 300, 850, "300 → 850", "m"),
 ("Paraguai · ANDE (2.700 kWh/ha)", 143, 143, "≈ 143 (estim., US$ 53/MWh)", "m"),
], (0, 0, ""), 900, "US$ por hectare irrigado por ano", f"Fontes: USDA{r(107)}, pivô{r(114)}, FAPIJA{r(111)}, La Rioja{r(32)}, ANDE{r(101)}. Choques de preço: Espanha +600% em 2022{r(108)}; EDIA (Portugal) €47 → €196/MWh{r(109)}.")
ge = ge.replace("Help Farm: </text>", "</text>")
cmp = [("Lindsay FieldNET Pivot Watch", "EUA", "Pressão e status do pivô; sem relatório de kWh", "US$ 440 com o 1º ano", "72,73"),
       ("Valley 365 + Solbras", "EUA / Brasil", "Diagnóstico de máquina; vende pivô solar e sistemas híbridos", "Não publicado; pivô solar paga em ≈ 2 anos contra diesel", "74,84,85"),
       ("Phytech (kit de bomba)", "Israel / EUA", "Pressão, vazão e liga/desliga; energia só pela conta de luz importada", "US$ 850–1.000 + US$ 200 pela integração da conta", "76"),
       ("Linkener", "Espanha", "Telemetria de consumo e potência contratada para regantes", "Mensalidade fixa (não publicada); até −20% na conta", "82"),
       ("Secure Meters Censeo", "Índia / global", "Eficiência de bombas (kWh por m³) em estações", "Não publicado", "78"),
       ("Lorentz (bombas solares)", "Alemanha", "Apps grátis, só para as próprias bombas, via Bluetooth", "Grátis", "77"),
       ("Way2 PowerHub (Auren)", "Brasil", "Medição de energia de 15 em 15 min para indústria e comércio", "Não publicado", "91,92"),
       ("Embrapii Rede Agrointeligente", "Brasil", "Pivô com gestão de energia em tempo real (em desenvolvimento)", "Modelo comercial em 2027", "93"),
       ("SolaQua / energia por assinatura", "Espanha / Brasil", "Usina sem investimento do produtor; PPA de 15–20 anos", "10–20% abaixo da tarifa", "87,89"),
       ("APEP (PG&E) / USDA REAP", "EUA", "Teste de bomba subsidiado; subsídio a solar e eficiência", "US$ 100/teste; até 50% do projeto", "79,80")]
ctab = "".join(f"<tr><td><b>{a}</b>{r(*map(int, e.split(',')))}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d, e in cmp)
ctab += "<tr class='hl'><td><b>Help Farm · RAPP Energia</b></td><td>Paraguai · Brasil · América do Sul</td><td>kWh por ativo + dado agronômico + projeto de geração + verificação da economia + pegada por lote</td><td>Medição incluída no ativo; diagnóstico, 30% da economia e US$/kWp</td></tr>"
pr = PRc
ptab = f"""<tr><td><b>Medição de energia por ativo</b><br><span class='note'>garra de corrente + alertas de demanda e reativos</span></td><td class='n' colspan='3'>incluída no preço do ativo (US$ 20 / 25 / 40 por mês)</td><td>Phytech cobra US$ 200 só para importar a conta{r(76)}</td></tr>
<tr><td><b>Diagnóstico e projeto de geração</b><br><span class='note'>60–90 dias de curva medida; taxa única por fazenda</span></td><td class='n'>{fu(pr['diag']['C'])}</td><td class='n'>{fu(pr['diag']['B'])}</td><td class='n'>{fu(pr['diag']['A'])}</td><td>APEP paga US$ 100 por teste de bomba{r(79)}; a REAP exige auditoria{r(80)}</td></tr>
<tr><td><b>Gestão com economia compartilhada</b><br><span class='note'>sem investimento do produtor; verificação IPMVP</span></td><td class='n' colspan='3'>30% da economia verificada, por 4 anos</td><td>Linkener: até −20% na conta{r(82)}; M&V custa 3–5% do projeto{r(94)}</td></tr>
<tr><td><b>…ou gestão por mensalidade</b><br><span class='note'>US$/fazenda/mês, para quem prefere valor fixo</span></td><td class='n'>{fu(pr['fixo']['C'])}</td><td class='n'>{fu(pr['fixo']['B'])}</td><td class='n'>{fu(pr['fixo']['A'])}</td><td>Linkener cobra mensalidade fixa{r(82)}</td></tr>
<tr><td><b>Originação do projeto solar</b><br><span class='note'>paga pela SPE ou pelo EPC parceiro, não pelo produtor</span></td><td class='n' colspan='3'>4% do investimento da usina</td><td>—</td></tr>
<tr><td><b>Monitoramento da usina + economia verificada</b><br><span class='note'>US$ por kWp instalado por ano</span></td><td class='n'>{pr['mv']['C']}</td><td class='n'>{pr['mv']['B']}</td><td class='n'>{pr['mv']['A']}</td><td>O&M no Brasil: ≈ R$ 100/sistema/mês, R$ 8 de software{r(90)}</td></tr>
<tr><td><b>Distrito de irrigação ou cooperativa</b><br><span class='note'>perímetro inteiro (ex.: FAPIJA)</span></td><td class='n' colspan='3'>diagnóstico ≈ US$ {fu(pr['perim_diag'])} + 30% da economia</td><td>FAPIJA: ≈ R$ 963 mil/ano sem usina{r(111)}</td></tr>"""
lab = [("Conta de energia/ano", "conta"), ("Economia sem obra (15%)", "gest"), ("Help Farm: 30% dessa economia", "hf_gest"),
       ("Usina solar (60% do consumo diurno), kWp", "kwp"), ("Investimento da usina", "capex"), ("Economia da usina/ano", "econ_solar"),
       ("Retorno da usina (anos)", "payback"), ("Help Farm: diagnóstico (uma vez)", "diag"), ("Help Farm: originação (uma vez, paga pela SPE/EPC)", "orig"),
       ("Help Farm: monitoramento da usina/ano", "mv"), ("Help Farm: média por ano (5 anos)", "hf_ano"), ("Ganho líquido do produtor/ano", "prod_liq"), ("Economia total sobre a conta", "pct_conta")]
def cell(k, v):
    if k == "payback": return str(v).replace(".", ",")
    if k == "pct_conta": return f"{v}%"
    if k == "kwp": return fu(v)
    return fu(v)
ftab = "".join(f"<tr{' class=hl' if k in ('hf_ano','prod_liq') else ''}><td>{a}</td>" + "".join(f"<td class='n'>{cell(k, F[b][k])}</td>" for b in "CBA") + "</tr>" for a, k in lab)
ftab += "<tr><td><b>Ganho do produtor ÷ o que paga à Help Farm pela energia</b></td>" + "".join(f"<td class='n'><b>{str(round(F[b]['prod_liq']/F[b]['hf_ano'],1)).replace('.',',')}×</b></td>" for b in "CBA") + "</tr>"
pay = [("Produtor irrigante, leiteiro, fruticultor", "Conta de luz e diesel: 30–50% do custo de quem irriga" + r(83,111), "Diagnóstico + 30% da economia ou mensalidade", "Sim"),
       ("Distrito de irrigação, perímetro, comunidade de regantes", "Conta do bombeamento coletivo; subsídio estadual no DIJA acaba em dez/2026" + r(111), "Contrato do perímetro (diagnóstico + 30%)", "Sim"),
       ("Cooperativa", "Coopercitrus e Sicredi já vendem e financiam solar ao associado", "Licença B2B2F com a energia incluída", "Sim (licença)"),
       ("Banco e fundo (FNE Sol, Pronaf, crédito verde)", "FNE para renováveis a 7,5% a.a." + r(104) + "; precisa provar a geração e a economia do projeto financiado", "Relatório de economia verificada por contrato", "Não (adicional)"),
       ("SPE de geração / EPC parceiro", "Usina por PPA 10–20% abaixo da tarifa" + r(87,89) + "; precisa de cliente qualificado e de curva de carga", "Originação de 4% do investimento", "Sim"),
       ("Governo e programas", "USDA REAP (até 50% do projeto, exige auditoria)" + r(80) + "; PRTR na Espanha; PM-KUSUM na Índia" + r(110), "Auditoria e verificação por projeto", "Não (adicional)"),
       ("Comprador e certificação", "Pegada por quilo exigida por varejistas e importadores", "Dentro da certificação por tonelada", "Não (adicional)")]
paytab = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in pay)
eqt = "".join(f"<tr><td><b>{p['pais']}</b></td><td>{p['faixa']}</td><td class='n'>{fu(p['receita'])}</td><td class='n'>+{fu(p['add_r'])} ({str(p['pct']).replace('.',',')}%)</td><td class='n'>{p['eq0']}</td><td class='n'><b>{p['eq1']}</b></td></tr>" for p in EN["paises"])
doc1.append(f"""<div class='sec'><h1>5. Energia: a nova camada do RAPP</h1>
<p>O RAPP aprende a assinatura de funcionamento de cada ativo. A mesma lógica vale para a energia: o motor passa a entender <b>como, quando e para quê</b> a fazenda usa energia, propõe a geração própria que dá retorno em cada atividade e depois prova a economia. São cinco funções novas:</p>
<div class='pts'>{fpts}</div>
<h2>O tamanho do problema</h2>
<p>A irrigação consome ≈ 1.900 PJ por ano no mundo{r(106)}. Nos EUA, o bombeamento custa US$ 3,3 bi por ano{r(107)}; na Espanha, a energia chega a 50% do custo do regante{r(83)}; no Brasil, a geração distribuída rural já soma 5,6 GW, 13% do total{r(96)}, e 116.758 fazendas nos EUA têm solar{r(97)}. O produtor já compra solar; o que falta é saber <b>quanto, onde e se deu certo</b>.</p></div>
<div class='sec'>{ge}
<h2>Quem já vende energia para a fazenda, e quanto cobra</h2>
<table><thead><tr><th style='width:24%'>Oferta</th><th style='width:12%'>Origem</th><th>O que faz</th><th style='width:26%'>Preço</th></tr></thead><tbody>{ctab}</tbody></table>
<div class='box'><b>A brecha:</b> as plataformas de irrigação (Lindsay, Valley, Netafim, Phytech) medem água e pressão, mas nenhuma publica medição de kWh. Os medidores de energia (Linkener, Way2, Censeo) não sabem se a lavoura precisava daquela água. Quem vende solar não mede a fazenda antes nem verifica a economia depois. A Help Farm é a única a juntar as três coisas. O concorrente mais próximo é o projeto da Embrapii, que só chega ao mercado em 2027{r(93)}.</div></div>
<div class='sec'><h2 style='margin-top:0'>Preço proposto da camada de energia (US$)</h2>
<table><thead><tr><th style='width:30%'>Item</th><th class='n'>Faixa C</th><th class='n'>Faixa B</th><th class='n'>Faixa A</th><th style='width:28%'>Referência de mercado</th></tr></thead><tbody>{ptab}</tbody></table>
<p>Regra usada: <b>a medição sozinha quase não se vende</b> (Lorentz dá de graça; Phytech cobra US$ 200 uma vez){r(76,77)}. O valor está na economia provada. Por isso a medição entra no preço do ativo e a Help Farm cobra pelo diagnóstico, por uma parte da economia verificada e pelo monitoramento da usina. A usina em si fica fora do balanço da Help Farm, numa SPE de geração com o know-how Moulin du Soleil / Sollar Machine.</p>
<h2>A conta do produtor: fazenda irrigada de 500 ha de pivô (US$, estimativa)</h2>
<table><thead><tr><th>Item</th><th class='n'>C · Paraguai (US$ 60/MWh)</th><th class='n'>B · Brasil (US$ 75/MWh)</th><th class='n'>A · EUA/Ibéria (US$ 130/MWh)</th></tr></thead><tbody>{ftab}</tbody></table>
<p class='note'>Premissas: 2.700 kWh/ha/ano{r(114)}; usina a US$ 0,70/0,75/1,10 por Wp{r(105)}, 1.600–1.700 kWh/kWp/ano, O&M de US$ 8/MWh; a usina compensa contra a tarifa diurna (US$ 60/87/140 por MWh). No Paraguai a energia é barata e a usina leva 8 anos para se pagar: lá o produto é a gestão e a troca do diesel (pivô solar contra diesel paga em ≈ 2 anos{r(84)}; Chaco: La Betty e Chortitzer já geram{r(99,100)}).</p></div>
<div class='sec'><h2 style='margin-top:0'>Quem paga a camada de energia</h2>
<table><thead><tr><th style='width:22%'>Pagador</th><th>Por que paga</th><th style='width:24%'>Como cobrar</th><th style='width:11%'>No cálculo?</th></tr></thead><tbody>{paytab}</tbody></table>
<h2>Equilíbrio por país com a energia</h2>
<p>Receita adicional média por fazenda Help Farm/mês, supondo que a camada de energia seja contratada por 15% das fazendas na faixa C, 30% na B e 35% na A, e que 20–40% delas façam usina. Margem de contribuição da camada: 65% (engenheiro de energia, garras de corrente e verificação).</p>
<table><thead><tr><th>País</th><th>Faixa</th><th class='n'>Receita/fazenda/mês (US$)</th><th class='n'>+ energia (média)</th><th class='n'>Equilíbrio sem energia</th><th class='n'>Com energia</th></tr></thead><tbody>{eqt}</tbody></table>
<div class='dark'><h3>Veredito: é um plus aceitável?</h3>
<p><b>Sim, como módulo do Help Farm, não como empresa separada.</b> (1) Usa o mesmo sensor, a mesma visita da unidade móvel e o mesmo motor. (2) Transforma o preço em economia: o produtor ganha de 4 a 5 vezes o que paga pela camada. (3) Abre pagadores novos: perímetros, SPEs de geração e bancos de crédito verde. (4) Ninguém pesquisado faz o ciclo completo.</p>
<p style='margin:0'><b>Limites:</b> a receita é menor que a do monitoramento (≈ 8% a mais no Ano 5) e depende de fazendas irrigadas ou de leite; no Paraguai, com energia barata, vale pelo diesel e pela rede fraca; obra de usina fica com a SPE/EPC; os preços não foram validados com clientes. O piloto da FAPIJA é a prova que falta.</p></div></div>""")
