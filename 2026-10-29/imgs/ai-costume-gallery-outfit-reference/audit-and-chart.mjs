import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire(`${process.argv[2]}/package.json`);
const { createCanvas } = require('@napi-rs/canvas');
const directory = path.dirname(fileURLToPath(import.meta.url));
const sourceUrl = 'https://ai-costume-gallery.pages.dev/';
const response = await fetch(sourceUrl);
if (!response.ok) throw new Error(`Source HTTP ${response.status}`);
const html = await response.text();

// Read JSON literals only; never execute the downloaded site's JavaScript.
function literal(name) {
  const line = html.split('\n').find(value => value.startsWith(`const ${name}=`));
  if (!line) throw new Error(`Missing ${name}`);
  return JSON.parse(line.slice(line.indexOf('=') + 1).replace(/;\s*$/, ''));
}
const meta = literal('META');
const rows = literal('D');
const counts = Object.fromEntries(meta.cats.map(category => [category,
  rows.filter(row => row['カテゴリ'] === category).length]));
const denim = rows.filter(row => row['キーワード'].split(' ').some(word => word.startsWith('denim')));
const report = {
  sourceUrl,
  retrievedAtUtc: new Date().toISOString(),
  reviewDateMelbourne: '2026-10-29',
  sourceHtmlSha256: crypto.createHash('sha256').update(html).digest('hex'),
  records: rows.length,
  uniqueIds: new Set(rows.map(row => row.id)).size,
  categoryCounts: counts,
  declaredCountsMatch: meta.total === rows.length && meta.cats.every(c => counts[c] === meta.counts[c]),
  probes: { denimAll: denim.length, denimSpring: denim.filter(row => row['カテゴリ'] === '春').length },
  limits: 'Metadata counts only. No bulk image download, full image QA, model generation test, or rights clearance.',
};
if (!report.declaredCountsMatch || report.uniqueIds !== report.records) throw new Error('Metadata checks failed');
fs.writeFileSync(path.join(directory, 'data-audit.json'), `${JSON.stringify(report, null, 2)}\n`);

const canvas = createCanvas(1440, 1120);
const ctx = canvas.getContext('2d');
ctx.fillStyle = '#ffffff';
ctx.fillRect(0, 0, 1440, 1120);
function text(value, x, y, size = 24, color = '#202525', weight = 'normal') {
  ctx.font = `${weight} ${size}px sans-serif`;
  ctx.fillStyle = color;
  ctx.fillText(value, x, y);
}
text('AI Costume Gallery: a wardrobe reference library', 64, 72, 38, '#202525', 'bold');
text('COSTUME-DB-01 | Public-page metadata checked 29 October 2026', 64, 111, 21, '#65716f');
text(report.records.toLocaleString('en-US'), 64, 194, 56, '#23775d', 'bold');
text('outfit image records', 64, 232);
text('8', 570, 194, 56, '#256fa0', 'bold');
text('categories', 570, 232);
text(meta.cats.slice(0, 4).reduce((sum, category) => sum + counts[category], 0).toLocaleString('en-US'),
  1060, 194, 56, '#202525', 'bold');
text('seasonal outfits', 1060, 232);
ctx.strokeStyle = '#dbe2df';
ctx.beginPath(); ctx.moveTo(64, 269); ctx.lineTo(1376, 269); ctx.stroke();
const labels = ['Spring', 'Summer', 'Autumn', 'Winter', 'Lingerie', 'Party', 'Swimwear', 'Sexy (site label)'];
const colors = ['#23775d', '#256fa0', '#996e2f', '#6958a1', '#788282', '#ac5466', '#26858b', '#788282'];
meta.cats.forEach((category, i) => {
  const y = 315 + i * 58;
  text(labels[i], 64, y + 24, 23);
  ctx.fillStyle = '#eef2f0'; ctx.fillRect(330, y, 900, 32);
  ctx.fillStyle = colors[i]; ctx.fillRect(330, y, counts[category] / 260 * 900, 32);
  text(String(counts[category]), 1260, y + 25, 24, '#202525', 'bold');
});
ctx.strokeStyle = '#dbe2df';
ctx.beginPath(); ctx.moveTo(64, 815); ctx.lineTo(1376, 815); ctx.stroke();
text('Keep reference roles separate', 64, 862, 29, '#202525', 'bold');
text('Character identity + outfit reference + pose / scene instructions', 64, 912, 28, '#256fa0');
text('The receiving image model must still preserve identity, garment details, and continuity.', 64, 958, 23);
text('Original chart using aggregate counts; no source garment images are reproduced.', 64, 1030, 20, '#65716f');
text('Counts describe catalog records, not unique designs, 3D meshes, or verified generation results.', 64, 1066, 20, '#65716f');
fs.writeFileSync(path.join(directory, 'catalog-and-workflow.png'), canvas.toBuffer('image/png'));
console.log(JSON.stringify(report, null, 2));
