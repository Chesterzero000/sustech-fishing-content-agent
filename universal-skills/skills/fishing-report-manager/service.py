# -*- coding: utf-8 -*-
"""
Fishing Report Manager Service - 渔获报告服务

调用 Community API 的渔获报告相关端点
"""

import os
import httpx
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

# API 配置
API_BASE_URL = os.getenv("API_BASE_URL", "https://qianyu.iepose.cn")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "")


class FishingReportService:
    """渔获报告服务类"""
    
    def __init__(self, base_url: str = None, api_key: str = None):
        """
        初始化服务
        
        Args:
            base_url: API 基础 URL
            api_key: 内部 API Key
        """
        self.base_url = base_url or API_BASE_URL
        self.api_key = api_key or INTERNAL_API_KEY
        self.headers = {
            "X-Internal-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def create_report(
        self,
        user_id: str,
        spot_id: str,
        fish_species: str,
        weight: float,
        length: float,
        **kwargs
    ) -> Dict[str, Any]:
        """
        创建渔获报告
        
        Args:
            user_id: 用户 ID
            spot_id: 钓点 ID
            fish_species: 鱼种
            weight: 重量（kg）
            length: 长度（cm）
            **kwargs: 其他参数（bait, weather, notes 等）
            
        Returns:
            Dict: 创建结果
        """
        url = f"{self.base_url}/api/v1/fishing-reports"
        
        data = {
            "user_id": user_id,
            "spot_id": spot_id,
            "fish_species": fish_species,
            "weight": weight,
            "length": length,
            **kwargs
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def get_reports(
        self,
        user_id: Optional[str] = None,
        spot_id: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        获取渔获报告列表
        
        Args:
            user_id: 用户 ID（可选）
            spot_id: 钓点 ID（可选）
            limit: 返回数量
            offset: 偏移量
            
        Returns:
            List[Dict]: 报告列表
        """
        url = f"{self.base_url}/api/v1/fishing-reports"
        
        params = {"limit": limit, "offset": offset}
        if user_id:
            params["user_id"] = user_id
        if spot_id:
            params["spot_id"] = spot_id
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def get_nearby_reports(
        self,
        latitude: float,
        longitude: float,
        radius: float = 10.0,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        获取附近的渔获报告
        
        Args:
            latitude: 纬度
            longitude: 经度
            radius: 半径（km）
            limit: 返回数量
            
        Returns:
            List[Dict]: 附近的报告列表
        """
        url = f"{self.base_url}/api/v1/fishing-reports/nearby"
        
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
    
    async def get_report_stats(
        self,
        user_id: Optional[str] = None,
        time_range: str = "month"
    ) -> Dict[str, Any]:
        """
        获取渔获报告统计
        
        Args:
            user_id: 用户 ID（可选）
            time_range: 时间范围（day/week/month/year）
            
        Returns:
            Dict: 统计数据
        """
        url = f"{self.base_url}/api/v1/fishing-reports/stats"
        
        params = {"time_range": time_range}
        if user_id:
            params["user_id"] = user_id
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
