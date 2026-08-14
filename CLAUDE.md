# CLAUDE.md — ShipIt API

## Stack
Python 3.12, FastAPI, pytest, GitHub Actions. In-memory store (no database).

## Commands
- `make test` — run the test suite (must be green before any PR)
- `make lint` — ruff check
- `make run` — local dev server on :8000

## Conventions
- Tests first: every behavior change lands with a test that fails without it.
- Pricing tier boundaries are inclusive — see app/pricing.py docstring.
- No new dependencies without discussion in the issue first.
- Conventional commits (`fix:`, `feat:`, `test:`, `chore:`).
- Small PRs: one bead / one concern per branch.

## Task tracking
Run `bd ready` before starting work. Claim with `bd update <id> --status in_progress`,
close with `bd close <id>`, and end every session by writing the next-session
prompt into the bead comments.

## Pipeline
CI runs lint + tests on every push and PR (.github/workflows/ci.yml).
Frank (the team MCP server) exposes pipeline state — ask it for failed jobs
and logs instead of guessing.
