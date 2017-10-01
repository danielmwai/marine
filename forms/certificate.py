"""Cert generation."""
from decimal import Decimal
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, Paragraph, TableStyle)
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from security import BarCode


class Canvas(canvas.Canvas):
    """Pagination extention for canvas."""

    def __init__(self, *args, **kwargs):
        """Constructor for my pagination."""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        """Get the pages first."""
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """To add page info to each page (page x of y)."""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        """Draw the final page."""
        self.setFont("Times-Roman", 7)
        self.drawRightString(20 * cm, 1 * cm,
                             "Page %d of %d" % (self._pageNumber, page_count))


def create_certificate(response, params):
    """Method for generation."""
    try:
        author = "Cargo Insurity"
        doc = SimpleDocTemplate(
            response, pagesize=letter, title="Marine Insurance", author=author,
            subject="Cargo Insurity", creator="Cargo Insurity",
            keywords="Marine Insurance", rightMargin=72, leftMargin=72,
            topMargin=72, bottomMargin=48)
        # container for the 'Flowable' objects

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))

        styler = styles['Right']
        elements = []

        header = Paragraph('''
                   <para align=center><font size=18><b>MARINE INSURANCE
                   COVER NOTE</b></font></para<br/><br/>
                   ''', styles["BodyText"])

        p0 = Paragraph('''
                   <para align=center><b>MARINE CERTIFICATE</b></para>
                   ''', styles["BodyText"])

        p1 = Paragraph('''
         <b>Summary of Cover : </b><br />
         All real and personal property of the Insured, of every kind,
         nature and description including new machinery and spare parts and
         / or second hand machinery packed in cartons and/or pallets and/or
         cases and / or approved packing and / or the Assureds' interest in
         liability for the property of others when held in trust, on
         commissions, sold but not delivered, on
         consignment of storage for processing repairs or alterations, under
         contract of purchase, under lease, or when the Assured has assumed or
         wishes to assume liability or is otherwise therefore or has agreed
                 to carry inspection thereon.''',
                       styles["Justify"])

        p2 = Paragraph('''
                   <para align=center><b>INTEREST AND SUMS INSURED</b></para>
                   ''', styles["BodyText"])

        p3 = Paragraph('''
                   <para><b>PERIOD :</b> %s</para>
                   ''' % (params['period']), styles["BodyText"])
        port = Paragraph('''
            <para><b>COUNTRY OF ORIGIN : </b> %s; <b>PORT : </b>%s</para>
            ''' % (params['country'], params['port']), styles["BodyText"])

        p4 = Paragraph('''
                   <para><b>Limits of Liability As per proforma Invoice :
                   </b><br/><br/></para>''', styles["BodyText"])

        p4a = Paragraph('''
                   <para><br/><b>BASIS OF SUM INSURED :</b></para>
                   ''', styles["BodyText"])

        p5 = Paragraph('''
                   <para><br/><b>EXCESS :</b></para>
                   ''', styles["BodyText"])

        p6 = Paragraph('''
                   <para><b>PACKAGING :</b> Approved Packing</para>
                   ''', styles["BodyText"])

        p7 = Paragraph('''
                   <para><b>BASIS OF VALUATION : </b>FOB  PLUS Duty
                   / Vat Plus 10% on the whole</para>
                   ''', styles["BodyText"])

        p8 = Paragraph('''
                   <para><b>CONVEYANCE :</b> Approved vessel and/or Dhow and
                   /or Airfreight /Parcel Post and or Rail and/or Road and/or
                   Conveyances</para>
                   ''', styles["BodyText"])

        p9 = Paragraph('''
                   <para><b>VOYAGE :</b> Form any Port and/or places in the
                   World to final destination in East Africa including inland
                   transit. Covered up to 30 days after completion of discharge
                   from carrying vessel AND/OR from East Africa to places
                   Worldwide</para>
                   ''', styles["BodyText"])

        p10 = Paragraph('''
         <para><b>
         Conditions :</b><br/>
          1. Institute standard conditions for cargo contracts<br/>
          2. Institute cargo clauses "A"<br/>
          3. Institute war clauses (cargo)<br/>
          4. Institute strikes clause (cargo)<br/>
          5. Institute war clauses (sending by post)<br/>
          6. Institute cargo clause (Air)<br/>
          7. Institute war clause (air cargo) and/or institute
          strike Clauses (Air Cargo)<br/>
          8. Institute replacement clause<br/>
          9. Institute classification clause<br/>
          10. Institute theft, pilferage, and non-delivery<br/>
          11. Bailee Clause<br/>
          12. Duty clause - including loss and expense incurred by the assured
          occasioned by circumstances outside their control to substantiate
          any claim for rebate of duty<br/>
          13. Deck cargoes other than containerized held covered<br/>
         </para>
         ''', styles["BodyText"])

        p11 = Paragraph('''
                   <para align=center><b>PREMIUM & TAXES </b></para>
                   ''', styles["BodyText"])
        cus_name = Paragraph('''
                   <para>%s</para>
                   ''' % (params['name']), styles["BodyText"])
        ins_name = Paragraph('''
                   <para>%s</para>
                   ''' % (params['insurance']), styles["BodyText"])
        handler = params['handler']
        bagent = 'N/A' if not handler else handler
        handler_name = Paragraph('''
                   <para>%s</para>
                   ''' % (bagent), styles["BodyText"])

        data0 = [['INSURED NAME', cus_name,
                 'PIN NO', params['pin']]]
        datai = [['INSURANCE FIRM', ins_name, ''],
                 ['BROKER / AGENT', handler_name]]

        btext = "MARINE COVER NOTE (KE)\nSerial No: %s\n" % (params['serial'])
        btext += "Insured: %s" % (params['name'])

        data = [['CERTIFICATE SERIAL NO.', params['serial'],
                BarCode(value=btext)]]

        data2 = [[p0], [p1], [p2], [p3], [port], [p4]]
        data2a = [[p4a]]

        data22 = [[p5], [p6], [p7], [p8], [p9], [p10]]

        data3 = [[p11]]

        goods = []

        goods.append(["HS Code", "Description of Items Insured",
                      "Quantity", "Sum Insured", "Premium"])
        grand_total = 0
        premium_total = 0

        items = params['goods']

        for item in items:
            row = []
            desc = Paragraph(item[1], styles['Normal'])
            row.append(item[0])
            row.append(desc)
            row.append(item[2])
            total = Decimal(str(item[3])) * Decimal(str(item[2]))
            prem = Decimal(str(item[4])) * total
            mt = '{:20,.2f}'.format(total)
            mp = '{:20,.2f}'.format(prem)
            premium = Paragraph(str(mp), styles['Right'])
            totals = Paragraph(str(mt), styles['Right'])
            row.append(totals)
            row.append(premium)
            grand_total += total
            premium_total += prem
            goods.append(row)
        gt = '{:20,.2f}'.format(grand_total)
        pt = '{:20,.2f}'.format(premium_total)
        gtotal = Paragraph(str(gt), styles['Right'])
        ptotal = Paragraph(str(pt), styles['Right'])
        goods.append(["", "TOTALS", "", gtotal, ptotal])
        tg = Table(goods, colWidths=(0.9 * inch, 2.8 * inch,
                                     0.65 * inch, 1.5 * inch, 1.2 * inch))
        tg.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
        ]))
        pmk = ['premium', 'stamp_duty', 'itl', 'pcf', ]
        pms = {0: 'Premium', 1: 'Stamp Duty', 2: 'Training Levy',
               3: 'Policy Holders Fund'}

        charges = []
        p_total = 0
        for pm in pms:
            vl = params[pmk[pm]]
            val = '{:20,.2f}'.format(vl)
            p_total += vl
            charges.append(['', '', pms[pm], Paragraph(str(val), styler)])
        ptotal = '{:20,.2f}'.format(p_total)
        desc = Paragraph(str(ptotal), styles['Right'])
        charges.append(['', '', 'Total Premium', desc])

        txs = {1: "Import Duty", 2: "Excise Duty",
               3: "Railway Development Levy",
               4: "Sugar Development Levy",
               5: "Value Added Tax"}
        all_tax = params['taxes']
        taxes = []
        t_total = 0
        mf = '<font size="8">%s</font>'
        for i in range(1, 6):
            if i in all_tax:
                if all_tax[i] > 0:
                    al = all_tax[i]
                    vall = '{:20,.2f}'.format(al)
                    t_total += al
                    taxes.append([txs[i],
                                  Paragraph(mf % (str(vall)), styler)])
            if i == 5:
                vat = (grand_total + t_total) * Decimal(0.1600)
                t_total += vat
                vatl = '{:20,.2f}'.format(vat)
                taxes.append([txs[i],
                              Paragraph(mf % (str(vatl)), styler)])
        ttotal = '{:20,.2f}'.format(t_total)
        tesc = Paragraph(mf % (str(ttotal)), styles['Right'])
        taxes.append(['Total Estimated Taxes', tesc])

        freight_cost = params['freight']
        basis_t = '{:20,.2f}'.format(t_total)
        basis_f = '{:20,.2f}'.format(freight_cost)
        basis_totals = t_total + freight_cost + grand_total
        basis_tt = '{:20,.2f}'.format(basis_totals)

        bf = Paragraph(str(basis_f), styles['Right'])
        bt = Paragraph(str(basis_t), styles['Right'])
        btt = Paragraph(str(basis_tt), styles['Right'])
        basis = [['Cost of Goods', gtotal], ['Freight Charges', bf],
                 ['Taxes', bt], ['Total', btt]]

        t0 = Table(data0, [1.9 * inch] + [3.6 * inch] + [0.6 * inch] + [1.2 * inch],
                   1 * [0.4 * inch])
        ti = Table(datai, [1.9 * inch] + [3.2 * inch] + [2.2 * inch],
                   2 * [0.3 * inch])

        t = Table(data, [1.9 * inch] + [3.8 * inch] + [1.6 * inch],
                  1 * [0.3 * inch])

        t1 = Table(basis, 2 * [3.6 * inch])

        t2 = Table(data2, 1 * [7.2 * inch])
        t2.setStyle(TableStyle(
            [('BACKGROUND', (0, 0), (-1, -6), '#cbcbcb'),
             ('BACKGROUND', (0, 2), (-1, -4), '#cbcbcb')]))

        t2a = Table(data2a, 1 * [7.2 * inch])

        t22 = Table(data22, 1 * [7.2 * inch])

        t3 = Table(data3, 1 * [7.2 * inch])
        t3.setStyle(TableStyle(
            [('BACKGROUND', (0, 0), (-1, -1), '#a7a5a5')]))

        t4 = Table(charges, 4 * [1.8 * inch])

        t5 = Table(taxes, 2 * [3.6 * inch])
        t5.setStyle(TableStyle([('FONTSIZE', (0, 0), (-1, -1), 8),
                                ("LINEBELOW", (0, 0), (-1, -1), 1,
                                 '#f3eded')]))

        hr = Paragraph("<br/><br/>", styles['Normal'])

        tax_sum = Paragraph('''
                   <para><b>TAX ESTIMATES</b></para>
                   ''', styles["BodyText"])
        data_sum = [[tax_sum]]
        t_sum = Table(data_sum, 1 * [7.2 * inch])
        t_sum.setStyle(TableStyle(
            [("LINEABOVE", (0, 0), (-1, -1), 2, colors.black)]))

        th = Table([[header]], [7.2 * inch], [0.2 * inch])

        elements.append(th)
        elements.append(hr)
        elements.append(t0)
        elements.append(ti)
        elements.append(t)
        elements.append(hr)
        elements.append(t2)
        elements.append(tg)
        elements.append(t2a)
        elements.append(t1)
        elements.append(t22)
        elements.append(t3)
        elements.append(t4)
        elements.append(hr)
        elements.append(t_sum)
        elements.append(hr)
        elements.append(t5)
        doc.build(elements, canvasmaker=Canvas)
    except Exception as e:
        raise e


def create_cert(response, params):
    """Actual method."""
    print params
    params['period'] = '%s to %s' % (params['voyage_start'],
                                     params['voyage_end'])
    create_certificate(response, params)


if __name__ == '__main__':
    create_cert('test.pdf')
    print 'done'
