# Organiza a pesquisa para quem abre pelo Explorador de Arquivos:
#  01-pesquisa/criativos-por-concorrente/<grupo>/<NN-concorrente>/  (links físicos dos vídeos e imagens, sem ocupar espaço extra)
#     + ficha.txt de cada concorrente (dados, textos dos anúncios, transcrição do começo de cada vídeo)
#  01-pesquisa/fontes/  (biblioteca de fontes e quadro por país em texto)
#  01-pesquisa/MAPA-DA-PESQUISA.txt
import json, os, re, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')
H = r"E:/Raio-X Survival Europa/01-pesquisa/"
D = H + "dados/"
CAT = json.load(open(D + 'concorrentes.json', encoding='utf-8'))
TR = json.load(open(D + 'criativos-concorrentes/transcricoes.json', encoding='utf-8')) if os.path.exists(D + 'criativos-concorrentes/transcricoes.json') else {}
RAIZ = H + 'criativos-por-concorrente/'
slug = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
limpa = lambda t: re.sub(r'\s*\[\d{5}\]$', '', t or '').strip()
def liga(src, dst):
    if os.path.exists(dst): return
    try: os.link(src, dst)
    except OSError: shutil.copyfile(src, dst)
os.makedirs(RAIZ, exist_ok=True)
mapa = {}; idx = ['CRIATIVOS POR CONCORRENTE', '=' * 26, 'Coleta: Biblioteca de Anúncios da Meta, 16/11/2026. Até 8 criativos diferentes por concorrente (4 mais antigos no ar + 4 mais novos).', 'Cada pasta tem os vídeos e imagens e um ficha.txt com produto, funil, anúncios ativos, o texto de cada anúncio e a transcrição do começo de cada vídeo.', '']
grupos = {}
for c in CAT['concorrentes']: grupos.setdefault(c['grupo'], []).append(c)
for g in sorted(grupos):
    gnome = CAT['grupos'][g]['nome']
    gdir = f"{g}-{slug(gnome)[:48]}"
    idx += ['', f'{g}. {gnome}', f'   {CAT["grupos"][g]["leitura"]}']
    L = sorted(grupos[g], key=lambda c: -(c['ativos'] or 0))
    for n, c in enumerate(L, 1):
        man = D + f"criativos-concorrentes/{c['slug']}/paginas/criativos/manifesto.json"
        cri = json.load(open(man, encoding='utf-8'))['criativos'] if os.path.exists(man) else []
        sel = {a['adArchiveId']: a for a in json.load(open(D + f"criativos-concorrentes/{c['slug']}/selecao.json", encoding='utf-8'))} if os.path.exists(D + f"criativos-concorrentes/{c['slug']}/selecao.json") else {}
        pasta = f"{gdir}/{n:02d}-{c['slug']}"
        os.makedirs(RAIZ + pasta, exist_ok=True)
        ficha = [c['pagina'].upper() if c.get('pagina') else c['slug'], f"Grupo: {gnome}", f"País: {c['pais']}", f"Produto: {c['produto']}", f"Funil e preço: {c['funil']}",
                 f"Anúncios ativos (16/11/2026): {c['ativos'] if c['ativos'] is not None else 'não medido'}", f"Anúncio mais antigo ativo na amostra: {c['dias_mais_antigo'] or '?'} dias", f"Novos nos últimos 7 dias: {c['novos_7d'] if c['novos_7d'] is not None else '?'}",
                 f"Biblioteca: https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&view_all_page_id={c['page_id']}&search_type=page&media_type=all", f"Página de vendas: {c['landing'] or '-'}", '']
        itens = []
        for k, a in enumerate(sorted(cri, key=lambda a: -(a.get('dias') or 0)), 1):
            aid = a['adArchiveId']; src_dir = D + f"criativos-concorrentes/{c['slug']}/paginas/criativos/"
            ext = 'mp4' if a.get('ehVideo') else 'jpg'
            if not os.path.exists(src_dir + f'{aid}.{ext}'): continue
            base = f"{k:02d}-{'video' if ext == 'mp4' else 'imagem'}-{a.get('dias') or 0}d-{aid}"
            liga(src_dir + f'{aid}.{ext}', RAIZ + pasta + f'/{base}.{ext}')
            capa = None
            if ext == 'mp4' and os.path.exists(src_dir + f'{aid}.jpg'):
                liga(src_dir + f'{aid}.jpg', RAIZ + pasta + f'/{base}-capa.jpg'); capa = f'{base}-capa.jpg'
            ad = sel.get(aid, {})
            t = TR.get(aid, {})
            itens.append({'id': aid, 'arquivo': f'{pasta}/{base}.{ext}', 'capa': f'{pasta}/{capa}' if capa else (f'{pasta}/{base}.jpg' if ext == 'jpg' else None), 'video': ext == 'mp4',
                          'dias': a.get('dias'), 'inicio': ad.get('startDate'), 'titulo': limpa(ad.get('title') or a.get('title')), 'texto': ad.get('bodyText') or a.get('bodyText') or '',
                          'link': ad.get('linkUrl') or a.get('linkUrl'), 'cta': ad.get('ctaText'), 'transcricao': t.get('texto'), 'gancho': t.get('gancho'), 'idioma': t.get('idioma')})
            ficha += [f'--- Criativo {k:02d} ({"vídeo" if ext == "mp4" else "imagem"}) · {a.get("dias")} dias no ar · desde {ad.get("startDate") or "?"} · id {aid}',
                      f'Arquivo: {base}.{ext}', f'Link do anúncio: https://www.facebook.com/ads/library/?id={aid}', f'Título: {limpa(ad.get("title") or a.get("title"))}',
                      f'Texto: {(ad.get("bodyText") or a.get("bodyText") or "").strip()}', f'Chamada: {ad.get("ctaText") or "-"} → {ad.get("linkUrl") or a.get("linkUrl") or "-"}']
            if t.get('texto'): ficha += [f'Gancho falado (primeiros segundos, {t.get("idioma")}): {t.get("gancho")}', f'Transcrição do primeiro minuto: {t.get("texto")}']
            ficha.append('')
        open(RAIZ + pasta + '/ficha.txt', 'w', encoding='utf-8').write('\n'.join(ficha))
        mapa[c['slug']] = {'pasta': pasta, 'itens': itens}
        idx.append(f"   {n:02d}. {c.get('pagina') or c['slug']} ({c['pais']}) · {c['ativos'] if c['ativos'] is not None else '?'} ativos · {len(itens)} criativos → {pasta}")
open(RAIZ + 'LEIA-ME.txt', 'w', encoding='utf-8').write('\n'.join(idx))
json.dump(mapa, open(D + 'criativos-concorrentes/mapa-organizado.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# ---------- fontes em texto
F = json.load(open(D + 'fontes.json', encoding='utf-8'))
os.makedirs(H + 'fontes', exist_ok=True)
lin = ['BIBLIOTECA DE FONTES', '=' * 20, f"{len(F['fontes'])} fontes resumidas (16/11/2026). Confiança: alta = órgão oficial ou grande veículo; média = imprensa menor; baixa = blog ou loja (só para achar a fonte oficial).", '']
for f in sorted(F['fontes'], key=lambda x: x['data'], reverse=True):
    lin += [f"[{f['id']}] {f['data']} · {f['pais']} · {f['categoria']} · confiança {f['confianca']}", f"    {f['titulo']}", f"    Resumo: {f['resumo']}", f"    Como usar: {f['uso']}", f"    {f['url']}", '']
open(H + 'fontes/fontes.txt', 'w', encoding='utf-8').write('\n'.join(lin))
q = ['O QUE CADA GOVERNO PEDE ÀS FAMÍLIAS', '=' * 35, '']
for p in F['quadro_paises']: q.append(f"{p['pais']:4} {p['guia']} · prazo {p['prazo']} · {p['quando']} · {p['gatilho']}")
open(H + 'fontes/governos-por-pais.txt', 'w', encoding='utf-8').write('\n'.join(q))
# ---------- mapa da pesquisa
M = """MAPA DA PESQUISA · Survival e preparação para crises na Europa (16/11/2026)
==========================================================================

COMO LER: abra index.html (na pasta de cima). O menu da esquerda segue as etapas na ordem.

paginas/                      telas da pesquisa (abrir pelo index.html)
  etapas.html                 roteiro das 7 etapas
  etapa-1-noticias.html       E1   notícias, linha do tempo e o que cada governo pede
  fontes.html                 E1.1 biblioteca de fontes, todas resumidas
  etapa-2-demanda.html        E2   demanda nos países principais (Trends + TikTok)
  etapa-2-europa.html         E2.1 momentos na Europa toda (38 países, pico a pico, com a causa)
  voz-do-publico.html         E3   o que o público diz (7.634 comentários)
  etapa-4-concorrentes.html   E4   concorrentes e números
  criativos-por-concorrente.html  E4.1 todos os criativos, separados por concorrente
  etapa-5-funis.html          E5   VSL minuto a minuto, checkout, quiz, advertoriais
  etapa-6-cpm.html            E6   CPM, custo por venda e verba de teste por país
  escolha-oferta.html         E7   escolha da oferta e do país

criativos-por-concorrente/    vídeos e imagens por grupo e concorrente + ficha.txt (comece pelo LEIA-ME.txt)
fontes/                       fontes.txt (todas as fontes resumidas) e governos-por-pais.txt
capturas-concorrentes/        prints das páginas de vendas
dados/                        dados brutos
  biblioteca/                 anúncios extraídos da Biblioteca da Meta, contagens, alcance na UE
  criativos-concorrentes/     arquivos originais dos criativos, seleção e transcrições
  ofertas/                    dossiê de cada página (pagina.json, prints), checkouts, VSLs, quizzes
    _vsl/transcricoes/        transcrição completa das 5 VSLs
  organico/                   vídeos do TikTok/YouTube e comentários
  trends/                     Google Trends (países principais e Europa toda) e momentos-europa.json
  fontes.json, concorrentes.json, cpm.json, cpm-verba.json, noticias.json, pesquisa.json
  _scripts/                   scripts usados na coleta (para refazer)
"""
open(H + 'MAPA-DA-PESQUISA.txt', 'w', encoding='utf-8').write(M)
print('ok', len(mapa), 'concorrentes', sum(len(v['itens']) for v in mapa.values()), 'criativos')
