from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TargetCreate(BaseModel):
    domain: str = Field(..., description="Domain to scan")
    organization: Optional[str] = None
    description: Optional[str] = None
    tags: list[str] = []


class TargetResponse(BaseModel):
    id: int
    user_id: int
    domain: str
    organization: Optional[str] = None
    description: Optional[str] = None
    tags: list
    is_active: bool
    risk_score: int
    asset_count: int
    created_at: datetime
    updated_at: datetime
    last_scanned_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TargetListResponse(BaseModel):
    targets: list[TargetResponse]
    total: int
    page: int
    per_page: int
