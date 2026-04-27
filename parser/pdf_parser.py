import fitz  # PyMuPDF
import pdfplumber
import os
import json
from PIL import Image
import io

def extract_text_and_images(pdf_path: str, output_image_dir: str) -> dict:
    """
    Extract all text (page-by-page) and all embedded images from a PDF.
    Returns a dict:
    {
        "pages": [{"page_num": 1, "text": "...", "images": ["path1.png", ...]}, ...],
        "full_text": "...",
        "all_images": ["path1.png", ...]
    }
    """
    os.makedirs(output_image_dir, exist_ok=True)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    pages_data = []
    all_images = []
    full_text_parts = []

    doc = fitz.open(pdf_path)

    for page_index in range(len(doc)):
        page = doc[page_index]
        page_num = page_index + 1

        # --- Extract text ---
        text = page.get_text("text").strip()
        full_text_parts.append(f"[PAGE {page_num}]\n{text}")

        # --- Extract images ---
        page_images = []
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                img_filename = f"{pdf_name}_page{page_num}_img{img_index + 1}.{image_ext}"
                img_path = os.path.join(output_image_dir, img_filename)

                with open(img_path, "wb") as f:
                    f.write(image_bytes)

                # Also verify it's a valid image
                try:
                    with Image.open(img_path) as im:
                        width, height = im.size
                        # Skip tiny/icon images (less than 50x50)
                        if width > 50 and height > 50:
                            page_images.append(img_path)
                            all_images.append(img_path)
                        else:
                            os.remove(img_path)
                except Exception:
                    os.remove(img_path)

            except Exception as e:
                print(f"  [WARN] Could not extract image xref={xref} on page {page_num}: {e}")

        pages_data.append({
            "page_num": page_num,
            "text": text,
            "images": page_images
        })

    doc.close()

    return {
        "pages": pages_data,
        "full_text": "\n\n".join(full_text_parts),
        "all_images": all_images
    }


def extract_tables_as_text(pdf_path: str) -> str:
    """
    Use pdfplumber to extract any tables from the PDF as formatted text.
    """
    table_texts = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                for t_idx, table in enumerate(tables):
                    table_texts.append(f"[TABLE on page {i+1}, table {t_idx+1}]")
                    for row in table:
                        cleaned_row = [str(cell).strip() if cell else "" for cell in row]
                        table_texts.append(" | ".join(cleaned_row))
                    table_texts.append("")
    except Exception as e:
        print(f"  [WARN] pdfplumber error: {e}")

    return "\n".join(table_texts)


def parse_document(pdf_path: str, output_image_dir: str) -> dict:
    """
    Full document parsing: text, images, and tables.
    """
    print(f"[PARSER] Parsing: {pdf_path}")
    result = extract_text_and_images(pdf_path, output_image_dir)
    table_text = extract_tables_as_text(pdf_path)

    if table_text.strip():
        result["full_text"] += f"\n\n[EXTRACTED TABLES]\n{table_text}"

    print(f"  → Pages: {len(result['pages'])}")
    print(f"  → Images extracted: {len(result['all_images'])}")
    return result
