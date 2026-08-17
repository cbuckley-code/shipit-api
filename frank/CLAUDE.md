# CLAUDE.md — frank/ (nested memory: loads when work touches this directory)

Frank is ShipIt's MCP surface: he serves the tools and live context of the
team's environment to every agent. Python + FastMCP, flat module layout
(`server.py`, `config.py`, `tools_infra.py`, `tools_github.py`, `audit.py`).

## Rules for this directory
- Every tool: one job, typed inputs, small capped output. Agents compose
  tools; never build "do everything" tools.
- Every tool records itself via `audit.record()` — first line of the body.
- All configuration from env vars via `config.py`. No secrets in code, ever.
- GitHub tools are read-only by design; write access stays with humans.

## Run & deploy
- Local: `python server.py` (set FRANK_AUTH_TOKEN first).
- Deploy: push to main touching `frank/**` → `.github/workflows/
  deploy-frank.yml` → Azure Container Apps. See `infra/azure-setup.md`.
- The deploy workflow injects GIT_SHA / DEPLOYED_AT / FRANK_GITHUB_REPO —
  don't set them by hand.
