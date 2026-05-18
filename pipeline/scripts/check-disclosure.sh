#!/usr/bin/env bash
# pipeline/scripts/check-disclosure.sh <ATTACKS/path.md> [--log-db]
# Lints disclosure-status frontmatter on an ATTACKS entry per ADR-003.
# Exit 0 = safe to push public, exit 1 = blocked.

set -euo pipefail
cd "$(dirname "$0")/../.."

FILE="${1:-}"
LOG_TO_DB="${2:-}"

[ -z "$FILE" ] && { echo "usage: check-disclosure.sh <path> [--log-db]"; exit 2; }
[ -f "$FILE" ] || { echo "FAIL: $FILE not found"; exit 1; }

FM=$(awk '/^---$/{c++; next} c==1' "$FILE")
status=$(echo "$FM" | grep -E '^disclosure_status:' | head -1 | awk '{print $2}')
target=$(echo "$FM" | grep -E '^disclosure_target:' | head -1 | awk '{print $2}')
title=$(echo "$FM" | grep -E '^title:' | head -1 | sed 's/^title:[[:space:]]*//; s/^"//; s/"$//')
attack_date=$(echo "$FM" | grep -E '^date:' | head -1 | awk '{print $2}')
SLUG=$(basename "$FILE" .md)

log_to_db() {
  local passed="$1"
  local reason="$2"
  export REDTEAM_ATTACK_SLUG="$SLUG"
  export REDTEAM_ATTACK_TITLE="${title:-$SLUG}"
  export REDTEAM_ATTACK_DATE="${attack_date:-$(date -u +%Y-%m-%d)}"
  export REDTEAM_DISCLOSURE_PASSED="$passed"
  export REDTEAM_DISCLOSURE_REASON="$reason"
  python3 - <<'PY'
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from lab.database import RedTeamDatabase

db = RedTeamDatabase(os.environ.get("REDTEAM_DB_PATH"))
slug = os.environ["REDTEAM_ATTACK_SLUG"]
passed = os.environ["REDTEAM_DISCLOSURE_PASSED"] == "true"
reason = os.environ["REDTEAM_DISCLOSURE_REASON"] or None

with db.get_connection() as conn:
    attack = conn.execute("SELECT id FROM attacks WHERE slug = ?", (slug,)).fetchone()

if attack is None:
    attack_id = db.create_attack(
        {
            "slug": slug,
            "title": os.environ["REDTEAM_ATTACK_TITLE"],
            "date": os.environ["REDTEAM_ATTACK_DATE"],
            "disclosure_status": "green" if passed else None,
        }
    )
else:
    attack_id = attack["id"]

db.create_disclosure_check(
    {
        "attack_id": attack_id,
        "passed": passed,
        "reason": reason,
        "disclosure_status_green": passed,
        "user_acknowledged": False,
    }
)
print(f"Logged disclosure check to database for attack '{slug}'")
PY
}

case "$status" in
  green)
    echo "OK: $FILE disclosure_status=green"
    if [ "$LOG_TO_DB" = "--log-db" ] || [ "$LOG_TO_DB" = "true" ]; then
      log_to_db true ""
    fi
    exit 0
    ;;
  yellow|red)
    ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    mkdir -p pipeline
    echo "{\"ts\":\"$ts\",\"event\":\"disclosure-block\",\"file\":\"$FILE\",\"status\":\"$status\",\"target\":\"$target\"}" >> pipeline/_violations.jsonl
    echo "BLOCK: $FILE disclosure_status=$status (logged)"
    if [ "$LOG_TO_DB" = "--log-db" ] || [ "$LOG_TO_DB" = "true" ]; then
      log_to_db false "disclosure_status=$status"
    fi
    exit 1
    ;;
  *)
    echo "FAIL: $FILE missing or invalid disclosure_status (got: '$status')"
    exit 1
    ;;
esac
