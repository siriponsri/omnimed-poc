# Event model — contract only in M0

Source: SRS §5 B0215–B0240, BR-EVT-01…04 และ exact excerpts. M0 ยังไม่มี event_outbox table, worker, dispatcher หรือ clinical transaction; ไม่อ้างว่า event delivery implemented

| Source event name | Future producer / trigger | Selected consumer / effect |
|---|---|---|
| patient.registered | M1 identity transaction | audit/projection by reference |
| encounter.started | PAT-02 service start | billing opens account when implemented |
| vitals.recorded | completed vital write transaction | doctor query refresh; no CDS |
| order.placed | authorized new order | matching lab/pharmacy worklist |
| order.revised / order.discontinued | new linked revision/action | receiving worklist updates; reject stale fulfillment |
| order.fulfilled | lab analysis technical_complete | one lab charge from source event |
| result.released | validated/released lab result | publish Observation; no extra charge |
| medication.dispensed | confirmed pharmacy dispense | one medication charge; avoid duplicate handling if order.fulfilled also emitted |
| encounter.checkout | after agreed synthetic closure contract | recorded stub-free contract; real Next Account posting OUT_OF_SCOPE |

Proposed envelope (field naming is a POC design, event names remain source-named):

```json
{
  "event_id": "00000000-0000-4000-8000-000000000001",
  "event_type": "order.fulfilled",
  "schema_version": 1,
  "tenant_id": "00000000-0000-4000-8000-000000000002",
  "aggregate_type": "analysis",
  "aggregate_id": "00000000-0000-4000-8000-000000000003",
  "occurred_at": "2026-09-08T00:00:00Z",
  "actor_id": "00000000-0000-4000-8000-000000000004",
  "correlation_id": "synthetic-example",
  "payload": {"order_id": "00000000-0000-4000-8000-000000000005"}
}
```

Example is documentation, not generated runtime evidence. Payload contains reference IDs only; no patient name, diagnosis, result, medication directions, secret or PHI body. UUIDs do not anonymize a patient reference; protect audit/event storage appropriately

A future command commits business rows and outbox row atomically. Consumer transaction inserts `(consumer_name,event_id)` receipt and resulting projection/charge together; unique receipt plus unique source charge key ensures retry does not double charge. On failure neither receipt nor projection commits. At-least-once delivery is not exactly-once execution; test crash-before/after-commit and replay. State machine stores attempt count, next attempt and terminal failure separately from immutable event content

No distributed broker or infinite retry. Bounded retry/backoff and manual dead-letter/replay operations are deferred; do not add a fake dispatcher that discards events. Changing event name/schema requires trace + ADR and explicit backwards-compatibility decision
