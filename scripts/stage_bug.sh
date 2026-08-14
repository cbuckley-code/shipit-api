#!/usr/bin/env bash
# Stage (or unstage) the on-camera bug for the recording demos.
#
#   ./scripts/stage_bug.sh        # introduce the bug
#   ./scripts/stage_bug.sh undo   # restore correct behavior
#
# The bug: the small-parcel tier boundary becomes EXCLUSIVE instead of
# inclusive, so a parcel weighing exactly 2.0 kg is overcharged at the
# medium rate. tests/test_pricing.py::test_two_kg_boundary catches it.
#
# Used in:
#   Lecture 2.3 — VS Code deep-dive (genuinely broken test, not a toy)
#   Lecture 6.2 — CI repair loop (commit the bug, pipeline goes red)
set -euo pipefail
cd "$(dirname "$0")/.."

TARGET="app/pricing.py"

if [[ "${1:-}" == "undo" ]]; then
  sed -i.bak 's/if weight_kg < SMALL_PARCEL_MAX_KG:/if weight_kg <= SMALL_PARCEL_MAX_KG:/' "$TARGET"
  rm -f "$TARGET.bak"
  echo "Bug removed — boundary is inclusive again. Run: make test"
else
  sed -i.bak 's/if weight_kg <= SMALL_PARCEL_MAX_KG:/if weight_kg < SMALL_PARCEL_MAX_KG:/' "$TARGET"
  rm -f "$TARGET.bak"
  echo "Bug staged — 2.0 kg parcels now overcharged. Run: make test (expect 1 failure)"
fi
