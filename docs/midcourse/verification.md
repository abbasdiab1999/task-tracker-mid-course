# Verification Record

## Baseline
Before feature work, the intended baseline is:
- Start the FastAPI application.
- Confirm `GET /health` returns HTTP 200 and `{"status":"ok"}`.
- Run the existing pytest suite.
- Record the exact pass count from the student's original Module 3 repository.

> If this package is being merged into an existing course repository, replace this baseline note with the actual original pass count.

## Backend verification
Run:

```bash
pytest -q
```

Expected result for this prepared package: all tests pass.

The added tests cover:
- Valid due date.
- Invalid due-date format.
- Overdue calculation.
- Overdue filtering.
- Tag trimming and case-insensitive de-duplication.
- Blank tag rejection.
- Updating tags without overwriting unrelated fields.
- Filtering by tag.
- Invalid status transition.
- PATCH requests that do not include status.

## Manual browser checks
1. Create a task without due date/tags.
2. Create a task with a future due date and two tags.
3. Create a task with a past due date and confirm `OVERDUE` appears.
4. Filter by tag.
5. Filter to overdue tasks.
6. Move a ToDo task to InProgress and then Done.
7. Attempt an invalid transition through the API and verify the server returns 422.
8. Confirm a failed update does not leave the board in a false client-side state.

## Behavior contract
- `POST /tasks` returns 201.
- `DELETE /tasks/{id}` returns 204 when the task exists.
- Missing task IDs return 404.
- Invalid Pydantic input returns 422.
- Invalid status transitions return 422.
- `GET /tasks` filter combinations return 200, including zero-result cases.
- Frontend error handling keeps the backend as the source of truth.

## Break Test 1 — Status transition
**Protected behavior:** `ToDo -> Done` must be rejected.

**Break:** Temporarily bypass `validate_status_transition()` in the PATCH route.

**Expected result:** `test_invalid_status_transition_returns_422` fails because the route returns 200 instead of 422.

**Conclusion:** The test meaningfully protects the business rule.

## Break Test 2 — Blank tags
**Protected behavior:** blank/whitespace-only tags must be rejected.

**Break:** Temporarily remove the blank-tag check from the Pydantic validator.

**Expected result:** `test_blank_tag_rejected` fails.

**Conclusion:** The test protects the new tag validation rule.

## After-refactor verification
After any focused cleanup:
1. Re-run `pytest -q`.
2. Re-run the manual behavior contract.
3. Confirm no unrelated files changed.
