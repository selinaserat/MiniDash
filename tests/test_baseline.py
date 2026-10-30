"""Independent endpoint and validation tests for the five baseline routes."""

def test_home(client):
    assert client.get("/").json()["status"] == "ok"


def test_restaurants_seeded(client):
    restaurants = client.get("/restaurants").json()
    assert len(restaurants) == 5
    assert all("avg_prep_minutes" in restaurant for restaurant in restaurants)


def test_menu_returns_prices(client):
    response = client.get("/restaurants/1/menu")
    assert response.status_code == 200
    assert response.json()[0]["price_cents"] == 1299


def test_missing_restaurant_menu(client):
    assert client.get("/restaurants/999/menu").status_code == 404


def test_place_and_retrieve_order(client,created_order):
    assert created_order["status"] == "PLACED"
    assert created_order["total_cents"] == 2598
    assert len(created_order["items"]) == 1
    assert client.get(f"/orders/{created_order['id']}").json()["total_cents"] == 2598


def test_missing_order(client):
    assert client.get("/orders/9999").status_code == 404


def test_invalid_quantity(client):
    response = client.post("/orders",json={"restaurant_id":1,"address":"X",
                                           "items":[{"menu_item_id":1,"quantity":0}]})
    assert response.status_code == 422


def test_wrong_restaurant_menu_item(client):
    response = client.post("/orders",json={"restaurant_id":1,"address":"X",
                                           "items":[{"menu_item_id":3,"quantity":1}]})
    assert response.status_code == 422


def test_cannot_create_empty_order(client):
    response = client.post("/orders",json={"restaurant_id":1,"address":"X","items":[]})
    assert response.status_code == 422
