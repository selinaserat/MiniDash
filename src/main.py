
"""
MiniDash - Main Application Entry Point

This file starts the FastAPI application and connects its main components:
1. Database initialization
2. Restaurant and order API endpoints
3. Frontend website files (HTML, CSS, JavaScript)
4. Application health check
"""

# ============================================================
# 1. IMPORTS
# ============================================================

# Used to define startup and shutdown behavior for FastAPI.
from contextlib import asynccontextmanager

# Used to locate the frontend files regardless of the working directory.
from pathlib import Path

# Main framework used to create the MiniDash API.
from fastapi import FastAPI

# Used to send the HTML homepage to the user's browser.
from fastapi.responses import FileResponse

# Used to serve CSS, JavaScript, and other frontend assets.
from fastapi.staticfiles import StaticFiles

# Database functions for creating tables and adding sample restaurants.
from src.database import initialize_database, seed_restaurants

# Import API endpoints defined in separate files.
from src.routes.orders import router as order_router
from src.routes.restaurants import router as restaurant_router


# ============================================================
# 2. APPLICATION STARTUP
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Prepare the application before it begins handling requests.

    initialize_database() creates the SQLite tables if needed.
    seed_restaurants() adds sample restaurant data.

    The yield statement marks the point where FastAPI begins
    serving requests. Code after yield would run during shutdown.
    """

    initialize_database()
    seed_restaurants()

    yield


# ============================================================
# 3. CREATE THE FASTAPI APPLICATION
# ============================================================

# Create the main MiniDash API and register its startup behavior.
# The title appears in FastAPI's interactive API documentation.
app = FastAPI(
    title="MiniDash API",
    lifespan=lifespan
)


# ============================================================
# 4. FRONTEND STATIC FILES
# ============================================================

# Locate the static folder in the main MiniDash project directory.
#
# Expected structure:
# MiniDash/
#   src/main.py
#   static/index.html
#   static/style.css
#   static/app.js

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

# Make frontend files accessible through URLs beginning with /static.
#
# Example:
# /static/style.css -> loads the website's design
# /static/app.js    -> loads the website's interactive features
app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


# ============================================================
# 5. REGISTER API ROUTES
# ============================================================

# Connect restaurant endpoints to the main application.
# These allow the frontend to retrieve restaurants and menus.
app.include_router(restaurant_router)

# Connect order endpoints to the main application.
# These handle order creation, status changes, and tracking.
app.include_router(order_router)


# ============================================================
# 6. API HEALTH CHECK
# ============================================================

@app.get("/")
def home():
    """
    Confirm that the MiniDash backend is running.

    Opening http://127.0.0.1:8000/ returns a simple JSON response.
    This is useful for checking server availability.
    """
    return {
        "message": "MiniDash API is running",
        "status": "ok"
    }


# ============================================================
# 7. CUSTOMER-FACING WEBSITE
# ============================================================

@app.get("/app", include_in_schema=False)
def show_app():
    """
    Display the MiniDash website.

    When someone visits http://127.0.0.1:8000/app,
    FastAPI sends static/index.html to their browser.

    The HTML then loads style.css and app.js automatically.
    The JavaScript communicates with the restaurant and order APIs.

    include_in_schema=False keeps this webpage route out of
    the Swagger API documentation.
    """
    return FileResponse(STATIC_DIR / "index.html")
