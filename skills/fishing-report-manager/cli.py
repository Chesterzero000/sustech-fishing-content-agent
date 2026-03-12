# -*- coding: utf-8 -*-
"""
Fishing Report Manager CLI - 渔获报告管理命令行工具
"""

import click
import asyncio
from .service import FishingReportService

service = FishingReportService()


@click.group()
def cli():
    """渔获报告管理 CLI"""
    pass


@cli.command()
@click.option("--user-id", required=True, help="用户 ID")
@click.option("--spot-id", required=True, help="钓点 ID")
@click.option("--fish-species", required=True, help="鱼种")
@click.option("--weight", type=float, required=True, help="重量 (kg)")
@click.option("--length", type=float, required=True, help="长度 (cm)")
def create(user_id, spot_id, fish_species, weight, length):
    """创建渔获报告"""
    async def _create():
        result = await service.create_report(
            user_id=user_id,
            spot_id=spot_id,
            fish_species=fish_species,
            weight=weight,
            length=length
        )
        click.echo(f"✅ 报告创建成功: {result}")
    
    asyncio.run(_create())


@cli.command()
@click.option("--user-id", help="用户 ID")
@click.option("--limit", default=20, help="返回数量")
def list(user_id, limit):
    """查询报告列表"""
    async def _list():
        reports = await service.get_reports(user_id=user_id, limit=limit)
        click.echo(f"📋 找到 {len(reports)} 条报告")
        for report in reports:
            click.echo(f"  - {report}")
    
    asyncio.run(_list())


@cli.command()
@click.option("--latitude", type=float, required=True, help="纬度")
@click.option("--longitude", type=float, required=True, help="经度")
@click.option("--radius", type=float, default=10.0, help="半径 (km)")
def nearby(latitude, longitude, radius):
    """查询附近的报告"""
    async def _nearby():
        reports = await service.get_nearby_reports(
            latitude=latitude,
            longitude=longitude,
            radius=radius
        )
        click.echo(f"📍 附近找到 {len(reports)} 条报告")
        for report in reports:
            click.echo(f"  - {report}")
    
    asyncio.run(_nearby())


if __name__ == "__main__":
    cli()
