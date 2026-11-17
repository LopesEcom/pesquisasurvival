# Catálogo único dos concorrentes: grupo, país, produto, funil, preço, anúncios ativos (conector Meta Ads, 16/11/2026) e links.
import json
D = r"E:/Raio-X Survival Europa/01-pesquisa/dados/"
met = json.load(open(D + 'biblioteca/metricas-paginas.json', encoding='utf-8'))
G = {
 'A': ('EUA · Livros com VSL (rede Global Brother, Digistore24)', 'O modelo a seguir: livro + VSL longa + checkout com bônus.'),
 'B': ('EUA · Livro grátis por quiz (captação de e-mail)', 'Isca grátis, quiz curto, oferta depois do e-mail.'),
 'C': ('EUA · Advertorial + produto físico', 'Matéria em primeira pessoa que vende um item (água, rádio, manta).'),
 'D': ('EUA · Lojas e produtos de preparação', 'Comida, energia, internet offline.'),
 'E': ('Europa · Advertorial com a campanha oficial', 'O mesmo modelo americano, já traduzido e usando o guia do governo.'),
 'F': ('Europa · Kits, mochilas e itens físicos', 'Lojas locais de kit de 72 h, rádio, filtro e comida.'),
 'G': ('Europa · Guias digitais e cursos (o formato que você venderia)', 'PDF ou curso no idioma local.'),
 'H': ('Fora do tema central (ruído útil)', 'Apareceram nas buscas, mas vendem outra coisa.'),
}
C = [
 # slug, grupo, país, produto, funil/preço, ativos, page_id, landing, dossiê
 ('the-lost-skills-of-independence', 'A', 'EUA', '200 habilidades dos avós (livro espiral)', 'VSL 23 min → Digistore24, US$ 39 + 3 bônus', 834, '984264748113661', 'https://www.thelostskillsofindependence.com/book', 'thelostskillsofindependence.com-book'),
 ('bug-in-guide', 'A', 'EUA', 'Guia de ficar em casa na crise (ex-SEAL)', 'VSL 31,6 min → Digistore24, US$ 37 + 2 bônus', 739, '319949591203932', 'https://www.buginguide.com/book/', 'buginguide.com-book'),
 ('the-amish-ways', 'A', 'EUA', 'Vida sem eletricidade dos Amish (livro)', 'VSL 46 min → Digistore24, US$ 29,25; campanha só no RU', 399, '385207881346032', 'https://www.theamishways.com/book/', 'theamishways.com-book'),
 ('the-lost-super-foods', 'A', 'EUA', '126 comidas que duram sem geladeira', 'VSL 30,7 min → Digistore24, US$ 27,75 ou só digital', 69, '105454587758042', 'https://thelostsuperfoods.com/book/', 'thelostsuperfoods.com-book'),
 ('amish-survival-secrets', 'B', 'EUA', 'Manual Amish grátis', 'quiz 5 perguntas → vídeo → e-mail; anúncio de 305 dias', 159, '852725977934152', 'https://reports.homesteadingsecrets.com/survey-amish-survival-guide7bmn7z7l', 'reports.homesteadingsecrets.com-survey-amish-survival-guide7bm'),
 ('amish-self-reliance-secrets', 'B', 'EUA', 'Livro Amish de conservas grátis', 'mesmo funil de quiz (página irmã)', None, '1079691441893643', 'https://reports.homesteadingsecrets.com/', None),
 ('roy-the-prepper', 'B', 'EUA', 'Guia grátis do sistema de água', 'quiz 3 perguntas → e-mail → vídeo', 28, '111268078396746', 'https://prep.royfoley.com/water-generator', None),
 ('ready-nation-usa', 'C', 'EUA', 'Bolsa/filtro de água', 'advertorial "se você tem filhos ou netos", cerca de US$ 70', 986, '1108073152395957', 'https://guardsurvival.com/pages/advertorial-v3-water-bag', 'guardsurvival.com-pages-advertorial-v3-water-bag'),
 ('blackout-water', 'C', 'EUA', 'Canudo filtro (5 unidades)', 'advertorial "The Outsider", 43% off, garantia 365 dias', 633, '1081077951748363', 'https://www.tryblackoutwater.com/pages/advertorial', None),
 ('ray-bennett', 'C', 'EUA', 'Mesmo canudo filtro (persona)', 'página-persona da Blackout Water', None, '1322972817559459', 'https://www.tryblackoutwater.com/', None),
 ('american-ready', 'C', 'EUA', 'Água e kits de reserva', 'advertorial "se você é pai ou avô"', 493, '1379406858587278', 'https://safereservesupply.com/', None),
 ('sierra-madre', 'C', 'EUA', 'Saco de dormir de emergência + livro', 'depoimento "nunca saio de casa sem isso"', 1383, '228755309377', 'https://offer.sierramadreresearch.com/emergency-sleeping-bag', None),
 ('terrashell-by-quietprotector', 'C', 'EUA', 'Manta térmica', 'oferta 68% off; 4.216 anúncios ativos', 4216, '1050667511458583', 'https://tryterrashell.com/', None),
 ('jake-morrison', 'C', 'EUA/RU', 'Manta térmica (persona da TerraShell)', '"Warmer than your quilts"', 1071, '768075889726058', 'https://tryterrashell.com/', None),
 ('preparedness-insiders', 'C', 'EUA', 'Gerador / bases de 90 dias', 'advertorial "o Pentágono prepara bases"', 4, '104525639386923', 'https://try.thegreatproject.com/tr-fb', None),
 ('food-storage-tips', 'C', 'EUA', 'Tampa de pote para conserva', '"#1 Prepper Hack", Black Friday', 388, '724248187440810', 'https://masongenie.com/', None),
 ('verva-masks', 'C', 'EUA', 'Máscara de gás', '"Built For Nuclear Fallout"', 362, '1077368128791116', 'https://shopverva.com/', None),
 ('linda-thompson', 'C', 'EUA', 'Cofre de sementes', '"Your Survival Vault Might Be Fake"', 0, '1086092167918967', 'https://gardenspulse.com/', None),
 ('4patriots', 'D', 'EUA', 'Gerador solar, comida', 'parcelado "menos de US$ 299/mês"', 370, '1449461518652183', 'https://go.4patriots.com/2200x/', 'go.4patriots.com-2200x'),
 ('prepper-disk', 'D', 'EUA', 'Internet offline 512 GB', 'US$ 297', 47, '534573416409327', 'https://www.prepperdisk.com/pages/landing', 'prepperdisk.com-pages-landing'),
 ('last-country-supply', 'D', 'EUA', 'Loja de suprimentos', 'loja; anúncio de 465 dias', 12, '542548632284482', 'https://lastcountrysupply.com/', None),
 ('emily-johnson', 'H', 'EUA', 'E-books de Bíblia e fim dos tempos', 'nicho de fé; 1.875 ativos', 1875, '909307485596444', 'https://thefaithmade.com/pages/last-days', 'thefaithmade.com-pages-last-days'),
 ('notfall-kompass', 'E', 'Alemanha', 'Filtro de água HYDRO-X1 (Virest)', 'advertorial "se você tem filhos ou netos"; 69 dias', 227, '1241103159077943', 'https://virest.de/products/hydra-x1-notfall-wasserfilter-1-500-liter', 'virest.de-products-hydra-x1-notfall-wass'),
 ('blackoutreport', 'E', 'Alemanha', 'Rádio de emergência', 'advertorial do guia da UE de 03/11', 10, '1514193808434156', 'https://blackoutreport.de/72-stunden-vorsorge', 'blackoutreport.de-72-stunden-vorsorge'),
 ('ready-families-network', 'E', 'Reino Unido', 'Filtro ClearX Pro', 'advertorial "120 litros da orientação oficial", compre 1 leve 2', 148, '1270045722861427', 'https://standbysupplyco.com/pages/uk-household-water-report', 'standbysupplyco.com-pages-uk-household-water-repor'),
 ('uk-be-ready', 'E', 'Reino Unido', 'Rádio de emergência (Helora)', 'advertorial do National Risk Register, 39,90 a 99,90', 265, '1406547739212538', 'https://helorafit.com/pages/uk-emergency-radio-report', 'helorafit.com-pages-uk-emergency-radio-repor'),
 ('simone-fischer', 'E', 'Alemanha', 'Dispositivo antiengasgo (Schutzheld)', 'advertorial de história familiar; 306 ativos', 306, '1154015154457510', 'https://schutzheld.shop/', None),
 ('virest', 'F', 'Alemanha', 'Filtro de água', 'loja Shopify, 19,99 a 359,94 €', 51, '1262073640311958', 'https://virest.de/', None),
 ('krisensicher26', 'F', 'Alemanha', 'Mochila 72 h pronta', '239,99 €', 4, '1323820117479917', 'https://krisensicher26.de/', 'krisensicher26.de'),
 ('adventureshop', 'F', 'Áustria', 'Kit blackout', '"5 erros na preparação para blackout"', 80, '108232371692698', 'https://adventure-shop.at/', None),
 ('aquasecours', 'F', 'França', 'Kit de água AQUA-GS1', 'vídeo + página de produto', 103, '1457458994107079', 'https://aquasecours.com/products/kit-de-survie-aqua-gs1', None),
 ('page-survie-entre-fran-ais', 'F', 'França', 'Kit de água (Autarka)', '"Un seul kit pour toute la famille"', 16, '1347986611740847', 'https://autarka-shop.com/products/aqua-gs1', None),
 ('nord-survival', 'F', 'França/Holanda', 'Kit de 72 h com a "lista oficial"', '3 pacotes; 32 anúncios no histórico, pausados hoje', 0, '1421560424371386', 'https://nord-survival.com/products/kit-de-survie-72h', 'nord-survival.com-products-kit-de-survie-72h'),
 ('swiss-lifebox', 'F', 'Suíça (DE/FR/IT)', 'Rádio e kits', 'anúncio em 3 idiomas; 799 ativos', 799, '847142251827090', 'https://swiss-lifebox.ch/', None),
 ('le-magazine-de-la-survie', 'F', 'Suíça/França', 'Mesmos kits (página-revista)', '"Soyez prêt en cas d\'urgence"; 453 ativos', 453, '1007887629080572', 'https://swiss-lifebox.ch/', None),
 ('help-bag', 'F', 'Polônia', 'Mochila de evacuação (inclusive para empresas)', 'loja; 101 ativos; 74 dias', 101, '311162672720289', 'https://helpbag.eu/', None),
 ('bezpieczne-radio', 'F', 'Polônia', 'Rádio e mochila', '"comprei um e dei outro aos meus pais"', 56, '947723775092334', 'https://bezpieczneradio.pl/', None),
 ('zolano-b-d-przygotowany', 'F', 'Polônia', 'Mochila 92 em 1', 'loja', 6, '1385226154670354', 'https://zolano.pl/', None),
 ('hydromeal', 'F', 'Holanda', 'Comida de emergência', '"Comida de verdade, não ração"', 7, '1287034351171112', 'https://hydromeal.nl/', None),
 ('everyneeding', 'H', 'Global', 'Gadgets variados', 'loja genérica', 259, '107240791720404', 'https://everyneeding.com/', None),
 ('frenley', 'H', 'Holanda', 'Gadgets e presentes', 'loja genérica', 32, '595742516949217', 'https://frenley.nl/', None),
 ('topdeals', 'G', 'França', 'Le Manuel de Survie (PDF 383 páginas)', '29,99, entrega por e-mail, garantia 30 dias', 16, '544816535383698', 'https://le-manuel-de-survie.impultienda.ar/', 'le-manuel-de-survie.impultienda.ar'),
 ('superarte', 'G', 'Espanha', 'Casa Refugio (PDF de 72 h para imprimir)', 'US$ 14,90, garantia 15 dias', 21, '793179617219751', 'https://casarefugio.impultienda.ar/', 'casarefugio.impultienda.ar'),
 ('survival-school-sos2012', 'G', 'Itália', 'Cursos presenciais de sobrevivência', 'inscrição por WhatsApp', 103, '150763148333365', 'https://www.sos2012.it/', None),
]
out = []
for slug, g, pais, prod, funil, ativos, pid, landing, dossie in C:
    m = met.get(pid, {})
    out.append({'slug': slug, 'grupo': g, 'grupo_nome': G[g][0], 'pais': pais, 'produto': prod, 'funil': funil, 'ativos': ativos, 'page_id': pid,
                'landing': landing, 'dossie': dossie, 'dias_mais_antigo': m.get('dias_mais_antigo'), 'novos_7d': m.get('novos_7d'), 'pagina': m.get('pagina') or slug})
# Búnker en Casa (ES) não tem criativos baixados, mas entra no catálogo
out.append({'slug': 'bunker-en-casa', 'grupo': 'G', 'grupo_nome': G['G'][0], 'pais': 'Espanha', 'produto': 'Manual e caixas de corte de luz', 'funil': '96 anúncios ativos; criativos não baixados (fora da amostra)', 'ativos': 96, 'page_id': '1446919845163973', 'landing': None, 'dossie': None, 'dias_mais_antigo': None, 'novos_7d': None, 'pagina': 'Búnker en Casa'})
json.dump({'fonte_ativos': 'conector Meta Ads, anúncios ATIVOS por página, sem filtro de país, 16/11/2026', 'grupos': {k: {'nome': v[0], 'leitura': v[1]} for k, v in G.items()}, 'concorrentes': out}, open(D + 'concorrentes.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'concorrentes')
