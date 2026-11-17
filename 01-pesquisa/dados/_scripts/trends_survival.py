from pytrends.request import TrendReq
import json,time,random,sys,traceback
OUT=sys.argv[1]
p=TrendReq(hl='en-US',tz=0,timeout=(10,30))
EU=['GB','DE','FR','ES','IT','PL','LT','LV','EE','FI','SE','NO','DK','NL','BE','AT','CH','IE','PT','CZ','RO','GR','HU','SK','US','CA','AU']
res={'regioes':{},'serie_topico_pais':{},'serie_local':{},'erros':[]}
def nap(): time.sleep(random.uniform(9,14))
def save(): json.dump(res,open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
def run(fn,label,tries=3):
    for i in range(tries):
        try: return fn()
        except Exception as e:
            res['erros'].append(f'{label}: {type(e).__name__} {str(e)[:120]}'); time.sleep(60*(i+1))
    return None
TOP={'survival_kit':'/m/067rck','survivalism':'/m/019sl2','prepper':'/g/11cfjl3_h','bug_out_bag':'/g/11bc59s8q1'}
# A. ranking por pais (mundo)
for nome,mid in TOP.items():
    for tf in ['today 12-m','today 3-m','today 5-y']:
        def f():
            p.build_payload([mid],timeframe=tf,geo='')
            d=p.interest_by_region(resolution='COUNTRY',inc_low_vol=True,inc_geo_code=True)
            d=d[d['geoCode'].isin(EU)]
            return {r['geoCode']:int(r[mid]) for _,r in d.iterrows()}
        r=run(f,f'regiao {nome} {tf}')
        res['regioes'][f'{nome}|{tf}']=r; save(); nap()
# B. serie do topico survival kit + survivalism por pais (5 anos, semanal) -> picos
for g in ['GB','DE','FR','ES','IT','PL','LT','NL','SE','FI','PT','IE','BE','AT','US']:
    def f():
        p.build_payload([TOP['survival_kit'],TOP['survivalism']],timeframe='today 5-y',geo=g)
        d=p.interest_over_time()
        return {str(i.date()):[int(r[TOP['survival_kit']]),int(r[TOP['survivalism']])] for i,r in d.iterrows()}
    res['serie_topico_pais'][g]=run(f,f'serie {g}'); save(); nap()
# C. termos locais (cada pais no seu idioma), 5 anos
LOC={'GB':['emergency kit','bug out bag','prepper','food stockpile','world war 3'],
 'DE':['Notfallrucksack','Notvorrat','Krisenvorsorge','Prepper','Notfallradio'],
 'FR':['kit de survie','sac d\'urgence','survivalisme','kit d\'urgence','troisième guerre mondiale'],
 'ES':['kit de supervivencia','kit de emergencia','mochila de emergencia','tercera guerra mundial','prepper'],
 'IT':['kit di sopravvivenza','kit di emergenza','zaino di emergenza','terza guerra mondiale','prepper'],
 'PL':['plecak ewakuacyjny','zestaw przetrwania','schron','III wojna światowa','prepper'],
 'LT':['išgyvenimo kuprinė','karas','slėptuvė','išgyvenimo','ekstremali situacija'],
 'NL':['noodpakket','noodtas','prepper','derde wereldoorlog','noodvoorraad'],
 'SE':['krisberedskap','om krisen eller kriget kommer','prepper','hemberedskap','krislåda'],
 'FI':['kotivara','72 tuntia','prepper','varautuminen','väestönsuoja'],
 'PT':['kit de sobrevivência','kit de emergência','mochila de emergência','terceira guerra mundial','prepper'],
 'US':['bug out bag','emergency food','survival kit','prepper','emp attack']}
for g,ts in LOC.items():
    def f():
        p.build_payload(ts,timeframe='today 5-y',geo=g)
        d=p.interest_over_time()
        return {str(i.date()):[int(r[t]) for t in ts] for i,r in d.iterrows()}
    res['serie_local'][g]={'termos':ts,'serie':run(f,f'local {g}')}; save(); nap()
save(); print('FIM', len(res['erros']),'erros')
