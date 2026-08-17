"""Frank's configuration — everything comes from the environment.

Frank holds the credentials so laptops don't have to (Lecture 5.5).
In the course deployment, these are injected by .github/workflows/
deploy-frank.yml from GitHub Actions secrets. Nothing here is ever
passed through a prompt.
"""

import os


# --- Transport -------------------------------------------------------------
HOST = os.environ.get("FRANK_HOST", "127.0.0.1")  # container sets 0.0.0.0
PORT = int(os.environ.get("FRANK_PORT", "8720"))

# Bearer token every MCP client must present. Generate with:
#   python -c "import secrets; print(secrets.token_urlsafe(32))"
AUTH_TOKEN = os.environ.get("FRANK_AUTH_TOKEN", "")

# --- Environment tools (pass 1, Lecture 5.3) -------------------------------
# Services Frank may health-check: "name=url" pairs, comma-separated.
# An allowlist, not a free-for-all.
#   FRANK_SERVICE_URLS="shipit=https://shipit.example.com/healthz"
_raw = os.environ.get("FRANK_SERVICE_URLS", "")
SERVICE_URLS = {}
for pair in _raw.split(","):
    if "=" in pair:
        name, _, url = pair.partition("=")
        SERVICE_URLS[name.strip()] = url.strip()

# Deploy metadata — baked in by the deploy workflow at push time.
GIT_SHA = os.environ.get("GIT_SHA", "unknown")
DEPLOYED_AT = os.environ.get("DEPLOYED_AT", "unknown")

# Audit ring buffer size (tail_log reads from this).
AUDIT_MAX_ENTRIES = int(os.environ.get("FRANK_AUDIT_MAX", "500"))

# --- GitHub tools (pass 2, Lecture 5.4) ------------------------------------
# Fine-grained PAT: ONE repo, Actions: read, nothing else (Lecture 5.5).
# FRANK_GITHUB_REPO is injected as the student's fork by the workflow.
GITHUB_TOKEN = os.environ.get("FRANK_GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("FRANK_GITHUB_REPO", "")  # "owner/name"
GITHUB_API = "https://api.github.com"

# Truncate job logs to the tail — the failure is almost always at the end.
MAX_LOG_CHARS = int(os.environ.get("FRANK_MAX_LOG_CHARS", "6000"))
