from fastapi import APIRouter

from .user import router as user_router

# 创建主路由
api_router = APIRouter()

# 注册子路由
api_router.include_router(user_router)

__all__ = ["api_router"]
