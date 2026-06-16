from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import Base


class LevelProgress(Base):
    __tablename__ = "level_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    level_number = Column(Integer, nullable=False)
    status = Column(String(20), default="locked")
    interview_score = Column(Float, nullable=True)
    notes_score = Column(Float, nullable=True)
    notes_approved = Column(Boolean, nullable=True, default=None)
    last_attempt_date = Column(DateTime(timezone=True), nullable=True)

    @classmethod
    async def get_by_user_and_level(cls, session: AsyncSession, user_id: int, level_number: int) -> Optional["LevelProgress"]:
        result = await session.execute(
            select(cls).where(cls.user_id == user_id, cls.level_number == level_number)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_all_for_user(cls, session: AsyncSession, user_id: int) -> list["LevelProgress"]:
        result = await session.execute(
            select(cls).where(cls.user_id == user_id).order_by(cls.level_number)
        )
        return list(result.scalars().all())
