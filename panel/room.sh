#!/usr/bin/env bash
# room.sh — run a panel session as a skillflow DAG.
#
# Builds the full graph (tensions -> select -> gate -> round, per round) and
# runs it. The selector seats every room mechanically; the gates stop every
# round until a person has done the colliding and approved the record.
#
# Usage: panel/room.sh "risk,measurement" 2 ./session1
#   $1  initial tensions, comma-separated
#   $2  number of rounds (default 2)
#   $3  session directory (default ./session-<timestamp>)
#
# Requires the `skillflow` CLI on PATH, or set SKILLFLOW_CMD, e.g.
#   SKILLFLOW_CMD="python3 -m skillflow.cli" PYTHONPATH=/path/to/skillflow
set -euo pipefail

TENSIONS="${1:?usage: room.sh \"tension1,tension2\" [rounds] [session-dir]}"
ROUNDS="${2:-2}"
SESSION="${3:-./session-$(date +%Y%m%d-%H%M%S)}"
PANEL_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -n "${SKILLFLOW_CMD:-}" ]; then
  # shellcheck disable=SC2206
  SF=($SKILLFLOW_CMD)
else
  command -v skillflow >/dev/null || {
    echo "error: skillflow CLI not found; pip install skillflow or set SKILLFLOW_CMD" >&2
    exit 2
  }
  SF=(skillflow)
fi

mkdir -p "$SESSION"
cd "$SESSION"
export SKILLFLOW_DB="$SESSION/skillflow.db"

"${SF[@]}" init >/dev/null
"${SF[@]}" add-node seed-panel --cmd "SKILLFLOW_DB='$SESSION/skillflow.db' python3 '$PANEL_DIR/seed.py'" >/dev/null
"${SF[@]}" add-node tensions --cmd "echo '$TENSIONS' > tensions.txt" >/dev/null
"${SF[@]}" add-edge seed-panel tensions >/dev/null
PREV="tensions"
i=1
while [ "$i" -le "$ROUNDS" ]; do
  "${SF[@]}" add-node "select-$i" --cmd \
    "python3 '$PANEL_DIR/select_room.py' --tensions \$(cat tensions.txt) --out room-$i.json" >/dev/null
  "${SF[@]}" add-node "round-$i" --cmd \
    "read -p 'Round $i room in room-$i.json. Collide, write record-$i.md, update tensions.txt. Continue? [y/N] ' a; [ \"\$a\" = y ]" >/dev/null
  "${SF[@]}" add-edge "$PREV" "select-$i" >/dev/null
  "${SF[@]}" add-edge "select-$i" "round-$i" >/dev/null
  PREV="round-$i"
  i=$((i + 1))
done

"${SF[@]}" run
