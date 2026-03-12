import json
import click

from .service import DroneControllerService


service = DroneControllerService()


@click.group(name="drone")
def drone_group():
    """Drone related commands"""
    pass


@drone_group.command("telemetry")
@click.option("--drone-id", required=True, help="Drone identifier")
def telemetry(drone_id):
    """Fetch real-time telemetry for a drone."""
    data = service.get_telemetry(drone_id)
    click.echo(json.dumps(data, indent=2))


@drone_group.command("trajectory")
@click.option("--drone-id", required=True, help="Drone identifier")
@click.option("--start-time", required=True, help="Start time (ISO 8601)")
@click.option("--end-time", required=True, help="End time (ISO 8601)")
def trajectory(drone_id, start_time, end_time):
    """Fetch historical trajectory for a drone."""
    data = service.get_trajectory(drone_id, start_time, end_time)
    click.echo(json.dumps(data, indent=2))


@drone_group.command("status")
@click.option("--drone-id", required=True, help="Drone identifier")
def status(drone_id):
    """Fetch current status of a drone."""
    data = service.get_status(drone_id)
    click.echo(json.dumps(data, indent=2))


@drone_group.command("send")
@click.option("--drone-id", required=True, help="Drone identifier")
@click.argument("command")
@click.option("--params", default="{}", help="JSON string of parameters")
def send(drone_id, command, params):
    """Send a control command to the drone."""
    try:
        parsed = json.loads(params)
    except Exception:
        parsed = {}
    data = service.send_command(drone_id, command, parsed)
    click.echo(json.dumps(data, indent=2))


if __name__ == "__main__":
    drone_group()
