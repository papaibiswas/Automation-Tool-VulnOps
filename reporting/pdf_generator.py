from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(output_path, scan_info, critical, high, medium):
    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    elements = []

    # 🔥 COVER PAGE
    elements.append(Paragraph("<b>Vulnerability Assessment Report</b>", styles['Title']))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Target: {scan_info['target']}", styles['Normal']))
    elements.append(Paragraph(f"Scan Type: {scan_info['scan_type']}", styles['Normal']))
    elements.append(Paragraph(f"Date: {scan_info['date']}", styles['Normal']))
    #elements.append(PageBreak())

    # 🔥 SUMMARY
    #elements.append(Paragraph("<b>Executive Summary</b>", styles['Heading1']))
    #elements.append(Spacer(1, 10))
    #elements.append(Paragraph(
    #    "This report contains vulnerabilities identified during automated scanning.",
    #    styles['Normal']
    #))
    #elements.append(PageBreak())

    # 🔥 COUNTS
    elements.append(Paragraph("<b>Vulnerability Summary</b>", styles['Heading1']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Critical: {len(critical)}", styles['Normal']))
    elements.append(Paragraph(f"High: {len(high)}", styles['Normal']))
    elements.append(Paragraph(f"Medium: {len(medium)}", styles['Normal']))
    #elements.append(PageBreak())

    # 🔥 DETAILS
    def add_section(title, vulns):
        elements.append(Paragraph(f"<b>{title}</b>", styles['Heading2']))
        elements.append(Spacer(1, 10))

        for v in vulns:
            elements.append(Paragraph(f"<b>{v['name']}</b>", styles['Normal']))
            elements.append(Paragraph(f"Host: {v['host']} | Port: {v['port']}", styles['Normal']))
            elements.append(Paragraph(f"Severity: {v['severity']}", styles['Normal']))
            elements.append(Paragraph(f"Description: {v['description']}", styles['Normal']))
            elements.append(Paragraph(f"Solution: {v['solution']}", styles['Normal']))
            elements.append(Spacer(1, 12))

    add_section("Critical Vulnerabilities", critical)
    add_section("High Vulnerabilities", high)
    add_section("Medium Vulnerabilities", medium)

    doc.build(elements)
    return output_path