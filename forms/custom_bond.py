
"""Creating AKI certificate."""
from django.conf import settings
from decimal import Decimal
from num2words import num2words
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from security import BarCode
STATIC_ROOT = settings.STATICFILES_DIRS[0]


def generate_bond(response, params):
    """Method to generate certificates."""
    try:
        author = params['insurance']
        doc = SimpleDocTemplate(
            response, pagesize=A4, title="Marine Insurance",
            author=author, subject="Marine Cargo Insurance",
            creator="Marine Cargo Insurance",
            keywords="Marine Cargo Insurance",
            rightMargin=46, leftMargin=46,
            topMargin=48, bottomMargin=18)
        story = []
        # ins_address = params['insurances']
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

        t1 = Paragraph('EAST AFRICAN COMMUNITY', styles["Normal"])
        t2 = Paragraph('Form CB 1', styles["Normal"])
        titles = [[t1, t2]]

        dt = Table(titles, [5.4 * inch, 1.6 * inch], [0.9 * inch])
        story.append(dt)
        story.append(Spacer(1, 2))

        addr = [['']]
        t0 = Table(addr, 1 * [5.6 * inch])
        dt0 = [[t0, BarCode(value=params['serial'])]]
        ft0 = Table(dt0, [5.6 * inch, 1.6 * inch], [0.9 * inch])
        story.append(ft0)
        btitle = 'BOND FOR DELIVERY OF PERISHABLE OR OTHER GOODS PRIOR '
        btitle += 'TO PAYMENT OF DUTIES / TAXES'
        ptext = '<para align=center><font size=12>%s</font></para>' % (btitle)
        story.append(Paragraph(ptext, styles["Normal"]))
        story.append(Spacer(1, 12))

        cl = params['clients']
        assured = float(params['insured'])
        amnt = '{:20,.2f}'.format(assured)
        amntw = num2words(int(assured))

        bdt = 'I / We ...<strong>%s</strong>... of ....' % (cl['name'])
        bdt += '<strong>%s, ' % (cl['address'])
        bdt += 'PIN NO. %s</strong>.<br/>' % (cl['pin'])
        bdt += 'And ... of ...'
        bdt += 'hereby acknowledge than I am/we are bound to the Commissioner '
        bdt += 'in the sum of <strong>Kshs %s ' % (amnt)
        bdt += '(%s KENYA SHILLINGS ONLY) </strong>' % (amntw.upper())
        bdt += 'to be paid to the Commissioner '
        bdt += 'for which payment I/We bind myself/ourselves jointly and '
        bdt += 'for and also my/our heirs, executors, '
        bdt += 'administrators, and assigns and every of them firmly '
        bdt += 'by these presents'
        story.append(Paragraph(bdt, styles["Justify"]))
        bdate = 'Dated this ________  day of ___________'
        story.append(Spacer(1, 12))
        story.append(Paragraph(bdate, styles["Normal"]))
        story.append(Spacer(1, 12))
        bgoods = 'WHEREAS the above named has/have imported perishable '
        bgoods += 'or other goods voyage/vehicle registration, number '
        bgoods += '...... which arrived from .... on the .... day of .... '
        bgoods += 'and whereas the importer wishes to take delivery of '
        bgoods += 'those goods before payment to customs of the duties '
        bgoods += 'on such goods;'
        story.append(Paragraph(bgoods, styles["Justify"]))
        story.append(Spacer(1, 12))
        bcond = 'The condition of this obligation is such that if the above '
        bcond += 'named ..... shall deliver to the Commissioner within three '
        bcond += 'month of taking delivery of the goods imported by him/them, '
        bcond += 'Customs entries of all goods so delivered and shall pay '
        bcond += 'duties due on the those goods, then this obligation shall '
        bcond += 'be void, but otherwise shall be and remain in force.'
        story.append(Paragraph(bcond, styles["Justify"]))
        story.append(Spacer(1, 12))
        ptext = 'Signed, sealed and delivered by<br/> the above named '
        sbhf = Paragraph(ptext, styles["Normal"])
        ptext = 'in the presence of'
        sdate = Paragraph(ptext, styles["Normal"])
        dataa = [[sbhf, ''], [sdate, '']]
        ts = Table(dataa, [4.6 * inch, 2.4 * inch],
                   style=[("LINEBELOW", (1, 0), (-1, 1), .25, colors.grey)])
        story.append(ts)
        story.append(Spacer(1, 24))
        ptext = 'Signed, sealed and delivered by<br/> the above named '
        sbhf = Paragraph(ptext, styles["Normal"])
        ptext = 'in the presence of'
        sdate = Paragraph(ptext, styles["Normal"])
        dataa = [[sbhf, ''], [sdate, '']]
        ts = Table(dataa, [4.6 * inch, 2.4 * inch],
                   style=[("LINEBELOW", (1, 0), (-1, 1), .25, colors.grey)])
        story.append(ts)
        story.append(Spacer(1, 48))
        ptext = 'Approved:'
        asign = Paragraph(ptext, styles["Normal"])
        datas = [[asign, '']]
        ts = Table(datas, [4.6 * inch, 2.4 * inch],
                   style=[("LINEBELOW", (1, 0), (-1, 1), .25, colors.grey)])
        story.append(ts)
        doc.build(story)
    except Exception, e:
        print 'error generating bond - %s' % (str(e))
        raise e
    else:
        pass


def create_bond(response, params):
    """Actual method."""
    params['clients'] = {'name': 'URGENT CARGO HANDLING LTD.',
                         'address': 'P.O BOX 2121-0050 NAIROBI',
                         'pin': 'P0006000126C'}
    generate_bond(response, params)
