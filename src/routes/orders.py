"""HTTP contracts for ordering, status changes, and tracking."""
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.repositories import store
from src.services import orders as order_service
from src.services import tracking

router = APIRouter(tags=["Orders"])


class OrderItemInput(BaseModel):
    # A menu item identifier and a strictly positive quantity.
    menu_item_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class OrderInput(BaseModel):
    # Reject empty addresses and orders without items.
    restaurant_id: int = Field(gt=0)
    address: str = Field(min_length=1)
    items: list[OrderItemInput] = Field(min_length=1)


class StatusInput(BaseModel):
    # Literal rejects misspelled or unrecognized status names.
    status: Literal["PLACED","PREPARING","READY","PICKED_UP","DELIVERED","CANCELLED"]


@router.post("/orders",status_code=201)
def place_order(payload: OrderInput):
    """Create a paid-total order and initial PLACED history entry."""
    return order_service.create_order(payload)


@router.get("/orders/{order_id}")
def get_order(order_id: int):
    """Retrieve an order with individual items, total, and current status."""
    result = store.order(order_id)
    if result is None:
        raise HTTPException(status_code=404,detail="Order not found")
    return result


@router.patch("/orders/{order_id}/status")
def update_status(order_id: int,payload: StatusInput):
    """Apply a valid transition or return conflict without modifying the order."""
    return tracking.transition(order_id,payload.status)


@router.get("/orders/{order_id}/tracking")
def get_tracking(order_id: int):
    """Poll this endpoint for status updates, ETA, and history."""
    return tracking.tracking(order_id)
