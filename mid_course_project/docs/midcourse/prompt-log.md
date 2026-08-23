# AI Prompt Log

This log is intentionally concise. It records meaningful prompts and the decision made after inspecting the output.

## Feature 1 — Due dates

### Prompt 1 — Backend model and rule
**Prompt**
> Using the existing FastAPI Task Tracker structure, add an optional `due_date` to task create/update/response models. Compute an `overdue` boolean rather than storing it. A task is overdue only when due_date is before today and status is not Done. Keep changes limited to models and a small business-rule helper. Do not add authentication, databases, or unrelated refactors.

**AI response summary**
The AI proposed the optional date field, an `is_overdue()` helper, and response serialization.

**Decision**
Accepted the general structure. Edited the proposed overdue logic to explicitly exclude `Done` tasks.

### Prompt 2 — Overdue filtering
**Prompt**
> Add an optional `overdue: bool` query parameter to GET /tasks. Filter using the existing `is_overdue()` helper. Preserve existing status and priority filters. Empty matches must return 200 with an empty list.

**AI response summary**
The AI added the filter in the existing list route.

**Decision**
Accepted after verifying that filter combinations still worked.

## Feature 2 — Tags

### Prompt 3 — Tag validation
**Prompt**
> Add `tags: list[str]` to TaskCreate and optional tags to TaskUpdate. Trim each tag, reject blank tags, cap each tag at 30 characters, and de-duplicate case-insensitively while preserving first occurrence. Do not introduce a new tag database or model.

**AI response summary**
The AI proposed a Pydantic field validator.

**Decision**
Edited the validator so duplicate detection is case-insensitive.

### Prompt 4 — Tag filter
**Prompt**
> Extend GET /tasks with optional `tag`. Match tags case-insensitively and exactly. Keep all existing filters and return 200 [] when nothing matches.

**AI response summary**
The AI added a normalized comparison against each task's tag list.

**Decision**
Accepted after tests.

## Frontend

### Prompt 5 — Focused UI integration
**Prompt**
> Update only the existing Task Tracker frontend needed for the two features: add due date and comma-separated tags to the create form, show due date/overdue and tag chips on cards, and add overdue/tag filters. Keep the three Kanban columns and existing backend rules. If a PATCH request is rejected, show the server error and reload the board so the UI returns to server truth.

**AI response summary**
The AI added form inputs, card rendering, filters, and error handling.

**Decision**
Accepted with minor simplification. No framework, authentication, or unrelated visual redesign was added.

## Tests

### Prompt 6 — Targeted tests
**Prompt**
> Write focused pytest tests for valid/invalid due dates, overdue detection and filtering, tag trimming/deduplication, blank-tag rejection, tag updates preserving unrelated fields, tag filtering, and the existing invalid status-transition rule. Generate tests only; do not rewrite production code.

**AI response summary**
The AI generated focused API tests.

**Decision**
Accepted, then I used a Break Test to check whether the status-transition test was meaningful.
