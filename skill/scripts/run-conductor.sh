#!/usr/bin/env bash
set -euo pipefail

# Simple invoker for Conductor commands defined in commands/conductor/*.toml
# Usage: run-conductor.sh <command> [args]

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CMD_DIR="$REPO_ROOT/commands/conductor"

if [ $# -lt 1 ]; then
  echo "Usage: $0 <command> [args]"
  echo "Available commands:"
  ls -1 "$CMD_DIR" | sed 's/\.toml$//'
  exit 1
fi

cmd="$1"
shift || true

if command -v conductor >/dev/null 2>&1; then
  conductor "$cmd" "$@"
else
  toml="$CMD_DIR/${cmd}.toml"
  if [ -f "$toml" ]; then
    echo "No 'conductor' binary installed. Showing TOML: $toml"
    echo "---"
    sed -n '1,200p' "$toml"
  else
    echo "Unknown command: $cmd"
    echo "Available:"
    ls -1 "$CMD_DIR" | sed 's/\.toml$//'
    exit 2
  fi
fi