"""Test pdf."""
from decimal import Decimal

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Paragraph, Table, Frame, TableStyle, Spacer)

# Security
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF


def coord(height, x, y, unit=1):
    """For cordinates."""
    x, y = x * unit, height - y * unit
    return x, y


def mypdf():
    """Test pdf."""
    try:
        pdf_file = 'test.pdf'
        canv = canvas.Canvas(pdf_file, pagesize=letter)
        width, height = letter
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))

        stylen = styles["BodyText"]
        story = []

        items = [[1, 'test 1', 500.50, 5], [1, 'test 2', 500.50, 5]]

        address = """ <font size="9">
        NAME : %s </font>""" % ('Wanjiku Customer')

        story.append(Paragraph(address, styles["Normal"]))

        story.append(Spacer(1, 36))

        order_number = '<para align=center><font size="14">'
        order_number += '<b>MARINE COVER NOTE</b></font></para>'

        story.append(Paragraph(order_number, styles["Normal"]))
        story.append(Spacer(1, 24))

        summary = '''
            <b>Summary of Cover : </b><br />
            All real and personal property of the Insured, of every kind,
            nature and description including new machinery and spare parts
            and / or second hand machinery packed in cartons and/or pallets
            and/or cases and / or approved packing and / or the Assureds'
            interest in liability for the property of others when held in
            trust, on commissions, sold but not delivered, on
           consignment of storage for processing repairs or alterations, under
           contract of purchase, under lease, or when the Assured has assumed
           or wishes to assume liability or is otherwise therefore or has
           agreed to carry inspection thereon.'''

        story.append(Paragraph(summary, styles["Justify"]))
        story.append(Spacer(1, 12))

        interest = '''
            <para align=center><b>INTEREST AND SUMS INSURED</b></para>'''
        story.append(Paragraph(interest, styles["Normal"]))
        story.append(Spacer(1, 12))

        period = '''
            <para><b>PERIOD :</b> %s</para>'''
        story.append(Paragraph(period, styles["Normal"]))
        story.append(Spacer(1, 12))

        limits = '''
            <para><b>Limits of Liability As per proforma Invoice :
            </b><br/></para>'''
        story.append(Paragraph(limits, styles["Normal"]))
        story.append(Spacer(1, 12))

        data = []

        data.append(["Item ID", "Description", "Price", "Quantity", "Total"])
        grand_total = 0

        for item in items:
            row = []
            desc = Paragraph(item[1], stylen)
            row.append(item[0])
            row.append(desc)
            row.append(item[2])
            row.append(item[3])
            total = Decimal(str(item[2])) * Decimal(str(item[2]))
            row.append(str(total))
            grand_total += total
            data.append(row)
        data.append(["", "Grand Total:", "", "", grand_total])
        t = Table(data, colWidths=(0.6 * inch, 3.4 * inch,
                                   1.0 * inch, 0.8 * inch, 1.0 * inch))
        t.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
        ]))
        story.append(t)

        other_info = '''
            <para><b>EXCESS :</b><br/>
            <b>PACKAGING :</b> Approved Packing<br/>
            <b>BASIS OF VALUATION : </b>FOB  PLUS Duty / Vat Plus 10% on the
            whole<br/><b>CONVEYANCE :</b> Approved vessel and/or Dhow and /or
            Airfreight /Parcel Post and or Rail and/or Road and/or
            Conveyances</para>
            '''
        story.append(Paragraph(other_info, styles["Normal"]))
        story.append(Spacer(1, 12))

        conditions = '''
            <para><b>Conditions :</b><br/>
            1. Institute standard conditions for cargo contracts<br/>
            2. Institute cargo clauses "A"<br/>
            3. Institute war clauses (cargo)<br/>
            4. Institute strikes clause (cargo)<br/>
            5. Institute war clauses (sending by post)<br/>
            6. Institute cargo clause (Air)<br/>
            7. Institute war clause (air cargo) and/or institute strike
            Clauses (Air Cargo)<br/>8. Institute replacement clause<br/>
            9. Institute classification clause<br/>
            10. Institute theft, pilferage, and non-delivery<br/>
            11. Bailee Clause<br/>
            12. Duty clause - including loss and expense incurred by the
            assured occasioned by circumstances outside their control to
            substantiate any claim for rebate of duty<br/>
            13. Deck cargoes other than containerized held covered<br/>
                   </para>'''
        story.append(Paragraph(conditions, styles["Normal"]))
        story.append(Spacer(1, 12))

        taxes = '''
            <para><b>PREMIUM & TAXES </b></para>'''
        story.append(Paragraph(taxes, styles["Normal"]))
        story.append(Spacer(1, 12))

        prems = []
        prems.append(["", "", "Total Premium", "10.00"])
        tp = Table(prems, 4 * [1.8 * inch])
        story.append(tp)

        taxs = []
        taxs.append(["Total Tax", "10.00", "Excise", "10.00"])
        tx = Table(taxs, 4 * [1.8 * inch])
        story.append(tx)

        report_url = 'THISSSSSSSS'
        qr_code = qr.QrCodeWidget(report_url)
        bounds = qr_code.getBounds()
        qwidth = bounds[2] - bounds[0]
        qheight = bounds[3] - bounds[1]
        d = Drawing(45, 45, transform=[45 / qwidth, 0, 0, 45. / qheight, 0, 0])
        d.add(qr_code)
        renderPDF.draw(d, canv, width - 100, height - 100)

        txt = "Thank you for your business!"
        story.append(Spacer(1, 24))
        story.append(Paragraph(txt, styles["Normal"]))

        f = Frame(0.55 * inch, inch, 7.0 * inch, 9.2 * inch, showBoundary=0)
        f.addFromList(story, canv)
        canv.save()
    except Exception, e:
        print 'Error - %s' % (str(e))


if __name__ == '__main__':
    mypdf()
