# ShipIt — Product Brief

**Status:** Approved · **Owner:** Product · **Last updated:** Sprint 14

## What we're building

ShipIt is the internal shipments API for our e-commerce ops team. It creates
shipments from orders, prices them by weight tier, and tracks each shipment
through its lifecycle (label created → dispatched → delivered, or cancelled).

## Why

Ops currently prices shipments in a spreadsheet and tracks status in Slack
threads. Both break weekly. A small, boring, well-tested API ends that.

## In scope (v1)

- Create a shipment from an order (order id, address, weight, expedited flag)
- Price automatically by weight tier — see ADR-001 for the tier decision
- Status transitions with validation (no delivering a cancelled parcel)
- List and filter shipments by status
- Health endpoint for monitoring

## Out of scope (v1) — deliberately

- **Rate limiting** — backlogged; ops tooling hits us in bursts (planned next)
- **Auth on write paths** — internal network only for v1 (planned next)
- **Persistence** — see ADR-002
- Carrier integration, label printing, webhooks

## Success criteria

- Every pricing rule covered by a test, including tier boundaries
- CI green on every merge to main; broken main is an incident
- A new engineer (or agent) can answer "why does it work this way?"
  from the docs in this folder without asking a human
