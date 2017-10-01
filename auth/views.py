"""AUTH views."""
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, VerifyForm
from main.views import dashboard
from forms.models import RegPerson, RegCompany, UserCompany
from forms.functions import get_persons
from .functions import (
    send_verification, create_account, perform_verification)
from django.conf import settings
from main.forms import QuoteForm
from main.functions import get_categories


def log_in(request):
    """Method to handle log in to system."""
    try:
        categories = get_categories()
        qform = QuoteForm()
        vform = VerifyForm()
        params = {'categories': categories, 'qform': qform, 'vform': vform}
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            params['form'] = form
            if form.is_valid():
                email = form.data['email'].strip()
                password = form.data['password'].strip()
                user = authenticate(email=email, password=password)
                if user is not None:
                    if user.is_active:
                        if not user.email_verified:
                            params['email'] = True
                            msg = ("Email address has not been verified. "
                                   "Click on Send Link button to resend "
                                   "verification email.")
                            messages.add_message(request, messages.ERROR, msg)
                            return render(request, 'login.html', params)
                        else:
                            login(request, user)
                            # grps = user.groups.all()
                            request.session['names'] = email
                            next_param = request.GET
                            print next_param
                            if 'next' in next_param:
                                next_page = next_param['next']
                                print 'NEXT PAGE', next_page
                                if '/login' not in next_page:
                                    return HttpResponseRedirect(next_page)
                            return HttpResponseRedirect(reverse(dashboard))
                    else:
                        msg = "Account is disabled awaiting approvals."
                        messages.add_message(request, messages.ERROR, msg)
                        return render(request, 'login.html', params)
                else:
                    msg = "Incorrect username and / or password."
                    messages.add_message(request, messages.ERROR, msg)
                    return render(request, 'login.html', params)
        else:
            form = LoginForm()
            params['form'] = form
            logout(request)
        return render(request, 'login.html', params)
    except Exception, e:
        print 'Error login - %s' % (str(e))
        raise e


def log_out(request):
    """Method to handle log out to system."""
    try:
        url = '/'
        logout(request)
        msg = 'You have successfully logged out.'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(url)
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def profile(request):
    """Method to handle log out to system."""
    try:
        account_id = request.user.id
        person, company = get_persons(account_id)
        print 'res', person
        return render(request, 'profile.html', {'person': person,
                      'company': company})
    except Exception, e:
        raise e


def account(request):
    """Method to handle email verifications."""
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            send_verification(request, email)
            msg = 'Verification email sent successfully'
            data = {"status_code": 0, "message": msg}
            return JsonResponse(data, safe=False)
        elif request.method == 'GET':
            uid = request.GET.get('uid')
            email = request.GET.get('email')
            verify = perform_verification(email, uid)
            if verify:
                msg = 'Email Verified successfully'
                messages.info(request, msg)
            else:
                msg = 'Email could not be verified.'
                messages.error(request, msg)
            return HttpResponseRedirect(reverse(log_in))

        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    except Exception, e:
        raise e


def register(request):
    """Method to handle log out to system."""
    try:
        return render(request, 'register.html', {'status': 200})
    except Exception, e:
        raise e


def registration(request, id):
    """Method to handle log out to system."""
    try:
        client_type_id = 1 if int(id) > 5 else int(id)
        cos = [2, 4, 5]
        tmpl = 'regco.html' if client_type_id in cos else 'registration.html'
        if request.method == 'POST':
            form = RegisterForm(data=request.POST)
            public_reg = settings.PUBLIC_REGISTRATION
            if not public_reg:
                msg = 'Registration temporarily disabled.'
                messages.error(request, msg)
                return HttpResponseRedirect(reverse(log_in))
            if form.is_valid():
                # human = True

                first_name = request.POST.get('first_name')
                middle_name = request.POST.get('middle_name')
                surname = request.POST.get('surname')
                pin_number = request.POST.get('kra_pin')
                idpass_number = request.POST.get('id_number')
                mobile_number = request.POST.get('mobile_number')
                postal_address = request.POST.get('postal_address')
                tax_status = request.POST.get('tax_status')

                client_type = request.POST.get('client_type')

                company_name = request.POST.get('company_name')
                reg_number = request.POST.get('coreg_number')
                etr_number = request.POST.get('etr_number')
                phy_address = request.POST.get('phy_address')
                site_id = request.POST.get('site_id')

                email = request.POST.get('email')
                password = request.POST.get('password1')

                # Create account
                user = create_account(email, client_type_id, password)
                if user:
                    account_id = user.id
                    # If account not personal make it inactive
                    if client_type_id > 1:
                        company_id = request.POST.get('company_id')
                        user.is_active = False
                        user.company_id = company_id
                        user.site_id = site_id
                        user.save(update_fields=["is_active", "company_id",
                                                 "site_id"])
                        # Attach this user to parent company
                        person_co = UserCompany(account_id=account_id,
                                                company_id=company_id,
                                                company_type=client_type_id)
                        person_co.save()
                    # Save other details
                    if int(client_type) == 1:
                        person_new = RegPerson(first_name=first_name,
                                               middle_name=middle_name,
                                               surname=surname,
                                               pin_number=pin_number,
                                               idpass_number=idpass_number,
                                               mobile_number=mobile_number,
                                               postal_address=postal_address,
                                               tax_status=tax_status,
                                               account_id=account_id,
                                               is_void=False)
                        person_new.save()
                    else:
                        company_new = RegCompany(company_name=company_name,
                                                 pin_number=pin_number,
                                                 reg_number=reg_number,
                                                 etr_number=etr_number,
                                                 mobile_number=mobile_number,
                                                 postal_address=postal_address,
                                                 physical_address=phy_address,
                                                 account_id=account_id,
                                                 is_void=False)
                        company_new.save()
                    send_verification(request, email)
                    msg = 'Account created successfully'
                    messages.info(request, msg)
                    return HttpResponseRedirect(reverse(log_in))
                else:
                    msg = 'Email is already registered.'
                    messages.add_message(request, messages.ERROR, msg)
                    return render(request, tmpl,
                                  {'form': form, 'status': 200,
                                   'cid': client_type_id})
            else:
                msg = 'Invalid captcha or there was an error.'
                messages.add_message(request, messages.ERROR, msg)
                return render(request, tmpl,
                              {'form': form, 'status': 200,
                               'cid': client_type_id})
        else:
            form = RegisterForm()
            return render(request, tmpl,
                          {'form': form, 'status': 200,
                           'cid': client_type_id})
    except Exception, e:
        raise e
