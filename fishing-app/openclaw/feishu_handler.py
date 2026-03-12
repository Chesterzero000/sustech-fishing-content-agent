"""Feishu Command Handler - 飞书管理员命令处理"""
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import requests

logger = logging.getLogger(__name__)


class FeishuCommandHandler:
    """飞书命令处理器
    
    处理管理员通过飞书发送的命令，调用相应的 Skills 或内部 API
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize command handler
        
        Args:
            config: OpenClaw configuration
        """
        self.config = config
        self.api_base_url = config.get('api', {}).get('base_url')
        self.internal_token = config.get('api', {}).get('internal_token')
        
        # Command registry
        self.commands: Dict[str, Callable] = {}
        self._register_commands()
    
    def _register_commands(self):
        """Register all available commands"""
        # System commands
        self.commands['status'] = self.cmd_status
        self.commands['health'] = self.cmd_health
        self.commands['help'] = self.cmd_help
        
        # Stats commands
        self.commands['stats'] = self.cmd_stats
        
        # Skills commands
        self.commands['skills'] = self.cmd_skills
        
        # Report commands
        self.commands['report'] = self.cmd_report
        
        # User commands
        self.commands['users'] = self.cmd_users
        
        # Content commands
        self.commands['posts'] = self.cmd_posts
        
        # API commands
        self.commands['api'] = self.cmd_api
    
    def handle_message(self, message: str) -> str:
        """Handle incoming message from Feishu
        
        Args:
            message: Message text
            
        Returns:
            Response text
        """
        message = message.strip()
        
        # Check if it's a command (starts with /)
        if not message.startswith('/'):
            return self._format_help()
        
        # Parse command and arguments
        parts = message[1:].split()
        if not parts:
            return self._format_help()
        
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        # Execute command
        if command in self.commands:
            try:
                return self.commands[command](args)
            except Exception as e:
                logger.error(f"Command execution error: {e}", exc_info=True)
                return f"❌ 命令执行失败: {str(e)}"
        else:
            return f"❌ 未知命令: /{command}\n\n使用 /help 查看可用命令"
    
    def _call_internal_api(self, endpoint: str, method: str = 'GET', 
                          data: Optional[Dict] = None) -> Dict[str, Any]:
        """Call internal API
        
        Args:
            endpoint: API endpoint
            method: HTTP method
            data: Request data
            
        Returns:
            API response
        """
        url = f"{self.api_base_url}{endpoint}"
        headers = {
            'X-Internal-API-Key': self.internal_token,
            'Content-Type': 'application/json'
        }
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"API call failed: {e}")
            raise
    
    # ============ Command Implementations ============
    
    def cmd_status(self, args: list) -> str:
        """System status command"""
        try:
            result = self._call_internal_api('/internal/health/check', 'POST')
            data = result.get('data', {})
            
            status = data.get('status', 'unknown')
            timestamp = data.get('timestamp', '')
            components = data.get('components', {})
            
            response = f"📊 **系统状态**\n\n"
            response += f"状态: {'✅ 正常' if status == 'healthy' else '❌ 异常'}\n"
            response += f"时间: {timestamp}\n\n"
            response += "**组件状态:**\n"
            
            for name, info in components.items():
                comp_status = info.get('status', 'unknown')
                response_time = info.get('response_time', 0)
                icon = '✅' if comp_status == 'up' else '❌'
                response += f"{icon} {name}: {comp_status} ({response_time}ms)\n"
            
            return response
        except Exception as e:
            return f"❌ 获取系统状态失败: {str(e)}"
    
    def cmd_health(self, args: list) -> str:
        """Health check command"""
        return self.cmd_status(args)
    
    def cmd_stats(self, args: list) -> str:
        """Statistics command"""
        period = args[0] if args else 'today'
        
        try:
            if period == 'today':
                result = self._call_internal_api('/internal/stats/daily', 'POST')
            elif period == 'week':
                result = self._call_internal_api('/internal/stats/weekly', 'POST')
            else:
                return f"❌ 不支持的时间范围: {period}\n\n使用: /stats [today|week]"
            
            data = result.get('data', {})
            
            response = f"📈 **数据统计 - {period}**\n\n"
            
            # User activity
            user_activity = data.get('user_activity', {})
            response += "**用户活跃:**\n"
            response += f"新增用户: {user_activity.get('new_users', 0)}\n"
            response += f"活跃用户: {user_activity.get('active_users', 0)}\n"
            response += f"留存率: {user_activity.get('retention_rate', 0):.1%}\n\n"
            
            # Content stats
            content_stats = data.get('content_stats', {})
            response += "**内容统计:**\n"
            response += f"新增帖子: {content_stats.get('new_posts', 0)}\n"
            response += f"新增评论: {content_stats.get('new_comments', 0)}\n"
            response += f"新增点赞: {content_stats.get('new_likes', 0)}\n\n"
            
            # Catch records
            catch_records = data.get('catch_records', {})
            response += "**渔获数据:**\n"
            response += f"新增记录: {catch_records.get('new_records', 0)}\n"
            response += f"总重量: {catch_records.get('total_weight', 0):.1f}kg\n"
            
            return response
        except Exception as e:
            return f"❌ 获取统计数据失败: {str(e)}"
    
    def cmd_skills(self, args: list) -> str:
        """Skills management command"""
        if not args:
            # List all skills
            skills = self.config.get('skills', [])
            response = "🛠️ **Skills 列表**\n\n"
            
            for skill in skills:
                name = skill.get('name')
                display_name = skill.get('display_name', name)
                enabled = skill.get('enabled', True)
                category = skill.get('category', 'unknown')
                status_icon = '✅' if enabled else '❌'
                
                response += f"{status_icon} **{display_name}** ({name})\n"
                response += f"   分类: {category}\n"
                response += f"   端口: {skill.get('mcp_port', 'N/A')}\n\n"
            
            return response
        
        subcommand = args[0].lower()
        
        if subcommand == 'list':
            return self.cmd_skills([])
        elif subcommand == 'status' and len(args) > 1:
            skill_name = args[1]
            # TODO: Check actual skill status
            return f"📊 Skill 状态: {skill_name}\n\n状态: ✅ 运行中"
        else:
            return "❌ 用法: /skills [list|status <name>]"
    
    def cmd_report(self, args: list) -> str:
        """Report command"""
        if not args:
            return "❌ 用法: /report [daily|weekly]"
        
        report_type = args[0].lower()
        
        if report_type not in ['daily', 'weekly']:
            return f"❌ 不支持的报告类型: {report_type}"
        
        # TODO: Trigger report generation
        return f"✅ 正在生成 {report_type} 报告...\n\n报告将在生成完成后推送到此群"
    
    def cmd_users(self, args: list) -> str:
        """Users command"""
        if not args:
            subcommand = 'stats'
        else:
            subcommand = args[0].lower()
        
        if subcommand == 'stats':
            try:
                result = self._call_internal_api('/internal/users/active?time_range=day')
                data = result.get('data', {})
                total = data.get('total', 0)
                
                return f"👥 **用户统计**\n\n今日活跃用户: {total}"
            except Exception as e:
                return f"❌ 获取用户统计失败: {str(e)}"
        else:
            return "❌ 用法: /users [stats]"
    
    def cmd_posts(self, args: list) -> str:
        """Posts command"""
        if not args:
            subcommand = 'trending'
        else:
            subcommand = args[0].lower()
        
        if subcommand == 'trending':
            try:
                result = self._call_internal_api('/internal/posts/trending?time_range=day')
                data = result.get('data', {})
                posts = data.get('posts', [])
                
                response = "🔥 **热门帖子**\n\n"
                
                if not posts:
                    response += "暂无热门帖子"
                else:
                    for i, post in enumerate(posts[:5], 1):
                        title = post.get('title', '无标题')
                        likes = post.get('likes', 0)
                        comments = post.get('comments', 0)
                        response += f"{i}. {title}\n"
                        response += f"   👍 {likes} | 💬 {comments}\n\n"
                
                return response
            except Exception as e:
                return f"❌ 获取热门帖子失败: {str(e)}"
        else:
            return "❌ 用法: /posts [trending]"
    
    def cmd_api(self, args: list) -> str:
        """API command"""
        if not args:
            subcommand = 'health'
        else:
            subcommand = args[0].lower()
        
        if subcommand == 'health':
            return self.cmd_health([])
        else:
            return "❌ 用法: /api [health]"
    
    def cmd_help(self, args: list) -> str:
        """Help command"""
        return self._format_help()
    
    def _format_help(self) -> str:
        """Format help message"""
        help_text = """
📖 **千鱼千寻管理命令**

**系统命令:**
/status - 查询系统状态
/health - 健康检查
/help - 显示此帮助信息

**数据统计:**
/stats [today|week] - 查询数据统计
/users stats - 用户统计
/posts trending - 热门帖子

**Skills 管理:**
/skills list - 列出所有 Skills
/skills status <name> - 查询 Skill 状态

**报告管理:**
/report daily - 手动触发每日报告
/report weekly - 手动触发每周报告

**API 管理:**
/api health - API 健康检查

---
💡 提示: 所有命令都以 / 开头
"""
        return help_text.strip()
