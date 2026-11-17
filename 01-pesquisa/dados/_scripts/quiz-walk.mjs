// Percorre um funil de quiz clicando na 1ª opção de cada pergunta, grava print e texto de cada etapa. Para antes de qualquer pagamento e não digita e-mail real.
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
const require = createRequire('C:/Users/Familia/.claude/skills/raio-x-infoprodutos/package.json');
const { chromium, devices } = require('playwright');
const [,, urlsArg, outDir] = process.argv;
fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const res = [];
for (const u of urlsArg.split(';').filter(Boolean)) {
  const slug = u.replace(/^https?:\/\/(www\.)?/, '').replace(/[^a-z0-9]+/gi, '-').slice(0, 40).replace(/-$/, '');
  const ctx = await browser.newContext({ ...devices['iPhone 13'], locale: 'en-US' });
  const page = await ctx.newPage();
  const net = new Set();
  page.on('request', r => { const x = r.url(); if (/wistia|vturb|vidalytics|youtube|vimeo|checkout|clickbank|digistore|ds24|buygoods|cart/i.test(x)) net.add(x.split('?')[0].slice(0, 140)); });
  const passos = [];
  try {
    await page.goto(u, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(5000);
    for (let i = 0; i < 14; i++) {
      const txt = (await page.evaluate(() => document.body.innerText)).slice(0, 1500);
      const shot = `${slug}-passo-${String(i).padStart(2, '0')}.jpg`;
      await page.screenshot({ path: path.join(outDir, shot), type: 'jpeg', quality: 55 });
      passos.push({ i, url: page.url(), texto: txt, print: shot });
      if (/card number|credit card|cvv|pay now|complete order/i.test(txt)) break;
      // campo de e-mail: não preencher, registrar e parar
      const email = await page.$('input[type=email], input[name*=email i]');
      if (email && await email.isVisible()) { passos[passos.length - 1].nota = 'pede e-mail aqui (não preenchido)'; break; }
      const cand = await page.$$('button:visible, a:visible, [role=button]:visible, label:visible, .answer:visible, [class*=option]:visible, [class*=answer]:visible');
      let clicou = false;
      for (const c of cand) {
        const t = ((await c.innerText().catch(() => '')) || '').trim();
        if (!t || t.length > 120 || /privacy|terms|contact|disclaimer|cookie/i.test(t)) continue;
        try { await c.click({ timeout: 3000 }); clicou = true; break; } catch {}
      }
      if (!clicou) break;
      await page.waitForTimeout(3500);
    }
  } catch (e) { passos.push({ erro: String(e).slice(0, 200) }); }
  res.push({ url: u, slug, passos, rede: [...net] });
  console.log(u, passos.length, 'passos', [...net].slice(0, 4).join(' '));
  await ctx.close();
}
await browser.close();
fs.writeFileSync(path.join(outDir, 'quiz.json'), JSON.stringify(res, null, 1));
