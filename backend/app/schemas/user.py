from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class UserBase(BaseModel):
    """用户基础模型"""

    age: int = Field(..., ge=1, le=150, description="年龄")
    gender: str = Field(..., pattern="^(male|female)$", description="性别")
    height: float = Field(..., gt=0, le=300, description="身高(cm)")
    weight: float = Field(..., gt=0, le=500, description="体重(kg)")
    goal: str = Field(
        ...,
        pattern="^(lose_weight|gain_weight|maintain)$",
        description="健康目标"
    )
    activity_level: str = Field(
        ...,
        pattern="^(sedentary|light|moderate|active)$",
        description="活动水平"
    )
    dietary_restrictions: List[str] = Field(
        default_factory=list,
        description="饮食限制"
    )
    allergies: List[str] = Field(default_factory=list, description="过敏源")
    preferences: List[str] = Field(default_factory=list, description="口味偏好")


class UserCreate(UserBase):
    """创建用户模型"""

    target_calories: Optional[int] = Field(
        None,
        ge=0,
        description="日目标卡路里（可选，系统可自动计算）"
    )
    target_protein: Optional[float] = Field(None, ge=0, description="日目标蛋白质(g)")
    target_carbs: Optional[float] = Field(None, ge=0, description="日目标碳水化合物(g)")
    target_fat: Optional[float] = Field(None, ge=0, description="日目标脂肪(g)")


class UserUpdate(BaseModel):
    """更新用户模型（所有字段可选）"""

    age: Optional[int] = Field(None, ge=1, le=150, description="年龄")
    gender: Optional[str] = Field(None, pattern="^(male|female)$", description="性别")
    height: Optional[float] = Field(None, gt=0, le=300, description="身高(cm)")
    weight: Optional[float] = Field(None, gt=0, le=500, description="体重(kg)")
    goal: Optional[str] = Field(
        None,
        pattern="^(lose_weight|gain_weight|maintain)$",
        description="健康目标"
    )
    activity_level: Optional[str] = Field(
        None,
        pattern="^(sedentary|light|moderate|active)$",
        description="活动水平"
    )
    dietary_restrictions: Optional[List[str]] = Field(None, description="饮食限制")
    allergies: Optional[List[str]] = Field(None, description="过敏源")
    preferences: Optional[List[str]] = Field(None, description="口味偏好")
    target_calories: Optional[int] = Field(None, ge=0, description="日目标卡路里")
    target_protein: Optional[float] = Field(None, ge=0, description="日目标蛋白质(g)")
    target_carbs: Optional[float] = Field(None, ge=0, description="日目标碳水化合物(g)")
    target_fat: Optional[float] = Field(None, ge=0, description="日目标脂肪(g)")


class UserResponse(UserBase):
    """用户响应模型"""

    id: str = Field(..., description="用户ID")
    target_calories: Optional[int] = Field(None, description="日目标卡路里")
    target_protein: Optional[float] = Field(None, description="日目标蛋白质(g)")
    target_carbs: Optional[float] = Field(None, description="日目标碳水化合物(g)")
    target_fat: Optional[float] = Field(None, description="日目标脂肪(g)")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    model_config = {"from_attributes": True}
