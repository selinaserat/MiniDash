"""Database queries: SQL stays here instead of inside HTTP routes."""
from src.database import get_connection


def restaurants():
    with get_connection() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM restaurants ORDER BY id")]


def restaurant(restaurant_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM restaurants WHERE id=?", (restaurant_id,)).fetchone()
        return dict(row) if row else None


def menu(restaurant_id):
    with get_connection() as conn:
        return [dict(row) for row in conn.execute(
            "SELECT id,name,price_cents FROM menu_items WHERE restaurant_id=? ORDER BY id",
            (restaurant_id,))]


def order(order_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
        if row is None:
            return None
        result = dict(row)
        result["items"] = [dict(item) for item in conn.execute("""
            SELECT oi.menu_item_id, mi.name, oi.quantity, mi.price_cents,
                   (oi.quantity * mi.price_cents) AS line_total_cents
            FROM order_items oi JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id=? ORDER BY oi.id
        """, (order_id,))]
        return result


def history(order_id):
    with get_connection() as conn:
        return [dict(row) for row in conn.execute("""
            SELECT status, changed_at FROM order_status_history
            WHERE order_id=? ORDER BY id
        """, (order_id,))]
