// Abre a página de vendas, acha o link de checkout e grava print + texto do checkout (sem preencher nada).
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
const require = createRequire('C:/Users/Familia/.claude/skills/raio-x-infoprodutos/package.json');
const { chromium, devices } = require('playwright');
const [,, urlsArg, outDir] = process.argv;
const urls = urlsArg.split(';').filter(Boolean);
const RX = /checkout-ds24|digistore24\.com\/(product|order)|pay\.clickbank|clkbank|\/checkout|\/order|cart|buy|orderform|secure\./i;
fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const res = [];
for (const u of urls) {
  const slug = u.replace(/^https?:\/\/(www\.)?/, '').replace(/[^a-z0-9]+/gi, '-').slice(0, 50).replace(/-$/, '');
  const ctx = await browser.newContext({ ...devices['iPhone 13'], locale: 'en-US' });
  const page = await ctx.newPage();
  const r = { url: u, slug, checkout: null, erro: null };
  try {
    await page.goto(u, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(6000);
    const links = await page.$$eval('a[href]', as => as.map(a => ({ t: (a.innerText || '').trim().slice(0, 80), h: a.href })));
    r.links_checkout = [...new Map(links.filter(l => /checkout-ds24|digistore24\.com\/(product|order)|pay\.clickbank|clkbank|\/checkout|orderform|\/cart|\/order|buygoods|sticky|secure/i.test(l.h)).map(l => [l.h.split('?')[0], l])).values()].slice(0, 6);
    const alvo = r.links_checkout[0];
    if (alvo) {
      await page.goto(alvo.h, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForTimeout(8000);
      r.checkout = { url: page.url(), titulo: await page.title() };
      r.checkout.texto = (await page.evaluate(() => document.body.innerText)).slice(0, 6000);
      await page.screenshot({ path: path.join(outDir, `${slug}-checkout.jpg`), fullPage: true, type: 'jpeg', quality: 60 });
      r.checkout.print = `${slug}-checkout.jpg`;
    }
  } catch (e) { r.erro = String(e).slice(0, 200); }
  res.push(r);
  console.log(u, '->', r.checkout ? r.checkout.url.slice(0, 90) : 'sem checkout', r.erro || '');
  await ctx.close();
}
await browser.close();
fs.writeFileSync(path.join(outDir, 'checkouts.json'), JSON.stringify(res, null, 1));
