import fs from 'node:fs';
import { createRequire } from 'node:module';

// The canvas package comes from the desktop app's bundled dependency directory.
const require = createRequire(`${process.argv[2]}/package.json`);
const { createCanvas } = require('@napi-rs/canvas');
const report = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const canvas = createCanvas(1440, 930);
const ctx = canvas.getContext('2d');
ctx.fillStyle = '#ffffff';
ctx.fillRect(0, 0, 1440, 930);

function text(value, x, y, size = 24, color = '#202525', weight = 'normal') {
  ctx.fillStyle = color;
  ctx.font = `${weight} ${size}px sans-serif`;
  ctx.fillText(value, x, y);
}
text('AI Pose Gallery: what the numbers count', 65, 72, 38, '#202525', 'bold');
text('Independent metadata audit | 28 October 2026 | commit 072a369', 65, 112, 20, '#63706d');
text(String(report.groups), 65, 193, 58, '#26755b', 'bold');
text('pose groups', 65, 230);
text(String(report.records), 490, 193, 58, '#276591', 'bold');
text('image / angle records', 490, 230);
text(String(report.referencedImagePaths), 990, 193, 58, '#202525', 'bold');
text('tracked image paths', 990, 230);
ctx.strokeStyle = '#d9e2de';
ctx.beginPath(); ctx.moveTo(65, 270); ctx.lineTo(1375, 270); ctx.stroke();
text('Records by collection', 65, 323, 28, '#202525', 'bold');
const labels = new Map([
  ['全身单人・标准系', 'Full-body / standard'],
  ['全身单人・性感系', 'Full-body / alternate'],
  ['上半身单人', 'Upper-body'],
  ['双人缠绵', 'Paired collection'],
]);
const colors = ['#26755b', '#276591', '#687779', '#a66653'];
const rows = [...report.collections].sort((a, b) =>
  [...labels.keys()].indexOf(a.name) - [...labels.keys()].indexOf(b.name));
rows.forEach((row, i) => {
  const y = 378 + i * 72;
  text(labels.get(row.name), 65, y + 21, 22);
  ctx.fillStyle = '#edf1ef'; ctx.fillRect(340, y - 3, 680, 32);
  ctx.fillStyle = colors[i]; ctx.fillRect(340, y - 3, row.records / 400 * 680, 32);
  text(`${row.records} records / ${row.groups} groups`, 1040, y + 22, 21);
});
text('View coverage', 65, 711, 28, '#202525', 'bold');
const full = report.angleCoverage[5];
text(`${full} groups have five angles; ${report.angleCoverage[4]} group has four.`, 65, 755, 25);
text('A view collection is not a 3D mesh, rig, or animation sequence.', 65, 800, 23, '#276591');
text('Original chart from aggregate counts only. Collection labels shortened for neutral presentation.',
  65, 861, 18, '#63706d');
text('No source pose images or raw metadata are reproduced in this figure.', 65, 891, 18, '#63706d');
fs.writeFileSync(process.argv[4], canvas.toBuffer('image/png'));
