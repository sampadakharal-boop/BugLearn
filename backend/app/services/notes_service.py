"""Handwritten Notes evaluation service.

Evaluates learner-submitted notes (transcribed from handwritten uploads)
against level learning objectives. Scoring dimensions:
  - Concept Coverage (35%): How many key concepts are mentioned
  - Completeness (15%): Length, structure, depth
  - Clarity & Understanding (20%): Own words, analogies, explanations
  - Accuracy (10%): Correct explanations (inferred from mentions)
  - Examples & Application (10%): Real examples, bug bounty scenarios
  - Organization & Structure (10%): Sectioning, summaries, visual aids

Image authenticity is evaluated separately in note_image_service.py.
"""
import re
import math
from typing import Dict, List, Optional, Tuple

from app.services.level_content import LEVELS

PASS_THRESHOLD = 65.0  # Minimum quality score percentage to pass

# Words/phrases that indicate genuine understanding vs memorization
UNDERSTANDING_INDICATORS = [
    "because", "this means", "in other words", "for example",
    "think of it as", "imagine", "similar to", "unlike",
    "the key insight", "essentially", "fundamentally",
    "what happens is", "the reason", "this is important because",
    "in practice", "one way to", "analogy", "compare",
    "on the other hand", "specifically", "this occurs when",
    "the main difference", "in contrast", "as a result",
]

# Spam/irrelevant patterns
SPAM_PATTERNS = [
    r"(.)\1{10,}",           # Repeated characters (aaaaaa...)
    r"\b(?:lorem ipsum|asdf|qwerty|test test|blah blah)\b",
    r"(?:^|\s)(?:\. ){5,}",  # Many standalone dots
]

# Lesson content phrases that indicate direct copying
COPIED_PHRASES = [
    "In this lesson, we will explore",
    "Welcome to this lesson on",
    "By the end of this lesson",
    "Let's dive into",
    "In this section, we'll cover",
]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def extract_keywords(text: str, concept: str) -> bool:
    """Check if a concept is mentioned using flexible matching."""
    text_lower = normalize_text(text)
    concept_lower = concept.lower().strip()

    # Direct match
    if concept_lower in text_lower:
        return True

    # Handle compound concepts like "SQL injection" -> also check "sqli"
    # Handle "Cross-Site Scripting (XSS)" -> check both
    for alt in concept_lower.replace("-", " ").replace("/", " ").split():
        if len(alt) > 2 and alt in text_lower:
            return True

    # Handle abbreviations: "SQL Injection" -> "sqli" should match
    if len(concept_lower) > 3 and concept_lower[:4] in text_lower:
        return True

    return False


def extract_abbreviation_variants(concept: str) -> List[str]:
    """Generate abbreviation variants for a concept."""
    variants = [concept.lower()]
    words = concept.lower().split()
    if len(words) >= 2:
        abbr = "".join(w[0] for w in words if w[0].isalpha())
        if len(abbr) >= 2:
            variants.append(abbr)
    return variants


def check_concept_coverage(notes_text: str, level_number: int) -> Tuple[float, List[str], List[str]]:
    """Check which key concepts are covered in the notes.
    
    Returns:
        (coverage_percentage, matched_concepts, missing_concepts)
    """
    level = LEVELS.get(level_number, {})
    key_concepts = level.get("key_concepts", [])

    if not key_concepts:
        return 100.0, [], []

    matched = []
    missing = []

    for concept in key_concepts:
        found = False
        for variant in extract_abbreviation_variants(concept):
            if extract_keywords(notes_text, variant):
                found = True
                break
        if found:
            matched.append(concept)
        else:
            missing.append(concept)

    if len(key_concepts) == 0:
        return 100.0, [], []

    coverage = (len(matched) / len(key_concepts)) * 100.0
    return coverage, matched, missing


def check_organization_and_structure(notes_text: str) -> float:
    """Evaluate how well-organized the notes are.
    
    Looks for:
    - Section headers / bullet points
    - Summaries
    - Clear topic separation
    - Structured flow
    """
    text_lower = notes_text.lower()
    score = 0.0

    # Section indicators
    section_patterns = [
        r"(?:^|\n)#+\s+\w+",           # Markdown headers
        r"(?:^|\n)\w+[:\n]",            # Topic labels
        r"(?:^|\n)[-*\u2022]\s",        # Bullet points
        r"\d+\.\s+[A-Z]",               # Numbered lists
        r"summary|overview|conclusion|key.?points|takeaway|recap",
        r"introduction|background|what is|definition",
    ]
    section_count = sum(1 for p in section_patterns if re.search(p, text_lower, re.MULTILINE))
    score += min(40, section_count * 10)

    # Check for topic separation
    paragraphs = [p.strip() for p in notes_text.split("\n\n") if len(p.strip()) > 20]
    if len(paragraphs) >= 3:
        score += 20
    elif len(paragraphs) >= 1:
        score += 10

    # Check for summary or recap section
    if re.search(r"summary|recap|key.?takeaway|what i learned|conclusion", text_lower):
        score += 20

    # Check for table-like or structured content
    if re.search(r"\|.*\|.*\|", text_lower):
        score += 10
    if re.search(r"(?:^|\n)---", text_lower):
        score += 10

    return min(100, score)


def check_completeness(notes_text: str, level_number: int) -> Tuple[float, int, bool]:
    """Evaluate notes completeness based on length and structure.
    
    Returns:
        (completeness_score, word_count, is_too_short)
    """
    words = notes_text.split()
    word_count = len(words)

    level = LEVELS.get(level_number, {})
    num_topics = len(level.get("topics", []))

    # Minimum word count based on number of topics
    min_words = num_topics * 20  # ~20 words per topic minimum
    adequate_words = num_topics * 60  # ~60 words per topic for good coverage

    is_too_short = word_count < min_words

    if word_count >= adequate_words:
        score = 100.0
    elif word_count >= min_words:
        score = 50.0 + ((word_count - min_words) / (adequate_words - min_words)) * 50.0
    else:
        score = max(0, (word_count / min_words) * 50.0)

    # Bonus for structure (paragraphs, sections)
    paragraphs = [p.strip() for p in notes_text.split("\n\n") if p.strip()]
    if len(paragraphs) >= num_topics:
        score = min(100, score + 10)
    elif len(paragraphs) >= num_topics // 2:
        score = min(100, score + 5)

    return score, word_count, is_too_short


def check_clarity_and_understanding(notes_text: str) -> float:
    """Evaluate clarity and depth of understanding.
    
    Looks for indicators of genuine understanding:
    - Own words / rephrasing
    - Analogies and comparisons
    - Causal explanations (because, therefore)
    - Specific details beyond surface level
    """
    text_lower = normalize_text(notes_text)

    # Count understanding indicators
    indicator_count = sum(1 for ind in UNDERSTANDING_INDICATORS if ind in text_lower)
    indicator_score = min(100, (indicator_count / 5) * 100)  # 5+ indicators = full score

    # Bonus for analogies
    analogy_words = ["like", "as if", "similar to", "resembles", "compare", "imagine"]
    analogy_count = sum(1 for w in analogy_words if f" {w} " in f" {text_lower} ")

    # Check for definition-style explanations
    definition_patterns = [
        r"refers to",
        r"is a (type|way|method|technique|kind|form)",
        r"can be (defined|described|understood)",
        r"occurs when",
        r"happens when",
        r"means that",
        r"is used to",
        r"involves",
    ]
    definition_count = sum(1 for p in definition_patterns if re.search(p, text_lower))

    score = indicator_score * 0.6 + min(100, analogy_count * 25) * 0.2 + min(100, definition_count * 20) * 0.2

    return min(100, score)


def check_accuracy(notes_text: str, level_number: int) -> float:
    """Evaluate accuracy based on correct usage of key concepts.
    
    This is a heuristic - we check that key concepts are mentioned
    in appropriate contexts with correct surrounding terminology.
    """
    level = LEVELS.get(level_number, {})
    topics = level.get("topics", [])

    total_checks = 0
    correct_checks = 0

    for topic in topics:
        topic_name = topic.get("name", "")
        topic_content = topic.get("content", "")
        topic_lower = topic_content.lower()

        # Check if the topic's main subject is mentioned
        words_in_topic = [w for w in topic_name.lower().split() if len(w) > 3]
        if words_in_topic:
            total_checks += 1
            mentioned = any(w in normalize_text(notes_text) for w in words_in_topic)
            if mentioned:
                correct_checks += 1

        # Check for key unique terms from this topic content
        # Extract unique multi-word terms (3+ words)
        sentences = re.split(r"[.!?]", topic_content)
        for sentence in sentences[:3]:  # Check first 3 sentences
            sentence_lower = sentence.lower().strip()
            # Extract notable phrases (containing security-relevant patterns)
            notable_patterns = re.findall(
                r"(?:attack|vulnerability|security|bypass|exploit|injection|theft|"
                r"protection|defense|authentication|authorization|encryption|"
                r"protocol|cookie|session|token|access|control|risk|impact|breach)[\w\s]+?(?:is|are|can|will|may)",
                sentence_lower
            )
            for pattern in notable_patterns:
                total_checks += 1
                # Check if the idea is reflected in notes
                key_terms = pattern.split()[:4]
                if all(term in normalize_text(notes_text) for term in key_terms):
                    correct_checks += 1

    if total_checks == 0:
        return 50.0  # Neutral score if nothing to check

    return (correct_checks / total_checks) * 100.0


def check_examples_and_application(notes_text: str) -> float:
    """Evaluate use of examples, real-world applications, and practical understanding."""
    text_lower = normalize_text(notes_text)

    # Example indicators
    example_patterns = [
        r"for example",
        r"for instance",
        r"such as",
        r"e\.g\.",
        r"like",
        r"in practice",
        r"real.world",
        r"scenario",
        r"case",
        r"demonstrate",
        r"practical",
        r"imagine you",
        r"suppose",
    ]
    example_count = sum(1 for p in example_patterns if re.search(p, text_lower))
    example_score = min(100, (example_count / 4) * 100)

    # Check for specific technical details (indicating practical knowledge)
    tech_patterns = [
        r"\bhttp\b", r"\bhttps?\b", r"\b(?:GET|POST|PUT|DELETE)\b",
        r"\b(?:port|header|cookie|token)\b",
        r"\b(?:payload|inject|exploit)\b",
        r"\b(?:server|client|browser|network)\b",
        r"\b(?:code|script|function|endpoint)\b",
        r"\b(?:tool|burp|nmap|ffuf|sqlmap)\b",
    ]
    tech_count = sum(1 for p in tech_patterns if re.search(p, text_lower))
    tech_score = min(100, (tech_count / 6) * 100)

    return example_score * 0.5 + tech_score * 0.5


def detect_spam(notes_text: str) -> Tuple[bool, float]:
    """Detect spammy or low-effort content.
    
    Returns:
        (is_spam, confidence_score 0-1)
    """
    text = notes_text.strip()
    text_lower = normalize_text(text)

    spam_score = 0.0
    reasons = []

    # Check for repeated characters
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, text_lower):
            spam_score += 0.4
            reasons.append("repeated characters/patterns")

    # Check for very short length (just a few words)
    words = text.split()
    if len(words) < 10:
        spam_score += 0.3
        reasons.append("too few words")

    # Check for irrelevant common words ratio (too generic)
    generic_words = {"the", "a", "an", "is", "are", "was", "were", "it", "this", "that",
                     "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
    if len(words) > 0:
        generic_ratio = sum(1 for w in words if w.lower() in generic_words) / len(words)
        if generic_ratio > 0.8:
            spam_score += 0.2
            reasons.append("too generic")

    return spam_score > 0.3, min(spam_score, 1.0)


def detect_copied_content(notes_text: str, level_number: int) -> Tuple[bool, float]:
    """Detect if notes are directly copied from lesson content.
    
    Returns:
        (is_copied, similarity_score 0-1)
    """
    level = LEVELS.get(level_number, {})
    topics = level.get("topics", [])
    text_norm = normalize_text(notes_text)

    if not topics or len(text_norm) < 50:
        return False, 0.0

    # Check for copied lesson phrases
    copied_phrase_count = sum(1 for phrase in COPIED_PHRASES if phrase.lower() in text_norm)
    if copied_phrase_count >= 2:
        return True, 0.8

    # Check for verbatim topic content matches
    max_similarity = 0.0
    for topic in topics:
        content = topic.get("content", "")
        content_norm = normalize_text(content)

        # Extract key sentences from topic content
        sentences = re.split(r"[.!?]", content_norm)
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 30:
                continue
            # Check for long exact substring matches
            for i in range(len(sentence) - 1, 20, -1):
                substr = sentence[:i]
                if substr in text_norm:
                    similarity = len(substr) / max(len(text_norm), 1)
                    max_similarity = max(max_similarity, similarity)
                    break

    return max_similarity > 0.4, min(max_similarity, 1.0)


def generate_feedback(
    quality_score: float,
    passed: bool,
    matched_concepts: List[str],
    missing_concepts: List[str],
    word_count: int,
    is_too_short: bool,
    is_spam: bool,
    spam_confidence: float,
    is_copied: bool,
    copy_confidence: float,
    has_examples: bool,
    has_analogies: bool,
    weak_areas: List[str],
    recommended_lessons: List[str],
) -> str:
    """Generate comprehensive, educational feedback for the learner."""
    lines = []

    if passed:
        lines.append(f"Excellent work! Your handwritten notes have been approved with a quality score of {quality_score:.1f}%.")
        lines.append("Your understanding of this level's concepts is clear and well-documented in your own handwriting.")
        if quality_score >= 85:
            lines.append("Your notes are exceptional — demonstrating deep understanding and excellent organization!")
    else:
        lines.append(f"Your handwritten notes scored {quality_score:.1f}%. A score of {PASS_THRESHOLD:.0f}% or higher is needed to pass.")
        lines.append("Here's how you can improve your notes:")

    # Image authenticity feedback
    suspicious_feedback = [a for a in weak_areas if "digitally generated" in a.lower() or "photograph" in a.lower() or "clearer" in a.lower()]
    if suspicious_feedback:
        for fb in suspicious_feedback:
            lines.append(f"\n📷 {fb}")

    # Anti-gaming feedback
    if is_spam:
        lines.append(f"\nWARNING: Your submission appears to contain spam or low-effort content (confidence: {spam_confidence:.0%}).")
        lines.append("Please write genuine notes showing your understanding. Quality, not quantity, matters.")
        lines.append("Review the level topics and write about what you learned in your own words.")

    if is_copied:
        lines.append(f"\nNOTE: Your submission appears to closely match lesson content ({copy_confidence:.0%} similarity).")
        lines.append("Copying directly from lesson text prevents real learning. Please rephrase concepts in your own words.")
        lines.append("True understanding means you can explain it without looking at the source material.")

    if is_too_short and word_count > 0:
        lines.append(f"\nYour notes are quite brief ({word_count} words). Try expanding each topic with:")
        lines.append("  - A definition in your own words")
        lines.append("  - Why it matters for bug bounty hunting")
        lines.append("  - A real-world example or scenario")
        lines.append("  - Any connections to other concepts you've learned")

    # Concept coverage feedback
    if missing_concepts:
        lines.append(f"\nMissing concepts ({len(missing_concepts)}):")
        lines.append("The following important topics were not found in your notes:")
        for concept in missing_concepts:
            lines.append(f"  - {concept}")
        lines.append("\nReview these topics and add your understanding of each one.")

    if matched_concepts:
        lines.append(f"\nWell covered ({len(matched_concepts)}/{len(matched_concepts) + len(missing_concepts)} concepts):")
        lines.append(", ".join(matched_concepts[:8]))
        if len(matched_concepts) > 8:
            lines.append(f"... and {len(matched_concepts) - 8} more")

    # Understanding encouragement
    if not has_analogies and not passed:
        lines.append("\nTry using analogies to explain complex concepts.")
        lines.append('For example: "A firewall is like a bouncer at a club who checks IDs before letting people in."')
        lines.append("Analogies show deep understanding and make your notes more memorable.")

    if not has_examples and not passed:
        lines.append("\nInclude practical examples from bug bounty contexts.")
        lines.append("For instance, describe a real vulnerability you learned about and how it would be exploited.")

    # Organization encouragement
    org_feedback = [a for a in weak_areas if "Organize" in a or "diagram" in a.lower() or "summary" in a.lower()]
    if org_feedback:
        for fb in org_feedback:
            lines.append(f"\n📝 {fb}")

    # Weak areas
    if weak_areas:
        areas_not_shown = [a for a in weak_areas if a not in suspicious_feedback and a not in org_feedback]
        if areas_not_shown:
            lines.append(f"\nAreas needing improvement ({len(areas_not_shown)}):")
            for area in areas_not_shown:
                lines.append(f"  - {area}")

    # Recommended lessons
    if recommended_lessons:
        lines.append(f"\nRecommended lessons to review ({len(recommended_lessons)}):")
        for lesson in recommended_lessons:
            lines.append(f"  - {lesson}")

    if passed:
        lines.append("\nKeep up this great practice — handwritten notes are one of the most effective ways to learn!")
        if quality_score >= 80:
            lines.append("\nYour note-taking skills are exceptional! You may be eligible for special Note Excellence badges.")
    else:
        lines.append("\nDon't be discouraged! Writing good notes is a skill that improves with practice.")
        lines.append("Review the feedback above, revisit the topics you missed, and try again.")
        lines.append("Each attempt helps reinforce your understanding.")

    return "\n".join(lines)


def evaluate_notes(
    notes_text: str,
    level_number: int,
    image_analysis: Optional[Dict] = None,
) -> Dict:
    """Full evaluation of submitted handwritten notes.
    
    Args:
        notes_text: Transcribed content from handwritten notes (or empty if only images)
        level_number: The level these notes cover
        image_analysis: Optional result from note_image_service.analyze_pages()
    
    Returns a comprehensive evaluation dict matching the SmartNotes model.
    """
    # Anti-gaming detection
    is_spam, spam_confidence = detect_spam(notes_text) if notes_text.strip() else (False, 0.0)
    is_copied, copy_confidence = detect_copied_content(notes_text, level_number) if notes_text.strip() else (False, 0.0)

    # Core evaluation (use transcription if available)
    if notes_text.strip():
        concept_coverage, matched_concepts, missing_concepts = check_concept_coverage(notes_text, level_number)
        completeness_score, word_count, is_too_short = check_completeness(notes_text, level_number)
        clarity_score = check_clarity_and_understanding(notes_text)
        accuracy_score = check_accuracy(notes_text, level_number)
        examples_score = check_examples_and_application(notes_text)
        organization_score = check_organization_and_structure(notes_text)
    else:
        # No transcription; rely on image analysis only
        concept_coverage = 0.0
        matched_concepts = []
        missing_concepts = []
        completeness_score = 0.0
        word_count = 0
        is_too_short = True
        clarity_score = 0.0
        accuracy_score = 0.0
        examples_score = 0.0
        organization_score = 0.0

    # Handwriting authenticity (from image analysis)
    handwriting_score = image_analysis.get("handwriting_score", 50.0) if image_analysis else 50.0
    flag_suspicious_image = image_analysis.get("suspicious", False) if image_analysis else False

    # Structural indicators from text
    has_diagrams = bool(
        re.search(r"diagram|flowchart|chart|graph|draw|sketch|visual|arrow|->|-->|===|==>", notes_text.lower())
        or re.search(r"\n\|.+\|\n\|[-|]+\|\n\|", notes_text)  # Markdown table
    ) if notes_text.strip() else False
    has_analogies = bool(
        re.search(r"like |as if|similar to|imagine|analogy|compare|resembles|think of", notes_text.lower())
    ) if notes_text.strip() else False
    has_examples = bool(
        re.search(r"for example|for instance|such as|e\.g\.|in practice|real.world|scenario", notes_text.lower())
    ) if notes_text.strip() else False
    has_summary = bool(
        re.search(r"summary|recap|takeaway|conclusion|what i learned|key point", notes_text.lower())
    ) if notes_text.strip() else False

    # Calculate overall quality score (weighted dimensions)
    # Image authenticity provides baseline; text content scales it
    if notes_text.strip():
        quality_score = (
            concept_coverage * 0.35 +
            completeness_score * 0.15 +
            clarity_score * 0.20 +
            accuracy_score * 0.10 +
            examples_score * 0.10 +
            organization_score * 0.10
        )
        # Handwriting score bonus (up to +10 for verified handwritten)
        if handwriting_score >= 70:
            quality_score += 5
        elif handwriting_score >= 50:
            quality_score += 2
    else:
        # Only images uploaded; quality is based on handwriting analysis
        quality_score = handwriting_score * 0.5

    # Penalties for anti-gaming flags
    if is_spam:
        quality_score *= 0.3
    if is_copied:
        quality_score *= 0.5
    if is_too_short and word_count < 20 and not image_analysis:
        quality_score *= 0.4
    if flag_suspicious_image:
        quality_score *= 0.6

    quality_score = round(min(100, max(0, quality_score)), 1)
    passed = (
        quality_score >= PASS_THRESHOLD
        and not is_spam
        and not is_copied
        and not is_too_short
        and not flag_suspicious_image
    )

    # Generate weak areas
    weak_areas = []
    if concept_coverage < 50 and notes_text.strip():
        weak_areas.append("Concept coverage is low — many key topics are missing")
    if completeness_score < 50 and notes_text.strip():
        weak_areas.append("Notes are too brief — expand each topic with more detail")
    if clarity_score < 40 and notes_text.strip():
        weak_areas.append("Try explaining concepts in your own words rather than listing terms")
    if accuracy_score < 50 and notes_text.strip():
        weak_areas.append("Some concepts may be incorrectly explained — review the lesson content")
    if examples_score < 40 and notes_text.strip():
        weak_areas.append("Include more real-world examples and bug bounty scenarios")
    if organization_score < 40 and notes_text.strip():
        weak_areas.append("Organize notes with clear sections, bullet points, or summaries")
    if handwriting_score < 50:
        weak_areas.append("Upload clearer photos of your handwritten notes for better evaluation")
    if not has_diagrams and notes_text.strip():
        weak_areas.append("Consider adding diagrams or flowcharts to visualize concepts")
    if not has_summary and notes_text.strip():
        weak_areas.append("Add a summary section to reinforce key takeaways")
    if is_spam:
        weak_areas.append("Submission flagged as low-effort — write genuine, thoughtful notes")
    if is_copied:
        weak_areas.append("Content appears to be copied — rewrite in your own words")
    if is_too_short:
        weak_areas.append("Notes are too brief to demonstrate understanding")
    if flag_suspicious_image:
        weak_areas.append("Uploaded images appear digitally generated — take photos of actual handwritten notes")

    # Determine has_examples and has_analogies for feedback
    has_examples = any(
        pat in normalize_text(notes_text)
        for pat in ["for example", "for instance", "such as", "e.g.", "in practice"]
    )
    has_analogies = any(
        word in normalize_text(notes_text)
        for word in ["like ", "as if", "similar to", "imagine", "analogy"]
    )

    # Map weak areas to recommended lessons
    recommended_lessons = []
    lesson_map = {
        "concept coverage": "Review all topics in this level",
        "too brief": "Study each topic section in detail",
        "own words": "Practice explaining concepts without looking at the lesson",
        "real-world": "Look at real bug bounty reports for practical examples",
        "diagram": "Add flowcharts or diagrams to visualize attack flows",
        "summary": "End notes with a summary of key takeaways",
    }
    for area in weak_areas:
        for keyword, lesson in lesson_map.items():
            if keyword in area.lower():
                if lesson not in recommended_lessons:
                    recommended_lessons.append(lesson)

    # If specific missing concepts, recommend revisiting
    if missing_concepts:
        recommended_lessons.append(f"Revisit: {', '.join(missing_concepts[:5])}")

    feedback = generate_feedback(
        quality_score=quality_score,
        passed=passed,
        matched_concepts=matched_concepts,
        missing_concepts=missing_concepts,
        word_count=word_count,
        is_too_short=is_too_short,
        is_spam=is_spam,
        spam_confidence=spam_confidence,
        is_copied=is_copied,
        copy_confidence=copy_confidence,
        has_examples=has_examples,
        has_analogies=has_analogies,
        weak_areas=weak_areas,
        recommended_lessons=recommended_lessons,
    )

    return {
        "quality_score": quality_score,
        "concept_coverage": round(concept_coverage, 1),
        "clarity_score": round(clarity_score, 1),
        "accuracy_score": round(accuracy_score, 1),
        "completeness_score": round(completeness_score, 1),
        "examples_score": round(examples_score, 1),
        "organization_score": round(organization_score, 1),
        "handwriting_score": round(handwriting_score, 1),
        "passed": passed,
        "pass_threshold": PASS_THRESHOLD,
        "matched_concepts": matched_concepts,
        "missing_concepts": missing_concepts,
        "weak_areas": weak_areas,
        "recommended_lessons": recommended_lessons,
        "word_count": word_count,
        "flag_spam": is_spam,
        "flag_too_short": is_too_short,
        "flag_copied": is_copied,
        "flag_suspicious_image": flag_suspicious_image,
        "has_diagrams": has_diagrams,
        "has_analogies": has_analogies,
        "has_examples": has_examples,
        "has_summary": has_summary,
        "organization_score": round(organization_score, 1),
        "feedback": feedback,
    }


def check_note_excellence_badges(notes: List[Dict]) -> List[Dict]:
    """Check if a user's notes qualify for Note Excellence badges.
    
    Args:
        notes: List of SmartNotes dicts (with quality_score, concept_coverage, etc.)
    
    Returns:
        List of badge dicts with badge name, title, description, and icon
    """
    badges = []
    
    if not notes:
        return badges
    
    # Top Note Maker: quality_score >= 85 on any single note
    best_score = max(n.get("quality_score", 0) for n in notes)
    if best_score >= 85:
        badges.append({
            "badge": "top_note_maker",
            "title": "Top Note Maker",
            "description": "Created exceptional handwritten notes with outstanding quality (85%+)",
            "icon": "📝",
        })
    
    # Knowledge Architect: concept_coverage >= 90 on any note
    best_coverage = max(n.get("concept_coverage", 0) for n in notes)
    if best_coverage >= 90:
        badges.append({
            "badge": "knowledge_architect",
            "title": "Knowledge Architect",
            "description": "Demonstrated comprehensive concept coverage (90%+) in handwritten notes",
            "icon": "🏛️",
        })
    
    # Master Note Taker: quality_score >= 75 on 3+ different levels
    high_quality_levels = set()
    for n in notes:
        if n.get("quality_score", 0) >= 75:
            high_quality_levels.add(n.get("level_number"))
    if len(high_quality_levels) >= 3:
        badges.append({
            "badge": "master_note_taker",
            "title": "Master Note Taker",
            "description": f"Created high-quality handwritten notes across {len(high_quality_levels)} different levels",
            "icon": "✍️",
        })
    
    # Elite Learner: quality_score >= 80 on 5+ different levels
    elite_levels = set()
    for n in notes:
        if n.get("quality_score", 0) >= 80:
            elite_levels.add(n.get("level_number"))
    if len(elite_levels) >= 5:
        badges.append({
            "badge": "elite_learner",
            "title": "Elite Learner",
            "description": f"Mastered note-taking across {len(elite_levels)} levels with scores of 80%+",
            "icon": "👑",
        })
    
    return badges
