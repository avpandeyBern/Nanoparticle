const { chromium } = require('/opt/node-tools/node_modules/playwright/index.js');
const { readFileSync } = require('fs');
(async () => {
  const [,, svgPath, outPath, widthPx] = process.argv;
  const svg = readFileSync(svgPath, 'utf8');
  const m = svg.match(/viewBox="([\d.\-]+) ([\d.\-]+) ([\d.\-]+) ([\d.\-]+)"/);
  const vbw = m ? parseFloat(m[3]) : 1000, vbh = m ? parseFloat(m[4]) : 1000;
  const W = parseInt(widthPx), H = Math.round(W * vbh / vbw);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  const html = `<!doctype html><html><head><meta charset="utf8"><style>*{margin:0;padding:0}html,body{width:${W}px;height:${H}px;overflow:hidden;background:#fff}svg{width:${W}px;height:${H}px;display:block}</style></head><body>${svg}</body></html>`;
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.screenshot({ path: outPath, clip: { x:0, y:0, width:W, height:H } });
  await browser.close();
  console.log(`wrote ${outPath} ${W}x${H}`);
})();
