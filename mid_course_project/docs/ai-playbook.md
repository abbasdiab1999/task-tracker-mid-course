# My AI Playbook

## When I reach for AI first

- **Boilerplate config files** — CI YAML, Dockerfiles, `.gitignore`, editor configs. The structure is predictable and AI gets the shape right quickly; I review the specifics.
- **Unfamiliar CLI flags or API signatures** — e.g. "what flag disables pager in git?". Faster than docs search for one-off lookups.
- **First-draft documentation** — README sections, release-evidence templates. AI produces a starting structure; I fill in real commands and results.
- **Security checklist prompts** — "what OWASP issues should I check in a FastAPI app with no auth?" gives me a list to manually verify, not a list to blindly accept.
- **Test scaffolding** — generating a pytest fixture or a basic test function shape when I know what to assert but want to avoid boilerplate.

## When I do not reach for AI first

- **Business logic I haven't read yet** — if I haven't read `business_rules.py` myself first, AI changes to it are unverifiable.
- **Debugging runtime failures** — I read the traceback and the relevant code myself first. AI often produces plausible-sounding wrong guesses for runtime state issues.
- **Anything touching secrets or credentials** — I never paste `.env` files, tokens, or connection strings into an AI prompt.
- **Learning a concept for the first time** — if I am still building my mental model, accepting AI output skips the understanding I need to review it later.
- **Scope decisions** — whether a feature is in or out of scope is a human decision. AI does not know the brief constraints and will propose features that violate them.

## My non-negotiables

- Never paste credentials, `.env` values, tokens, production logs, or real personal data into an AI tool.
- Never commit AI-suggested code I cannot explain line by line.
- Always run AI-suggested commands myself before recording them as evidence.
- Always record AI contributions (used, rejected, corrected) so the audit trail exists.
- Never use `|| true`, `continue-on-error`, or skip test steps in CI to make a workflow "green".

## My review rules

1. Read the diff line by line — not just the summary.
2. Run every suggested command and compare the actual output to what AI said would happen.
3. Grade each AI finding: **Useful** (correct and actionable), **Noise** (not wrong but irrelevant to scope), or **Wrong** (factually incorrect or scope-violating).
4. Reject or correct anything graded Noise or Wrong before merging.
5. Record one rejected suggestion per review session so the decision is visible.

## What I am still figuring out

- How to set consistent AI guardrails on a team where different people have different risk tolerances.
- When a Dockerfile or CI workflow is "good enough" versus when to spend time on hardening that's unlikely to matter for a course project.
- How to evaluate AI security findings quickly without becoming either too credulous (accept everything) or too dismissive (ignore everything).

## Decision Card

| Situation | AI role | Human gate |
|---|---|---|
| **New feature** | Draft shape only — no logic | Read brief, verify scope, run tests |
| **Code review** | List potential issues | Grade each finding; verify with file evidence |
| **Debugging** | Suggest hypotheses | Read traceback first; test each hypothesis manually |
| **Infrastructure** | Draft config | Run every command; check outputs match claims |
| **Never paste** | — | Credentials, tokens, `.env`, production data |
| **One rule** | AI drafts; I decide | No AI suggestion ships without a line-level review |
