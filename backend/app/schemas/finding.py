from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class FindingResponse(BaseModel):
    id: int
    type: str
    severity: str
    title: str
    description: Optional[str] = None
    technical_detail: Optional[str] = None
    remediation: Optional[str] = None
    cvss_score: Optional[float] = None
    cve_id: Optional[str] = None
    evidence: dict
    is_false_positive: bool
    is_bookmarked: bool
    created_at: datetime
    source: Optional[str] = None

    class Config:
        from_attributes = True


class FindingListResponse(BaseModel):
    findings: list[FindingResponse]
    total: int
    page: int
    per_page: int


class FindingUpdate(BaseModel):
    is_false_positive: Optional[bool] = None
    is_bookmarked: Optional[bool] = None
