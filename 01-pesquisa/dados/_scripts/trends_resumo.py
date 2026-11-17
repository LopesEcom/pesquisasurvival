import json,statistics as st,sys
sys.stdout.reconfigure(encoding='utf-8')
P=r"E:/Raio-X Survival Europa/01-pesquisa/dados/"
d=json.load(open(P+"trends/trends.json",encoding='utf-8'))
POP={'GB':69,'DE':84,'FR':68,'ES':48,'IT':59,'PL':37,'LT':2.9,'NL':18,'SE':10.5,'FI':5.6,'PT':10.4,'IE':5.3,'BE':11.8,'AT':9.2,'US':335}
IDI={'GB':'inglês','IE':'inglês','US':'inglês','DE':'alemão','AT':'alemão','FR':'francês','BE':'francês/holandês','ES':'espanhol','IT':'italiano','PL':'polonês','LT':'lituano','NL':'holandês','SE':'sueco','FI':'finlandês','PT':'português'}
def mom(v): 
    base=st.mean(v[:-12]) or 0.01; return round(st.mean(v[-12:])/base,2)
out=[]
for g,s in d['serie_topico_pais'].items():
    ks=sorted(s); kit=[s[k][0] for k in ks]
    loc=d['serie_local'].get(g)
    melhor=None
    if loc and loc['serie']:
        lk=sorted(loc['serie'])
        for i,t in enumerate(loc['termos']):
            v=[loc['serie'][k][i] for k in lk]
            if max(v)<3: continue
            pk=max(range(len(v)),key=lambda j:v[j])
            m=mom(v)
            if not melhor or m>melhor['momento']: melhor=dict(termo=t,momento=m,pico=lk[pk],ult4=v[-4:])
    pk=max(range(len(kit)),key=lambda j:kit[j])
    top3=sorted(range(len(kit)),key=lambda j:-kit[j])[:3]
    recente=any(ks[j]>='2026-09-01' for j in top3)
    out.append(dict(pais=g,idioma=IDI.get(g),pop_mi=POP.get(g),topico_kit_momento=mom(kit),topico_kit_pico=ks[pk],pico_recente=recente,
        ult4=kit[-4:],termo_local_mais_forte=melhor,
        interesse_12m=(d['regioes'].get('survival_kit|today 12-m') or {}).get(g),
        interesse_3m=(d['regioes'].get('survival_kit|today 3-m') or {}).get(g),
        survivalism_12m=(d['regioes'].get('survivalism|today 12-m') or {}).get(g),
        prepper_12m=(d['regioes'].get('prepper|today 12-m') or {}).get(g)))
out.sort(key=lambda x:-x['topico_kit_momento'])
json.dump(dict(fonte="Google Trends via pytrends, coleta 16/11/2026; topico 'Survival kit' (/m/067rck) e 'Survivalism' (/m/019sl2) independem de idioma; momento = media das ultimas 12 semanas / media dos 5 anos anteriores",paises=out),open(P+"trends/resumo-paises.json","w",encoding='utf-8'),ensure_ascii=False,indent=1)
for o in out: print(o['pais'],o['topico_kit_momento'],o['topico_kit_pico'],o['pico_recente'],o['ult4'],(o['termo_local_mais_forte'] or {}).get('termo'),(o['termo_local_mais_forte'] or {}).get('momento'),o['interesse_12m'],o['interesse_3m'])
