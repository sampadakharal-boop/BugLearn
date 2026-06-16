from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.models.user import User
from app.models.level_progress import LevelProgress
from app.models.leaderboard import Leaderboard
from app.models.interview_attempt import InterviewAttempt
from app.schemas.user import UserRegister, UserLogin, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register(data: UserRegister, session: AsyncSession = Depends(get_session)):
    existing = await User.get_by_email(session, data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        current_level=1,
        xp_points=0
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    for level_num in range(1, 8):
        progress = LevelProgress(
            user_id=user.id,
            level_number=level_num,
            status="in_progress" if level_num == 1 else "locked"
        )
        session.add(progress)
    await session.commit()

    lb_entry = Leaderboard(user_id=user.id, xp_points=0, level_reached=1)
    session.add(lb_entry)
    await session.commit()

    access_token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            current_level=user.current_level,
            xp_points=user.xp_points,
            created_at=user.created_at.isoformat()
        )
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, session: AsyncSession = Depends(get_session)):
    user = await User.get_by_email(session, data.email)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            current_level=user.current_level,
            xp_points=user.xp_points,
            created_at=user.created_at.isoformat()
        )
    )


@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        current_level=user.current_level,
        xp_points=user.xp_points,
        created_at=user.created_at.isoformat()
    )
