import os
import io
import qrcode
from base64 import b64encode
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle

class LumiaReceiptGenerator:
    """
    Generates professional PDF trust certificates and QR verification codes
    for Portaldot transactions.
    """
    
    def __init__(self):
        self.brand_color = colors.HexColor("#8b5cf6") # Lumia Purple
        self.bg_color = colors.HexColor("#080710")    # Deep Space
        self.text_primary = colors.whitesmoke
        self.text_secondary = colors.HexColor("#9ca3af")
        
    def generate_qr_base64(self, tx_hash: str) -> str:
        """Generates a QR code for a transaction hash and returns it as a base64 string."""
        # In a real app, this URL would point to a public verification page
        verify_url = f"https://lumia.trust/verify/{tx_hash}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(verify_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return b64encode(buffered.getvalue()).decode()

    def generate_pdf_bytes(self, receipt_data: dict, tx_hash: str) -> bytes:
        """Generates a professional PDF certificate and returns the raw bytes."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'LumiaTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=self.brand_color,
            spaceAfter=20,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'LumiaBody',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.black,
            spaceAfter=12,
            fontName='Helvetica'
        )

        label_style = ParagraphStyle(
            'LumiaLabel',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.gray,
            fontName='Helvetica-Bold'
        )

        elements = []

        # 1. Header (Lumia Logo Placeholder / Title)
        elements.append(Paragraph("LUMIA TRUST CERTIFICATE", title_style))
        elements.append(Paragraph("Official On-Chain Transaction Verification", body_style))
        elements.append(Spacer(1, 1*cm))

        # 2. Transaction Summary Table
        data = [
            [Paragraph("Transaction Hash", label_style), Paragraph(tx_hash, body_style)],
            [Paragraph("Scanner ID", label_style), Paragraph(receipt_data.get('scanner_id', 'Unknown'), body_style)],
            [Paragraph("Risk Score", label_style), Paragraph(f"{receipt_data.get('risk_score', '0')}/100", body_style)],
            [Paragraph("Risk Level", label_style), Paragraph(receipt_data.get('risk_level', 'Unknown'), body_style)],
            [Paragraph("Timestamp", label_style), Paragraph(receipt_data.get('timestamp_readable', 'N/A'), body_style)],
            [Paragraph("Registry Proof", label_style), Paragraph("On-Chain Smart Contract (ink! 5.0)", body_style)]
        ]

        t = Table(data, colWidths=[5*cm, 10*cm])
        t.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 2*cm))

        # 3. AI Safety Briefing
        elements.append(Paragraph("AI SECURITY BRIEFING", label_style))
        briefing_text = receipt_data.get('ai_briefing', "No briefing available.")
        elements.append(Paragraph(briefing_text.replace('\n', '<br/>'), body_style))
        elements.append(Spacer(1, 2*cm))

        # 4. QR Verification Code
        qr_pil = qrcode.make(f"https://lumia.trust/verify/{tx_hash}")
        qr_buffer = io.BytesIO()
        qr_pil.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        qr_img = Image(qr_buffer, width=3*cm, height=3*cm)
        
        qr_table_data = [
            [qr_img, Paragraph("<b>Scan to Verify</b><br/>Verify this certificate directly on the Portaldot blockchain ledger via the Lumia Protocol portal.", body_style)]
        ]
        qr_table = Table(qr_table_data, colWidths=[4*cm, 11*cm])
        qr_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(qr_table)

        # 5. Footer
        elements.append(Spacer(1, 2*cm))
        elements.append(Paragraph("© 2026 Lumia Protocol. Fulfilling Portaldot Season 1 Hackathon Requirements.", label_style))

        doc.build(elements)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
