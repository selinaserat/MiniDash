"""Public restaurant and menu endpoints."""
from fastapi import APIRouter, HTTPException

from src.repositories import store

# Prefix-free router allows exact paths without implicit trailing slash redirects.
router = APIRouter(tags=["Restaurants"])


@router.get("/restaurants")
def list_restaurants():
    """List seeded restaurant names, cuisines, hours and prep times."""
    return store.restaurants()


@router.get("/restaurants/{restaurant_id}/menu")
def get_menu(restaurant_id: int):
    """Show menu prices in cents for a known restaurant."""
    if not store.restaurant(restaurant_id):
        raise HTTPException(status_code=404,detail="Restaurant not found")
    return store.menu(restaurant_id)
