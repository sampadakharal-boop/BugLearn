from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.core.database import get_session
from app.core.security import get_current_user
from app.models.user import User
from app.models.level_progress import LevelProgress
from app.models.leaderboard import Leaderboard
from app.models.interview_attempt import InterviewAttempt
from app.services.level_content import LEVELS, get_level, TOTAL_LEVELS
from app.schemas.level import CurrentLevelResponse, LevelResponse, LevelProgressResponse

router = APIRouter(prefix="/levels", tags=["levels"])


async def get_progress(session: AsyncSession, user_id: int, level_number: int):
    progress = await LevelProgress.get_by_user_and_level(session, user_id, level_number)
    if not progress:
        progress = LevelProgress(
            user_id=user_id,
            level_number=level_number,
            status="locked"
        )
        session.add(progress)
        await session.commit()
        await session.refresh(progress)
    return progress


@router.get("/current", response_model=CurrentLevelResponse)
async def get_current_level(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    level_num = user.current_level
    level_data = get_level(level_num)

    if not level_data:
        raise HTTPException(status_code=404, detail="Level not found")

    progress = await get_progress(session, user.id, level_num)

    return CurrentLevelResponse(
        level_number=level_num,
        level_data=LevelResponse(**level_data),
        progress=LevelProgressResponse(
            level_number=progress.level_number,
            status=progress.status,
            interview_score=progress.interview_score,
            last_attempt_date=progress.last_attempt_date.isoformat() if progress.last_attempt_date else None
        ),
        total_levels=TOTAL_LEVELS
    )


@router.get("/{level_number}", response_model=CurrentLevelResponse)
async def get_specific_level(
    level_number: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    all_progress = await LevelProgress.get_all_for_user(session, user.id)

    if level_number > len(all_progress):
        raise HTTPException(status_code=404, detail="Level not found")

    target_progress = None
    for p in all_progress:
        if p.level_number == level_number:
            target_progress = p
            break

    if not target_progress:
        raise HTTPException(status_code=404, detail="Level progress not found")

    if level_number > user.current_level or target_progress.status == "locked":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This level is locked. Complete the current level first."
        )

    level_data = get_level(level_number)
    if not level_data:
        raise HTTPException(status_code=404, detail="Level content not found")

    return CurrentLevelResponse(
        level_number=level_number,
        level_data=LevelResponse(**level_data),
        progress=LevelProgressResponse(
            level_number=target_progress.level_number,
            status=target_progress.status,
            interview_score=target_progress.interview_score,
            last_attempt_date=target_progress.last_attempt_date.isoformat() if target_progress.last_attempt_date else None
        ),
        total_levels=TOTAL_LEVELS
    )


@router.get("/", response_model=list)
async def get_all_level_progress(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    all_progress = await LevelProgress.get_all_for_user(session, user.id)
    results = []
    for p in all_progress:
        if p.level_number > user.current_level and p.status == "locked":
            continue
        level_data = get_level(p.level_number)
        results.append({
            "level_number": p.level_number,
            "title": level_data["title"] if level_data else f"Level {p.level_number}",
            "status": p.status,
            "interview_score": p.interview_score,
            "last_attempt_date": p.last_attempt_date.isoformat() if p.last_attempt_date else None,
            "xp_reward": level_data["xp_reward"] if level_data else 0
        })
    return results


@router.get("/{level_number}/quiz")
async def get_quiz(
    level_number: int,
    user: User = Depends(get_current_user),
):
    from app.services.level_content import LEVELS
    level_data = LEVELS.get(level_number)
    if not level_data:
        raise HTTPException(status_code=404, detail="Level not found")
    quiz_data = level_data.get("quiz", [])
    safe = [{"q": item["q"], "opts": item["opts"], "id": i} for i, item in enumerate(quiz_data)]
    return {"level_number": level_number, "questions": safe}


@router.post("/{level_number}/quiz/submit")
async def submit_quiz(
    level_number: int,
    data: dict,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    from app.services.level_content import LEVELS
    from app.models.quiz_attempt import QuizAttempt

    level_data = LEVELS.get(level_number)
    if not level_data:
        raise HTTPException(status_code=404, detail="Level not found")

    quiz_data = level_data.get("quiz", [])
    answers = data.get("answers", [])
    correct = 0
    total = len(quiz_data)
    results = []

    for i, q in enumerate(quiz_data):
        user_ans = answers[i] if i < len(answers) else -1
        is_correct = user_ans == q["ans"]
        if is_correct:
            correct += 1
        results.append({"id": i, "correct": is_correct, "correct_answer": q["ans"]})

    passed = correct >= total * 0.7
    attempt = QuizAttempt(user_id=user.id, level_number=level_number, score=correct, total=total, passed=passed, answers=str(answers))
    session.add(attempt)
    await session.commit()

    return {"score": correct, "total": total, "passed": passed, "results": results}
