import test from 'node:test';
import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);

test('Level 3 provenance is internally complete', async () => {
  const { stdout, stderr } = await execFileAsync(process.execPath, ['scripts/validate-provenance.mjs']);
  assert.equal(stderr, '');
  assert.match(stdout, /Validated Level 3 provenance: 8 domains, 16 authorities, 15 Otherworld source groups and 31 public files\./);
});
