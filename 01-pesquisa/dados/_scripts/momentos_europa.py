# Detecta, país por país, os MOMENTOS em que o tema subiu (picos semanais em 5 anos + o dia exato nos últimos 90 dias)
# e liga cada pico ao acontecimento mais provável. Saída: trends/momentos-europa.json
import json, statistics as st, datetime as dt, sys
sys.stdout.reconfigure(encoding='utf-8')
D = r"E:/Raio-X Survival Europa/01-pesquisa/dados/"
T = json.load(open(D + 'trends/europa-toda.json', encoding='utf-8'))
NOME = {'GB':'Reino Unido','IE':'Irlanda','DE':'Alemanha','AT':'Áustria','CH':'Suíça','FR':'França','BE':'Bélgica','NL':'Holanda','LU':'Luxemburgo','ES':'Espanha','PT':'Portugal','IT':'Itália','MT':'Malta','GR':'Grécia','CY':'Chipre','PL':'Polônia','CZ':'Tchéquia','SK':'Eslováquia','HU':'Hungria','RO':'Romênia','BG':'Bulgária','HR':'Croácia','SI':'Eslovênia','RS':'Sérvia','BA':'Bósnia','ME':'Montenegro','MK':'Macedônia do Norte','AL':'Albânia','LT':'Lituânia','LV':'Letônia','EE':'Estônia','FI':'Finlândia','SE':'Suécia','NO':'Noruega','DK':'Dinamarca','IS':'Islândia','MD':'Moldávia','UA':'Ucrânia'}
POP = {'GB':69,'IE':5.3,'DE':84,'AT':9.2,'CH':8.9,'FR':68,'BE':11.8,'NL':18,'LU':0.7,'ES':48,'PT':10.4,'IT':59,'MT':0.5,'GR':10.4,'CY':1.3,'PL':37,'CZ':10.9,'SK':5.4,'HU':9.6,'RO':19,'BG':6.4,'HR':3.9,'SI':2.1,'RS':6.6,'BA':3.2,'ME':0.6,'MK':1.8,'AL':2.4,'LT':2.9,'LV':1.9,'EE':1.4,'FI':5.6,'SE':10.5,'NO':5.6,'DK':5.9,'IS':0.4,'MD':2.4,'UA':37}
IDI = {'GB':'inglês','IE':'inglês','MT':'inglês','DE':'alemão','AT':'alemão','CH':'alemão/francês/italiano','LU':'francês/alemão','FR':'francês','BE':'francês/holandês','NL':'holandês','ES':'espanhol','PT':'português','IT':'italiano','GR':'grego','CY':'grego','PL':'polonês','CZ':'tcheco','SK':'eslovaco','HU':'húngaro','RO':'romeno','MD':'romeno','BG':'búlgaro','HR':'croata','SI':'esloveno','RS':'sérvio','BA':'bósnio','ME':'montenegrino','MK':'macedônio','AL':'albanês','LT':'lituano','LV':'letão','EE':'estoniano','FI':'finlandês','SE':'sueco','NO':'norueguês','DK':'dinamarquês','IS':'islandês','UA':'ucraniano'}
# acontecimentos: (data, paises ('*' = todos), descrição curta, id da fonte)
EV = [
 ('2022-02-24', '*', 'Invasão russa da Ucrânia', None),
 ('2022-09-21', '*', 'Mobilização russa e ameaça nuclear de Putin', None),
 ('2022-09-01', 'DE AT CH', 'Crise do gás e medo de apagão no inverno', None),
 ('2024-09-15', 'AT CZ PL SK HU RO', 'Tempestade Boris e enchentes na Europa Central', None),
 ('2025-03-04', '*', 'Plano ReArm Europe e debate de rearmamento', None),
 ('2026-01-04', 'DE', 'Apagão em Berlim após incêndio criminoso em cabos', None),
 ('2024-03-01', 'FR', 'Macron não descarta tropas na Ucrânia; debate de guerra na França', None),
 ('2024-05-15', 'NO', 'Noruega passa a pedir estoque de 1 semana', None),
 ('2024-06-15', 'DK', 'Dinamarca lança guia de 3 dias', None),
 ('2024-11-18', 'SE FI NO DK EE LV LT', 'Folhetos nórdicos de guerra chegam às casas', 'nórdicos'),
 ('2024-11-19', '*', 'Rússia muda a doutrina nuclear', None),
 ('2024-12-08', 'NL BE', 'Holanda prepara campanha nacional de noodpakket', None),
 ('2025-03-19', 'FR', 'França anuncia guia de sobrevivência para todas as casas', None),
 ('2025-03-26', '*', 'UE lança a estratégia de 72 horas (Preparedness Union)', 'UE 72 h 2025'),
 ('2025-04-28', 'ES PT FR', 'Apagão ibérico (Espanha e Portugal sem luz)', 'apagão'),
 ('2025-06-22', '*', 'EUA bombardeiam o Irã (guerra de 12 dias)', None),
 ('2025-09-10', 'PL LT LV EE', 'Drones russos derrubados sobre a Polônia', None),
 ('2025-09-24', 'DK NO', 'Drones fecham aeroportos na Dinamarca', None),
 ('2025-11-05', 'BE', 'Drones sobre aeroportos e bases na Bélgica', None),
 ('2025-11-16', 'NL', 'Campanha "Denk vooruit" (noodpakket)', 'Holanda'),
 ('2025-11-20', 'FR', 'Guia "Tous responsables" do governo francês', 'Tous responsables'),
 ('2025-11-25', 'CZ', 'Manual "72 hodin" enviado a 5,2 mi de casas', 'Tchéquia'),
 ('2026-03-01', '*', 'Guerra EUA/Israel x Irã e fechamento de Ormuz (28/02 e 02/03)', 'Irã'),
 ('2026-03-05', 'EE LV FI', 'Novos folhetos de preparação de Estônia, Letônia e Finlândia', 'folhetos 2026'),
 ('2026-03-24', 'LT LV EE', 'Drones caem na Lituânia, Letônia e Estônia', 'drones bálticos'),
 ('2025-12-23', 'RO MD', 'RO-Alert manda Tulcea e Galați se abrigar', 'Romênia'),
 ('2026-04-25', 'RO MD', 'Destroços de drone em Galați e Tulcea; evacuação', 'Romênia'),
 ('2026-05-21', 'LV EE LT', 'Letônia: alerta de drone em 3 municípios e queda do governo (14/05)', 'Letônia'),
 ('2026-05-29', 'RO MD BG', 'Drone russo atinge prédio em Galați (2 feridos)', 'Romênia'),
 ('2026-08-14', 'LV EE LT', 'OTAN derruba drone sobre a Letônia', 'Letônia'),
 ('2026-09-01', 'LV EE LT FI', 'Ordem de abrigo nas fronteiras da Letônia e da Estônia por drones', 'Letônia'),
 ('2026-04-03', 'PL', 'Polônia decola caças com ataque russo à Ucrânia', 'Polônia'),
 ('2026-05-13', 'PL RO MD SK', 'Ataque russo com 800 drones após cessar-fogo; Polônia em alerta', 'Polônia'),
 ('2026-03-10', 'BG', 'Bulgária: só 18 dos 247 abrigos prontos', 'Bulgária'),
 ('2026-09-16', 'PL', 'Polônia fecha aeroportos de Lublin e Rzeszów por drones', 'Polônia'),
 ('2026-04-15', 'BE', 'Bélgica lança "Prêts. Ensemble / Samen voorbereid"', 'Bélgica'),
 ('2026-05-22', 'DE', 'Alemanha aprova pacto de proteção civil de 10 bi €', 'Alemanha'),
 ('2026-09-10', 'RO MD PL', 'Drones russos na Romênia e na Moldávia', 'Romênia'),
 ('2026-09-24', 'PL ES FR IT RO MD', 'Guia polonês de ataque aéreo; alerta da CIA sobre drones no sul', 'Polônia'),
 ('2026-10-01', 'BE', 'Guia prático belga de 72 h', 'Bélgica'),
 ('2026-10-22', 'GB IE', 'Be Ready no Reino Unido (3 dias)', 'Be Ready'),
 ('2026-10-27', 'FR', 'Normandia pede kit de 3 dias; Newsweek "33 países"', 'Normandia'),
 ('2026-11-03', '*', 'Comissão Europeia publica diretrizes de 72 h', 'UE 03/11'),
 ('2026-11-10', 'IT GR ES PT', 'Onda de matérias sobre o kit da UE (Itália, Grécia, Espanha)', 'Itália'),
 ('2026-11-11', 'LT LV EE FI PL', 'Alertas de abrigo por drones nos Bálticos', 'drones 11/11'),
]
EV = [(dt.date.fromisoformat(d), set(p.split()) if p != '*' else {'*'}, t, f) for d, p, t, f in EV]
def causa(g, dia, janela=12):
    best = None
    for d, ps, t, f in EV:
        if '*' not in ps and g not in ps: continue
        dd = abs((dia - d).days)
        if dd <= (janela + 9 if g in ps else janela):
            peso = dd - (6 if g in ps else 0)   # evento do próprio país ganha prioridade
            if best is None or peso < best[0]: best = (peso, d, t)
    return (best[2], str(best[1])) if best else (None, None)
def picos(datas, v, k=6, viz=4, minimo=3):
    mx = max(v) if v else 0
    if mx < minimo: return []
    cand = [i for i in range(len(v)) if v[i] >= max(minimo, 0.3 * mx) and v[i] == max(v[max(0, i - viz):i + viz + 1])]
    cand.sort(key=lambda i: -v[i])
    out, usados = [], []
    for i in cand:
        if any(abs(i - j) <= viz for j in usados): continue
        usados.append(i); out.append(i)
        if len(out) >= k: break
    return sorted(out)
res = {'gerado_em': '2026-11-16', 'metodo': 'Google Trends, tópicos que independem de idioma (Survival kit, Survivalism, Bomb shelter, Emergency management = "preparação"; World War III = "medo de guerra"), 5 anos semanal e 90 dias diário por país. Pico = semana que é a maior da vizinhança de 4 semanas e passa de 30% do máximo do país. Índice 0 a 100 é relativo dentro de cada país.', 'paises': [], 'momentos': []}
for g, o in T['serie_5a'].items():
    s = o.get('serie') or {}
    if not s: res['paises'].append({'pais': g, 'nome': NOME.get(g, g), 'sem_dados': True}); continue
    ks = sorted(s); idx = {n: i for i, n in enumerate(o['nomes'])}
    prep = [sum(s[k][idx[n]] for n in ('survival_kit', 'survivalism', 'bomb_shelter', 'emergency_management')) for k in ks]
    war = [s[k][idx['world_war_iii']] for k in ks]
    base = st.mean(prep[:-12]) if len(prep) > 20 else 0
    ult12 = st.mean(prep[-12:]); ult4 = prep[-4:]
    mom = round(ult12 / base, 1) if base >= 0.5 else None
    mxp = max(prep) or 1
    pk = picos(ks, prep); pkw = picos(ks, war, k=3)
    lista = []
    for i in pk:
        d = dt.date.fromisoformat(ks[i]) + dt.timedelta(days=3)
        c, cd = causa(g, d)
        lista.append({'semana': ks[i], 'indice': round(100 * prep[i] / mxp), 'causa': c, 'data_causa': cd})
        res['momentos'].append({'pais': g, 'nome': NOME.get(g, g), 'semana': ks[i], 'indice': round(100 * prep[i] / mxp), 'causa': c, 'tipo': 'preparação'})
    guerra = []
    for i in pkw:
        d = dt.date.fromisoformat(ks[i]) + dt.timedelta(days=3); c, cd = causa(g, d)
        guerra.append({'semana': ks[i], 'indice': war[i], 'causa': c})
    # 90 dias: dia exato do pico
    s9 = (T['serie_90d'].get(g) or {}).get('serie') or {}
    dia_pico = None; ult7 = None
    if s9:
        k9 = sorted(s9); i9 = {n: i for i, n in enumerate(T['serie_90d'][g]['nomes'])}
        p9 = [sum(s9[k][i9[n]] for n in ('survival_kit', 'survivalism', 'bomb_shelter', 'emergency_management')) for k in k9]
        if max(p9) > 0:
            j = max(range(len(p9)), key=lambda i: p9[i])
            c, cd = causa(g, dt.date.fromisoformat(k9[j]), janela=6)
            dia_pico = {'dia': k9[j], 'causa': c}
            ult7 = round(100 * st.mean(p9[-7:]) / max(p9))
    ultimo_pico = lista[-1]['semana'] if lista else None
    agora = bool(ultimo_pico and ultimo_pico >= '2026-09-01')
    d90 = (dia_pico or {}).get('dia') or ''
    vb = max(prep) < 6 or (sum(1 for x in prep if x == 0) > 0.5 * len(prep) and (POP.get(g) or 0) < 20)
    if d90 >= '2026-10-15' and (ult7 or 0) >= 30: sit = 'em alta agora'
    elif (ultimo_pico or '') >= '2026-09-01' or d90 >= '2026-09-01': sit = 'subiu e esfriou' if (ult7 or 0) < 30 else 'em alta agora'
    elif any(x['semana'] >= '2026-01-01' for x in lista): sit = 'subiu em 2026'
    else: sit = 'estável'
    if vb and sit != 'em alta agora': sit = 'volume baixo'
    res['paises'].append({'situacao': sit, 'pais': g, 'nome': NOME.get(g, g), 'idioma': IDI.get(g), 'pop_mi': POP.get(g), 'volume_baixo': max(prep) < 6 or (sum(1 for x in prep if x == 0) > 0.5 * len(prep) and (POP.get(g) or 0) < 20),
                          'momento_12s': mom, 'ult4': ult4, 'pico_5a': ks[prep.index(max(prep))], 'picos': lista, 'picos_guerra': guerra,
                          'dia_pico_90d': dia_pico, 'ultimos7_vs_pico90': ult7, 'em_alta_agora': agora})
# termos locais (16 países)
loc = {}
for g, o in T.get('serie_local', {}).items():
    s = o.get('serie') or {}
    if not s: continue
    ks = sorted(s); linhas = []
    for j, t in enumerate(o['termos']):
        v = [s[k][j] for k in ks]
        if max(v) < 3: linhas.append({'termo': t, 'sem_volume': True}); continue
        base = st.mean(v[:-12]) or 0
        linhas.append({'termo': t, 'pico': ks[v.index(max(v))], 'momento_12s': round(st.mean(v[-12:]) / base, 1) if base else None, 'ult4': v[-4:]})
    loc[g] = linhas
res['termos_locais'] = loc
res['momentos'].sort(key=lambda m: m['semana'])
# agrupa momentos por acontecimento
grupo = {}
for m in res['momentos']:
    grupo.setdefault(m['causa'] or 'sem notícia ligada (a investigar)', []).append(m)
res['por_acontecimento'] = [{'causa': c, 'paises': sorted({x['nome'] for x in L}), 'semanas': sorted({x['semana'] for x in L}), 'n': len(L)} for c, L in sorted(grupo.items(), key=lambda kv: min(x['semana'] for x in kv[1]))]
json.dump(res, open(D + 'trends/momentos-europa.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for p in res['paises']:
    if p.get('sem_dados'): print(p['pais'], 'sem dados'); continue
    print(p['pais'], 'mom', p['momento_12s'], 'agora', p['em_alta_agora'], 'dia90', p['dia_pico_90d'], '|', [(x['semana'], x['indice'], (x['causa'] or '?')[:30]) for x in p['picos']])
