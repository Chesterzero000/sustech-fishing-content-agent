"""CLI commands for weather-advisor skill"""
import click
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from cli.utils import print_response, handle_error
from skills.weather_advisor.service import WeatherAdvisorService
from cli.main import weather


@weather.command()
@click.option('--city', help='City name (e.g., 深圳)')
@click.option('--lat', type=float, help='Latitude')
@click.option('--lon', type=float, help='Longitude')
@click.option('--format', type=click.Choice(['markdown', 'json', 'pretty-json']), default='markdown')
def current(city, lat, lon, format):
    """Get current weather and fishing conditions
    
    Example:
        fishing-cli weather current --city "深圳"
        fishing-cli weather current --lat 22.5 --lon 114.0
    """
    if not city and not (lat and lon):
        click.echo("Error: Must provide either --city or both --lat and --lon", err=True)
        return
    
    try:
        service = WeatherAdvisorService()
        response = service.get_current(city=city, latitude=lat, longitude=lon)
        print_response(response, format=format)
    
    except Exception as e:
        handle_error(e)


@weather.command()
@click.option('--city', help='City name')
@click.option('--lat', type=float, help='Latitude')
@click.option('--lon', type=float, help='Longitude')
@click.option('--days', type=int, default=7, help='Forecast days (1-7)')
@click.option('--format', type=click.Choice(['markdown', 'json', 'pretty-json']), default='markdown')
def forecast(city, lat, lon, days, format):
    """Get weather forecast
    
    Example:
        fishing-cli weather forecast --city "深圳" --days 7
        fishing-cli weather forecast --lat 22.5 --lon 114.0 --days 3
    """
    if not city and not (lat and lon):
        click.echo("Error: Must provide either --city or both --lat and --lon", err=True)
        return
    
    try:
        service = WeatherAdvisorService()
        response = service.get_forecast(city=city, latitude=lat, longitude=lon, days=days)
        print_response(response, format=format)
    
    except Exception as e:
        handle_error(e)


@weather.command('fishing-index')
@click.option('--city', help='City name')
@click.option('--lat', type=float, help='Latitude')
@click.option('--lon', type=float, help='Longitude')
@click.option('--format', type=click.Choice(['markdown', 'json', 'pretty-json']), default='markdown')
def fishing_index(city, lat, lon, format):
    """Calculate fishing suitability index
    
    Example:
        fishing-cli weather fishing-index --city "深圳"
        fishing-cli weather fishing-index --lat 22.5 --lon 114.0
    """
    if not city and not (lat and lon):
        click.echo("Error: Must provide either --city or both --lat and --lon", err=True)
        return
    
    try:
        service = WeatherAdvisorService()
        response = service.get_current(city=city, latitude=lat, longitude=lon)
        print_response(response, format=format)
    
    except Exception as e:
        handle_error(e)
