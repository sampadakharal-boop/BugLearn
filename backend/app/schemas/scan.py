from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field


class ScanCreate(BaseModel):
    target_id: int
    scan_type: str = Field(default="full", pattern="^(full|quick|subdomain|port|tech|endpoint|js)$")
    name: Optional[str] = None


class ScanProgress(BaseModel):
    scan_id: int
    status: str
    progress: float
    modules_completed: list[str]
    modules_pending: list[str]
    current_module: Optional[str] = None
    subdomains_count: int = 0
    endpoints_count: int = 0
    findings_count: int = 0
    ports_count: int = 0
    tech_count: int = 0


class ScanResponse(BaseModel):
    id: int
    user_id: int
    target_id: int
    name: Optional[str] = None
    status: str
    progress: float
    scan_type: str
    subdomains_count: int
    endpoints_count: int
    findings_count: int
    ports_count: int
    tech_count: int
    modules_completed: list
    modules_pending: list
    errors: list
    results: dict = {}
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ScanListResponse(BaseModel):
    scans: list[ScanResponse]
    total: int
    page: int
    per_page: int


class ScanResultsResponse(BaseModel):
    scan_id: int
    target_id: int
    target_domain: str
    scan_type: str
    status: str
    progress: float
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    results: dict
    findings: list[dict]
    subdomains_count: int
    ports_count: int
    tech_count: int
    endpoints_count: int
    findings_count: int
    errors: list[str]
