DDR_SECTIONS = [
    "property_issue_summary",
    "area_wise_observations",
    "probable_root_cause",
    "severity_assessment",
    "recommended_actions",
    "additional_notes",
    "missing_or_unclear_information",
]

SECTION_DISPLAY_NAMES = {
    "property_issue_summary": "1. Property Issue Summary",
    "area_wise_observations": "2. Area-wise Observations",
    "probable_root_cause": "3. Probable Root Cause",
    "severity_assessment": "4. Severity Assessment",
    "recommended_actions": "5. Recommended Actions",
    "additional_notes": "6. Additional Notes",
    "missing_or_unclear_information": "7. Missing or Unclear Information",
}


def build_ddr_prompt(inspection_text: str, thermal_text: str) -> str:
    """
    Build the master prompt for Groq Llama 3 to generate a structured DDR.
    """
    # Truncate if too long (keep within ~12k tokens each)
    MAX_CHARS = 14000
    if len(inspection_text) > MAX_CHARS:
        inspection_text = inspection_text[:MAX_CHARS] + "\n\n[... TRUNCATED FOR LENGTH ...]"
    if len(thermal_text) > MAX_CHARS:
        thermal_text = thermal_text[:MAX_CHARS] + "\n\n[... TRUNCATED FOR LENGTH ...]"

    prompt = f"""You are a senior property diagnostics expert preparing a professional Detailed Diagnostic Report (DDR) for a client.

You have been given TWO source documents:

==================================================
[DOCUMENT 1: INSPECTION REPORT]
==================================================
{inspection_text}

==================================================
[DOCUMENT 2: THERMAL REPORT]
==================================================
{thermal_text}

==================================================
YOUR TASK:
==================================================
Read both documents carefully and generate a comprehensive DDR with the EXACT 7 sections listed below.

RULES (MUST FOLLOW):
- Do NOT invent or assume any fact not present in the documents
- Combine information from both documents intelligently — no duplication
- If both documents mention the same issue, merge them into ONE observation
- If the two documents CONFLICT on the same point (e.g., different temperature values, different severity), write BOTH values and clearly flag: "[CONFLICT: Document 1 states X, Document 2 states Y]"
- If information for any section is not available in either document, write exactly: "Not Available"
- Use simple, client-friendly language — avoid excessive jargon
- Be concise but thorough
- For severity, always explain WHY (e.g., "Critical — standing water indicates active leak likely causing structural damage")

OUTPUT FORMAT:
Return a valid JSON object with EXACTLY these keys:

{{
  "property_issue_summary": "...",
  "area_wise_observations": "...",
  "probable_root_cause": "...",
  "severity_assessment": "...",
  "recommended_actions": "...",
  "additional_notes": "...",
  "missing_or_unclear_information": "..."
}}

Each value should be a well-written paragraph or structured list (use \\n for new lines within strings).
Do not include markdown, code fences, or any text outside the JSON object.
"""
    return prompt


def build_image_mapping_prompt(
    section_name: str,
    section_text: str,
    image_descriptions: list
) -> str:
    """
    Build a prompt to ask the LLM which images belong to a given section.
    image_descriptions: list of {"id": "img_path", "context": "page text snippet"}
    """
    img_list = "\n".join(
        [f"  Image {i+1}: {d['id']} (from page containing: '{d['context'][:200]}')"
         for i, d in enumerate(image_descriptions)]
    )

    return f"""You are placing images into a diagnostic report section.

Section: {section_name}
Section Content:
{section_text[:1000]}

Available images and their page context:
{img_list}

Which of the above images are RELEVANT to this section?
Reply with a JSON array of the image paths that are relevant. Example: ["/path/img1.png", "/path/img2.png"]
If none are relevant, reply with: []
"""
