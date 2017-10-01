"""Main forms views."""
from urllib import urlencode
from decimal import Decimal
from django.utils import timezone
from django.shortcuts import render
from django.contrib.sites.models import Site
from auth.forms import LoginForm
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import (
    RegPerson, HSCodes, RegCargo, HSCategory,
    CustomerOrders, CustomerInvoice, CustomerGoods, RegCompany,
    BondsApplication)
from auth.views import profile
from .functions import (
    auto_suggest, gen_invoice_number, make_payment, get_persons,
    hs_lists, get_user, get_registrations, update_person,
    update_company, check_account, get_premium_data, new_person,
    new_company, get_bond_data, get_xrate, invoice_data,
    create_notes, get_taxes)
from .forms import CargoForm, BondForm
from main.models import RegPorts
from main.views import dashboard
from auth.forms import RegisterForm
from auth.models import AppUser
from auth.functions import create_account, send_verification
from main.functions import get_categories, get_rate, get_duty


def public_search(request):
    """Method for public search."""
    try:
        if request.method == 'GET':
            print 'public get'
            data = auto_suggest(request)
            return JsonResponse(data, safe=False)
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def search(request):
    """Some default page for Bad request error page."""
    try:
        if request.method == 'POST':
            vals = ''
            filter_type = request.POST.get('filter')
            if filter_type == 'ports':
                country_id = request.POST.get('country_id')
                ports = RegPorts.objects.filter(country_id=country_id)
                for port in ports:
                    port_id = port.id
                    port_name = port.port_name
                    vals += '<option value="%s">%s</option>' % (
                        port_id, port_name)
                return HttpResponse(vals)
            elif filter_type == 'category':
                section_id = request.POST.get('section_id')
                items = HSCategory.objects.filter(section_id=section_id)
                vals = '<option value="">Please Select Category</option>'
                for item in items:
                    category_id = item.id
                    category_name = item.category_name
                    vals += '<option value="%s">%s</option>' % (
                        category_id, category_name)
                return HttpResponse(vals)
            elif filter_type == 'goods':
                category_id = request.POST.get('category_id')
                items = HSCodes.objects.filter(category_id=category_id)
                vals = hs_lists(items)
                return HttpResponse(vals)
            elif filter_type == 'currency':
                currency_id = request.POST.get('currency_id')
                rate = get_xrate(currency_id)
                return JsonResponse(rate, safe=False)

        elif request.method == 'GET':
            print 'Get customer'
            data = auto_suggest(request)
            return JsonResponse(data, safe=False)
        form = LoginForm()
        return render(request, 'forms/forms.html', {'form': form})
    except Exception, e:
        print 'error - %s' % (str(e))
        raise e


@login_required(login_url='/login/')
def register(request):
    """Some default page for Bad request error page."""
    try:
        account_id = request.user.id
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            first_name = request.POST.get('first_name')
            middle_name = request.POST.get('middle_name')
            surname = request.POST.get('surname')
            pin_number = request.POST.get('pin_number')
            idpass_number = request.POST.get('id_number')
            mobile_number = request.POST.get('mobile_number')
            postal_address = request.POST.get('postal_address')
            tax_status = request.POST.get('tax_status')
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
            msg = 'Person details saved successfully'
            messages.info(request, msg)
            return HttpResponseRedirect(reverse(dashboard))
        result = RegPerson.objects.filter(
            account_id=account_id, is_void=False)
        if result:
            return HttpResponseRedirect(reverse(profile))
        else:
            result = RegCompany.objects.filter(
                account_id=account_id, is_void=False)
            if result:
                return HttpResponseRedirect(reverse(profile))
        form = LoginForm()
        return render(request, 'forms/register.html', {'form': form})
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def cargo(request):
    """Some default page for Bad request error page."""
    try:
        created_by = request.user.id
        categories = get_categories()
        if request.method == 'POST':
            # Save order details first
            transact_type = request.POST.get('transact_type')
            person_id = request.POST.get('person_id')
            origin_port_id = request.POST.get('port_id')
            country_id = request.POST.get('country_id')
            dest_port_id = request.POST.get('dest_port')
            inland_warehouse = request.POST.get('warehouse')
            voyage_start = request.POST.get('voyage_start')
            voyage_end = request.POST.get('voyage_end')
            transport_mode = request.POST.get('transport_mode')
            logistics_type = request.POST.get('logistics_id')
            conso_id = request.POST.get('conso_id')
            handler = request.POST.get('ins_handler')
            agent_id = request.POST.get('agent_id')
            broker_id = request.POST.get('broker_id')
            bank_id = request.POST.get('bank_id')
            pay_bank = request.POST.get('pay_bank')
            vessel = request.POST.get('vessel_name')
            total_cost = float(request.POST.get('total_cost'))
            payable_amount = float(request.POST.get('total_amount'))
            total_freight = float(request.POST.get('total_freight'))
            total_tax = float(request.POST.get('total_tax'))
            total_premium = float(request.POST.get('total_premiums'))
            sum_assured = float(request.POST.get('sum_assured'))
            insurance = request.POST.get('insurance_co')
            payment_mode = request.POST.get('payment_mode')
            # Extras
            tax_ws = request.POST.get('tax_ws')
            tax_ts = request.POST.get('tax_ts')
            tax_se = request.POST.get('tax_se')
            tax_ov = request.POST.get('tax_ov')
            tax_sl = request.POST.get('tax_sl')
            war_strike = int(tax_ws) if tax_ws else 0
            trans_ship = int(tax_ts) if tax_ts else 0
            storage_ext = int(tax_se) if tax_se else 0
            over_age = int(tax_ov) if tax_ov else 0
            short_land = int(tax_sl) if tax_sl else 0
            vessel_id = int(vessel) if vessel else None
            time_now = timezone.now()
            if int(transact_type) == 2:
                origin_port_id = request.POST.get('ex_port_id')
                country_id = request.POST.get('ex_country_id')
                dest_port_id = request.POST.get('ex_dest_port')
                inland_warehouse = request.POST.get('ex_warehouse')
            if not agent_id:
                agent_id = None
            if not broker_id:
                broker_id = None
            if not conso_id:
                conso_id = None
            if not bank_id:
                bank_id = pay_bank
            else:
                bank_id = None
            new_order = CustomerOrders(
                transaction_type=transact_type,
                person_id=person_id,
                origin_port_id=origin_port_id,
                country_id=country_id,
                dest_port_id=dest_port_id,
                inland_warehouse=inland_warehouse,
                voyage_start=voyage_start,
                voyage_end=voyage_end,
                transport_mode=transport_mode,
                logistics_type=logistics_type,
                consolidator_id=conso_id,
                insurance_id=insurance,
                handler=handler,
                agent_id=agent_id,
                broker_id=broker_id,
                is_paid=False,
                total_tax=total_tax,
                total_cost=total_cost,
                total_premium=total_premium,
                sum_assured=sum_assured,
                war_strike=war_strike,
                storage_ext=storage_ext,
                trans_ship=trans_ship,
                over_age=over_age,
                short_land=short_land,
                bank_id=bank_id,
                vessel_id=vessel_id,
                pay_method=payment_mode,
                total_freight=total_freight,
                created_by_id=created_by,
                created_at=time_now)
            new_order.save()
            order_id = new_order.pk
            invoice_no = gen_invoice_number(insurance)

            trans_id = int(transport_mode)
            total_premiums = Decimal(total_premium)
            stamp_duty = get_duty(trans_id, sum_assured)
            phf = total_premiums * Decimal(0.0025)
            itl = total_premiums * Decimal(0.0020)

            war_strike = 0.00000
            storage_ext = 0.00000
            trans_ship = 0.00000
            over_age = 0.00000
            short_land = 0.00000
            new_invoice = CustomerInvoice(
                invoice_no=invoice_no,
                policy_no=None,
                payable_amount=payable_amount,
                sum_assured=sum_assured,
                total_premium=total_premium,
                stamp_duty=stamp_duty,
                pcf_amount=phf,
                itl_amount=itl,
                war_strike=war_strike,
                storage_ext=storage_ext,
                trans_ship=trans_ship,
                over_age=over_age,
                short_landing=short_land,
                discount=0.0,
                paid_amount=0.000,
                pay_status=False,
                insurance_id=insurance,
                person_id=person_id,
                orders_id=order_id,
                created_by_id=created_by,
                created_at=time_now)
            new_invoice.save()
            inv_id = new_invoice.pk
            # Save this goods to customer goods and delete tmp
            tmps = RegCargo.objects.select_related().filter(
                account_id=created_by, person_id=person_id)
            for tmp in tmps:
                sum_assured = tmp.quantity * tmp.price
                ins_co = tmp.insurance_id
                a_type = tmp.ship_type
                cat_id = tmp.category_id
                ctype = tmp.cover_type
                ptype = tmp.package_type
                freight = tmp.freight_cost
                #
                covers = {1: 'a', 2: 'b', 3: 'c'}
                cid = covers[ctype]
                amount = sum_assured + freight
                tentry = tmp.goods
                taxes = get_taxes(amount, tentry, 2)
                rail_dev = taxes['rail_dev']
                sugar_dev = taxes['sugar_dev']
                excise_duty = taxes['excise_duty']
                import_duty = taxes['import_duty']
                cargo_rate = get_rate(ins_co, cat_id, a_type, ptype, cid)
                new_good = CustomerGoods(
                    amount=tmp.quantity,
                    price=tmp.price,
                    freight_cost=tmp.freight_cost,
                    package_type=tmp.package_type,
                    cargo_rate=cargo_rate,
                    import_duty=import_duty,
                    excise_duty=excise_duty,
                    sugardev_levy=sugar_dev,
                    raildev_levy=rail_dev,
                    goods_id=tmp.goods_id,
                    orders_id=order_id,
                    person_id=tmp.person_id,
                    created_by_id=created_by,
                    created_at=time_now)
                new_good.save()
            tmps.delete()
            p_mode = int(payment_mode)
            make_payment(inv_id, payable_amount, int(payment_mode))
            msg = 'Order saved successfully and Invoice created.'
            messages.info(request, msg)
            # return HttpResponseRedirect(reverse(dashboard))
            domain = Site.objects.get_current()
            ret_url = 'https://%s/payment/' % (domain)
            if p_mode == 2:
                pay_amount = int(payable_amount * 100)
                dparts = 'kenswitchpaymentsurface/Payment.aspx?'
                url = 'https://apps.kenswitch.com:8066/' + dparts
                params = {'id': 'bWFyaW5l', 'txnid': invoice_no,
                          'amount': pay_amount, 'rec_bank': 34,
                          'rec_acc': '01001030021701', 'return_url': ret_url}
                dest = urlencode(params)
                full_address = url + dest
                return HttpResponseRedirect(full_address)
            else:
                return HttpResponseRedirect(reverse(dashboard))
        form = CargoForm()
        rform = RegisterForm()
        person, company = get_persons(created_by)
        return render(request, 'forms/cargo.html',
                      {'form': form, 'person': person, 'rform': rform,
                       'categories': categories})
    except Exception, e:
        print 'error on cargo - %s' % (str(e))
        raise e


def premiums(request):
    """Some default page for Bad request error page."""
    try:
        covers = {1: 'a', 2: 'b', 3: 'c'}
        if request.method == 'POST':
            account_id = request.user.id
            item_id = request.POST.get('item_id')
            person_id = int(request.POST.get('person_id'))
            if item_id:
                tmps = RegCargo.objects.select_related().filter(
                    account_id=account_id, person_id=person_id,
                    pk=item_id)
                tmps.delete()
                data = get_premium_data(request, account_id, person_id)
                return JsonResponse(data)
            # Do the premiums calculation
            x_rate = float(request.POST.get('exchange_rate'))
            ins_co = int(request.POST.get('insurance_co'))
            goods_type = int(request.POST.get('goods_type'))
            quantity = int(request.POST.get('quantity'))
            cover_id = int(request.POST.get('cover'))
            oprice = request.POST.get('price')
            trans_id = int(request.POST.get('transport_mode'))
            category_id = int(request.POST.get('goods_category'))
            packaging = request.POST.get('package_type')
            package_type = int(packaging) if packaging else 0
            fcost = float(request.POST.get('freight_cost'))
            freight_cost = fcost * x_rate
            # Optional premiums
            fprice = float(oprice.replace(',', ''))
            price = fprice * x_rate
            cover = covers[cover_id]
            # Check rate first
            rate = get_rate(ins_co, category_id, trans_id, package_type, cover)
            if not rate:
                msg = 'The selected goods are not covered.'
                data = {'status': 9, 'premium': 0,
                        'response': '', 'taxes': 0, 'tax': 0,
                        'sum_assured': 0, 'message': msg}
                return JsonResponse(data)
            # Temporariry save this data
            tmpid, created = RegCargo.objects.update_or_create(
                account_id=account_id, goods_id=goods_type,
                person_id=person_id, is_void=False,
                defaults={'insurance_id': ins_co,
                          'goods_id': goods_type,
                          'quantity': quantity,
                          'price': price, 'package_type': package_type,
                          'cover_type': cover_id,
                          'freight_cost': freight_cost,
                          'ship_type': trans_id,
                          'is_void': False,
                          'person_id': person_id,
                          'category_id': category_id,
                          'account_id': account_id})
            data = get_premium_data(request, account_id, person_id)
        return JsonResponse(data)
    except Exception, e:
        print 'premiums error - %s' % (str(e))
        raise e


@login_required(login_url='/login/')
def claims(request, id):
    """Some default page for Bad request error page."""
    try:
        claim = CustomerInvoice.objects.get(id=id)
        return render(request, 'forms/claims.html', {'claim': claim})
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def edit_cargo(request, id):
    """Some default page for Bad request error page."""
    try:
        idata = invoice_data(request, id)
        if not idata:
            msg = "Invoice not found."
            messages.error(request, msg)
            return HttpResponseRedirect(reverse(dashboard))
        rates = idata['rates']
        charges = idata['charges']
        others = idata['others']
        premium = idata['premium']
        tax_premium = idata['tax_premium']
        insured = idata['insured']
        invoice = idata['invoice']
        tcost = idata['tcost']
        pcost = idata['pcost']
        fcost = idata['fcost']
        cost_freight = idata['cost_freight']
        goods = idata['goods']
        if request.method == 'POST':
            action_id = request.POST.get('action_id')
            if not action_id:
                inv_id = invoice['invoice'].id
                create_notes(request, inv_id)
                # Change the approval status
                msg = "Application ammended successfully."
                messages.info(request, msg)
                return HttpResponseRedirect(reverse(dashboard))
            else:
                dnt = request.POST.get('discount')
                discount = float(dnt) if dnt else 0
                if discount > 0:
                    idata = invoice_data(request, id, discount)
                    rates = idata['rates']
                    charges = idata['charges']
                    others = idata['others']
                    premium = idata['premium']
                    tax_premium = idata['tax_premium']
                    insured = idata['insured']
                    invoice = idata['invoice']
                    tcost = idata['tcost']
                    pcost = idata['pcost']
                    fcost = idata['fcost']
                    cost_freight = idata['cost_freight']
                    goods = idata['goods']
                pf = '{:20,.2f}'.format(premium)
                cff = '{:20,.2f}'.format(cost_freight)
                tcostf = '{:20,.2f}'.format(tcost)
                pcostf = '{:20,.2f}'.format(pcost)
                insuredf = '{:20,.2f}'.format(insured)
                taxpf = '{:20,.2f}'.format(tax_premium)
                dtxt = 'Premium (Discount %s%%)' % (discount)
                dt = '<table class="table">'
                dt += '<thead><tr><th>Item</th><th>Value</th>'
                dt += '<th>Rate</th><th>%s</th></tr>' % (dtxt)
                dt += '</thead><tbody>'
                dt += '<tr><td>Cost and Freight</td>'
                dt += '<td align="right">%s</td>' % (cff)
                dt += '<td align="right">-</td>'
                dt += '<td align="right">%s</td></tr>' % (pcostf)
                dt += '<tr><td>Tax Estimates</td>'
                dt += '<td align="right">%s</td>' % (tcostf)
                dt += '<td  align="right">0.00100</td>'
                dt += '<td align="right">%s</td></tr>' % (taxpf)
                dt += '<tr><td>Sum Insured</td>'
                dt += '<td align="right">%s</td>' % (insuredf)
                dt += '<td></td><td></td></tr>'
                for charge in rates:
                    if charge in charges:
                        itm = rates[charge]
                        nm = itm['name']
                        rt = itm['rate'] if 'rate' in itm else "-"
                        rtf = '{:20,.5f}'.format(rt) if rt != '-' else rt
                        cg = '{:20,.2f}'.format(charges[charge])
                        dt += '<tr><td>%s</td><td></td>' % (nm)
                        dt += '<td align="right">%s</td>' % (rtf)
                        dt += '<td align="right">%s</td></tr>' % (cg)

                dt += '<tr><td><strong>Total Premiums</strong></td><td></td>'
                dt += '<td></td><td align="right">'
                dt += '<strong>%s</strong></td></tr>' % (pf)
                dt += '</tbody></table>'
                result = {'status': 0, 'message': dt}
                return JsonResponse(result)
        inv_data = invoice['invoice']
        return render(request, 'forms/cargo_edit.html',
                      {'invoice': invoice, 'goods': goods, 'freight': fcost,
                       'taxes': tcost, 'others': others, 'insured': insured,
                       'premium': premium, 'data': inv_data})
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def csform(request, id):
    """Some default page for Bad request error page."""
    try:
        claim = CustomerInvoice.objects.get(id=id)
        return render(request, 'forms/csform.html', {'claim': claim})
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def registrations(request):
    """Some default page for Bad request error page."""
    try:
        registrations = get_registrations(request)
        return render(request, 'forms/registrations.html',
                      {'claim': {}, 'registrations': registrations})
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def reg_validate(request, id):
    """Some default page for Bad request error page."""
    try:
        user_group = ''
        grps = ['User', 'Manager', 'Admin']
        if request.method == 'POST':
            account_type = int(request.POST.get('account_type'))
            if account_type == 1:
                # Edit a person
                update_person(request)
            else:
                # Edit a company
                update_company(request)
            msg = 'Account modified successfully'
            messages.info(request, msg)
            return HttpResponseRedirect(reverse(registrations))
        coid = request.user.company_id
        sid = request.user.site_id
        user = get_user(id)
        regs = get_registrations(request)
        if not user:
            return render(request, 'forms/registrations.html',
                          {'registrations': regs})
        else:
            if coid != user.company_id or sid != user.site_id:
                return render(request, 'forms/registrations.html',
                              {'registrations': regs})

        groups = user.groups.all()

        for group in groups:
            if str(group) in grps:
                user_group = str(group)
        account = check_account(user)
        if account:
            account_type = 1
            acc_id = user.regperson.id
            vals = {'surname': user.regperson.surname, 'email': user.email,
                    'middle_name': user.regperson.middle_name,
                    'first_name': user.regperson.first_name,
                    'staff_number': user.regperson.staff_number,
                    'id_number': user.regperson.idpass_number,
                    'mobile_number': user.regperson.mobile_number,
                    'postal_address': user.regperson.postal_address,
                    'user_level': user_group}
        else:
            account_type = 2
            acc_id = user.regcompany.id
            vals = {'company_name': user.regcompany.company_name,
                    'email': user.email,
                    'kra_pin': user.regcompany.pin_number,
                    'coreg_number': user.regcompany.reg_number,
                    'etr_number': user.regcompany.etr_number,
                    'physical_address': user.regcompany.physical_address,
                    'mobile_number': user.regcompany.mobile_number,
                    'postal_address': user.regcompany.postal_address,
                    'user_level': user_group}
        form = RegisterForm(data=vals)
        return render(request, 'forms/vregistrations.html',
                      {'form': form, 'registrations': registrations,
                       'account': account_type, 'account_id': acc_id})
    except Exception, e:
        raise e


@login_required(login_url='/login/')
def new_user(request):
    """Some default page for Bad request error page."""
    try:
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(data=request.POST)
            first_name = request.POST.get('first_name')
            middle_name = request.POST.get('middle_name')
            surname = request.POST.get('surname')
            staff_number = request.POST.get('staff_number')
            idpass_number = request.POST.get('id_number')
            mobile_number = request.POST.get('mobile_number')
            postal_address = request.POST.get('postal_address')
            email = request.POST.get('email')
            # Make random password
            password = AppUser.objects.make_random_password()
            company_id = request.user.company_id
            site_id = request.user.site_id
            client_type_id = request.user.person_type
            user = create_account(email, client_type_id, password)
            if user:
                account_id = user.pk
                person_new = RegPerson(first_name=first_name,
                                       middle_name=middle_name,
                                       surname=surname,
                                       staff_number=staff_number,
                                       idpass_number=idpass_number,
                                       mobile_number=mobile_number,
                                       postal_address=postal_address,
                                       account_id=account_id,
                                       is_void=False)
                person_new.save()
                user.company_id = company_id
                user.site_id = site_id
                user.person_type = client_type_id
                user.save(update_fields=["company_id", "person_type",
                                         "site_id"])
                # Add group
                group = Group.objects.get(name='User')
                user.groups.add(group)
                msg = 'Person details saved successfully'
                more_txt = '<p>Password: %s</p>' % (password)
                send_verification(request, email, more_txt)
                messages.info(request, msg)
                return HttpResponseRedirect(reverse(registrations))
            else:
                msg = 'Email already registered'
                messages.error(request, msg)
                return render(request, 'forms/registration.html',
                              {'form': form})
        return render(request, 'forms/registration.html',
                      {'form': form})
    except Exception, e:
        print 'error creating account -%s' % (str(e))
        raise e


def cbm_calculator(request):
    """Method to calculate the CBM."""
    try:
        form = {}
        return render(request, 'forms/cbm.html',
                      {'form': form})
    except Exception, e:
        raise e
    else:
        pass


def bonds(request):
    """Method for bonds forms."""
    try:
        bonds = BondsApplication.objects.filter(
            is_active=True)
        return render(request, 'forms/bonds.html',
                      {'bonds': bonds})
    except Exception, e:
        raise e
    else:
        pass


def new_bonds(request):
    """Method for bonds forms."""
    try:
        form = BondForm()
        account_id = request.user.id
        if request.method == 'POST':
            form = BondForm(data=request.POST)
            bond_amount = request.POST.get('bond_amount')
            bond_class = request.POST.get('bond_class')
            insurance = request.POST.get('insurance_co')
            amount = float(bond_amount.replace(',', ''))
            bond_new = BondsApplication(
                bond_id=bond_class,
                insurance_id=insurance,
                amount=amount,
                client_id=account_id,
                created_by_id=account_id,
                is_active=True)
            bond_new.save()
            msg = 'Bond created successfully awaiting verification '
            msg += 'and approval.'
            messages.info(request, msg)
            return HttpResponseRedirect(reverse(bonds))
        return render(request, 'forms/bonds_new.html',
                      {'form': form})
    except Exception, e:
        raise e
    else:
        pass


def validate_bonds(request, id):
    """Method for bonds forms."""
    try:
        form = BondForm()
        # account_id = request.user.id
        bdata = get_bond_data(id)
        bond = bdata if bdata else {}
        if request.method == 'POST':
            msg = 'Bond validated successfully.'
            messages.info(request, msg)
            return HttpResponseRedirect(reverse(bonds))
        return render(request, 'forms/bonds_validate.html',
                      {'form': form, 'bond': bond})
    except Exception, e:
        raise e
    else:
        pass


def new_client(request):
    """Method to create new clients."""
    try:
        status_code = 0
        email = request.POST.get('email')
        ctype = int(request.POST.get('ctype'))
        password = AppUser.objects.make_random_password()
        company_id = request.user.company_id
        site_id = request.user.site_id
        client_type_id = 1
        user = create_account(email, client_type_id, password)
        if user:
            acc_id = user.pk
            if ctype == 2:
                new_company(request, acc_id)
                print 'New company'
            else:
                new_person(request, acc_id)
            user.company_id = company_id
            user.site_id = site_id
            user.person_type = client_type_id
            user.save(update_fields=["company_id", "person_type",
                                     "site_id"])
            msg = 'Customer profile created successfully'
            more_txt = '<p>Password: %s</p>' % (password)
            send_verification(request, email, more_txt)
        else:
            status_code, acc_id = 9, 0
            msg = 'Email already registered in the system.'
        data = {'status': status_code, 'message': msg,
                'person_id': acc_id}
    except Exception, e:
        print 'error creating client - %s' % (str(e))
        data = {'status': 9, 'message': 'Failed', 'person_id': 0}
        return JsonResponse(data)
    else:
        return JsonResponse(data)
