"""Order creation rules and all-or-nothing purchase persistence."""
from fastapi import HTTPException

from src.database import get_connection
from src.repositories import store
from src.services.tracking import calculate_eta, iso, utc_now


def create_order(payload, now=None):
    """Validate quantities and restaurant ownership, calculate cents, then commit."""
    current_time = now or utc_now()
    with get_connection() as conn:
        conn.execute("BEGIN IMMEDIATE")
        restaurant = conn.execute("SELECT * FROM restaurants WHERE id=?",
                                  (payload.restaurant_id,)).fetchone()
        if restaurant is None:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        total = 0
        # Check every item before writing the order to prevent partial purchases.
        for item in payload.items:
            menu_item = conn.execute("SELECT * FROM menu_items WHERE id=? AND restaurant_id=?",
                                     (item.menu_item_id,payload.restaurant_id)).fetchone()
            if menu_item is None:
                raise HTTPException(status_code=422, detail="MENU_ITEM_NOT_IN_RESTAURANT")
            total += menu_item["price_cents"] * item.quantity
        eta = calculate_eta("PLACED",restaurant["avg_prep_minutes"],current_time)
        cursor = conn.execute("""
            INSERT INTO orders(restaurant_id,status,total_cents,address,created_at,eta_at)
            VALUES(?,?,?,?,?,?)
        """,(payload.restaurant_id,"PLACED",total,payload.address,iso(current_time),eta))
        order_id = cursor.lastrowid
        for item in payload.items:
            conn.execute("INSERT INTO order_items(order_id,menu_item_id,quantity) VALUES(?,?,?)",
                         (order_id,item.menu_item_id,item.quantity))
        conn.execute("INSERT INTO order_status_history(order_id,status,changed_at) VALUES(?,?,?)",
                     (order_id,"PLACED",iso(current_time)))
    return store.order(order_id)
