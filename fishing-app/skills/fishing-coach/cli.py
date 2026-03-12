"""CLI commands for fishing-coach skill"""
import click
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from cli.utils import print_response, handle_error
from skills.fishing_coach.service import FishingCoachService


# Get the coach group from main CLI
from cli.main import coach


@coach.command()
@click.argument('question')
@click.option('--user-id', help='User ID for personalization')
@click.option('--latitude', type=float, help='User latitude')
@click.option('--longitude', type=float, help='User longitude')
@click.option('--voice-style', help='Voice style (friendly/professional/humorous)')
@click.option('--format', type=click.Choice(['markdown', 'json', 'pretty-json']), default='markdown')
def ask(question, user_id, latitude, longitude, voice_style, format):
    """Ask the fishing coach a question
    
    Example:
        fishing-cli coach ask "鲫鱼怎么钓?"
        fishing-cli coach ask "今天适合钓鱼吗?" --latitude 22.5 --longitude 114.0
    """
    try:
        service = FishingCoachService(voice_style=voice_style)
        response = service.ask(
            question=question,
            user_id=user_id,
            latitude=latitude,
            longitude=longitude
        )
        print_response(response, format=format)
    
    except Exception as e:
        handle_error(e)


@coach.command()
@click.argument('question')
@click.option('--user-id', required=True, help='User ID (required for chat)')
@click.option('--voice-style', help='Voice style')
@click.option('--format', type=click.Choice(['markdown', 'json', 'pretty-json']), default='markdown')
def chat(question, user_id, voice_style, format):
    """Multi-turn chat with user context
    
    Example:
        fishing-cli coach chat "鲫鱼怎么钓?" --user-id user123
    """
    try:
        service = FishingCoachService(voice_style=voice_style)
        response = service.chat(question=question, user_id=user_id)
        print_response(response, format=format)
    
    except Exception as e:
        handle_error(e)


@coach.command()
@click.option('--user-id', required=True, help='User ID')
@click.option('--format', type=click.Choice(['markdown', 'json', 'pretty-json']), default='markdown')
def memory(user_id, format):
    """Get user memory and preferences
    
    Example:
        fishing-cli coach memory --user-id user123
    """
    try:
        service = FishingCoachService()
        response = service.get_user_memory(user_id)
        print_response(response, format=format)
    
    except Exception as e:
        handle_error(e)
