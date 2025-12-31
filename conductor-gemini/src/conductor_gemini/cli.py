import click
import sys
import os
from pathlib import Path
from conductor_core.project_manager import ProjectManager
from conductor_core.task_runner import TaskRunner

class Context:
    def __init__(self, base_path=None):
        self.base_path = base_path or os.getcwd()
        self.manager = ProjectManager(self.base_path)
        self.runner = TaskRunner(self.manager)

@click.group()
@click.option('--base-path', type=click.Path(exists=True), help='Base path for the project')
@click.pass_context
def main(ctx, base_path):
    """Conductor Gemini CLI Adapter"""
    ctx.obj = Context(base_path)

@main.command()
@click.option('--goal', required=True, help='Initial project goal')
@click.pass_obj
def setup(ctx, goal):
    """Initialize a new Conductor project"""
    try:
        ctx.manager.initialize_project(goal)
        click.echo(f"Initialized Conductor project in {ctx.manager.conductor_path}")
    except Exception as e:
        click.echo(f"Error during setup: {e}", err=True)
        sys.exit(1)

@main.command()
@click.argument('description')
@click.pass_obj
def new_track(ctx, description):
    """Initialize a new track"""
    try:
        track_id = ctx.manager.create_track(description)
        click.echo(f"Created track {track_id}: {description}")
    except Exception as e:
        click.echo(f"Error creating track: {e}", err=True)
        sys.exit(1)

@main.command()
@click.pass_obj
def status(ctx):
    """Display project status"""
    try:
        report = ctx.manager.get_status_report()
        click.echo(report)
    except FileNotFoundError:
        click.echo("Error: Project not set up.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error getting status: {e}", err=True)
        sys.exit(1)

@main.command()
@click.argument('track_description', required=False)
@click.pass_obj
def implement(ctx, track_description):
    """Implement the current track"""
    try:
        track_id, description, status_char = ctx.runner.get_track_to_implement(track_description)
        click.echo(f"Selecting track: {description} ({track_id})")
        
        # Update status to IN_PROGRESS (~)
        ctx.runner.update_track_status(track_id, "~")
        click.echo(f"Track status updated to IN_PROGRESS.")
        
        # Load context for the AI
        plan_path = ctx.manager.conductor_path / "tracks" / track_id / "plan.md"
        spec_path = ctx.manager.conductor_path / "tracks" / track_id / "spec.md"
        workflow_path = ctx.manager.conductor_path / "workflow.md"
        
        click.echo(f"\nTrack Context Loaded:")
        click.echo(f"- Plan: {plan_path}")
        click.echo(f"- Spec: {spec_path}")
        click.echo(f"- Workflow: {workflow_path}")
        
        click.echo("\nReady to implement. Follow the workflow in workflow.md.")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@main.command()
@click.pass_obj
def revert(ctx):
    """Revert a task or phase (Not yet implemented)"""
    click.echo("Revert command is not yet fully implemented in the CLI adapter.")

@main.command()
@click.argument('track_id')
@click.pass_obj
def archive(ctx, track_id):
    """Archive a completed track"""
    try:
        ctx.runner.archive_track(track_id)
        click.echo(f"Track {track_id} archived successfully.")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main()