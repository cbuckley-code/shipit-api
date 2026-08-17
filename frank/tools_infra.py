"""Pass 1 — environment tools (Lecture 5.3).

Each tool: one job, typed inputs, small output. Agents compose them —
we don't build "do everything" tools. Container-era design: health from
/proc, services checked over HTTP, deploy metadata baked in at push time.
"""

from __future__ import annotations

import shutil
import time
from pathlib import Path

import requests

import audit
import config


class ToolError(Exception):
    """Raised for user-visible tool failures (bad input, missing state)."""


def instance_health() -> dict:
    """CPU load, memory, disk, and uptime for the container Frank runs in."""
    audit.record("instance_health")
    load1, load5, load15 = Path("/proc/loadavg").read_text().split()[:3]

    meminfo = {}
    for line in Path("/proc/meminfo").read_text().splitlines():
        key, _, rest = line.partition(":")
        meminfo[key] = int(rest.strip().split()[0])  # kB

    disk = shutil.disk_usage("/")
    uptime_seconds = float(Path("/proc/uptime").read_text().split()[0])

    return {
        "load_avg": {"1m": float(load1), "5m": float(load5), "15m": float(load15)},
        "memory": {
            "total_mb": meminfo["MemTotal"] // 1024,
            "available_mb": meminfo["MemAvailable"] // 1024,
        },
        "disk_root": {
            "total_gb": round(disk.total / 1e9, 1),
            "free_gb": round(disk.free / 1e9, 1),
        },
        "uptime_hours": round(uptime_seconds / 3600, 1),
    }


def service_status(name: str) -> dict:
    """Health-check an allowlisted service over HTTP (status, latency)."""
    audit.record("service_status", name=name)
    url = config.SERVICE_URLS.get(name)
    if url is None:
        raise ToolError(
            f"service {name!r} is not in Frank's allowlist "
            f"({', '.join(config.SERVICE_URLS) or 'empty — set FRANK_SERVICE_URLS'}). "
            "Least privilege: Frank only checks services it was configured for."
        )
    started = time.monotonic()
    try:
        resp = requests.get(url, timeout=5)
        return {
            "service": name,
            "url": url,
            "ok": resp.ok,
            "status_code": resp.status_code,
            "latency_ms": round((time.monotonic() - started) * 1000),
        }
    except requests.RequestException as exc:
        return {"service": name, "url": url, "ok": False, "error": str(exc)}


def tail_log(lines: int = 50) -> dict:
    """Recent tool-call audit entries — what has Frank been asked lately?"""
    lines = max(1, min(lines, config.AUDIT_MAX_ENTRIES))
    audit.record("tail_log", lines=lines)
    return {"lines": lines, "entries": audit.tail(lines)}


def deploy_status() -> dict:
    """What's deployed right now — baked in by the deploy workflow."""
    audit.record("deploy_status")
    return {
        "git_sha": config.GIT_SHA,
        "deployed_at": config.DEPLOYED_AT,
        "repo": config.GITHUB_REPO or "unset",
    }
