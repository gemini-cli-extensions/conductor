#!/bin/bash
set -e

echo "Building Conductor VS Code Extension..."
cd conductor-vscode
npm install
npx vsce package -o ../conductor.vsix
echo "Build complete: conductor.vsix"
