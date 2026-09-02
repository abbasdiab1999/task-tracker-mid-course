# Mini ADR — Mid-Course Feature Design

**Status:** Accepted

## Context
The Task Tracker needed two small end-to-end features that could be implemented, tested, demonstrated, and explained within the project timebox. I selected **Due Dates + Overdue Filter** and **Tags / Labels**.

## Decision
Due dates are stored directly on each task as an optional date. Overdue state is **computed**, not persisted, because it depends on the current date and task status. The backend exposes an `overdue` boolean in task responses and supports an optional overdue filter.

Tags are stored on each task as a normalized list of strings. Validation trims tags, rejects blanks, limits length, and removes case-insensitive duplicates. Tag filtering uses a case-insensitive exact match.

## Alternatives considered
1. **Persist an `overdue` field.** Rejected because it can become stale as time passes or status changes.
2. **Create a separate Tag model/table.** Rejected as unnecessary complexity for an in-memory Module 3 project.
3. **Use comma-separated tags internally.** Rejected because a list is easier to validate, update, and test.
4. **Add task comments instead.** Rejected because it would introduce additional models/endpoints and increase scope.

## Consequences
The implementation remains small and testable. The due-date rule lives in one backend function, and tag normalization lives in Pydantic validation. The frontend only needs small additions to the existing create form, cards, and filter controls.
