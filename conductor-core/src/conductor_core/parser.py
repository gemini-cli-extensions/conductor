import re
from pathlib import Path
from .models import Plan, Phase, Task, TaskStatus

class MarkdownParser:
    @staticmethod
    def parse_plan(content: str) -> Plan:
        phases = []
        current_phase = None
        
        lines = content.splitlines()
        for line in lines:
            # Match Phase heading
            phase_match = re.match(r"^##\s+(?:Phase\s*\d+:\s*)?(.*?)(?:\s*\[checkpoint:\s*([0-9a-f]+)\])?$", line, re.IGNORECASE)
            if phase_match:
                current_phase = Phase(name=phase_match.group(1).strip(), checkpoint_sha=phase_match.group(2))
                phases.append(current_phase)
                continue
            
            # Match Task
            task_match = re.match(r"^\s*-\s*\[([ x~])\]\s*(?:Task:\s*)?(.*?)(?:\s*\[([0-9a-f]{7,})\])?$", line)
            if task_match and current_phase:
                status_char = task_match.group(1)
                description = task_match.group(2).strip()
                sha = task_match.group(3)
                
                status = TaskStatus.PENDING
                if status_char == "x": status = TaskStatus.COMPLETED
                if status_char == "~": status = TaskStatus.IN_PROGRESS
                
                current_phase.tasks.append(Task(description=description, status=status, commit_sha=sha))
        
        return Plan(phases=phases)

    @staticmethod
    def serialize_plan(plan: Plan) -> str:
        lines = [f"# Implementation Plan: {plan.track_id}", ""]
        for i, phase in enumerate(plan.phases, 1):
            checkpoint = f" [checkpoint: {phase.checkpoint_sha}]" if phase.checkpoint_sha else ""
            lines.append(f"## Phase {i}: {phase.name}{checkpoint}")
            for task in phase.tasks:
                sha = f" [{task.commit_sha[:7]}]" if task.commit_sha else ""
                lines.append(f"- [{task.status.value}] Task: {task.description}{sha}")
            lines.append("")
        return "
".join(lines)
