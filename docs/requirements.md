# MiniDash Track C Requirements (EARS)

## Scope

Customers order restaurant food and poll delivery status. No authentication, payments, GPS tracking, or production distance API.

## Acceptance criteria

- **R1:** WHEN the service starts with a fresh database, THE SYSTEM SHALL seed five restaurants with cuisine, hours, and prep time.
- **R2:** WHEN a customer requests a restaurant menu, THE SYSTEM SHALL return menu item identifiers, names, and integer-cent prices, or a 404 for an unknown restaurant.
- **R3:** WHEN an order is posted with valid items from one restaurant, THE SYSTEM SHALL create it with status PLACED, a correct total, and an initial timestamped history event.
- **R4:** IF any submitted item belongs to a different restaurant or has nonpositive quantity, THEN THE SYSTEM SHALL reject the order without storing it.
- **R5:** WHEN a status change follows PLACED → PREPARING → READY → PICKED_UP → DELIVERED, THE SYSTEM SHALL persist the new status and a timestamped history event.
- **R6:** WHEN an order in PLACED is cancelled, THE SYSTEM SHALL record CANCELLED and prevent any later transitions.
- **R7:** IF an order has reached PREPARING or later, THEN THE SYSTEM SHALL reject cancellation with HTTP 409 and leave the status and history unchanged.
- **R8:** IF any other illegal or repeated status transition is requested, THEN THE SYSTEM SHALL reject it with HTTP 409 without any data changes.
- **R9:** WHEN the customer GETs /orders/{id}/tracking, THE SYSTEM SHALL return current status, chronological history, and latest ETA.
- **R10:** WHEN an order status changes, THE SYSTEM SHALL recalculate ETA using restaurant prep time, the documented fixed-drive model, and an injectable clock.
- **R11:** WHEN a client polls the tracking endpoint after a valid transition, THE SYSTEM SHALL observe the updated status.
- **R12:** WHEN the simulation is run with an existing PLACED order ID, THE SYSTEM SHALL advance it through each valid driver step via API calls.
- **R13:** IF a requested restaurant or order does not exist, THEN THE SYSTEM SHALL respond 404.

## Out of scope

Login, payment processing, geolocation, push notifications, user accounts, UI frontend, and production deployment.
