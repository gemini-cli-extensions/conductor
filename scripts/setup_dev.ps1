Write-Host "Installing development dependencies..."
pip install mypy ruff pre-commit pytest-cov pyrefly

Write-Host "Installing project in editable mode..."
pip install -e .

Write-Host "Installing pre-commit hooks..."
pre-commit install

Write-Host "Development environment setup complete!"
