# 🏗️ DDR Report Generator — AI-Powered Property Diagnostic System

Automatically converts raw **Inspection Reports** and **Thermal Reports** (PDFs) into a professional, structured **Detailed Diagnostic Report (DDR)** using Groq Llama 3.1.

---

## 🎯 What It Does

| Input | Output |
|---|---|
| `inspection_report.pdf` + `thermal_report.pdf` | `DDR-YYYYMMDD-HHMMSS.html` + `.pdf` |

The AI reads both documents, merges information intelligently, and produces a clean 7-section DDR with images placed in the correct sections.

---

## 📋 DDR Sections Generated

1. Property Issue Summary
2. Area-wise Observations *(with relevant images)*
3. Probable Root Cause
4. Severity Assessment *(with reasoning)*
5. Recommended Actions
6. Additional Notes
7. Missing or Unclear Information

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone <repo-url>
cd ddr-report-generator
pip install -r requirements.txt
```

> **Note:** If WeasyPrint fails to install due to system dependencies, try:
> ```bash
> sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0
> pip install weasyprint
> ```

### 2. Set Your API Key

```bash
cp .env.example .env
# Edit .env and add your Groq API key
GROQ_API_KEY=gsk-your-key-here
```

### 3a. Run via Streamlit UI (Recommended)

```bash
streamlit run app.py
```

Open http://localhost:8501, upload your PDFs, and download your DDR report.

### 3b. Run via Command Line

```bash
python main.py \
  --inspection "path/to/inspection_report.pdf" \
  --thermal    "path/to/thermal_report.pdf" \
  --property-name "42 Baker Street, Floor 3" \
  --output-dir outputs/
```

Reports are saved to `outputs/` folder.

---

## 🗂️ Project Structure

```
ddr-report-generator/
├── main.py                   # CLI entry point & pipeline orchestrator
├── app.py                    # Streamlit web UI
├── requirements.txt
├── .env.example              # API key template
├── parser/
│   ├── pdf_parser.py         # Extract text + images from PDFs (PyMuPDF)
│   └── image_mapper.py       # Map images to DDR sections
├── ai/
│   ├── llm_client.py         # Groq API wrapper
│   ├── prompt_builder.py     # DDR prompts
│   └── merger.py             # Generate + merge DDR sections
├── report/
│   └── pdf_exporter.py       # HTML/PDF report generator
├── templates/
│   └── ddr_template.html     # Jinja2 report template
└── outputs/                  # Generated reports (created automatically)
```

---

## ⚙️ Tech Stack

| Component | Library |
|---|---|
| PDF parsing | PyMuPDF (fitz) + pdfplumber |
| AI / LLM | Groq Llama 3.1 8B |
| Report template | Jinja2 |
| PDF export | WeasyPrint |
| Web UI | Streamlit |

---

## 🛡️ Key Rules Enforced

- ✅ No facts invented — AI only uses information from the provided documents
- ✅ Conflicts flagged explicitly with `[CONFLICT: ...]`
- ✅ Missing information marked as `"Not Available"`
- ✅ Images placed under the most relevant sections
- ✅ Simple, client-friendly language

---

## ⚠️ Known Limitations

- Scanned PDFs without text layer require OCR (pytesseract) — basic support included
- Very large PDFs (>50 pages) are chunked and summarized before processing
- PDF export requires WeasyPrint + system fonts/libraries

---

## 📄 License

MIT
