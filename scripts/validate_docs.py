#!/usr/bin/env python3
"""Documentation validation script for conductor-next.

This script validates documentation files against the project's style guides:
- Markdown files (markdownlint rules)
- Mermaid diagrams
- CSL-JSON reference files
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Tuple


class DocumentationValidator:
    """Validates documentation files against style guides."""

    def __init__(self, base_path: Path = Path(".")):
        self.base_path = base_path
        self.errors: List[Tuple[Path, str]] = []
        self.warnings: List[Tuple[Path, str]] = []

    def validate_all(self) -> bool:
        """Run all validation checks.

        Returns:
            True if all checks pass, False otherwise.
        """
        print("🔍 Running documentation validation...\n")

        # Validate Markdown files
        self._validate_markdown_files()

        # Validate Mermaid files
        self._validate_mermaid_files()

        # Validate CSL-JSON files
        self._validate_csl_json_files()

        # Print results
        self._print_results()

        return len(self.errors) == 0

    def _validate_markdown_files(self) -> None:
        """Validate all Markdown files."""
        print("📄 Validating Markdown files...")

        md_files = list(self.base_path.rglob("*.md"))
        md_files = [f for f in md_files if not any(x in str(f) for x in ["node_modules", ".git", "vendor"])]

        for md_file in md_files:
            self._check_markdown_file(md_file)

        print(f"   Checked {len(md_files)} Markdown files\n")

    def _check_markdown_file(self, file_path: Path) -> None:
        """Check a single Markdown file."""
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")

            # Check for H1 heading (should exist and be first)
            heading_lines = [i for i, line in enumerate(lines) if line.startswith("#")]
            if heading_lines:
                first_heading_line = heading_lines[0]
                first_heading = lines[first_heading_line]
                if not first_heading.startswith("# "):
                    self.warnings.append((file_path, f"Line {first_heading_line + 1}: First heading should be H1"))

            # Check for frontmatter
            if content.startswith("---"):
                # Check if frontmatter is properly closed
                if content.count("---") < 2:
                    self.errors.append((file_path, "Frontmatter not properly closed"))

            # Check for code blocks without language
            code_block_pattern = r"^```\s*$"
            for i, line in enumerate(lines):
                if re.match(code_block_pattern, line):
                    self.warnings.append((file_path, f"Line {i + 1}: Code block without language specifier"))

            # Check line length (120 chars)
            for i, line in enumerate(lines):
                if len(line) > 120:
                    # Skip code blocks and tables
                    in_code_block = False
                    for j in range(i):
                        if lines[j].startswith("```"):
                            in_code_block = not in_code_block
                    if not in_code_block and not line.startswith("|"):
                        self.warnings.append((file_path, f"Line {i + 1}: Line exceeds 120 characters"))

            # Check for trailing whitespace
            for i, line in enumerate(lines):
                if line.rstrip() != line:
                    self.warnings.append((file_path, f"Line {i + 1}: Trailing whitespace"))

            # Check for multiple consecutive blank lines
            blank_count = 0
            for i, line in enumerate(lines):
                if line.strip() == "":
                    blank_count += 1
                    if blank_count > 2:
                        self.warnings.append((file_path, f"Line {i + 1}: Multiple consecutive blank lines"))
                else:
                    blank_count = 0

        except Exception as e:
            self.errors.append((file_path, f"Error reading file: {e}"))

    def _validate_mermaid_files(self) -> None:
        """Validate all Mermaid diagram files."""
        print("🧜 Validating Mermaid diagram files...")

        mmd_files = list(self.base_path.rglob("*.mmd"))
        mmd_files.extend(self.base_path.rglob("*.mermaid"))

        for mmd_file in mmd_files:
            self._check_mermaid_file(mmd_file)

        print(f"   Checked {len(mmd_files)} Mermaid files\n")

    def _check_mermaid_file(self, file_path: Path) -> None:
        """Check a single Mermaid file."""
        try:
            content = file_path.read_text(encoding="utf-8")

            # Check for diagram type
            valid_types = ["flowchart", "sequenceDiagram", "classDiagram", "erDiagram", "gantt", "graph"]
            has_valid_type = any(t in content for t in valid_types)

            if not has_valid_type:
                self.warnings.append((file_path, "No valid diagram type found"))

            # Check for node naming (should use descriptive names)
            # Simple check: warn if nodes are single letters
            single_letter_nodes = re.findall(r"\b([A-Z])\b", content)
            if single_letter_nodes:
                self.warnings.append((file_path, "Consider using descriptive node names instead of single letters"))

        except Exception as e:
            self.errors.append((file_path, f"Error reading file: {e}"))

    def _validate_csl_json_files(self) -> None:
        """Validate all CSL-JSON files."""
        print("📚 Validating CSL-JSON reference files...")

        csl_files = list(self.base_path.rglob("references.json"))
        csl_files.extend(self.base_path.rglob("*.csl.json"))

        for csl_file in csl_files:
            self._check_csl_json_file(csl_file)

        print(f"   Checked {len(csl_files)} CSL-JSON files\n")

    def _check_csl_json_file(self, file_path: Path) -> None:
        """Check a single CSL-JSON file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Check structure
            if "references" not in data:
                self.errors.append((file_path, "Missing 'references' array"))
                return

            refs = data["references"]
            if not isinstance(refs, list):
                self.errors.append((file_path, "'references' should be an array"))
                return

            # Check each reference
            for i, ref in enumerate(refs):
                # Required fields
                if "id" not in ref:
                    self.errors.append((file_path, f"Reference {i}: Missing 'id' field"))

                if "type" not in ref:
                    self.errors.append((file_path, f"Reference {i}: Missing 'type' field"))

                # Check ID format (alphanumeric + hyphens)
                if "id" in ref:
                    if not re.match(r"^[a-zA-Z0-9-]+$", ref["id"]):
                        self.warnings.append((file_path, f"Reference {i}: ID should be alphanumeric with hyphens only"))

                # Check date format
                if "issued" in ref:
                    issued = ref["issued"]
                    if "date-parts" not in issued:
                        self.warnings.append((file_path, f"Reference {i}: 'issued' should have 'date-parts'"))

        except json.JSONDecodeError as e:
            self.errors.append((file_path, f"Invalid JSON: {e}"))
        except Exception as e:
            self.errors.append((file_path, f"Error reading file: {e}"))

    def _print_results(self) -> None:
        """Print validation results."""
        print("=" * 60)
        print("VALIDATION RESULTS")
        print("=" * 60)

        if not self.errors and not self.warnings:
            print("\n✅ All documentation checks passed!")
            return

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for file_path, message in self.errors:
                print(f"   {file_path}: {message}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for file_path, message in self.warnings:
                print(f"   {file_path}: {message}")

        print("\n" + "=" * 60)

        if self.errors:
            print(f"\n❌ Validation FAILED: {len(self.errors)} error(s)")
            sys.exit(1)
        else:
            print(f"\n✅ Validation PASSED with {len(self.warnings)} warning(s)")


def main():
    """Main entry point."""
    validator = DocumentationValidator()
    success = validator.validate_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
