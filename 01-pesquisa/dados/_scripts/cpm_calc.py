import json,statistics as st
P=r"E:/Raio-X Survival Europa/01-pesquisa/dados/"
c=json.load(open(P+"cpm.json",encoding='utf-8'))
fx=c['usd_eur']
out=[]
TICKET=37.0   # front em EUR (premissa: mesmo preço do Lost SuperFoods, US$ 37)
AOV=55.0      # ticket médio com bump/upsell (premissa: AOV Digistore survival US$ 55-65 ~ EUR 50-58)
for g,(t,l,a) in c['paises'].items():
    vals=[v for v in [t,(l/fx if l else None),a] if v]
    cpm=round(st.median(vals),2)
    lo,hi=round(min(vals),2),round(max(vals),2)
    # funil: CTR no link 1,2% e conversão da VSL 1,5% (meio da régua VTurb 1-2%)
    cpa_mid=round(cpm/(1000*0.012*0.015),1)
    cpa_bom=round(cpm/(1000*0.015*0.02),1)
    cpa_ruim=round(cpm/(1000*0.009*0.01),1)
    dia=TICKET*3            # 3 criativos x 1 ticket por dia
    teste_min=dia*3         # 3 dias
    teste_seg=TICKET*5*4    # 5 criativos x 4 dias
    imp=int(teste_min/cpm*1000)
    out.append(dict(pais=g,cpm_eur=cpm,cpm_faixa=[lo,hi],fontes=len(vals),cpa_estimado=dict(bom=cpa_bom,medio=cpa_mid,ruim=cpa_ruim),
       verba_dia=dia,teste_min=teste_min,teste_seguro=teste_seg,impressoes_teste_min=imp,
       corte_oferta=[TICKET*2,TICKET*3],fecha_conta=cpa_mid<=AOV*0.9))
out.sort(key=lambda x:x['cpm_eur'])
json.dump(dict(premissas=dict(ticket_front_eur=TICKET,ticket_medio_eur=AOV,ctr=[0.009,0.012,0.015],conversao_vsl=[0.01,0.015,0.02],
   regra="1 ticket por criativo por dia; 3 criativos x 3 dias = teste minimo; 5 criativos x 4 dias = teste seguro; oferta sem venda apos 2-3 tickets medios desliga",
   fontes_regua="skill low-ticket 05-teste-e-escala.md; Ouro VTurb (conversao VSL frio 1-2%)",cpm="mediana das 3 fontes, USD convertido a 1,1193"),paises=out),
   open(P+"cpm-verba.json","w",encoding='utf-8'),ensure_ascii=False,indent=1)
for o in out: print(o['pais'],o['cpm_eur'],o['cpm_faixa'],o['cpa_estimado'],o['teste_min'],o['fecha_conta'])
