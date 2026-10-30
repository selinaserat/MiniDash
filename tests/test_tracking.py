"""Track C state transitions, history, ETA and polling behavior."""
from datetime import UTC, datetime, timedelta

from src.repositories import store
from src.services.tracking import calculate_eta, transition


def test_placed_has_initial_timestamp(client,created_order):
    response = client.get(f"/orders/{created_order['id']}/tracking")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PLACED"
    assert len(data["history"]) == 1
    assert data["history"][0]["status"] == "PLACED"
    datetime.fromisoformat(data["history"][0]["changed_at"])


def test_full_transition_history_and_eta(client,created_order):
    order_id = created_order["id"]
    previous_eta = created_order["eta_at"]
    for status in ("PREPARING", "READY", "PICKED_UP", "DELIVERED"):
        response = client.patch(f"/orders/{order_id}/status",json={"status":status})
        assert response.status_code == 200
        assert response.json()["status"] == status
        if status == "PREPARING":
            assert response.json()["eta_at"] != previous_eta
    data = client.get(f"/orders/{order_id}/tracking").json()
    assert [item["status"] for item in data["history"]] == [
        "PLACED","PREPARING","READY","PICKED_UP","DELIVERED"]
    assert data["estimated_arrival_at"] is not None


def test_invalid_skip_does_not_modify_order(client,created_order):
    order_id = created_order["id"]
    response = client.patch(f"/orders/{order_id}/status",json={"status":"DELIVERED"})
    assert response.status_code == 409
    tracking = client.get(f"/orders/{order_id}/tracking").json()
    assert tracking["status"] == "PLACED"
    assert len(tracking["history"]) == 1


def test_cancel_only_before_preparing(client,created_order):
    order_id = created_order["id"]
    response = client.patch(f"/orders/{order_id}/status",json={"status":"CANCELLED"})
    assert response.status_code == 200
    assert response.json()["eta_at"] is None
    assert client.patch(f"/orders/{order_id}/status",json={"status":"PREPARING"}).status_code == 409


def test_cannot_cancel_after_preparing(client,created_order):
    order_id = created_order["id"]
    assert client.patch(f"/orders/{order_id}/status",json={"status":"PREPARING"}).status_code == 200
    assert client.patch(f"/orders/{order_id}/status",json={"status":"CANCELLED"}).status_code == 409
    assert len(client.get(f"/orders/{order_id}/tracking").json()["history"]) == 2


def test_repeated_same_status_is_rejected(client,created_order):
    order_id = created_order["id"]
    for _ in range(2):
        assert client.patch(f"/orders/{order_id}/status",json={"status":"PLACED"}).status_code == 409
    assert len(client.get(f"/orders/{order_id}/tracking").json()["history"]) == 1


def test_tracking_unknown_order(client):
    assert client.get("/orders/900/tracking").status_code == 404


def test_status_unknown_order(client):
    assert client.patch("/orders/900/status",json={"status":"PREPARING"}).status_code == 404


def test_invalid_status_name(client,created_order):
    assert client.patch(f"/orders/{created_order['id']}/status",json={"status":"FLYING"}).status_code == 422


def test_eta_fixed_clock_and_prep_time():
    # Fixed input makes boundary tests independent of real-world clock time.
    now = datetime(2026,10,30,12,0,tzinfo=UTC)
    assert calculate_eta("PLACED",20,now) == (now+timedelta(minutes=32)).isoformat()
    assert calculate_eta("READY",20,now) == (now+timedelta(minutes=12)).isoformat()
    assert calculate_eta("CANCELLED",20,now) is None


def test_injected_clock_records_transition(client,created_order):
    fixed = datetime(2026,10,30,13,0,tzinfo=UTC)
    transition(created_order["id"],"PREPARING",now=fixed)
    history = store.history(created_order["id"])
    assert history[-1]["changed_at"] == fixed.isoformat()


def test_polling_returns_latest_status(client,created_order):
    order_id = created_order["id"]
    before = client.get(f"/orders/{order_id}/tracking").json()
    client.patch(f"/orders/{order_id}/status",json={"status":"PREPARING"})
    after = client.get(f"/orders/{order_id}/tracking").json()
    assert before["status"] == "PLACED"
    assert after["status"] == "PREPARING"
