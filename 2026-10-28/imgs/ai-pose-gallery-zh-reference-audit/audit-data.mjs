import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const root = path.resolve(process.argv[2]);
const read = file => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
const data = read('data/pose-zh.json');
const original = read('data/pose.json');
const groups = new Map();
const systems = new Map();
for (const item of data) {
  const key = `${item.体系}|${item.姿势编号 || item.id}`;
  if (!groups.has(key)) groups.set(key, []);
  groups.get(key).push(item);
  const entry = systems.get(item.体系) || { records: 0, groups: new Set() };
  entry.records++;
  entry.groups.add(key);
  systems.set(item.体系, entry);
}
const tracked = new Set(execFileSync('git', ['ls-tree', '-r', '--name-only', 'HEAD'],
  { cwd: root, encoding: 'utf8' }).trim().split('\n'));
const paths = data.flatMap(item => [item.缩略图, item.原图]);
const coverage = {};
for (const items of groups.values()) {
  const count = new Set(items.map(item => item.角度)).size;
  coverage[count] = (coverage[count] || 0) + 1;
}
const checks = {
  records1439: data.length === 1439,
  idsUnique: new Set(data.map(item => item.id)).size === data.length,
  groups288: groups.size === 288,
  sourceOrderAndPathsPreserved: original.length === data.length && original.every((item, i) =>
    item.id === data[i].id && item.サムネ === data[i].缩略图 && item.原寸 === data[i].原图),
  referencedPathsUnique: new Set(paths).size === 2878,
  referencedPathsTracked: paths.every(file => tracked.has(file)),
  fiveAngleGroups287: coverage[5] === 287,
  fourAngleGroups1: coverage[4] === 1,
};
const report = {
  commit: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim(),
  records: data.length,
  groups: groups.size,
  uniqueIds: new Set(data.map(item => item.id)).size,
  uniqueJapaneseNames: new Set(original.map(item => item.ポーズ名)).size,
  uniqueChineseNames: new Set(data.map(item => item.姿势名称)).size,
  categories: new Set(data.map(item => item.分类)).size,
  angles: new Set(data.map(item => item.角度)).size,
  referencedImagePaths: paths.length,
  angleCoverage: coverage,
  collections: [...systems].map(([name, value]) => ({
    name, records: value.records, groups: value.groups.size,
  })),
  checks,
  allChecksPass: Object.values(checks).every(Boolean),
  scope: 'Metadata and Git tree only; no image decode, visual consistency, or model generation test.',
};
console.log(JSON.stringify(report, null, 2));
if (!report.allChecksPass) process.exitCode = 1;
