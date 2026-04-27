"""
DDR Report Generator — Main Orchestration Script
Usage:
  python main.py --inspection <path> --thermal <path> [--property-name "<name>"] [--output-dir <dir>]
"""
import os
import sys
import argparse
from datetime import datetime

# ── Project imports ──────────────────────────────────────────────────
from parser.pdf_parser import parse_document
from parser.image_mapper import map_images_to_sections
from ai.merger import generate_ddr_sections, chunk_and_summarize
from report.pdf_exporter import export_ddr


def run_pipeline(
    inspection_pdf: str,
    thermal_pdf: str,
    property_name: str = "Inspected Property",
    output_dir: str = "outputs",
) -> dict:
    """
    Full DDR generation pipeline.
    Returns paths to generated report files.
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_id = f"DDR-{timestamp}"
    image_dir = os.path.join(output_dir, "images", report_id)

    print("\n" + "═" * 60)
    print("  DDR REPORT GENERATION PIPELINE")
    print("═" * 60)
    print(f"  Inspection: {inspection_pdf}")
    print(f"  Thermal:    {thermal_pdf}")
    print(f"  Report ID:  {report_id}")
    print("═" * 60 + "\n")

    # ── STEP 1: Parse both documents ──────────────────────────────────
    print("[STEP 1] Parsing documents...")
    inspection_data = parse_document(inspection_pdf, image_dir)
    thermal_data    = parse_document(thermal_pdf, image_dir)

    # ── STEP 2: Prepare text (chunking if needed) ─────────────────────
    print("\n[STEP 2] Preparing text for AI processing...")
    inspection_text = chunk_and_summarize(inspection_data["full_text"])
    thermal_text    = chunk_and_summarize(thermal_data["full_text"])

    # ── STEP 3: Generate DDR sections via LLM ────────────────────────
    print("\n[STEP 3] Generating DDR sections via LLM...")
    sections = generate_ddr_sections(inspection_text, thermal_text)

    print("\n  Generated sections:")
    for k, v in sections.items():
        preview = v[:80].replace("\n", " ") + ("..." if len(v) > 80 else "")
        print(f"  • {k}: {preview}")

    # ── STEP 4: Map images to sections ───────────────────────────────
    print("\n[STEP 4] Mapping images to DDR sections...")
    section_images = map_images_to_sections(
        inspection_pages=inspection_data["pages"],
        thermal_pages=thermal_data["pages"],
        llm_section_texts=sections,
    )

    total_images = sum(len(v) for v in section_images.values())
    print(f"  Total images placed: {total_images}")
    for section, imgs in section_images.items():
        if imgs:
            print(f"  • {section}: {len(imgs)} image(s)")

    # ── STEP 5: Export DDR report ─────────────────────────────────────
    print("\n[STEP 5] Exporting DDR report...")
    results = export_ddr(
        sections=sections,
        section_images=section_images,
        output_dir=output_dir,
        property_name=property_name,
        report_id=report_id,
    )

    print("\n" + "═" * 60)
    print("  DONE!")
    print(f"  HTML Report: {results['html']}")
    if results.get("pdf"):
        print(f"  PDF Report:  {results['pdf']}")
    print("═" * 60 + "\n")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="DDR Report Generator — converts inspection + thermal PDFs into a structured report"
    )
    parser.add_argument(
        "--inspection", required=True,
        help="Path to the inspection report PDF"
    )
    parser.add_argument(
        "--thermal", required=True,
        help="Path to the thermal report PDF"
    )
    parser.add_argument(
        "--property-name", default="Inspected Property",
        help="Name of the property/site (shown on cover page)"
    )
    parser.add_argument(
        "--output-dir", default="outputs",
        help="Directory where generated reports will be saved (default: outputs/)"
    )

    args = parser.parse_args()

    # Validate inputs
    if not os.path.isfile(args.inspection):
        print(f"[ERROR] Inspection PDF not found: {args.inspection}")
        sys.exit(1)
    if not os.path.isfile(args.thermal):
        print(f"[ERROR] Thermal PDF not found: {args.thermal}")
        sys.exit(1)

    results = run_pipeline(
        inspection_pdf=args.inspection,
        thermal_pdf=args.thermal,
        property_name=args.property_name,
        output_dir=args.output_dir,
    )

    return results


if __name__ == "__main__":
    main()
