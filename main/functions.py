"""Common functions."""
from django.shortcuts import get_object_or_404
from forms.models import HSSchedule, HSCategory, CustomerInvoice
from auth.emails import send_email


def send_notification(request, email, hmsg, params):
    """Method to send out emails."""
    try:
        msg = ''
        send_email(email, msg, hmsg, params=params)
    except Exception, e:
        print 'error sending email - %s' % (str(e))


def get_cert_info(request, cert_number):
    """Method to verify certificate."""
    try:
        results = {}
        result = get_object_or_404(CustomerInvoice,
                                   invoice_no=cert_number)
        if result:
            results['company'] = result.insurance.company_name
            results['premium'] = result.total_premium
            person = result.person.regperson
            if person.id:
                name = person.full_name
                pin = person.pin_number.upper()
            else:
                company = result.regcompany
                name = company.company_name
                pin = company.pin_number
            results['name'] = name
            results['pin'] = pin
    except Exception, e:
        print 'error checking certificate - %s' % (str(e))
        return {}
    else:
        return results


def get_rate(ins_co, category, ship_mode, package_type, cover='a'):
    """Method to get the rate per underwriter."""
    try:
        rate = 0.00000
        schedule = get_object_or_404(HSSchedule,
                                     insurance_id=ins_co, category_id=category)
        if schedule:
            if int(ship_mode) == 2:
                rate = schedule.air_rate
            else:
                if int(package_type) == 1:
                    cname = 'sea_rate_c%s' % (cover)
                    rate = getattr(schedule, cname)
                else:
                    cname = 'sea_rate_nc%s' % (cover)
                    rate = getattr(schedule, cname)
    except Exception, e:
        print 'No schedule for this item  %s' % (str(e))
        return 0.00000
    else:
        return rate


def get_schedules(request):
    """Method to get request."""
    try:
        rates = ['sea_rate_ca', 'sea_rate_cb', 'sea_rate_cc',
                 'sea_rate_nca', 'sea_rate_ncb', 'sea_rate_ncc',
                 'air_rate']
        ins_id = request.user.company_id
        schedules = HSSchedule.objects.filter(
            insurance_id=ins_id).order_by('id')
        if not schedules:
            scds = HSCategory.objects.all().order_by('id')
            schedules = []
            for scd in scds:
                schedule = {}
                schedule['category_id'] = scd.id
                schedule['category_name'] = scd.category_name
                for rt in rates:
                    schedule[rt] = '0.00000'
                schedules.append(schedule)
            # schedules.c1_sea_rate_ca = 0.00000
    except Exception, e:
        raise e
    else:
        return schedules


def get_data(request):
    """Method to get data."""
    try:
        dts = []
        dts.append(['#', 'Section Name', 'Category Name'])
        data = get_schedules(request)
        cnt = 0
        for dt in data:
            cnt += 1
            dts.append([cnt, dt.category.section.section_name,
                        dt.category.category_name])

    except Exception, e:
        raise e
    else:
        return dts


def extract_post_params(request, naming='cc_'):
    """Extract from POST params values starting with some naming."""
    try:
        reqs = request.POST
        req_vals = {}
        for req in reqs:
            val = request.POST.get(req).strip()
            if req.startswith(naming):
                vals = req.split(naming)
                if len(vals) > 2:
                    cid, cvalue = vals[1], vals[2]
                    if cid not in req_vals:
                        req_vals[cid] = {}
                    if len(req_vals) > 0:
                        req_vals[cid][cvalue] = val
                    else:
                        req_vals[cid] = {cvalue: val}
                else:
                    cid = vals[1]
                    req_vals[cid] = val.split(',')
        return req_vals
    except Exception, e:
        raise e


def get_category(cat_id):
    """Get category details."""
    try:
        category = HSCategory.objects.get(pk=int(cat_id))
    except Exception, e:
        print 'error getting category - %s' % (str(e))
        return 0
    else:
        return category


def get_categories():
    """Method to get all cateogories."""
    try:
        myvars = {}
        sdet = {}
        items = HSCategory.objects.all()
        vals = '<option value="">Please Select Category</option>'
        for item in items:
            section_id = item.section_id
            gname = repr(item.section.section_name)
            gname = gname.replace("u'", "").replace("'", "")
            sdet[section_id] = gname
            category_id = item.id
            category_name = item.category_name
            gcat = {'id': category_id, 'name': category_name}
            if section_id not in myvars:
                myvars[section_id] = [gcat]
            else:
                myvars[section_id].append(gcat)
        for var in myvars:
            otitle = sdet[var]
            otl = len(otitle)
            tshort = '%s ...' % (otitle[:100]) if otl > 100 else otitle
            vals += '<optgroup label="%s" title="%s">' % (tshort, otitle)
            gitems = myvars[var]
            for i, itm in enumerate(gitems):
                gname = repr(itm['name'])
                gname = gname.replace("u'", "").replace("'", "")
                itm_id = itm['id']
                itl = len(gname)
                itms = '%s ...' % (gname[:100]) if itl > 100 else gname
                vals += '<option value="%s" title="%s">%s</option>' % (
                    itm_id, gname, itms)
            vals += '</optgroup>'
    except Exception, e:
        raise e
    else:
        return vals


def myround(x, base=5):
    """Round to the nearest five."""
    try:
        return int(base * round(float(x) / base))
    except Exception, e:
        print 'error rounding to 5 - %s' % (str(e))
        return 0


def get_duty(freight, sum_assured):
    """Method to calculate duty."""
    try:
        min_val = 40
        freight_type = int(freight)
        if freight_type == 2:
            duty_cost = min_val
        else:
            value_cost = (sum_assured / 10000) * 5
            sea_cost = myround(value_cost)
            duty_cost = min_val if sea_cost < min_val else sea_cost
    except Exception, e:
        print 'error getting duty - %s' % (str(e))
        return 0
    else:
        return duty_cost
