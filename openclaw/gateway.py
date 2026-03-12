"""OpenClaw Gateway - Main Entry Point"""
import logging
import sys
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from openclaw.config_loader import get_config
from openclaw.feishu_handler import FeishuCommandHandler
from openclaw.cron_scheduler import CronScheduler

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


class OpenClawGateway:
    """OpenClaw Gateway - 千鱼千寻智能执行层
    
    职责:
    - 飞书消息接入
    - Skills 路由和执行
    - 定时任务管理
    - 智能监控和告警
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize OpenClaw Gateway
        
        Args:
            config_path: Path to openclaw.yaml
        """
        logger.info("Initializing OpenClaw Gateway...")
        
        # Load configuration
        self.config = get_config()
        logger.info(f"Loaded configuration: {self.config.get('name')}")
        
        # Initialize Feishu handler
        self.feishu_handler = FeishuCommandHandler(self.config.get_all())
        logger.info("Feishu handler initialized")
        
        # Initialize cron scheduler
        self.cron_scheduler = CronScheduler(self.config.get_all())
        logger.info("Cron scheduler initialized")
        
        # TODO: Initialize other components
        # - MCP server manager
        # - Monitoring system
        
        logger.info("OpenClaw Gateway initialized successfully")
    
    def handle_feishu_message(self, message: str) -> str:
        """Handle message from Feishu
        
        Args:
            message: Message text
            
        Returns:
            Response text
        """
        logger.info(f"Handling Feishu message: {message}")
        
        try:
            response = self.feishu_handler.handle_message(message)
            logger.info(f"Response generated: {len(response)} chars")
            return response
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            return f"❌ 处理消息时出错: {str(e)}"
    
    def start(self):
        """Start OpenClaw Gateway"""
        logger.info("Starting OpenClaw Gateway...")
        
        # Start cron scheduler
        self.cron_scheduler.start()
        
        # TODO: Start other services
        # - Start MCP servers
        # - Start monitoring
        # - Start Feishu bot
        
        logger.info("OpenClaw Gateway started")
    
    def stop(self):
        """Stop OpenClaw Gateway"""
        logger.info("Stopping OpenClaw Gateway...")
        
        # Stop cron scheduler
        self.cron_scheduler.stop()
        
        # TODO: Stop other services
        
        logger.info("OpenClaw Gateway stopped")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenClaw Gateway')
    parser.add_argument('--config', help='Path to openclaw.yaml')
    parser.add_argument('--test-command', help='Test a command')
    
    args = parser.parse_args()
    
    # Initialize gateway
    gateway = OpenClawGateway(args.config)
    
    # Test mode
    if args.test_command:
        print("\n" + "="*60)
        print("Testing command:", args.test_command)
        print("="*60 + "\n")
        
        response = gateway.handle_feishu_message(args.test_command)
        # Handle encoding for Windows console
        import sys
        if sys.platform == 'win32':
            # Remove emoji for Windows console
            response = response.encode('ascii', errors='ignore').decode('ascii')
        print(response)
        print("\n" + "="*60)
        return
    
    # Normal mode
    try:
        gateway.start()
        
        # Keep running
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    finally:
        gateway.stop()


if __name__ == '__main__':
    main()
