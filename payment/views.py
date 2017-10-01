"""Payments module."""
import json
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from forms.models import (
    MpesaPayments, CustomerPayments, CustomerInvoice)


@csrf_exempt
def payments(request):
    """Method for payment callback."""
    try:
        if request.method == 'POST':
            rdata = json.loads(request.body)
            if rdata:
                time_now = timezone.now()
                amount = float(rdata['transAmount']) * 1.0000
                MpesaPayments(trans_amount=amount,
                              first_name=rdata['firstname'],
                              last_name=rdata['lastname'],
                              trans_time=rdata['transTime'],
                              trans_type=rdata['transType'],
                              trans_id=rdata['transId'],
                              response_id=rdata['Id'],
                              msisdn=rdata['msisdn'],
                              created_at=time_now,
                              bill_ref_no=rdata['billRefNumber']).save()
                # More details to payment table
                invoice_no = rdata['billRefNumber'][1:]
                CustomerPayments(invoice_no=invoice_no,
                                 paid_amount=amount,
                                 payment_type=1,
                                 payment_details=str(rdata),
                                 created_at=time_now).save()
                reconcile_payment(invoice_no, amount)
            results = {"responseDesc": "OK", "responseCode": 0}
        else:
            results = {"responseDesc": "Invalid request", "responseCode": 8}
        return JsonResponse(results, safe=False)
    except Exception, e:
        print 'error - %s' % (str(e))
        results = {"responseDesc": "Invalid Payload", "responseCode": 9}


@csrf_exempt
def kenpay(request):
    """Method for payment callback."""
    try:
        if request.method == 'POST':
            rdata = json.loads(request.body)
            if rdata:
                time_now = timezone.now()
                if 'reference_number' in rdata and 'amount' in rdata:
                    # Handle success
                    invoice_no = rdata['reference_number'][1:]
                    amount = float(rdata['amount']) * 1.0000
                    CustomerPayments(invoice_no=invoice_no,
                                     paid_amount=amount,
                                     payment_type=3,
                                     payment_details=str(rdata),
                                     created_at=time_now).save()
                    reconcile_payment(invoice_no, amount)
                    results = {"responseDesc": "OK", "responseCode": 0}
                else:
                    results = {"responseDesc": "Missing Parameters",
                               "responseCode": 6}
            else:
                results = {"responseDesc": "Missing Key Parameters",
                           "responseCode": 7}
        else:
            results = {"responseDesc": "Invalid request", "responseCode": 8}
        return JsonResponse(results, safe=False)
    except Exception, e:
        print 'error - %s' % (str(e))
        results = {"responseDesc": "Invalid Payload", "responseCode": 9}


def reconcile_payment(invoice_no, amount):
    """Method to calculate if customer has paid."""
    try:
        time_now = timezone.now()
        invoice = CustomerInvoice.objects.get(invoice_no=invoice_no)
        payable_amount = invoice.payable_amount
        paid = invoice.paid_amount

        new_paid = paid + amount
        pay_status = True if new_paid >= payable_amount else False

        invoice.paid_amount = new_paid
        invoice.pay_status = pay_status
        invoice.paid_at = time_now
        invoice.save(update_fields=["pay_status", "paid_amount", "paid_at"])
    except Exception, e:
        raise e
    else:
        pass
