# -*- coding: utf-8 -*-
"""
Fishing Report Manager MCP Server - 渔获报告管理 MCP 服务器
"""

import os
import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent
from .service import FishingReportService

# MCP 服务器配置
MCP_PORT = int(os.getenv("MCP_PORT_FISHING_REPORT", "8008"))
service = FishingReportService()

# 创建 MCP 服务器
app = Server("fishing-report-manager")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="create_fishing_report",
            description="创建渔获报告",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "spot_id": {"type": "string"},
                    "fish_species": {"type": "string"},
                    "weight": {"type": "number"},
                    "length": {"type": "number"}
                },
                "required": ["user_id", "spot_id", "fish_species", "weight", "length"]
            }
        ),
        Tool(
            name="get_fishing_reports",
            description="获取渔获报告列表",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "limit": {"type": "number", "default": 20}
                }
            }
        ),
        Tool(
            name="get_nearby_reports",
            description="获取附近的渔获报告",
            inputSchema={
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                    "radius": {"type": "number", "default": 10.0}
                },
                "required": ["latitude", "longitude"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """调用工具"""
    if name == "create_fishing_report":
        result = await service.create_report(**arguments)
        return [TextContent(type="text", text=str(result))]
    
    elif name == "get_fishing_reports":
        reports = await service.get_reports(**arguments)
        return [TextContent(type="text", text=str(reports))]
    
    elif name == "get_nearby_reports":
        reports = await service.get_nearby_reports(**arguments)
        return [TextContent(type="text", text=str(reports))]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """启动 MCP 服务器"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
