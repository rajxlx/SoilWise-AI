from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether


def make_report(analysis) -> bytes:
    """Build a paginated PDF; Paragraph handles wrapping and XML-escapes user data."""
    out = BytesIO()
    doc = SimpleDocTemplate(out, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm,
                            topMargin=18*mm, bottomMargin=18*mm,
                            title="SoilWise Soil Health Report", author="SoilWise")
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="SmallNote", parent=styles["BodyText"], fontSize=8,
                              leading=11, textColor=colors.HexColor("#555555")))
    story = [Paragraph("SoilWise — Soil Health Report", styles["Title"]), Spacer(1, 6*mm)]
    details = [
        ["Field", escape(str(analysis.field_name))],
        ["Health score", f"{int(analysis.health_score)}/100"],
        ["N / P / K (mg/kg)", f"{analysis.nitrogen:g} / {analysis.phosphorus:g} / {analysis.potassium:g}"],
        ["pH", f"{analysis.ph:g}"],
        ["Organic matter", f"{analysis.organic_matter:g}%"],
        ["Moisture", f"{analysis.moisture:g}%"],
    ]
    table = Table(details, colWidths=[42*mm, 125*mm], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#edf4e9")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#d5dfd0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.extend([table, Spacer(1, 7*mm), Paragraph("Findings", styles["Heading2"])])
    issues = analysis.diagnosis.get("issues", [])
    if not issues:
        story.append(Paragraph("No threshold alerts were identified by this screening.", styles["BodyText"]))
    else:
        for issue in issues:
            story.append(Paragraph(f"<b>{escape(str(issue.get('nutrient', 'Finding')))}</b>: "
                                   f"{escape(str(issue.get('message', '')))}", styles["BodyText"]))
            story.append(Spacer(1, 2*mm))
    story.extend([Spacer(1, 5*mm), Paragraph("Recommended next steps", styles["Heading2"])])
    for item in analysis.recommendations:
        story.append(KeepTogether([
            Paragraph(escape(str(item.get("title", "Recommendation"))), styles["Heading3"]),
            Paragraph(escape(str(item.get("detail", ""))), styles["BodyText"]),
            Spacer(1, 3*mm),
        ]))
    story.extend([Spacer(1, 5*mm), Paragraph(
        "Advisory screening only. Confirm results with a soil laboratory and local agricultural extension officer. "
        "Do not use this report alone to determine fertilizer dosage.", styles["SmallNote"]
    )])
    doc.build(story)
    return out.getvalue()
