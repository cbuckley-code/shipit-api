"""Frank — the course MCP server (Sections 5–7).

A custom MCP surface serving the tools and live context of ShipIt's
environment to every agent the team uses: Claude Desktop, Claude Code,
VS Code, and GitHub Copilot. One server. Every agent.

Local run:
    export FRANK_AUTH_TOKEN=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
    python server.py

Course deployment: push to main → .github/workflows/deploy-frank.yml
→ Azure Container Apps → the run summary prints Frank's HTTPS URL.

NOTE FOR RECORDING: FastMCP's auth API has been evolving — verify the
current auth-provider import against https://gofastmcp.com docs when you
record Lecture 5.5. The fallback below keeps Frank runnable either way.
"""

from __future__ import annotations

from fastmcp import FastMCP

import config
import tools_github
import tools_infra

# --- Auth: bearer token on the HTTP transport (Lecture 5.5) ----------------
auth = None
if config.AUTH_TOKEN:
    try:
        from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

        auth = StaticTokenVerifier(
            tokens={config.AUTH_TOKEN: {"client_id": "team", "scopes": []}}
        )
    except ImportError:
        print(
            "WARNING: StaticTokenVerifier not found in this FastMCP version; "
            "starting WITHOUT transport auth. Do not expose this bind."
        )

mcp = FastMCP(name="frank", auth=auth)

# --- Pass 1: environment (Lecture 5.3) -------------------------------------
mcp.tool(tools_infra.instance_health)
mcp.tool(tools_infra.service_status)
mcp.tool(tools_infra.tail_log)
mcp.tool(tools_infra.deploy_status)

# --- Pass 2: pipeline (Lecture 5.4) ----------------------------------------
mcp.tool(tools_github.list_workflow_runs)
mcp.tool(tools_github.get_failed_jobs)
mcp.tool(tools_github.get_job_log)
mcp.tool(tools_github.pr_checks)


if __name__ == "__main__":
    if not config.AUTH_TOKEN:
        print("WARNING: FRANK_AUTH_TOKEN is not set — do not expose this bind.")
    mcp.run(transport="http", host=config.HOST, port=config.PORT)
