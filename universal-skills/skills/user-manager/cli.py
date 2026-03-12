# -*- coding: utf-8 -*-
"""User Manager CLI"""
import click
import asyncio
from .service import UserManagerService

service = UserManagerService()

@click.group()
def cli():
    """用户管理 CLI"""
    pass

@cli.command()
@click.option("--code", required=True)
def login(code):
    """微信登录"""
    async def _login():
        result = await service.wx_login(code)
        click.echo(f"✅ 登录成功: {result}")
    asyncio.run(_login())

@cli.command()
@click.option("--user-id", required=True)
def profile(user_id):
    """获取用户资料"""
    async def _profile():
        result = await service.get_profile(user_id)
        click.echo(f"👤 用户资料: {result}")
    asyncio.run(_profile())

if __name__ == "__main__":
    cli()
