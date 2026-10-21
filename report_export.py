import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf_report(report_text):

    file_path = "ClinicalGenAI_Monitoring_Report.pdf"

    document = SimpleDocTemplate(
        file_path,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "ClinicalGenAI Monitoring Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    paragraphs = report_text.split("\n")

    for paragraph in paragraphs:

        if paragraph.strip():

            story.append(
                Paragraph(
                    paragraph,
                    styles["BodyText"]
                )
            )

            story.append(
                Spacer(1, 10)
            )

    document.build(story)

    return (file_path)