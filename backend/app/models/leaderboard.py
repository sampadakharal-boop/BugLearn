from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import Base


class Leaderboard(Base):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)
    xp_points = Column(Integer, default=0)
    level_reached = Column(Integer, default=1)
    rank = Column(Integer, nullable=True)

    @classmethod
    async def get_by_user_id(cls, session: AsyncSession, user_id: int) -> Optional["Leaderboard"]:
        result = await session.execute(select(cls).where(cls.user_id == user_id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_top(cls, session: AsyncSession, limit: int = 20) -> list["Leaderboard"]:
        result = await session.execute(
            select(cls).order_by(cls.xp_points.desc()).limit(limit)
        )
        return list(result.scalars().all())
