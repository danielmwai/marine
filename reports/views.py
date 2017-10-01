"""Reports views."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forms.models import CustomerInvoice


@login_required(login_url='/login/')
def reports(request):
    """Some default page for Bad request error page."""
    try:
        return render(request, 'reports/reports.html')
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def insurance(request):
    """Some default page for Bad request error page."""
    try:
        coid = request.user.company_id
        policies = CustomerInvoice.objects.filter(insurance_id=coid)
        return render(request, 'reports/insurance.html',
                      {'policies': policies})
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def agency(request):
    """Some default page for Bad request error page."""
    try:
        return render(request, 'reports/agents.html')
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def krakebs(request):
    """Some default page for Bad request error page."""
    try:
        return render(request, 'reports/krakebs.html')
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def regulator(request):
    """Some default page for Bad request error page."""
    try:
        return render(request, 'reports/regulator.html')
    except Exception, e:
        raise e
