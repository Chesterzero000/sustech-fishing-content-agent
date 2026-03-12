"""Report Agent - 数据报告生成"""
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import requests

logger = logging.getLogger(__name__)


class ReportAgent:
    """报告生成代理
    
    负责生成每日/每周数据报告并推送到飞书
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize report agent
        
        Args:
            config: OpenClaw configuration
        """
        self.config = config
        self.api_base_url = config.get('api', {}).get('base_url')
        self.internal_token = config.get('api', {}).get('internal_token')
        self.feishu_webhook = config.get('feishu', {}).get('webhooks', {}).get('reports')
    
    def generate_daily_report(self, date: str = None) -> Dict[str, Any]:
        """Generate daily report
        
        Args:
            date: Report date (YYYY-MM-DD), defaults to yesterday
            
        Returns:
            Report data
        """
        if date is None:
            date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        logger.info(f"Generating daily report for {date}")
        
        try:
            # Fetch data from internal API
            stats = self._fetch_daily_stats(date)
            
            # Generate report
            report = {
                'type': 'daily',
                'date': date,
                'generated_at': datetime.now().isoformat(),
                'data': stats
            }
            
            # Format report message
            message = self._format_daily_report(report)
            
            # Send to Feishu
            if self.feishu_webhook:
                self._send_to_feishu(message)
            
            # Save to database
            self._save_report(report)
            
            logger.info(f"Daily report generated successfully for {date}")
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate daily report: {e}", exc_info=True)
            raise
    
    def generate_weekly_report(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Generate weekly report
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            Report data
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        logger.info(f"Generating weekly report for {start_date} to {end_date}")
        
        try:
            # Fetch data from internal API
            stats = self._fetch_weekly_stats(start_date, end_date)
            
            # Generate report
            report = {
                'type': 'weekly',
                'start_date': start_date,
                'end_date': end_date,
                'generated_at': datetime.now().isoformat(),
                'data': stats
            }
            
            # Format report message
            message = self._format_weekly_report(report)
            
            # Send to Feishu
            if self.feishu_webhook:
                self._send_to_feishu(message)
            
            # Save to database
            self._save_report(report)
            
            logger.info(f"Weekly report generated successfully")
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate weekly report: {e}", exc_info=True)
            raise
    
    def _fetch_daily_stats(self, date: str) -> Dict[str, Any]:
        """Fetch daily statistics from API
        
        Args:
            date: Report date
            
        Returns:
            Statistics data
        """
        url = f"{self.api_base_url}/internal/stats/daily"
        headers = {
            'X-Internal-API-Key': self.internal_token,
            'Content-Type': 'application/json'
        }
        data = {'date': date}
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result.get('data', {})
    
    def _fetch_weekly_stats(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Fetch weekly statistics from API
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            Statistics data
        """
        url = f"{self.api_base_url}/internal/stats/weekly"
        headers = {
            'X-Internal-API-Key': self.internal_token,
            'Content-Type': 'application/json'
        }
        data = {
            'start_date': start_date,
            'end_date': end_date
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result.get('data', {})
    
    def _format_daily_report(self, report: Dict[str, Any]) -> str:
        """Format daily report as text message
        
        Args:
            report: Report data
            
        Returns:
            Formatted message
        """
        date = report['date']
        data = report['data']
        
        message = f"📊 **千鱼千寻每日数据报告**\n\n"
        message += f"📅 日期: {date}\n\n"
        
        # User activity
        user_activity = data.get('user_activity', {})
        message += "👥 **用户活跃**\n"
        message += f"• 新增用户: {user_activity.get('new_users', 0)}\n"
        message += f"• 活跃用户: {user_activity.get('active_users', 0)}\n"
        message += f"• 留存率: {user_activity.get('retention_rate', 0):.1%}\n\n"
        
        # Content stats
        content_stats = data.get('content_stats', {})
        message += "📝 **内容统计**\n"
        message += f"• 新增帖子: {content_stats.get('new_posts', 0)}\n"
        message += f"• 新增评论: {content_stats.get('new_comments', 0)}\n"
        message += f"• 新增点赞: {content_stats.get('new_likes', 0)}\n\n"
        
        # Catch records
        catch_records = data.get('catch_records', {})
        message += "🎣 **渔获数据**\n"
        message += f"• 新增记录: {catch_records.get('new_records', 0)}\n"
        message += f"• 总重量: {catch_records.get('total_weight', 0):.1f}kg\n"
        
        popular_species = catch_records.get('popular_species', [])
        if popular_species:
            message += f"• 热门鱼种: {', '.join(popular_species[:3])}\n"
        
        message += "\n"
        
        # System health
        system_health = data.get('system_health', {})
        message += "⚙️ **系统健康**\n"
        message += f"• API 调用: {system_health.get('api_calls', 0)}\n"
        message += f"• 错误率: {system_health.get('error_rate', 0):.2%}\n"
        message += f"• 平均响应: {system_health.get('avg_response_time', 0):.0f}ms\n\n"
        
        message += f"---\n"
        message += f"⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return message
    
    def _format_weekly_report(self, report: Dict[str, Any]) -> str:
        """Format weekly report as text message
        
        Args:
            report: Report data
            
        Returns:
            Formatted message
        """
        start_date = report['start_date']
        end_date = report['end_date']
        data = report['data']
        
        message = f"📊 **千鱼千寻每周数据摘要**\n\n"
        message += f"📅 周期: {start_date} ~ {end_date}\n\n"
        
        # User growth
        user_growth = data.get('user_growth', {})
        message += "👥 **用户增长**\n"
        message += f"• 新增用户: {user_growth.get('new_users', 0)}\n"
        message += f"• 增长率: {user_growth.get('growth_rate', 0):.1%}\n\n"
        
        # Content trends
        content_trends = data.get('content_trends', {})
        message += "📝 **内容趋势**\n"
        message += f"• 互动率: {content_trends.get('engagement_rate', 0):.1%}\n\n"
        
        # Popular spots
        popular_spots = data.get('popular_spots', [])
        if popular_spots:
            message += "📍 **热门钓点**\n"
            for i, spot in enumerate(popular_spots[:5], 1):
                message += f"{i}. {spot.get('name', '未知')} ({spot.get('visits', 0)}次)\n"
            message += "\n"
        
        # Top catches
        top_catches = data.get('top_catches', [])
        if top_catches:
            message += "🏆 **本周之最**\n"
            for i, catch in enumerate(top_catches[:5], 1):
                species = catch.get('species', '未知')
                weight = catch.get('weight', 0)
                message += f"{i}. {species} - {weight:.1f}kg\n"
            message += "\n"
        
        message += f"---\n"
        message += f"⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return message
    
    def _send_to_feishu(self, message: str):
        """Send report to Feishu webhook
        
        Args:
            message: Report message
        """
        if not self.feishu_webhook:
            logger.warning("Feishu webhook not configured, skipping send")
            return
        
        try:
            payload = {
                "msg_type": "text",
                "content": {
                    "text": message
                }
            }
            
            response = requests.post(self.feishu_webhook, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info("Report sent to Feishu successfully")
        except Exception as e:
            logger.error(f"Failed to send report to Feishu: {e}")
            raise
    
    def _save_report(self, report: Dict[str, Any]):
        """Save report to database
        
        Args:
            report: Report data
        """
        try:
            url = f"{self.api_base_url}/internal/reports/save"
            headers = {
                'X-Internal-API-Key': self.internal_token,
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, headers=headers, json=report, timeout=30)
            response.raise_for_status()
            
            logger.info("Report saved to database")
        except Exception as e:
            logger.error(f"Failed to save report: {e}")
            # Don't raise - saving is optional
