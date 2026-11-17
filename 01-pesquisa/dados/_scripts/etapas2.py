# Executado de dentro de etapas.py (usa as mesmas funções). Telas VISUAIS e em PALAVRAS SIMPLES:
#   etapa-1-noticias, fontes, etapa-2-europa, etapa-4-concorrentes, criativos-por-concorrente, etapa-6-cpm e o roteiro (etapas.html)
rows_e6 = rows  # tabela da Etapa 6, montada em etapas.py
FO = J('fontes.json'); CAT = J('concorrentes.json')
_le = D + 'trends/leitura-europa.html'
LEITURA_EU = open(_le, encoding='utf-8').read() if os.path.exists(_le) else ''
MOM = J('trends/momentos-europa.json')
TEU = J('trends/europa-toda.json')
MAPA = J('criativos-concorrentes/mapa-organizado.json') if os.path.exists(D + 'criativos-concorrentes/mapa-organizado.json') else {}
PR = J('prints/prints.json') if os.path.exists(D + 'prints/prints.json') else {}
fontes = FO['fontes']; FID = {f['id']: f for f in fontes}
NP = {p['pais']: p for p in MOM['paises']}
nome_pais = lambda g: (NP.get(g) or {}).get('nome') or NOME.get(g, g)
def fonte_por_url(trecho):
    return next((f for f in fontes if trecho in f['url']), None)
def thumb(rel, cls='', alt=''):
    src = img(rel) if rel else None
    return f'<span class="thumb {cls}">' + (f'<img src="{src}" alt="{esc(alt)}" loading="lazy">' if src else '<span class="noimg">sem print</span>') + '</span>'
def print_fonte(f):
    return f'prints/fontes/{f["id"]}.jpg' if f and (PR.get(f['id']) or {}).get('ok') else None
def tldr(itens): return '<div class="tldr">' + ''.join(f'<div><b>{a}</b>{b}</div>' for a, b in itens) + '</div>'
def box(titulo, inner, aberto=False, extra=''): return f'<details class="box"{" open" if aberto else ""}><summary>{titulo}{extra}</summary><div class="in">{inner}</div></details>'
def spark(vals, w=240, h=46):
    if not vals or max(vals) == 0: return '<svg class="spark" viewBox="0 0 240 46"></svg>'
    mx = max(vals); k = len(vals) - 1 or 1
    pts = [(round(i * w / k, 1), round(h - 3 - (v / mx) * (h - 8), 1)) for i, v in enumerate(vals)]
    d = 'M' + ' L'.join(f'{x},{y}' for x, y in pts)
    return f'<svg class="spark" viewBox="0 0 {w} {h}" preserveAspectRatio="none"><path class="a" d="{d} L{w},{h} L0,{h} Z"/><path class="l" d="{d}"/><circle class="now" cx="{pts[-1][0]}" cy="{pts[-1][1]}" r="3"/></svg>'
def serie_prep(g, chave='serie_5a'):
    o = TEU[chave].get(g) or {}; s = o.get('serie') or {}
    if not s: return []
    ix = [o['nomes'].index(x) for x in ('survival_kit', 'survivalism', 'bomb_shelter', 'emergency_management')]
    return [sum(s[k][i] for i in ix) for k in sorted(s)]
def hbars(itens, fmt=lambda v: n(v)):
    mx = max(v for _, v, _ in itens) or 1
    return '<div class="hbars">' + ''.join(f'<div class="r"><span>{esc(t)}</span><span class="t"><i class="{c}" style="width:{max(2, round(100 * v / mx))}%"></i></span><span class="v">{fmt(v)}</span></div>' for t, v, c in itens) + '</div>'

# ------------------------------------------------------------------ ETAPA 1 · NOTÍCIAS (linha do tempo com prints)
G = lambda causa: next((a['paises'] for a in MOM['por_acontecimento'] if a['causa'].startswith(causa)), [])
TL = [
 ('24/02/2022', 'A Rússia invade a Ucrânia', 'Foi a maior procura por "3ª Guerra Mundial" em quase todos os países.', G('Invasão'), None, True),
 ('nov/2024', 'Os nórdicos mandam folheto de guerra para as casas', 'Suécia, Noruega, Dinamarca e Finlândia ensinam a aguentar de 3 dias a 1 semana.', ['Suécia', 'Noruega', 'Dinamarca', 'Finlândia'], 'theconversation.com', False),
 ('26/03/2025', 'A União Europeia pede estoque de 3 dias pela primeira vez', 'Primeira grande onda de busca na Europa.', G('UE lança'), 'cnn.com/2025/03/26', False),
 ('28/04/2025', 'Apagão na Espanha e em Portugal', 'Dois países inteiros sem luz. A busca nos dois bate o recorde.', ['Espanha', 'Portugal'], 'canal26.com', False),
 ('nov/2025', 'Holanda, França e Tchéquia mandam guias para as casas', 'Na Holanda, metade das casas passa a ter kit.', ['Holanda', 'França', 'Tchéquia'], 'dutchnews.nl', False),
 ('28/02/2026', 'Começa a guerra com o Irã e o mar de Ormuz fecha', 'Volta o medo de guerra grande e de faltar combustível.', G('Guerra EUA'), 'goodmorningamerica.com', True),
 ('23 a 25/03/2026', 'Drones caem na Lituânia, Letônia e Estônia', 'Na Letônia, a crise derruba o governo em maio.', ['Lituânia', 'Letônia', 'Estônia'], 'aljazeera.com/amp/news/2026/3/25', True),
 ('abr/2026', 'Bélgica lança campanha nacional de 4 anos', 'A busca belga bate o recorde de 5 anos.', ['Bélgica'], 'phaenyx.com', False),
 ('22/05/2026', 'Alemanha separa 10 bilhões de euros para proteção civil', 'E admite que os abrigos públicos não cabem nem 1% do povo.', ['Alemanha'], 'bbk.bund.de', False),
 ('set/2026', 'Drones na Romênia e na Moldávia; Polônia ensina a se abrigar', 'Na Polônia, a busca bate o recorde do ano.', ['Polônia', 'Romênia', 'Moldávia'], 'notesfrompoland.com', True),
 ('22/10/2026', 'Reino Unido pede: prepare a casa para 3 dias', 'Água, enlatados e lanternas somem das prateleiras.', ['Reino Unido', 'Irlanda'], 'gov.uk/government/news', False),
 ('03/11/2026', 'A União Europeia publica o guia de 3 dias', 'É o que deixa o assunto quente agora em 13 países.', ['Itália', 'Espanha', 'Bélgica', 'Suíça', 'Irlanda', 'Finlândia', 'Suécia'], 'civil-protection-humanitarian-aid.ec.europa.eu', False),
 ('11/11/2026', 'Alerta de abrigo nos três Bálticos', 'Drones vindos da Rússia ou de Belarus. O alerta é cancelado em horas.', ['Lituânia', 'Letônia', 'Estônia'], 'cyprus-mail.com/2026/11/11', True),
]
tl = '<div class="tl">'
for dt_, tit, txt, ps, url, war in TL:
    f = fonte_por_url(url) if url else None
    th = (f'<a href="{esc(f["url"])}" target="_blank" rel="noopener">' + thumb(print_fonte(f), alt=f['titulo']) + '</a>') if f else ''
    tl += f'<div class="it{" war" if war else ""}"><div><div class="dt">{esc(dt_)}</div><h4>{esc(tit)}</h4><p>{esc(txt)}</p><div class="chips">' + ''.join(f'<span class="chip">{esc(p)}</span>' for p in ps[:9]) + (f'<span class="chip">+{len(ps) - 9}</span>' if len(ps) > 9 else '') + f'</div></div>{th}</div>'
tl += '</div>'
PRZ = lambda p: p if p not in ('–', '') else 'sem guia'
gov = '<div class="ggrid">' + ''.join(f'<div class="gcard"><div class="c">{esc(nome_pais(p["pais"]))}</div><div class="d">{esc(PRZ(p["prazo"]))}</div><div class="g">{esc(p["guia"])} · {esc(p["quando"])}</div></div>' for p in FO['quadro_paises']) + '</div>'
corpo = head('Etapa 1 · notícias', 'O que <em>aconteceu</em>, em ordem', 'A linha do tempo mostra os fatos que fizeram os europeus procurar o assunto. Bolinha verde: governo pedindo para se preparar. Bolinha vermelha: susto ou guerra.', [])
corpo += tldr([('Nenhuma', 'fonte oficial diz que a Rússia vai atacar a Lituânia.'), ('3 dias', 'é o que a União Europeia e o Reino Unido pedem para cada casa aguentar.'), ('13 países', 'estão com o assunto quente agora, depois do guia da UE de 03/11.')])
corpo += sec('linha', '01', 'Linha do tempo', tl, 'Clique no print para abrir a notícia.')
corpo += sec('governos', '02', 'Quanto tempo cada governo pede para aguentar', gov, 'Onde o governo já manda guia de graça (nórdicos, Bálticos, Polônia, Tchéquia), um guia pago precisa dar mais: cardápio, lista de compras com preço e o que fazer em cada dia.')
corpo += sec('uso', '03', 'Como usar na oferta', note('<b>Mostre o pedido do governo. Não prometa guerra.</b> Dá para provar, o Facebook aceita e as pessoas confiam. O comentário mais curtido da pesquisa (16 mil curtidas) reclama de quem espalha medo.', 'g', 'recomendado') + box('Vídeos de notícia mais vistos', table(['Rede', 'Canal', 'Assunto', '#Visualizações', '#Comentários', 'Data', 'Link'], rows_v)))
corpo += '<div class="btns">' + btn('Ver todas as fontes, com print', 'fontes.html', 'primary', False) + '</div>'
pagina('etapa-1-noticias.html', 'Etapa 1 · Notícias', 'E1', corpo, ('Ver todas as fontes', 'cada uma com print e resumo', 'Etapa 1.1', 'fontes.html'))

# ------------------------------------------------------------------ ETAPA 1.1 · FONTES (cartões com print)
CATN = {'Oficial': ('governo', 'g'), 'Imprensa': ('jornal', 'n'), 'Dado de mercado': ('estudo', 'a'), 'Blog/comercial': ('blog ou loja', 'r')}
CONFN = {'alta': ('confiável', 'g'), 'média': ('mais ou menos', 'a'), 'baixa': ('não use como prova', 'r')}
REG = [('ue', 'União Europeia e vários países', lambda p: p.startswith('UE') or p in ('33 países', 'Europa')),
       ('rui', 'Reino Unido e Irlanda', lambda p: p in ('GB', 'IE')),
       ('oeste', 'França, Bélgica, Holanda, Alemanha, Áustria e Suíça', lambda p: p.split('/')[0] in ('FR', 'BE', 'NL', 'CH', 'DE', 'AT', 'DACH', 'LU')),
       ('sul', 'Espanha, Portugal, Itália e Grécia', lambda p: p.split('/')[0] in ('ES', 'PT', 'IT', 'GR')),
       ('leste', 'Polônia, Bálticos, Tchéquia, Romênia e Bulgária', lambda p: p.split('/')[0] in ('PL', 'LT', 'LV', 'EE', 'RO', 'CZ', 'MD', 'BG')),
       ('nord', 'Países nórdicos', lambda p: p.split('/')[0] in ('SE', 'NO', 'DK', 'FI', 'Nórdicos')),
       ('glob', 'Guerra no mundo e números de mercado', lambda p: True)]
def regiao(p):
    for k, nm, f in REG:
        if f(p): return k
def scard(f):
    c = CATN.get(f['categoria'], (f['categoria'], 'n')); cf = CONFN.get(f['confianca'], (f['confianca'], 'n'))
    return (f'<article class="scard"><a href="{esc(f["url"])}" target="_blank" rel="noopener">{thumb(print_fonte(f), alt=f["titulo"])}</a><div class="ph">'
            f'<div class="m">{dmy(f["data"]) if len(f["data"]) == 10 else esc(f["data"])} · {esc(f["pais"])} {pill(*c)} {pill(*cf)}</div>'
            f'<h4>{link(f["titulo"], f["url"])}</h4><p>{esc(f["resumo"])}</p><div class="use">→ {esc(f["uso"])}</div></div></article>')
cnt = {}
for f in fontes: cnt[f['categoria']] = cnt.get(f['categoria'], 0) + 1
nprint = sum(1 for f in fontes if print_fonte(f))
corpo = head('Etapa 1.1 · fontes', 'Todas as <em>fontes</em>', f'{len(fontes)} notícias e documentos, cada um com o print da página, um resumo curto e para que serve na oferta. Separados por região: clique na região para abrir.', [])
corpo += tldr([(str(cnt.get('Oficial', 0)), 'sites de governo'), (str(cnt.get('Imprensa', 0)), 'jornais'), (str(cnt.get('Dado de mercado', 0) + cnt.get('Blog/comercial', 0)), 'estudos, blogs e lojas (só para achar a fonte de verdade)'), (str(nprint), 'com print da página')])
for i, (k, nm, fn) in enumerate(REG):
    L = sorted([x for x in fontes if regiao(x['pais']) == k], key=lambda x: x['data'], reverse=True)
    if L: corpo += box(f'{esc(nm)} <span class="chip">{len(L)}</span>', '<div class="sgrid">' + ''.join(scard(x) for x in L) + '</div>', aberto=(i == 0))
pagina('fontes.html', 'Todas as fontes', 'E1.1', corpo, ('Ver em que países o assunto está quente', 'mapa da Europa', 'Etapa 2.1', 'etapa-2-europa.html'))

# ------------------------------------------------------------------ ETAPA 2.1 · EUROPA TODA (mapa + gráficos)
POS = {'IS': (0, 0), 'NO': (5, 0), 'SE': (6, 0), 'FI': (7, 0), 'EE': (8, 0), 'IE': (1, 1), 'GB': (2, 1), 'DK': (5, 1), 'LT': (7, 1), 'LV': (8, 1),
       'BE': (3, 2), 'NL': (4, 2), 'DE': (5, 2), 'PL': (6, 2), 'UA': (7, 2), 'FR': (3, 3), 'LU': (4, 3), 'CZ': (5, 3), 'SK': (6, 3), 'MD': (7, 3),
       'PT': (1, 4), 'ES': (2, 4), 'CH': (4, 4), 'AT': (5, 4), 'HU': (6, 4), 'RO': (7, 4), 'IT': (4, 5), 'SI': (5, 5), 'HR': (6, 5), 'RS': (7, 5), 'BG': (8, 5),
       'MT': (4, 6), 'BA': (5, 6), 'ME': (6, 6), 'MK': (7, 6), 'AL': (6, 7), 'GR': (7, 7), 'CY': (8, 7)}
SITC = {'em alta agora': ('hot', 'quente agora', 'g'), 'subiu e esfriou': ('cool', 'subiu e já caiu', 'a'), 'subiu em 2026': ('early', 'subiu no começo do ano', 'n'), 'estável': ('flat', 'parado', 'n'), 'volume baixo': ('low', 'pouca busca', 'n')}
P = [p for p in MOM['paises'] if not p.get('sem_dados')]
tiles = '<div class="tiles">'
for g, (x, y) in POS.items():
    p = NP.get(g); c = SITC[p['situacao']][0] if p and not p.get('sem_dados') else 'low'
    tiles += f'<a class="tile {c}" href="#p-{g}" style="grid-column:{x + 1};grid-row:{y + 1}" title="{esc(nome_pais(g))}"><b>{g}</b><span>{esc(nome_pais(g)[:11])}</span></a>'
tiles += '</div><div class="leg">' + ''.join(f'<span><i class="{c}"></i>{t}</span>' for c, t, _ in SITC.values()) + '</div>'
def pcard(p):
    c, t, pl = SITC[p['situacao']]
    s = serie_prep(p['pais']); u7 = p.get('ultimos7_vs_pico90')
    picos = p['picos'][-3:][::-1]
    li = ''.join(f'<li><b>{dmy(x["semana"])}</b> · {esc(x["causa"] or "motivo não achado")}</li>' for x in picos)
    return (f'<div class="pcard" id="p-{p["pais"]}"><h4>{esc(p["nome"])} {pill(t, pl)}</h4><div class="sub">{esc(p.get("idioma") or "")} · {n(p.get("pop_mi"), 1)} milhões de pessoas</div>{spark(s)}'
            + (f'<div class="sub" style="margin-top:6px">Força agora, perto do pico dos últimos 3 meses: {n(u7)} de 100</div><div class="meter"><i style="width:{u7 or 0}%"></i></div>' if u7 is not None else '')
            + f'<ul>{li or "<li>sem pico claro</li>"}</ul></div>')
ordem = {'em alta agora': 0, 'subiu e esfriou': 1, 'subiu em 2026': 2, 'estável': 3, 'volume baixo': 4}
P.sort(key=lambda p: (ordem[p['situacao']], -(p.get('pop_mi') or 0)))
grupos_sit = {}
for p in P: grupos_sit.setdefault(p['situacao'], []).append(p)
agora = grupos_sit.get('em alta agora', [])
acont_ok = [a for a in MOM['por_acontecimento'] if not a['causa'].startswith('sem notícia')]
rows_ev = [tr([td(esc(', '.join(dmy(s) for s in a['semanas'][:3])) + (' …' if len(a['semanas']) > 3 else '')), td('<b>' + esc(a['causa']) + '</b>'), td(esc(', '.join(a['paises'])))]) for a in acont_ok]
corpo = head('Etapa 2.1 · Europa toda', 'Onde o assunto está <em>quente</em> agora', 'Cada quadradinho é um país. Verde: muita gente buscando agora. Clique no país para ver o gráfico dos últimos 5 anos e o que fez a busca subir.', [])
corpo += tldr([(f'{len(agora)} países', 'quentes agora, puxados pelo guia da União Europeia de 03/11.'), ('2 semanas', 'é quanto dura um pico. Depois a busca cai pela metade.'), ('2022', 'foi a última vez que a Lituânia buscou muito o assunto.')])
corpo += sec('mapa', '01', 'Mapa da Europa', tiles)
corpo += sec('agora', '02', 'Os países quentes agora', '<div class="pgrid">' + ''.join(pcard(p) for p in agora) + '</div>', 'O gráfico mostra a busca nos últimos 5 anos. A bolinha é hoje.')
outros = ''
for sit in ('subiu e esfriou', 'subiu em 2026', 'estável', 'volume baixo'):
    L = grupos_sit.get(sit, [])
    if L: outros += box(f'{SITC[sit][1].capitalize()} <span class="chip">{len(L)} países</span>', '<div class="pgrid">' + ''.join(pcard(p) for p in L) + '</div>')
corpo += sec('outros', '03', 'Os outros países', outros)
corpo += sec('resumo', '04', 'O que isso quer dizer', LEITURA_EU + box('O que fez a busca subir, acontecimento por acontecimento', table(['Semanas', 'O que aconteceu', 'Países onde subiu'], rows_ev)) +
  box('Como medi', '<ul class="cl"><li>Google Trends: mostra quando as pessoas buscam mais ou menos um assunto, não o número exato.</li><li>Assuntos que valem em qualquer idioma: kit de sobrevivência, sobrevivência, abrigo antibomba e emergências. Separado: "3ª Guerra Mundial".</li><li>Pico: a semana com mais busca do que as 4 semanas antes e depois.</li><li>Motivo: a notícia daquela mesma semana. É a explicação mais provável, não uma prova.</li><li>Países pequenos têm pouca busca e o número pula à toa.</li></ul>'))
pagina('etapa-2-europa.html', 'Etapa 2.1 · Europa toda', 'E2.1', corpo, ('Ler o que as pessoas pedem e do que reclamam', '7.634 comentários', 'Etapa 3', 'voz-do-publico.html'))

# ------------------------------------------------------------------ ETAPA 4 · CONCORRENTES (barras)
conc = CAT['concorrentes']
GN = {'A': 'Livros com vídeo de vendas (EUA)', 'B': 'Livro grátis com perguntas (EUA)', 'C': 'Matéria que vende um produto (EUA)', 'D': 'Lojas (EUA)', 'E': 'Matéria que vende um produto (Europa)', 'F': 'Kits e mochilas (Europa)', 'G': 'Guias em PDF e cursos (Europa)', 'H': 'Fora do assunto'}
GL = {'A': 'O modelo a copiar: anúncio, página com vídeo longo, compra pela Digistore24 com brindes.', 'B': 'Dão um livro de graça, fazem perguntas, pedem o e-mail e vendem depois.',
      'C': 'Parece reportagem contada por uma pessoa. No fim, vende um objeto.', 'D': 'Lojas de comida, energia e internet sem rede.', 'E': 'O modelo americano já traduzido, usando o pedido do governo.',
      'F': 'Lojas locais de kit de 3 dias, mochila, rádio, filtro e comida.', 'G': 'O mesmo tipo de produto que você venderia: guia em PDF ou curso no idioma do país.', 'H': 'Apareceram na busca, mas vendem outra coisa.'}
top_us = sorted([c for c in conc if c['grupo'] in 'ABCD' and c['ativos']], key=lambda c: -c['ativos'])[:12]
top_eu = sorted([c for c in conc if c['grupo'] in 'EFG' and c['ativos']], key=lambda c: -c['ativos'])[:12]
cor = lambda c: '' if c['grupo'] in 'AEG' else 'a'
corpo = head('Etapa 4 · concorrentes', 'Quem já <em>vende</em> isso', 'Quanto maior a barra, mais anúncios a página tem no ar hoje. Página que mantém centenas de anúncios rodando está vendendo. Verde: o tipo de oferta mais parecido com a sua. Amarelo: produto físico.', [])
corpo += tldr([('834', 'anúncios no ar do livro The Lost Skills of Independence (o modelo a copiar)'), ('3 a 74 dias', 'é a idade dos concorrentes na Europa: o mercado começou agora'), ('2', 'guias em PDF anunciados na Europa (Espanha e França)')])
corpo += sec('eua', '01', 'Estados Unidos: os maiores', hbars([(c['pagina'] if len(c['pagina']) < 26 else c['pagina'][:24] + '…', c['ativos'], cor(c)) for c in top_us]))
corpo += sec('europa', '02', 'Europa: os maiores', hbars([(c['pagina'] if len(c['pagina']) < 26 else c['pagina'][:24] + '…', c['ativos'], cor(c)) for c in top_eu]))
corpo += sec('quem', '03', 'Quem vê esses anúncios na Europa', note('A Meta mostra quem viu os anúncios na Europa. <b>A maior parte do público tem mais de 55 anos.</b> The Amish Ways já faz campanha só para o Reino Unido.', 'b') + box('Ver os números anúncio por anúncio', table(['Anúncio', 'Página', 'País', '#Pessoas alcançadas', '#Com 55 anos ou mais', '#Mulheres'], rows_alc)))
corpo += '<div class="btns">' + btn('Ver os anúncios de cada concorrente', 'criativos-por-concorrente.html', 'primary', False) + btn('Ver as análises das páginas', 'ofertas.html', '', False) + '</div>'
pagina('etapa-4-concorrentes.html', 'Etapa 4 · Concorrentes', 'E4', corpo, ('Ver os anúncios de cada um', 'organizados por grupo', 'Etapa 4.1', 'criativos-por-concorrente.html'))

# ------------------------------------------------------------------ ETAPA 4.1 · ANÚNCIOS POR CONCORRENTE (abre e fecha)
REL = '../criativos-por-concorrente/'
def card_cri(i):
    cap = (REL + i['capa']) if i.get('capa') else None
    if i['video']: media = f'<video src="{esc(REL + i["arquivo"])}"' + (f' poster="{esc(cap)}"' if cap else '') + ' controls muted playsinline preload="none" style="width:100%;height:100%;object-fit:cover;background:#000"></video>'
    else: media = f'<img src="{esc(REL + i["arquivo"])}" alt="" loading="lazy" style="width:100%;height:100%;object-fit:cover">'
    fala = f'<div class="tx">🎙 “{esc(i["gancho"][:140])}”</div>' if i.get('gancho') else ''
    mais = ''
    if i.get('texto') or i.get('transcricao'):
        mais = '<details class="mini"><summary>ver texto e fala completos</summary>' + (f'<div class="tx"><b>Texto do anúncio:</b> {esc(i["texto"])}</div>' if i.get('texto') else '') + (f'<div class="tx"><b>Fala do 1º minuto:</b> {esc(i["transcricao"])}</div>' if i.get('transcricao') else '') + '</details>'
    return (f'<article class="ad"><div class="media">{media}<span class="fmt">{i["dias"]} dias</span></div><div class="body"><div class="t">“{esc(i["titulo"] or "sem título")}”</div>{fala}{mais}</div>'
            f'<div class="foot">{btn("Ver o anúncio", "https://www.facebook.com/ads/library/?id=" + i["id"])}</div></article>')
def lp_print(c):
    if (PR.get(c['slug']) or {}).get('ok'): return f'prints/concorrentes/{c["slug"]}.jpg'
    if c.get('dossie') and os.path.exists(D + f'ofertas/{c["dossie"]}/celular.jpg'): return f'ofertas/{c["dossie"]}/celular.jpg'
    return None
grupos = {}
for c in conc: grupos.setdefault(c['grupo'], []).append(c)
tot = sum(len(v['itens']) for v in MAPA.values())
corpo = head('Etapa 4.1 · anúncios', 'Os anúncios de <em>cada concorrente</em>', 'Clique no concorrente para abrir os anúncios dele. Em cada um: a foto da página de vendas, os anúncios mais antigos (os que dão lucro) e os mais novos (o que estão testando agora). Nos vídeos, o microfone mostra o que a pessoa fala no começo.', [])
corpo += '<div class="gsum">' + ''.join(f'<a href="#g{g}"><b>{len(grupos[g])}</b><span>{esc(GN[g])}</span></a>' for g in sorted(grupos)) + '</div>'
for g in sorted(grupos):
    inner = ''
    for c in sorted(grupos[g], key=lambda c: -(c['ativos'] or 0)):
        m = MAPA.get(c['slug'], {'itens': [], 'pasta': ''})
        lp = img(lp_print(c)) if lp_print(c) else None
        strip = ''.join(f'<img src="{esc(REL + (i["capa"] or i["arquivo"]))}" alt="" loading="lazy">' for i in m['itens'][:4] if (i.get('capa') or not i['video']))
        resumo = (f'<span class="lp">' + (f'<img src="{lp}" alt="" loading="lazy">' if lp else '') + '</span>'
                  f'<span><span class="nm">{esc(c.get("pagina") or c["slug"])}</span> ' + pill((n(c['ativos']) + ' no ar') if c['ativos'] is not None else 'não contado', 'g' if (c['ativos'] or 0) >= 100 else 'a') +
                  f'<span class="ds" style="display:block">{esc(c["pais"])} · {esc(c["produto"])}</span></span><span class="strip">{strip}</span>')
        links = btn('Todos os anúncios dele', LIB(c['page_id'])) + (btn('Página de vendas', c['landing']) if c.get('landing') else '') + (btn('Análise da página', 'oferta-' + c['dossie'] + '.html', 'sm ghost', False) if c.get('dossie') and os.path.exists(PG + 'oferta-' + c['dossie'] + '.html') else '')
        corpoc = (f'<p class="d"><b>Como vende:</b> {esc(c["funil"])}. <b>Anúncio mais antigo no ar:</b> {n(c["dias_mais_antigo"]) if c.get("dias_mais_antigo") is not None else "?"} dias. <b>Novos nesta semana:</b> {n(c["novos_7d"]) if c.get("novos_7d") is not None else "?"}.</p><div class="btns">{links}</div>'
                  + (('<div class="ads">' + ''.join(card_cri(i) for i in m['itens']) + '</div>') if m['itens'] else note('Nenhum anúncio baixado. Veja todos pelo botão "Todos os anúncios dele".', 'a')))
        inner += f'<details class="box comp" id="c-{c["slug"]}"><summary>{resumo}</summary><div class="in">{corpoc}</div></details>'
    corpo += sec(f'g{g}', g, esc(GN[g]), inner, esc(GL[g]))
pagina('criativos-por-concorrente.html', 'Etapa 4.1 · Anúncios por concorrente', 'E4.1', corpo, ('Ver as páginas de vendas por dentro', 'vídeo de vendas, compra e ofertas extras', 'Etapa 5', 'etapa-5-funis.html'))

# ------------------------------------------------------------------ ETAPA 6 · CUSTO (barras)
cps = sorted(cpm['paises'], key=lambda c: c['cpm_eur'])
corpo = head('Etapa 6 · custo', 'Quanto custa <em>anunciar</em> em cada país', 'A barra mostra quanto custa para 1.000 pessoas verem o seu anúncio (o CPM). Quanto menor, mais barato testar. O custo de cada venda é uma estimativa, que o primeiro teste vai confirmar.', [])
corpo += tldr([('333 €', 'é o mínimo para testar em um país: 3 anúncios por 3 dias.'), ('cerca de 33 €', 'é o custo estimado de cada venda na Espanha.'), ('cerca de 55 €', 'é o custo estimado de cada venda no Reino Unido.')])
corpo += sec('cpm', '01', 'Custo para 1.000 pessoas verem o anúncio', hbars([(NOME.get(c['pais'], c['pais']), c['cpm_eur'], 'a' if c['cpm_eur'] >= 9 else '') for c in cps], fmt=lambda v: n(v, 2) + ' €'), 'Média de 3 sites que estimam esse custo em 2026. Não é dado da própria Meta.')
corpo += sec('venda', '02', 'Custo estimado de cada venda', hbars([(NOME.get(c['pais'], c['pais']), c['cpa_estimado']['medio'], 'a' if c['cpa_estimado']['medio'] > 45 else '') for c in cps], fmt=lambda v: n(v) + ' €'),
  'Se o guia custar 37 € e cada cliente gastar 55 € com os extras, a conta fecha onde a barra está abaixo de 45 €. Amarelo: só fecha se o anúncio for muito bom.')
corpo += sec('regras', '03', 'Quando parar um teste', '<ul class="cl"><li><b>Anúncio</b> que gastou 37 € sem vender: pausa.</li><li><b>Oferta</b> que gastou de 110 € a 165 € sem nenhuma venda: desliga e tenta a próxima.</li><li><b>Vendendo caro?</b> Troque nesta ordem: o anúncio, o formato do anúncio, a página e, por último, a oferta.</li><li>Decida pela venda e pelo lucro, não por cliques.</li></ul>' + box('Tabela completa por país', table(['País', '#Transparencyads €', '#Lebesgue US$', '#AdSpendSpy €', '#Média', '#Venda: boa / média / ruim', '#Por dia', '#Teste mínimo', '#Teste seguro', '#Pessoas alcançadas', 'Prioridade'], rows_e6)))
pagina('etapa-6-cpm.html', 'Etapa 6 · Quanto custa anunciar', 'E6', corpo, ('Escolher o que vender e onde começar', '6 caminhos comparados', 'Etapa 7', 'escolha-oferta.html'))

# ------------------------------------------------------------------ ROTEIRO (miniaturas)
cards_e = [
 ('E1', 'Notícias', 'etapa-1-noticias.html', 'Linha do tempo do que aconteceu.', False),
 ('E1.1', 'Todas as fontes', 'fontes.html', f'{len(fontes)} notícias com print e resumo.', True),
 ('E2', 'Procura nos países principais', 'etapa-2-demanda.html', 'Quanto cada país busca e o que viraliza.', False),
 ('E2.1', 'Mapa da Europa', 'etapa-2-europa.html', f'{len(P)} países: quem está quente agora.', True),
 ('E3', 'O que as pessoas dizem', 'voz-do-publico.html', 'Pedem mochila, lista e preço. Não gostam de medo.', False),
 ('E4', 'Concorrentes', 'etapa-4-concorrentes.html', 'Quem tem mais anúncios no ar.', False),
 ('E4.1', 'Anúncios por concorrente', 'criativos-por-concorrente.html', f'{len(conc)} concorrentes, {tot} anúncios.', True),
 ('E5', 'Páginas de vendas por dentro', 'etapa-5-funis.html', 'Vídeos de vendas minuto a minuto.', False),
 ('E6', 'Quanto custa anunciar', 'etapa-6-cpm.html', 'Custo por país e verba de teste.', False),
 ('E7', 'Escolha', 'escolha-oferta.html', 'Você escolhe o que vender e onde.', False)]
def mini(f):
    rel = f'prints/telas/{f[:-5]}.jpg'
    return thumb(rel if os.path.exists(D + rel) else None)
corpo = head('Roteiro', 'A pesquisa em <em>7 etapas</em>', 'Siga na ordem. Os cartões cinza aprofundam a etapa de cima.', [])
corpo += '<div class="steps">' + ''.join(f'<a class="step{" sub" if s else ""}" href="{f}">{mini(f)}<div class="ph"><div class="k">{k}</div><h4>{esc(t)}</h4><p>{esc(d)}</p></div></a>' for k, t, f, d, s in cards_e) + '</div>'
corpo += note('No computador, dentro de 01-pesquisa: <b>criativos-por-concorrente</b> (vídeos e uma ficha de cada concorrente), <b>fontes</b> (todas as fontes em texto) e <b>MAPA-DA-PESQUISA.txt</b> (o que tem em cada pasta).', 'b', 'pastas')
pagina('etapas.html', 'Roteiro das 7 etapas', '00', corpo, ('Começar pela Etapa 1', 'notícias', 'Etapa 1', 'etapa-1-noticias.html'))

# ------------------------------------------------------------------ estilo visual (acrescenta uma vez ao estilo.css do gerador)
_css = open(PG + 'estilo.css', encoding='utf-8').read().split('VISUAL SURVIVAL')[0]
_css = _css[:_css.rfind('/*')] if 'VISUAL SURVIVAL' in open(PG + 'estilo.css', encoding='utf-8').read() else _css
open(PG + 'estilo.css', 'w', encoding='utf-8').write(_css.rstrip() + chr(10) + open(r'E:/Raio-X Survival Europa/01-pesquisa/dados/_scripts/visual.css', encoding='utf-8').read())
