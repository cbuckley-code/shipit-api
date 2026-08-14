import pytest
from fastapi.testclient import TestClient

from app.main import app, store

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_store():
    store.clear()
    yield
    store.clear()


def make_shipment(**overrides):
    body = {
        "order_id": "ord-1001",
        "address": "600 Grant St, Denver, CO",
        "weight_kg": 1.2,
        "expedited": False,
    }
    body.update(overrides)
    resp = client.post("/shipments", json=body)
    assert resp.status_code == 201, resp.text
    return resp.json()


def test_healthz():
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_create_shipment_computes_cost():
    data = make_shipment()
    assert data["id"] == 1
    assert data["status"] == "label_created"
    assert data["cost_usd"] == 5.99


def test_get_shipment():
    created = make_shipment()
    resp = client.get(f"/shipments/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["order_id"] == "ord-1001"


def test_get_missing_shipment_404():
    resp = client.get("/shipments/999")
    assert resp.status_code == 404


def test_list_filters_by_status():
    a = make_shipment()
    make_shipment(order_id="ord-1002")
    client.post(f"/shipments/{a['id']}/transition", json={"status": "dispatched"})

    resp = client.get("/shipments", params={"status": "dispatched"})
    assert resp.status_code == 200
    ids = [s["id"] for s in resp.json()]
    assert ids == [a["id"]]


def test_list_rejects_unknown_status():
    resp = client.get("/shipments", params={"status": "teleported"})
    assert resp.status_code == 422


def test_valid_transition():
    created = make_shipment()
    resp = client.post(
        f"/shipments/{created['id']}/transition", json={"status": "dispatched"}
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "dispatched"


def test_invalid_transition_409():
    created = make_shipment()
    resp = client.post(
        f"/shipments/{created['id']}/transition", json={"status": "delivered"}
    )
    assert resp.status_code == 409


def test_validation_rejects_bad_weight():
    resp = client.post(
        "/shipments",
        json={"order_id": "ord-1", "address": "somewhere", "weight_kg": -1},
    )
    assert resp.status_code == 422
