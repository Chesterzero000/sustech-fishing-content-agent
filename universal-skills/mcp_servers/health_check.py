#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP 服务器健康检查脚本
检查所有 MCP 服务器的健康状态
"""

import asyncio
import httpx
from typing import Dict, List
from datetime import datetime

# MCP 服务器配置
MCP_SERVERS = [
    {"name": "fishing-coach", "port": 8001},
    {"name": "weather-advisor", "port": 8002},
    {"name": "spot-manager", "port": 8003},
    {"name": "fish-identifier", "port": 8004},
    {"name": "catch-tracker", "port": 8005},
    {"name": "social-manager", "port": 8006},
    {"name": "drone-controller", "port": 8007},
    {"name": "fishing-report-manager", "port": 8008},
    {"name": "angler-radar", "port": 8009},
    {"name": "user-manager", "port": 8010},
    {"name": "persona-manager", "port": 8011},
    {"name": "feedback-manager", "port": 8012},
]


async def check_server(server: Dict) -> Dict:
    """检查单个服务器"""
    name = server["name"]
    port = server["port"]
    url = f"http://localhost:{port}/health"
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            start_time = datetime.now()
            response = await client.get(url)
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return {
                "name": name,
                "port": port,
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time": round(response_time, 2),
                "error": None
            }
    except Exception as e:
        return {
            "name": name,
            "port": port,
            "status": "down",
            "response_time": None,
            "error": str(e)
        }


async def check_all_servers() -> List[Dict]:
    """检查所有服务器"""
    tasks = [check_server(server) for server in MCP_SERVERS]
    return await asyncio.gather(*tasks)


def print_report(results: List[Dict]):
    """打印健康检查报告"""
    print("\n" + "=" * 80)
    print(f"MCP 服务器健康检查报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    healthy_count = sum(1 for r in results if r["status"] == "healthy")
    total_count = len(results)
    
    print(f"\n总览: {healthy_count}/{total_count} 服务器健康\n")
    
    # 打印详细信息
    print(f"{'服务名称':<30} {'端口':<8} {'状态':<12} {'响应时间':<12}")
    print("-" * 80)
    
    for result in results:
        name = result["name"]
        port = result["port"]
        status = result["status"]
        response_time = f"{result['response_time']}ms" if result['response_time'] else "N/A"
        
        # 状态图标
        status_icon = "✅" if status == "healthy" else "❌"
        
        print(f"{name:<30} {port:<8} {status_icon} {status:<10} {response_time:<12}")
        
        if result["error"]:
            print(f"  错误: {result['error']}")
    
    print("\n" + "=" * 80)
    
    # 返回状态码
    return 0 if healthy_count == total_count else 1


async def main():
    """主函数"""
    results = await check_all_servers()
    exit_code = print_report(results)
    return exit_code


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
