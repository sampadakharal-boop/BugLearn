import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_session
from app.core.security import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.level_progress import LevelProgress
from app.models.interview_attempt import InterviewAttempt
from app.models.leaderboard import Leaderboard
from app.models.achievement import Achievement
from app.models.quiz_attempt import QuizAttempt
from app.models.smart_notes import SmartNotes
from app.schemas.interview import (
    InterviewStartRequest,
    InterviewStartResponse,
    ClientQuestion,
    InterviewSubmitRequest,
    InterviewSubmitResponse,
    WrongQuestionDetail,
    InterviewHistoryResponse,
)
from app.services.interview_service import (
    select_questions,
    build_client_questions,
    evaluate_answers,
)
from app.services.level_content import LEVELS, TOTAL_LEVELS

router = APIRouter(prefix="/interview", tags=["interview"])


async def unlock_achievement(session, user, badge, title, desc, icon):
    has = await Achievement.has_badge(session, user.id, badge)
    if not has:
        a = Achievement(user_id=user.id, badge=badge, title=title, description=desc, icon=icon)
        session.add(a)


async def _check_and_complete_level(session, user, level_number, progress):
    """Check if all three checkpoints are met and complete the level."""
    # Check interview passed
    if not progress.interview_score or progress.interview_score < 86:
        return False

    # Check notes approved
    if not progress.notes_approved:
        return False

    # All checkpoints met — complete level
    progress.status = "completed"
    level_data = LEVELS.get(level_number, {})
    xp_gain = level_data.get("xp_reward", 100)
    await user.add_xp(session, xp_gain)

    # Unlock next level
    next_level = level_number + 1
    if next_level <= TOTAL_LEVELS:
        next_progress = await LevelProgress.get_by_user_and_level(session, user.id, next_level)
        if next_progress:
            next_progress.status = "in_progress"
        else:
            next_progress = LevelProgress(
                user_id=user.id,
                level_number=next_level,
                status="in_progress"
            )
            session.add(next_progress)

    await user.advance_level(session)

    lb = await Leaderboard.get_by_user_id(session, user.id)
    if lb:
        lb.xp_points = user.xp_points
        lb.level_reached = user.current_level

    # Achievements
    if level_number == 1:
        await unlock_achievement(session, user, "first_blood", "First Blood", "Completed Level 1", "⚔️")
    elif level_number == 4:
        await unlock_achievement(session, user, "deep_diver", "Deep Diver", "Completed Level 4 - Recon", "🔍")
    elif level_number == 6:
        await unlock_achievement(session, user, "vuln_hunter", "Vulnerability Hunter", "Completed Level 6 - Vulns", "💉")

    return True


@router.post("/start", response_model=InterviewStartResponse)
async def start_interview(
    data: InterviewStartRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    level_number = data.level_number

    if level_number != user.current_level:
        raise HTTPException(status_code=400, detail="Can only start interview for current level")

    progress = await LevelProgress.get_by_user_and_level(session, user.id, level_number)
    if not progress:
        raise HTTPException(status_code=404, detail="Level progress not found")

    if progress.status == "completed":
        raise HTTPException(status_code=400, detail="Level already completed")

    quiz_result = await session.execute(
        select(QuizAttempt).where(
            QuizAttempt.user_id == user.id,
            QuizAttempt.level_number == level_number,
            QuizAttempt.passed == True
        ).limit(1)
    )
    quiz_passed = quiz_result.scalar_one_or_none()
    if not quiz_passed:
        raise HTTPException(status_code=400, detail="You must pass the level quiz before taking the interview")

    level_data = LEVELS.get(level_number)
    if not level_data:
        raise HTTPException(status_code=404, detail="Level not found")

    # Get previously used question IDs for this level
    previous_attempts = await InterviewAttempt.get_for_user_and_level(session, user.id, level_number)
    exclude_ids = []
    for attempt in previous_attempts:
        if attempt.questions_json:
            try:
                prev_qs = json.loads(attempt.questions_json)
                exclude_ids.extend([q["id"] for q in prev_qs])
            except (json.JSONDecodeError, KeyError, TypeError):
                pass

    # Select questions, excluding previously used ones
    selected = select_questions(level_number, exclude_ids)

    if not selected:
        # If all questions exhausted, allow reuse
        selected = select_questions(level_number)

    # Create attempt record with questions stored
    attempt = InterviewAttempt(
        user_id=user.id,
        level_number=level_number,
        score=0.0,
        total=len(selected),
        correct_count=0,
        passed=False,
        questions_json=json.dumps(selected),
        answers_json=json.dumps([]),
        weak_areas=None,
        recommended_lessons=None,
        feedback=None,
    )
    session.add(attempt)
    await session.commit()
    await session.refresh(attempt)

    client_questions = build_client_questions(selected)

    return InterviewStartResponse(
        attempt_id=attempt.id,
        level_number=level_number,
        total_questions=len(client_questions),
        questions=[ClientQuestion(**q) for q in client_questions],
    )


@router.post("/submit", response_model=InterviewSubmitResponse)
async def submit_interview(
    data: InterviewSubmitRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    attempt = await session.get(InterviewAttempt, data.attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Interview attempt not found")
    if attempt.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not your interview attempt")
    if attempt.passed:
        raise HTTPException(status_code=400, detail="Interview already passed")

    if not attempt.questions_json:
        raise HTTPException(status_code=400, detail="Interview questions not found")

    questions = json.loads(attempt.questions_json)

    if len(data.answers) != len(questions):
        raise HTTPException(
            status_code=400,
            detail=f"Expected {len(questions)} answers, got {len(data.answers)}"
        )

    result = evaluate_answers(questions, data.answers)

    # Update attempt record
    attempt.score = result["score_pct"]
    attempt.correct_count = result["correct_count"]
    attempt.total = result["total"]
    attempt.passed = result["passed"]
    attempt.answers_json = json.dumps(data.answers)
    attempt.weak_areas = json.dumps(result["weak_areas"]) if result["weak_areas"] else None
    attempt.recommended_lessons = json.dumps(result["recommended_lessons"]) if result["recommended_lessons"] else None
    attempt.feedback = result["feedback"]

    progress = await LevelProgress.get_by_user_and_level(session, user.id, attempt.level_number)
    if progress:
        progress.interview_score = result["score_pct"]
        progress.last_attempt_date = datetime.now(timezone.utc)

    if result["passed"]:
        # Try to complete the level if notes are already approved
        await _check_and_complete_level(session, user, attempt.level_number, progress)

    await session.commit()

    return InterviewSubmitResponse(
        total=result["total"],
        correct_count=result["correct_count"],
        score_pct=result["score_pct"],
        passed=result["passed"],
        pass_threshold=result["pass_threshold"],
        min_score_pct=result["min_score_pct"],
        weak_areas=result["weak_areas"],
        recommended_lessons=result["recommended_lessons"],
        feedback=result["feedback"],
        wrong_questions=[
            WrongQuestionDetail(**wq) for wq in result["wrong_questions"]
        ],
    )


@router.get("/history", response_model=list[InterviewHistoryResponse])
async def get_interview_history(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(InterviewAttempt)
        .where(InterviewAttempt.user_id == user.id)
        .order_by(InterviewAttempt.created_at.desc())
    )
    return [
        InterviewHistoryResponse(
            id=a.id,
            level_number=a.level_number,
            score=a.score,
            total=a.total,
            correct_count=a.correct_count,
            passed=a.passed,
            feedback=a.feedback,
            weak_areas=a.weak_areas,
            recommended_lessons=a.recommended_lessons,
            created_at=a.created_at.isoformat(),
        )
        for a in list(result.scalars().all())
    ]


@router.get("/prompt/{level_number}")
async def get_interview_prompt(
    level_number: int,
    user: User = Depends(get_current_user),
):
    level_data = LEVELS.get(level_number)
    if not level_data:
        raise HTTPException(status_code=404, detail="Level not found")
    return {"level_number": level_number, "prompt": level_data["interview_prompt"]}
