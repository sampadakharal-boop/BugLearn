from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    levels,
    interview,
    leaderboard,
    achievements,
    notes,
)

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(levels.router)
router.include_router(interview.router)
router.include_router(leaderboard.router)
router.include_router(achievements.router)
router.include_router(notes.router)


@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "BugLearn - ReconForge Learning System", "version": "2.0.0"}
