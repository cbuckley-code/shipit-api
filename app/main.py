"""ShipIt — a small shipments API.

The demo application for the "Claude for Engineering Teams" course.
Frank (the MCP server) monitors this service; Claude Code and Copilot
fix and extend it via the beads work queue.

Run locally:  make run
Run tests:    make test
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from app.shipments import TRANSITIONS, ShipmentStore, TransitionError

app = FastAPI(title="ShipIt API", version="1.0.0")
store = ShipmentStore()


class ShipmentIn(BaseModel):
    order_id: str = Field(min_length=1)
    address: str = Field(min_length=1)
    weight_kg: float = Field(gt=0, le=1000)
    expedited: bool = False


class ShipmentOut(BaseModel):
    id: int
    order_id: str
    address: str
    weight_kg: float
    expedited: bool
    status: str
    cost_usd: float


class TransitionIn(BaseModel):
    status: str


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok", "service": "shipit-api"}


@app.post("/shipments", response_model=ShipmentOut, status_code=201)
def create_shipment(body: ShipmentIn) -> ShipmentOut:
    shipment = store.create(
        order_id=body.order_id,
        address=body.address,
        weight_kg=body.weight_kg,
        expedited=body.expedited,
    )
    return ShipmentOut(**shipment.__dict__)


@app.get("/shipments", response_model=list[ShipmentOut])
def list_shipments(status: str | None = Query(default=None)) -> list[ShipmentOut]:
    if status is not None and status not in TRANSITIONS:
        raise HTTPException(status_code=422, detail=f"unknown status {status!r}")
    return [ShipmentOut(**s.__dict__) for s in store.list(status)]


@app.get("/shipments/{shipment_id}", response_model=ShipmentOut)
def get_shipment(shipment_id: int) -> ShipmentOut:
    shipment = store.get(shipment_id)
    if shipment is None:
        raise HTTPException(status_code=404, detail="shipment not found")
    return ShipmentOut(**shipment.__dict__)


@app.post("/shipments/{shipment_id}/transition", response_model=ShipmentOut)
def transition_shipment(shipment_id: int, body: TransitionIn) -> ShipmentOut:
    shipment = store.get(shipment_id)
    if shipment is None:
        raise HTTPException(status_code=404, detail="shipment not found")
    try:
        shipment.transition(body.status)
    except TransitionError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return ShipmentOut(**shipment.__dict__)
