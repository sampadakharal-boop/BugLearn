from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased

from app.core.database import get_session
from app.core.security import get_current_user, get_optional_user
from app.models.leaderboard import Leaderboard
from app.models.user import User
from app.models.level_progress import LevelProgress

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/")
async def get_leaderboard(
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_optional_user)
):
    result = await session.execute(
        select(User, Leaderboard)
        .join(Leaderboard, User.id == Leaderboard.user_id)
        .order_by(Leaderboard.xp_points.desc())
        .limit(limit)
    )
    rows = result.all()

    entries = []
    for rank, (user, lb) in enumerate(rows, 1):
        lb.rank = rank
        entries.append({
            "rank": rank,
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "xp_points": lb.xp_points,
            "level_reached": lb.level_reached,
            "is_current_user": current_user is not None and current_user.id == user.id
        })

    await session.commit()

    return entries
