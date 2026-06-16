import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "BugLearn - ReconForge Learning System"
    VERSION: str = "2.0.0"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite+aiosqlite:///./reconforge.db"

    @property
    def is_vercel(self) -> bool:
        return "VERCEL" in os.environ
    REDIS_URL: str = "redis://localhost:6379/0"

    @property
    def is_sqlite(self) -> bool:
        return "sqlite" in self.DATABASE_URL

    SECRET_KEY: str = "buglearn-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://buglearn.vercel.app",
        "https://buglearn-*.vercel.app",
        "https://*.vercel.app",
    ]

    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"

    PASS_INTERVIEW_SCORE: int = 86
    XP_PER_LEVEL_COMPLETE: int = 100
    XP_PER_INTERVIEW_PASS: int = 50

    UPLOAD_DIR: str = "uploads/notes"
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: list[str] = [".png", ".jpg", ".jpeg", ".webp"]
    MAX_FILES_PER_SUBMISSION: int = 5

    NOTES_PASS_THRESHOLD: float = 65.0

    NOTE_BADGE_TOP_MAKER_SCORE: float = 85.0
    NOTE_BADGE_ARCHITECT_COVERAGE: float = 90.0
    NOTE_BADGE_MASTER_LEVELS: int = 3
    NOTE_BADGE_MASTER_SCORE: float = 75.0
    NOTE_BADGE_ELITE_LEVELS: int = 5
    NOTE_BADGE_ELITE_SCORE: float = 80.0

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
