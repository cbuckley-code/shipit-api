# ADR-002: In-memory store, no database (v1)

**Status:** Accepted · **Deciders:** Eng · **Date:** Sprint 12

## Context

v1's job is to replace the spreadsheet workflow and prove the API shape.
Ops loses nothing if shipment state resets on deploy — the spreadsheet was
never durable either. Every infrastructure component we add is something
the pipeline, tests, and on-call rotation must carry.

## Decision

v1 uses a process-local in-memory store (`ShipmentStore`). No database,
no migrations, no connection pooling, no test fixtures beyond `store.clear()`.

## Consequences

- The service is a single process; state resets on restart. Acceptable for v1.
- Tests are fast and dependency-free — `make test` runs in under a second.
- The store interface (`create` / `get` / `list`) is deliberately shaped so a
  Postgres-backed implementation can replace it without touching handlers.
- Revisit when ops needs shipment history across deploys (likely v2).
