import os
from weasyprint import HTML

# Ensure directories exist
os.makedirs("sample_data", exist_ok=True)

# 1. Inspection Report Content
inspection_html = """
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .header { background: #0f2d5e; color: white; padding: 20px; text-align: center; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }
        .section h2 { color: #0f2d5e; margin-top: 0; }
        .observation { margin-bottom: 20px; }
        img { max-width: 100%; border-radius: 4px; margin-top: 10px; }
        .page-break { page-break-after: always; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Site Inspection Report</h1>
        <p>Property: Sunrise Apartments, Block A, Unit 302</p>
        <p>Date: October 24, 2026</p>
    </div>

    <div class="section">
        <h2>1. Site Observations</h2>
        
        <div class="observation">
            <h3>1.1 Kitchen Area</h3>
            <p>Significant water staining and dampness observed on the wooden base of the kitchen sink cabinet. Dark patches indicate prolonged exposure to moisture. Primary concern is a potential slow leak from the trap or supply lines.</p>
            <p><strong>Finding:</strong> Evidence of mold growth (green/black spots) starting to form in the rear corner.</p>
            <img src="images/inspection_kitchen.png" alt="Kitchen Sink Cabinet Staining">
        </div>

        <div class="observation">
            <h3>1.2 Living Room</h3>
            <p>A hairline crack (approx. 15cm) observed on the ceiling plaster near the center chandelier. No signs of active water ingress at the time of inspection.</p>
        </div>

        <div class="observation">
            <h3>1.3 Bedroom 1</h3>
            <p>No visible defects on walls or ceiling. Window frame appears intact but user reports drafty conditions during rain.</p>
        </div>
    </div>

    <div class="section">
        <h2>2. General Notes</h2>
        <p>The property is generally well-maintained, however, the kitchen moisture issue requires immediate attention to prevent structural damage to the cabinetry and health risks from mold.</p>
    </div>
</body>
</html>
"""

# 2. Thermal Report Content
thermal_html = """
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .header { background: #8a1a1a; color: white; padding: 20px; text-align: center; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }
        .section h2 { color: #8a1a1a; margin-top: 0; }
        .thermal-finding { margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 20px; }
        img { max-width: 100%; border: 1px solid #333; }
        .temp { font-weight: bold; color: #d35400; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Thermal Imaging & Analysis Report</h1>
        <p>Property: Sunrise Apartments, Block A</p>
        <p>Instrument: FLIR E8-XT Professional</p>
    </div>

    <div class="section">
        <h2>Thermal Findings</h2>

        <div class="thermal-finding">
            <h3>Location: Kitchen Sink (Under-side)</h3>
            <p>Thermal scan reveals a cold anomaly (<span class="temp">21.6°C</span>) against an ambient cabinet temperature of <span class="temp">26.8°C</span>. This температурный перепад (temperature delta) is consistent with active moisture accumulation or a slow leak.</p>
            <p>The pattern is localized around the P-trap assembly.</p>
            <img src="images/thermal_kitchen.png" alt="Thermal Scan - Kitchen Sink">
        </div>

        <div class="thermal-finding">
            <h3>Location: Living Room Ceiling</h3>
            <p>Thermal profile is uniform across the ceiling area. No thermal anomalies or cold spots detected near the reported hairline crack. This suggests the crack is likely structural or cosmetic and not related to the upper floor plumbing.</p>
        </div>

        <div class="thermal-finding">
            <h3>Location: Bedroom 1 Window</h3>
            <p>Significant heat ingress detected around the top left corner of the window frame. Surface temperature recorded at <span class="temp">32.4°C</span> compared to wall temperature of <span class="temp">25.5°C</span>. This indicates a failure in the weather stripping or sealant.</p>
        </div>
    </div>
</body>
</html>
"""

# 3. Complex Inspection Report
complex_inspection_html = """
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .header { background: #1a5e0f; color: white; padding: 20px; text-align: center; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }
        .observation { margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Complex Site Inspection Report</h1>
        <p>Property: Industrial Warehouse, Zone C</p>
        <p>Date: October 24, 2026</p>
    </div>

    <div class="section">
        <h2>Observations</h2>
        <div class="observation">
            <h3>Basement Storage</h3>
            <p>Walls appear dry. No visible staining or water ingress noted. Dust accumulation suggests no recent moisture activity.</p>
        </div>
        <div class="observation">
            <h3>Electrical Room</h3>
            <p>Main distribution board shows signs of aging. Dust on breakers. Cover plate is slightly loose. No burning smell or tripping reported.</p>
        </div>
        <div class="observation">
            <h3>Roof (External)</h3>
            <p>Inspection from ground level shows several loose or missing shingles in the Northwest corner. Guttering appears clear.</p>
        </div>
        <div class="observation">
            <h3>Staff Bathroom</h3>
            <p>Minor hairline cracks on floor tiles. Grouting appears aged but intact.</p>
        </div>
    </div>
</body>
</html>
"""

# 4. Complex Thermal Report
complex_thermal_html = """
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .header { background: #5e0f5e; color: white; padding: 20px; text-align: center; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }
        img { max-width: 100%; border: 1px solid #333; }
        .alert { color: #c0392b; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Advanced Thermal Analysis Report</h1>
        <p>Property: Industrial Warehouse, Zone C</p>
    </div>

    <div class="section">
        <h2>Thermal Anomalies</h2>
        <div class="observation">
            <h3>Basement Wall (West)</h3>
            <p><span class="alert">CRITICAL:</span> Thermal imaging reveals a large moisture plume behind the drywall (18.2°C anomaly). Hidden leak likely originating from external ground-water infiltration.</p>
        </div>
        <div class="observation">
            <h3>Main Electrical Panel</h3>
            <p><span class="alert">DANGER:</span> Circuit breaker CB12 is recording a temperature of 85.3°C. This indicates a severe overload or loose connection. Immediate fire hazard.</p>
            <img src="images/thermal_electrical.png">
        </div>
        <div class="observation">
            <h3>Roof Heat Loss Audit</h3>
            <p>Aerial scan shows significant heat escaping from the NW corner (34°C internal thermal signature). Confirms insulation is missing or compromised in this area.</p>
            <img src="images/thermal_roof.png">
        </div>
        <div class="observation">
            <h3>Staff Bathroom</h3>
            <p>Uniform thermal distribution. No cold spots detected near floor cracks. Issues are cosmetic.</p>
        </div>
    </div>
</body>
</html>
"""

# Write files and generate PDFs
print("Saving HTML files...")
with open("sample_data/inspection.html", "w") as f:
    f.write(inspection_html)
with open("sample_data/thermal.html", "w") as f:
    f.write(thermal_html)
with open("sample_data/complex_inspection.html", "w") as f:
    f.write(complex_inspection_html)
with open("sample_data/complex_thermal.html", "w") as f:
    f.write(complex_thermal_html)

print("Generating PDFs from HTML...")
HTML(string=inspection_html, base_url="sample_data").write_pdf("sample_data/inspection_report.pdf")
HTML(string=thermal_html, base_url="sample_data").write_pdf("sample_data/thermal_report.pdf")
HTML(string=complex_inspection_html, base_url="sample_data").write_pdf("sample_data/complex_inspection_report.pdf")
HTML(string=complex_thermal_html, base_url="sample_data").write_pdf("sample_data/complex_thermal_report.pdf")

print("Success! All PDFs generated in sample_data/ folder.")
