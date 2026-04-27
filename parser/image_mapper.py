import os
import json
from typing import List, Dict

# Keywords that suggest which DDR section an image belongs to
SECTION_KEYWORDS = {
    "property_issue_summary": [
        "overview", "summary", "whole", "entire", "building", "property", "exterior", "facade"
    ],
    "area_wise_observations": [
        "room", "area", "zone", "wall", "ceiling", "floor", "roof", "basement",
        "bathroom", "kitchen", "bedroom", "corridor", "staircase", "window", "door",
        "crack", "leak", "stain", "damp", "moisture", "thermal", "temperature",
        "hot", "cold", "heat", "pipe", "duct", "hvac"
    ],
    "probable_root_cause": [
        "source", "origin", "cause", "root", "reason", "pipe", "drain", "infiltration"
    ],
    "severity_assessment": [
        "damage", "severe", "critical", "major", "minor", "risk", "alert"
    ],
    "recommended_actions": [
        "repair", "fix", "seal", "replace", "action", "treatment", "waterproof"
    ],
}


def map_images_to_sections(
    inspection_pages: List[Dict],
    thermal_pages: List[Dict],
    llm_section_texts: Dict[str, str]
) -> Dict[str, List[str]]:
    """
    Maps extracted images to DDR sections.

    Strategy:
    1. For each image, find the page it came from.
    2. Look at the text of that page for keywords.
    3. Match to the best DDR section.
    4. Fallback: assign to area_wise_observations.

    Returns: { "section_name": ["img_path1", "img_path2", ...] }
    """
    section_images: Dict[str, List[str]] = {
        "property_issue_summary": [],
        "area_wise_observations": [],
        "probable_root_cause": [],
        "severity_assessment": [],
        "recommended_actions": [],
        "additional_notes": [],
    }

    all_pages = inspection_pages + thermal_pages

    for page_data in all_pages:
        page_text = page_data.get("text", "").lower()
        images = page_data.get("images", [])

        if not images:
            continue

        best_section = _score_page_to_section(page_text)

        for img_path in images:
            section_images[best_section].append(img_path)

    return section_images


def _score_page_to_section(page_text: str) -> str:
    """
    Score page text against section keywords, return best-matching section.
    """
    scores = {}
    for section, keywords in SECTION_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in page_text)
        scores[section] = score

    # Normalize to valid sections
    valid_sections = [
        "property_issue_summary",
        "area_wise_observations",
        "probable_root_cause",
        "severity_assessment",
        "recommended_actions",
    ]

    best = max(valid_sections, key=lambda s: scores.get(s, 0))
    # If nothing matched well, default to area_wise_observations
    if scores.get(best, 0) == 0:
        return "area_wise_observations"
    return best
