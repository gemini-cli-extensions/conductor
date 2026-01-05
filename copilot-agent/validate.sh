#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Validating copilot agent at $ROOT_DIR"

# Check manifest
if [ ! -f "$ROOT_DIR/agent-manifest.json" ]; then
  echo "Missing agent-manifest.json" >&2
  exit 1
fi

# Check adapters present and executable
for a in "$ROOT_DIR"/adapter/*.sh; do
  if [ ! -f "$a" ]; then
    echo "Missing adapter scripts in $ROOT_DIR/adapter" >&2
    exit 1
  fi
  chmod +x "$a"
done

# Validate homedir script
if [ ! -f "$ROOT_DIR/scripts/homedir-setup.sh" ]; then
  echo "Missing homedir-setup.sh" >&2
  exit 1
fi

chmod +x "$ROOT_DIR/scripts/homedir-setup.sh"

echo "All checks passed. Run ./validate.sh for more checks or try installing the homedir helper."