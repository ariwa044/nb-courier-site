from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.colors import HexColor
from reportlab.graphics.shapes import Drawing, Rect, Path
from reportlab.graphics import renderPDF

def generate_receipt_pdf(response, package):
    # Brand colors
    BRAND_YELLOW = HexColor('#FDB813')
    BRAND_BLUE = HexColor('#205875')
    LIGHT_BLUE = HexColor('#E8F1F5')

    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        leftMargin=15*mm,
        rightMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )
    
    elements = []

    from reportlab.platypus import Image

    def create_simple_logo():
        logo = Image('static/images/logo.png', width=20*mm, height=20*mm)
        return logo

    # Header with company info
    header_data = [
        [create_simple_logo(), 'SHIPPING RECEIPT', '', f'Receipt #{package.package_id}'],
        ['', '','CHASEXPRESS', '', f'Date: {package.shipping_date.strftime("%Y-%m-%d")}'],
       # ['', '283 Pier Drive, Brooklyn...', '', f'Time: {package.shipping_date.strftime("%H:%M")}'],
    ]

    # Create header table with styling
    header_table = Table(header_data, colWidths=[25*mm, 70*mm, 30*mm, 50*mm])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONT', (0,0), (-1,-1), 'Helvetica', 9),
        ('FONT', (1,0), (1,0), 'Helvetica-Bold', 12),  # Receipt title
        ('FONT', (-1,0), (-1,0), 'Helvetica-Bold', 10),  # Receipt number
        ('TEXTCOLOR', (0,0), (-1,-1), BRAND_BLUE),
        ('SPAN', (1,0), (2,0)),  # Merge cells for receipt title
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 10*mm))

    # Basic receipt info
    receipt_header = Table([
        ['TRACKING NUMBER:', package.tracking_code, 'SHIPPING METHOD:', package.get_mode_of_transit_display()]
    ], colWidths=[35*mm, 55*mm, 35*mm, 55*mm])
    receipt_header.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), 'Helvetica', 9),
        ('FONT', (0,0), (0,0), 'Helvetica-Bold', 9),
        ('FONT', (2,0), (2,0), 'Helvetica-Bold', 9),
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BLUE),
        ('GRID', (0,0), (-1,-1), 0.5, BRAND_BLUE),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(receipt_header)
    elements.append(Spacer(1, 5*mm))

    # Shipping details in two columns
    shipping_details = [
        ['FROM:', 'TO:'],
        [package.sender, package.receiver],
        [package.sending_location, package.receiving_location],
        [package.tel, package.email],
        ['', '']
    ]

    shipping_table = Table(shipping_details, colWidths=[90*mm, 90*mm])
    shipping_table.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), 'Helvetica', 9),
        ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 9),
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BLUE),
        ('GRID', (0,0), (-1,-1), 0.5, BRAND_BLUE),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(shipping_table)
    elements.append(Spacer(1, 5*mm))

    # Package details
    package_details = [
        ['PACKAGE DETAILS'],
        ['Description', 'Weight', 'Rate', 'Amount'],
        [package.package_name, f'{package.package_weight} kg', 
         f'${package.shipping_cost/package.package_weight:.2f}/kg', f'${package.shipping_cost:.2f}']
    ]

    package_table = Table(package_details, colWidths=[90*mm, 30*mm, 30*mm, 30*mm])
    package_table.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), 'Helvetica', 9),
        ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 9),
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BLUE),
        ('GRID', (0,0), (-1,-1), 0.5, BRAND_BLUE),
        ('PADDING', (0,0), (-1,-1), 6),
        ('SPAN', (0,0), (-1,0)),  # Merge first row
    ]))
    elements.append(package_table)
    elements.append(Spacer(1, 5*mm))

    # Totals section
    totals = [
        ['', '', 'Subtotal:', f'${package.shipping_cost:.2f}'],
        ['', '', 'Tax (10%):', f'${package.shipping_cost * 0.1:.2f}'],
        ['', '', 'Total:', f'${package.shipping_cost * 1.1:.2f}']
    ]

    totals_table = Table(totals, colWidths=[90*mm, 30*mm, 30*mm, 30*mm])
    totals_table.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), 'Helvetica', 9),
        ('FONT', (-2,0), (-2,-1), 'Helvetica-Bold', 9),
        ('ALIGN', (-2,-1), (-1,-1), 'RIGHT'),
        ('LINEABOVE', (-2,-1), (-1,-1), 1, BRAND_BLUE),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(totals_table)
    elements.append(Spacer(1, 10*mm))

    # Footer
    footer_text = '''Thank you for choosing CHASEXPRESS!
 visit www.chaselogix.com'''
    
    footer = Paragraph(
        footer_text,
        ParagraphStyle(
            'Footer',
            fontName='Helvetica',
            fontSize=8,
            textColor=BRAND_BLUE,
            alignment=1  # Center alignment
        )
    )
    elements.append(footer)

    # Build PDF
    doc.build(elements)