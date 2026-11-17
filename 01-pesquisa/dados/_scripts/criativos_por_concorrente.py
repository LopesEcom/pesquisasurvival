# Separa os anúncios por concorrente (EUA + Europa), escolhe até 8 criativos diferentes de cada um
# (4 mais antigos no ar + 4 mais novos) e baixa cada concorrente na sua própria pasta.
import json, os, re, subprocess, sys, datetime as dt
sys.stdout.reconfigure(encoding='utf-8')
D = r"E:/Raio-X Survival Europa/01-pesquisa/dados/"
OUT = D + "criativos-concorrentes/"
BAIXAR = os.path.expanduser('~/.claude/skills/raio-x-infoprodutos/scripts/baixar-criativos.mjs')
T = dt.date(2026, 11, 16)
ads = []
for f, regiao in [('biblioteca/mineracao-survival-eua.json', 'EUA'), ('biblioteca/europa/mineracao-survival-europa.json', 'Europa')]:
    for a in json.load(open(D + f, encoding='utf-8')):
        a['_regiao'] = regiao; ads.append(a)
por = {}
for a in ads: por.setdefault(a['pageId'], []).append(a)
slug = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:40]
indice = []
for pid, L in por.items():
    L = [a for a in L if a.get('startDate') and ((a.get('imageUrls') or [None])[0] or (a.get('videoUrls') or [None])[0])]
    if not L: continue
    vistos, uni = set(), []
    for a in sorted(L, key=lambda a: a['startDate']):
        mid = ((a.get('videoUrls') or a.get('imageUrls') or [''])[0] or '').split('?')[0].rsplit('/', 1)[-1]
        k = mid or re.sub(r'\W+', '', ((a.get('title') or '') + (a.get('bodyText') or '')[:80]).lower())[:90]
        if k in vistos: continue
        vistos.add(k); uni.append(a)
    sel = uni[:4] + [a for a in uni[-4:] if a not in uni[:4]]
    nome = L[0]['pageName']; s = slug(nome) or pid
    pasta = OUT + s
    os.makedirs(pasta, exist_ok=True)
    json.dump([{**a, 'title': (a.get('title') or '') + ' [' + a['adArchiveId'][-5:] + ']'} for a in sel], open(pasta + '/selecao.json', 'w', encoding='utf-8'), ensure_ascii=False)
    indice.append({'page_id': pid, 'pagina': nome, 'slug': s, 'regiao': L[0]['_regiao'], 'anuncios_na_amostra': len(L), 'criativos_diferentes': len(uni), 'selecionados': len(sel)})
json.dump(indice, open(OUT + 'indice.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(indice), 'concorrentes', sum(i['selecionados'] for i in indice), 'criativos')
if '--baixar' in sys.argv:
    for i in indice:
        pasta = OUT + i['slug']
        man = pasta + '/paginas/criativos/manifesto.json'
        if os.path.exists(man) and len(json.load(open(man, encoding='utf-8')).get('criativos', [])) >= i['selecionados']: continue
        r = subprocess.run(['node', BAIXAR, '--dados', pasta + '/selecao.json', '--out', pasta, '--top', '8'], capture_output=True, text=True, encoding='utf-8', errors='replace')
        print(i['pagina'], '|', (r.stdout.strip().splitlines() or ['?'])[-1], flush=True)
    print('FIM')
