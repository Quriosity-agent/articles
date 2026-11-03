import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(`${process.argv[2]}/package.json`);
const sharp = require('sharp');
const directory = path.dirname(fileURLToPath(import.meta.url));
for (const name of ['git-packfile-layout', 'pando-branch-packs']) {
  const input = path.join(directory, `${name}.svg`);
  const output = path.join(directory, `${name}.png`);
  await sharp(input, { density: 150 }).resize({ width: 1800 }).flatten({ background: '#ffffff' }).png().toFile(output);
  const metadata = await sharp(output).metadata();
  console.log(`${name}: ${metadata.width} x ${metadata.height}, ${metadata.format}`);
}
