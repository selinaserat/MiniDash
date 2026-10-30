# Import FastAPI, the framework used to build our REST API.
# FastAPI allows MiniDash to receive HTTP requests
# and send responses back to customers.
from fastapi import FastAPI


# Create the main MiniDash application.
# The title appears in the automatic API documentation
# at http://127.0.0.1:8000/docs.
app = FastAPI(title="MiniDash API")


# Define the application's home endpoint.
# @app.get("/") means this function responds to
# HTTP GET requests sent to the root URL (/).
@app.get("/")
def home():
    """
    Health-check endpoint.

    This endpoint confirms that the MiniDash API
    is running and responding to requests.
    """

    # Return a Python dictionary.
    # FastAPI automatically converts it into JSON.
    return {
        "message": "MiniDash API is running",
        "status": "ok"
    }