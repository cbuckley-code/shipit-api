"""Pass 2 — GitHub Actions tools (Lecture 5.4).

All read-only, all scoped to the single repo the fine-grained PAT allows —
the student's own fork, injected by the deploy workflow. Frank observes the
pipeline; write access never leaves the humans (Lecture 5.5).
"""

from __future__ import annotations

import requests

import audit
import config
from tools_infra import ToolError


def _gh(path: str, accept: str = "application/vnd.github+json") -> requests.Response:
    if not config.GITHUB_TOKEN or not config.GITHUB_REPO:
        raise ToolError(
            "GitHub tools are not configured — set FRANK_GITHUB_TOKEN and "
            "FRANK_GITHUB_REPO (owner/name)."
        )
    resp = requests.get(
        f"{config.GITHUB_API}/repos/{config.GITHUB_REPO}{path}",
        headers={
            "Authorization": f"Bearer {config.GITHUB_TOKEN}",
            "Accept": accept,
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=15,
    )
    if resp.status_code == 404:
        raise ToolError(f"GitHub returned 404 for {path} — check repo and PAT scope.")
    resp.raise_for_status()
    return resp


def list_workflow_runs(limit: int = 10) -> dict:
    """Most recent workflow runs: id, workflow, branch, status, conclusion."""
    audit.record("list_workflow_runs", limit=limit)
    limit = max(1, min(limit, 30))
    data = _gh(f"/actions/runs?per_page={limit}").json()
    return {
        "repo": config.GITHUB_REPO,
        "runs": [
            {
                "run_id": run["id"],
                "workflow": run["name"],
                "branch": run["head_branch"],
                "sha": run["head_sha"][:8],
                "status": run["status"],
                "conclusion": run["conclusion"],
                "created_at": run["created_at"],
                "url": run["html_url"],
            }
            for run in data.get("workflow_runs", [])
        ],
    }


def get_failed_jobs(run_id: int) -> dict:
    """Failed jobs in a run, with the failed steps named."""
    audit.record("get_failed_jobs", run_id=run_id)
    data = _gh(f"/actions/runs/{run_id}/jobs?per_page=50").json()
    failed = []
    for job in data.get("jobs", []):
        if job["conclusion"] == "failure":
            failed.append(
                {
                    "job_id": job["id"],
                    "name": job["name"],
                    "failed_steps": [
                        step["name"]
                        for step in job.get("steps", [])
                        if step.get("conclusion") == "failure"
                    ],
                    "url": job["html_url"],
                }
            )
    return {"run_id": run_id, "failed_jobs": failed, "count": len(failed)}


def get_job_log(job_id: int) -> dict:
    """Tail of a job's log — the failure is almost always at the end."""
    audit.record("get_job_log", job_id=job_id)
    resp = _gh(f"/actions/jobs/{job_id}/logs")
    text = resp.text
    truncated = len(text) > config.MAX_LOG_CHARS
    if truncated:
        text = text[-config.MAX_LOG_CHARS :]
    return {"job_id": job_id, "truncated": truncated, "log_tail": text}


def pr_checks(pr_number: int) -> dict:
    """Check runs for a PR's head commit: name, status, conclusion."""
    audit.record("pr_checks", pr_number=pr_number)
    pr = _gh(f"/pulls/{pr_number}").json()
    sha = pr["head"]["sha"]
    data = _gh(f"/commits/{sha}/check-runs?per_page=50").json()
    return {
        "pr": pr_number,
        "title": pr["title"],
        "head_sha": sha[:8],
        "checks": [
            {
                "name": check["name"],
                "status": check["status"],
                "conclusion": check["conclusion"],
            }
            for check in data.get("check_runs", [])
        ],
    }
