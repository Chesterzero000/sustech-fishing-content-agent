# -*- coding: utf-8 -*-
"""
任务调度器 - 执行定时任务
"""

import asyncio
from datetime import datetime
from agents.report_agent import ReportAgent
from integrations.feishu_client import FeishuClient


async def run_daily_report():
    """执行每日报告任务"""
    print(f"[{datetime.now()}] 开始生成每日报告...")
    
    try:
        # 生成报告
        agent = ReportAgent()
        report = await agent.generate_daily_report()
        
        # 发送到飞书
        feishu = FeishuClient()
        await feishu.send_markdown("千鱼千寻每日数据报告", report)
        
        print(f"[{datetime.now()}] ✅ 每日报告已发送")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ 每日报告失败: {e}")


async def run_weekly_report():
    """执行每周报告任务"""
    print(f"[{datetime.now()}] 开始生成每周报告...")
    
    try:
        # 生成报告
        agent = ReportAgent()
        report = await agent.generate_weekly_report()
        
        # 发送到飞书
        feishu = FeishuClient()
        await feishu.send_markdown("千鱼千寻每周数据摘要", report)
        
        print(f"[{datetime.now()}] ✅ 每周报告已发送")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ 每周报告失败: {e}")


if __name__ == "__main__":
    # 测试运行
    asyncio.run(run_daily_report())
