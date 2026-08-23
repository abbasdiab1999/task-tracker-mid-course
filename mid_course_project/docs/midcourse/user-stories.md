# User Stories

## Feature 1 — Due Dates + Overdue Filter

### Story 1
As a team member, I want to optionally assign a due date when creating a task so that I can see when the task is expected to be completed.

**Acceptance criteria**
- A task may be created without a due date.
- A valid ISO date is accepted and returned by the API.
- An invalid date format returns HTTP 422.
- The due date is visible on the task card in the frontend.

### Story 2
As a team member, I want overdue tasks to be clearly identified so that I can prioritize late work.

**Acceptance criteria**
- A task is overdue when its due date is before today and its status is not `Done`.
- A completed task is not shown as overdue.
- Overdue tasks display an `OVERDUE` pill in the frontend.

### Story 3
As a team member, I want to filter the board to overdue tasks so that I can focus only on delayed work.

**Acceptance criteria**
- `GET /tasks?overdue=true` returns only overdue tasks.
- `GET /tasks?overdue=false` excludes overdue tasks.
- An empty result returns `200` with `[]`.

**AI assumption corrected:** The initial design treated every past-due task as overdue, including completed tasks. I corrected the rule so `Done` tasks are not considered overdue.

---

## Feature 2 — Tags / Labels

### Story 1
As a team member, I want to add tags to a task so that I can categorize related work.

**Acceptance criteria**
- A task may have zero or more tags.
- Tags are trimmed before storage.
- Blank tags are rejected with HTTP 422.
- Duplicate tags are removed case-insensitively.
- Each tag is at most 30 characters.

### Story 2
As a team member, I want tags shown on task cards so that I can understand task categories at a glance.

**Acceptance criteria**
- Each tag is rendered as a compact chip/pill.
- A task with no tags renders normally.
- Updating tags does not overwrite unrelated fields.

### Story 3
As a team member, I want to filter tasks by tag so that I can quickly find work in one category.

**Acceptance criteria**
- `GET /tasks?tag=<value>` performs a case-insensitive exact tag match.
- Only tasks containing the selected tag are returned.
- No matches returns `200` with `[]`.

**AI assumption corrected:** The first design preserved duplicate tags with different capitalization. I changed the validator to de-duplicate tags case-insensitively while preserving the first entered form.
