
# MiniDash — AI Interaction Log

## Project Information

**Project:** MiniDash — Track C: Live Order Tracking  
**AI tool:** ChatGPT (OpenAI)  
**Development environment:** Python, FastAPI, SQLite, PyCharm, GitHub  
**Development period:** October 2026

This log documents how AI assisted with the development of MiniDash. It includes generated code, documentation, debugging, testing, revisions, and verification. Exact interaction timestamps are omitted where they were not recorded.

## Entry 1 — Initial FastAPI and SQLite Setup

**Prompt:** Requested assistance creating a FastAPI application with a SQLite database for a food delivery tracking system.

**AI contribution:** Provided starter application code, database initialization instructions, and Git setup commands.

**My verification:** Initialized the SQLite database and confirmed that the `restaurants`, `menu_items`, `orders`, and `order_items` tables existed.

**Outcome:** Created the initial Git commit, `402b17e`.

## Entry 2 — Requirements and Architecture

**Prompt:** Requested assistance documenting MiniDash's requirements, system architecture, and development tasks.

**AI contribution:** Helped structure the requirements, architecture documentation, and implementation plan.

**My verification:** Added the documentation files to the project and committed them.

**Outcome:** Documentation commit `b9751ed`.

## Entry 3 — SQLite Connection Management

**Prompt:** Requested help investigating database connection warnings encountered during automated testing.

**AI contribution:** Suggested improvements to SQLite connection handling and restaurant endpoints.

**My verification:** Reviewed test output and continued testing after the database changes.

**Outcome:** Database improvements committed as `8bec88b`.

## Entry 4 — Order Processing and Status Transitions

**Prompt:** Requested implementation guidance for creating orders and tracking their progress.

**AI contribution:** Assisted with order routes, service logic, and database repository organization.

**My verification:** Tested order creation and the progression through PLACED, PREPARING, READY, PICKED_UP, and DELIVERED.

**Outcome:** Implemented order processing and tracking functionality.

## Entry 5 — Automated Testing

**Prompt:** Requested help verifying the application's behavior.

**AI contribution:** Assisted with tests covering orders, restaurant data, tracking, and invalid operations.

**My verification:** Ran `python -m pytest -q` and confirmed that all 21 tests passed.

**Outcome:** Added automated regression tests and verified the application.

## Entry 6 — Demonstration and GitHub Workflow

**Prompt:** Requested guidance preparing the application for demonstration and submission.

**AI contribution:** Explained demonstration scripts, Git commits, version-control checks, and GitHub synchronization.

**My verification:** Reviewed Git history and successfully pushed the project to GitHub.

**Outcome:** Created a documented Git history and published the project repository.

## Entry 7 — Customer-Facing Website

**Prompt:** Requested a visual MiniDash website similar in functionality to a modern food-delivery interface.

**AI contribution:** Generated HTML, CSS, and JavaScript for restaurant browsing, menus, a shopping cart, and delivery tracking.

**My changes:** Chose to build the files manually in PyCharm rather than download a prepared ZIP. Connected the static frontend to the FastAPI application.

**My verification:** Opened `/app` locally and confirmed that restaurant information loaded.

**Outcome:** Added the customer-facing website.

## Entry 8 — Revision of Food Images and Price Handling

**Prompt:** Reported that pasta displayed a burger emoji and menu prices appeared as `$NaN`.

**Original AI-generated behavior:** The frontend displayed the same burger emoji for all dishes and attempted to read prices using `item.price`.

**My decision:** Requested more accurate food-specific emojis and corrected price handling.

**Revised solution:** Replaced hardcoded emojis with name-based selection functions and added support for prices supplied through `price_cents`.

**My verification:** Refreshed the website and confirmed that the design and displayed content worked after the changes.

**Outcome:** Substantially revised the original frontend implementation.

## Entry 9 — Checkout Validation

**Prompt:** Reported a checkout failure stating that the delivery address was missing.

**AI contribution:** Identified the required `address` field from FastAPI's validation response and recommended prompting the customer for an address.

**My verification:** Entered a demonstration address and successfully created an order.

**Outcome:** Corrected checkout request data to match the backend's requirements.

## Entry 10 — Rejected Tracking Endpoint and Corrected Implementation

**Prompt:** Reported that live tracking displayed `Method Not Allowed`.

**Original AI-generated implementation:** Requested `GET /orders/{order_id}/status`.

**Problem:** The backend uses that path for status updates rather than retrieving tracking information.

**My decision:** Did not retain the incorrect endpoint. Used the API documentation to identify the appropriate tracking route.

**Revised solution:** Changed the request to `GET /orders/{order_id}/tracking`.

**My verification:** Created Order #2 and confirmed that tracking information appeared and updated as the order progressed.

**Outcome:** Rejected the incorrect API integration and replaced it with the verified tracking endpoint.

## Entry 11 — Invalid Status Validation

**Prompt:** Requested help interpreting an HTTP 422 error during the order demonstration.

**AI contribution:** Explained that status values must match the backend's permitted values exactly.

**My verification:** Corrected the status to `PICKED_UP` and continued the workflow through `DELIVERED`.

**Outcome:** Confirmed that the API validates status values and that the full delivery lifecycle works.

## Entry 12 — Final Verification and Repository Update

**Prompt:** Requested help confirming the final GitHub submission state.

**AI contribution:** Provided Git status, commit, push, and testing commands.

**My verification:** Confirmed that all 21 automated tests passed and Git reported a clean working tree.

**Outcome:** Pushed the customer-facing website in commit `4a91d38` and confirmed that the local branch was synchronized with `origin/main`.

## Summary

AI was used to accelerate implementation, documentation, debugging, and testing. However, generated code required verification against the actual FastAPI endpoints and database response formats.

Two important corrections were made to AI-generated frontend code:

1. Revised the menu display and price calculations to eliminate incorrect emojis and `$NaN` values.
2. Replaced the incorrect order-tracking API endpoint after encountering HTTP 405.

The project was verified through automated tests, API testing, browser demonstrations, and Git version-control checks.
