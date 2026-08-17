# CLAUDE.md — ShipIt (monorepo root)

## Repo layout
Monorepo: the product and its agent infrastructure live together, so one
checkout gives an agent the whole world.
- `app/` + `tests/` — the ShipIt API (this file governs it)
- `frank/` — the team's MCP surface; has its own nested CLAUDE.md that
  loads when work touches that directory
- `docs/` — brief, ADRs, plans (the source of truth)
- `.claude/` — team playbook: commands and agents, versioned like code
- `.github/workflows/` — CI, agent repair, and push-to-deploy for Frank

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

## Planning
Feature plans live in `docs/plans/` (template: `docs/templates/feature-plan.md`).
Work a plan's task table in order; each task's definition of done is the prompt.
End every session by updating the plan and writing the next-session prompt.
(Teams running beads instead: `bd ready` before starting work.)

## Slash commands
Team workflows live in `.claude/commands/` and are versioned with the code.
Start with `/plan-feature <name>` — it plans against the product brief and
ADRs in `docs/` before any code is written.

## Pipeline
CI runs lint + tests on every push and PR (.github/workflows/ci.yml).
Frank (the team MCP server) exposes pipeline state — ask it for failed jobs
and logs instead of guessing.
