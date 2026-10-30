# Incremental implementation and verification slices

This is a planned sequence, not a claim that each slice has already been separately committed.

1. [ ] Baseline SQLite schema and seed data. Test: five restaurants returned from a fresh test DB.
2. [ ] Restaurant and menu routes. Test: menu prices and unknown restaurant 404.
3. [ ] Order creation and lookup. Test: total in cents, invalid quantity, and wrong-restaurant item.
4. [ ] Status transition state machine. Test: valid progression, invalid jumps, cancellations, repeated transitions.
5. [ ] Timestamped status history. Test: initial history and monotonically ordered records.
6. [ ] ETA and injectable clock. Test: fixed-clock calculations and recomputation.
7. [ ] Polling and driver simulator. Test: polling observes updates; simulator demo against a live server.
8. [ ] Fresh-clone verification and documentation. Test: run README commands and record results.

For each completed slice: check changes, run tests, note AI usage, and commit with a meaningful message. Record actual commits and verification evidence.
