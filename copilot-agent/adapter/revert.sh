#!/usr/bin/env bash
set -euo pipefail

if command -v conductor >/dev/null 2>&1; then
  conductor revert "$@"
else
  echo "No 'conductor' CLI detected; to run revert open: ../commands/conductor/revert.toml"
fi