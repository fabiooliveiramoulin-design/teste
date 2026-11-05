# Página "Help Farm ajuda a economizar energia" (energia.html)
import sys
_m = sys.modules["__main__"]
Page, shell, stl, feats, explainer = _m.Page, _m.shell, _m.stl, _m.feats, _m.explainer


def svg_bombeamento(pg):
    # esquema: sol -> painéis -> bomba solar no rio -> recalque -> reservatório elevado -> gravidade -> pivô/lavoura
    return f'''<svg class="sig" viewBox="0 0 560 330" role="img" aria-label="Bombeamento solar off-grid com recalque para reservatório elevado">
<rect x="0" y="0" width="560" height="330" rx="20" fill="#2E1D10"/>
<circle cx="70" cy="62" r="22" fill="#FFB500"/>
<g stroke="#FFB500" stroke-width="3" stroke-linecap="round" opacity=".7">{"".join('<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (70 + 30 * dx, 62 + 30 * dy, 70 + 40 * dx, 62 + 40 * dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7)))}</g>
<path d="M40 262 L190 262 L330 150 L520 150 L520 320 L40 320 Z" fill="#4A2F1B"/>
<path d="M40 268 Q90 258 150 268 T260 270 L260 320 L40 320 Z" fill="#2F6E8F" opacity=".85"/>
<g transform="translate(110 180)"><g fill="#3A5F86" stroke="#9BC4E8" stroke-width="1.2">
<polygon points="0,30 34,0 74,0 40,30"/><polygon points="44,30 78,0 118,0 84,30"/></g>
<line x1="20" y1="30" x2="20" y2="58" stroke="#C9A36B" stroke-width="3"/><line x1="64" y1="30" x2="64" y2="58" stroke="#C9A36B" stroke-width="3"/></g>
<rect x="196" y="250" width="26" height="20" rx="4" fill="#8FCB5A"/>
<path d="M150 232 Q190 240 205 250" fill="none" stroke="#FFB500" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M222 258 L330 170 L388 170" fill="none" stroke="#9BC4E8" stroke-width="5" stroke-linecap="round"/>
<rect x="388" y="112" width="70" height="58" rx="6" fill="#5E7C93" stroke="#9BC4E8" stroke-width="1.5"/>
<rect x="392" y="132" width="62" height="34" rx="3" fill="#2F6E8F"/>
<line x1="400" y1="170" x2="400" y2="150" stroke="#C9A36B" stroke-width="3"/><line x1="446" y1="170" x2="446" y2="150" stroke="#C9A36B" stroke-width="3"/>
<path d="M458 160 L520 160" fill="none" stroke="#9BC4E8" stroke-width="4" stroke-dasharray="8 5"/>
<g stroke="#8FCB5A" stroke-width="2" fill="none" opacity=".9"><path d="M470 214 Q495 200 520 214"/><path d="M470 232 Q495 218 520 232"/><path d="M470 250 Q495 236 520 250"/></g>
{stl(pg, 116, 68, "sol de dia = bombeamento", "sol de día = bombeo", "daytime sun = pumping", "lb lo")}
{stl(pg, 108, 172, "painéis solares", "paneles solares", "solar panels", "lb lw")}
{stl(pg, 228, 296, "bomba solar no rio ou poço", "bomba solar en el río o pozo", "solar pump at river or well", "lb lm")}
{stl(pg, 300, 236, "recalque", "rebombeo", "lift main", "lb lg")}
{stl(pg, 423, 100, "reservatório elevado", "reservorio elevado", "elevated reservoir", "lb lw", "middle")}
{stl(pg, 520, 274, "pivô e lavoura por gravidade", "pivote y cultivo por gravedad", "pivot and crops by gravity", "lb lg", "end")}
{stl(pg, 300, 40, "a água guardada no alto é a “bateria”", "el agua guardada en altura es la “batería”", "water stored up high is the “battery”", "lb lm")}
</svg>'''


def energia():
    pg = Page()
    title = pg.title("Energia — Help Farm", "Energía — Help Farm", "Energy — Help Farm")
    passos = [
        (("Mede os consumos internos", "Desde a implantação, garras de corrente e medidores entram nas bombas, pivôs, ordenha, câmaras frias e secadores, junto com os outros sensores."),
         ("Mide los consumos internos", "Desde la implantación, pinzas de corriente y medidores se instalan en bombas, pivotes, ordeñe, cámaras de frío y secadoras, junto con los demás sensores."),
         ("Measures internal consumption", "From day one, current clamps and meters go on pumps, pivots, milking, cold rooms and dryers, alongside the other sensors.")),
        (("Cruza energia com produção", "O RAPP calcula quanto custa cada m³ de água bombeada, cada hectare irrigado, cada litro de leite resfriado, e separa o que é uso do que é desperdício."),
         ("Cruza energía con producción", "El RAPP calcula cuánto cuesta cada m³ de agua bombeada, cada hectárea regada, cada litro de leche enfriada, y separa el uso del desperdicio."),
         ("Crosses energy with output", "RAPP works out the cost of each m³ of water pumped, each hectare irrigated, each litre of milk cooled, and separates use from waste.")),
        (("Propõe eficiência e geração própria", "Primeiro o que não exige obra. Depois, um projeto solar para cada atividade que dá retorno: ligado à rede, híbrido ou off-grid."),
         ("Propone eficiencia y generación propia", "Primero lo que no exige obra. Después, un proyecto solar para cada actividad con retorno: conectado a la red, híbrido u off-grid."),
         ("Proposes efficiency and own generation", "First, what needs no works. Then a solar project for each activity that pays back: grid-tied, hybrid or off-grid.")),
        (("Monitora e prova a economia", "A usina vira mais um ativo do RAPP. Todo mês, a geração e a economia na conta são verificadas e entram no relatório do produtor."),
         ("Monitorea y prueba el ahorro", "La planta pasa a ser un activo más del RAPP. Cada mes, la generación y el ahorro en la factura se verifican y entran en el informe del productor."),
         ("Monitors and proves the savings", "The plant becomes one more RAPP asset. Every month, generation and bill savings are verified and go into the producer’s report.")),
    ]
    rows = [
        (("Bombeamento e recalque", "Bombeo y rebombeo", "Pumping and lift"),
         ("kWh por m³, altura, horas de bomba, rendimento", "kWh por m³, altura, horas de bomba, rendimiento", "kWh per m³, head, pump hours, efficiency"),
         ("Bomba gasta, operação fora da janela de desconto", "Bomba desgastada, operación fuera de la franja de descuento", "Worn pump, running outside the discount window"),
         ("Bomba solar off-grid enchendo reservatório elevado de dia", "Bomba solar off-grid llenando reservorio elevado de día", "Off-grid solar pump filling an elevated reservoir by day")),
        (("Pivô central", "Pivote central", "Centre pivot"),
         ("kWh por hectare, pressão, umidade do solo", "kWh por hectárea, presión, humedad del suelo", "kWh per hectare, pressure, soil moisture"),
         ("Lâmina aplicada sem o solo pedir; demanda contratada alta", "Lámina aplicada sin que el suelo la pida; demanda contratada alta", "Water applied the soil did not need; contracted demand too high"),
         ("Usina ligada à rede ou pivô solar híbrido (troca do diesel)", "Planta conectada a la red o pivote solar híbrido (reemplazo del diésel)", "Grid-tied plant or hybrid solar pivot (replacing diesel)")),
        (("Ordenha e resfriamento", "Ordeñe y enfriamiento", "Milking and cooling"),
         ("kWh por litro, temperatura do tanque", "kWh por litro, temperatura del tanque", "kWh per litre, tank temperature"),
         ("Compressor em falha, pré-resfriamento ausente", "Compresor con falla, sin preenfriamiento", "Failing compressor, no pre-cooling"),
         ("Solar no galpão, casando com o horário da ordenha", "Solar en el galpón, coincidiendo con el horario del ordeñe", "Solar on the shed roof, matched to milking times")),
        (("Câmara fria e packing", "Cámara de frío y empaque", "Cold room and packing"),
         ("kWh por tonelada, abertura de portas", "kWh por tonelada, apertura de puertas", "kWh per tonne, door openings"),
         ("Isolamento ruim, degelo mal regulado", "Aislamiento deficiente, deshielo mal regulado", "Poor insulation, badly set defrost")),
        (("Secagem e armazenagem", "Secado y almacenamiento", "Drying and storage"),
         ("kWh e lenha por tonelada seca", "kWh y leña por tonelada seca", "kWh and firewood per tonne dried"),
         ("Aeração ligada sem necessidade", "Aireación encendida sin necesidad", "Aeration running when not needed"),
         ("Solar para aeração e motores do armazém", "Solar para aireación y motores del depósito", "Solar for aeration and storage motors")),
        (("Poços e bebedouros remotos", "Pozos y bebederos remotos", "Remote wells and troughs"),
         ("Nível, vazão, horas de gerador", "Nivel, caudal, horas de generador", "Level, flow, generator hours"),
         ("Gerador a diesel para pouca água", "Generador diésel para poca agua", "Diesel generator for little water"),
         ("Kit solar off-grid com caixa d’água", "Kit solar off-grid con tanque", "Off-grid solar kit with water tank")),
    ]
    rows[3] = rows[3] + (("Solar com o pico de geração no horário mais quente", "Solar con el pico de generación en el horario más caluroso", "Solar peaking at the hottest hours"),)
    th = "".join(pg.t(*h, "th") for h in [("Atividade", "Actividad", "Activity"), ("O que o RAPP mede", "Qué mide el RAPP", "What RAPP measures"), ("Desperdício típico", "Desperdicio típico", "Typical waste"), ("Projeto de geração", "Proyecto de generación", "Generation project")])
    trs = "".join("<tr>%s</tr>" % "".join(pg.t(*c, "td") for c in r) for r in rows)
    offgrid = [
        (("Sem rede e sem diesel", "a bomba trabalha com o sol e enche o reservatório; a água guardada no alto faz o papel da bateria"),
         ("Sin red y sin diésel", "la bomba trabaja con el sol y llena el reservorio; el agua guardada en altura cumple el papel de batería"),
         ("No grid, no diesel", "the pump runs on sunshine and fills the reservoir; water stored up high does the job of a battery")),
        (("Recalque por etapas", "do rio para a chapada, cada estação de recalque pode ter a sua usina, dimensionada pela vazão medida"),
         ("Rebombeo por etapas", "del río a la meseta, cada estación de rebombeo puede tener su planta, dimensionada por el caudal medido"),
         ("Staged lifting", "from river to plateau, each lift station can have its own plant, sized from the measured flow")),
        (("Onde a rede não chega", "fazendas no Chaco, pastos distantes e áreas com rede fraca ou quedas de tensão"),
         ("Donde la red no llega", "establecimientos en el Chaco, potreros lejanos y zonas con red débil o caídas de tensión"),
         ("Where the grid does not reach", "farms in the Chaco, distant pastures and areas with a weak grid or voltage drops")),
        (("Pago pela economia", "contra o diesel, o bombeamento solar costuma se pagar em poucos anos; o RAPP acompanha a geração e a água bombeada"),
         ("Pagado por el ahorro", "frente al diésel, el bombeo solar suele pagarse en pocos años; el RAPP sigue la generación y el agua bombeada"),
         ("Paid for by the savings", "against diesel, solar pumping usually pays back in a few years; RAPP tracks generation and water pumped")),
    ]
    modos = [
        (("Diagnóstico na implantação", "Faz parte da entrada do Help Farm: 60 a 90 dias de consumo medido e o relatório com as atividades que podem economizar."),
         ("Diagnóstico en la implantación", "Forma parte de la entrada de Help Farm: 60 a 90 días de consumo medido y el informe con las actividades que pueden ahorrar."),
         ("Diagnosis at onboarding", "Part of joining Help Farm: 60 to 90 days of measured consumption and a report on the activities that can save.")),
        (("Você divide só a economia", "A eficiência sem obra pode ser contratada por uma parte da economia verificada na fatura. Se não economizar, não paga."),
         ("Usted comparte solo el ahorro", "La eficiencia sin obra puede contratarse por una parte del ahorro verificado en la factura. Si no ahorra, no paga."),
         ("You only share the savings", "No-works efficiency can be contracted for a share of the savings verified on the bill. No savings, no payment.")),
        (("A usina do seu jeito", "Compra própria, financiamento verde ou energia contratada sem investimento, com parceiros de engenharia solar."),
         ("La planta a su manera", "Compra propia, financiamiento verde o energía contratada sin inversión, con socios de ingeniería solar."),
         ("The plant your way", "Own purchase, green financing or contracted energy with no upfront investment, through solar-engineering partners.")),
        (("Pegada de carbono no lote", "kWh e diesel por quilo produzido entram no certificado de origem Help Farm, o dado que compradores e importadores pedem."),
         ("Huella de carbono en el lote", "kWh y diésel por kilo producido entran en el certificado de origen Help Farm, el dato que piden compradores e importadores."),
         ("Carbon footprint on the lot", "kWh and diesel per kilo produced go into the Help Farm origin certificate, the data buyers and importers ask for.")),
    ]
    body = f'''
<div class="hero hv">
  <div class="wrap">
    <div>
      {pg.t("Help Farm · energia", "Help Farm · energía", "Help Farm · energy", "span", "eyebrow")}
      {pg.t("Help Farm ajuda a <em>economizar energia</em>.", "Help Farm ayuda a <em>ahorrar energía</em>.", "Help Farm helps you <em>save energy</em>.", "h1", raw=True)}
      {pg.t("Desde a implantação, uma das funções do Help Farm é avaliar quais atividades da fazenda podem receber ações de eficiência energética. Cruzamos os consumos internos com a produção e propomos ao produtor um projeto de energia solar, inclusive off-grid para bombeamento e recalque.", "Desde la implantación, una de las funciones de Help Farm es evaluar qué actividades del establecimiento pueden recibir acciones de eficiencia energética. Cruzamos los consumos internos con la producción y proponemos al productor un proyecto de energía solar, incluso off-grid para bombeo y rebombeo.", "From onboarding, one of Help Farm’s jobs is to assess which farm activities can benefit from energy efficiency. We cross internal consumption with production and propose a solar project to the farmer, including off-grid systems for pumping and lifting water.", "p", "lead")}
      <div class="cta"><a class="btn primary" href="#como">{pg.t("Como funciona", "Cómo funciona", "How it works")}</a><a class="btn ghost" href="mailto:investidores@helpcure.com.py?subject=Help%20Farm%20Energia">{pg.t("Quero avaliar minha fazenda", "Quiero evaluar mi establecimiento", "Assess my farm")}</a></div>
    </div>
    <div class="hv-media" style="aspect-ratio:auto;overflow:visible;box-shadow:none;background:none;border-radius:0"><figure style="margin:0"><img src="img/energia-recalque.webp" srcset="img/energia-recalque-960.webp 960w, img/energia-recalque.webp 1376w" sizes="(max-width:960px) 100vw, 560px" alt="Bombeamento solar sem bateria: módulos na margem do rio, bomba solar, tubulação de recalque até o reservatório elevado e pivô central na lavoura" style="width:100%;border-radius:20px;aspect-ratio:16/9;object-fit:cover;box-shadow:0 18px 40px rgba(0,0,0,.35);display:block"><figcaption style="font-size:13px;color:#D9C6AC;margin-top:10px">{pg.t("Imagem ilustrativa: módulos solares na margem do rio, bomba solar sem bateria, recalque até o reservatório elevado e pivô irrigando por gravidade.", "Imagen ilustrativa: módulos solares en la orilla del río, bomba solar sin batería, rebombeo hasta el reservorio elevado y pivote regando por gravedad.", "Illustrative image: solar modules on the riverbank, battery-free solar pump, lift main to the elevated reservoir and a pivot irrigating by gravity.")}</figcaption></figure></div>
  </div>
</div>

<section id="como">
  <div class="wrap">
    <div class="head">{pg.t("Como funciona", "Cómo funciona", "How it works", "span", "eyebrow")}{pg.t("Os mesmos sensores, uma pergunta a mais: quanto custa cada atividade em energia?", "Los mismos sensores, una pregunta más: ¿cuánto cuesta cada actividad en energía?", "The same sensors, one more question: what does each activity cost in energy?", "h2")}
    {pg.t("O motor RAPP já aprende a assinatura normal de cada bomba, pivô e máquina. Com a energia medida no mesmo histórico, ele sabe se a lavoura precisava daquela água, se a bomba está gastando mais do que deveria e em que horário a energia sai mais cara.", "El motor RAPP ya aprende la firma normal de cada bomba, pivote y máquina. Con la energía medida en el mismo historial, sabe si el cultivo necesitaba esa agua, si la bomba gasta más de lo que debería y en qué horario la energía sale más cara.", "The RAPP engine already learns the normal signature of each pump, pivot and machine. With energy measured on the same timeline, it knows whether the crop needed that water, whether the pump is using more than it should and when energy costs the most.", "p", "muted")}</div>
    <div class="g g4 steps">{"".join('<div class="step">%s%s</div>' % (pg.t(a[0], b[0], c[0], "h3"), pg.t(a[1], b[1], c[1], "p")) for a, b, c in passos)}</div>
    {explainer(pg, "energia", ("Recalque solar sem bateria", "Rebombeo solar sin batería", "Solar water lifting with no battery"), "53 s", [
        ("A energia das bombas pesa no custo de irrigar", "La energía de las bombas pesa en el costo de regar", "Pump energy weighs on the cost of irrigating"),
        ("Primeiro, o Help Farm mede o consumo e a água que a lavoura pede", "Primero, Help Farm mide el consumo y el agua que pide el cultivo", "First, Help Farm measures consumption and the water the crop needs"),
        ("De dia, os módulos solares ligam a bomba direto, sem bateria", "De día, los módulos solares encienden la bomba directamente, sin batería", "By day, solar modules run the pump directly, with no battery"),
        ("A bomba recalca a água do rio até um reservatório no alto", "La bomba eleva el agua del río hasta un reservorio en altura", "The pump lifts river water to a reservoir on high ground"),
        ("À noite, a água desce por gravidade até o pivô", "De noche, el agua baja por gravedad hasta el pivote", "At night, water flows down by gravity to the pivot"),
        ("A usina se paga com a economia, conferida todo mês pelo RAPP", "La planta se paga con el ahorro, verificado cada mes por el RAPP", "The plant pays for itself with savings RAPP checks every month")])}
  </div>
</section>

<section class="soft">
  <div class="wrap">
    <div class="head">{pg.t("Onde a energia pesa", "Dónde pesa la energía", "Where energy weighs", "span", "eyebrow")}{pg.t("Cada atividade, a sua solução.", "Cada actividad, su solución.", "Each activity, its own solution.", "h2")}
    {pg.t("Na irrigação, a energia pode chegar a 30–50% do custo. O projeto não é uma usina genérica: é dimensionado pela curva de consumo medida em cada atividade.", "En el riego, la energía puede llegar al 30–50% del costo. El proyecto no es una planta genérica: se dimensiona con la curva de consumo medida en cada actividad.", "In irrigation, energy can reach 30–50% of costs. The project is not a generic plant: it is sized from the consumption curve measured for each activity.", "p", "muted")}</div>
    <div class="tablewrap"><table class="hft"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>
  </div>
</section>

<section class="dark">
  <div class="wrap split" style="align-items:start">
    <div>
      {pg.t("Off-grid", "Off-grid", "Off-grid", "span", "eyebrow")}
      {pg.t("Bombeamento e recalque com o sol.", "Bombeo y rebombeo con el sol.", "Pumping and lifting with the sun.", "h2")}
      {pg.t("Onde a rede é cara, fraca ou não existe, a bomba solar trabalha durante o dia e eleva a água até um reservatório. Dali, a água desce por gravidade para o pivô, o gotejamento ou o bebedouro, quando for preciso.", "Donde la red es cara, débil o no existe, la bomba solar trabaja durante el día y eleva el agua hasta un reservorio. Desde allí, el agua baja por gravedad al pivote, al goteo o al bebedero, cuando haga falta.", "Where the grid is expensive, weak or missing, the solar pump works during the day and lifts water to a reservoir. From there, water flows down by gravity to the pivot, drip lines or troughs whenever needed.", "p", "muted", attrs=' style="margin-top:14px;color:#D9C6AC"')}
      <div class="sigbox" style="margin-top:24px">{svg_bombeamento(pg)}</div>
    </div>
    <div>{feats(pg, offgrid)}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head">{pg.t("Exemplo", "Ejemplo", "Example", "span", "eyebrow")}{pg.t("Fazenda irrigada de 500 ha de pivô no Brasil.", "Establecimiento regado de 500 ha de pivote en Brasil.", "A 500 ha centre-pivot farm in Brazil.", "h2")}</div>
    <div class="kpis k4">
      <div class="kpi">{pg.t("US$ 101 mil", "US$ 101 mil", "US$ 101k", "b")}{pg.t("conta de energia por ano, antes", "factura de energía por año, antes", "energy bill per year, before", "span")}</div>
      <div class="kpi"><b>−15%</b>{pg.t("só com eficiência, sem obra: demanda, reativos, horário e manejo", "solo con eficiencia, sin obra: demanda, reactivos, horario y manejo", "efficiency alone, no works: demand, reactive power, timing and scheduling", "span")}</div>
      <div class="kpi"><b>≈ 240 kWp</b>{pg.t("de usina solar para o bombeamento diurno, com retorno em cerca de 5 a 6 anos", "de planta solar para el bombeo diurno, con retorno en unos 5 a 6 años", "solar plant for daytime pumping, paying back in about 5 to 6 years", "span")}</div>
      <div class="kpi"><b>≈ −47%</b>{pg.t("na conta de luz, somando eficiência e usina", "en la factura, sumando eficiencia y planta", "on the bill, efficiency and plant combined", "span")}</div>
    </div>
    {pg.t("Estimativa com 2.700 kWh por hectare por ano e tarifas médias do Brasil em 2026. O número de cada fazenda sai do diagnóstico, com as faturas reais e o consumo medido.", "Estimación con 2.700 kWh por hectárea por año y tarifas medias de Brasil en 2026. El número de cada establecimiento sale del diagnóstico, con las facturas reales y el consumo medido.", "Estimate based on 2,700 kWh per hectare per year and average Brazilian tariffs in 2026. Each farm’s figure comes from the diagnosis, using real bills and measured consumption.", "p", "note", attrs=' style="margin-top:14px"')}
  </div>
</section>

<section class="soft">
  <div class="wrap">
    <div class="head">{pg.t("Para o produtor", "Para el productor", "For the farmer", "span", "eyebrow")}{pg.t("A conta de luz ajuda a pagar o monitoramento.", "La factura de luz ayuda a pagar el monitoreo.", "The power bill helps pay for monitoring.", "h2")}</div>
    <div class="g g4 steps">{"".join('<div class="step">%s%s</div>' % (pg.t(a[0], b[0], c[0], "h3"), pg.t(a[1], b[1], c[1], "p")) for a, b, c in modos)}</div>
    <div class="cta" style="margin-top:28px"><a class="btn dark" href="tecnologia.html">{pg.t("Ver o motor RAPP", "Ver el motor RAPP", "See the RAPP engine")} →</a><a class="btn primary" href="certificacao.html">{pg.t("Certificação de origem", "Certificación de origen", "Origin certification")}</a></div>
  </div>
</section>
'''
    shell(pg, "energia.html", title, body, "Help Farm avalia o consumo de energia da fazenda e propõe eficiência e geração solar, inclusive off-grid para bombeamento e recalque.")
