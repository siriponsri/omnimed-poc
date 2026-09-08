import assert from 'node:assert/strict';
import test from 'node:test';
import { parseReadiness } from '../lib/readiness.ts';

test('readiness is fail closed and only accepts the explicit ready response', () => {
  for (const body of [null, {}, { status: 'alive' }, { status: true }, 'ready', []]) {
    assert.deepEqual(parseReadiness(true, body), { status: 'unavailable' });
  }
  assert.deepEqual(parseReadiness(false, { status: 'ready' }), { status: 'unavailable' });
  assert.deepEqual(parseReadiness(true, { status: 'ready' }), { status: 'ready' });
});
test('upstream diagnostic/credential fields never reach the browser status response', () => {
  assert.deepEqual(parseReadiness(true, { status: 'ready', database_url: 'sensitive', exception: 'private' }), { status: 'ready' });
});
