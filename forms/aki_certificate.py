
"""Creating AKI certificate."""
import os.path
from PIL import Image as PImage
from django.conf import settings
from decimal import Decimal
from num2words import num2words
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, Image,
    TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from security import BarCode
STATIC_ROOT = settings.STATICFILES_DIRS[0]


def generate_certificate(response, params):
    """Method to generate certificates."""
    try:
        author = params['insurance']
        doc = SimpleDocTemplate(
            response, pagesize=A4, title="Marine Insurance",
            author=author, subject="Marine Cargo Insurance",
            creator="Marine Cargo Insurance",
            keywords="Marine Cargo Insurance",
            rightMargin=48, leftMargin=48,
            topMargin=24, bottomMargin=18)
        story = []
        ins_id = params['insurance_id']
        # ins_id = ins_id if ins_id == 13 else 0
        ins_aprf = 'ICEA' if ins_id == 13 else 'XXX'
        ins_prf = 'AAR' if ins_id == 34 else ins_aprf
        logo = "%s/img/logo_%s.png" % (STATIC_ROOT, ins_id)

        if not os.path.isfile(logo):
            logo = "%s/img/logo_0.png" % (STATIC_ROOT)
        ins_address = params['insurances']
        coname = params['insurance']
        para = '<para align=center><font size=14>'
        company_name = '%s%s</font></para>' % (para, coname)
        address_parts = ["phy_addr",
                         "postal_addr", "tel", "email"]
        im = PImage.open(logo)
        imw, imh = im.size
        print imw, imh
        limw = imw / 900.0
        limh = imh * (0.9 / imw)
        print limw, limh

        im = Image(logo, limw * inch, limh * inch)
        story.append(im)
        cert_id = params['cert_id']
        cert_no = '%s/MCI/%s/%s' % (ins_prf, cert_id, params['serial'][2:])

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

        story.append(Paragraph(company_name, styles["Center"]))
        story.append(Spacer(1, 2))
        print params

        # Create return address
        inss = []
        copin = ins_address['pin'] if 'pin' in ins_address else ''
        for addr in address_parts:
            part = ins_address[addr] if addr in ins_address else addr
            addr_vl = part.strip() if part else addr
            addr_val = '<font size=10>%s</font>' % (addr_vl)
            inss.append(Paragraph(addr_val, styles["Normal"]))
        addr = [[inss]]
        t0 = Table(addr, 1 * [5.6 * inch])
        btext = "MARINE CERTIFICATE (KE)\nPolicy No: %s\n" % (params['serial'])
        btext += "Insured: %s" % (params['name'])
        dt0 = [[t0, BarCode(value=btext)]]
        ft0 = Table(dt0, [5.6 * inch, 1.6 * inch], [0.9 * inch])
        story.append(ft0)
        head = '<strong>MARINE CARGO INSURANCE CERTIFICATE</strong>'
        sagents = 'OCEANIC MARINE SURVEYORS KENYA LIMITED'
        story.append(Spacer(1, 12))
        ptext = '<para align=center><font size=14>%s</font></para>' % (head)
        story.append(Paragraph(ptext, styles["Normal"]))
        story.append(Spacer(1, 12))

        insps = '<strong>Insured:</strong> %s' % (params['name'])
        person = Paragraph(insps, styles["Normal"])
        inspn = '<strong>PIN No(s):</strong> %s' % (params['pin'])
        pin = Paragraph(inspn, styles["Normal"])
        inst = '<strong>Insured Telephone:</strong> %s' % (params['tel'])
        tel = Paragraph(inst, styles["Normal"])
        inss = '<strong>Survey Agents:</strong> %s' % (sagents)
        survey = Paragraph(inss, styles["Normal"])

        insd = [[person], [pin], [tel], [survey]]

        inst = Table(insd, 1 * [3.2 * inch])

        pnum = '00012333'
        policy = Paragraph('<strong>Policy No: </strong>', styles["Normal"])
        cert = Paragraph('<strong>Cert No.: </strong>', styles["Normal"])
        charges = Paragraph('<strong>Charges </strong>', styles["Normal"])
        currency = Paragraph('<strong>Kshs </strong>', styles["Right"])
        tcharges = Paragraph(
            '<strong>Total Charges </strong>', styles["Normal"])

        basis_totals = float(params['amount'])
        phfv = float(params['pcf'])
        tlevyv = float(params['itl'])
        sdutyv = float(params['stamp_duty'])
        #
        premium = '{:20,.2f}'.format(basis_totals)
        phff = '{:20,.2f}'.format(phfv)
        tlf = '{:20,.2f}'.format(tlevyv)
        sdf = '{:20,.2f}'.format(sdutyv)
        bp = Paragraph(str(premium), styles['Right'])
        phf = Paragraph(str(phff), styles['Right'])
        tlevy = Paragraph(str(tlf), styles['Right'])
        sduty = Paragraph(str(sdf), styles['Right'])
        btotals = basis_totals + phfv + tlevyv + sdutyv
        tpremium = '{:20,.2f}'.format(btotals)
        bpt = Paragraph('<strong>%s</strong>' %
                        (str(tpremium)), styles['Right'])
        dt = [[policy, pnum], [cert, cert_no],
              [''], [charges, currency], ['Premium', bp], ['PHF', phf],
              ['Stamp Duty', sduty], ['Training Levy', tlevy],
              [tcharges, bpt]]
        t0 = Table(dt, [1.1 * inch, 2.1 * inch],
                   style=[("LINEBELOW", (0, 0), (-1, 7), .25, colors.grey)])
        handler = params['handler'] if params['handler'] else 'N/A'
        agnt = '<strong>Agency: </strong> %s' % (handler)
        agency = Paragraph(agnt, styles["Normal"])
        agntp = '<strong>PIN: </strong> '
        agencyp = Paragraph(agntp, styles["Normal"])
        ins_co = params['insurance']
        #
        insco = '<strong>Insurance Company: </strong>%s' % (ins_co)
        insurance = Paragraph(insco, styles["Normal"])
        instp = '<strong>PIN: </strong> %s' % (copin)
        insurancep = Paragraph(instp, styles["Normal"])
        #
        cagnt = '<strong>Clearing Agent: </strong>'
        cagency = Paragraph(cagnt, styles["Normal"])
        cagntp = '<strong>PIN: </strong> '
        cagencyp = Paragraph(cagntp, styles["Normal"])
        #
        ioffice = '<strong>Issuing office: </strong>'
        issue_office = Paragraph(ioffice, styles["Normal"])
        iofficer = '<strong>Issuing officer: </strong>'
        issue_officer = Paragraph(iofficer, styles["Normal"])
        tps = [[agency, agencyp],
               [insurance, insurancep],
               [cagency, cagencyp], [issue_office], [issue_officer]]
        assured = round(float(params['insured']))
        amnt = '{:20,.2f}'.format(assured)
        amntw = num2words(int(assured))
        tpin = Table(tps, [4.4 * inch, 2.2 * inch],
                     style=[("LINEBELOW", (0, 0), (-1, 3), .25, colors.grey)])
        amount = Paragraph('Sum Insured (%s) (%s)' %
                           (amnt, amntw), styles["Normal"])
        data = [[inst, t0]]
        data2 = [[amount]]
        data3 = [[tpin]]
        #
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
        tg = Table(goods, colWidths=(0.8 * inch, 2.8 * inch,
                                     0.65 * inch, 1.3 * inch, 1.1 * inch))
        tg.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
        ]))

        data4 = [[tg]]

        fdate = '<strong>From: </strong> %s' % (params['voyage_start'])
        from_date = Paragraph(fdate, styles["Normal"])
        tdate = '<strong>To: </strong> %s' % (params['voyage_end'])
        to_date = Paragraph(tdate, styles["Normal"])
        #
        vsel = '<strong>Vessel: </strong> N/A'
        vessel = Paragraph(vsel, styles["Normal"])
        loadp = '<strong>Loading at: </strong> %s' % (params['port'])
        origin = Paragraph(loadp, styles["Normal"])
        #
        dport = '<strong>Port of Discharge: </strong> MOMBASA'
        port = Paragraph(dport, styles["Normal"])
        tship = '<strong>Transshipping: </strong> '
        trans_ship = Paragraph(tship, styles["Normal"])
        data5 = [[from_date, to_date],
                 [vessel, origin],
                 [port, trans_ship]]
        data6 = [['S/No.', 'Marks', 'Description of Goods']]

        t1 = Table(data, 2 * [3.3 * inch])
        t1.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
        t2 = Table(data2, 1 * [6.4 * inch])
        t3 = Table(data3, 2 * [3.3 * inch])
        t4 = Table(data4, 2 * [3.3 * inch])
        t5 = Table(data5, 2 * [3.3 * inch],
                   style=[("LINEBELOW", (0, 0), (-1, 1), .25, colors.grey)])
        t6 = Table(data6, 2 * [1.65 * inch] + [3.3 * inch])
        data0 = [[t1], [t2], [t3], [t4], [t5], [t6]]
        t = Table(data0, 1 * [6.9 * inch],
                  style=[('BOX', (0, 0), (-1, -1), 2, colors.black),
                         ('INNERGRID', (0, 0), (0, -1), 1, colors.grey),
                         ('BOX', (0, 0), (-1, -1), 0.25, colors.grey),
                         ('BOX', (0, 0), (0, -1), 0.25, colors.grey)
                         ])
        story.append(t)
        story.append(Spacer(1, 12))
        ptext = 'Signed on behalf of'
        sbhf = Paragraph(ptext, styles["Normal"])
        ptext = 'Date of issue'
        sdate = Paragraph(ptext, styles["Normal"])
        dataa = [[sbhf, ''], [sdate, params['cert_date']]]
        ts = Table(dataa, [2.4 * inch, 4.4 * inch],
                   style=[("LINEBELOW", (1, 0), (-1, 1), .25, colors.grey)])
        story.append(ts)
        story.append(Spacer(1, 24))
        ptext = 'AUTHORIZED SIGNATORY'
        asign = Paragraph(ptext, styles["Normal"])
        datas = [[asign, '']]
        ts = Table(datas, [2.4 * inch, 4.4 * inch],
                   style=[("LINEBELOW", (1, 0), (-1, 1), .25, colors.grey)])
        story.append(ts)
        doc.build(story)
    except Exception, e:
        print 'error generating certificate - %s' % (str(e))
        raise e
    else:
        pass


def create_mcert(response, params):
    """Actual method."""
    params['period'] = '%s to %s' % (params['voyage_start'],
                                     params['voyage_end'])
    generate_certificate(response, params)
