# MiniDash AI coding conventions

1. Python 3.13, FastAPI, SQLite (`sqlite3`) and pytest; use no undisclosed dependencies.
2. Keep HTTP routes thin, business rules in `src/services`, and SQL in `src/repositories` or database initialization.
3. Explain significant code blocks with meaningful comments and docstrings; use integer cents for prices.
4. Every new behavior requires an automated test. Run pytest, ruff, and pip check before committing.
5. Keep every AI interaction and substantive rejection honestly documented in AI_LOG.md.
6. Never commit `.env`, local databases, secrets, private customer data or virtual environments.
