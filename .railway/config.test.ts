import assert from 'node:assert/strict';
import { test } from 'node:test';
import { createRailwayContext, project } from 'railway/iac';
import spec from './railway.ts';

const evaluate = (environment: string) => spec(createRailwayContext({ environment, command: 'plan' }), project);

test('rejects non-demo environments and missing repository before provisioning', async () => {
  const prior = process.env.OMNIMED_GITHUB_REPOSITORY;
  try {
    delete process.env.OMNIMED_GITHUB_REPOSITORY;
    await assert.rejects(async () => evaluate('production'), /dedicated Railway environment/);
    await assert.rejects(async () => evaluate('demo'), /actual owner\/repository/);
    process.env.OMNIMED_GITHUB_REPOSITORY = 'https://github.com/example/repo';
    await assert.rejects(async () => evaluate('demo'), /actual owner\/repository/);
  } finally {
    if (prior === undefined) delete process.env.OMNIMED_GITHUB_REPOSITORY;
    else process.env.OMNIMED_GITHUB_REPOSITORY = prior;
  }
});

test('evaluates GitHub Docker services with private references and guarded seed startup', async () => {
  const prior = process.env.OMNIMED_GITHUB_REPOSITORY;
  try {
    process.env.OMNIMED_GITHUB_REPOSITORY = 'synthetic-example/omnimed';
    const definition = await evaluate('demo');
    const resources = definition.resources?.flat() || [];
    assert.equal(resources.length, 3);
    const backend = resources.find((r) => r.name === 'backend');
    const frontend = resources.find((r) => r.name === 'frontend');
    assert.ok(backend?.type === 'service' && frontend?.type === 'service');
    assert.equal(backend.source?.repo, 'synthetic-example/omnimed');
    assert.equal(backend.source?.rootDirectory, '/');
    assert.equal(frontend.source?.rootDirectory, '/');
    assert.equal(backend.build?.dockerfilePath, 'backend/Dockerfile');
    assert.equal(frontend.build?.dockerfilePath, 'frontend/Dockerfile');
    assert.equal(backend.deploy?.healthcheckPath, '/api/health/ready');
    assert.deepEqual(backend.deploy?.preDeployCommand, ['alembic -c db/alembic.ini upgrade head', 'python scripts/seed_demo.py']);
    assert.deepEqual(backend.variables?.DATABASE_URL, { type: 'reference', resource: 'database.Postgres', output: 'DATABASE_URL' });
    assert.deepEqual(backend.variables?.SYNTHETIC_DEMO_ONLY, { type: 'literal', value: 'true' });
    assert.deepEqual(frontend.variables?.API_INTERNAL_HOST, { type: 'reference', resource: 'service.backend', output: 'RAILWAY_PRIVATE_DOMAIN' });
    assert.equal(backend.networking?.serviceDomains, undefined);
    assert.equal(frontend.variables?.DATABASE_URL, undefined);
  } finally {
    if (prior === undefined) delete process.env.OMNIMED_GITHUB_REPOSITORY;
    else process.env.OMNIMED_GITHUB_REPOSITORY = prior;
  }
});
