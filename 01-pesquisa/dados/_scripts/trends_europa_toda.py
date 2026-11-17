# Varre toda a Europa no Google Trends: 5 anos semanal + 90 dias diário por país, tópicos que independem de idioma
# + termos locais nos idiomas que ainda não tinham sido medidos. Saída: trends/europa-toda.json
from pytrends.request import TrendReq
import json, time, random, sys
OUT = sys.argv[1]
p = TrendReq(hl='en-US', tz=0, timeout=(10, 30))
PAISES = ['GB','IE','DE','AT','CH','FR','BE','NL','LU','ES','PT','IT','MT','GR','CY','PL','CZ','SK','HU','RO','BG','HR','SI','RS','BA','ME','MK','AL','LT','LV','EE','FI','SE','NO','DK','IS','MD','UA']
res = {'topicos': {}, 'serie_5a': {}, 'serie_90d': {}, 'serie_local': {}, 'erros': []}
def save(): json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def nap(): time.sleep(random.uniform(8, 13))
def run(fn, label, tries=3):
    for i in range(tries):
        try: return fn()
        except Exception as e:
            res['erros'].append(f'{label}: {type(e).__name__} {str(e)[:120]}'); save(); time.sleep(60 * (i + 1))
    return None
TOP = {'survival_kit': '/m/067rck', 'survivalism': '/m/019sl2'}
for nome in ['Bomb shelter', 'World War III', 'Emergency management']:
    def f():
        s = p.suggestions(nome)
        return next((x for x in s if x.get('type')), None)
    s = run(f, 'sugestao ' + nome); nap()
    if s: TOP[nome.lower().replace(' ', '_')] = s['mid']; res['topicos'][nome] = s
res['topicos']['_usados'] = TOP; save()
mids = list(TOP.values())[:5]; nomes = list(TOP.keys())[:5]
for g in PAISES:
    for tf, chave in [('today 5-y', 'serie_5a'), ('today 3-m', 'serie_90d')]:
        def f():
            p.build_payload(mids, timeframe=tf, geo=g)
            d = p.interest_over_time()
            if d is None or d.empty: return {}
            return {str(i.date()): [int(r[m]) for m in mids] for i, r in d.iterrows()}
        res[chave][g] = {'nomes': nomes, 'serie': run(f, f'{chave} {g}')}; save(); nap()
LOC = {
 'LV': ['ārkārtas soma', 'patvertne', '72 stundas', 'karš', 'izdzīvošanas'],
 'EE': ['hädaolukord', 'varjend', '72 tundi', 'sõda', 'ellujäämis'],
 'NO': ['egenberedskap', 'tilfluktsrom', 'beredskap', 'nødlager', 'krig'],
 'DK': ['nødpakke', 'beredskab', 'beskyttelsesrum', 'krisekasse', 'krig'],
 'CZ': ['evakuační zavazadlo', 'nouzový balíček', 'kryt', 'válka', 'prepper'],
 'SK': ['evakuačná batožina', 'núdzový balíček', 'kryt', 'vojna', 'prepper'],
 'RO': ['kit de urgență', 'rucsac de urgență', 'adăpost', 'război', 'kit de supraviețuire'],
 'GR': ['κιτ έκτακτης ανάγκης', 'καταφύγιο', 'πόλεμος', 'τσάντα έκτακτης ανάγκης', 'επιβίωση'],
 'HU': ['túlélőcsomag', 'óvóhely', 'vészhelyzeti csomag', 'háború', 'prepper'],
 'HR': ['paket za hitne slučajeve', 'sklonište', 'rat', 'ruksak za preživljavanje', 'preživljavanje'],
 'SI': ['nujni paket', 'zaklonišče', 'vojna', 'preživetje', 'nahrbtnik za nujne primere'],
 'BG': ['аварийна раница', 'бомбоубежище', 'война', 'оцеляване', 'аварийен комплект'],
 'CH': ['Notvorrat', 'Notfallrucksack', 'Bunker', 'Krieg', 'Stromausfall'],
 'BE': ['noodpakket', 'kit d\'urgence', 'prepper', 'oorlog', 'guerre'],
 'AT': ['Notvorrat', 'Notfallrucksack', 'Blackout', 'Krieg', 'Prepper'],
 'IE': ['emergency kit', 'be winter ready', 'stockpile', 'power outage', 'prepper'],
}
for g, ts in LOC.items():
    def f():
        p.build_payload(ts, timeframe='today 5-y', geo=g)
        d = p.interest_over_time()
        if d is None or d.empty: return {}
        return {str(i.date()): [int(r[t]) for t in ts] for i, r in d.iterrows()}
    res['serie_local'][g] = {'termos': ts, 'serie': run(f, f'local {g}')}; save(); nap()
save(); print('FIM', len(res['erros']), 'erros')
