# -*- coding: utf-8 -*-
"""User Manager MCP Server"""
import os
import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent
from .service import UserManagerService

MCP_PORT = int(os.getenv("MCP_PORT_USER_MANAGER", "8010"))
service = UserManagerService()
app = Server("user-manager")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="wx_login", description="微信登录", inputSchema={"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}),
        Tool(name="get_user_profile", description="获取用户资料", inputSchema={"type": "object", "properties": {"user_id": {"type": "string"}}, "required": ["user_id"]})
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "wx_login":
        result = await service.wx_login(arguments["code"])
        return [TextContent(type="text", text=str(result))]
    elif name == "get_user_profile":
        result = await service.get_profile(arguments["user_id"])
        return [TextContent(type="text", text=str(result))]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
