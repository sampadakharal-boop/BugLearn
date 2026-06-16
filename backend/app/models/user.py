from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    current_level = Column(Integer, default=1)
    xp_points = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    @classmethod
    async def get_by_id(cls, session: AsyncSession, user_id: int) -> Optional["User"]:
        result = await session.execute(select(cls).where(cls.id == user_id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> Optional["User"]:
        result = await session.execute(select(cls).where(cls.email == email))
        return result.scalar_one_or_none()

    async def add_xp(self, session: AsyncSession, amount: int):
        self.xp_points += amount
        await session.commit()

    async def advance_level(self, session: AsyncSession):
        self.current_level += 1
        await session.commit()
