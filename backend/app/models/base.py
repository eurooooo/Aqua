from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """所有数据库模型的基类"""

    pass


class TimestampMixin:
    """时间戳混入类，提供创建和更新时间字段"""

    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        nullable=False,
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="更新时间"
    )
