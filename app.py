"""
DDR Report Generator — Streamlit Web UI
Run with: streamlit run app.py
"""
import os
import sys
import tempfile
import streamlit as st
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DDR Report Generator",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.hero-banner {
    background: linear-gradient(135deg, #0f2d5e 0%, #1a4a8a 60%, #2d6cbe 100%);
    border-radius: 16px;
    padding: 40px 48px;
    color: white;
    margin-bottom: 32px;
}
.hero-banner h1 { font-size: 2.2rem; font-weight: 700; margin-bottom: 8px; }
.hero-banner p  { opacity: 0.85; font-size: 1.05rem; margin: 0; }
.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 20px;
    padding: 4px 16px;
    font-size: 0.8rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 16px;
}

.step-card {
    background: #f7f9fc;
    border: 1px solid #dde3ed;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 12px;
}
.step-card h4 { color: #0f2d5e; margin-bottom: 4px; }
.step-card p  { color: #666; font-size: 0.9rem; margin: 0; }

.success-banner {
    background: #f0faf5;
    border: 1px solid #2ecc71;
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 24px;
}

.section-preview {
    background: #f7f9fc;
    border-left: 4px solid #1a4a8a;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin-bottom: 12px;
    white-space: pre-wrap;
    font-size: 0.9rem;
}

div[data-testid="stSidebar"] { background: #0f2d5e !important; }
div[data-testid="stSidebar"] * { color: white !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero Banner ────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-tag">AI-Powered</div>
    <h1>🏗️ DDR Report Generator</h1>
    <p>Upload your Inspection Report and Thermal Report — get a professional Detailed Diagnostic Report in seconds.</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")

    api_key = st.text_input(
        "🔑 Groq API Key",
        type="password",
        placeholder="gsk-...",
        help="Your Groq API key. Required to generate the report."
    )

    property_name = st.text_input(
        "🏠 Property / Site Name",
        value="Inspected Property",
        placeholder="e.g. 42 Baker Street, Floor 3"
    )

    model_choice = st.selectbox(
        "🤖 LLM Model",
        options=["llama-3.1-8b-instant"],
        index=0,
        help="Llama 3.1 8B via Groq is used for fast and accurate diagnostics."
    )

    st.markdown("---")
    st.markdown("### 📋 How It Works")
    steps = [
        ("1️⃣", "Upload both PDFs"),
        ("2️⃣", "AI extracts text & images"),
        ("3️⃣", "LLM merges & generates DDR"),
        ("4️⃣", "Download your report"),
    ]
    for icon, text in steps:
        st.markdown(f"**{icon}** {text}")

    st.markdown("---")
    st.markdown("<small style='opacity:0.6'>Built for property diagnostics professionals</small>", unsafe_allow_html=True)

# ── File Upload ────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📄 Inspection Report")
    inspection_file = st.file_uploader(
        "Upload Inspection PDF",
        type=["pdf"],
        key="inspection_upload",
        label_visibility="collapsed"
    )
    if inspection_file:
        st.success(f"✅ {inspection_file.name} ({inspection_file.size // 1024} KB)")

with col2:
    st.markdown("### 🌡️ Thermal Report")
    thermal_file = st.file_uploader(
        "Upload Thermal PDF",
        type=["pdf"],
        key="thermal_upload",
        label_visibility="collapsed"
    )
    if thermal_file:
        st.success(f"✅ {thermal_file.name} ({thermal_file.size // 1024} KB)")

st.markdown("---")

# ── Generate Button ────────────────────────────────────────────────────
col_btn, col_info = st.columns([1, 3])
with col_btn:
    generate_clicked = st.button(
        "🚀 Generate DDR Report",
        type="primary",
        use_container_width=True,
        disabled=(not inspection_file or not thermal_file or not api_key)
    )

with col_info:
    if not api_key:
        st.warning("⚠️ Please enter your Groq API Key in the sidebar.")
    elif not inspection_file or not thermal_file:
        st.info("📁 Please upload both PDF documents to continue.")
    else:
        st.success("✅ Ready to generate! Click the button to start.")

# ── Generate Logic ─────────────────────────────────────────────────────
if generate_clicked and inspection_file and thermal_file and api_key:
    # Set API key in environment
    os.environ["GROQ_API_KEY"] = api_key

    # Save uploaded files to temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        inspection_path = os.path.join(tmpdir, "inspection.pdf")
        thermal_path    = os.path.join(tmpdir, "thermal.pdf")
        output_dir      = os.path.join(tmpdir, "outputs")

        with open(inspection_path, "wb") as f:
            f.write(inspection_file.getbuffer())
        with open(thermal_path, "wb") as f:
            f.write(thermal_file.getbuffer())

        os.makedirs(output_dir, exist_ok=True)

        # Import pipeline (after API key is set)
        from main import run_pipeline

        # Progress UI
        progress_bar = st.progress(0, text="Initializing pipeline...")
        status_area = st.empty()

        try:
            status_area.info("📖 Step 1/4 — Parsing documents…")
            progress_bar.progress(10, text="Parsing documents...")

            # Override model if needed
            import ai.llm_client as llm_mod
            # Monkey-patch model for this session
            _original_call = llm_mod.call_llm_json
            def _patched_call(prompt, model=model_choice, temperature=0.2):
                return _original_call(prompt, model=model_choice, temperature=temperature)
            llm_mod.call_llm_json = _patched_call

            status_area.info("🤖 Step 2/4 — AI is reading and merging both documents…")
            progress_bar.progress(30, text="AI processing...")

            results = run_pipeline(
                inspection_pdf=inspection_path,
                thermal_pdf=thermal_path,
                property_name=property_name,
                output_dir=output_dir,
            )

            progress_bar.progress(80, text="Building report...")
            status_area.info("📝 Step 3/4 — Assembling DDR report…")

            # Read generated files
            html_content = None
            pdf_content  = None

            if results.get("html") and os.path.exists(results["html"]):
                with open(results["html"], "r", encoding="utf-8") as f:
                    html_content = f.read()

            if results.get("pdf") and os.path.exists(results["pdf"]):
                with open(results["pdf"], "rb") as f:
                    pdf_content = f.read()

            progress_bar.progress(100, text="Done!")
            status_area.empty()

            # ── Success banner ────────────────────────────────────────
            st.markdown("""
            <div class="success-banner">
                <strong>✅ DDR Report generated successfully!</strong><br/>
                Download your report below.
            </div>
            """, unsafe_allow_html=True)

            # ── Download buttons ──────────────────────────────────────
            st.markdown("### 📥 Download Report")
            dl_col1, dl_col2, _ = st.columns([1, 1, 2])
            report_id = results.get("report_id", "DDR-report")

            if html_content:
                with dl_col1:
                    st.download_button(
                        label="⬇️ Download HTML",
                        data=html_content.encode("utf-8"),
                        file_name=f"{report_id}.html",
                        mime="text/html",
                        use_container_width=True,
                    )

            if pdf_content:
                with dl_col2:
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_content,
                        file_name=f"{report_id}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
            elif not pdf_content:
                with dl_col2:
                    st.info("PDF not available (WeasyPrint not installed). Use HTML report.")

            # ── Section preview ───────────────────────────────────────
            st.markdown("---")
            st.markdown("### 👁️ DDR Preview")

            from ai.prompt_builder import SECTION_DISPLAY_NAMES
            # Re-run to show sections — read from the pipeline's returned sections
            # We'll parse them from the HTML or show a message
            st.info("💡 Open the downloaded HTML/PDF to view the full formatted report.")

        except Exception as e:
            progress_bar.empty()
            status_area.empty()
            st.error(f"❌ Error generating report: {str(e)}")
            st.exception(e)

# ── Footer ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center><small style='color:#aaa'>DDR Report Generator &nbsp;|&nbsp; AI Diagnostics System &nbsp;|&nbsp; "
    f"Powered by Groq Llama 3.1</small></center>",
    unsafe_allow_html=True
)
