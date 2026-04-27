import os
from fpdf import FPDF
from PIL import Image, ImageDraw

def create_mock_image(filename, text, color):
    img = Image.new('RGB', (400, 300), color=color)
    d = ImageDraw.Draw(img)
    d.text((10,150), text, fill=(255,255,255))
    img.save(filename)

def generate_inspection_report(folder):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15, style='B')
    pdf.cell(200, 10, txt="Visual Inspection Report", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Date: 2026-04-28", ln=True)
    pdf.cell(200, 10, txt="Inspector: John Doe", ln=True)
    pdf.ln(10)
    
    # Area 1
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(200, 10, txt="1. Roof Area", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Observation: Visible water ponding near the HVAC unit. The membrane seems slightly degraded. Expected severity: Medium.")
    
    img_path1 = os.path.join(folder, "roof_visual.jpg")
    create_mock_image(img_path1, "Roof Visual: Water Ponding", (100, 100, 100))
    pdf.image(img_path1, w=100)
    
    pdf.ln(10)
    # Area 2
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(200, 10, txt="2. Electrical Panel (Basement)", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Observation: Dust accumulation and slight corrosion on terminal C. No immediate visual hazards found.")
    
    img_path2 = os.path.join(folder, "elec_visual.jpg")
    create_mock_image(img_path2, "Electrical Panel Visual", (80, 80, 80))
    pdf.image(img_path2, w=100)

    pdf.ln(10)
    # Area 3 (Missing in thermal)
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(200, 10, txt="3. North Wall Exterior", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Observation: Small cracks present in the concrete. Needs filling before winter.")

    pdf.output(os.path.join(folder, "Inspection_Report.pdf"))
    
    # Cleanup images
    os.remove(img_path1)
    os.remove(img_path2)

def generate_thermal_report(folder):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15, style='B')
    pdf.cell(200, 10, txt="Thermal Imaging Document", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Date: 2026-04-28", ln=True)
    pdf.cell(200, 10, txt="Technician: Jane Smith", ln=True)
    pdf.ln(10)
    
    # Area 1
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(200, 10, txt="A. Roof Area near HVAC", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Thermal finding: Significant temperature drop detected under the ponding water. Anomalous cold spot indicates compromised insulation under the membrane. Severity: High.")
    
    img_path1 = os.path.join(folder, "roof_thermal.jpg")
    create_mock_image(img_path1, "Roof Thermal: Cold Spot (Blue)", (0, 0, 200)) # blue for cold
    pdf.image(img_path1, w=100)
    
    pdf.ln(10)
    # Area 2
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(200, 10, txt="B. Basement Electrical Panel", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Thermal finding: Overheating observed on terminal B. Temperature is 85C, well above safe operational limits. Immediate action required. Severity: Critical.")
    
    img_path2 = os.path.join(folder, "elec_thermal.jpg")
    create_mock_image(img_path2, "Electric Thermal: Hot Spot (Red)", (200, 0, 0)) # red for hot
    pdf.image(img_path2, w=100)

    # Note: North Wall is missing, simulating missing data
    # Note: Terminal B is hot in thermal, but Terminal C had corrosion in visual (simulating conflict/different findings)

    pdf.output(os.path.join(folder, "Thermal_Report.pdf"))
    
    # Cleanup images
    os.remove(img_path1)
    os.remove(img_path2)

if __name__ == "__main__":
    folder = "sample_reports"
    if not os.path.exists(folder):
        os.makedirs(folder)
    generate_inspection_report(folder)
    generate_thermal_report(folder)
    print("PDF reports generated successfully in 'sample_reports' folder.")
