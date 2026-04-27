import os
import base64
from datetime import datetime
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader

# PDF export
try:
    from weasyprint import HTML as WeasyHTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    print("[WARN] WeasyPrint not installed. PDF export will be skipped. HTML report will still be generated.")


TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")


def _image_to_data_uri(image_path: str) -> str:
    """Convert image path to base64 data URI for embedding in HTML."""
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        ext = os.path.splitext(image_path)[1].lower().lstrip(".")
        if ext in ("jpg", "jpeg"):
            mime = "image/jpeg"
        elif ext == "png":
            mime = "image/png"
        else:
            mime = f"image/{ext}"
        b64 = base64.b64encode(data).decode("utf-8")
        return f"data:{mime};base64,{b64}"
    except Exception as e:
        print(f"  [WARN] Could not embed image {image_path}: {e}")
        return ""


def _prepare_image_list(image_paths: List[str]) -> List[Dict]:
    """
    Convert a list of image file paths into a list of dicts
    with 'path' (data URI) and 'caption' for the template.
    """
    result = []
    for img_path in image_paths:
        if os.path.exists(img_path):
            data_uri = _image_to_data_uri(img_path)
            if data_uri:
                caption = os.path.basename(img_path)
                result.append({"path": data_uri, "caption": caption})
    return result


def build_ddr_html(
    sections: Dict[str, str],
    section_images: Dict[str, List[str]],
    property_name: str = "Inspected Property",
    report_id: str = None,
) -> str:
    """
    Render the DDR HTML using the Jinja2 template.
    Returns the rendered HTML string.
    """
    if report_id is None:
        report_id = f"DDR-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    generated_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    # Prepare image dicts for template
    template_images = {}
    for section_key, paths in section_images.items():
        template_images[section_key] = _prepare_image_list(paths)

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("ddr_template.html")

    html = template.render(
        sections=sections,
        images=template_images,
        property_name=property_name,
        report_id=report_id,
        generated_date=generated_date,
    )
    return html


def save_html_report(html: str, output_path: str) -> str:
    """Save HTML report to file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[EXPORTER] HTML report saved: {output_path}")
    return output_path


def save_pdf_report(html: str, output_path: str) -> str:
    """Convert HTML to PDF using WeasyPrint."""
    if not WEASYPRINT_AVAILABLE:
        print("[EXPORTER] WeasyPrint not available. Skipping PDF export.")
        return None

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    WeasyHTML(string=html).write_pdf(output_path)
    print(f"[EXPORTER] PDF report saved: {output_path}")
    return output_path


def export_ddr(
    sections: Dict[str, str],
    section_images: Dict[str, List[str]],
    output_dir: str,
    property_name: str = "Inspected Property",
    report_id: str = None,
) -> Dict[str, str]:
    """
    Full export pipeline: build HTML, save HTML, save PDF.
    Returns: {"html": path, "pdf": path or None}
    """
    if report_id is None:
        report_id = f"DDR-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    html = build_ddr_html(sections, section_images, property_name, report_id)

    html_path = os.path.join(output_dir, f"{report_id}.html")
    pdf_path = os.path.join(output_dir, f"{report_id}.pdf")

    save_html_report(html, html_path)
    pdf_result = save_pdf_report(html, pdf_path)

    return {
        "html": html_path,
        "pdf": pdf_result,
        "report_id": report_id,
    }
