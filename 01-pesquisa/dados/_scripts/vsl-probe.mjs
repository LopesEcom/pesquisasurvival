// Abre páginas de VSL, identifica o player e a duração do vídeo, espera o botão aparecer e grava print do topo.
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
const require = createRequire('C:/Users/Familia/.claude/skills/raio-x-infoprodutos/package.json');
const { chromium, devices } = require('playwright');
const [,, urlsArg, outDir] = process.argv;
fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const out = [];
for (const u of urlsArg.split(';').filter(Boolean)) {
  const slug = u.replace(/^https?:\/\/(www\.)?/, '').replace(/[^a-z0-9]+/gi, '-').slice(0, 50).replace(/-$/, '');
  const ctx = await browser.newContext({ ...devices['iPhone 13'], locale: 'en-US' });
  const page = await ctx.newPage();
  const net = new Set();
  page.on('request', r => { const x = r.url(); if (/vturb|converteai|vidalytics|wistia|vimeo|youtube|jwplayer|brightcove|m3u8|\.mp4|smartplayer|bunny|cloudflarestream|mediadelivery/i.test(x)) net.add(x.split('?')[0].slice(0, 140)); });
  const r = { url: u, slug };
  try {
    await page.goto(u, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(12000);
    r.titulo = await page.title();
    r.iframes = await page.$$eval('iframe', fs => fs.map(f => f.src).filter(Boolean).slice(0, 8));
    r.videos = await page.$$eval('video', vs => vs.map(v => ({ src: (v.currentSrc || v.src || '').slice(0, 140), dur: v.duration })));
    r.headline = (await page.evaluate(() => document.body.innerText)).slice(0, 1200);
    r.links_compra = await page.$$eval('a[href]', as => as.filter(a => /checkout|clickbank|digistore|ds24|order|buy|cart|buygoods/i.test(a.href)).map(a => a.href.slice(0, 140)).slice(0, 5));
    r.botoes_ocultos = await page.$$eval('[style*="display: none"], .hidden, [class*="delay"], [class*="esconder"], [class*="smartplayer-scroll"]', es => es.length);
    await page.screenshot({ path: path.join(outDir, slug + '-topo.jpg'), type: 'jpeg', quality: 60 });
    r.print = slug + '-topo.jpg';
  } catch (e) { r.erro = String(e).slice(0, 200); }
  r.rede_video = [...net].slice(0, 10);
  out.push(r);
  console.log(u, '|', r.titulo, '| videos', JSON.stringify(r.videos), '| rede', r.rede_video.length);
  await ctx.close();
}
await browser.close();
fs.writeFileSync(path.join(outDir, 'vsl-probe.json'), JSON.stringify(out, null, 1));
