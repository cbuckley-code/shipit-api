"""Frank's audit log — every tool call is a recorded event (Lecture 5.5).

Kept in an in-memory ring buffer so `tail_log` can answer "what has Frank
been asked lately?" without any platform log plumbing. In a container
platform the ring resets on each revision — by design for the course;
production teams ship these lines to their log stack too (they also go
to stdout, which Azure Container Apps captures).
"""

from __future__ import annotations

import collections
import datetime
import json
import sys

import config

_ring: collections.deque = collections.deque(maxlen=config.AUDIT_MAX_ENTRIES)


def record(tool: str, **args) -> None:
    entry = {
        "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "tool": tool,
        "args": args,
    }
    _ring.append(entry)
    print(json.dumps({"audit": entry}), file=sys.stdout, flush=True)


def tail(n: int) -> list[dict]:
    return list(_ring)[-n:]
