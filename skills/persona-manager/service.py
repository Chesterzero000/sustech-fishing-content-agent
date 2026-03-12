# -*- coding: utf-8 -*-
"""Persona Manager Service"""
import os
import httpx
from typing import Dict, Any, List

API_BASE_URL = os.getenv("API_BASE_URL", "https://qianyu.iepose.cn")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "")

class PersonaManagerService:
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or API_BASE_URL
        self.api_key = api_key or INTERNAL_API_KEY
        self.headers = {"X-Internal-API-Key": self.api_key, "Content-Type": "application/json"}
    
    async def list_personas(self) -> List[Dict[str, Any]]:
        """获取人设列表"""
        url = f"{self.base_url}/api/v1/voice-styles"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def get_persona(self, style_id: str) -> Dict[str, Any]:
        """获取人设详情"""
        url = f"{self.base_url}/api/v1/voice-styles/{style_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
