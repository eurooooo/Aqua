"""用户相关API路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.services import user as user_service

router = APIRouter(prefix="/api/user", tags=["user"])


@router.get("/profile", response_model=UserResponse)
async def get_user_profile(db: AsyncSession = Depends(get_db)):
    """
    获取用户档案

    注：当前为单用户应用，返回第一个用户的档案
    """
    user = await user_service.get_user(db)
    if not user:
        raise HTTPException(status_code=404, detail="用户档案不存在，请先创建")
    return user


@router.post("/profile", response_model=UserResponse, status_code=201)
async def create_or_update_profile(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建或更新用户档案

    - 如果用户不存在，创建新用户
    - 如果用户已存在，更新用户信息
    - 自动计算营养目标（如果未提供）
    """
    existing_user = await user_service.get_user(db)

    if existing_user:
        # 更新现有用户
        return await user_service.update_user(db, existing_user, user_data)
    else:
        # 创建新用户
        return await user_service.create_user(db, user_data)


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    部分更新用户档案

    只更新提供的字段，自动重新计算营养目标
    """
    user = await user_service.get_user(db)
    if not user:
        raise HTTPException(status_code=404, detail="用户档案不存在，请先创建")

    return await user_service.partial_update_user(db, user, user_data)
