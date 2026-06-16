from pydantic import BaseModel
from typing import List, Optional


class NotesSubmitRequest(BaseModel):
    level_number: int


class NotesScoreBreakdown(BaseModel):
    concept_coverage: float
    clarity_score: float
    accuracy_score: float
    completeness_score: float
    examples_score: float


class NewBadge(BaseModel):
    badge: str
    title: str
    description: str
    icon: str


class NotesSubmitResponse(BaseModel):
    id: int
    level_number: int
    quality_score: float
    passed: bool
    pass_threshold: float
    score_breakdown: NotesScoreBreakdown
    matched_concepts: List[str]
    missing_concepts: List[str]
    weak_areas: List[str]
    recommended_lessons: List[str]
    word_count: int
    flag_spam: bool
    flag_too_short: bool
    flag_copied: bool
    feedback: str
    created_at: str
    new_badges: Optional[List[NewBadge]] = None


class NotesStatusResponse(BaseModel):
    level_number: int
    has_passed_notes: bool
    latest_attempt: Optional[NotesSubmitResponse] = None
    total_attempts: int
    new_badges: Optional[List[NewBadge]] = None
