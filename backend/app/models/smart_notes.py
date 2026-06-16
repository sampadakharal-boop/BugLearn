from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import Base


class SmartNotes(Base):
    __tablename__ = "smart_notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    level_number = Column(Integer, nullable=False)
    notes_text = Column(Text, nullable=True)
    quality_score = Column(Float, nullable=False)
    concept_coverage = Column(Float, nullable=False, default=0.0)
    clarity_score = Column(Float, nullable=False, default=0.0)
    accuracy_score = Column(Float, nullable=False, default=0.0)
    completeness_score = Column(Float, nullable=False, default=0.0)
    examples_score = Column(Float, nullable=False, default=0.0)
    handwriting_score = Column(Float, nullable=True, default=0.0)
    page_count = Column(Integer, nullable=False, default=0)
    passed = Column(Boolean, nullable=False, default=False)
    feedback = Column(Text, nullable=True)
    missing_concepts = Column(Text, nullable=True)
    matched_concepts = Column(Text, nullable=True)
    weak_areas = Column(Text, nullable=True)
    recommended_lessons = Column(Text, nullable=True)
    word_count = Column(Integer, nullable=False, default=0)
    flag_spam = Column(Boolean, nullable=False, default=False)
    flag_too_short = Column(Boolean, nullable=False, default=False)
    flag_copied = Column(Boolean, nullable=False, default=False)
    flag_suspicious_image = Column(Boolean, nullable=False, default=False)
    image_paths = Column(Text, nullable=True)
    image_analysis_json = Column(Text, nullable=True)
    has_diagrams = Column(Boolean, nullable=True, default=False)
    has_analogies = Column(Boolean, nullable=True, default=False)
    has_examples = Column(Boolean, nullable=True, default=False)
    has_summary = Column(Boolean, nullable=True, default=False)
    organization_score = Column(Float, nullable=True, default=0.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    @classmethod
    async def get_for_user_and_level(cls, session: AsyncSession, user_id: int, level_number: int) -> list["SmartNotes"]:
        result = await session.execute(
            select(cls).where(cls.user_id == user_id, cls.level_number == level_number)
            .order_by(cls.created_at.desc())
        )
        return list(result.scalars().all())

    @classmethod
    async def get_latest_for_user_and_level(cls, session: AsyncSession, user_id: int, level_number: int) -> Optional["SmartNotes"]:
        result = await session.execute(
            select(cls).where(cls.user_id == user_id, cls.level_number == level_number)
            .order_by(cls.created_at.desc()).limit(1)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_passed_for_user_and_level(cls, session: AsyncSession, user_id: int, level_number: int) -> Optional["SmartNotes"]:
        result = await session.execute(
            select(cls).where(cls.user_id == user_id, cls.level_number == level_number, cls.passed == True)
            .limit(1)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_all_for_user(cls, session: AsyncSession, user_id: int) -> list["SmartNotes"]:
        result = await session.execute(
            select(cls).where(cls.user_id == user_id)
            .order_by(cls.created_at.desc())
        )
        return list(result.scalars().all())
