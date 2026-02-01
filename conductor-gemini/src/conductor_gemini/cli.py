import os
import sys

import click
from conductor_core.errors import ConductorError
from conductor_core.models import CapabilityContext, PlatformCapability
from conductor_core.project_manager import ProjectManager
from conductor_core.task_runner import TaskRunner


class Context:
    def __init__(self, base_path=None) -> None:
        self.base_path = base_path or os.getcwd()
        self.manager = ProjectManager(self.base_path)
        # Gemini CLI has terminal and file system access
        self.capabilities = CapabilityContext(
            available_capabilities=[PlatformCapability.TERMINAL, PlatformCapability.FILE_SYSTEM, PlatformCapability.VCS]
        )
        self.runner = TaskRunner(self.manager, capability_context=self.capabilities)


def handle_error(e) -> None:
    if isinstance(e, ConductorError):
        data = e.to_dict()
        click.echo(f"[{data['error']['category'].upper()}] ERROR: {data['error']['message']}", err=True)
        if data["error"]["details"]:
            click.echo(f"Details: {data['error']['details']}", err=True)
    else:
        click.echo(f"UNEXPECTED ERROR: {e}", err=True)
    sys.exit(1)


@click.group()
@click.option("--base-path", type=click.Path(exists=True), help="Base path for the project")
@click.pass_context
def main(ctx, base_path) -> None:
    """Conductor Gemini CLI Adapter"""
    ctx.obj = Context(base_path)


@main.command()
@click.option("--goal", required=True, help="Initial project goal")
@click.pass_obj
def setup(ctx, goal) -> None:
    """Initialize a new Conductor project"""
    try:
        ctx.manager.initialize_project(goal)
        click.echo(f"Initialized Conductor project in {ctx.manager.conductor_path}")
    except Exception as e:
        handle_error(e)


@main.command()
@click.argument("description")
@click.pass_obj
def new_track(ctx, description) -> None:
    """Initialize a new track"""
    try:
        track_id = ctx.manager.create_track(description)
        click.echo(f"Created track {track_id}: {description}")
    except Exception as e:
        handle_error(e)


@main.command()
@click.pass_obj
def status(ctx) -> None:
    """Display project status"""
    try:
        report = ctx.manager.get_status_report()
        click.echo(report)
    except FileNotFoundError:
        click.echo("Error: Project not set up. Run 'setup' first.", err=True)
        sys.exit(1)
    except Exception as e:
        handle_error(e)


@main.command()
@click.argument("track_description", required=False)
@click.pass_obj
def implement(ctx, track_description) -> None:
    """Implement the current track"""
    try:
        track_id, description, _status_char = ctx.runner.get_track_to_implement(track_description)
        click.echo(f"Selecting track: {description} ({track_id})")

        # Update status to IN_PROGRESS (~)
        ctx.runner.update_track_status(track_id, "~")
        click.echo("Track status updated to IN_PROGRESS.")

        # Load context for the AI
        plan_path = ctx.manager.conductor_path / "tracks" / track_id / "plan.md"
        spec_path = ctx.manager.conductor_path / "tracks" / track_id / "spec.md"
        workflow_path = ctx.manager.conductor_path / "workflow.md"

        click.echo("\nTrack Context Loaded:")
        click.echo(f"- Plan: {plan_path}")
        click.echo(f"- Spec: {spec_path}")
        click.echo(f"- Workflow: {workflow_path}")

        click.echo("\nReady to implement. Follow the workflow in workflow.md.")

    except Exception as e:
        handle_error(e)


@main.command()
@click.argument("track_id")
@click.argument("task_description")
@click.pass_obj
def revert(ctx, track_id, task_description) -> None:
    """Revert a specific task to pending status"""
    try:
        ctx.runner.revert_task(track_id, task_description)
        click.echo(f"Task '{task_description}' in track {track_id} has been reset to pending.")
    except Exception as e:
        handle_error(e)


@main.command()
@click.argument("track_id")
@click.pass_obj
def archive(ctx, track_id) -> None:
    """Archive a completed track"""
    try:
        ctx.runner.archive_track(track_id)
        click.echo(f"Track {track_id} archived successfully.")
    except Exception as e:
        handle_error(e)


if __name__ == "__main__":
    main()  # pragma: no cover
