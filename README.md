# MiniDash — Track C: Live Order Tracking

A SQLite-backed REST API built with Python FastAPI. This repository implements the five baseline endpoints and the Live Order Tracking feature. Source files include comments explaining the design.

## Start in PyCharm / macOS

Use Python 3.13 (or another supported Python 3.10+). From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.database
python -m uvicorn src.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive documentation. A database called `minidash.db` is created locally; it is intentionally ignored by Git.

## Test and lint

In another terminal with `.venv` activated:

```bash
python -m pytest -q
python -m ruff check src tests scripts
python -m pip check
```

## Baseline API

- `GET /restaurants`
- `GET /restaurants/{id}/menu`
- `POST /orders`
- `GET /orders/{id}`
- `PATCH /orders/{id}/status`

## Track C API

- `GET /orders/{id}/tracking` — poll repeatedly to see status, ETA and ordered history
- The API rejects illegal status changes with HTTP 409; cancellation is allowed only from PLACED.

To place an order in Swagger, POST `/orders` with:

```json
{"restaurant_id":1,"address":"123 Demo Street","items":[{"menu_item_id":1,"quantity":2}]}
```

Copy the returned `id`, then run the driver simulator while the server is running:

```bash
python scripts/simulate_driver.py 1
```

Replace `1` with your order's ID. Repeatedly request `/orders/{id}/tracking` to poll for updates.

## Design notes

See `docs/requirements.md`, `docs/design.md` and `docs/tasks.md`. The distance model deliberately assumes a fixed 12-minute drive because the baseline has no geographic coordinates. ETA is recalculated on each transition; it is a demonstration estimate, not a real-world route prediction. All monetary values are stored in integer cents.

## Instructor rubric and evidence

`AI_LOG.md` is a truthful log *template*, not a fabricated history. Document actual prompts and reviews. `docs/reflection_template.md` contains prompts to answer based on your actual experience. The assignment also requires separate meaningful slice commits; importing this complete package as one commit **does not satisfy that history requirement**. Reconstructing commits with invented AI interactions is not appropriate; continue with authentic commits as you review and improve slices.
