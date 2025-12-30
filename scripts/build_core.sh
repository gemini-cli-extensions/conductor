#!/bin/bash
set -e

echo "Building Conductor Core Package..."
cd conductor-core
python -m pip install --upgrade build
python -m build
echo "Build complete: conductor-core/dist/"
