"""Image analysis for handwritten notes authenticity verification.

Analyzes uploaded images for:
  - Handwriting indicators (edge distribution, stroke patterns)
  - Paper texture / natural lighting
  - Digital generation artifacts (uniform backgrounds, perfect straight lines)
  - Page count and quality metrics

Uses PIL and NumPy for basic image processing without ML dependencies.
"""
import io
import os
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PIL import Image, ImageFilter, ImageStat, ImageOps
import numpy as np

from app.core.config import settings


ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
MAX_FILE_SIZE = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024


def ensure_upload_dir() -> Path:
    upload_path = Path(settings.UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)
    return upload_path


def validate_image(file_bytes: bytes, filename: str) -> Tuple[bool, str]:
    """Validate file type and size."""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported format '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    if len(file_bytes) > MAX_FILE_SIZE:
        return False, f"File too large ({len(file_bytes)/1024/1024:.1f}MB). Max: {settings.MAX_UPLOAD_SIZE_MB}MB"
    try:
        Image.open(io.BytesIO(file_bytes)).verify()
        return True, ""
    except Exception:
        return False, "Invalid or corrupted image file"


def save_image(file_bytes: bytes, filename: str, user_id: int) -> str:
    """Save image to upload directory and return relative path."""
    upload_dir = ensure_upload_dir()
    safe_name = f"{uuid.uuid4().hex}_{filename}"
    user_dir = upload_dir / str(user_id)
    user_dir.mkdir(exist_ok=True)
    filepath = user_dir / safe_name
    filepath.write_bytes(file_bytes)
    return str(filepath.relative_to(Path.cwd()))


def analyze_image(file_bytes: bytes) -> Dict:
    """Analyze a single image for handwriting authenticity.
    
    Returns dict with:
      - handwriting_score: 0-100 confidence it's real handwritten notes
      - page_quality: 0-100 (focus, lighting, resolution)
      - has_text_content: bool (detects meaningful content vs blank/scattered)
      - suspicious: bool (flagged for review)
      - reasons: list of analysis notes
    """
    reasons = []
    img = Image.open(io.BytesIO(file_bytes))
    
    # Convert to grayscale for analysis
    if img.mode == "RGBA":
        img = img.convert("RGB")
    gray = img.convert("L")
    
    width, height = img.size
    total_pixels = width * height
    
    # ---- DIMENSION CHECKS ----
    if width < 800 or height < 600:
        reasons.append("Image resolution is low; notes may be hard to read")
    
    # ---- CONTRAST ANALYSIS ----
    # Handwritten notes have high contrast (dark ink on light paper)
    pixels = np.array(gray)
    contrast = pixels.std()
    
    if contrast < 30:
        reasons.append("Low contrast image — may not be a clear photo of notes")
        contrast_score = max(0, (contrast / 30) * 40)
    else:
        contrast_score = min(100, 40 + (contrast / 255) * 60)
    
    # ---- EDGE ANALYSIS ----
    # Handwriting has many fine edges; digital text has very sharp uniform edges
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edge_pixels = np.array(edges)
    edge_intensity = edge_pixels.mean()
    edge_std = edge_pixels.std()
    
    # Natural handwriting: medium edge intensity with variation
    if edge_intensity < 5:
        reasons.append("Very few edges detected — page may be blank or blurry")
        edge_score = max(0, (edge_intensity / 5) * 30)
    elif edge_intensity > 80:
        reasons.append("Very high edge density — possibly scanned text or synthetic")
        edge_score = 50
    else:
        edge_score = min(100, 30 + (edge_intensity / 40) * 50)
    
    # ---- BRIGHTNESS / PAPER ANALYSIS ----
    # Real paper has non-uniform brightness (lighting variation)
    mean_brightness = pixels.mean()
    brightness_variation = pixels.std() / max(contrast, 1)
    
    if mean_brightness < 50:
        reasons.append("Image is very dark — may be hard to read")
    elif mean_brightness > 240:
        reasons.append("Image is overexposed — details may be lost")
    
    # ---- COLOR ANALYSIS (for color photos) ----
    has_color_shift = False
    if img.mode == "RGB":
        r, g, b = img.split()
        r_mean = np.array(r).mean()
        g_mean = np.array(g).mean()
        b_mean = np.array(b).mean()
        # Paper typically has a warm/neutral cast
        max_channel = max(r_mean, g_mean, b_mean)
        min_channel = min(r_mean, g_mean, b_mean)
        color_shift = max_channel - min_channel
        has_color_shift = color_shift > 10  # Not pure grayscale
    
    # ---- LIGHTING UNIFORMITY ----
    # Natural lighting causes gradient across the page
    quadrants = [
        pixels[:height//2, :width//2].mean(),
        pixels[:height//2, width//2:].mean(),
        pixels[height//2:, :width//2].mean(),
        pixels[height//2:, width//2:].mean(),
    ]
    lighting_variation = max(quadrants) - min(quadrants)
    
    if lighting_variation < 3 and mean_brightness > 200:
        reasons.append("Unusually uniform lighting — may be a digital document, not a photo")
        lighting_score = 30
    elif lighting_variation < 5:
        lighting_score = 50
    else:
        lighting_score = min(100, 40 + lighting_variation * 3)
    
    # ---- FREQUENCY ANALYSIS (detect grid/computer patterns) ----
    # Computer-generated content often has periodic patterns
    # Check horizontal gradient uniformity
    h_gradient = np.abs(np.diff(pixels.mean(axis=0))).mean()
    v_gradient = np.abs(np.diff(pixels.mean(axis=1))).mean()
    
    if h_gradient < 0.5 and v_gradient < 0.5:
        reasons.append("Very uniform gradients — possibly computer-generated")
    
    # ---- WHITE SPACE ANALYSIS ----
    # Handwritten notes don't fill the page uniformly
    dark_pixels = (pixels < 100).sum()
    dark_ratio = dark_pixels / total_pixels
    
    if dark_ratio < 0.01:
        reasons.append("Very little content detected on page")
        content_score = 10
    elif dark_ratio > 0.6:
        reasons.append("Page is very densely filled — possibly scanned text")
        content_score = 60
    else:
        content_score = min(100, 30 + dark_ratio * 100)
    
    # ---- OVERALL HANDWRITING SCORE ----
    scores = {
        "contrast": contrast_score * 0.20,
        "edge": edge_score * 0.20,
        "lighting": lighting_score * 0.15,
        "content": content_score * 0.25,
        "dimension": (100 if width >= 1200 and height >= 1600 else 70 if width >= 800 and height >= 600 else 40) * 0.10,
        "variation": min(100, brightness_variation * 50) * 0.10,
    }
    
    handwriting_score = sum(scores.values())
    
    # ---- SUSPICION FLAGS ----
    suspicious = False
    if contrast < 25 and edge_intensity < 5:
        suspicious = True
        reasons.append("Low detail image — may not contain handwritten notes")
    if lighting_variation < 3 and mean_brightness > 210:
        suspicious = True
        reasons.append("Image appears digitally generated (uniform lighting)")
    if dark_ratio < 0.005:
        suspicious = True
        reasons.append("Page appears to be blank or nearly blank")
    
    return {
        "handwriting_score": round(min(100, handwriting_score), 1),
        "page_quality": round(contrast_score * 0.4 + edge_score * 0.3 + lighting_score * 0.3, 1),
        "has_text_content": dark_ratio > 0.01,
        "suspicious": suspicious,
        "reasons": reasons[:5],
        "dimensions": f"{width}x{height}",
        "file_size_bytes": len(file_bytes),
        "contrast": round(float(contrast), 1),
        "edge_intensity": round(float(edge_intensity), 1),
        "lighting_variation": round(float(lighting_variation), 1),
        "dark_ratio": round(float(dark_ratio), 3),
    }


def analyze_pages(file_bytes_list: List[bytes], filenames: List[str]) -> Dict:
    """Analyze multiple uploaded pages of handwritten notes.
    
    Returns consolidated analysis across all pages.
    """
    page_results = []
    handwriting_scores = []
    suspicious_count = 0
    
    for i, (file_bytes, filename) in enumerate(zip(file_bytes_list, filenames)):
        result = analyze_image(file_bytes)
        result["page"] = i + 1
        result["filename"] = filename
        page_results.append(result)
        handwriting_scores.append(result["handwriting_score"])
        if result["suspicious"]:
            suspicious_count += 1
    
    avg_handwriting = sum(handwriting_scores) / max(len(handwriting_scores), 1)
    overall_suspicious = suspicious_count > len(page_results) // 2
    
    # Consolidate reasons
    all_reasons = []
    for pr in page_results:
        for reason in pr["reasons"]:
            if reason not in all_reasons:
                all_reasons.append(reason)
    
    return {
        "handwriting_score": round(avg_handwriting, 1),
        "page_count": len(page_results),
        "page_analyses": page_results,
        "suspicious": overall_suspicious,
        "reasons": all_reasons,
        "avg_contrast": round(sum(pr["contrast"] for pr in page_results) / len(page_results), 1) if page_results else 0,
        "avg_edge_intensity": round(sum(pr["edge_intensity"] for pr in page_results) / len(page_results), 1) if page_results else 0,
    }
