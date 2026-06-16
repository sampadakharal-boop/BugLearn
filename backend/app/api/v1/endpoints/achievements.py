from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import get_current_user
from app.models.user import User
from app.models.achievement import Achievement

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("/")
async def get_achievements(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    achievements = await Achievement.get_for_user(session, user.id)
    return [{"id": a.id, "badge": a.badge, "title": a.title, "description": a.description, "icon": a.icon, "earned_at": a.earned_at.isoformat()} for a in achievements]
