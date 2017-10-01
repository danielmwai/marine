"""MINS views."""
# from reportlab.pdfgen import canvas

from decimal import Decimal
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from forms.models import (
    CustomerInvoice, CustomerPayments, HSSchedule, ISettings)
from forms.certificate import create_cert
from forms.aki_certificate import create_mcert
from forms.custom_bond import create_bond
from forms.pvcoc import create_pvcoc
from forms.eslip import create_eslip
from forms.functions import get_invoice, get_billing_info, get_bond_data
from forms.xlsreports import write_xls
from .functions import (
    get_schedules, get_data, extract_post_params, get_categories, get_duty,
    get_category, get_rate, send_notification, get_cert_info)
from payment.views import reconcile_payment
from .forms import QuoteForm
from auth.forms import VerifyForm
from simplemathcaptcha import utils


@login_required(login_url='/login/')
def dashboard(request):
    """Some default page for Bad request error page."""
    try:
        user_id = request.user.id
        invoices = CustomerInvoice.objects.filter(
            created_by_id=user_id).order_by("pay_status")
        return render(request, 'main/dashboard.html',
                      {'invoices': invoices})
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def register(request):
    """Some default page for Bad request error page."""
    try:
        return render(request, 'main/dashboard.html')
    except Exception, e:
        raise e


def get_pvcoc(request, id):
    """Get certificate."""
    params = get_invoice(request, id)
    if not params:
        return render(request, 'main/dashboard.html')
    mc_name = "CI00000000.pdf"
    file_name = 'attachment; filename="%s"' % (mc_name)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = file_name

    create_pvcoc(response, params)
    return response


def get_cert(request, id):
    """Get certificate."""
    params = get_invoice(request, id, 2)
    if not params:
        return render(request, 'main/dashboard.html')
    serial = params['serial']
    mc_name = "MCN%s.pdf" % (serial)
    file_name = 'attachment; filename="%s"' % (mc_name)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = file_name

    create_cert(response, params)
    return response


def get_mcert(request, id):
    """Get certificate."""
    params = get_invoice(request, id, 2)
    if not params:
        return render(request, 'main/dashboard.html')
    serial = params['serial']
    mc_name = "M%s.pdf" % (serial)
    file_name = 'attachment; filename="%s"' % (mc_name)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = file_name

    create_mcert(response, params)
    return response


def get_bond(request, id):
    """Get certificate."""
    # params = get_invoice(request, id)
    bdata = get_bond_data(id)
    params = {'insurance': 'Pioneer', 'serial': '12345567'}
    if bdata:
        params['insurance'] = bdata.insurance.company_name
        params['insured'] = bdata.amount
    if not params:
        return render(request, 'main/dashboard.html')
    serial = params['serial']
    mc_name = "M%s.pdf" % (serial)
    file_name = 'attachment; filename="%s"' % (mc_name)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = file_name

    create_bond(response, params)
    return response


def get_eslip(request, id):
    """Get certificate."""
    params = get_invoice(request, id)
    if not params:
        return render(request, 'main/dashboard.html')
    serial = params['serial']
    mc_name = "S%s.pdf" % (serial)
    file_name = 'attachment; filename="%s"' % (mc_name)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = file_name

    create_eslip(response, params)
    return response


@csrf_exempt
def verify(request):
    """Method to do merchant verification."""
    try:
        if request.method == 'POST':
            print request
            ref_number = request.POST.get('reference_number')
            results = get_billing_info(request, ref_number)
        else:
            results = {"message": "Invalid request", "code": 8}
        return JsonResponse(results, safe=False)
    except Exception, e:
        raise e


@csrf_exempt
def cert_verify(request):
    """Method to do merchant verification."""
    try:
        form = VerifyForm()
        code, res, msg = 9, '', 'Invalid Request'
        if request.method == 'POST':
            cert_number = request.POST.get('cert_number')
            c0 = request.POST.get('captcha_0')
            c1 = request.POST.get('captcha_1')
            h0 = utils.hash_answer(c0)
            res += '<table width="100%">'
            if c1 != h0:
                res += '<tr><td width="30%">Status:</td>'
                res += '<td width="60%">Invalid Request</td></tr>'
                res += '</table>'
                results = {"message": msg, "code": code, 'msg': res}
                return JsonResponse(results, safe=False)
            results = get_cert_info(request, cert_number)
            if results:
                code = 0
                by = results['company']
                premium = '{:20,.2f}'.format(results['premium'])
                msg = "Success"
                res += '<tr><td width="30%">Status</td>'
                res += '<td width="60%">Valid</td></tr>'
                res += '<tr><td>Insured Name</td>'
                res += '<td>%s</td></tr>' % (results['name'])
                res += '<tr><td>Insured PIN</td>'
                res += '<td>%s</td></tr>' % (results['pin'])
                res += '<tr><td>Premium</td>'
                res += '<td>%s</td></tr>' % (premium)
                res += '<tr><td>Valid Until</td><td>31-Jan-2017</td></tr>'
                res += '<tr><td>Issued By</td><td>%s</td></tr>' % (by)
            else:
                code = 8
                msg = "Failed"
                res += '<tr><td width="30%">Status:</td>'
                res += '<td width="60%">Invalid Certificate</td></tr>'
            res += '</table>'
            results = {"message": msg, "code": code, 'msg': res}
            return JsonResponse(results, safe=False)
        return render(request, 'verify.html', {'form': form})
    except Exception, e:
        print 'error getting cert - %s' % (str(e))
        raise e


def epayment(request):
    """Method to do merchant verification."""
    try:
        if request.method == 'POST':
            acc_id = 'bWFyaW5l'
            host = Site.objects.get_current()
            amnt = request.POST.get('amnt')
            # item_id = request.POST.get('id')
            txnid = request.POST.get('txid')
            pay_opt = int(request.POST.get('pay_opt'))
            amount = int(float(amnt) * 100)
            ret_url = 'https://%s/payment/' % (host)
            url = 'https://apps.kenswitch.com:8066/kenswitchpaymentsurface'
            if pay_opt == 2:
                url += '/Payment.aspx?id=%s&' % (acc_id)
                url += 'txnid=%s&amount=%s&rec_bank=34' % (txnid, amount)
                url += '&rec_acc=01001030021701&return_url=%s' % (ret_url)
            elif pay_opt == 3:
                url += '/MpesaPayment.aspx?id=%s&' % (acc_id)
                url += 'txnid=%s&amount=%s' % (txnid, amount)
                url += '&return_url=%s' % (ret_url)
            else:
                url += '/PrepareInsurancePaymentDetails.aspx'
                url += '?id=%s&txnid=%s' % (acc_id, txnid)
                url += '&return_url=%s' % (ret_url)
            results = {"message": "Success", "code": 0, 'url': url}
        else:
            results = {"message": "Invalid request", "code": 8}
        return JsonResponse(results, safe=False)
    except Exception, e:
        raise e


def quote(request):
    """Method to do merchant verification."""
    try:
        form = QuoteForm()
        categories = get_categories()
        category = ''
        goods_name = 'Goods details'
        if request.method == 'POST':
            # results = {"message": "Invalid request", "code": 8}
            equote = request.POST.get('d')
            email = request.POST.get('email')
            mobile_number = request.POST.get('mobile_number')
            if equote:
                intro = '<p>Quote # 00000</p>'
                hmsg = '%s<table width="90%%">%s</table>' % (intro, equote)
                fs = 'style="width:60%; float: left; text-align: right;"'
                vs = 'style="width:30%; float: right; text-align: right;"'
                hmsg = hmsg.replace('class="field"', fs)
                hmsg = hmsg.replace('class="value"', vs)
                hmsg = hmsg.replace('<i class="fa fa-usd"></i>', 'USD')
                hmsg = hmsg.replace(
                    'class="cart-total text-center"', 'align="right"')
                hmsg = hmsg.decode('utf-8', 'ignore')
                hmsg += '<br/><p>Yours Marine Insurer.</>'
                params = {'subject': "Marine Insurance Quotation"}
                send_notification(request, email, hmsg, params)
                results = {"message": "Invalid request", "code": 8}
                return JsonResponse(results, safe=False)
            oprice = request.POST.get('sum_assured')
            category = request.POST.get('goods_category')
            ship_mode = request.POST.get('shipping_mode')
            package_type = request.POST.get('package_type')
            ins_co = int(request.POST.get('insurance_co'))
            iprice = float(oprice.replace(',', ''))
            cid = request.POST.get('currency_id')
            cval = request.POST.get('currency_value')
            vals = {'sum_assured': iprice, 'package_type': package_type,
                    'shipping_mode': ship_mode, 'email': email,
                    'mobile_number': mobile_number, 'currency_id': cid,
                    'currency_value': cval}
            # request.POST
            price = iprice
            currency = 'KES '
            if cid and cid == 'USD':
                price = iprice * float(cval)
                currency = '<i class="fa fa-usd"></i> '
            my_rate = get_rate(ins_co, category, ship_mode, package_type)
            price = Decimal(price)
            rate = my_rate * 100
            form = QuoteForm(data=vals)
            gross = price * my_rate
            trans_ship = price * Decimal(0.00250)
            losses = price * Decimal(0.00150)
            over_age = price * Decimal(0.00185)
            stamp_duty = get_duty(ship_mode, price)
            net = gross + stamp_duty + trans_ship + losses + over_age
            # Messages
            info_m13 = ('Thank you for your enquiry. For this specific '
                        'category, we would need to speak with you directly '
                        'for more information. Kindly contact us on '
                        '+254 719 071 999')
            info_m1 = ('We are not offering cover for this types of goods. '
                       'Please check again later or contact our customer '
                       'care for help.')
            info_msg = info_m13 if ins_co == 13 else info_m1

            advert = 'img/advert.jpg' if ins_co == 13 else None

            goods_cat = get_category(category)
            if goods_cat:
                goods_name = goods_cat.category_name
            ivalue = '{:20,.2f}'.format(iprice)
            assured = '{:20,.2f}'.format(price)
            anet = '{:20,.2f}'.format(net)
            agross = '{:20,.2f}'.format(gross)
            aship = '{:20,.2f}'.format(trans_ship)
            sduty = '{:20,.2f}'.format(stamp_duty)
            alosses = '{:20,.2f}'.format(losses)
            overage = '{:20,.2f}'.format(over_age)
            value = '%s %s' % (currency, ivalue)
            amount = {'assured': assured, 'net': anet, 'gross': agross,
                      'losses': alosses, 'over_age': overage,
                      'goods': goods_name, 'ivalue': value,
                      'trans_ship': aship, 'stamp_duty': sduty}
            return render(request, 'quote.html',
                          {'form': form, 'amount': amount, 'rate': rate,
                           'categories': categories, 'category': category,
                           'info': info_msg, 'advert': advert})
        return render(request, 'quotation.html',
                      {'form': form, 'categories': categories,
                       'category': category})
    except Exception, e:
        print 'error getting quote %s' % (str(e))
        raise e


@login_required(login_url='/login/')
def payment(request):
    """Method to redirect to after payment."""
    try:
        time_now = timezone.now()
        if request.method == 'GET':
            txn_id = str(request.GET.get('txn_id'))
            ref_no = request.GET.get('pay_ref')
            error_no = request.GET.get('error_code')
            if txn_id and ref_no:
                rdata = request.GET
                invoice_no = txn_id[1:]
                inv = get_object_or_404(CustomerInvoice,
                                        invoice_no=invoice_no)
                amount = inv.payable_amount
                CustomerPayments(invoice_no=invoice_no,
                                 paid_amount=amount,
                                 payment_type=2,
                                 payment_details=str(rdata),
                                 created_at=time_now).save()
                # Reconcile
                reconcile_payment(invoice_no, amount)
                msg = "Payment was successful."
                messages.add_message(request, messages.INFO, msg)
                return HttpResponseRedirect(reverse(payment))
            elif txn_id and error_no:
                print 'Failed'
                msg = "Payment was not successful."
                messages.add_message(request, messages.ERROR, msg)
                return HttpResponseRedirect(reverse(payment))
        user_id = request.user.id
        invoices = CustomerInvoice.objects.filter(
            created_by_id=user_id, pay_status=False)
        ainvoices = CustomerInvoice.objects.filter(
            created_by_id=user_id).values_list('invoice_no', flat=True)
        payments = CustomerPayments.objects.filter(
            invoice_no__in=ainvoices)
        return render(request, 'main/payment.html',
                      {'invoices': invoices, 'payments': payments})
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def schedule(request):
    """Method to redirect to after payment."""
    try:
        # user_id = request.user.id
        admin = False
        if request.user.groups.filter(name='Admin').exists():
            admin = True
        schedules = get_schedules(request)
        return render(request, 'main/schedule.html',
                      {'schedules': schedules, 'admin': admin})
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def re_setup(request):
    """Method to redirect to after payment."""
    try:
        ins_id = request.user.company_id
        settings = ISettings.objects.filter(
            insurance_id=ins_id, is_void=False)
        admin = False
        vals = {}
        vals['INSLM'] = 'Insurance Retention Limit'
        vals['INSRL'] = 'Sum Insured Amount Over Retention Limit'
        vals['INSSR'] = 'Certificates Serial Start Range'
        vals['INSER'] = 'Certificates Serial End Range'
        if request.user.groups.filter(name='Admin').exists():
            admin = True
        return render(request, 'main/resetup.html',
                      {'admin': admin, 'settings': settings,
                       'vals': vals})
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def edit_resetup(request):
    """Method to redirect to after payment."""
    try:
        ins_id = request.user.company_id
        settings = ISettings.objects.filter(
            insurance_id=ins_id, is_void=False)
        vals = {}
        for setting in settings:
            vals[setting.setting_name] = setting.setting_value
        if request.method == 'POST':
            dts = extract_post_params(request, 'setup_')
            for dt in dts:
                setting_name = str(dt)
                setting_value = dts[setting_name][0]
                contact, created = ISettings.objects.update_or_create(
                    setting_name=setting_name, insurance_id=ins_id,
                    defaults={'setting_name': setting_name,
                              'setting_value': setting_value,
                              'insurance_id': ins_id})
            msg = 'Setup edited successfully'
            messages.info(request, msg)
            return HttpResponseRedirect(reverse(re_setup))
        admin = False
        if request.user.groups.filter(name='Admin').exists():
            admin = True
        return render(request, 'main/edit_resetup.html',
                      {'admin': admin, 'vals': vals})
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def edit_schedule(request):
    """Method to redirect to after payment."""
    try:
        # user_id = request.user.id
        ins_id = request.user.company_id
        ws = 0.0000
        if request.method == 'POST':
            for category_id in range(1, 98):
                naming = "%s_" % (str(category_id))
                dt = extract_post_params(request, naming)
                contact, created = HSSchedule.objects.update_or_create(
                    category_id=category_id, insurance_id=ins_id,
                    defaults={'category_id': category_id,
                              'sea_rate_ca': dt['sea_rate_ca'][0],
                              'sea_rate_cb': dt['sea_rate_cb'][0],
                              'sea_rate_cc': dt['sea_rate_cc'][0],
                              'sea_rate_nca': dt['sea_rate_nca'][0],
                              'sea_rate_ncb': dt['sea_rate_ncb'][0],
                              'sea_rate_ncc': dt['sea_rate_ncc'][0],
                              'air_rate': dt['air_rate'][0],
                              'road_rate': ws,
                              'rail_rate': ws,
                              'war_strike': ws,
                              'trans_ship': ws,
                              'storage_ext': ws,
                              'over_age': ws,
                              'short_landing': ws,
                              'insurance_id': ins_id},)
            msg = 'Schedule edited successfully'
            messages.info(request, msg)
            return HttpResponseRedirect(reverse(schedule))
        admin = False
        if request.user.groups.filter(name='Admin').exists():
            admin = True
        if not admin:
            return HttpResponseRedirect(reverse(schedule))
        schedules = get_schedules(request)
        return render(request, 'main/edit_schedule.html',
                      {'schedules': schedules})
    except Exception, e:
        print 'error getting schedule - %s' % (str(e))


def get_report(request, id):
    """Get certificate."""
    data = get_data(request)
    if not data:
        return render(request, 'main/dashboard.html')
    mc_name = "RI00000000.xlsx"
    file_name = 'attachment; filename="%s"' % (mc_name)
    ctype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = HttpResponse(content_type=ctype)
    response['Content-Disposition'] = file_name

    write_xls(response, data)
    return response


def handler_400(request):
    """Some default page for Bad request error page."""
    try:
        return render(request, '400.html', {'status': 400})
    except Exception, e:
        raise e


def handler_404(request):
    """Some default page for the Page not Found."""
    try:
        return render(request, '404.html', {'status': 404})
    except Exception, e:
        raise e


def handler_500(request):
    """Some default page for Server Errors."""
    try:
        return render(request, '500.html', {'status': 500})
    except Exception, e:
        raise e


def csrf_error(request, reason):
    """Some default page for Server Errors."""
    try:
        return render(request, '500.html', {'reason': reason})
    except Exception, e:
        raise e
