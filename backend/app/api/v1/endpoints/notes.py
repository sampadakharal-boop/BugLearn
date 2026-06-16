import json
from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_session
from app.core.security import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.level_progress import LevelProgress
from app.models.smart_notes import SmartNotes
from app.models.leaderboard import Leaderboard
from app.models.achievement import Achievement
from app.schemas.notes import (
    NotesSubmitResponse,
    NotesScoreBreakdown,
    NotesStatusResponse,
)
from app.services.notes_service import evaluate_notes, check_note_excellence_badges
from app.services.note_image_service import validate_image, save_image, analyze_pages
from app.services.level_content import LEVELS, TOTAL_LEVELS

router = APIRouter(prefix="/notes", tags=["notes"])


async def unlock_achievement(session, user, badge, title, desc, icon):
    has = await Achievement.has_badge(session, user.id, badge)
    if not has:
        a = Achievement(user_id=user.id, badge=badge, title=title, description=desc, icon=icon)
        session.add(a)


async def _complete_level(session, user, progress):
    """Mark level completed after all checkpoints passed."""
    progress.status = "completed"
    level_data = LEVELS.get(progress.level_number, {})
    xp_gain = level_data.get("xp_reward", 100)
    await user.add_xp(session, xp_gain)

    next_level = progress.level_number + 1
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

    level_number = progress.level_number
    if level_number == 1:
        await unlock_achievement(session, user, "first_blood", "First Blood", "Completed Level 1", "⚔️")
    elif level_number == 4:
        await unlock_achievement(session, user, "deep_diver", "Deep Diver", "Completed Level 4 - Recon", "🔍")
    elif level_number == 6:
        await unlock_achievement(session, user, "vuln_hunter", "Vulnerability Hunter", "Completed Level 6 - Vulns", "💉")


@router.post("/submit", response_model=NotesSubmitResponse)
async def submit_notes(
    level_number: int = Form(...),
    files: List[UploadFile] = File(...),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    if level_number < 1:
        raise HTTPException(status_code=400, detail="Invalid level number")

    level_data = LEVELS.get(level_number)
    if not level_data:
        raise HTTPException(status_code=404, detail="Level not found")

    if not files:
        raise HTTPException(status_code=400, detail="At least one image file is required")

    if len(files) > settings.MAX_FILES_PER_SUBMISSION:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {settings.MAX_FILES_PER_SUBMISSION} files allowed"
        )

    progress = await LevelProgress.get_by_user_and_level(session, user.id, level_number)
    if not progress:
        raise HTTPException(status_code=404, detail="Level progress not found")

    # Check if already passed notes for this level
    existing_passed = await SmartNotes.get_passed_for_user_and_level(session, user.id, level_number)
    if existing_passed:
        raise HTTPException(status_code=400, detail="Notes already approved for this level")

    # Validate and save uploaded images
    saved_paths = []
    file_bytes_list = []
    for f in files:
        contents = await f.read()
        valid, err = validate_image(contents, f.filename or "image.jpg")
        if not valid:
            raise HTTPException(status_code=400, detail=f"Invalid file '{f.filename}': {err}")
        path = save_image(contents, f.filename or "image.jpg", user.id)
        saved_paths.append(path)
        file_bytes_list.append(contents)

    # Analyze images for handwriting authenticity
    image_analysis = analyze_pages(file_bytes_list, [f.filename or f"page_{i}.jpg" for i, f in enumerate(files)])

    # Evaluate notes (image-only, no text transcription)
    result = evaluate_notes("", level_number, image_analysis=image_analysis)

    # Update level progress
    progress.notes_score = result["quality_score"]
    progress.notes_approved = result["passed"]
    progress.last_attempt_date = datetime.now(timezone.utc)

    notes_entry = SmartNotes(
        user_id=user.id,
        level_number=level_number,
        notes_text="",
        quality_score=result["quality_score"],
        concept_coverage=result["concept_coverage"],
        clarity_score=result["clarity_score"],
        accuracy_score=result["accuracy_score"],
        completeness_score=result["completeness_score"],
        examples_score=result["examples_score"],
        handwriting_score=result["handwriting_score"],
        page_count=image_analysis.get("page_count", 1),
        passed=result["passed"],
        feedback=result["feedback"],
        missing_concepts=json.dumps(result["missing_concepts"]),
        matched_concepts=json.dumps(result["matched_concepts"]),
        weak_areas=json.dumps(result["weak_areas"]),
        recommended_lessons=json.dumps(result["recommended_lessons"]),
        word_count=0,
        flag_spam=result["flag_spam"],
        flag_too_short=result["flag_too_short"],
        flag_copied=result["flag_copied"],
        flag_suspicious_image=result["flag_suspicious_image"],
        image_paths=json.dumps(saved_paths),
        image_analysis_json=json.dumps(image_analysis),
        has_diagrams=result.get("has_diagrams", False),
        has_analogies=result.get("has_analogies", False),
        has_examples=result.get("has_examples", False),
        has_summary=result.get("has_summary", False),
        organization_score=result.get("organization_score", 0.0),
    )
    session.add(notes_entry)

    # Check for note excellence badges if notes passed
    new_badges = []
    if result["passed"]:
        all_user_notes = await SmartNotes.get_all_for_user(session, user.id)
        notes_dicts = []
        for n in all_user_notes:
            notes_dicts.append({
                "quality_score": n.quality_score,
                "concept_coverage": n.concept_coverage,
                "level_number": n.level_number,
            })
        eligible_badges = check_note_excellence_badges(notes_dicts)
        for badge_info in eligible_badges:
            await unlock_achievement(
                session, user,
                badge_info["badge"],
                badge_info["title"],
                badge_info["description"],
                badge_info["icon"],
            )
            new_badges.append(badge_info)

    # Award XP bonus for note quality
    if result["passed"]:
        note_xp = int(result["quality_score"])
        await user.add_xp(session, note_xp)
        lb = await Leaderboard.get_by_user_id(session, user.id)
        if lb:
            lb.xp_points = user.xp_points

    # If notes pass and interview already passed, complete the level
    if result["passed"] and progress.interview_score and progress.interview_score >= 86:
        await _complete_level(session, user, progress)

    await session.commit()
    await session.refresh(notes_entry)

    return NotesSubmitResponse(
        id=notes_entry.id,
        level_number=notes_entry.level_number,
        quality_score=notes_entry.quality_score,
        passed=notes_entry.passed,
        pass_threshold=result["pass_threshold"],
        score_breakdown=NotesScoreBreakdown(
            concept_coverage=notes_entry.concept_coverage,
            clarity_score=notes_entry.clarity_score,
            accuracy_score=notes_entry.accuracy_score,
            completeness_score=notes_entry.completeness_score,
            examples_score=notes_entry.examples_score,
        ),
        matched_concepts=result["matched_concepts"],
        missing_concepts=result["missing_concepts"],
        weak_areas=result["weak_areas"],
        recommended_lessons=result["recommended_lessons"],
        word_count=0,
        flag_spam=notes_entry.flag_spam,
        flag_too_short=notes_entry.flag_too_short,
        flag_copied=notes_entry.flag_copied,
        feedback=notes_entry.feedback or "",
        created_at=notes_entry.created_at.isoformat(),
        new_badges=new_badges if new_badges else None,
    )


@router.get("/status/{level_number}", response_model=NotesStatusResponse)
async def get_notes_status(
    level_number: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    if level_number < 1:
        raise HTTPException(status_code=400, detail="Invalid level number")

    level_data = LEVELS.get(level_number)
    if not level_data:
        raise HTTPException(status_code=404, detail="Level not found")

    all_attempts = await SmartNotes.get_for_user_and_level(session, user.id, level_number)
    passed_notes = await SmartNotes.get_passed_for_user_and_level(session, user.id, level_number)
    latest = all_attempts[0] if all_attempts else None

    latest_response = None
    if latest:
        try:
            missing = json.loads(latest.missing_concepts) if latest.missing_concepts else []
            matched = json.loads(latest.matched_concepts) if latest.matched_concepts else []
            weak = json.loads(latest.weak_areas) if latest.weak_areas else []
            rec = json.loads(latest.recommended_lessons) if latest.recommended_lessons else []
        except (json.JSONDecodeError, TypeError):
            missing = []
            matched = []
            weak = []
            rec = []

        latest_response = NotesSubmitResponse(
            id=latest.id,
            level_number=latest.level_number,
            quality_score=latest.quality_score,
            passed=latest.passed,
            pass_threshold=65.0,
            score_breakdown=NotesScoreBreakdown(
                concept_coverage=latest.concept_coverage,
                clarity_score=latest.clarity_score,
                accuracy_score=latest.accuracy_score,
                completeness_score=latest.completeness_score,
                examples_score=latest.examples_score,
            ),
            matched_concepts=matched,
            missing_concepts=missing,
            weak_areas=weak,
            recommended_lessons=rec,
            word_count=latest.word_count,
            flag_spam=latest.flag_spam,
            flag_too_short=latest.flag_too_short,
            flag_copied=latest.flag_copied,
            feedback=latest.feedback or "",
            created_at=latest.created_at.isoformat(),
        )

    return NotesStatusResponse(
        level_number=level_number,
        has_passed_notes=passed_notes is not None,
        latest_attempt=latest_response,
        total_attempts=len(all_attempts),
    )
