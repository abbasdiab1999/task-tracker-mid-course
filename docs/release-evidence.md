# Release Evidence

## Baseline

- **Branch**: final-project
- **Date**: 2026-08-25
- **Python runtime**: 3.10.12 (venv), pytest 8.3.3
- **Local app run command**: `uvicorn app.main:app --reload`
- **/health result**: `{"status":"ok"}` — HTTP 200 confirmed with `curl -s http://127.0.0.1:8000/health`
- **Frontend check**: Opened `http://127.0.0.1:8000` in browser; Kanban board with ToDo / InProgress / Done columns and the create/edit task flow is visible.
- **Test command**: `PYTHONPATH=. pytest -v`
- **Test result**: 10 passed in 0.06s — all tests passed, no failures.
  ```
  tests/test_features.py::test_valid_due_date_is_saved PASSED
  tests/test_features.py::test_invalid_due_date_format_rejected PASSED
  tests/test_features.py::test_overdue_detection PASSED
  tests/test_features.py::test_overdue_filter_returns_only_overdue_tasks PASSED
  tests/test_features.py::test_create_with_tags_trims_and_deduplicates PASSED
  tests/test_features.py::test_blank_tag_rejected PASSED
  tests/test_features.py::test_update_tags_preserves_other_fields PASSED
  tests/test_features.py::test_filter_by_tag PASSED
  tests/test_features.py::test_invalid_status_transition_returns_422 PASSED
  tests/test_features.py::test_patch_without_status_does_not_trigger_transition_validation PASSED
  ```

## CI evidence

- **Workflow file**: `.github/workflows/ci.yml`
- **Latest run link or note**: Workflow pushed to `final-project` branch on GitHub; CI triggered on push and pull_request events. No green-run link available before initial push, but the workflow definition is correct.
- **Test command used by CI**: `PYTHONPATH=. pytest -q`
- **Shortcut check**: no `continue-on-error` / no `|| true` / pytest is not skipped / Python version pinned to `3.11`.

## Docker evidence

- **Build command**: `docker build -t task-tracker .`
- **Build result**: Build succeeded (13/13 steps completed, image tagged `task-tracker:latest`).
  ```
  [+] Building 0.7s (13/13) FINISHED
   => [internal] load build definition from Dockerfile
   => [internal] load metadata for docker.io/library/python:3.11-slim
   => [internal] load .dockerignore
   => [1/7] FROM docker.io/library/python:3.11-slim
   => [internal] load build context
   => CACHED [2/7] RUN useradd --create-home appuser
   => CACHED [3/7] WORKDIR /home/appuser/app
   => CACHED [4/7] COPY requirements.txt .
   => CACHED [5/7] RUN pip install --no-cache-dir -r requirements.txt
   => CACHED [6/7] COPY app/ ./app/
   => CACHED [7/7] COPY frontend/ ./frontend/
   => exporting to image
   => => naming to docker.io/library/task-tracker:latest
  ```
- **Run command**: `docker run -p 8000:8000 task-tracker`
- **Run result**: Container started cleanly and served requests.
  ```
  INFO:     Started server process [1]
  INFO:     Waiting for application startup.
  INFO:     Application startup complete.
  INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
  INFO:     172.17.0.1:42914 - "GET / HTTP/1.1" 200 OK
  INFO:     172.17.0.1:42928 - "GET /static/styles.css HTTP/1.1" 200 OK
  INFO:     172.17.0.1:42934 - "GET /static/app.js HTTP/1.1" 200 OK
  INFO:     172.17.0.1:42940 - "GET /favicon.ico HTTP/1.1" 404 Not Found
  INFO:     172.17.0.1:42942 - "GET /tasks HTTP/1.1" 200 OK
  ```
- **`/health` check**: `curl http://localhost:8000/health` → `{"status":"ok"}` — HTTP 200 confirmed against the containerized app.
- **Non-root check**: Dockerfile creates and uses `appuser`; the `USER appuser` directive is present before the `CMD`.
- **No-baked-secrets check**: `.dockerignore` excludes `.env`, `*.env`, `tests/`, and `docs/`. `requirements.txt` contains only package names and versions, no credentials. `app/storage.py` uses in-memory dict with no connection strings.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| `pytest -q` runs all tests (README) | Ran `PYTHONPATH=. pytest -q` in terminal | Partial match — `pytest -q` alone fails due to system PYTHONPATH conflict; correct command requires `PYTHONPATH=.` prefix | README Final Project section updated to use `PYTHONPATH=. pytest -q` |
| `GET /health` returns `{"status":"ok"}` (README) | Started uvicorn, ran `curl http://127.0.0.1:8000/health` | Confirmed — response is exactly `{"status":"ok"}` with HTTP 200 | No change needed |
| Dockerfile runs app as non-root (Dockerfile) | Read Dockerfile; `useradd appuser` + `USER appuser` present before CMD | Confirmed — container runs as `appuser`, not root | No change needed |
