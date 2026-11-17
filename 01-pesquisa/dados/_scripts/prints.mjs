// Tira prints do topo das páginas: fontes (notícias, documentos) e páginas de vendas dos concorrentes.
// Não clica em nada: esconde barras fixas (cookies, avisos) só para a foto ficar limpa.
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
const require = createRequire('C:/Users/Familia/.claude/skills/raio-x-infoprodutos/package.json');
const { chromium, devices } = require('playwright');
const D = 'E:/Raio-X Survival Europa/01-pesquisa/dados/';
const fontes = JSON.parse(fs.readFileSync(D + 'fontes.json', 'utf8')).fontes;
const cat = JSON.parse(fs.readFileSync(D + 'concorrentes.json', 'utf8')).concorrentes;
const jobs = [];
for (const f of fontes) if (!/youtube\.com|\.pdf$/i.test(f.url)) jobs.push({ tipo: 'fonte', id: f.id, url: f.url, out: D + `prints/fontes/${f.id}.jpg`, mobile: false });
for (const c of cat) if (c.landing) jobs.push({ tipo: 'concorrente', id: c.slug, url: c.landing, out: D + `prints/concorrentes/${c.slug}.jpg`, mobile: true });
fs.mkdirSync(D + 'prints/fontes', { recursive: true }); fs.mkdirSync(D + 'prints/concorrentes', { recursive: true });
const browser = await chromium.launch({ headless: true });
const res = fs.existsSync(D + 'prints/prints.json') ? JSON.parse(fs.readFileSync(D + 'prints/prints.json', 'utf8')) : {};
async function um(j) {
  if (fs.existsSync(j.out) && res[j.id]?.ok) return;
  const ctx = await browser.newContext(j.mobile ? { ...devices['iPhone 13'], locale: 'en-GB' } : { viewport: { width: 1280, height: 820 }, locale: 'en-GB', userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36' });
  const page = await ctx.newPage();
  try {
    await page.goto(j.url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForTimeout(5000);
    await page.evaluate(() => {
      for (const el of document.querySelectorAll('body *')) {
        const s = getComputedStyle(el);
        if ((s.position === 'fixed' || s.position === 'sticky') && el.getBoundingClientRect().height > 60) el.style.setProperty('display', 'none', 'important');
        if (/cookie|consent|gdpr|didomi|onetrust|cmp/i.test((el.id || '') + ' ' + (el.className || ''))) el.style.setProperty('display', 'none', 'important');
      }
      document.documentElement.style.overflow = 'auto'; document.body.style.overflow = 'auto';
    });
    await page.waitForTimeout(500);
    await page.screenshot({ path: j.out, type: 'jpeg', quality: 62 });
    const titulo = await page.title();
    const txt = (await page.evaluate(() => document.body.innerText || '')).slice(0, 400);
    const bloqueado = /access denied|forbidden|captcha|just a moment|are you a robot|verify you are human|403|404 not found|page not found/i.test(titulo + ' ' + txt);
    res[j.id] = { ok: !bloqueado, tipo: j.tipo, url: j.url, titulo, bloqueado };
  } catch (e) { res[j.id] = { ok: false, tipo: j.tipo, url: j.url, erro: String(e).slice(0, 120) }; }
  console.log(j.tipo, j.id, res[j.id].ok ? 'ok' : 'falhou', (res[j.id].titulo || res[j.id].erro || '').slice(0, 60));
  fs.writeFileSync(D + 'prints/prints.json', JSON.stringify(res, null, 1));
  await ctx.close();
}
const fila = [...jobs];
await Promise.all([1, 2, 3].map(async () => { while (fila.length) await um(fila.shift()); }));
await browser.close();
console.log('FIM', Object.values(res).filter(r => r.ok).length, 'de', jobs.length);
