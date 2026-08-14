"""Shipment domain model and in-memory store.

Deliberately simple: the course is about the agent pipeline around this app,
not the app itself. The in-memory store keeps the demo dependency-free;
swapping in Postgres is left as a student exercise.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Optional

from app.pricing import calc_shipping_cost

# Valid status transitions. "Add rate limiting" (the Section 7.6 money-demo
# story) is intentionally NOT implemented — agents add it on camera.
TRANSITIONS = {
    "label_created": {"dispatched", "cancelled"},
    "dispatched": {"delivered"},
    "delivered": set(),
    "cancelled": set(),
}


class TransitionError(Exception):
    pass


@dataclass
class Shipment:
    id: int
    order_id: str
    address: str
    weight_kg: float
    expedited: bool = False
    status: str = "label_created"
    cost_usd: float = field(default=0.0)

    def transition(self, new_status: str) -> None:
        allowed = TRANSITIONS.get(self.status, set())
        if new_status not in allowed:
            raise TransitionError(
                f"cannot move shipment {self.id} from {self.status!r} to {new_status!r}"
            )
        self.status = new_status


class ShipmentStore:
    def __init__(self) -> None:
        self._items: dict[int, Shipment] = {}
        self._ids = itertools.count(1)

    def create(
        self, order_id: str, address: str, weight_kg: float, expedited: bool = False
    ) -> Shipment:
        shipment = Shipment(
            id=next(self._ids),
            order_id=order_id,
            address=address,
            weight_kg=weight_kg,
            expedited=expedited,
            cost_usd=calc_shipping_cost(weight_kg, expedited),
        )
        self._items[shipment.id] = shipment
        return shipment

    def get(self, shipment_id: int) -> Optional[Shipment]:
        return self._items.get(shipment_id)

    def list(self, status: Optional[str] = None) -> list[Shipment]:
        items = list(self._items.values())
        if status is not None:
            items = [s for s in items if s.status == status]
        return items

    def clear(self) -> None:
        self._items.clear()
        self._ids = itertools.count(1)
