# -*- coding: utf-8 -*-
"""
Report Agent - 数据报告生成器
生成每日/每周数据报告
"""

import os
import httpx
from datetime import datetime, timedelta
from typing import Dict, Any, List

API_BASE_URL = os.getenv("API_BASE_URL", "https://qianyu.iepose.cn")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "")


class ReportAgent:
    """报告生成代理"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.api_key = INTERNAL_API_KEY
        self.headers = {
            "X-Internal-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def generate_daily_report(self, date: str = None) -> str:
        """生成每日报告"""
        target_date = date or (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # 获取统计数据
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/internal/stats/daily",
                json={"date": target_date},
                headers=self.headers
            )
            stats = response.json()["data"]
        
        # 生成 Markdown 报告
        report = f"""# 千鱼千寻每日数据报告

**日期**: {target_date}
**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 📊 用户活跃

- 新增用户: {stats['user_activity']['new_users']} 人
- 活跃用户: {stats['user_activity']['active_users']} 人
- 留存率: {stats['user_activity']['retention_rate']:.1%}

## 📝 内容统计

- 新增帖子: {stats['content_stats']['new_posts']} 条
- 新增评论: {stats['content_stats']['new_comments']} 条
- 新增点赞: {stats['content_stats']['new_likes']} 次

## 🎣 渔获数据

- 新增记录: {stats['catch_records']['new_records']} 条
- 总重量: {stats['catch_records']['total_weight']:.1f} kg
- 热门鱼种: {', '.join(stats['catch_records']['popular_species']) or '暂无'}

## 🔧 系统健康

- API 调用: {stats['system_health']['api_calls']} 次
- 错误率: {stats['system_health']['error_rate']:.2%}
- 平均响应时间: {stats['system_health']['avg_response_time']:.0f} ms

---

*本报告由 OpenClaw 自动生成*
"""
        return report
    
    async def generate_weekly_report(self, start_date: str = None, end_date: str = None) -> str:
        """生成每周报告"""
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        # 获取统计数据
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/internal/stats/weekly",
                json={"start_date": start_date, "end_date": end_date},
                headers=self.headers
            )
            stats = response.json()["data"]
        
        # 生成 Markdown 报告
        report = f"""# 千鱼千寻每周数据摘要

**周期**: {start_date} ~ {end_date}
**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 📈 用户增长

- 新增用户: {stats['user_growth']['new_users']} 人
- 增长率: {stats['user_growth']['growth_rate']:.1%}

## 📊 内容趋势

- 参与率: {stats['content_trends']['engagement_rate']:.1%}

## 🏆 热门钓点

{self._format_list(stats['popular_spots'])}

## 🎣 精彩渔获

{self._format_list(stats['top_catches'])}

---

*本报告由 OpenClaw 自动生成*
"""
        return report
    
    def _format_list(self, items: List[Dict]) -> str:
        """格式化列表"""
        if not items:
            return "暂无数据"
        return "\n".join([f"- {item}" for item in items])
