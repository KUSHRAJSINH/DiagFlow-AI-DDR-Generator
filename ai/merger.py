import json
from typing import Dict, List
from ai.llm_client import call_llm_json, call_llm_text
from ai.prompt_builder import build_ddr_prompt, DDR_SECTIONS

FALLBACK_NOT_AVAILABLE = "Not Available"


def generate_ddr_sections(inspection_text: str, thermal_text: str) -> Dict[str, str]:
    """
    Use the LLM to generate all 7 DDR sections from the two documents.
    Returns: { "property_issue_summary": "...", ... }
    """
    print("[MERGER] Generating DDR sections via LLM...")
    prompt = build_ddr_prompt(inspection_text, thermal_text)

    try:
        result = call_llm_json(prompt)
    except ValueError as e:
        print(f"  [MERGER] LLM call failed: {e}. Using fallback.")
        return _fallback_sections()

    # Ensure all 7 sections are present
    validated = {}
    if not isinstance(result, dict):
        print(f"  [MERGER] LLM did not return a dictionary. Type: {type(result)}")
        return _fallback_sections()

    for section in DDR_SECTIONS:
        val = result.get(section, "")
        # Convert to string and strip, handle None case
        value = str(val).strip() if val is not None else ""
        validated[section] = value if value else FALLBACK_NOT_AVAILABLE

    return validated


def _fallback_sections() -> Dict[str, str]:
    """Return a placeholder DDR if LLM fails."""
    return {section: FALLBACK_NOT_AVAILABLE for section in DDR_SECTIONS}


def chunk_and_summarize(full_text: str, max_chars: int = 14000) -> str:
    """
    If a document is too long, summarize it in chunks before sending to the main DDR prompt.
    """
    if len(full_text) <= max_chars:
        return full_text

    print(f"  [MERGER] Document too long ({len(full_text)} chars). Chunking and summarizing...")

    chunk_size = 8000
    chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
    summaries = []

    for idx, chunk in enumerate(chunks):
        print(f"  [MERGER] Summarizing chunk {idx+1}/{len(chunks)}...")
        prompt = f"""Summarize the following section of a property inspection/thermal report.
Preserve all specific details: measurements, area names, temperatures, issue types, severity mentions.
Format as bullet points.

TEXT:
{chunk}

SUMMARY (bullet points, preserve all specific details):"""
        try:
            summary = call_llm_text(prompt)
            summaries.append(f"[SECTION {idx+1}]\n{summary}")
        except Exception as e:
            summaries.append(f"[SECTION {idx+1}]\n[SUMMARY FAILED: {e}]")

    return "\n\n".join(summaries)
