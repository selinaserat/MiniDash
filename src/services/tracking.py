"""Track C order state machine and deterministic ETA rules."""
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException

from src.database import get_connection
from src.repositories import store

# Legal transitions are explicitly enumerated to prevent skipping steps.
NEXT_STATES = {
    "PLACED": {"PREPARING", "CANCELLED"},
    "PREPARING": {"READY"},
    "READY": {"PICKED_UP"},
    "PICKED_UP": {"DELIVERED"},
    "DELIVERED": set(),
    "CANCELLED": set(),
}

# A simple documented model: travel takes 12 minutes, independent of location.
# This is a deliberately simplified distance assumption for the assignment.
TRAVEL_MINUTES = 12


def utc_now():
    """Central time source; tests can pass a fixed timestamp to service functions."""
    return datetime.now(UTC)


def iso(timestamp):
    """Serialize a timezone-aware timestamp consistently in UTC."""
    return timestamp.astimezone(UTC).isoformat()


def calculate_eta(status, prep_minutes, now):
    """Recalculate ETA from status, restaurant prep, and assumed travel time."""
    remaining = {
        "PLACED": prep_minutes + TRAVEL_MINUTES,
        "PREPARING": max(1, prep_minutes // 2) + TRAVEL_MINUTES,
        "READY": TRAVEL_MINUTES,
        "PICKED_UP": TRAVEL_MINUTES,
        "DELIVERED": 0,
        "CANCELLED": 0,
    }[status]
    # A cancelled order has no arrival estimate.
    return None if status == "CANCELLED" else iso(now + timedelta(minutes=remaining))


def transition(order_id, new_status, now=None):
    """Atomically validate, persist and record a status transition."""
    current_time = now or utc_now()
    with get_connection() as conn:
        # BEGIN IMMEDIATE serializes competing writers, avoiding duplicate history.
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("""
            SELECT o.status, r.avg_prep_minutes FROM orders o
            JOIN restaurants r ON r.id=o.restaurant_id WHERE o.id=?
        """, (order_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Order not found")
        if new_status not in NEXT_STATES[row["status"]]:
            raise HTTPException(status_code=409, detail="INVALID_STATUS_TRANSITION")
        eta = calculate_eta(new_status, row["avg_prep_minutes"], current_time)
        conn.execute("UPDATE orders SET status=?,eta_at=? WHERE id=?",
                     (new_status, eta, order_id))
        conn.execute("INSERT INTO order_status_history(order_id,status,changed_at) VALUES(?,?,?)",
                     (order_id,new_status,iso(current_time)))
    return store.order(order_id)


def tracking(order_id):
    """Return status, ETA, and chronological history for polling clients."""
    current = store.order(order_id)
    if current is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order_id":order_id, "status":current["status"],
            "estimated_arrival_at":current["eta_at"],
            "history":store.history(order_id)}
