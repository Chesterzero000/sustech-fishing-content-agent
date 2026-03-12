# -*- coding: utf-8 -*-
"""
Angler Radar Service - 钓友雷达服务
"""

import os
import httpx
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

API_BASE_URL = os.getenv("API_BASE_URL", "https://qianyu.iepose.cn")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "")


class AnglerRadarService:
    """钓友雷达服务类"""
    
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or API_BASE_URL
        self.api_key = api_key or INTERNAL_API_KEY
        self.headers = {
            "X-Internal-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def update_location(
        self,
        user_id: str,
        latitude: float,
        longitude: float,
        **kwargs
    ) -> Dict[str, Any]:
        """更新用户位置"""
        url = f"{self.base_url}/api/v1/angler-radar/location"
        data = {
            "user_id": user_id,
            "latitude": latitude,
            "longitude": longitude,
            **kwargs
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def get_nearby_anglers(
        self,
        latitude: float,
        longitude: float,
        radius: float = 5.0,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """获取附近钓友"""
        url = f"{self.base_url}/api/v1/angler-radar/nearby"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "radius": radius,
            "limit": limit
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def set_sharing(
        self,
        user_id: str,
        enabled: bool
    ) -> Dict[str, Any]:
        """设置位置共享"""
        url = f"{self.base_url}/api/v1/angler-radar/sharing"
        data = {"user_id": user_id, "enabled": enabled}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def delete_location(self, user_id: str) -> Dict[str, Any]:
        """删除用户位置"""
        url = f"{self.base_url}/api/v1/angler-radar/location/{user_id}"
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
