from typing import List, Optional
from uuid import uuid4

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """用户模型"""

    __tablename__ = "users"

    # 主键
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
        comment="用户ID"
    )

    # 基本信息
    age: Mapped[int] = mapped_column(comment="年龄")
    gender: Mapped[str] = mapped_column(String(10), comment="性别: male/female")
    height: Mapped[float] = mapped_column(comment="身高(cm)")
    weight: Mapped[float] = mapped_column(comment="体重(kg)")

    # 健康目标
    goal: Mapped[str] = mapped_column(
        String(20),
        comment="健康目标: lose_weight/gain_weight/maintain"
    )
    activity_level: Mapped[str] = mapped_column(
        String(20),
        comment="活动水平: sedentary/light/moderate/active"
    )

    # 饮食偏好（JSON存储列表）
    dietary_restrictions: Mapped[List[str]] = mapped_column(
        JSON,
        default=list,
        comment="饮食限制: ['vegetarian', 'gluten_free', ...]"
    )
    allergies: Mapped[List[str]] = mapped_column(
        JSON,
        default=list,
        comment="过敏源: ['peanuts', 'dairy', ...]"
    )
    preferences: Mapped[List[str]] = mapped_column(
        JSON,
        default=list,
        comment="口味偏好: ['spicy', 'mild', ...]"
    )

    # 营养目标（可选）
    target_calories: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        comment="日目标卡路里"
    )
    target_protein: Mapped[Optional[float]] = mapped_column(
        nullable=True,
        comment="日目标蛋白质(g)"
    )
    target_carbs: Mapped[Optional[float]] = mapped_column(
        nullable=True,
        comment="日目标碳水化合物(g)"
    )
    target_fat: Mapped[Optional[float]] = mapped_column(
        nullable=True,
        comment="日目标脂肪(g)"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, age={self.age}, goal={self.goal})>"
