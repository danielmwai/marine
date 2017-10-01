"""PVCOC document."""
from decimal import Decimal
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import (
    Image, Paragraph, SimpleDocTemplate, Table)
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.conf import settings
from .certificate import BarCode

STATIC_ROOT = settings.STATICFILES_DIRS[0]


def create_eslip(response, params):
    """Method to create PVCOC document."""
    try:
        doc = SimpleDocTemplate(response, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        elements = []
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))

        logo = "%s/img/kenswitch.jpg" % (STATIC_ROOT)

        img = Image(logo)
        img.drawHeight = 0.9 * inch
        img.drawWidth = 3.2 * inch
        # Other details
        cus_name = Paragraph('''
                   <para>%s</para>
                   ''' % (params['name']), styles["BodyText"])
        ins_name = Paragraph('''
                   <para>%s</para>
                   ''' % (params['insurance']), styles["BodyText"])
        handler_name = Paragraph('''
                   <para>%s</para>
                   ''' % (params['handler']), styles["BodyText"])

        data0 = [['INSURED NAME', cus_name,
                  '', 'PIN NO: %s' % (params['pin'])]]

        data1 = [['INSURANCE FIRM', ins_name, handler_name],
                 ['INVOICE NO.', params['serial'], ''],
                 ['BANK', params['bank'], BarCode(value=params['serial'])]]

        header = [[img]]

        data = [['', '', '', ''],
                ['HS Code', 'Quantity', 'Product', 'Premium']]

        items = params['goods']
        grand_total = 0
        premium_total = 0
        for item in items:
            print item
            row = []
            desc = Paragraph(item[1], styles['Normal'])
            row.append(item[0])
            row.append(item[2])
            row.append(desc)
            total = Decimal(str(item[3])) * Decimal(str(item[2]))
            prem = Decimal(str(item[4])) * total
            mt = '{:20,.2f}'.format(total)
            mp = '{:20,.2f}'.format(prem)
            premium = Paragraph(str(mp), styles['Right'])
            totals = Paragraph(str(mt), styles['Right'])
            print totals
            # row.append(totals)
            row.append(premium)
            grand_total += total
            premium_total += prem
            data.append(row)
        gt = '{:20,.2f}'.format(grand_total)
        pt = '{:20,.2f}'.format(premium_total)
        gtotal = Paragraph(str(gt), styles['Right'])
        ptotal = Paragraph(str(pt), styles['Right'])
        gt = '{:20,.2f}'.format(grand_total)
        gtotal = Paragraph(str(gt), styles['Right'])
        print gtotal
        data.append(["", "TOTALS", "", ptotal])
        th = Table(header, colWidths=(7.2 * inch))
        t = Table(data, 4 * [1.8 * inch],
                  style=[('BOX', (0, 0), (-1, -1), 2, colors.black),
                         ('GRID', (0, 1), (-1, -1),
                          0.5, colors.black),
                         ('SPAN', (0, 0), (1, 0)),
                         ('SPAN', (3, 0), (3, 0)),
                         ('ALIGN', (1, 0),
                          (3, -1), 'CENTER')
                         ])
        # Other details for customer
        t0 = Table(data0, [1.9 * inch] + [2.2 * inch] + 2 * [1.6 * inch],
                   1 * [0.2 * inch])

        t1 = Table(data1, [1.9 * inch] + [2.2 * inch] + [3.2 * inch],
                   3 * [0.4 * inch])
        elements.append(th)
        elements.append(t0)
        elements.append(t1)
        elements.append(t)
        doc.build(elements)
    except Exception, e:
        print "error creating pvcoc - %s" % (str(e))
    else:
        pass
    finally:
        pass
