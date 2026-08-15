Give me a standup-ready status of ShipIt, end to end.

Use Frank's MCP tools (mcp__frank__*) — do not guess:

1. `instance_health` and `service_status("shipit")` — is the box and the
   service healthy?
2. `list_workflow_runs` (last 5) — is CI green? If a run failed, call
   `get_failed_jobs` and name the failing step.
3. `deploy_status` — what's actually deployed right now?

Then summarize in under 10 lines, newest problem first:
- One line each: service, pipeline, deploy
- If anything is red: what broke, where to look, and the single next action
- If everything is green: say so in one line and stop — no padding
