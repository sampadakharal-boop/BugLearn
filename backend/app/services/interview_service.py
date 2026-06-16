"""Interview service for mastery-based assessment system."""
import random
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone

from app.services.interview_questions import INTERVIEW_QUESTIONS
from app.services.level_content import LEVELS

PASS_THRESHOLD = 9  # 9 out of 10 questions correct (90%)
TOTAL_QUESTIONS_PER_INTERVIEW = 10


def select_questions(
    level_number: int,
    exclude_ids: Optional[List[int]] = None
) -> List[Dict]:
    """Select 10 random questions from the level's question bank.
    
    Args:
        level_number: The level to select questions for
        exclude_ids: Question IDs to exclude (previously used in failed attempts)
    
    Returns:
        List of 10 question dicts (without the 'correct' field for client)
    """
    bank = INTERVIEW_QUESTIONS.get(level_number, [])
    if not bank:
        return []
    
    # Filter out excluded IDs
    if exclude_ids:
        available = [q for q in bank if q["id"] not in exclude_ids]
    else:
        available = list(bank)
    
    # If we don't have enough, just use all available
    if len(available) < TOTAL_QUESTIONS_PER_INTERVIEW:
        available = list(bank)
    
    selected = random.sample(
        available,
        min(TOTAL_QUESTIONS_PER_INTERVIEW, len(available))
    )
    
    return selected


def build_client_questions(questions: List[Dict]) -> List[Dict]:
    """Remove correct answers and explanations from questions sent to client."""
    return [
        {
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
        }
        for q in questions
    ]


def evaluate_answers(
    questions: List[Dict],
    user_answers: List[int]
) -> Dict:
    """Evaluate user answers against correct answers.
    
    Args:
        questions: The full question objects (with correct answers)
        user_answers: List of selected answer indices (one per question)
    
    Returns:
        Evaluation result with score, details, and feedback
    """
    if len(user_answers) != len(questions):
        return {
            "error": f"Expected {len(questions)} answers, got {len(user_answers)}"
        }
    
    results = []
    correct_count = 0
    wrong_questions = []
    weak_topics = set()
    
    for i, (q, user_ans) in enumerate(zip(questions, user_answers)):
        is_correct = user_ans == q["correct"]
        if is_correct:
            correct_count += 1
        else:
            wrong_questions.append({
                "question_id": q["id"],
                "question": q["question"],
                "user_answer_index": user_ans,
                "user_answer": q["options"][user_ans] if 0 <= user_ans < len(q["options"]) else "No answer",
                "correct_answer_index": q["correct"],
                "correct_answer": q["options"][q["correct"]],
                "explanation": q["explanation"],
            })
            # Extract topic from explanation for weak area identification
            weak_topics.add(q["explanation"].split(":")[0].strip() if ":" in q["explanation"] else q["question"][:50])
        
        results.append({
            "question_number": i + 1,
            "question_id": q["id"],
            "correct": is_correct,
            "correct_answer_index": q["correct"],
        })
    
    passed = correct_count >= PASS_THRESHOLD
    score_pct = (correct_count / len(questions)) * 100
    
    # Generate weak areas and recommended lessons
    weak_areas = list(weak_topics) if weak_topics else []
    recommended_lessons = _get_recommended_lessons(weak_areas)
    
    # Build feedback text
    feedback = _build_feedback(correct_count, len(questions), passed, wrong_questions)
    
    return {
        "total": len(questions),
        "correct_count": correct_count,
        "score_pct": score_pct,
        "passed": passed,
        "pass_threshold": PASS_THRESHOLD,
        "min_score_pct": (PASS_THRESHOLD / TOTAL_QUESTIONS_PER_INTERVIEW) * 100,
        "results": results,
        "wrong_questions": wrong_questions,
        "weak_areas": weak_areas,
        "recommended_lessons": recommended_lessons,
        "feedback": feedback,
    }


def _get_recommended_lessons(weak_areas: List[str]) -> List[str]:
    """Map weak areas to relevant lesson topics from level content."""
    lesson_map = {
        "authentication": "Authentication & Authorization",
        "password reset": "Password Reset Security",
        "session": "Session Management",
        "cookie": "Cookie Security",
        "jwt": "JWT Security",
        "xss": "Cross-Site Scripting (XSS)",
        "cross-site scripting": "Cross-Site Scripting (XSS)",
        "sqli": "SQL Injection",
        "sql injection": "SQL Injection",
        "csrf": "CSRF Attacks",
        "idor": "IDOR / Broken Access Control",
        "access control": "IDOR / Broken Access Control",
        "ssrf": "Server-Side Request Forgery (SSRF)",
        "command injection": "Command Injection",
        "file upload": "File Upload Vulnerabilities",
        "path traversal": "Path Traversal / LFI",
        "lfi": "Path Traversal / LFI",
        "api": "API Security Testing",
        "graphql": "API Security Testing (GraphQL)",
        "business logic": "Business Logic Vulnerabilities",
        "cors": "Browser Security (CORS)",
        "csp": "Content Security Policy",
        "sop": "Same-Origin Policy",
        "recon": "Reconnaissance",
        "dns": "DNS & Subdomain Enumeration",
        "subdomain": "DNS & Subdomain Enumeration",
        "automation": "Automation for Recon",
        "hacker mindset": "Hacker Thinking",
        "oauth": "Authentication (OAuth)",
        "mfa": "Authentication (MFA/2FA)",
        "privilege escalation": "Privilege Escalation",
        "race condition": "Business Logic (Race Conditions)",
        "toctou": "Business Logic (Race Conditions)",
        "chaining": "Vulnerability Chaining",
        "report": "Report Writing",
        "capstone": "Final Capstone",
    }
    
    recommended = set()
    for area in weak_areas:
        area_lower = area.lower()
        for keyword, lesson in lesson_map.items():
            if keyword in area_lower:
                recommended.add(lesson)
                break
    
    return list(recommended)


def _build_feedback(
    correct_count: int,
    total: int,
    passed: bool,
    wrong_questions: List[Dict]
) -> str:
    """Build detailed feedback text."""
    lines = []
    
    if passed:
        lines.append(f"Congratulations! You passed with {correct_count}/{total} correct ({correct_count/total*100:.0f}%).")
    else:
        lines.append(f"You scored {correct_count}/{total}. You need {PASS_THRESHOLD}/{total} to pass.")
    
    if wrong_questions:
        lines.append(f"\nYou missed {len(wrong_questions)} question(s):")
        for wq in wrong_questions:
            lines.append(f"\n  Q: {wq['question']}")
            lines.append(f"  Your answer: {wq['user_answer']}")
            lines.append(f"  Correct answer: {wq['correct_answer']}")
            lines.append(f"  Explanation: {wq['explanation']}")
    
    lines.append(f"\nPass threshold: {PASS_THRESHOLD}/{total} correct ({PASS_THRESHOLD/total*100:.0f}%)")
    
    if passed:
        lines.append("\nYou have mastered this level! The next level is now unlocked.")
    else:
        points_needed = PASS_THRESHOLD - correct_count
        lines.append(f"\nYou need {points_needed} more correct answer(s) to pass. Review the topics above and try again.")
    
    return "\n".join(lines)
