# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: **yes** — Python 3.11, FastAPI, uvicorn, pytest command with `PYTHONPATH=.`, Docker build/run commands.
- Docs-first/read-first guardrail included: **yes** — "Before generating or changing code, read AGENTS.md, the relevant source file, and docs/midcourse/mini-adr.md."
- Unexpected app/frontend edits rule included: **yes** — "Only change app/ or frontend/ for a bug fix or security fix. Record any such change in docs/final-ai-review.md."

## AI code review mini-log

The file reviewed is `app/main.py` (the FastAPI application entrypoint).

| AI comment | Grade | Reason | Verification or decision |
|---|---|---|---|
| "CORS `allow_origins` includes `http://localhost:5500` and `http://127.0.0.1:5500`; in production these should be restricted to known domains." | **Useful** | Correct observation. Wildcard-style development origins are fine for a local tool but the comment correctly flags that this list would need tightening before a real deployment. | Accepted as a note. No change made because this app is intentionally a local-only course project with no production deployment. |
| "Consider adding `limit` and `offset` query parameters to `GET /tasks` for pagination." | **Noise** | Pagination is a new product feature and the brief explicitly prohibits adding features. AI did not check scope constraints before suggesting this. | Rejected. Violates the no-new-features ground rule. |
| "The `serialize` helper could be replaced with a computed field on `TaskResponse` using Pydantic's `@computed_field`." | **Noise** | This is a style preference, not a bug or security issue. The current approach is readable and tested. Refactoring would risk introducing regressions for no functional gain. | Rejected. Beyond scope of final project. |

## AI security mini-review

| Finding | File evidence | Grade | Reason | Next action |
|---|---|---|---|---|
| In-memory storage means all tasks are lost on restart; no persistence means no risk of data exposure through DB credentials or SQL injection. | `app/storage.py` lines 1-40 — no DB connection strings, no external calls | **Valid** | The in-memory design eliminates a whole class of persistence-layer vulnerabilities. It is an intentional architectural choice recorded in `docs/midcourse/mini-adr.md`. | No action needed; document in release evidence. |
| No authentication or authorisation on any endpoint — any client can read, create, or delete tasks. | `app/main.py` — all routes have no auth dependency | **Valid** | The brief explicitly prohibits adding authentication as a new feature. The risk is accepted for a local course tool not exposed to the internet. | Noted. Would be first thing to add if scope expanded. |
| `allow_credentials=True` in CORS middleware combined with broad `allow_methods=["*"]` and `allow_headers=["*"]` allows any credentialed cross-origin request from the listed origins. | `app/main.py` lines 18-23 | **False Positive** | The listed origins are `localhost` variants only, not wildcards. `allow_credentials=True` with explicit origin list is acceptable for a local tool. FastAPI/Starlette enforce that `allow_origins=["*"]` and `allow_credentials=True` cannot be used together. | No change. AI flagged this without checking the origin list carefully. |

## Manual security check

I manually read `app/storage.py` and `app/models.py` to check for any path-traversal or injection risk. The storage module uses integer dict keys and the models use Pydantic field validators (`min_length`, `field_validator` on `title` and `tags`). There is no file I/O, no shell command execution, and no templating that could accept unsanitised user input. The `title` field is stripped of leading/trailing whitespace and rejected if blank. Tags are stripped, deduplicated, and length-capped at 30 characters. No injection surface was found beyond the unauthenticated endpoints already noted above.

## One AI output I rejected or corrected

AI suggested adding pagination (`limit` / `offset`) query parameters to `GET /tasks` to "improve scalability". I rejected this because:
1. The project brief explicitly prohibits new product features.
2. The in-memory storage holds a small number of tasks in a course context — pagination adds complexity with zero benefit.
3. Accepting it would mean explaining an untested API change to a grader who checks scope compliance.

I recorded the suggestion here as evidence of active review rather than blind acceptance.

## Three AI usage rules

1. **Never paste**: credentials, `.env` values, tokens, production logs, or real personal/customer data into AI prompts or the repo.
2. **Always verify**: run every AI-suggested command and check its output before recording it as evidence. A command that AI says works is only evidence after I have run it myself.
3. **Record AI contributions by**: noting in `docs/final-ai-review.md` which suggestions were used, graded, corrected, or rejected, so the diff between AI output and my decision is visible.

## Ownership statement

I wrote the task tracker backend and tests during the mid-course sprint, starting from a FastAPI template and adding due-date and tag features myself. For the final project I used AI to draft the CI workflow, Dockerfile, and documentation templates, then reviewed each file line by line: I corrected the pytest command to include `PYTHONPATH=.`, removed a suggested pagination feature that violated the scope rules, and verified the CORS finding was a false positive by reading the origin list. Every file in this repo can be explained by me at the line level. I am comfortable submitting this as my own work because the decisions — what to include, what to reject, and what to verify — were mine throughout.
