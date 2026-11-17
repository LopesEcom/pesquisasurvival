# Monta as telas das 7 etapas (padrão visual do estilo.css da raio-x) e liga no menu de todas as telas.
import json, os, re, shutil, hashlib, html, sys, glob, datetime as dt
sys.stdout.reconfigure(encoding='utf-8')
H = r"E:/Raio-X Survival Europa/01-pesquisa/"
D = H + "dados/"
PG = H + "paginas/"
IMG = PG + "img/"
os.makedirs(IMG, exist_ok=True)
J = lambda f: json.load(open(D + f, encoding='utf-8'))
esc = lambda s: html.escape(str(s if s is not None else ''), quote=True)
def n(v, d=0):
    if v is None: return '–'
    s = f"{v:,.{d}f}"
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')
def img(rel):
    src = rel if os.path.isabs(rel) else D + rel
    if not os.path.exists(src): return None
    h = hashlib.md5(rel.encode()).hexdigest()[:6]
    nome = 'et-' + h + '-' + os.path.basename(src)[-28:]
    dst = IMG + nome
    if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst) or os.path.getsize(src) != os.path.getsize(dst): shutil.copyfile(src, dst)
    return 'img/' + nome
def link(t, u): return f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(t)} ↗</a>' if u else esc(t)
def btn(t, u, cls='sm ghost', ext=True): return f'<a class="btn {cls}" href="{esc(u)}"' + (' target="_blank" rel="noopener"' if ext else '') + f'>{t}' + (' <span class="ar">↗</span>' if ext else '') + '</a>'
def pill(t, c='n'): return f'<span class="pill {c}">{esc(t)}</span>'
NAT = {'obs': 'observado', 'calc': 'calculado', 'inf': 'inferido', 'rec': 'recomendado'}
def nat(k): return f'<span class="nat {k}">{NAT[k]}</span>'
def note(h, c='', eb=''): return f'<div class="note {c}">' + (f'<span class="eyebrow {c}">{esc(eb)}</span>' if eb else '') + h + '</div>'
def table(head, rows): return '<div class="tbl"><table><thead><tr>' + ''.join(f'<th{" class=\"num\"" if h.startswith("#") else ""}>{h.lstrip("#")}</th>' for h in head) + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'
def tr(cells): return '<tr>' + ''.join(cells) + '</tr>'
def td(v, cls=''): return f'<td{" class=\"" + cls + "\"" if cls else ""}>{v}</td>'
def sec(i, num, t, inner, lead=''): return f'<section class="blk" id="{i}"><h2><span class="n">{num}</span>{t}</h2>' + (f'<p class="lead">{lead}</p>' if lead else '') + inner + '</section>'
def stat(v, l, d, k='obs', src=''): return f'<div class="stat"><div class="v">{v}</div><div class="l">{esc(l)}</div><div class="d">{esc(d)}</div><div>{nat(k)}' + (f' <small>· {esc(src)}</small>' if src else '') + '</div></div>'
def head(eb, h1, ans, meta=()): return f'<header class="ph"><span class="eyebrow">{eb}</span><h1>{h1}</h1><p class="answer">{ans}</p>' + ('<div class="meta">' + ''.join(f'<span>{m}</span>' for m in meta) + '</div>' if meta else '') + '</header>'
def toc(items): return '<nav class="toc" aria-label="Nesta tela">' + ''.join(f'<a href="#{a}">{b}</a>' for a, b in items) + '</nav>'
def dmy(iso): return f"{iso[8:10]}/{iso[5:7]}/{iso[:4]}" if iso else '–'
LIB = lambda pid: f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&view_all_page_id={pid}&search_type=page&media_type=all"

# ------------------------------------------------------------------ menu das etapas
ETAPAS = [
 ('etapas', 'etapas.html', 'Roteiro das 7 etapas', '00'),
 ('e1', 'etapa-1-noticias.html', 'Etapa 1 · Notícias', 'E1'),
 ('e1b', 'fontes.html', '↳ Todas as fontes', 'E1.1'),
 ('e2', 'etapa-2-demanda.html', 'Etapa 2 · Procura por país', 'E2'),
 ('e2b', 'etapa-2-europa.html', '↳ A Europa toda', 'E2.1'),
 ('e3', 'voz-do-publico.html', 'Etapa 3 · O que as pessoas dizem', 'E3'),
 ('e4', 'etapa-4-concorrentes.html', 'Etapa 4 · Concorrentes', 'E4'),
 ('e4b', 'criativos-por-concorrente.html', '↳ Anúncios por concorrente', 'E4.1'),
 ('e5', 'etapa-5-funis.html', 'Etapa 5 · Páginas de vendas por dentro', 'E5'),
 ('e6', 'etapa-6-cpm.html', 'Etapa 6 · Quanto custa anunciar', 'E6'),
 ('e7', 'escolha-oferta.html', 'Etapa 7 · Escolha', 'E7'),
]
def bloco_menu(prefix='', atual=''):
    s = '<div class="grp">Etapas da pesquisa</div>'
    for i, f, l, k in ETAPAS:
        sub = l.startswith('↳')
        s += f'<a class="{"sub " if sub else ""}{"on" if atual == f else ""}" href="{prefix}{f}"><span class="dot"></span>{l.lstrip("↳ ")}<span class="k">{k}</span></a>'
    return s

shell = open(PG + 'validacao.html', encoding='utf-8').read()
def pagina(arquivo, titulo, code, corpo, prox=None):
    h = shell
    h = re.sub(r'<title>.*?</title>', f'<title>{esc(titulo)} · Survival Europa</title>', h, flags=re.S)
    h = h.replace('class="on" href="validacao.html"', 'class="" href="validacao.html"')
    h = re.sub(r'<span class="code">TELA<b>.*?</b></span>', f'<span class="code">TELA<b>{code}</b></span>', h)
    h = re.sub(r'<span class="title">.*?</span>', f'<span class="title">{esc(titulo)}</span>', h, count=1)
    i = h.find('<main class="page">') + len('<main class="page">'); j = h.find('<footer class="foot">')
    nxt = ''
    if prox: nxt = f'<div class="next-action"><span class="eyebrow">Próxima etapa</span><div class="tx">{prox[0]}<small>{prox[1]}</small></div>{btn(prox[2], prox[3], "primary", False)}</div>'
    h = h[:i] + corpo + nxt + h[j:]
    open(PG + arquivo, 'w', encoding='utf-8').write(h.replace('—', ','))

# ------------------------------------------------------------------ dados
noticias = J('noticias.json')
vids = J('organico/videos.json')['videos']
tr_ = J('trends/resumo-paises.json')['paises']
cpm = J('cpm-verba.json'); cpmraw = J('cpm.json')
cont = J('biblioteca/contagens-paginas.json')['paginas']
met = J('biblioteca/metricas-paginas.json')
alc = {**J('biblioteca/alcance-ue.json'), **J('biblioteca/alcance-ue-europa.json')}
ads_us = {a['adArchiveId']: a for a in J('biblioteca/mineracao-survival-eua.json')}
ads_eu = {a['adArchiveId']: a for a in J('biblioteca/europa/mineracao-survival-europa.json')}
NOME = {'GB': 'Reino Unido', 'IE': 'Irlanda', 'DE': 'Alemanha', 'AT': 'Áustria', 'CH': 'Suíça', 'NL': 'Holanda', 'BE': 'Bélgica', 'FR': 'França', 'ES': 'Espanha', 'PT': 'Portugal', 'IT': 'Itália', 'PL': 'Polônia', 'LT': 'Lituânia', 'LV': 'Letônia', 'EE': 'Estônia', 'FI': 'Finlândia', 'SE': 'Suécia', 'NO': 'Noruega', 'DK': 'Dinamarca', 'CZ': 'Tchéquia', 'RO': 'Romênia', 'GR': 'Grécia', 'HU': 'Hungria', 'US': 'EUA', 'CA': 'Canadá', 'AU': 'Austrália'}
TIER = {'GB': ('1', 'g', 'Testar primeiro'), 'ES': ('1', 'g', 'Testar primeiro'), 'IE': ('2', 'g', 'Junto com o RU'), 'FR': ('2', 'a', 'Segunda onda'), 'IT': ('2', 'a', 'Segunda onda'), 'PT': ('2', 'a', 'Segunda onda (idioma seu)'),
        'DE': ('3', 'a', 'Depois de validar'), 'NL': ('3', 'n', 'Observar'), 'BE': ('3', 'n', 'Observar'), 'AT': ('3', 'n', 'Junto com a DE'), 'PL': ('3', 'n', 'Observar'), 'SE': ('3', 'n', 'Observar'), 'FI': ('3', 'n', 'Observar'), 'LT': ('3', 'r', 'Não priorizar'), 'US': ('ref', 'n', 'Referência')}

# ------------------------------------------------------------------ ETAPA 1
nt = noticias['noticias']
rows = [tr([td(esc(x['data'])), td(esc(x['pais'])), td('<b>' + esc(x['tema']) + '</b>'), td(esc(x['resumo'])), td(' · '.join(link('fonte ' + str(k + 1), u) for k, u in enumerate(x['fontes'])))]) for x in nt]
NEWS = re.compile(r'BBC|metrouk|abc\.es|509stories|masdak|cbsnews|10 News|LBC|CBS|Wall Street|Firstpost|India Today|bfmtv|60 Minutes|BFBS|Be Prepared UK|Kanał Zero', re.I)
nv = sorted([v for v in vids if NEWS.search(v.get('autor') or '')], key=lambda v: -(v.get('views') or 0))[:14]
rows_v = [tr([td(esc(v['plataforma'])), td('<b>' + esc(v['autor']) + '</b>'), td(esc((v.get('descricao') or v.get('titulo') or '')[:150])), td(n(v.get('views')), 'num'), td(n(v.get('comentarios')), 'num'), td(dmy(v.get('data')))]) + '' for v in nv]
rows_v = [r.replace('</tr>', f'<td>{link("abrir", v["url"])}</td></tr>') for r, v in zip(rows_v, nv)]
corpo = head('Etapa 1 · contexto', 'O que está <em>acontecendo</em> e o que é exagero',
  'Não achei fonte oficial dizendo que a Rússia vai atacar a Lituânia. O que move a procura são as campanhas oficiais de 72 horas (UE em 03/11, Reino Unido em 22/10, França desde 2025) e os alertas de inteligência sobre ações limitadas nos Bálticos até 2029.',
  ['coleta 16/11/2026', '11 notícias com fonte', f'{len(nv)} vídeos de notícia'])
corpo += toc([('linha', 'Linha do tempo'), ('videos', 'Vídeos de notícia'), ('uso', 'Como usar na oferta')])
corpo += '<div class="stats">' + stat('03/11/2026', 'novo guia de estoque da Comissão Europeia', '72 h, cerca de 6 litros de água por pessoa', 'obs', 'Insider Paper') + stat('22/10/2026', 'Be Ready no Reino Unido', 'preparar a casa para 3 dias sem serviços', 'obs', 'gov.uk') + stat('6,4 mi', 'views da BBC sobre a corrida aos estoques', '27/10/2026', 'obs', 'YouTube') + stat('0', 'fonte oficial de ataque iminente à Lituânia', 'BND: ação limitada possível nos Bálticos', 'obs', 'buscas 16/11') + '</div>'
corpo += sec('linha', '01', 'Linha do tempo das notícias', table(['Data', 'País', 'Tema', 'O que diz', 'Fontes'], rows), 'Tudo com link. Onde a fonte é fraca (blog, site partidário) a notícia não entrou como fato.')
corpo += sec('videos', '02', 'Vídeos de notícia mais vistos', table(['Rede', 'Canal', 'Assunto', '#Views', '#Coment.', 'Data', 'Link'], rows_v), 'TikTok e YouTube, buscados em 10 termos e 7 idiomas. As notícias de março de 2025 (kit de 72 h da UE) seguem circulando e as de outubro e novembro de 2026 (RU, BBC) são as mais vistas agora.')
corpo += sec('uso', '03', 'Como usar isso na oferta', note('<b>Use a campanha oficial como prova, não a guerra como promessa.</b> Os advertoriais que escalam na Europa abrem com "o governo mandou as famílias se prepararem" (Ready Families no RU, BlackoutReport na Alemanha citando a UE). Isso é verificável e passa na política de anúncios. "A Rússia vai atacar" não tem fonte oficial, o público rejeita ("This needs to stop. They want us living fear!", 16 mil curtidas) e cai em anúncio de tema social na Meta.', 'g', 'recomendado') +
  note('A Lituânia é o gatilho da notícia, mas quase não busca o tema (país de 2,9 milhões de pessoas, buscas estáveis desde 2022). O dinheiro está nos países grandes que estão no pico agora (Etapa 2).', 'a', 'atenção'))
pagina('etapa-1-noticias.html', 'Etapa 1 · Notícias', 'E1', corpo, ('Ver quais países estão buscando agora', 'Google Trends + TikTok por país', 'Etapa 2', 'etapa-2-demanda.html'))

# ------------------------------------------------------------------ ETAPA 2
ordem = ['GB', 'ES', 'IE', 'FR', 'IT', 'PT', 'DE', 'AT', 'NL', 'BE', 'PL', 'SE', 'FI', 'LT', 'US']
tm = {t['pais']: t for t in tr_}
cpmP = {c['pais']: c for c in cpm['paises']}
rows = []
for g in ordem:
    t = tm.get(g);
    if not t: continue
    lt = t.get('termo_local_mais_forte') or {}
    tier = TIER.get(g, ('3', 'n', ''))
    rows.append(tr([td(f'<b>{NOME[g]}</b>'), td(esc(t['idioma'])), td(n(t['pop_mi'], 1), 'num'), td(n(t['topico_kit_momento'], 1) + 'x', 'num'), td(dmy(t['topico_kit_pico'])), td(esc(', '.join(map(str, t['ult4'])))),
                    td(esc(lt.get('termo', '–')) + (f' <small>({n(lt.get("momento"), 1)}x, pico {dmy(lt.get("pico"))})</small>' if lt else '')), td(n(cpmP.get(g, {}).get('cpm_eur'), 2) + ' €', 'num'), td(pill(('Tier ' + tier[0]) if tier[0] != 'ref' else 'ref', tier[1]) + ' ' + esc(tier[2]))]))
reg = J('trends/trends.json')['regioes']
def top_reg(k):
    v = reg.get(k) or {}; return ', '.join(f'{NOME.get(a, a)} {b}' for a, b in sorted(v.items(), key=lambda x: -x[1])[:8])
LANG = [('Inglês (RU, IE)', r'emergency|72 hour|prepper|stockpile|survival kit|uk', ['tiktok', 'youtube']), ('Espanhol', r'supervivencia|emergencia|72 horas|mochila', None), ('Francês', r'survie|urgence|guerre', None), ('Alemão', r'notfall|stromausfall|krise', None), ('Português', r'sobreviv|emergência|kit', None), ('Polonês', r'plecak|ewakuac', None)]
lv = []
for nome_l, rx, _ in LANG:
    vs = sorted([v for v in vids if re.search(rx, (v.get('termo') or '') + ' ' + (v.get('descricao') or ''), re.I)], key=lambda v: -(v.get('views') or 0))[:3]
    for v in vs: lv.append(tr([td(f'<b>{nome_l}</b>'), td(esc(v['autor'])), td(esc((v.get('descricao') or '')[:110])), td(n(v.get('views')), 'num'), td(n(v.get('salvos')) if v.get('salvos') else '–', 'num'), td(dmy(v.get('data'))), td(link('abrir', v['url']))]))
corpo = head('Etapa 2 · demanda', 'Quais países estão <em>buscando agora</em>',
  'Reino Unido, Irlanda e Itália estão no pico de 5 anos neste outono; a Espanha está subindo nesta semana; a França teve pico em 25/10. Alemanha, Polônia e nórdicos buscam, mas estão estáveis desde 2022 (já se acostumaram ao tema); a Lituânia tem volume tão baixo que o índice oscila entre 0 e 12.',
  ['Google Trends, 5 anos, semanal', '27 países no ranking por tópico', '60 termos locais em 12 países', '120 vídeos'])
corpo += toc([('ranking', 'Ranking por país'), ('topico', 'Interesse por tópico'), ('tiktok', 'TikTok e YouTube por idioma'), ('leitura', 'Leitura')])
corpo += '<div class="stats">' + stat('17x', 'Irlanda: busca de kit acima da média de 5 anos', 'pico em 08/11/2026', 'calc', 'Trends') + stat('4,4x', 'Reino Unido: pico de 5 anos', 'semana de 25/10/2026, depois do Be Ready', 'calc', 'Trends') + stat('15x', 'Espanha: "mochila de emergencia"', 'pico em 15/11/2026 (esta semana)', 'calc', 'Trends') + stat('83x', 'Itália: "kit di emergenza"', 'pico em 08/11/2026', 'calc', 'Trends') + '</div>'
corpo += sec('ranking', '01', 'Ranking dos países', table(['País', 'Idioma', '#Pop. (mi)', '#Momento', 'Pico do tópico', 'Últimas 4 semanas', 'Termo local mais forte', '#CPM', 'Decisão'], rows),
  'Momento = média das últimas 12 semanas dividida pela média dos 5 anos anteriores (tópico "Survival kit" do Google, que junta todos os idiomas). Acima de 2x é demanda nova. O CPM vem da Etapa 6.')
corpo += sec('topico', '02', 'Interesse relativo por tópico (índice 0 a 100)', '<div class="grid g2">' + ''.join(f'<div class="card"><span class="eyebrow">{a}</span><p>{esc(top_reg(b))}</p></div>' for a, b in [('Survival kit · 12 meses', 'survival_kit|today 12-m'), ('Survival kit · 3 meses', 'survival_kit|today 3-m'), ('Survivalismo · 12 meses', 'survivalism|today 12-m'), ('Prepper · 12 meses', 'prepper|today 12-m')]) + '</div>',
  'Índice proporcional ao tamanho de cada país: mostra onde o tema pesa mais na busca, não o volume absoluto. A Holanda lidera "survival kit" por causa da campanha "Denk vooruit" (noodpakket); Dinamarca e Noruega lideram "survivalismo"; Alemanha e Áustria lideram "prepper".')
corpo += sec('tiktok', '03', 'O que viraliza por idioma', table(['Idioma', 'Perfil', 'Vídeo', '#Views', '#Salvos', 'Data', 'Link'], lv), 'Salvamentos (só no TikTok) são o melhor sinal de intenção: quem salva quer fazer depois.')
corpo += sec('leitura', '04', 'Leitura', note('<b>Ordem de entrada sugerida:</b> 1) Reino Unido + Irlanda em inglês (pico agora, funil americano modelável quase direto, concorrentes americanos já testando lá); 2) Espanha (subindo nesta semana, apagão de 2025 na memória, CPM barato); 3) França, Itália e Portugal; 4) Alemanha só depois de validar (cultura prepper forte, mas CPM alto e muito produto físico).', 'g', 'recomendado') +
  note('Lituânia, Letônia, Estônia, Polônia e nórdicos: o medo é real, mas a busca não cresceu em 2026 (estável desde a invasão de 2022) e o idioma é pequeno. Não priorizar.', 'a', 'atenção'))
pagina('etapa-2-demanda.html', 'Etapa 2 · Procura por país', 'E2', corpo, ('Ler o que o público pede e do que reclama', '7.634 comentários', 'Etapa 3', 'voz-do-publico.html'))

# ------------------------------------------------------------------ ETAPA 4
def tipo_of(p): return p.get('tipo', '')
rows_us = []
for p in cont:
    pid = p['page_id'].split('+')[0]; mm = met.get(pid, {})
    rows_us.append(tr([td('<b>' + esc(p['pagina']) + '</b>'), td(esc(p.get('dominio', ''))), td(esc(tipo_of(p))), td(n(p.get('ativos')), 'num'), td(n(p.get('historico_all')), 'num'), td(n(mm.get('dias_mais_antigo')), 'num'), td(n(mm.get('novos_7d')), 'num'), td(btn('Biblioteca', LIB(pid)) + (btn('Página', 'https://' + p['dominio']) if p.get('dominio') else ''))]))
EU = [('1241103159077943', 'DE', 'Notfall Kompass', 'advertorial "se você tem filhos ou netos" + filtro de água'), ('311162672720289', 'PL', 'Help Bag', 'mochila de evacuação pronta'), ('1457458994107079', 'FR', 'Aquasecours', 'kit de água'), ('1514193808434156', 'DE/AT', 'BlackoutReport', 'advertorial da UE 72 h + rádio'),
      ('1421560424371386', 'FR', 'Nord Survival', 'kit de 72 h (lista oficial francesa)'), ('947723775092334', 'PL', 'Bezpieczne Radio', 'rádio e mochila'), ('1347986611740847', 'FR', 'Page survie entre français', 'kit de água'), ('544816535383698', 'FR', 'Topdeals (Le Manuel de Survie)', 'PDF 383 páginas'),
      ('793179617219751', 'ES', 'SuperArte (Casa Refugio)', 'PDF imprimível 72 h'), ('1406547739212538', 'GB', 'UK Be Ready', 'advertorial + rádio'), ('1270045722861427', 'GB', 'Ready Families Network', 'advertorial + filtro'), ('1323820117479917', 'DE', 'Krisensicher26', 'mochila 72 h (239,99 €)'),
      ('1154015154457510', 'DE', 'Simone Fischer (Schutzheld)', 'produto de segurança'), ('847142251827090', 'CH/FR/IT', 'Swiss LifeBox', 'rádio e kits'), ('150763148333365', 'IT', 'Survival School Sos2012', 'curso presencial'), ('1385226154670354', 'PL', 'Zolano', 'mochila 92 em 1'), ('1287034351171112', 'NL', 'Hydromeal', 'comida de emergência'), ('1446919845163973', 'ES', 'Búnker en Casa', 'manual (68 anúncios no histórico)')]
rows_eu = []
for pid, pais, nome, tipo in EU:
    mm = met.get(pid, {})
    rows_eu.append(tr([td(esc(pais)), td('<b>' + esc(nome) + '</b>'), td(esc(mm.get('dominio') or '')), td(esc(tipo)), td(n(mm.get('dias_mais_antigo')), 'num'), td(n(mm.get('novos_7d')), 'num'), td(btn('Biblioteca', LIB(pid)) + (btn('Página', 'https://' + mm['dominio']) if mm.get('dominio') else ''))]))
rows_alc = []
allads = {**ads_us, **ads_eu}
for aid, v in alc.items():
    x = v.get('dados') or {}
    ag = {}; m_ = f_ = 0
    for c in x.get('age_country_gender_reach_breakdown', []):
        for a in c['age_gender_breakdowns']:
            s = sum((a.get(k) or 0) for k in ('male', 'female', 'unknown')); ag[a['age_range']] = ag.get(a['age_range'], 0) + s; m_ += a.get('male') or 0; f_ += a.get('female') or 0
    T = sum(ag.values())
    if not T: continue
    pg = (allads.get(aid) or {}).get('pageName') or re.sub(r'.*Buscar por palabra clave o anunciante\s+', '', v.get('trecho', ''))[:30].split(' Anuncios')[0]
    rows_alc.append(tr([td(link(aid, 'https://www.facebook.com/ads/library/?id=' + aid)), td('<b>' + esc(pg) + '</b>'), td(esc(', '.join(l['name'] for l in x.get('location_audience', [])))), td(n(x.get('total_reach') or x.get('eu_total_reach')), 'num'), td(n(100 * (ag.get('55-64', 0) + ag.get('65+', 0)) / T) + '%', 'num'), td(n(100 * f_ / max(1, m_ + f_)) + '%', 'num')]))
def cards(manifesto, base, ads):
    out = []
    for c in manifesto:
        aid = c['adArchiveId']; a = ads.get(aid, {})
        jpg = img(f'{base}/{aid}.jpg'); mp4 = img(f'{base}/{aid}.mp4') if c.get('ehVideo') and os.path.exists(D + f'{base}/{aid}.mp4') else None
        if not jpg: continue
        media = f'<video src="{mp4}" poster="{jpg}" controls muted playsinline preload="none" style="width:100%;height:100%;object-fit:cover;background:#000"></video>' if mp4 else f'<img src="{jpg}" alt="" loading="lazy" style="width:100%;height:100%;object-fit:cover">'
        out.append(f'<article class="ad"><div class="media">{media}<span class="fmt">{"vídeo" if mp4 else "imagem"}</span></div><div class="body"><div class="pg">{esc(c.get("pageName"))}</div><div class="t">“{esc(c.get("title") or (a.get("title") or ""))}”</div><div class="tx">{esc((a.get("bodyText") or "")[:260])}</div><div class="days">{c.get("dias")} dias no ar · desde {dmy(a.get("startDate"))}</div></div><div class="foot">{btn("Anúncio", "https://www.facebook.com/ads/library/?id=" + aid)}{btn("Todos da marca", LIB(a.get("pageId", "")))}{btn("Página", a.get("linkUrl")) if a.get("linkUrl") else ""}</div></article>')
    return '<div class="ads">' + ''.join(out) + '</div>'
man_us = json.load(open(D + 'biblioteca/paginas/criativos/manifesto.json', encoding='utf-8'))
man_us = man_us if isinstance(man_us, list) else man_us.get('criativos', man_us.get('itens', []))
man_eu = json.load(open(D + 'biblioteca/europa/paginas/criativos/manifesto.json', encoding='utf-8'))['criativos']
corpo = head('Etapa 4 · concorrência', 'Todos os <em>concorrentes</em> e os criativos deles',
  f'{len(cont)} funis americanos medidos no conector (até 1.383 anúncios ativos numa página) e {len(EU)} concorrentes europeus, quase todos de produto físico e com 3 a 74 dias no ar. Abaixo, {len(man_us)} criativos americanos e {len(man_eu)} europeus para assistir aqui mesmo.',
  ['Biblioteca de Anúncios 16/11/2026', '1.686 anúncios EUA + 900 Europa extraídos', 'alcance da UE em 16 anúncios'])
corpo += toc([('eua', 'Concorrentes EUA'), ('europa', 'Concorrentes Europa'), ('alcance', 'Alcance na Europa'), ('gal', 'Criativos'), ('anatomia', 'Anatomia')])
corpo += sec('eua', '01', 'Funis americanos (a origem do modelo)', table(['Página', 'Domínio', 'Tipo', '#Ativos', '#Histórico', '#Dias (amostra)', '#Novos 7d', 'Links'], rows_us), 'Ativos e histórico: conector Meta Ads, sem filtro de país. Dias: anúncio ativo mais antigo na amostra extraída (a página pode ser bem mais antiga; os livros da Global Brother trocam o criativo toda semana).')
corpo += sec('europa', '02', 'Concorrentes na Europa', table(['País', 'Página', 'Domínio', 'Produto', '#Dias (amostra)', '#Novos 7d', 'Links'], rows_eu), 'Extração por termo local em 9 países. A onda europeia começou em setembro de 2026 e quase tudo é produto físico. Infoproduto digital: só Casa Refugio (ES), Le Manuel de Survie (FR) e o manual da Búnker en Casa (ES).')
corpo += sec('alcance', '03', 'Quem eles atingem na Europa (transparência da UE)', table(['Anúncio', 'Página', 'País segmentado', '#Alcance', '#55+', '#Mulheres'], rows_alc), 'A Meta mostra o alcance de anúncio veiculado na UE e no RU. The Amish Ways roda campanha só para o Reino Unido; o público de survival na Europa é majoritariamente 55+.')
corpo += sec('gal', '04', 'Criativos organizados por concorrente', note('Os criativos agora ficam numa tela só, separados por grupo e por concorrente, cada um com a ficha (país, produto, funil, anúncios ativos), os vídeos para assistir, o texto do anúncio e a transcrição do começo do vídeo. No Explorador de Arquivos, a mesma organização está em <b>01-pesquisa/criativos-por-concorrente</b>.', 'b', 'nova organização') + '<div class="btns">' + btn('Abrir criativos por concorrente', 'criativos-por-concorrente.html', 'primary', False) + '</div>')
corpo += sec('anatomia', '05', 'Anatomia dos vencedores', note('Gancho, estrutura, objeção, texto na tela e chamada de 5 vencedores estão na tela de criativos.', 'b', 'continua') + '<div class="btns">' + btn('Abrir a anatomia', 'criativos.html#anatomia', 'primary', False) + '</div>')
pagina('etapa-4-concorrentes.html', 'Etapa 4 · Concorrentes', 'E4', corpo, ('Ver cada funil por dentro', 'página, VSL, checkout e upsell', 'Etapa 5', 'etapa-5-funis.html'))

# ------------------------------------------------------------------ ETAPA 5
VSL = [
 ('The Lost SuperFoods', 'Claude Davis', 'https://thelostsuperfoods.com/', '30,7 min', '0k44wnx0ed / om8a7gdxi2', 'Wistia, versão vertical (celular) e horizontal', 'lost-super-foods.txt', 'ofertas/_vsl/thelostsuperfoods-com-topo.jpg', None, 'US$ 27,75 físico+digital; botão "só digital"', '60 dias "honor guarantee"', [
   ('0 a 2', 'Gancho: a supercomida da Guerra Fria que ainda é comestível 60 anos depois (demonstração).'), ('2 a 4', 'Quem fala: avô/avós, "não sou doomsday, preparo como nossos avós".'), ('4 a 5', 'Tese: dinheiro não se come; comida que não estraga vale mais numa crise.'),
   ('5 a 7', 'História: "Fat Boris" na fome de Leningrado (quem guardou comida sobreviveu).'), ('7 a 9', 'Inimigo: ninguém avisa antes da crise; kit de comida de emergência é golpe de 1.200 calorias.'), ('9 a 10', 'Missão: salvar esse conhecimento antes que suma.'),
   ('10 a 22', 'Produto: lista longa de comidas e receitas (fascinações), cada uma com uma história.'), ('23 a 24', 'Bônus: estufa o ano todo e projetos para a casa.'), ('25 a 26', 'Preço e por que barato ("não quero enriquecer"); garantia de honra.'), ('27 a 30', 'Três opções, prova da família, chamada.')]),
 ('A Navy SEAL\'s Bug-In Guide', 'Joel Lambert (ex-SEAL)', 'https://www.buginguide.com/', '31,6 min', 'uqw89w7z6h / ws90ldpp6f', 'Wistia, lead "Great Depression" vertical e horizontal', 'bug-in-guide.txt', 'ofertas/_vsl/buginguide-com-topo.jpg', 'ofertas/_checkouts/buginguide-com-book-checkout.jpg', 'US$ 37 (de 59) + 2 bônus', '2 meses "keep the book"', [
   ('0 a 10', 'História longa: 3 amigos na Grande Depressão; quem se preparou em casa salvou os outros.'), ('10', 'Revelação: "o primeiro guia de bug-in" (ficar em casa, não fugir).'), ('11 a 22', 'Os 10 capítulos da "Life Pie": comida, água, segurança, energia, comunicação, remédios.'),
   ('23', 'Bônus (4 acres, EMP do jeito dos pioneiros).'), ('24', 'Escassez: tiragem pequena de livro impresso.'), ('25', 'Preço, chamada e garantia.'), ('26', 'Objeção: "dá para aprender sozinho" (tempo e dinheiro).'), ('27 a 31', 'Recapitulação dos benefícios e chamada final.')]),
 ('The Lost Skills of Independence', 'Joel Lambert (ex-SEAL)', 'https://www.thelostskillsofindependence.com/', '23,2 min', '24vau4uwr3', 'Wistia', 'lost-skills-independence.txt', 'ofertas/_vsl/thelostskillsofindependence-com-topo.jpg', 'ofertas/_checkouts/thelostskillsofindependence-com-book-checkout.jpg', 'US$ 39 (de 166) + frete 9,99 + 3 livros digitais grátis', '60 dias "keep the book"', [
   ('0 a 2', 'Gancho: "Por que não fazem mais livros assim?" e amostra rápida de habilidades.'), ('2', 'Autoridade: instrutor do BUD/S, missões atrás das linhas inimigas.'), ('3 a 17', 'Tour pelos capítulos com 1 exemplo concreto cada (defumador, ovos que duram, remédio).'),
   ('17', 'Exclusividade: "não está no YouTube nem em lugar nenhum".'), ('18', 'Envio e rastreio.'), ('19 a 22', 'Patriotismo, saqueadores, legado para os filhos.'), ('23', 'Preço e chamada.')]),
 ('The Self-Sufficient Backyard', 'Ron e Johanna', 'https://selfsufficientbackyard.com/', '25,2 min', '469zk3w8t1 / vv23cdo0l2', 'Wistia, VSL de março de 2025 com lead novo de abril', 'self-sufficient-backyard.txt', 'ofertas/_vsl/selfsufficientbackyard-com-topo.jpg', None, 'US$ 37 digital (ClickBank e Digistore24); 3 upsells; até US$ 155,20 por venda', '60 dias', [
   ('0 a 3', 'Promessa: casa que gera dinheiro e não fica sem energia num apagão ou EMP.'), ('3 a 9', 'História: 40 anos fora da rede (cabana, lago no Canadá, terceira casa menor).'), ('10 a 18', 'Tour pelos projetos (1.000 pés quadrados, ervas, energia, água, estufa, pomar).'),
   ('19 a 20', 'Bônus.'), ('21 a 23', 'Preço e "não precisa de terra nem de habilidade".'), ('24 a 25', 'Garantia e despedida.')]),
 ('The Amish Ways', 'Eddie Swartzentruber (ex-Amish)', 'https://www.theamishways.com/', '46,2 min', 'k9tlq8ql20', 'Wistia + 3 vídeos de depoimento (20 a 55 s)', 'amish-ways.txt', 'ofertas/_vsl/theamishways-com-topo.jpg', 'ofertas/_checkouts/theamishways-com-book-checkout.jpg', 'US$ 29,25 (Black Friday); 3 cópias US$ 87; 5 cópias US$ 136,75', '60 dias', [
   ('0 a 2', 'Demonstração: receita do hambúrguer Amish em conserva ("comida de sobrevivência não precisa ter gosto de papelão").'), ('2 a 6', 'Segredos que os Amish não mostram para quem é de fora.'), ('6 a 8', 'Autor ex-Amish.'),
   ('8 a 10', 'Medo: relato de fome com carroça de mortos.'), ('10 a 32', 'Tour longo: geladeira sem energia, ibuprofeno natural, filtro sem energia, escambo, remédios, horta.'), ('33 a 35', '3 presentes (bônus).'), ('36 a 37', 'Preço (US$ 39 com US$ 40 de desconto).'), ('38 a 46', 'Garantia, escassez de impressão, recapitulação e fechamento.')])]
blocos = ''
for nome, autor, url, dur, wid, player, trans, topo, ck, preco, gar, linha in VSL:
    it = img(topo); ci = img(ck) if ck else None
    shots = '<div class="grid g3" style="margin-top:12px">' + (f'<figure class="card" style="margin:0;padding:8px"><img style="width:100%;height:420px;object-fit:cover;object-position:top;border-radius:6px" src="{it}" alt="" loading="lazy"><figcaption>página da VSL (celular)</figcaption></figure>' if it else '') + (f'<figure class="card" style="margin:0;padding:8px"><img style="width:100%;height:420px;object-fit:cover;object-position:top;border-radius:6px" src="{ci}" alt="" loading="lazy"><figcaption>checkout Digistore24</figcaption></figure>' if ci else '') + '</div>'
    tl = table(['Minuto', 'O que acontece'], [tr([td(esc(a)), td(esc(b))]) for a, b in linha])
    blocos += f'<div class="card" style="margin-bottom:18px"><span class="eyebrow">{esc(autor)}</span><h3 style="margin:6px 0">{esc(nome)} {pill(dur, "g")}</h3><div class="kv"><div><b>Página</b> {link(url, url)}</div><div><b>Player</b> {esc(player)} (id {esc(wid)})</div><div><b>Preço</b> {esc(preco)}</div><div><b>Garantia</b> {esc(gar)}</div><div><b>Transcrição</b> {link(trans, "../dados/ofertas/_vsl/transcricoes/" + trans)}</div></div>{tl}{shots}</div>'
quiz = J('ofertas/_quiz/quiz.json')
qhtml = ''
for r in quiz:
    passos = [p for p in r['passos'] if p.get('print')]
    vistos = set(); sel = []
    for p in passos:
        k = (p.get('texto') or '')[:120]
        if k in vistos: continue
        vistos.add(k); sel.append(p)
    qhtml += f'<h3 style="margin:14px 0 6px">{esc(r["url"])}</h3><div class="grid g3">' + ''.join(f'<figure class="card" style="margin:0;padding:8px"><img style="width:100%;height:420px;object-fit:cover;object-position:top;border-radius:6px" src="{img("ofertas/_quiz/" + p["print"])}" alt="" loading="lazy"><figcaption>passo {p["i"]}' + (' · ' + esc(p.get('nota')) if p.get('nota') else '') + '</figcaption></figure>' for p in sel[:6]) + '</div>'
ADV = [('Ready Nation USA', 'guardsurvival.com-pages-advertorial-v3-water-bag', 'EUA', 'história de um parente investigador + bolsa/filtro de água'), ('Blackout Water', 'tryblackoutwater.com-pages-advertorial', 'EUA', '"The Outsider": canudo filtro, 5 unidades 43% off, garantia 365 dias'),
       ('Ready Families Network', 'standbysupplyco.com-pages-uk-household-water-repor', 'RU', 'orientação oficial de 120 litros + filtro "compre 1 leve 2"'), ('UK Be Ready / Helora', 'helorafit.com-pages-uk-emergency-radio-repor', 'RU', 'National Risk Register + rádio de 39,90 a 99,90'),
       ('BlackoutReport', 'blackoutreport.de-72-stunden-vorsorge', 'DE', 'guia da UE de 03/11 + manchetes de apagão + rádio'), ('Notfall Kompass / Virest', 'virest.de-products-hydra-x1-notfall-wass', 'DE', 'filtro HYDRO-X1 19,99 a 359,94 €, 60 dias de garantia'),
       ('Krisensicher26', 'krisensicher26.de', 'DE', 'mochila 72 h pronta 239,99 €'), ('Nord Survival', 'nord-survival.com-products-kit-de-survie-72h', 'FR', 'kit 72 h com a "lista oficial", 3 pacotes'),
       ('Casa Refugio', 'casarefugio.impultienda.ar', 'ES', 'PDF imprimível de 72 h, US$ 14,90 (de 37), garantia 15 dias'), ('Le Manuel de Survie', 'le-manuel-de-survie.impultienda.ar', 'FR', 'PDF 383 páginas + 4 bônus, 29,99, garantia 30 dias'),
       ('4Patriots', 'go.4patriots.com-2200x', 'EUA', 'gerador solar parcelado (menos de US$ 299/mês)'), ('Prepper Disk', 'prepperdisk.com-pages-landing', 'EUA', 'internet offline de 512 GB, US$ 297')]
adv = '<div class="grid g3">' + ''.join(f'<div class="card"><span class="eyebrow">{esc(p)}</span><h3 style="margin:6px 0">{esc(nm)}</h3><p>{esc(ds)}</p>' + (f'<img src="{img("ofertas/" + sl + "/computador.jpg")}" alt="" loading="lazy" style="width:100%;border:1px solid #E4E4E4;border-radius:8px">' if img("ofertas/" + sl + "/computador.jpg") else '') + f'<p><a href="{("oferta-" + sl + ".html") if os.path.exists(PG + "oferta-" + sl + ".html") else "#"}">dossiê</a> · {link("página", json.load(open(D + "ofertas/" + sl + "/pagina.json", encoding="utf-8"))["url"])}</p></div>' for nm, sl, p, ds in ADV) + '</div>'
formula = table(['Etapa do funil', 'O que a rede Global Brother faz (Lost SuperFoods, Bug-In, Lost Skills, Amish Ways)', 'Natureza'], [
  tr([td('<b>1. Anúncio</b>'), td('Vídeo vertical de truque/receita ou imagem da página do livro; texto longo; chamada "Learn more"; 40 a 800 anúncios ativos por livro, trocados toda semana.'), td(nat('obs'))]),
  tr([td('<b>2. Página</b>'), td('URL /book: carta de vendas longa (29 mil a 53 mil px no celular) com a VSL embutida, avaliações "Verified Purchase", "Last Books Available", "Due to recent events... surge in demand", bônus e garantia "keep the book".'), td(nat('obs'))]),
  tr([td('<b>3. VSL</b>'), td('23 a 46 min, Wistia, versão vertical para celular. Lead de história ou demonstração; autoridade (ex-SEAL, ex-Amish, avô); medo histórico (fome, Grande Depressão); tour longo do produto; bônus; preço só nos últimos 20%.'), td(nat('obs'))]),
  tr([td('<b>4. Checkout</b>'), td('Digistore24 (checkout-ds24.com/globalbro): cupom aplicado, cronômetro de 5 min, bônus "grátis" de US$ 29 a 39, seletor de 1/2/3 cópias, Google Pay, cartão e PayPal, frete a parte.'), td(nat('obs'))]),
  tr([td('<b>5. Upsell</b>'), td('Não visível sem comprar. Indícios: SSB tem 3 upgrades (pacote médico, programa ampliado, pacote dos "Lost Books"); Digistore24 cita até US$ 155,20 por venda.'), td(nat('inf'))]),
  tr([td('<b>6. Preço</b>'), td('US$ 27,75 a 39 na entrada (Black Friday); ticket médio informado pela Digistore24 de US$ 58,75 a 64,45.'), td(nat('obs'))])])
corpo = head('Etapa 5 · funis', 'Cada funil <em>por dentro</em>: página, VSL, checkout e upsell',
  '5 VSLs transcritas (23 a 46 minutos), 4 checkouts abertos, 2 funis de quiz percorridos e 12 advertoriais/páginas europeias. Os livros que mais escalam são da mesma rede e seguem a mesma fórmula.',
  ['transcrições completas em dados/ofertas/_vsl/transcricoes', 'checkouts abertos sem comprar', 'quizzes até o e-mail'])
corpo += toc([('formula', 'A fórmula'), ('vsl', 'VSLs minuto a minuto'), ('quiz', 'Funis de quiz'), ('advertorial', 'Advertoriais e páginas europeias'), ('upsell', 'Upsell')])
corpo += sec('formula', '01', 'A fórmula que se repete', formula)
corpo += sec('vsl', '02', 'As 5 VSLs minuto a minuto', blocos, 'Duração medida no Wistia. A linha do tempo é resumo da transcrição (a transcrição inteira fica em dados, para consulta, nunca para copiar).')
corpo += sec('quiz', '03', 'Funis de quiz (livro grátis)', note('Homesteading Secrets: anúncio "você ganhou um livro" → quiz de 5 perguntas ("quão preparado você está?") → vídeo curto → livro grátis. Roy Foley: 3 perguntas → "Congrats! You qualify!" → e-mail → vídeo. Paramos no e-mail (não enviamos dado pessoal); o que é vendido depois é lacuna.', 'b', 'como funciona') + qhtml)
corpo += sec('advertorial', '04', 'Advertoriais e páginas europeias', adv, 'Clique em "dossiê" para a ficha completa de cada um.')
corpo += sec('upsell', '05', 'Upsell e order bump', '<p>Detalhe com links na tela de ofertas validadas.</p><div class="btns">' + btn('Ver upsells', 'ofertas.html#upsells', 'primary', False) + '</div>')
pagina('etapa-5-funis.html', 'Etapa 5 · Páginas de vendas por dentro', 'E5', corpo, ('Ver quanto custa testar em cada país', 'CPM, CPA e verba de teste', 'Etapa 6', 'etapa-6-cpm.html'))

# ------------------------------------------------------------------ ETAPA 6
pr = cpm['premissas']
rows = []
for c in cpm['paises']:
    g = c['pais']; raw = cpmraw['paises'].get(g, [None] * 3)
    rows.append(tr([td(f'<b>{NOME.get(g, g)}</b>'), td(n(raw[0], 2) if raw[0] else '–', 'num'), td(n(raw[1], 2) if raw[1] else '–', 'num'), td(n(raw[2], 2) if raw[2] else '–', 'num'), td('<b>' + n(c['cpm_eur'], 2) + ' €</b>', 'num'),
                    td(f"{n(c['cpa_estimado']['bom'], 0)} / {n(c['cpa_estimado']['medio'], 0)} / {n(c['cpa_estimado']['ruim'], 0)} €", 'num'), td(n(c['verba_dia'], 0) + ' €', 'num'), td(n(c['teste_min'], 0) + ' €', 'num'), td(n(c['teste_seguro'], 0) + ' €', 'num'), td(n(c['impressoes_teste_min']), 'num'),
                    td(pill(('Tier ' + TIER[g][0]) if g in TIER and TIER[g][0] != 'ref' else ('ref' if g in TIER else '–'), TIER.get(g, ('', 'n'))[1]))]))
corpo = head('Etapa 6 · custo', 'CPM, custo por venda e <em>verba de teste</em> por país',
  'Com um front de 37 euros, o teste mínimo é de 333 euros por país (3 criativos, 1 ticket por criativo por dia, 3 dias). O custo por venda estimado vai de cerca de 26 euros (Hungria, Polônia) a 55 euros (Reino Unido); na Espanha fica perto de 33.',
  ['3 fontes de CPM (2026)', 'premissas declaradas', 'régua da /low-ticket e do Ouro VTurb'])
corpo += toc([('tabela', 'Tabela por país'), ('premissas', 'Premissas'), ('regras', 'Regras de corte')])
corpo += '<div class="stats">' + stat('5,94 €', 'CPM mediano na Espanha', 'faixa 5,18 a 7,10', 'calc', '3 fontes') + stat('9,89 €', 'CPM mediano no Reino Unido', 'faixa 9,23 a 10,55', 'calc', '3 fontes') + stat('333 €', 'teste mínimo por país', '3 criativos x 37 € x 3 dias', 'calc', 'régua low-ticket') + stat('740 €', 'teste seguro por país', '5 criativos x 37 € x 4 dias', 'calc', 'régua low-ticket') + '</div>'
corpo += sec('tabela', '01', 'Tabela por país', table(['País', '#Transparencyads €', '#Lebesgue US$', '#AdSpendSpy €', '#CPM mediano', '#CPA bom / médio / ruim', '#Verba/dia', '#Teste mínimo', '#Teste seguro', '#Impressões no teste', 'Prioridade'], rows),
  'CPM mediano das 3 fontes (US$ convertido a 1,1193). CPA estimado = CPM ÷ (1.000 × CTR × conversão da página): bom = CTR 1,5% e conversão 2%; médio = 1,2% e 1,5%; ruim = 0,9% e 1%.')
corpo += sec('premissas', '02', 'Premissas (troque pelos seus números depois do 1º teste)', '<ul class="cl">' + ''.join(f'<li>{esc(x)}</li>' for x in [
  'Ticket de entrada: 37 euros (mesmo preço dos livros americanos); ticket médio com bump e upsell: 55 euros (ticket médio de survival na Digistore24: US$ 55 a 64).',
  'CTR no link de 0,9% a 1,5% e conversão da página/VSL de 1% a 2% (régua do Ouro VTurb para VSL fria: 1 a 2%).',
  'CPM de 2026 de 3 fontes que estimam a partir de dados de e-commerce (não é dado da Meta). Survival para público 55+ pode ter CPM diferente.',
  'Na régua da /low-ticket o CPA ideal é 50% do preço e o máximo 90%; aqui a conta usa o ticket médio porque o funil de survival vive de upsell (até US$ 155,20 por venda no SSB).',
  'Fontes: ' + ', '.join(f"{k} ({v['periodo']})" for k, v in cpmraw['fontes'].items())]) + '</ul>' + note('Conta que fecha: Espanha, Itália, Portugal e França ficam com CPA médio abaixo do ticket médio de 55 euros. Reino Unido e Alemanha só fecham com o cenário bom ou com upsell forte; por isso o RU entra junto com a Irlanda e com criativo já validado.', 'a', 'leitura'))
corpo += sec('regras', '03', 'Regras de corte do teste', '<ul class="cl">' + ''.join(f'<li>{x}</li>' for x in [
  '<b>Criativo</b> que gastou o valor de 1 ticket (37 €) sem vender: pausa.', '<b>Oferta</b> que gastou 2 a 3 tickets médios (110 a 165 €) sem nenhuma venda em nenhum criativo: desliga e vai para a próxima.',
  '<b>Ordem de troca</b> quando vende caro: criativo → formato do criativo → página → oferta.', '<b>Campanha</b>: vendas com evento de compra, ABO 1 conjunto por criativo, público aberto (sugestão 45+), 1 país por conjunto, início à meia-noite, UTM em cada anúncio.',
  '<b>Decida por venda, custo por venda e lucro</b>, nunca por CTR ou retenção.']) + '</ul>')
pagina('etapa-6-cpm.html', 'Etapa 6 · Quanto custa anunciar', 'E6', corpo, ('Escolher a oferta e o país de entrada', '6 caminhos com escala e demanda medidas', 'Etapa 7', 'escolha-oferta.html'))

# ------------------------------------------------------------------ ROTEIRO
cards_e = [
 ('E1', 'Notícias e gatilho', 'etapa-1-noticias.html', 'Não há fonte oficial de ataque iminente à Lituânia; o que move a busca são as campanhas oficiais de 72 h (UE, RU, França).'),
 ('E2', 'Demanda por país', 'etapa-2-demanda.html', 'Reino Unido, Irlanda e Itália no pico de 5 anos; Espanha subindo nesta semana; Bálticos e nórdicos estáveis.'),
 ('E3', 'Voz do público', 'voz-do-publico.html', '7.634 comentários: pedem mochila, lista e preço; rejeitam medo e reclamam de não ter dinheiro.'),
 ('E4', 'Concorrentes e criativos', 'etapa-4-concorrentes.html', f'{len(cont)} funis americanos (até 1.383 ativos) e {len(EU)} europeus; {len(man_us) + len(man_eu)} criativos para assistir.'),
 ('E5', 'Funis destrinchados', 'etapa-5-funis.html', '5 VSLs transcritas (23 a 46 min), 4 checkouts, 2 quizzes, upsells e 12 advertoriais.'),
 ('E6', 'CPM e verba', 'etapa-6-cpm.html', 'CPM de 26 países em 3 fontes; teste mínimo de 333 € por país; CPA estimado de 26 a 55 €.'),
 ('E7', 'Escolha do país e da oferta', 'escolha-oferta.html', 'Você escolhe a oferta a modelar e o país de entrada. Recomendado: Bug-In Guide modelado, RU + Espanha.')]
corpo = head('Roteiro', 'A pesquisa em <em>7 etapas</em>', 'Cada etapa tem a sua tela, com fonte, número e o que ficou de fora. Comece pela 1 e vá até a 7, onde você decide a oferta e o país.', ['coleta 16/11/2026', 'Europa + EUA como referência'])
corpo += '<div class="grid g2">' + ''.join(f'<a class="card link" href="{f}"><span class="eyebrow">{k}</span><h3 style="margin:6px 0 4px">{esc(t)}</h3><p>{esc(d)}</p></a>' for k, t, f, d in cards_e) + '</div>'
corpo += note('Depois que você escolher (Etapa 7), vêm a modelagem nos 3 eixos, a oferta com preço e bumps, a página de vendas e os criativos, nas pastas 02 a 07.', 'b', 'depois da escolha')
pagina('etapas.html', 'Roteiro das 7 etapas', '00', corpo, ('Começar pela Etapa 1', 'notícias e gatilho', 'Etapa 1', 'etapa-1-noticias.html'))

exec(open(r'E:/Raio-X Survival Europa/01-pesquisa/dados/_scripts/etapas2.py', encoding='utf-8').read())
# ------------------------------------------------------------------ injeta o menu em todas as telas
def injeta(path, prefix):
    h = open(path, encoding='utf-8').read()
    h = re.sub(r'<div class="grp">Etapas da pesquisa</div>.*?(?=<div class="grp">Decisão</div>)', '', h, flags=re.S)
    h = re.sub(r'<a class="sub[^"]*" href="(?:paginas/)?oferta-[^"]+">.*?</a>', '', h, flags=re.S)  # menu mais curto: as análises ficam na tela de ofertas
    atual = os.path.basename(path)
    h = h.replace('<nav aria-label="Navegação global">', '<nav aria-label="Navegação global">' + bloco_menu(prefix, atual if prefix == '' else ''), 1)
    open(path, 'w', encoding='utf-8').write(h)
for f in glob.glob(PG + '*.html'): injeta(f, '')
for f in [H + 'index.html', H + 'Pesquisa - clique aqui.html']:
    if os.path.exists(f) and 'Navegação global' in open(f, encoding='utf-8').read(): injeta(f, 'paginas/')
print('ok', len(os.listdir(IMG)))
