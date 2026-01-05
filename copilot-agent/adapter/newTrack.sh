#!/usr/bin/env bash
set -euo pipefail

if command -v conductor >/dev/null 2>&1; then
  conductor newTrack "$@"
else
  echo "No 'conductor' CLI detected; to run newTrack open: ../commands/conductor/newTrack.toml"
fi