# -*- coding: utf-8 -*-
"""
Feishu Client - 飞书客户端
用于发送消息到飞书群
"""

import os
import httpx
from typing import Dict, Any

FEISHU_WEBHOOK_REPORTS = os.getenv("FEISHU_WEBHOOK_REPORTS", "")


class FeishuClient:
    """飞书客户端"""
    
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or FEISHU_WEBHOOK_REPORTS
    
    async def send_markdown(self, title: str, content: str) -> Dict[str, Any]:
        """发送 Markdown 消息"""
        if not self.webhook_url:
            raise ValueError("Feishu webhook URL not configured")
        
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {"tag": "plain_text", "content": title}
                },
                "elements": [
                    {"tag": "markdown", "content": content}
                ]
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.webhook_url, json=payload)
            response.raise_for_status()
            return response.json()
    
    async def send_text(self, text: str) -> Dict[str, Any]:
        """发送文本消息"""
        if not self.webhook_url:
            raise ValueError("Feishu webhook URL not configured")
        
        payload = {"msg_type": "text", "content": {"text": text}}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.webhook_url, json=payload)
            response.raise_for_status()
            return response.json()
