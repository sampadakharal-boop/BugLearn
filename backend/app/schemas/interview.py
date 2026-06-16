from pydantic import BaseModel
from typing import List, Optional


class InterviewStartRequest(BaseModel):
    level_number: int


class ClientQuestion(BaseModel):
    id: int
    question: str
    options: List[str]


class InterviewStartResponse(BaseModel):
    attempt_id: int
    level_number: int
    total_questions: int
    questions: List[ClientQuestion]


class AnswerEntry(BaseModel):
    question_id: int
    selected_index: int


class InterviewSubmitRequest(BaseModel):
    attempt_id: int
    answers: List[int]


class WrongQuestionDetail(BaseModel):
    question_id: int
    question: str
    user_answer_index: int
    user_answer: str
    correct_answer_index: int
    correct_answer: str
    explanation: str


class InterviewSubmitResponse(BaseModel):
    total: int
    correct_count: int
    score_pct: float
    passed: bool
    pass_threshold: int
    min_score_pct: float
    weak_areas: List[str]
    recommended_lessons: List[str]
    feedback: str
    wrong_questions: List[WrongQuestionDetail]


class InterviewHistoryResponse(BaseModel):
    id: int
    level_number: int
    score: float
    total: int
    correct_count: int
    passed: bool
    feedback: Optional[str] = None
    weak_areas: Optional[str] = None
    recommended_lessons: Optional[str] = None
    created_at: str
