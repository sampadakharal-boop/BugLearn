from pydantic import BaseModel
from typing import Optional


class TopicResponse(BaseModel):
    name: str
    content: str
    emoji: str


class TaskResponse(BaseModel):
    title: str
    description: str
    expected_answer: str
    xp_reward: int


class LevelResponse(BaseModel):
    title: str
    subtitle: str
    description: str
    topics: list
    task: dict
    interview_prompt: str
    xp_reward: int


class LevelProgressResponse(BaseModel):
    level_number: int
    status: str
    interview_score: Optional[float] = None
    last_attempt_date: Optional[str] = None


class CurrentLevelResponse(BaseModel):
    level_number: int
    level_data: LevelResponse
    progress: LevelProgressResponse
    total_levels: int
