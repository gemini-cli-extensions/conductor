"""Determines the next unblocked setup step in the Conductor workflow."""

import json
import os
import sys


def determine_resumption():
  """Checks existing setup artifacts and returns the next unblocked step."""
  # Accept the project root as argv[1] so this script is correct from any cwd.
  # SKILL.md invokes it by a path relative to the skill directory while this
  # resolved conductor/ relative to cwd; no single working directory satisfied
  # both. Defaults to cwd, so existing callers are unaffected.
  project_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
  conductor_dir = os.path.join(project_root, "conductor")
  files = [
      "product.md",
      "product-guidelines.md",
      "tech-stack.md",
      "code_styleguides",
      "workflow.md",
  ]

  checklist = {}
  for filename in files:
    path = os.path.join(conductor_dir, filename)
    checklist[filename] = os.path.exists(path)

  setup_complete = os.path.exists(os.path.join(conductor_dir, "index.md"))

  next_step = None

  chain = [
      ("product.md", "Product Definition"),
      ("product-guidelines.md", "Product Guidelines"),
      ("tech-stack.md", "Technology Stack"),
      ("code_styleguides", "Code Style Guides"),
      ("workflow.md", "Workflow Configuration"),
  ]

  for filename, step_name in chain:
    if not checklist[filename]:
      next_step = {
          "step": step_name,
          "file": filename,
      }
      break

  return {
      "setup_complete": setup_complete,
      "checklist": checklist,
      "next_step": next_step,
  }


if __name__ == "__main__":
  result = determine_resumption()
  print(json.dumps(result, indent=2))
  sys.exit(0)
