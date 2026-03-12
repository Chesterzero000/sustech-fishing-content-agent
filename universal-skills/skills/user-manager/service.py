# -*- coding: utf-8 -*-
"""User Manager Service"""
import os
import httpx
from typing import Dict, Any, Optional

API_BASE_URL = os.getenv("API_BASE_URL", "https://qianyu.iepose.cn")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "")

class UserManagerService:
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or API_BASE_URL
        self.api_key = api_key or INTERNAL_API_KEY
        self.headers = {"X-Internal-API-Key": self.api_key, "Content-Type": "application/json"}
    
    async def wx_login(self, code: str) -> Dict[str, Any]:
        """微信登录"""
        url = f"{self.base_url}/api/v1/wx/login"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={"code": code}, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def get_profile(self, user_id: str) -> Dict[str, Any]:
        """获取用户资料"""
        url = f"{self.base_url}/api/v1/user/{user_id}/profile"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def update_profile(self, user_id: str, **kwargs) -> Dict[str, Any]:
        """更新用户资料"""
        url = f"{self.base_url}/api/v1/user/{user_id}/profile"
        async with httpx.AsyncClient() as client:
            response = await client.put(url, json=kwargs, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def add_fishing_record(self, user_id: str, **kwargs) -> Dict[str, Any]:
        """添加钓鱼记录"""
        url = f"{self.base_url}/api/v1/user/{user_id}/fishing-record"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=kwargs, headers=self.headers)
            response.raise_for_status()
            return response.json()
