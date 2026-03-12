# -*- coding: utf-8 -*-
"""Feedback Manager Service"""
import os
import httpx
from typing import Dict, Any, List, Optional

API_BASE_URL = os.getenv("API_BASE_URL", "https://qianyu.iepose.cn")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "")

class FeedbackManagerService:
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or API_BASE_URL
        self.api_key = api_key or INTERNAL_API_KEY
        self.headers = {"X-Internal-API-Key": self.api_key, "Content-Type": "application/json"}
    
    async def submit_feedback(self, user_id: str, feedback_type: str, **kwargs) -> Dict[str, Any]:
        """提交反馈"""
        url = f"{self.base_url}/api/v1/feedback"
        data = {"user_id": user_id, "feedback_type": feedback_type, **kwargs}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def get_feedback_stats(self) -> Dict[str, Any]:
        """获取反馈统计"""
        url = f"{self.base_url}/api/v1/feedback/stats"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def get_user_feedback(self, user_id: str) -> List[Dict[str, Any]]:
        """获取用户反馈"""
        url = f"{self.base_url}/api/v1/feedback/user/{user_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def get_unresolved_feedback(self) -> List[Dict[str, Any]]:
        """获取未解决反馈"""
        url = f"{self.base_url}/api/v1/feedback/unresolved"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
