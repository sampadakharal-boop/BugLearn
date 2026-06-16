from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import Base


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    badge = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=False)
    icon = Column(String(10), default="🏆")
    earned_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    @classmethod
    async def get_for_user(cls, session: AsyncSession, user_id: int) -> list["Achievement"]:
        result = await session.execute(
            select(cls).where(cls.user_id == user_id).order_by(cls.earned_at.desc())
        )
        return list(result.scalars().all())

    @classmethod
    async def has_badge(cls, session: AsyncSession, user_id: int, badge: str) -> bool:
        result = await session.execute(
            select(cls).where(cls.user_id == user_id, cls.badge == badge)
        )
        return result.scalar_one_or_none() is not None
