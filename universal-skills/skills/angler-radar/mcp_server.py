# -*- coding: utf-8 -*-
"""Angler Radar MCP Server"""
import os
import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent
from .service import AnglerRadarService

MCP_PORT = int(os.getenv("MCP_PORT_ANGLER_RADAR", "8009"))
service = AnglerRadarService()
app = Server("angler-radar")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="update_angler_location",
            description="更新钓友位置",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"}
                },
                "required": ["user_id", "latitude", "longitude"]
            }
        ),
        Tool(
            name="get_nearby_anglers",
            description="获取附近钓友",
            inputSchema={
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                    "radius": {"type": "number", "default": 5.0}
                },
                "required": ["latitude", "longitude"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "update_angler_location":
        result = await service.update_location(**arguments)
        return [TextContent(type="text", text=str(result))]
    elif name == "get_nearby_anglers":
        result = await service.get_nearby_anglers(**arguments)
        return [TextContent(type="text", text=str(result))]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
