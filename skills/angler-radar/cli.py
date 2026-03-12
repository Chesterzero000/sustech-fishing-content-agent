# -*- coding: utf-8 -*-
"""Angler Radar CLI"""
import click
import asyncio
from .service import AnglerRadarService

service = AnglerRadarService()

@click.group()
def cli():
    """钓友雷达 CLI"""
    pass

@cli.command()
@click.option("--user-id", required=True)
@click.option("--latitude", type=float, required=True)
@click.option("--longitude", type=float, required=True)
def update_location(user_id, latitude, longitude):
    """更新位置"""
    async def _update():
        result = await service.update_location(user_id, latitude, longitude)
        click.echo(f"✅ 位置已更新: {result}")
    asyncio.run(_update())

@cli.command()
@click.option("--latitude", type=float, required=True)
@click.option("--longitude", type=float, required=True)
@click.option("--radius", type=float, default=5.0)
def nearby(latitude, longitude, radius):
    """查询附近钓友"""
    async def _nearby():
        anglers = await service.get_nearby_anglers(latitude, longitude, radius)
        click.echo(f"📍 附近找到 {len(anglers)} 位钓友")
    asyncio.run(_nearby())

if __name__ == "__main__":
    cli()
