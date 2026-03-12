"""CLI framework for 千鱼千寻 OpenClaw skills"""
import click
from typing import Optional


@click.group()
@click.version_option(version="2.0.0", prog_name="fishing-cli")
def fishing_cli():
    """千鱼千寻 CLI - OpenClaw Integration
    
    Command-line interface for all fishing mini-program skills.
    Each skill provides its own subcommands.
    """
    pass


# Import skill CLI commands dynamically
import sys
import os
import importlib.util

# Add skills directory to path
skills_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'skills')

def load_skill_cli(skill_name):
    """Dynamically load skill CLI module"""
    skill_path = os.path.join(skills_dir, skill_name, 'cli.py')
    if not os.path.exists(skill_path):
        return None
    
    spec = importlib.util.spec_from_file_location(f"{skill_name}.cli", skill_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load skill command groups
try:
    coach_module = load_skill_cli('fishing-coach')
    fish_module = load_skill_cli('fish-identifier')
    weather_module = load_skill_cli('weather-advisor')
    spots_module = load_skill_cli('spot-manager')
    catch_module = load_skill_cli('catch-tracker')
    social_module = load_skill_cli('social-manager')
    drone_module = load_skill_cli('drone-controller')
    
    # Register skill command groups
    if coach_module:
        fishing_cli.add_command(coach_module.coach_group, name='coach')
    if fish_module:
        fishing_cli.add_command(fish_module.fish_group, name='fish')
    if weather_module:
        fishing_cli.add_command(weather_module.weather_group, name='weather')
    if spots_module:
        fishing_cli.add_command(spots_module.spots_group, name='spots')
    if catch_module:
        fishing_cli.add_command(catch_module.catch_group, name='catch')
    if social_module:
        fishing_cli.add_command(social_module.social_group, name='social')
    if drone_module:
        fishing_cli.add_command(drone_module.drone_group, name='drone')
except Exception as e:
    # Silently fail if skills can't be loaded
    pass



# Utility commands
@fishing_cli.command()
def config():
    """Show current configuration"""
    from shared import config as cfg
    
    click.echo("=== Configuration ===")
    all_config = cfg.get_all()
    
    # Mask sensitive values
    sensitive_keys = ['password', 'secret', 'key', 'token']
    for key, value in sorted(all_config.items()):
        if any(s in key.lower() for s in sensitive_keys) and value:
            display_value = "***" + value[-4:] if len(value) > 4 else "***"
        else:
            display_value = value
        click.echo(f"{key}: {display_value}")


@fishing_cli.command()
def skills():
    """List available skills"""
    click.echo("=== Available Skills ===\n")
    
    skills_list = [
        ("fishing-coach", "AI fishing coach with RAG and knowledge graph"),
        ("fish-identifier", "Fish species recognition from images"),
        ("weather-advisor", "Weather forecasts and fishing conditions"),
        ("spot-manager", "Fishing spot search and management"),
        ("catch-tracker", "Catch record logging and statistics"),
        ("social-manager", "Social posts and community features"),
        ("drone-controller", "Drone/boat telemetry tracking")
    ]
    
    for name, desc in skills_list:
        click.echo(f"  {name:20s} - {desc}")
    
    click.echo(f"\nTotal: {len(skills_list)} skills")
    click.echo("\nUse 'fishing-cli <skill> --help' for skill-specific commands")


if __name__ == "__main__":
    fishing_cli()
