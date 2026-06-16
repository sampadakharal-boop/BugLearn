import re
import json
from typing import Dict, Any, List


def normalize(text: str) -> str:
    return text.lower().strip()


def extract_keywords(text: str) -> set:
    tokens = re.findall(r'\b[a-zA-Z]{2,}\b', normalize(text))
    return set(tokens)


def score_technical_correctness(transcript: str, key_concepts: List[str]) -> tuple:
    """Score 0-40 based on technical accuracy"""
    normalized = normalize(transcript)
    matched = 0
    total = len(key_concepts)
    missing = []

    for concept in key_concepts:
        if concept.lower() in normalized:
            matched += 1
        else:
            missing.append(concept)

    if total == 0:
        return 0, []

    score = int((matched / total) * 40)

    return min(score, 40), missing


def score_concept_completeness(transcript: str, key_concepts: List[str]) -> tuple:
    """Score 0-25 based on how many concepts are meaningfully explained"""
    normalized = normalize(transcript)
    sentences = [s.strip() for s in re.split(r'[.!?]', normalized) if s.strip()]

    if not sentences:
        return 0, []

    words = normalized.split()
    unique_words = len(set(words))
    sentence_count = len(sentences)

    completeness = 0
    if sentence_count >= 3:
        completeness += 5
    if unique_words >= 20:
        completeness += 5
    if unique_words >= 40:
        completeness += 5

    concept_density = sum(1 for c in key_concepts if c.lower() in normalized)
    if concept_density >= len(key_concepts) * 0.7:
        completeness += 10
    elif concept_density >= len(key_concepts) * 0.4:
        completeness += 5
    else:
        completeness += 0

    return min(completeness, 25), []


def score_clarity(transcript: str) -> int:
    """Score 0-20 based on explanation clarity"""
    normalized = normalize(transcript)
    sentences = [s.strip() for s in re.split(r'[.!?]', normalized) if s.strip()]
    words = normalized.split()

    if not sentences:
        return 0

    clarity = 0

    avg_sentence_length = len(words) / max(len(sentences), 1)
    if 8 <= avg_sentence_length <= 25:
        clarity += 5

    if len(sentences) >= 2:
        clarity += 5

    structure_words = ["first", "second", "then", "because", "therefore", "however", "for example", "specifically", "additionally", "in other words", "such as", "also"]
    has_structure = any(word in normalized for word in structure_words)
    if has_structure:
        clarity += 5

    if len(words) >= 30:
        clarity += 5

    return min(clarity, 20)


def score_real_world_understanding(transcript: str, level_number: int) -> int:
    """Score 0-15 based on real-world examples and practical understanding"""

    normalized = normalize(transcript)
    rw = 0

    real_world_indicators = [
        "example", "real world", "practical", "actual", "scenario",
        "like when", "for instance", "in practice", "commonly",
        "happen", "attack", "vulnerability", "exploit", "impact",
        "bug", "bounty", "reported", "found", "case"
    ]

    found = sum(1 for word in real_world_indicators if word in normalized)
    if found >= 5:
        rw += 7
    elif found >= 3:
        rw += 4
    elif found >= 1:
        rw += 2

    technical_terms = [
        "server", "client", "browser", "database", "api", "request",
        "response", "header", "cookie", "token", "jwt", "xss",
        "sqli", "csrf", "idor", "authentication", "session",
        "encryption", "dns", "http", "https", "protocol"
    ]

    tech_found = sum(1 for t in technical_terms if t in normalized)
    if tech_found >= 5:
        rw += 5
    elif tech_found >= 3:
        rw += 3

    if "http" in normalized and "https" in normalized:
        rw += 3

    return min(rw, 15)


def evaluate_interview(transcript: str, level_number: int) -> Dict[str, Any]:
    from app.services.level_content import LEVELS

    level_data = LEVELS.get(level_number)
    if not level_data:
        return {
            "score": 0,
            "passed": False,
            "missing_points": ["Level not found"],
            "feedback": "Invalid level number."
        }

    key_concepts = level_data.get("key_concepts", [])

    tech_score, tech_missing = score_technical_correctness(transcript, key_concepts)
    concept_score, _ = score_concept_completeness(transcript, key_concepts)
    clarity_score = score_clarity(transcript)
    real_world_score = score_real_world_understanding(transcript, level_number)

    total_score = tech_score + concept_score + clarity_score + real_world_score
    passed = total_score >= 86

    all_missing = tech_missing
    if concept_score < 15:
        all_missing.append("Need more complete coverage of key concepts")
    if clarity_score < 10:
        all_missing.append("Explanation could be clearer and better structured")
    if real_world_score < 10:
        all_missing.append("Include real-world examples or practical scenarios")

    tech_pct = (tech_score / 40) * 100 if tech_score > 0 else 0
    concept_pct = (concept_score / 25) * 100 if concept_score > 0 else 0
    clarity_pct = (clarity_score / 20) * 100 if clarity_score > 0 else 0
    rw_pct = (real_world_score / 15) * 100 if real_world_score > 0 else 0

    feedback_parts = []
    if passed:
        feedback_parts.append(f"Excellent work! You scored {total_score}/100, passing the interview.")
    else:
        feedback_parts.append(f"You scored {total_score}/100. The minimum passing score is 86. Keep studying and try again.")

    feedback_parts.append(f"Technical accuracy: {tech_score}/40 ({tech_pct:.0f}%)")
    feedback_parts.append(f"Concept completeness: {concept_score}/25 ({concept_pct:.0f}%)")
    feedback_parts.append(f"Clarity: {clarity_score}/20 ({clarity_pct:.0f}%)")
    feedback_parts.append(f"Real-world understanding: {real_world_score}/15 ({rw_pct:.0f}%)")

    feedback = ". ".join(feedback_parts)

    return {
        "score": total_score,
        "passed": passed,
        "missing_points": all_missing[:8],
        "feedback": feedback
    }
