import { parseReadiness } from '../../../lib/readiness';
export const dynamic = 'force-dynamic';
export async function GET() {
  try {
    const origin = process.env.API_INTERNAL_URL || (process.env.API_INTERNAL_HOST ? `http://${process.env.API_INTERNAL_HOST}:${process.env.API_INTERNAL_PORT || '8000'}` : 'http://127.0.0.1:8000');
    const response = await fetch(`${origin}/api/health/ready`, { cache: 'no-store', signal: AbortSignal.timeout(4000) });
    const result = parseReadiness(response.ok, await response.json());
    return Response.json(result, { status: result.status === 'ready' ? 200 : 503, headers: { 'Cache-Control': 'no-store' } });
  } catch {
    return Response.json({ status: 'unavailable' }, { status: 503, headers: { 'Cache-Control': 'no-store' } });
  }
}
