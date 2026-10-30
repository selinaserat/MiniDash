"""FastAPI entry point for all MiniDash endpoints."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import initialize_database, seed_restaurants
from src.routes.orders import router as order_router
from src.routes.restaurants import router as restaurant_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and seed SQLite once when the server or test client starts."""
    initialize_database()
    seed_restaurants()
    yield  # FastAPI serves requests between startup and shutdown.


app = FastAPI(title="MiniDash API", lifespan=lifespan)
app.include_router(restaurant_router)
app.include_router(order_router)


@app.get("/")
def home():
    """Health check used to confirm the API server is online."""
    return {"message":"MiniDash API is running","status":"ok"}
