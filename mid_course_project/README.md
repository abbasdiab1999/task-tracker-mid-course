# Task Tracker — Mid-Course Project

This repository is a compact FastAPI Task Tracker implementation prepared for the **AI-Assisted Feature Extension Sprint**. It demonstrates two scoped end-to-end features:

1. **Due Dates + Overdue Filter**
2. **Tags / Labels**

The implementation includes backend validation, filtering, a browser-based Kanban board, pytest coverage, and the required `docs/midcourse/` documentation.

## Project structure

```text
app/
  main.py
  models.py
  storage.py
  business_rules.py
frontend/
  index.html
  app.js
  styles.css
tests/
  conftest.py
  test_features.py
docs/midcourse/
  user-stories.md
  mini-adr.md
  prompt-log.md
  verification.md
  reflection.md
```

## Setup

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the backend + frontend

From the repository root:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

## Run tests

```bash
pytest -q
```

## Feature summary

### Due dates
- Optional due date on create/update.
- Invalid dates rejected by Pydantic.
- `overdue` is computed by the backend.
- Completed tasks are not considered overdue.
- `GET /tasks?overdue=true|false` supported.
- Due date and overdue state shown in the UI.

### Tags
- Zero or more tags per task.
- Tags are trimmed.
- Blank tags rejected.
- Maximum 30 characters per tag.
- Case-insensitive de-duplication.
- `GET /tasks?tag=<tag>` supported.
- Tags rendered as chips in the UI.

## Status transitions

Allowed transitions:

```text
ToDo -> InProgress
InProgress -> ToDo
InProgress -> Done
Done -> InProgress
```

Invalid transitions return HTTP 422.

## Submission checklist

- [x] Two scoped features implemented.
- [x] Both features visible in the frontend.
- [x] At least four new pytest tests.
- [x] User stories with acceptance criteria.
- [x] Mini ADR.
- [x] AI prompt log.
- [x] Verification record and Break Tests.
- [x] Reflection.
- [x] README run/test instructions.
- [ ] Merge/adapt these changes into the student's original Module 3 repository if required.
- [ ] Create/push public branch named `mid-course-project`.
- [ ] Replace baseline placeholder in `docs/midcourse/verification.md` with the original repository's actual test result.
- [ ] Submit the public repository URL.
