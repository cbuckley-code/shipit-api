"""Pricing tests.

test_two_kg_boundary is the test the on-camera bug breaks (Lecture 2.3 /
Section 6.2 repair-loop demo). scripts/stage_bug.sh changes an inclusive
tier boundary to exclusive — a realistic off-by-boundary regression.
"""

import pytest

from app.pricing import calc_shipping_cost


def test_small_parcel_rate():
    assert calc_shipping_cost(0.5) == 5.99


def test_two_kg_boundary():
    """Exactly 2.0 kg ships at the small-parcel rate (inclusive boundary)."""
    assert calc_shipping_cost(2.0) == 5.99


def test_medium_parcel_rate():
    assert calc_shipping_cost(5.0) == 9.99


def test_ten_kg_boundary():
    """Exactly 10.0 kg ships at the medium rate (inclusive boundary)."""
    assert calc_shipping_cost(10.0) == 9.99


def test_large_parcel_rate():
    # 14.99 base + 5 kg over × 0.55 = 17.74
    assert calc_shipping_cost(15.0) == 17.74


def test_expedited_multiplier():
    assert calc_shipping_cost(1.0, expedited=True) == round(5.99 * 1.75, 2)


def test_rejects_non_positive_weight():
    with pytest.raises(ValueError):
        calc_shipping_cost(0)
    with pytest.raises(ValueError):
        calc_shipping_cost(-3.2)
