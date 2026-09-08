export type Readiness = { status: 'ready' | 'unavailable' };
// Public allowlist: never forward database exceptions, URLs, or arbitrary upstream payloads.
export function parseReadiness(ok: boolean, body: unknown): Readiness {
  return { status: ok && typeof body === 'object' && body !== null && 'status' in body && body.status === 'ready' ? 'ready' : 'unavailable' };
}
