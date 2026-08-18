# ShipIt — the course monorepo

The demo project for **Claude for Engineering Teams — From Chat to Agent
Pipelines**. A small FastAPI shipments service with a real test suite and
CI — plus **Frank**, the team's MCP server, living in `frank/` with a
push-to-deploy pipeline to Azure.

```
app/ tests/            the product (deliberately small and boring)
frank/                 the team's MCP surface (+ its own CLAUDE.md)
docs/                  brief, ADRs, plans — the source of truth
.claude/               team playbook: settings.json + commands/ + skills/ + rules/ + agents/
.github/workflows/     ci.yml · agent-repair.yml · deploy-frank.yml
infra/azure-setup.md   fork + one secret + push → Frank is live
```

Monorepo on purpose: one checkout gives an agent the product, the infra,
the docs, and the playbook — cross-cutting changes land in one PR, and
nested CLAUDE.md files scope memory per directory.

## Quick start

**Fork this repo first** (recommended — Sections 5–7 of the course need CI
runs and PRs in a repo you own, and your Claude Project can read your fork
via the GitHub connector). A plain clone works if you're just following
along. After forking, enable workflows on your fork (Actions tab → enable).

```bash
git clone https://github.com/YOUR-USERNAME/shipit-api.git
cd shipit-api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make test     # 16 tests, all green — your baseline
make run      # http://localhost:8000/docs
```

## Where this repo appears in the course

| Lecture | What happens here |
|---|---|
| 2.1–2.2 | The docs/ feed the ShipIt Project; you fork this repo and tour `.claude/` |
| 2.3 | Desktop Code tab: `scripts/stage_bug.sh` breaks a real test; you prompt the fix |
| 2.4 | VS Code: `/plan-feature rate limiting` → build it → push → CI green (`deploy-frank.yml` stays dormant — Section 4 wakes it) |
| 2.6 | CLI: the drill, the playbook, `CLAUDE.md` — then build the shipment-history feature terminal-only, driven from your phone |
| 4.x | Frank is built AND deployed here — `deploy-frank.yml` wakes up, Azure URL in the run summary |
| 5.2 | Repair loop: stage the bug, push, CI goes red, `agent-repair.yml` opens the fix PR |
| 5.5 | Money demo: "Auth on write paths" — intentionally **not implemented**, agents build it live |

## Secrets you'll add during the course

Values never go in the repo — add them on your fork under
**Settings → Secrets and variables → Actions**. Full steps: `infra/azure-setup.md`.

| Secret | Used by | When you add it |
|---|---|---|
| `AZURE_CREDENTIALS` | `deploy-frank.yml` (azure/login) | Section 4.5 — one Cloud Shell command creates it |
| `FRANK_AUTH_TOKEN` | `deploy-frank.yml` → Frank's bearer token | Section 4.5 — any long random string |
| `FRANK_GITHUB_TOKEN` | `deploy-frank.yml` → Frank's GitHub tools | Section 4.5 — fine-grained PAT, this repo, Actions: read |
| `ANTHROPIC_API_KEY` | `agent-repair.yml` (headless `claude -p`) | Section 5.2 — the repair loop's engine |
| `FRANK_URL` / `FRANK_TOKEN` *(optional)* | `agent-repair.yml` — diagnose via Frank | After Frank is live; without them the loop falls back to `gh` |

CI (`ci.yml`) needs no secrets — it's green on a bare fork.

## The on-camera bug

```bash
./scripts/stage_bug.sh        # 2.0 kg parcels overcharged; 1 test fails
./scripts/stage_bug.sh undo   # back to green
```

It's an inclusive-vs-exclusive tier boundary in `app/pricing.py` — small,
realistic, and it produces a clean failing-test narrative rather than a toy.

## API surface

- `GET /healthz` — liveness (Frank's `service_status` checks this)
- `POST /shipments` — create; cost computed from weight + expedited flag
- `GET /shipments[?status=]` — list/filter
- `GET /shipments/{id}` — fetch
- `POST /shipments/{id}/transition` — status transitions (label_created → dispatched → delivered, or cancelled)

**No rate limiting. No auth on write paths. No transition history endpoint.**
All three are intentional gaps: students build the first in VS Code (2.4)
and the second-to-last in the CLI (2.6); agents ship auth in the 5.5 money demo.

## Task tracking (Bonus section)

The bonus lectures show beads as the agent-fleet queue:

```bash
bd init
bd create "Add auth to write paths" -p 1
bd ready
```

`CLAUDE.md` already tells agents how plans in `docs/plans/` drive the work.

## Deploying Frank (Section 4)

Fork + one secret + push: see `infra/azure-setup.md`. The
`deploy-frank.yml` workflow builds `frank/` from source and prints
Frank's HTTPS `/mcp` URL in the run summary.
