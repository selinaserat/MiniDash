
# MiniDash — Track C: Live Order Tracking

For my Software Engineering project, I created MiniDash, a food delivery application using Python, FastAPI, and SQLite. I also built a frontend using HTML, CSS, and JavaScript so users can interact with the application.

Users can browse restaurants, view menus, add items to their cart, place orders, and track their deliveries.

The main feature I worked on for Track C is live order tracking. Orders move through different stages, from being placed to being delivered. The website automatically checks for updates so users can see when their order status changes.

## Technologies Used

- Python and FastAPI for the backend
- SQLite for storing restaurant and order information
- HTML, CSS, and JavaScript for the frontend
- Pytest for automated testing
- Ruff for checking the Python code
- Git and GitHub for version control
- PyCharm for development

## How to Run MiniDash

I developed and tested MiniDash using PyCharm on macOS.

First, open the project folder in a terminal.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Set up the SQLite database:

```bash
python -m src.database
```

Start the application:

```bash
python -m uvicorn src.main:app --reload
```

Once the server is running, open the following links in your browser.

**MiniDash Website:**

http://127.0.0.1:8000/app

**FastAPI Documentation:**

http://127.0.0.1:8000/docs

The website is where users can browse restaurants and place orders. The FastAPI documentation can be used to test the backend endpoints and update order statuses.

## Features

### Restaurant Browsing

Users can view the available restaurants and select one to see its menu.

### Shopping Cart and Checkout

Users can add menu items to their cart, view the total price, and place an order by entering a delivery address.

### Live Order Tracking

After placing an order, users can follow its progress through five stages:

1. PLACED
2. PREPARING
3. READY
4. PICKED_UP
5. DELIVERED

Orders can also be cancelled while they are still in the PLACED stage.

The application stores the order status history with timestamps and calculates an estimated arrival time.

The website checks for updates approximately every five seconds, so the customer can see changes without manually refreshing the page.

## API Endpoints

The application includes the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /restaurants | View available restaurants |
| GET | /restaurants/{id}/menu | View a restaurant's menu |
| POST | /orders | Create a new order |
| GET | /orders/{id} | View an existing order |
| PATCH | /orders/{id}/status | Update an order's status |
| GET | /orders/{id}/tracking | View tracking information and order history |

The backend checks that status changes are valid. For example, an order cannot move directly from PLACED to DELIVERED. Invalid transitions are rejected.

## How to Test Order Tracking

1. Start the application.
2. Open the MiniDash website at http://127.0.0.1:8000/app.
3. Select a restaurant and add items to the cart.
4. Place an order and enter a delivery address.
5. Open http://127.0.0.1:8000/docs in another browser tab.
6. Find `PATCH /orders/{id}/status`.
7. Enter the order ID and update its status.

For example, to change an order to PREPARING, use:

```json
{
  "status": "PREPARING"
}
```

Click Execute and return to the MiniDash website.

The tracking section should update automatically.

Continue updating the order through READY, PICKED_UP, and DELIVERED to test the complete delivery process.

### Driver Simulation

The project also includes a driver simulation script.

With the application running, open another terminal and enter:

```bash
python scripts/simulate_driver.py 1
```

Replace `1` with the ID of the order you want to simulate.

## Automated Testing

I used Pytest to test the backend and verify that the main features were working correctly.

To run the tests:

```bash
python -m pytest -q
```

To check the Python code using Ruff:

```bash
python -m ruff check src tests scripts
```

To check installed package dependencies:

```bash
python -m pip check
```

I finished the project with **21 automated tests passing**.

I also manually tested the website by browsing restaurants, placing orders, updating order statuses, and checking that the tracking information updated correctly.

## Design and Implementation

The application uses separate routes, services, and repository files to organize the backend.

SQLite is used to store the restaurant, menu, and order information.

For delivery estimates, I used a simplified distance model with an assumed 12-minute driving time. This is only meant for demonstrating the tracking feature and does not calculate actual driving routes.

I also used integer cents when storing prices to avoid problems with money calculations.

More details about the requirements, design decisions, and development tasks can be found in the `docs` folder.

## Project Documentation

The repository includes:

- `docs/requirements.md` — Project requirements and acceptance criteria
- `docs/design.md` — Application design and architecture
- `docs/tasks.md` — Development tasks
- `AI_LOG.md` — Record of how I used ChatGPT during development
- `MiniDash Reflection.pdf` — My reflection on using AI and what I learned
- `tests/` — Automated tests
- `scripts/` — Driver simulation script
- `static/` — Frontend HTML, CSS, and JavaScript files

## AI Usage

I used ChatGPT throughout the project to help me understand how to implement features, organize the code, troubleshoot errors, and write tests.

I tested the AI-generated code myself instead of assuming everything would work correctly. Some suggestions needed changes, especially when connecting the frontend to the backend.

I documented these interactions and corrections in `AI_LOG.md`.

## What I Learned

Working on MiniDash helped me get more comfortable using FastAPI, SQLite, and JavaScript.

I also learned more about how the frontend and backend communicate, how to test API endpoints, and how to debug errors when something isn't working.

One of the biggest things I learned is that AI can help with coding, but I still need to understand the code, test it, and make sure it works the way I intended.
