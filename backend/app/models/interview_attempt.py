from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import Base


class InterviewAttempt(Base):
    __tablename__ = "interview_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    level_number = Column(Integer, nullable=False)
    audio_transcript = Column(Text, nullable=True)
    score = Column(Float, nullable=False)
    total = Column(Integer, nullable=False, default=10)
    correct_count = Column(Integer, nullable=False, default=0)
    passed = Column(Boolean, nullable=False)
    feedback = Column(Text, nullable=True)
    weak_areas = Column(Text, nullable=True)
    recommended_lessons = Column(Text, nullable=True)
    questions_json = Column(Text, nullable=True)
    answers_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    @classmethod
    async def get_for_user_and_level(cls, session: AsyncSession, user_id: int, level_number: int) -> list["InterviewAttempt"]:
        result = await session.execute(
            select(cls).where(cls.user_id == user_id, cls.level_number == level_number)
            .order_by(cls.created_at.desc())
        )
        return list(result.scalars().all())
