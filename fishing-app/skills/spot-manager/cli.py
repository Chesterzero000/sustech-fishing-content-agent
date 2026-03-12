"""CLI commands for spot-manager skill"""
import click
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from cli.utils import print_response, handle_error
from skills.spot_manager.service import SpotManagerService
from cli.main import spots


@spots.command()
@click.option('--lat', type=float, required=True, help='Latitude')
@click.option('--lon', type=float, required=True, help='Longitude')
@click.option('--radius', type=float, default=10.0, help='Search radius in km (default: 10)')
@click.option('--fish', help='Filter by fish species')
@click.option('--format', type=click.Choice(['markdown', 'json', 'pretty-json']), default='markdown')
def nearby(lat, lon, radius, fish, format):
    """Find nearby fishing spots
    
    Example:
        fishing-cli spots nearby --lat 22.5 --lon 114.0 --radius 10
        fishing-cli spots nearby --lat 22.5 --lon 114.0 --fish "鲫鱼"
    """
    try:
        service = SpotManagerService()
        response = service.search_nearby(
            latitude=lat,
            longitude=lon,
            radius=radius,
            fish_species=fish
        )
        print_response(response, format=format)
    
    except Exception as e:
        handle_error(e)


@spots.command()
@click.option('--fish', required=True, help='Fish species to search for')
@click.option('--city', help='Filter by city')
@click.option('--format', type=click.Choice(['markdown', 'json', 'pretty-json']), default='markdown')
def search(fish, city, format):
    """Search spots by fish species
    
    Example:
        fishing-cli spots search --fish "鲫鱼"
        fishing-cli spots search --fish "鲤鱼" --city "深圳"
    """
    try:
        service = SpotManagerService()
        response = service.search_by_fish(fish_species=fish, city=city)
        print_response(response, format=format)
    
    except Exception as e:
        handle_error(e)


@spots.command()
@click.option('--id', 'spot_id', type=int, required=True, help='Spot ID')
@click.option('--format', type=click.Choice(['markdown', 'json', 'pretty-json']), default='markdown')
def details(spot_id, format):
    """Get spot details
    
    Example:
        fishing-cli spots details --id 123
    """
    try:
        service = SpotManagerService()
        response = service.get_spot_details(spot_id)
        print_response(response, format=format)
    
    except Exception as e:
        handle_error(e)


@spots.command()
@click.option('--limit', type=int, default=20, help='Number of spots to return')
@click.option('--offset', type=int, default=0, help='Offset for pagination')
@click.option('--format', type=click.Choice(['markdown', 'json', 'pretty-json']), default='markdown')
def list(limit, offset, format):
    """List all fishing spots
    
    Example:
        fishing-cli spots list --limit 20
        fishing-cli spots list --limit 10 --offset 20
    """
    try:
        service = SpotManagerService()
        response = service.list_spots(limit=limit, offset=offset)
        print_response(response, format=format)
    
    except Exception as e:
        handle_error(e)
