# Help Farm Energia — estudo FAPIJA/DIJA e atratividade (PDF)
import json, asyncio, html as H
src = open("/home/claude/hfp/gen.py").read()
exec(src[:src.index("# ============================================================== DOC 1")])  # CSS, page, cover, range_chart, bars, r, us, n0
from playwright.async_api import async_playwright
from pypdf import PdfWriter, PdfReader
O = json.load(open("calc.json"))
def rs(v): return "R$ " + n0(v)
def mi(v): return ("R$ " + f"{v/1e6:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".") + " mi")
FX = 5.40
REFS = [
 ("Planilha FAPIJA — Resumo de produção anual 2024 (Limoeiro do Norte/CE)", "arquivo enviado pelo usuário"),
 ("FIERGETICA/COELCE/PROCEL — Diagnóstico energético do DIJA (jul/2001)", "arquivo enviado pelo usuário"),
 ("Assembleia Legislativa do Ceará — acordo do Jaguaribe-Apodi (2026)", "https://www2.al.ce.gov.br/legislativo/tramit2026/au3_26.pdf"),
 ("Diário do Nordeste — acordo resolve a questão do Jaguaribe-Apodi (20/02/2026)", "https://diariodonordeste.verdesmares.com.br/opiniao/colunistas/egidio-serpa/invasao-de-terras-elmano-resolve-questao-do-jaguaribe-apodi-1.3744338"),
 ("O Povo — tarifa de água do Jaguaribe-Apodi sobe 4,64% em 2026", "https://mais.opovo.com.br/jornal/economia/2026/01/12/tarifa-de-agua-no-perimetro-irrigado-jaguaribe-apodi-tem-reajuste-de-464-para-2026.html"),
 ("O Povo — produção do perímetro projetada em R$ 250 mi (2026)", "https://mais.opovo.com.br/jornal/economia/2026/10/19/valor-de-producao-do-perimetro-irrigado-jaguaribe-apodi-tem-rs-250-milhoes-projetados-neste-ano.html"),
 ("Redalyc — energia até 35% do custo da irrigação no Jaguaribe-Apodi (2014)", "https://www.redalyc.org/pdf/1190/119031262017.pdf"),
 ("CORE — energia 30% do custo de produção no Baixo Acaraú (CE)", "https://core.ac.uk/download/328077823.pdf"),
 ("Canal Solar — Maniçoba (BA): usina solar com BESS, energia >50% do orçamento do distrito", "https://canalsolar.com.br/en/Bahia-solar-power-plant-Bess-fruit-production/"),
 ("Diário do Nordeste — baixa qualidade da energia no Apodi ameaça o agro (out/2025)", "https://diariodonordeste.verdesmares.com.br/opiniao/colunistas/egidio-serpa/baixa-qualidade-da-energia-eletrica-no-apodi-ameaca-o-agro-cearense-1.3699266"),
 ("ANEEL/Enel CE — Resolução Homologatória 3.574/2026 (tarifas 2026/27)", "https://www.enel.com.br/content/dam/enel-br/Tarifas/2026/04-abril/Resolu%C3%A7%C3%A3o%20Homologat%C3%B3ria%203574%20(002)%20-%20Reajuste%20Tarif%C3%A1rio%20CE.pdf"),
 ("CNA — desconto de irrigante na área da Sudene (90% Grupo A)", "https://cnabrasil.org.br/publicacoes/alteracao-no-desconto-da-tarifa-de-energia-eletrica-para-irrigacao-na-area-atendida-pela-sudene"),
 ("Agência Gov — Portaria 137/2026, janela de desconto do irrigante", "https://agenciagov.ebc.com.br/noticias/202607/irrigantes-e-aquicultores-terao-mais-flexibilidade-para-acessar-desconto-na-conta-de-luz"),
 ("SciELO/RBEAA — consumo de energia em pivôs centrais", "https://scielo.br/j/rbeaa/a/Kc6B9vdSwgDMgh58nLYg8bP/abstract/?lang=en"),
 ("Confea — custo médio de usina fotovoltaica no Brasil (R$ 3,50–5,50/Wp)", "https://www.confea.org.br/midias/uploads-imce/contecc%202024/ELE/CUSTO_M%C3%89DIO_DE_UMA_USINA_FOTOVOLTAICA_NO_BRASIL__AN%C3%81LISE_E_PERSPECTIVAS.pdf"),
 ("BNB — Distrito de Maniçoba, usina de 4,6 MW pelo FNE Sol (R$ 24,9 mi)", "https://economicnewsbrasil.com.br/2022/11/02/bnb-celebra-parceria-com-distrito-de-irrigacao-de-manicoba-dim/"),
 ("Canal Solar — Lei 14.300, Fio B não compensado em 2026 (60%)", "https://canalsolar.com.br/consumidores-60-do-fio-b-2026/"),
 ("Correio da Manhã — FNE para energia renovável a 7,52% a.a. (2026/27)", "https://www.correiodamanha.com.br/economia/2026/07/amp/302403-projetos-rurais-sustentaveis-terao-juros-mais-baixos.html"),
 ("Cenário Energia — Cogerh economiza 17–24% no mercado livre", "https://cenarioenergia.com.br/2025/12/03/cogerh-economiza-r-25-milhoes-apos-migracao-para-o-mercado-livre-de-energia/"),
 ("InfoMoney — energia por assinatura: 10–20% abaixo da tarifa", "https://www.infomoney.com.br/?p=2072005"),
 ("UFU — pivô fotovoltaico conectado à rede: payback de 20 anos com desconto noturno", "https://repositorio.ufu.br/handle/123456789/22328"),
 ("Embrapa — pivôs centrais no Brasil em 2024 (33.846 pivôs, 2,2 mi ha)", "https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1167756/1/Agricultura-irrigada-por-pivos-centrais-no-Brasil-em-2024.pdf"),
 ("FAO AQUASTAT — mais de 307 mi ha equipados para irrigação", "https://www.fao.org/aquastat/en/data-analysis/irrig-water-use/conclusions"),
 ("iGrow News — energia e CO2 da irrigação no mundo (Qin et al., 2024)", "https://igrownews.com/irrigations-environmental-impact-a-study-on-energy-consumption-co2-emissions/"),
 ("USDA NASS — Irrigation and Water Management Survey 2023", "https://data-origin.nass.usda.gov/Publications/Highlights/2024/Census22_HL_Irrigation_4.pdf"),
 ("Nature Communications — emissões do bombeamento nos EUA (0,54 tCO2e/ha)", "https://link.springer.com/10.1038/s41467-024-44920-0"),
 ("iAgua — FENACORE: conta de luz dos regantes +600% (2022)", "https://www.iagua.es/noticias/fenacore/factura-electrica-regantes-se-encarece-mas-600-ultimo-ano"),
 ("ECO Sapo — EDIA/Alqueva: €47→196/MWh; 55 MWp solar", "https://eco.sapo.pt/especiais/o-coracao-hidrico-do-alentejo-que-sangra-nas-contas-publicas/"),
 ("Vanguardia — México, corte do subsídio da Tarifa 9 (2024)", "https://vanguardia.com.mx/coahuila/afectan-a-productores-de-coahuila-recibos-de-luz-de-500-mil-pesos-cfe-retira-apoyo-al-agro-GD13109294"),
 ("Angel One — PM-KUSUM: 10.203 MW e 2 mi de agricultores (nov/2025)", "https://www.angelone.in/news/government-schemes/pm-kusum-achieves-installation-of-10-203-mw-and-benefits-over-20-lakh-farmers"),
 ("RenewEconomy — bomba híbrida solar em algodão (NSW): diesel −50%", "https://reneweconomy.com.au/solar-hybrid-pump-cuts-nsw-irrigators-fuel-bill-in-half-14798/"),
 ("Bichos de Campo — olival em La Rioja: energia de US$ 300 para 850/ha", "https://bichosdecampo.com/olivicolas-el-costo-de-la-tarifa-electrica-paso-de-300-a-850-dolares-por-hectarea-por-ano/"),
 ("ABC Color — tarifa média da ANDE (Paraguai)", "https://www.abc.com.py/economia/2023/07/11/tarifa-media-nacional-de-electricidad-sin-impuestos-ronda-lo-g-373kwh/"),
 ("Portal Frutícola — INIA Chile: irrigação fotovoltaica economiza até 60%", "https://www.portalfruticola.com/noticias/2025/03/05/energia-fotovoltaica/"),
 ("Canal Solar — primeiro pivô 100% solar (Valley + Solbras)", "https://canalsolar.com.br/en/primeiro-pivo-do-mundo-acionado-exclusivamente-por-energia-solar-e-lancado-no-brasil"),
 ("La Comarca — regantes de Fayón economizam até 70% com autoconsumo", "https://www.lacomarca.net/placas-autoconsumo-regantes-fayon-cumplen-creces-hemos-ahorrado-mas-esperado/"),
 ("eixos — fator de emissão do SIN 2023 (0,0385 tCO2/MWh)", "https://eixos.com.br/brasil-tem-menor-taxa-de-emissao-de-carbono-na-geracao-eletrica-em-onze-anos/"),
 ("Low Carbon Power — Paraguai, 25 gCO2e/kWh", "https://lowcarbonpower.org/es/region/Paraguay"),
 ("Green Calculus — fator de emissão do diesel (DEFRA 2026)", "https://greencalculus.com/methodology/diesel-combustion/"),
 ("Sylvera — preços de crédito de carbono 2025–2026", "https://www.sylvera.com/blog/carbon-offset-price"),
 ("Argus — I-REC no Brasil a US$ 0,18–0,20/MWh", "https://www.argusmedia.com/en/news-and-insights/latest-market-news/2666040-i-rec-i-track-demand-soars-in-feb-alongside-supply"),
 ("GOGLA — créditos de carbono para bombas solares (AMS-I.A/I.B)", "https://gogla.org/blog/can-companies-overcome-carbon-market-hurdles-for-solar-pumps/"),
 ("ESG Today — Walmart Project Gigaton", "https://www.esgtoday.com/walmart-hits-goal-to-reduce-1-billion-tons-of-supply-chain-emissions-6-years-ahead-of-2030-target/"),
 ("ESG News — metas de escopo 3 da Tesco", "https://esgnews.com/?p=22068"),
 ("Rödl — CSRD após o Omnibus (dez/2025)", "https://www.roedl.com/en/insights/eu-reaches-agreement-on-omnibus-procedure-for-sustainability-reporting/"),
 ("Revista Cultivar — certificação Soja Baixo Carbono (Embrapa)", "https://revistacultivar.com.br/noticias/primeira-versao-das-diretrizes-tecnicas-para-certificacao-soja-baixo-carbono-e-publicada"),
 ("MDPI Foods — pegada de carbono da banana do Equador", "https://www.mdpi.com/2304-8158/11/20/3288"),
]
P = O["prod"]; C = O["conta"]; Bc = C["base"]; L = O["alavancas"]; S = O["solar"]; T = O["economia_total"]; HF = O["hf_fapija"]; F = O["fazenda"]; U = O["upside"]
d = []
d.append(f"""<div class='sec first'><h1>Resumo</h1>
<p><b>Energia é um dos maiores custos de quem irriga, e a Help Farm já mede as bombas e os pivôs.</b> Somar a geração própria e a gestão de energia ao Help Farm transforma o monitoramento em economia que o produtor vê na conta de luz. No caso da FAPIJA, a energia cortada paga o projeto inteiro.</p>
<div class='kpis'>
<div class='kpi'><b>{mi(Bc['total'])}/ano</b><span>conta de energia estimada do perímetro Jaguaribe-Apodi (cenário base; {Bc['pct_vbp']}% do valor da produção de 2024)</span></div>
<div class='kpi'><b>−{T['pct_sem_solar']}% a −{T['pct']}%</b><span>economia possível: sem investimento (eficiência, manejo, mercado livre) e com usina solar de {str(S['mwp']).replace('.',',')} MWp</span></div>
<div class='kpi'><b>{str(S['payback']).replace('.',',')} anos</b><span>retorno da usina solar ({mi(S['capex'])}), financiável pelo FNE Sol a 7,5–7,9% a.a.</span></div>
<div class='kpi'><b>US$ {n0(U['total']/1e6*10/10)}</b><span>—</span></div></div>
<h2>Por que agora</h2>
<div class='pts'>
<div class='pt'><i>1</i><b>O subsídio acaba em dezembro de 2026.</b> O acordo de 2026 faz o Estado do Ceará pagar 25% da conta da estação de bombeamento principal do DIJA só de agosto de 2025 a dezembro de 2026{r(3,4)}. Em 2027 a conta volta inteira para o distrito, que já opera com 62% de autossuficiência financeira{r(5)}.</div>
<div class='pt'><i>2</i><b>O próprio acordo cita uma usina solar.</b> A isenção da tarifa de água vale por 10 anos ou até a implantação de usina fotovoltaica ou poços{r(3)}. A porta política já está aberta.</div>
<div class='pt'><i>3</i><b>Há precedentes perto.</b> O Distrito de Maniçoba (BA) financiou 4,6 MW pelo FNE Sol (R$ 24,9 mi){r(16)}; a Cogerh (CE) economiza 17–24% por mês no mercado livre{r(19)}.</div>
<div class='pt'><i>4</i><b>O problema é mundial.</b> São mais de 307 mi ha irrigados{r(23)}. Nos EUA o bombeamento custa US$ 3,3 bi por ano (≈ US$ 150/ha){r(25)}; na Espanha a conta dos regantes subiu mais de 600% em 2022{r(27)}; em Portugal o MWh da EDIA foi de €47 para €196{r(28)}.</div></div>
<h2>Vale a pena para o Help Farm?</h2>
<p><b>Sim, como alavanca de venda e de margem, não como negócio de crédito de carbono.</b> Numa fazenda irrigada típica de 500 ha, a economia de energia (≈ US$ {n0(F['economia_us'])}/ano) paga {str(round(F['economia_us']/F['assinatura_us'],1)).replace('.',',')} vezes a assinatura Help Farm (≈ US$ {n0(F['assinatura_us'])}/ano). Para a empresa, a linha de energia (diagnóstico, parte da economia, venda de energia solar e grandes perímetros) somaria ≈ US$ {n0(U['total'])} por ano no Ano 5, cerca de 14% sobre a receita do cenário Paraguai + Brasil. Isso é suficiente para devolver o valuation aos US$ 9 mi negociados (seção 7). O carbono vale pouco no Brasil, onde a rede já é limpa: o valor está na <b>pegada medida por produto</b> para o comprador, não no crédito.</p>
<p class='note'>Todos os valores da FAPIJA são estimativas a partir de dados públicos e do diagnóstico de 2001: ainda não temos as faturas atuais. O primeiro passo é pedir 12 meses de contas da estação principal e das unidades dos pivôs. Câmbio de referência: US$ 1 = R$ 5,40.</p></div>""")
# fix KPI 4
d[0] = d[0].replace(f"<div class='kpi'><b>US$ {n0(U['total']/1e6*10/10)}</b><span>—</span></div>", f"<div class='kpi'><b>+US$ {str(round(U['total']/1e6,1)).replace('.',',')} mi/ano</b><span>receita adicional estimada do Help Farm no Ano 5 com a linha de energia (Paraguai + Brasil)</span></div>")

# 1. FAPIJA
top = "".join(f"<tr><td>{a}</td><td class='n'>{n0(b)}</td><td class='n'>{mi(c)}</td><td class='n'>{n0(c/b)}</td></tr>" for a, b, c in O["top"])
grp = "".join(f"<tr><td><b>{a}</b></td><td class='n'>{n0(P[k][0])}</td><td class='n'>{mi(P[k][1])}</td><td class='n'>{n0(P[k][1]/P[k][0])}</td></tr>" for a, k in [("Culturas perenes", "perenes"), ("Culturas temporárias", "temporarias"), ("Propriedades adjacentes (Del Monte, Banesa)", "adjacentes")])
grp += f"<tr class='hl'><td><b>Total</b></td><td class='n'>{n0(P['total'][0])}</td><td class='n'>{mi(P['total'][1])}</td><td class='n'>{n0(P['total'][1]/P['total'][0])}</td></tr>"
d.append(f"""<div class='sec'><h1>1. O caso FAPIJA</h1>
<p>A FAPIJA reúne os produtores do Perímetro Irrigado Jaguaribe-Apodi (DIJA), na Chapada do Apodi, a 15 km de Limoeiro do Norte (CE). A água sai do rio Jaguaribe por uma estação de bombeamento principal (5.400 kW de demanda contratada, tarifa azul), sobe para a chapada, corre por canais e é pressurizada nos pivôs{r(2)}.</p>
<h2>Produção de 2024{r(1)}</h2>
<table><thead><tr><th>Grupo</th><th class='n'>Área (ha)</th><th class='n'>Valor da produção</th><th class='n'>R$/ha</th></tr></thead><tbody>{grp}</tbody></table>
<table><thead><tr><th>Principais culturas</th><th class='n'>Área (ha)</th><th class='n'>Valor</th><th class='n'>R$/ha</th></tr></thead><tbody>{top}</tbody></table>
<p class='note'>A FAPIJA projeta R$ 250 mi para 2026{r(6)}. Banana é 57% do valor: cultura perene, irrigada o ano inteiro, e exportada pelas empresas adjacentes, o que torna a energia e a pegada de carbono decisivas.</p></div>
<div class='sec'><h2>O que o diagnóstico de 2001 já mostrava{r(2)}</h2>
<table><thead><tr><th>Medida</th><th class='n'>Economia na conta</th><th class='n'>Retorno</th></tr></thead><tbody>
<tr><td>Ajustar as demandas contratadas das 40 unidades</td><td class='n'>−7,4%</td><td class='n'>imediato</td></tr>
<tr><td>Capacitores (fator de potência)</td><td class='n'>−4,5%</td><td class='n'>10,5 meses</td></tr>
<tr><td>Todo o sistema elétrico (demanda, reativos, iluminação, motores)</td><td class='n'>−12,9% a −13,2%</td><td class='n'>6–7 meses</td></tr>
<tr><td>Manejo da irrigação pela necessidade da cultura</td><td class='n'>−3,5% (água −14%)</td><td class='n'>—</td></tr>
<tr><td>Elétrico + troca de pivô por irrigação localizada</td><td class='n'>−29,1% (água −41%)</td><td class='n'>—</td></tr></tbody></table>
<p>O estudo achou eficiência de aplicação de 79,5% (projeto: 87,5%), uniformidade baixa, transformadores sobrecarregados e irrigação iniciada sem medir a umidade do solo. Recomendou tensiômetros e uma comissão interna de conservação de energia. <b>É exatamente o que a Help Farm faz de forma contínua:</b> sensores de solo, vibração e corrente nas bombas, assinatura de cada pivô e alerta quando sai do normal. O diagnóstico de 2001 foi uma fotografia; o Help Farm é o filme.</p>
<h2>A situação em 2026</h2>
<ul><li><b>Subsídio de 25% na estação principal até dez/2026</b>, dentro do acordo sobre as ocupações irregulares{r(3,4)}.</li>
<li><b>Tarifa de água K2 2026:</b> R$ 42,15–115,37 por 1.000 m³ + R$ 29,50–52,99/ha/mês; reajuste de 4,64%; autossuficiência de 62%{r(5)}.</li>
<li><b>Energia pesa até 35% do custo da irrigação</b> no Jaguaribe-Apodi e 30% do custo de produção no Baixo Acaraú{r(7,8)}; em Maniçoba passa de 50% do orçamento do distrito{r(9)}.</li>
<li><b>Rede fraca:</b> um produtor perdeu mais de R$ 10 mi com quedas de tensão em 2025 e uma fazenda planejada para 2.000 ha opera 400 ha por falta de rede{r(10)}. Geração local também é segurança de abastecimento.</li></ul></div>""")

# 2. conta estimada
ct = "".join(f"<tr><td><b>{k.capitalize()}</b></td><td class='n'>{n0(v['mwh'])}</td><td class='n'>{mi(v['energia'])}</td><td class='n'>{mi(v['demanda'])}</td><td class='n'><b>{mi(v['total'])}</b></td><td class='n'>{n0(v['rs_ha'])}</td><td class='n'>{str(v['pct_vbp']).replace('.',',')}%</td></tr>" for k, v in C.items())
wf = [("Conta atual (base)", Bc["total"])]
acc = Bc["total"]; rows = ""
for k, v in L.items():
    acc -= v; rows += f"<tr><td>{k}</td><td class='n'>−{mi(v)}</td><td class='n'>{mi(acc)}</td></tr>"
d.append(f"""<div class='sec'><h1>2. Quanto a FAPIJA gasta e quanto pode economizar</h1>
<p>Sem as faturas atuais, a conta foi estimada em três cenários de consumo por hectare (bombeamento do rio à chapada + pressurização nos pivôs) sobre os 5.658 ha irrigáveis{r(7)}. Um pivô consome ≈ 2.700 kWh/ha/ano só na pressurização{r(14)}. Tarifas Enel CE 2026/27{r(11)}: fora de ponta R$ 0,37/kWh sem impostos (≈ R$ 0,47 com); janela do irrigante com 90% de desconto{r(12,13)}; demanda R$ 20,82/kW·mês. Premissa: 50% do consumo de dia, 47% na janela com desconto e 3% na ponta.</p>
<table><thead><tr><th>Cenário</th><th class='n'>Consumo (MWh/ano)</th><th class='n'>Energia</th><th class='n'>Demanda</th><th class='n'>Conta/ano</th><th class='n'>R$/ha</th><th class='n'>% do valor da produção</th></tr></thead><tbody>{ct}</tbody></table>
<h2>As quatro alavancas, em sequência (cenário base)</h2>
<table><thead><tr><th>Alavanca</th><th class='n'>Economia/ano</th><th class='n'>Conta depois</th></tr></thead><tbody><tr><td><b>Conta atual estimada</b></td><td class='n'>—</td><td class='n'>{mi(Bc['total'])}</td></tr>{rows}
<tr class='hl'><td><b>Economia total</b></td><td class='n'>−{mi(T['rs'])} ({T['pct']}%)</td><td class='n'>{mi(Bc['total']-T['rs'])}</td></tr></tbody></table>
<div class='box'><b>Leitura:</b> sem investir em usina, só com gestão de demanda, manejo e mercado livre, a economia fica em ≈ {T['pct_sem_solar']}% ({mi(T['sem_solar'])}/ano), na faixa que o diagnóstico de 2001 já previa (13–29%). A usina solar de ≈ {str(S['mwp']).replace('.',',')} MWp ({mi(S['capex'])} a R$ 4,50/Wp{r(15)}) gera ≈ {n0(S['mwh'])} MWh/ano e se paga em ≈ {str(S['payback']).replace('.',',')} anos. Com o FNE Sol (12 anos, 1 de carência, 7,5–7,9% a.a.){r(16,18)}, a parcela fica abaixo da economia desde o primeiro ano.</div>
<div class='warn'><b class='h'>Cuidados técnicos.</b> (1) A energia solar só compensa contra o consumo de dia sem desconto: contra a janela noturna com 90% de desconto o retorno passa de 20 anos{r(21)}. (2) Pela Lei 14.300, 60% do Fio B não é compensado em 2026 e o percentual sobe até 2028{r(17)}: preferir usina atrás do medidor da estação principal (autoconsumo local) ao autoconsumo remoto. (3) Bateria (BESS) para irrigar à noite só depois de medir a curva de carga com o Help Farm.</div></div>""")

# 3. mundo
g = range_chart("Custo de energia da irrigação e choques de preço", [
 ("EUA · média do bombeamento", 153, 153, "≈ US$ 153/ha (2023)", "m"),
 ("EUA · poços elétricos", 165, 165, "US$ 66,8/acre", "m"),
 ("Argentina · olival (La Rioja)", 300, 850, "US$ 300 → 850/ha", "m"),
 ("Brasil · FAPIJA (estimativa base)", Bc["rs_ha"] / FX, Bc["rs_ha"] / FX, f"≈ US$ {n0(Bc['rs_ha']/FX)}/ha", "e"),
 ("Brasil · pivô (2.700 kWh/ha)", 2700 * 0.30 / FX, 2700 * 0.30 / FX, "≈ US$ 150/ha (estim.)", "m"),
], (0, 0, ""), 900, "US$ por hectare irrigado por ano", f"Fontes: USDA{r(25)}, La Rioja{r(32)}, FAPIJA (seção 2), pivô{r(14)}.")
g = g.replace("<rect x='205.0' y='4' width='0.0'", "<rect x='205.0' y='4' width='0'").replace("Help Farm: </text>", "</text>")
wt = [("EUA", "US$ 3,3 bi/ano em bombeamento; 53 mi acres irrigados; 0,54 tCO2e/ha", "Custo e carbono", r(25, 26)),
      ("Espanha", "Conta dos regantes +600% em 2022; Fayón economizou até 70% com solar", "Choque de preço", r(27, 36)),
      ("Portugal", "EDIA (Alqueva): €47 → €196/MWh; 55 MWp solar cobrem ~60% do consumo", "Choque de preço", r(28)),
      ("México", "Corte do subsídio da Tarifa 9: contas de até MXN 550 mil por poço (2024)", "Fim de subsídio", r(29)),
      ("Índia", "PM-KUSUM: 10.203 MW, 2 mi de agricultores; retorno contra diesel < 3 anos", "Programa público", r(30)),
      ("Austrália", "Bomba híbrida solar de 500 kW em algodão: diesel −50%, retorno < 5 anos", "Diesel", r(31)),
      ("Argentina", "Energia ≈ 30% do custo do olival; US$ 850/ha/ano", "Custo", r(32)),
      ("Chile", "INIA: irrigação fotovoltaica economiza até 60%", "Pequenos irrigantes", r(34)),
      ("Paraguai", "ANDE barata (≈ US$ 53/MWh), mas rede rural fraca e muito diesel no Chaco", "Diesel e rede", r(33)),
      ("Brasil", "33.846 pivôs em 2,2 mi ha (2024); desconto de 90% só na janela noturna", "Fim de subsídio, rede fraca", r(22, 12))]
wtr = "".join(f"<tr><td><b>{a}</b></td><td>{b}{s}</td><td>{c}</td></tr>" for a, b, c, s in wt)
d.append(f"""<div class='sec'><h1>3. O problema no mundo</h1>
<p>A irrigação usa ≈ 1.900 PJ de energia e emite ≈ 216 Mt de CO2 por ano no mundo{r(24)}. Onde a energia é cara ou o subsídio acaba, ela vira 30–50% do custo de quem irriga. Onde a energia vem do diesel, o custo e o carbono são ainda maiores.</p>
{g}
<table><thead><tr><th>País</th><th>O que acontece</th><th>Gatilho de venda</th></tr></thead><tbody>{wtr}</tbody></table>
<p class='note'>Economia publicada com energia solar na irrigação: 50–70% da conta (Fayón 70%, Chile 60%, EDIA 60%, Austrália −50% de diesel){r(36,34,28,31)}. Retorno de 2 anos (pivô solar contra diesel no Brasil){r(35)} a menos de 5 anos (Austrália).</p></div>""")

# 4. modelo de negócio
mods = [("Diagnóstico energético contínuo", "Sensores de corrente e vibração em bombas e pivôs, curva de carga, demanda contratada, fator de potência e janela de desconto", "Taxa única: US$ 3 mil por fazenda; ≈ R$ 150 mil por perímetro", "Entra junto com a implantação Help Farm"),
        ("Gestão de energia (ESCO)", "Ajuste de demanda, capacitores, motores, manejo pela umidade do solo e escolha da janela de desconto (Portaria 137/2026)", "30% da economia medida, por 5 anos, sem investimento do cliente", f"FAPIJA: ≈ {mi(HF['esco_ano'])}/ano"),
        ("Mercado livre", "Migração da estação principal (Grupo A) e compra de energia", "Comissão de gestão (incluída na ESCO)", "Cogerh: −17% a −24%"),
        ("Usina solar como serviço (PPA)", "Uma SPE com know-how Moulin/Sollar constrói e opera a usina; o cliente compra a energia 15% abaixo da tarifa por 15–20 anos", "Margem entre a tarifa com desconto e o custo nivelado (≈ R$ 0,27/kWh)", f"FAPIJA: margem ≈ {mi(HF['ppa_margem_ano'])}/ano; cliente economiza {mi(HF['cliente_ppa_economia'])}/ano sem investir"),
        ("Usina vendida (EPC)", "Projeto e obra financiados pelo FNE Sol em nome do distrito", "Margem de 10–15% da obra", f"FAPIJA: ≈ {mi(HF['epc_margem'])} uma vez"),
        ("Pegada de carbono e certificado", "kWh, diesel e emissões medidos por lote, dentro do certificado de origem ouro/prata/bronze", "Incluído na certificação por tonelada (US$ 0,50–1,00/t)", "Exportadores de banana e soja")]
mr = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{e}</td></tr>" for a, b, c, e in mods)
d.append(f"""<div class='sec'><h1>4. Help Farm Energia: o que vender e como cobrar</h1>
<p>A Help Farm já instala sensores em bombas, pivôs e máquinas e aprende a assinatura de cada ativo. A energia é o mesmo dado lido de outro jeito: quanto cada m³ de água custa em kWh e em reais. O know-how da Moulin du Soleil e da Sollar Machine em usinas solares e baterias completa a oferta.</p>
<table><thead><tr><th style='width:18%'>Produto</th><th style='width:34%'>O que faz</th><th style='width:24%'>Como cobra</th><th>Exemplo</th></tr></thead><tbody>{mr}</tbody></table>
<div class='box'><b>Proposta para a FAPIJA, em quatro fases:</b> (1) Help Farm nas 40 unidades e na estação principal, com diagnóstico em 60 dias; (2) gestão de demanda, capacitores e manejo (ESCO, sem investimento); (3) migração da estação principal para o mercado livre; (4) usina solar de ≈ {str(S['mwp']).replace('.',',')} MWp atrás do medidor da estação principal, por PPA ou FNE Sol, pronta antes do fim do subsídio estadual. Com o certificado de origem, a banana exportada passa a sair com pegada de carbono medida.</div></div>""")

# 5. atratividade
d.append(f"""<div class='sec'><h1>5. Fica atrativo vender o projeto?</h1>
<h2>Para o produtor: a energia paga a assinatura</h2>
<table><thead><tr><th>Fazenda irrigada típica (500 ha de pivô, faixa B)</th><th class='n'>Valor</th></tr></thead><tbody>
<tr><td>Consumo de energia</td><td class='n'>{n0(F['mwh'])} MWh/ano</td></tr>
<tr><td>Conta de energia estimada</td><td class='n'>{rs(F['conta_rs'])} (≈ US$ {n0(F['conta_us'])})</td></tr>
<tr><td>Economia de 20% (gestão + manejo, sem usina)</td><td class='n'>≈ US$ {n0(F['economia_us'])}/ano</td></tr>
<tr><td>Assinatura Help Farm (grãos US$ 6/ha + fazenda + 6 ativos)</td><td class='n'>≈ US$ {n0(F['assinatura_us'])}/ano</td></tr>
<tr class='hl'><td>Economia ÷ assinatura</td><td class='n'>{str(round(F['economia_us']/F['assinatura_us'],1)).replace('.',',')}×</td></tr></tbody></table>
<p>A conversa muda de "quanto custa monitorar" para "quanto você deixa de pagar de luz". É o argumento mais fácil de provar: aparece na fatura do mês seguinte.</p>
<h2>Para a Help Farm: nova receita com margem alta</h2>
<table><thead><tr><th>Linha de energia no Ano 5 (Paraguai + Brasil, estimativa)</th><th class='n'>US$/ano</th></tr></thead><tbody>
<tr><td>ESCO: 30% da economia em {U['fazendas_irrigadas']} fazendas irrigadas (30% das fazendas no Brasil, 10% no Paraguai)</td><td class='n'>{n0(U['esco'])}</td></tr>
<tr><td>PPA solar: 0,5 MWp em 30% dessas fazendas</td><td class='n'>{n0(U['ppa'])}</td></tr>
<tr><td>Dois perímetros do porte da FAPIJA (ESCO + PPA)</td><td class='n'>{n0(U['perimetros'])}</td></tr>
<tr><td>Diagnósticos</td><td class='n'>{n0(U['diagnosticos'])}</td></tr>
<tr class='hl'><td><b>Total</b></td><td class='n'><b>{n0(U['total'])}</b></td></tr></tbody></table>
<p>Isso soma ≈ 14% à receita do Ano 5 do cenário Paraguai + Brasil (US$ 21 mi), com margem maior que a do monitoramento (a ESCO não tem custo de kit, e a usina é financiada fora do caixa da Help Farm, numa SPE). <b>Para o investidor</b>, essa linha devolve o valuation para perto dos US$ 9 mi negociados, que tinham caído para US$ 7,5 mi com os preços de mercado (estimativa; a planilha ainda não inclui a energia).</p>
<h2>Riscos</h2>
<ul><li><b>Dados:</b> a conta da FAPIJA é estimada. Sem as faturas, o retorno da usina pode variar de 5 a 9 anos.</li>
<li><b>Regulação:</b> Fio B, janela do irrigante e mercado livre mudam; a usina precisa ser desenhada sobre a curva de carga medida.</li>
<li><b>Foco:</b> obra de usina é outro negócio. A Help Farm deve vender o dado, o diagnóstico e a gestão; a usina fica numa SPE com parceiro de EPC e o know-how Moulin/Sollar.</li>
<li><b>Paraguai:</b> a ANDE é barata (≈ US$ 53/MWh){r(33)}; lá o argumento é diesel e rede fraca, não tarifa.</li></ul></div>""")

# 6. carbono
d.append(f"""<div class='sec'><h1>6. Carbono: onde vale e onde não vale</h1>
<table><thead><tr><th>Situação</th><th>Emissão evitada</th><th>Quanto vale</th></tr></thead><tbody>
<tr><td><b>Brasil, rede elétrica (FAPIJA)</b></td><td>{n0(S['mwh'])} MWh/ano × 0,0385 tCO2/MWh{r(37)} ≈ {n0(S['mwh']*0.0385)} tCO2/ano</td><td>US$ 1–6/t (crédito de renovável){r(40)} ≈ US$ {n0(S['mwh']*0.0385*1)}–{n0(S['mwh']*0.0385*6)}/ano; I-REC a US$ 0,2/MWh{r(41)} ≈ US$ {n0(S['mwh']*0.2)}/ano</td></tr>
<tr><td><b>Paraguai, rede (ANDE, hídrica)</b></td><td>25 gCO2e/kWh{r(38)}: quase nada</td><td>Perto de zero</td></tr>
<tr><td><b>Pivô a diesel (Chaco, Argentina, Austrália)</b></td><td>2,66 kg CO2e por litro{r(39)}; 500 ha ≈ 400 mil L ≈ 1.090 tCO2/ano (estimativa)</td><td>≈ US$ 6,5 mil/ano em crédito, mas ≈ US$ 440 mil/ano em diesel economizado: o diesel é o argumento</td></tr>
<tr><td><b>Pegada por produto para o comprador</b></td><td>kWh, diesel, água e insumos por kg de banana, soja ou carne</td><td>Acesso a mercado: Tesco (escopo 3 −55% até 2032), Walmart Gigaton (5.900 fornecedores){r(43,44)}, Soja Baixo Carbono da Embrapa{r(46)}</td></tr></tbody></table>
<div class='box'><b>Conclusão sobre carbono.</b> No Brasil e no Paraguai a rede já é limpa, então o crédito de carbono da usina é pequeno, e as metodologias para bombas solares têm problemas de qualidade{r(42)}. O valor está em <b>medir a pegada de cada lote</b> e entregá-la dentro do certificado de origem Help Farm: é o que varejistas e importadores pedem aos fornecedores. A banana do perímetro, exportada pelas empresas adjacentes, é o primeiro produto para isso (pegada de referência da banana do Equador: 0,19–0,22 kg CO2e/kg na porteira{r(47)}). A CSRD europeia foi restringida em 2025{r(45)}: a pressão chega pelo comprador, não por lei.</div>
<h2>Próximos passos</h2>
<div class='pts'><div class='pt'><i>1</i>Pedir à FAPIJA as faturas de 12 meses da estação principal e das unidades dos pivôs, e o contrato de demanda.</div>
<div class='pt'><i>2</i>Instalar o Help Farm (corrente, vibração e solo) em 5 pivôs e na estação principal: curva de carga real em 60 dias.</div>
<div class='pt'><i>3</i>Propor a ESCO (gestão de demanda, capacitores, manejo e janela de desconto) e a migração para o mercado livre.</div>
<div class='pt'><i>4</i>Dimensionar a usina com a SPE (know-how Moulin/Sollar) e abrir o FNE Sol no BNB antes de dezembro de 2026.</div>
<div class='pt'><i>5</i>Incluir a linha de energia na planilha do investidor como cenário adicional.</div></div></div>""")
refs = "<div class='sec'><h1>Referências</h1><ol class='refs'>" + "".join(f"<li><b>{H.escape(a)}</b> — {u}</li>" for a, u in REFS) + "</ol></div>"
open("doc.html", "w").write(page("".join(d) + refs))
cv = cover("Estudo de caso · FAPIJA · Jaguaribe-Apodi (CE)", "Energia própria no Help Farm: <em>a conta de luz</em> que paga o projeto",
           "Produção de 2024, diagnóstico energético do perímetro, custo da energia na irrigação no mundo e a análise de atratividade da geração solar, da gestão de energia e da pegada de carbono como serviço Help Farm.",
           [(mi(Bc['total']) + "/ano", "conta de energia estimada do perímetro"), (f"−{T['pct_sem_solar']}% a −{T['pct']}%", "economia sem e com usina solar"), (f"+US$ {str(round(U['total']/1e6,1)).replace('.',',')} mi/ano", "receita adicional do Help Farm no Ano 5")],
           "file:///home/claude/hfe/cv.jpg")
open("cover.html", "w").write(cv)
HD = "<div style='font-family:Inter,Arial;font-size:7pt;color:#5E4A38;width:100%;padding:0 15mm;display:flex;justify-content:space-between'><span><b style='color:#2E1D10'>Help Farm</b> · Energia própria · caso FAPIJA</span><span>Novembro de 2026</span></div>"
FT = "<div style='font-family:Inter,Arial;font-size:7pt;color:#5E4A38;width:100%;padding:0 15mm;display:flex;justify-content:space-between'><span>Estudo para a FAPIJA, investidores e equipe de prospecção</span><span>Página <span class='pageNumber'></span> de <span class='totalPages'></span></span></div>"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto("file:///home/claude/hfe/cover.html"); await pg.wait_for_timeout(300); await pg.pdf(path="_c.pdf", format="A4", print_background=True)
        await pg.goto("file:///home/claude/hfe/doc.html"); await pg.wait_for_timeout(300)
        await pg.pdf(path="_b.pdf", format="A4", print_background=True, display_header_footer=True, header_template=HD, footer_template=FT, margin=dict(top="17mm", bottom="15mm", left="15mm", right="15mm"))
        w = PdfWriter()
        for x in ["_c.pdf", "_b.pdf"]:
            for q in PdfReader(x).pages: w.add_page(q)
        w.write("HelpFarm_Energia_Propria_FAPIJA.pdf"); print(len(w.pages))
        await b.close()
asyncio.run(main())
