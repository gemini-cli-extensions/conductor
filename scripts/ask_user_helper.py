#!/usr/bin/env python3
"""AskUser Tool Helper - Structured user input for Conductor.

This module provides helper functions for using the AskUser tool
for structured user interactions in Conductor workflows.

Usage:
    from ask_user_helper import ask_yesno, ask_choice, ask_text, ask_batch
    
    # Yes/No question
    confirmed = ask_yesno("Do you want to proceed with the setup?")
    
    # Single choice
    framework = ask_choice("Select a framework:", ["React", "Vue", "Angular"])
    
    # Multi-select
    features = ask_choice("Select features:", ["Auth", "API", "Database"], multi=True)
    
    # Text input
    project_name = ask_text("Enter project name:", placeholder="my-project")
    
    # Batch questions
    responses = ask_batch([
        {"type": "text", "question": "Project name:", "key": "name"},
        {"type": "choice", "question": "Framework:", "options": ["React", "Vue"], "key": "framework"},
        {"type": "yesno", "question": "Enable TypeScript?", "key": "typescript"},
    ])
"""

import json
import sys
from typing import Any, Dict, List, Optional, Union


class AskUserTool:
    """AskUser tool wrapper for structured user input."""

    def __init__(self):
        """Initialize AskUser tool."""
        self.tool_name = "AskUser"

    def ask_yesno(self, question: str) -> bool:
        """Ask a yes/no question.

        Args:
            question: The question to ask

        Returns:
            True if yes, False if no
        """
        return self._call_tool({
            "type": "yesno",
            "question": question,
        })

    def ask_choice(
        self,
        question: str,
        options: List[str],
        multi: bool = False,
        default: Optional[Union[str, List[str]]] = None,
    ) -> Union[str, List[str]]:
        """Ask a single or multi-select choice question.

        Args:
            question: The question to ask
            options: List of options to choose from
            multi: If True, allow multiple selections
            default: Default value(s) if user skips

        Returns:
            Selected option(s)
        """
        return self._call_tool({
            "type": "choice",
            "question": question,
            "options": options,
            "multi": multi,
            "default": default,
        })

    def ask_text(
        self,
        question: str,
        placeholder: str = "",
        default: str = "",
        validate: Optional[str] = None,
    ) -> str:
        """Ask for text input.

        Args:
            question: The question to ask
            placeholder: Placeholder text for the input
            default: Default value if user skips
            validate: Regex pattern for validation (optional)

        Returns:
            User's text input
        """
        return self._call_tool({
            "type": "text",
            "question": question,
            "placeholder": placeholder,
            "default": default,
            "validate": validate,
        })

    def ask_batch(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Ask multiple questions in a single batch.

        Args:
            questions: List of question dicts with format:
                {
                    "type": "yesno|choice|text",
                    "question": "The question",
                    "key": "response_key",
                    "options": [...],  # for choice type
                    "multi": False,    # for choice type
                    "placeholder": "", # for text type
                    "default": "",     # optional default
                }

        Returns:
            Dict mapping keys to responses
        """
        return self._call_tool({
            "type": "batch",
            "questions": questions,
        })

    def _call_tool(self, params: Dict[str, Any]) -> Any:
        """Call the AskUser tool with given parameters.

        Args:
            params: Tool parameters

        Returns:
            User's response

        Note:
            This is a placeholder. In actual implementation, this would
            call the AskUser MCP tool via the appropriate interface.
        """
        # For now, return a placeholder response
        # In production, this would integrate with the actual AskUser tool
        print(f"[AskUser] {json.dumps(params, indent=2)}")
        print("[AskUser] (Waiting for user input...)")

        # Placeholder responses for testing
        if params.get("type") == "yesno":
            return True
        elif params.get("type") == "choice":
            options = params.get("options", [])
            if params.get("multi"):
                return options[:1] if options else []
            return options[0] if options else ""
        elif params.get("type") == "text":
            return params.get("default", "user-input")
        elif params.get("type") == "batch":
            responses = {}
            for q in params.get("questions", []):
                key = q.get("key", "unknown")
                if q.get("type") == "yesno":
                    responses[key] = True
                elif q.get("type") == "choice":
                    options = q.get("options", [])
                    responses[key] = options[0] if options else ""
                elif q.get("type") == "text":
                    responses[key] = q.get("default", "user-input")
            return responses

        return None


# Convenience functions
_ask_user = AskUserTool()


def ask_yesno(question: str) -> bool:
    """Ask a yes/no question using AskUser tool."""
    return _ask_user.ask_yesno(question)


def ask_choice(
    question: str,
    options: List[str],
    multi: bool = False,
    default: Optional[Union[str, List[str]]] = None,
) -> Union[str, List[str]]:
    """Ask a single or multi-select choice question using AskUser tool."""
    return _ask_user.ask_choice(question, options, multi, default)


def ask_text(
    question: str,
    placeholder: str = "",
    default: str = "",
    validate: Optional[str] = None,
) -> str:
    """Ask for text input using AskUser tool."""
    return _ask_user.ask_text(question, placeholder, default, validate)


def ask_batch(questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Ask multiple questions in a single batch using AskUser tool."""
    return _ask_user.ask_batch(questions)


def generate_skill_snippet() -> str:
    """Generate a code snippet for using AskUser in skills.

    Returns:
        Markdown code snippet for skill documentation
    """
    return '''```markdown
## AskUser Tool Examples

### Yes/No Question

Use for binary confirmations:

\`\`\`
- [ ] **Ask:** "Do you want to proceed with the setup?"
  - **Type:** yesno
  - **Expected:** true/false
\`\`\`

### Single Choice

Use for menu-style selections:

\`\`\`
- [ ] **Ask:** "Select a framework:"
  - **Type:** choice
  - **Options:** ["React", "Vue", "Angular", "Svelte"]
  - **Multi:** false
\`\`\`

### Multi-Select Choice

Use for feature selection:

\`\`\`
- [ ] **Ask:** "Which features do you need?"
  - **Type:** choice
  - **Options:** ["Authentication", "API", "Database", "Testing", "CI/CD"]
  - **Multi:** true
\`\`\`

### Text Input

Use for free-form input:

\`\`\`
- [ ] **Ask:** "Enter project name:"
  - **Type:** text
  - **Placeholder:** "my-awesome-project"
  - **Validate:** "^[a-z][a-z0-9-]*$"
\`\`\`

### Batch Questions

Use for related questions to reduce turns:

\`\`\`
- [ ] **Ask Batch:**
  - Project name (text)
  - Framework (choice)
  - Enable TypeScript (yesno)
\`\`\`
```'''


if __name__ == "__main__":
    # Demo/test mode
    print("="*60)
    print("AskUser Tool Helper - Demo")
    print("="*60)

    # Demo yesno
    print("\n1. Yes/No Question:")
    result = ask_yesno("Do you want to proceed?")
    print(f"   Response: {result}")

    # Demo choice
    print("\n2. Single Choice:")
    result = ask_choice(
        "Select a framework:",
        ["React", "Vue", "Angular", "Svelte"]
    )
    print(f"   Response: {result}")

    # Demo multi-select
    print("\n3. Multi-Select Choice:")
    result = ask_choice(
        "Select features:",
        ["Auth", "API", "Database", "Testing"],
        multi=True
    )
    print(f"   Response: {result}")

    # Demo text
    print("\n4. Text Input:")
    result = ask_text(
        "Enter project name:",
        placeholder="my-project",
        validate=r"^[a-z][a-z0-9-]*$"
    )
    print(f"   Response: {result}")

    # Demo batch
    print("\n5. Batch Questions:")
    result = ask_batch([
        {"type": "text", "question": "Project name:", "key": "name", "default": "demo-project"},
        {"type": "choice", "question": "Framework:", "options": ["React", "Vue"], "key": "framework"},
        {"type": "yesno", "question": "Enable TypeScript?", "key": "typescript"},
    ])
    print(f"   Response: {json.dumps(result, indent=2)}")

    print("\n" + "="*60)
    print("Demo complete!")
    print("="*60)
