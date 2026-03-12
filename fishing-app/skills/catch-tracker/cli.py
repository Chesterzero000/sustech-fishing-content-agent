"""Catch Tracker CLI Commands"""
import click
from .service import CatchTrackerService
from cli.utils import format_output, handle_error


@click.group(name='catch')
def catch_group():
    """Catch record management commands"""
    pass


@catch_group.command('log')
@click.option('--user-id', required=True, help='User ID')
@click.option('--species', required=True, help='Fish species name')
@click.option('--weight', required=True, type=float, help='Fish weight in kg')
@click.option('--length', type=float, help='Fish length in cm')
@click.option('--spot-id', type=int, help='Fishing spot ID')
@click.option('--image', help='Path to catch photo')
@click.option('--notes', help='Additional notes')
@click.option('--lat', type=float, help='GPS latitude')
@click.option('--lon', type=float, help='GPS longitude')
def log_catch(user_id, species, weight, length, spot_id, image, notes, lat, lon):
    """Log a new catch record"""
    try:
        service = CatchTrackerService()
        result = service.log_catch(
            user_id=user_id,
            fish_species=species,
            weight=weight,
            length=length,
            spot_id=spot_id,
            image_path=image,
            notes=notes,
            latitude=lat,
            longitude=lon
        )
        format_output(result)
    except Exception as e:
        handle_error(e)


@catch_group.command('list')
@click.option('--user-id', required=True, help='User ID')
@click.option('--limit', default=20, type=int, help='Number of records to return')
@click.option('--offset', default=0, type=int, help='Offset for pagination')
def list_catches(user_id, limit, offset):
    """List catch history for a user"""
    try:
        service = CatchTrackerService()
        result = service.get_catches(
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        format_output(result)
    except Exception as e:
        handle_error(e)


@catch_group.command('stats')
@click.option('--user-id', required=True, help='User ID')
def get_stats(user_id):
    """Get catch statistics for a user"""
    try:
        service = CatchTrackerService()
        result = service.get_statistics(user_id=user_id)
        format_output(result)
    except Exception as e:
        handle_error(e)


@catch_group.command('delete')
@click.option('--catch-id', required=True, type=int, help='Catch record ID')
@click.option('--user-id', help='User ID for ownership verification')
def delete_catch(catch_id, user_id):
    """Delete a catch record"""
    try:
        service = CatchTrackerService()
        result = service.delete_catch(
            catch_id=catch_id,
            user_id=user_id
        )
        format_output(result)
    except Exception as e:
        handle_error(e)
