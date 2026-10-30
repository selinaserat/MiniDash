# Import APIRouter to define restaurant-related API endpoints.
# Routers let us organize endpoints in separate files.
from fastapi import APIRouter

# Create a router for restaurant endpoints.
# The prefix means all routes here begin with /restaurants.
# The tag groups these endpoints in Swagger UI.
router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)


# Define the GET /restaurants endpoint.
# Customers will use this endpoint to browse restaurants.
@router.get("/")
def list_restaurants():
    """
    Return the list of available restaurants.

    This is a temporary response used to verify routing.
    In the next steps, the endpoint will retrieve real
    restaurant records from our SQLite database.
    """

    # Return an empty list until the database query is connected.
    return []