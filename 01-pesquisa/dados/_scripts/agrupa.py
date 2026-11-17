import json,glob,collections,re,datetime as dt,sys
sys.stdout.reconfigure(encoding='utf-8')
ads=json.load(open(sys.argv[1],encoding='utf-8'))
today=dt.date(2026,11,16)
rx=re.compile(r"surviv|prepp|grid|\bemp\b|blackout|stockpil|shortage|collapse|crisis|self[- ]suffic|off[- ]grid|food storage|shelf life|bunker|nuclear|\bwar\b|amish|lost (ways|skills|foods|book)|homestead|depression|famine|power outage|emergency|notfall|krise|stromausfall|survie|urgence|supervivencia|emergencia|sopravvivenza|ewakua|przetrw|noodpakket|kris|72",re.I)
noise=re.compile(r"itunes|play\.google|apps\.apple|kindle|netflix|drama|novel|PLAY_GAME|INSTALL",re.I)
pg=collections.defaultdict(lambda:{'n':0,'dom':collections.Counter(),'start':[],'tit':collections.Counter(),'fmt':collections.Counter(),'rel':0,'ids':[]})
for a in ads:
    p=pg[(a['pageId'],a['pageName'])]
    p['n']+=1; p['ids'].append(a['adArchiveId'])
    if a.get('linkDomain'): p['dom'][a['linkDomain']]+=1
    if a.get('startDate'): p['start'].append(a['startDate'])
    p['tit'][(a.get('title') or a.get('bodyText') or '')[:70]]+=1; p['fmt'][a.get('displayFormat')]+=1
    t=' '.join(str(a.get(k) or '') for k in ('bodyText','title','linkDescription'))
    if rx.search(t) and not noise.search(str(a.get('linkDomain'))+str(a.get('ctaType'))): p['rel']+=1
rows=[]
for (pid,name),p in pg.items():
    if p['rel']<int(sys.argv[2] if len(sys.argv)>2 else 2): continue
    old=min(p['start']) if p['start'] else None
    dias=(today-dt.date.fromisoformat(old)).days if old else None
    rows.append(dict(rel=p['rel'],page_id=pid,pagina=name,n=p['n'],dias=dias,inicio=old,dominios=dict(p['dom'].most_common(3)),fmt=dict(p['fmt']),titulo=p['tit'].most_common(1)[0][0]))
rows.sort(key=lambda r:-r['rel'])
for r in rows[:int(sys.argv[3]) if len(sys.argv)>3 else 70]: print(r['rel'],r['page_id'],r['pagina'][:30],r['n'],r['dias'],r['dominios'],r['fmt'],r['titulo'][:60])
json.dump(rows,open(sys.argv[1].replace('mineracao-','paginas-'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
