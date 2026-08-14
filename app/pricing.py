"""Shipping cost calculation.

Tier boundaries are inclusive: a parcel weighing exactly 2.0 kg ships at the
small-parcel rate. See tests/test_pricing.py::test_two_kg_boundary — this is
the invariant the on-camera bug (scripts/stage_bug.sh) violates.
"""

SMALL_PARCEL_MAX_KG = 2.0
MEDIUM_PARCEL_MAX_KG = 10.0

SMALL_RATE = 5.99
MEDIUM_RATE = 9.99
LARGE_BASE = 14.99
LARGE_PER_KG = 0.55  # per kg over the medium max

EXPEDITED_MULTIPLIER = 1.75


def calc_shipping_cost(weight_kg: float, expedited: bool = False) -> float:
    """Return the shipping cost in USD for a parcel of the given weight."""
    if weight_kg <= 0:
        raise ValueError("weight_kg must be positive")

    if weight_kg <= SMALL_PARCEL_MAX_KG:
        cost = SMALL_RATE
    elif weight_kg <= MEDIUM_PARCEL_MAX_KG:
        cost = MEDIUM_RATE
    else:
        cost = LARGE_BASE + (weight_kg - MEDIUM_PARCEL_MAX_KG) * LARGE_PER_KG

    if expedited:
        cost *= EXPEDITED_MULTIPLIER

    return round(cost, 2)
