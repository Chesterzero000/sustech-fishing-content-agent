"""CLI utilities and helpers"""
import click
from typing import Any, Dict
from shared import ResponseFormatter


def print_response(response: Dict[str, Any], format: str = "markdown"):
    """Print response in specified format
    
    Args:
        response: Response dictionary from skill
        format: Output format ('json', 'markdown', 'pretty-json')
    """
    if format == "json":
        click.echo(ResponseFormatter.to_json(response))
    elif format == "pretty-json":
        click.echo(ResponseFormatter.to_json(response, pretty=True))
    else:  # markdown
        click.echo(ResponseFormatter.to_markdown(response))


def handle_error(error: Exception, verbose: bool = False):
    """Handle and display errors consistently
    
    Args:
        error: Exception that occurred
        verbose: If True, show full traceback
    """
    error_response = ResponseFormatter.error(
        error=str(error),
        code=type(error).__name__,
        details={"verbose": str(error)} if verbose else None
    )
    
    click.echo(ResponseFormatter.to_markdown(error_response), err=True)
    
    if verbose:
        import traceback
        click.echo("\n=== Traceback ===", err=True)
        click.echo(traceback.format_exc(), err=True)
