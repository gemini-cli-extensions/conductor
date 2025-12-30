import click
import sys
import os
from pathlib import Path
from conductor_core.project_manager import ProjectManager

class Context:
    def __init__(self, base_path=None):
        self.base_path = base_path or os.getcwd()
        self.manager = ProjectManager(self.base_path)

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
    tracks_file = ctx.manager.conductor_path / "tracks.md"
    if not tracks_file.exists():
        click.echo("Error: Project not set up.", err=True)
        sys.exit(1)
    click.echo(tracks_file.read_text())

@main.command()
@click.pass_obj
def implement(ctx):
    """Implement the current track"""
    click.echo("Implementing current track...")

if __name__ == '__main__':
    main()