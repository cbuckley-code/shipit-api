# ADR-001: Weight-tier pricing with inclusive boundaries

**Status:** Accepted · **Deciders:** Product + Eng · **Date:** Sprint 12

## Context

Marketing launched with the promise **"2 kg ships for $5.99."** Pricing must
be simple enough for ops to explain on a support call, and boundary behavior
must be unambiguous — boundary disputes were the #1 source of refund tickets
in the spreadsheet era.

## Decision

Three weight tiers with **inclusive upper boundaries**:

| Tier | Weight | Price |
|---|---|---|
| Small | ≤ 2.0 kg (inclusive) | $5.99 |
| Medium | ≤ 10.0 kg (inclusive) | $9.99 |
| Large | > 10.0 kg | $14.99 + $0.55/kg over 10 |

Expedited shipping multiplies the final price by 1.75.

A parcel weighing **exactly 2.0 kg ships at the small rate**. This is the
customer-friendly reading of the marketing promise and the cheaper-for-the-
customer resolution of every boundary case.

## Consequences

- `calc_shipping_cost` must use `<=` comparisons on tier boundaries.
- **Every tier boundary gets an exact-boundary test** (see
  `tests/test_pricing.py::test_two_kg_boundary` and `::test_ten_kg_boundary`).
  A boundary regression is a pricing incident, not a rounding quirk — it
  overcharges exactly the customers the promise was made to.
- Support scripts can say: "at or under 2 kilos, it's $5.99."
