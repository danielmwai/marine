"""Method to write excel files."""
from openpyxl import Workbook


def write_xls(response, data):
    """Method to write excel."""
    try:
        wb = Workbook()
        ws = wb.active
        for dt in data:
            ws.append(dt)
        # Save the file
        wb.save(response)
    except Exception, e:
        print "error creating excel - %s" % (str(e))
        raise e
    else:
        pass
