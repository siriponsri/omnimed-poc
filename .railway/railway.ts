import { defineRailway, project, service, github, postgres } from 'railway/iac';

// Optional deployment tooling only. Product images never import this package.
export default defineRailway((ctx) => {
  if (ctx.environment !== 'demo') throw new Error('Select a dedicated Railway environment named demo.');
  const repository = process.env.OMNIMED_GITHUB_REPOSITORY;
  if (!repository || !/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(repository)) {
    throw new Error('Set OMNIMED_GITHUB_REPOSITORY to the actual owner/repository before planning.');
  }
  const db = postgres('Postgres');
  const backend = service('backend', {
    source: github(repository, { branch: 'main', rootDirectory: '/' }),
    build: { builder: 'DOCKERFILE', dockerfilePath: 'backend/Dockerfile' },
    preDeploy: ['alembic -c db/alembic.ini upgrade head', 'python scripts/seed_demo.py'],
    start: 'python scripts/start_backend.py',
    healthcheck: '/api/health/ready',
    healthcheckTimeout: 120,
    replicas: 1,
    deploy: { restartPolicyType: 'ON_FAILURE', restartPolicyMaxRetries: 3 },
    env: {
      APP_ENV: 'demo', SYNTHETIC_DEMO_ONLY: 'true', PORT: '8000',
      DATABASE_URL: db.env.DATABASE_URL,
    },
  });
  const frontend = service('frontend', {
    source: github(repository, { branch: 'main', rootDirectory: '/' }),
    build: { builder: 'DOCKERFILE', dockerfilePath: 'frontend/Dockerfile' },
    start: 'node server.js', healthcheck: '/', healthcheckTimeout: 120, replicas: 1,
    deploy: { restartPolicyType: 'ON_FAILURE', restartPolicyMaxRetries: 3 },
    env: {
      NODE_ENV: 'production', NEXT_TELEMETRY_DISABLED: '1', HOSTNAME: '0.0.0.0', PORT: '3000',
      API_INTERNAL_HOST: backend.env.RAILWAY_PRIVATE_DOMAIN, API_INTERNAL_PORT: '8000',
    },
  });
  return project('omnimed-demo', { resources: [db, backend, frontend] });
});
