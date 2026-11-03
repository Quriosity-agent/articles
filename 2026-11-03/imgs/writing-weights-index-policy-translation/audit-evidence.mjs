import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { strict as assert } from 'node:assert';

const directory = path.dirname(fileURLToPath(import.meta.url));
const commit = '4d09ba6d6a7e891dd8063974dfe81b3d78e3494f';
const base = `https://raw.githubusercontent.com/RikiyaT/lm_understand-logs/${commit}/exp5_write_from_scratch`;
async function json(relative) {
  const response = await fetch(`${base}/${relative}`);
  if (!response.ok) throw new Error(`HTTP ${response.status}: ${relative}`);
  return response.json();
}
const evaluation = await json('eval/minatar_eval.json');
const application = await json('runs/breakout/apply.json');
const run = await json('runs/breakout/reply/run.json');
const parameters = 600 * 32 + 32 + 32 * 32 + 32 + 32 * 6 + 6;
assert.equal(parameters, 20486);
assert.equal(application.parameters, parameters);
assert.equal(application.edit_report.applied, 92);
assert.equal(application.edit_report.errors.length, 0);
assert.equal(application.nonzero_total, 815);
assert.equal(run.audit.tool_free, true);

const originalExperiment = Object.fromEntries(Object.entries(evaluation).map(([game, rows]) => {
  const best = prefix => Math.max(...Object.entries(rows).filter(([name]) => name.startsWith(prefix)).map(([, row]) => row.mean));
  assert.equal(rows.hand.episodes, 1000);
  return [game, { generatedMean: rows.hand.mean, episodes: rows.hand.episodes,
    bestPpo100M: best('ppo100_'), bestPpo500M: best('ppo500_') }];
}));
assert.equal(originalExperiment.breakout.generatedMean.toFixed(1), '517.4');
assert.equal(originalExperiment.seaquest.generatedMean.toFixed(1), '53.1');
assert.equal(originalExperiment.asterix.generatedMean.toFixed(1), '53.2');

// These are transcribed chart values, not outputs of a model evaluation here.
const chartRows = [
  ['GPT-6 Astra', 60.7, 85.0, 'proprietary'],
  ['Gemini 4 Carbon', 57.7, 68.6, 'proprietary'],
  ['Claude Opus 5.5', 51.2, 61.6, 'proprietary'],
  ['Gemini 4 Argon', 36.0, 70.4, 'proprietary'],
  ['Kimi K3.1 Pro', 29.8, 49.8, 'proprietary'],
  ['Qwen3.8 2.4T A95B', 12.5, 36.8, 'open-weight'],
  ['DeepSeek V4.1 Flash', 10.0, 31.6, 'open-weight'],
  ['GLM 5.3', 6.2, 45.2, 'open-weight'],
  ['Mistral Large 4', 2.6, 37.1, 'open-weight'],
  ['MiniMax M3.1 Flash', 0.2, 26.7, 'open-weight'],
  ['Step 5 Preview', 0.1, 34.8, 'open-weight'],
].map(([model, weightsIndex, policyIndex, authorGroup]) => ({ model, weightsIndex, policyIndex, authorGroup }));
const squash = q => 100 * q / (1 + q);
assert.equal(squash(0), 0);
assert.equal(squash(1), 50);
assert.equal(squash(3), 75);
const report = {
  reviewDateMelbourne: '2026-11-03',
  retrievedAtUtc: new Date().toISOString(),
  originalResearchCommit: commit,
  originalExperiment,
  sampledBreakoutRun: { parameters, appliedStatements: application.edit_report.applied,
    parserErrors: application.edit_report.errors.length, nonzeroWeights: application.nonzero_total,
    authorToolAudit: run.audit.tool_free },
  indexFormulaChecks: { q0: squash(0), q1: squash(1), q3: squash(3) },
  chartRows,
  limits: 'Read-only JSON checks and chart transcription. No model invocation, game episodes, training, parser execution, or independent performance reproduction. Original experiment logs are not the cross-model index harness.',
};
fs.writeFileSync(path.join(directory, 'evidence-audit.json'), `${JSON.stringify(report, null, 2)}\n`);
console.log(JSON.stringify({ originalExperiment, parameters, sampledRunChecks: 'passed', indexChecks: 'passed', chartRows: chartRows.length }, null, 2));
