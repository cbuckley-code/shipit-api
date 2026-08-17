---
paths:
  - "app/pricing.py"
  - "tests/test_pricing.py"
---

# Pricing rules

- Tier boundaries are **inclusive** — a 2.0 kg parcel is a small parcel. ADR-001 is the authority.
- Never change a boundary without citing ADR-001 in the PR description.
- Every pricing change lands with a boundary test (see `test_two_kg_boundary`).
