# -*- coding: utf-8 -*-
"""
内部 API 认证中间件
用于保护内部 API 端点，只允许 OpenClaw 等内部服务访问
"""

import os
from typing import Callable
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

# 从环境变量获取内部 API Key
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "")

# 需要认证的内部 API 路径前缀
INTERNAL_API_PREFIXES = [
    "/internal/",
    "/admin/internal/",
]

# 不需要认证的路径（白名单）
PUBLIC_PATHS = [
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
]


class InternalAPIAuthMiddleware(BaseHTTPMiddleware):
    """
    内部 API 认证中间件
    
    验证请求头中的 X-Internal-API-Key 是否匹配配置的密钥
    """
    
    async def dispatch(self, request: Request, call_next: Callable):
        """
        处理请求
        
        Args:
            request: FastAPI 请求对象
            call_next: 下一个中间件或路由处理器
            
        Returns:
            响应对象
        """
        path = request.url.path
        
        # 检查是否是公开路径
        if any(path.startswith(public_path) for public_path in PUBLIC_PATHS):
            return await call_next(request)
        
        # 检查是否是内部 API 路径
        is_internal_api = any(
            path.startswith(prefix) for prefix in INTERNAL_API_PREFIXES
        )
        
        if is_internal_api:
            # 验证 API Key
            api_key = request.headers.get("X-Internal-API-Key", "")
            
            if not INTERNAL_API_KEY:
                logger.error("INTERNAL_API_KEY not configured in environment")
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={
                        "code": 500,
                        "message": "Internal API authentication not configured",
                        "data": None
                    }
                )
            
            if api_key != INTERNAL_API_KEY:
                logger.warning(
                    f"Unauthorized internal API access attempt: {path} "
                    f"from {request.client.host}"
                )
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "code": 401,
                        "message": "Invalid or missing internal API key",
                        "data": None
                    }
                )
            
            logger.info(f"Internal API access authorized: {path}")
        
        # 继续处理请求
        response = await call_next(request)
        return response


def verify_internal_api_key(api_key: str) -> bool:
    """
    验证内部 API Key
    
    Args:
        api_key: 要验证的 API Key
        
    Returns:
        bool: 是否有效
    """
    if not INTERNAL_API_KEY:
        logger.error("INTERNAL_API_KEY not configured")
        return False
    
    return api_key == INTERNAL_API_KEY


def get_internal_api_key_dependency():
    """
    FastAPI 依赖项：验证内部 API Key
    
    用法:
        @app.get("/internal/something", dependencies=[Depends(get_internal_api_key_dependency)])
        async def internal_endpoint():
            ...
    
    Raises:
        HTTPException: 如果 API Key 无效
    """
    async def verify_key(request: Request):
        api_key = request.headers.get("X-Internal-API-Key", "")
        
        if not verify_internal_api_key(api_key):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing internal API key"
            )
        
        return True
    
    return verify_key


# 便捷函数：生成随机 API Key
def generate_api_key(length: int = 32) -> str:
    """
    生成随机 API Key
    
    Args:
        length: Key 长度
        
    Returns:
        str: 随机生成的 API Key
    """
    import secrets
    import string
    
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


if __name__ == "__main__":
    # 测试：生成一个新的 API Key
    print("Generated API Key:")
    print(generate_api_key())
