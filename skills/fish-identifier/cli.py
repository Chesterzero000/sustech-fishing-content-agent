"""CLI commands for fish-identifier skill"""
import click
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from cli.utils import print_response, handle_error
from skills.fish_identifier.service import FishIdentifierService
from cli.main import fish


@fish.command()
@click.argument('image_path', type=click.Path(exists=True))
@click.option('--format', type=click.Choice(['markdown', 'json', 'pretty-json']), default='markdown')
def recognize(image_path, format):
    """Recognize fish species from image
    
    Example:
        fishing-cli fish recognize ./my_catch.jpg
        fishing-cli fish recognize ./photo.jpg --format json
    """
    try:
        service = FishIdentifierService()
        response = service.recognize(image_path=image_path)
        print_response(response, format=format)
    
    except Exception as e:
        handle_error(e)


@fish.command()
@click.argument('fish_name')
@click.option('--format', type=click.Choice(['markdown', 'json', 'pretty-json']), default='markdown')
def tips(fish_name, format):
    """Get fishing tips for a species
    
    Example:
        fishing-cli fish tips "鲫鱼"
        fishing-cli fish tips "草鱼" --format json
    """
    try:
        service = FishIdentifierService()
        response = service.get_tips(fish_name)
        print_response(response, format=format)
    
    except Exception as e:
        handle_error(e)
