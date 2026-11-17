// Print do topo de cada tela da pesquisa (miniaturas do roteiro). Esconde a barra lateral para a miniatura mostrar o conteúdo.
import { createRequire } from 'node:module';
import fs from 'node:fs';
const require = createRequire('C:/Users/Familia/.claude/skills/raio-x-infoprodutos/package.json');
const { chromium } = require('playwright');
const PG = 'file:///E:/Raio-X%20Survival%20Europa/01-pesquisa/paginas/';
const OUT = 'E:/Raio-X Survival Europa/01-pesquisa/dados/prints/telas/';
fs.mkdirSync(OUT, { recursive: true });
const telas = ['etapa-1-noticias', 'fontes', 'etapa-2-demanda', 'etapa-2-europa', 'voz-do-publico', 'etapa-4-concorrentes', 'criativos-por-concorrente', 'etapa-5-funis', 'etapa-6-cpm', 'escolha-oferta'];
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1100, height: 690 } });
for (const t of telas) {
  await p.goto(PG + t + '.html'); await p.waitForTimeout(700);
  await p.addStyleTag({ content: '.side,.topbar,.bottomnav,.next-action{display:none!important}.main{margin-left:0!important}.app{display:block!important}' });
  await p.waitForTimeout(200);
  await p.screenshot({ path: OUT + t + '.jpg', type: 'jpeg', quality: 70 });
  console.log(t);
}
await b.close();
