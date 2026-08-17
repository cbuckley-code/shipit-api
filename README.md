# ShipIt — the course monorepo

The demo project for **Claude for Engineering Teams — From Chat to Agent
Pipelines**. A small FastAPI shipments service with a real test suite and
CI — plus **Frank**, the team's MCP server, living in `frank/` with a
push-to-deploy pipeline to Azure.

```
app/ tests/            the product (deliberately small and boring)
frank/                 the team's MCP surface (+ its own CLAUDE.md)
docs/                  brief, ADRs, plans — the source of truth
.claude/               team playbook: settings.json + commands/ + agents/
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
| 2.3 | VS Code deep-dive: `scripts/stage_bug.sh` breaks a real test; Claude fixes it hunk-by-hunk |
| 3.1 | `CLAUDE.md` is built on camera — repo memory for every agent session |
| 5.x | Frank's GitHub tools point at this repo's Actions runs |
| 6.2 | Repair loop: stage the bug, push, CI goes red, `agent-repair.yml` opens the fix PR |
| 7.x | beads database lives here (`bd init` on camera in 7.2); agents work the queue |
| 7.6 | Money demo: "Add rate limiting to the API" — intentionally **not implemented**, agents build it live |

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

**No rate limiting. No auth on write paths.** Both are intentional gaps —
they're the stories the PM writes in Jira for the Section 7 demos.

## Task tracking (Section 7)

Initialize beads on camera in Lecture 7.2:

```bash
bd init
bd create "Add rate limiting to the API" -p 1
bd ready
```

`CLAUDE.md` already tells agents to run `bd ready` before starting work.

## Deploying next to Frank (optional, Section 6)

Run it as a systemd service on the same EC2 box as Frank so
`service_status("shipit")` and `tail_log("shipit")` return live data.
See `frank-mcp-server/deploy/ec2-setup.md` for the unit file pattern.
