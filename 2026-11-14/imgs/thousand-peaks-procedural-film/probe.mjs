import puppeteer from 'puppeteer-core';
import { mkdir } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';

const html = resolve(process.argv[2]);
const out = resolve(process.argv[3]);
await mkdir(out, { recursive: true });
const chrome = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const browser = await puppeteer.launch({
  executablePath: chrome,
  headless: true,
  args: ['--enable-gpu', '--ignore-gpu-blocklist', '--use-angle=metal', '--enable-webgl',
    '--allow-file-access-from-files'],
});
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });
  const network = [], errors = [];
  page.on('request', req => { if (/^https?:/.test(req.url())) network.push(req.url()); });
  page.on('pageerror', err => errors.push(err.message));
  await page.setOfflineMode(true);
  await page.goto(pathToFileURL(html).href + '?shot=1&scale=1&quiet=1',
    { waitUntil: 'load', timeout: 60000 });
  await page.waitForFunction('window.K?.ready', { timeout: 45000 });
  const capture = async (t, name) => {
    const errs = await page.evaluate(t => {
      K.debug.renderAt(t);
      return K.debug.renderAt(t);
    }, t);
    if (errs.length) throw new Error(JSON.stringify(errs));
    const png = await page.screenshot({ type: 'png', path: join(out, name + '.png') });
    return createHash('sha256').update(png).digest('hex');
  };
  const first = await capture(25, 'first-25');
  const second = await capture(25, 'second-25');
  await capture(85, 'dusk-85');
  const returned = await capture(25, 'returned-25');
  await page.evaluate(() => { K.debug.cam = [30, 6, 150, 0, 80, 10, 50]; });
  const alternate = await capture(25, 'alternate-25');
  const film = await page.evaluate(() => ({
    version: THREE.REVISION, shots: K.film.shots.length, duration: K.DUR,
  }));
  console.log(JSON.stringify({
    immediateMatch: first === second, afterDuskMatch: first === returned,
    cameraChanged: first !== alternate, httpRequests: network, pageErrors: errors, film,
  }));
} finally {
  await browser.close();
}
