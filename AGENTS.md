# AGENTS.md — Task Tracker Repo Guardrails

## Stack

- **Backend**: Python 3.11, FastAPI, Pydantic v2, Uvicorn
- **Frontend**: Vanilla HTML/CSS/JS (no build step)
- **Testing**: pytest with httpx TestClient
- **Storage**: In-memory dict (no database)

## Run commands

```bash
# Install
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# Start API
uvicorn app.main:app --reload

# Run tests
PYTHONPATH=. pytest -q

# Health check
curl http://127.0.0.1:8000/health
```

## Docker

```bash
docker build -t task-tracker .
docker run -p 8000:8000 task-tracker
curl http://localhost:8000/health
```

## Project scope rules

- **No new product features**: do not add comments, auth, notifications, a production database, or unrelated UI changes.
- **app/ and frontend/ are protected**: only change these directories for a small bug fix, security fix, or documentation-supported correction. Explain any such change in `docs/final-ai-review.md`.
- **No secrets or personal data**: do not paste credentials, `.env` values, tokens, production logs, or real personal/customer data into AI tools or the repo.

## Read-first / docs-first guardrails

Before generating or changing code, read:
1. This file (`AGENTS.md`) for current rules and commands.
2. The relevant source file in `app/` to understand existing logic.
3. `docs/midcourse/mini-adr.md` for architecture decisions that constrain scope.

Do **not** propose changes to `app/` or `frontend/` without first confirming the change is a bug fix or security fix with file-level evidence. Record any such change in `docs/final-ai-review.md`.

## CI guardrails

- The CI workflow (`.github/workflows/ci.yml`) must run `pytest`. Do not use `continue-on-error`, `|| true`, or skip the test step.
- Pin a specific Python version (e.g., `3.11`). Do not use `python-version: "*"`.

## Ownership rule

Every changed line, config choice, and AI suggestion must be explainable by the developer. If you cannot explain it, do not submit it.
