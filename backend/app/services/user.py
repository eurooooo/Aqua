"""用户相关业务逻辑"""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import UserCreate, UserUpdate


def calculate_nutrition_targets(
    age: int,
    gender: str,
    weight: float,
    height: float,
    activity_level: str,
    goal: str
) -> dict:
    """
    计算每日营养目标

    使用Mifflin-St Jeor公式计算基础代谢率(BMR)，
    然后根据活动水平和健康目标调整。

    Args:
        age: 年龄
        gender: 性别 (male/female)
        weight: 体重(kg)
        height: 身高(cm)
        activity_level: 活动水平 (sedentary/light/moderate/active)
        goal: 健康目标 (lose_weight/gain_weight/maintain)

    Returns:
        dict: 包含target_calories, target_protein, target_carbs, target_fat
    """
    # 1. 计算基础代谢率 (BMR)
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:  # female
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # 2. 根据活动水平计算每日总能量消耗 (TDEE)
    activity_multipliers = {
        "sedentary": 1.2,    # 久坐
        "light": 1.375,      # 轻度活动
        "moderate": 1.55,    # 中度活动
        "active": 1.725      # 高度活动
    }
    tdee = bmr * activity_multipliers.get(activity_level, 1.2)

    # 3. 根据健康目标调整卡路里
    goal_adjustments = {
        "lose_weight": -500,   # 减重：每天减少500卡路里
        "gain_weight": 500,    # 增重：每天增加500卡路里
        "maintain": 0          # 维持：不调整
    }
    target_calories = int(tdee + goal_adjustments.get(goal, 0))

    # 4. 计算宏量营养素目标
    # 蛋白质：每公斤体重1.6-2.2g（取1.8g）
    target_protein = round(weight * 1.8, 1)

    # 脂肪：占总卡路里的25-30%（取25%）
    target_fat = round((target_calories * 0.25) / 9, 1)  # 1g脂肪=9卡路里

    # 碳水化合物：剩余卡路里
    remaining_calories = target_calories - (target_protein * 4 + target_fat * 9)
    target_carbs = round(remaining_calories / 4, 1)  # 1g碳水=4卡路里

    return {
        "target_calories": target_calories,
        "target_protein": target_protein,
        "target_carbs": target_carbs,
        "target_fat": target_fat
    }


async def get_user(db: AsyncSession) -> Optional[User]:
    """
    获取用户档案（单用户应用）

    Args:
        db: 数据库会话

    Returns:
        User对象或None
    """
    result = await db.execute(select(User).limit(1))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """
    创建新用户

    Args:
        db: 数据库会话
        user_data: 用户创建数据

    Returns:
        创建的User对象
    """
    # 计算营养目标
    nutrition_targets = calculate_nutrition_targets(
        age=user_data.age,
        gender=user_data.gender,
        weight=user_data.weight,
        height=user_data.height,
        activity_level=user_data.activity_level,
        goal=user_data.goal
    )

    # 使用用户提供的值，如果没有则使用计算值
    user_dict = user_data.model_dump()
    user_dict.update({
        "target_calories": user_data.target_calories or nutrition_targets["target_calories"],
        "target_protein": user_data.target_protein or nutrition_targets["target_protein"],
        "target_carbs": user_data.target_carbs or nutrition_targets["target_carbs"],
        "target_fat": user_data.target_fat or nutrition_targets["target_fat"]
    })

    new_user = User(**user_dict)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_user(db: AsyncSession, user: User, user_data: UserCreate) -> User:
    """
    更新用户档案（完整更新）

    Args:
        db: 数据库会话
        user: 现有用户对象
        user_data: 新的用户数据

    Returns:
        更新后的User对象
    """
    # 计算营养目标
    nutrition_targets = calculate_nutrition_targets(
        age=user_data.age,
        gender=user_data.gender,
        weight=user_data.weight,
        height=user_data.height,
        activity_level=user_data.activity_level,
        goal=user_data.goal
    )

    # 更新所有字段
    for field, value in user_data.model_dump(exclude_unset=False).items():
        setattr(user, field, value)

    # 更新营养目标
    user.target_calories = user_data.target_calories or nutrition_targets["target_calories"]
    user.target_protein = user_data.target_protein or nutrition_targets["target_protein"]
    user.target_carbs = user_data.target_carbs or nutrition_targets["target_carbs"]
    user.target_fat = user_data.target_fat or nutrition_targets["target_fat"]

    await db.commit()
    await db.refresh(user)
    return user


async def partial_update_user(db: AsyncSession, user: User, user_data: UserUpdate) -> User:
    """
    部分更新用户档案

    Args:
        db: 数据库会话
        user: 现有用户对象
        user_data: 更新数据（只包含需要更新的字段）

    Returns:
        更新后的User对象
    """
    update_data = user_data.model_dump(exclude_unset=True)

    # 更新提供的字段
    for field, value in update_data.items():
        setattr(user, field, value)

    # 如果更新了影响营养目标的字段，重新计算
    if any(field in update_data for field in ["age", "gender", "weight", "height", "activity_level", "goal"]):
        nutrition_targets = calculate_nutrition_targets(
            age=user.age,
            gender=user.gender,
            weight=user.weight,
            height=user.height,
            activity_level=user.activity_level,
            goal=user.goal
        )

        # 只在用户未手动设置时更新
        if "target_calories" not in update_data:
            user.target_calories = nutrition_targets["target_calories"]
        if "target_protein" not in update_data:
            user.target_protein = nutrition_targets["target_protein"]
        if "target_carbs" not in update_data:
            user.target_carbs = nutrition_targets["target_carbs"]
        if "target_fat" not in update_data:
            user.target_fat = nutrition_targets["target_fat"]

    await db.commit()
    await db.refresh(user)
    return user
