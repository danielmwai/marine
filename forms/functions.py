"""Common methods."""
import json
import urllib2
import collections
from decimal import Decimal
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import (
    RegPerson, HSSection, CustomerInvoice, CustomerGoods, RegCompany,
    RegCargo, HSCodes, BondsApplication, CurrencyExchange, ApprovalNotes)
from main.models import (
    RegCountry, RegConsolidators, RegInsurance,
    RegBroker, RegAgents, RegBank, RegSites)
import listings
from auth.models import AppUser
from main.functions import get_rate, get_duty


def new_person(request, account_id):
    """Method to create new account."""
    try:
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        surname = request.POST.get('surname')
        pin_number = request.POST.get('kra_pin')
        idpass_number = request.POST.get('id_number')
        mobile_number = request.POST.get('mobile_number')
        postal_address = request.POST.get('postal_address')
        tax_status = request.POST.get('tax_status')
        person_new = RegPerson(
            first_name=first_name, middle_name=middle_name,
            surname=surname, pin_number=pin_number,
            idpass_number=idpass_number, mobile_number=mobile_number,
            postal_address=postal_address, account_id=account_id,
            tax_status=tax_status, is_void=False)
        person_new.save()
    except Exception, e:
        raise e
    else:
        pass


def new_company(request, account_id):
    """Method to create new account."""
    try:
        pin_number = request.POST.get('kra_pin')
        mobile_number = request.POST.get('mobile_number')
        postal_address = request.POST.get('postal_address')
        company_name = request.POST.get('company_name')
        reg_number = request.POST.get('coreg_number')
        etr_number = request.POST.get('etr_number')
        phy_address = request.POST.get('phy_address')
        company_new = RegCompany(
            company_name=company_name,
            pin_number=pin_number,
            reg_number=reg_number,
            etr_number=etr_number,
            mobile_number=mobile_number,
            postal_address=postal_address,
            physical_address=phy_address,
            account_id=account_id,
            is_void=False)
        company_new.save()
    except Exception, e:
        raise e
    else:
        pass


def get_registrations(request):
    """Get all registrations."""
    try:
        coid = request.user.company_id
        registrations = AppUser.objects.filter(company_id=coid)
        return registrations
    except Exception:
        return {}


def get_insurance(coid):
    """Get all registrations."""
    try:
        company = {}
        print 'COID', coid
        account = get_object_or_404(
            AppUser, company_id=coid, person_type=5, primary=True)
        if account:
            account_id = account.pk
            print account_id
            co_obj = get_object_or_404(RegCompany, account_id=account_id)
            if co_obj:
                company['name'] = co_obj.company_name
                company['pin'] = co_obj.pin_number.upper()
                company['phy_addr'] = co_obj.physical_address
                company['postal_addr'] = co_obj.postal_address
                company['email'] = co_obj.email_address
                company['tel'] = co_obj.mobile_number
        return company
    except Exception, e:
        print 'error getting insurance  - %s' % (str(e))
        return {}


def get_user(user_id):
    """Method to get user by id."""
    try:
        user = AppUser.objects.get(id=user_id)
        return user
    except Exception:
        return False


def get_bond_data(bond_id):
    """Method to get bond details."""
    try:
        bond = BondsApplication.objects.get(id=bond_id)
        return bond
    except Exception:
        return False


def get_persons(account_id):
    """Method to get persons."""
    try:
        company = {}
        person = get_person(account_id)
        if not person:
            person = {}
            company = get_object_or_404(RegCompany, account_id=account_id)
    except Exception, e:
        print 'error getting person - %s' % (str(e))
        return person, company
    else:
        return person, company


def get_person(account_id):
    """Method to get persons."""
    try:
        person = get_object_or_404(RegPerson, account_id=account_id)
    except Exception:
        return None
    else:
        return person


def get_xrate(currency_id):
    """Method to get persons."""
    try:
        status = {"status": 0}
        rates = get_object_or_404(CurrencyExchange, id=currency_id)
        if rates:
            rate = '{:20,.4f}'.format(rates.exchange_rate)
            status["x_rate"] = rate
    except Exception:
        return {"status": 0, "x_rate": 1.0000}
    else:
        return status


def check_account(user):
    """Method to check account id."""
    try:
        if user.regperson:
            return True
        else:
            return False
    except Exception:
        return False


def get_taxes(amount, tentry, qtype=1):
    """Method to calculate all taxes."""
    try:
        taxes = {}
        amount = Decimal(amount)
        new_amnt = amount
        excise_duty = Decimal(0)
        import_duty = Decimal(0)
        raildev_levy = Decimal(0)
        sugardev_levy = Decimal(0)
        if tentry.excise_duty:
            excise_rate = tentry.excise_duty
            excise_value = amount * excise_rate
            excise_duty = excise_rate if excise_rate > 1 else excise_value
            new_amnt = amount + excise_duty
        if tentry.import_duty:
            import_rate = tentry.import_duty
            import_value = new_amnt * import_rate
            import_duty = import_rate if import_rate > 1 else import_value
            import_duty = new_amnt * tentry.import_duty
        if tentry.raildev_levy:
            raildev_levy = amount * tentry.raildev_levy
        if tentry.sugardev_levy:
            sugardev_levy = amount * tentry.sugardev_levy
        all_tax = excise_duty + import_duty + raildev_levy + sugardev_levy
        vat_tax = (all_tax + amount) * Decimal(0.1600)
        taxes['excise_duty'] = excise_duty
        taxes['import_duty'] = import_duty
        taxes['rail_dev'] = raildev_levy
        taxes['sugar_dev'] = sugardev_levy
        taxes['vat'] = vat_tax
        all_taxes = all_tax + vat_tax
        if qtype == 2:
            return taxes
    except Exception, e:
        print 'error getting taxes - %s' % (str(e))
        return Decimal(0)
    else:
        return all_taxes


def get_premium_data(request, account_id, person_id):
    """Method to get premium data."""
    try:
        html = ""
        covers = {1: 'a', 2: 'b', 3: 'c'}
        all_temp = RegCargo.objects.filter(
            account_id=account_id, person_id=person_id, is_void=False)
        total_premium = 0
        total_assured = 0
        total_tax = 0
        cnt = 1
        #
        ins_co = int(request.POST.get('insurance_co'))
        trans_id = int(request.POST.get('transport_mode'))
        fcost = float(request.POST.get('freight_cost'))
        x_rate = float(request.POST.get('exchange_rate'))
        freight_cost = fcost * x_rate
        for vals in all_temp:
            a_price = vals.price
            a_type = vals.ship_type
            a_quantity = vals.quantity
            good_id = vals.goods_id
            cat_id = vals.category_id
            ctype = vals.cover_type
            ptype = vals.package_type
            freight = vals.freight_cost
            #
            cid = covers[ctype]
            tentry = HSCodes.objects.get(pk=good_id)
            rate = get_rate(ins_co, cat_id, a_type, ptype, cid)
            cost = a_price * a_quantity
            premium_rate = rate
            # Total assured = Price + Freight + Tax
            # assured = Decimal(amount) + amount * Decimal(0.1) + freight_cost
            # print assured
            amount = cost + Decimal(freight_cost)
            premium = amount * premium_rate
            tax_value = get_taxes(amount, tentry)
            name = "%s - %s" % (tentry.hs_code, tentry.goods_details)
            html += "<tr>"
            html += "<tr><td>%s</td><td>%s</td>" % (cnt, name)
            html += "<td>%s</td>" % (a_quantity)
            fprice = '{:20,.2f}'.format(a_price)
            famount = '{:20,.2f}'.format(amount)
            fprem = '{:20,.2f}'.format(premium)
            html += "<td align='right'>%s</td>" % (fprice)
            html += "<td align='right'>%s</td>" % (famount)
            html += "<td align='right'>%s</td>" % (fprem)
            cs = 'class="btn btn-danger remove_itm"'
            html += '<td><button id="%s" type="button" %s>' % (vals.id, cs)
            html += '<i class="fa fa-trash"></i> Remove </button></td>'
            html += "</tr>"
            cnt += 1
            # Footer
            total_premium += premium
            total_assured += amount
            total_tax += tax_value
        idf = (total_assured + total_tax) * Decimal(0.02)
        total_tax = total_tax + idf
        tax_premium = total_tax * Decimal(0.001)
        total_basis = total_assured + total_tax
        all_charges = get_other_costs(total_basis, trans_id)
        other_charges = all_charges['totals']
        charges = tax_premium + other_charges
        cus_premium = total_premium + tax_premium
        total_prems = other_charges + cus_premium
        # tprems = total_premium + stamp_duty + pcf + itl
        freight = Decimal(freight_cost * 1.00)
        ffreight = '{:20,.2f}'.format(freight)
        ftax = '{:20,.2f}'.format(total_tax)
        fbasis = '{:20,.2f}'.format(total_basis)
        premsf = '{:20,.2f}'.format(total_prems)
        chargesf = '{:20,.2f}'.format(charges)
        #
        fmt = '{:20,.2f}'
        fassured = '{:20,.2f}'.format(total_assured)
        fpremium = '{:20,.2f}'.format(total_premium)
        html += "<tr class='border_bottom'><td></td><td>"
        html += "<b>Totals</b></td><td></td><td></td>"
        html += "<td align='right'><b>%s</b></td>" % (fassured)
        html += "<td align='right'><b>%s</b></td>" % (fpremium)
        html += "<td></td></tr>"
        html += "<tr><td></td><td colspan='5'>"
        html += "<table width='100%'><thead>"
        html += "<tr class='bbottom'><th>Cost</th>"
        html += "<th>Freight</th><th>Estimated Taxes</th>"
        html += "<th>Basis of Sum Insured</th>"
        html += "<th>Other Charges</th>"
        html += "<th>Total Premium</th></tr>"
        html += "</thead><tbody><tr><td align='left'>%s</td>" % (fassured)
        html += "<td align='left'>%s</td>" % (ffreight)
        html += "<td align='left'>%s</td>" % (ftax)
        html += "<td align='left'>%s</td>" % (fbasis)
        html += "<td align='left'>%s</td>" % (chargesf)
        html += "<td align='left'>%s</td></tr>" % (premsf)
        html += "</tbody></table>"
        html += "</td></tr>"
        html += "<tr><td colspan='7'></td></tr>"
        ctitle = "Premiums (Cost + Freight + Tax Estimates)"
        summ = ""
        summ += "<tr><td>%s</td><td></td>" % (ctitle)
        summ += "<td align='right'>%s</td></tr>" % fmt.format(cus_premium)
        # Do a for loop in here
        rates = all_charges['rates']
        for charge in rates:
            if charge in all_charges:
                itm = rates[charge]
                nm = itm['name']
                rt = itm['rate'] if 'rate' in itm else "-"
                rtf = '{:20,.5f}'.format(rt) if rt != '-' else rt
                cg = '{:20,.2f}'.format(all_charges[charge])
                summ += '<tr><td>%s</td>' % (nm)
                summ += '<td align="right">%s</td>' % (rtf)
                summ += '<td align="right">%s</td></tr>' % (cg)
        summ += "<tr><td><strong>Total Premiums</strong></td>"
        summ += "<td></td><td align='right'><strong>"
        summ += "%s</strong></td></tr>" % fmt.format(total_prems)
        if not all_temp:
            summ, html = "", ""
        inv_premium = "%.2f" % total_premium
        inv_assured = "%.2f" % total_assured
        inv_amount = "%.2f" % total_prems
        data = {'status': 0, 'premium': inv_premium,
                'response': html, 'taxes': summ, 'tax': total_tax,
                'sum_assured': total_basis, 'freight': freight,
                'cost': inv_assured, 'amount': inv_amount}
    except Exception, e:
        raise e
    else:
        return data


def update_person(request):
    """Method to get persons."""
    try:
        acc_id = int(request.POST.get('account_id'))
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        surname = request.POST.get('surname')
        staff_number = request.POST.get('staff_number')
        idpass_number = request.POST.get('id_number')
        mobile_number = request.POST.get('mobile_number')
        postal_address = request.POST.get('postal_address')
        person = get_object_or_404(RegPerson, pk=acc_id)
        person.first_name = first_name
        person.middle_name = middle_name
        person.surname = surname
        person.staff_number = staff_number
        person.idpass_number = idpass_number
        person.mobile_number = mobile_number
        person.postal_address = postal_address
        person.save(
            update_fields=["first_name", "middle_name",
                           "surname", "staff_number",
                           "idpass_number", "mobile_number",
                           "postal_address"])
    except Exception:
        return None
    else:
        return True


def update_company(request):
    """Method to get persons."""
    try:
        print request.POST
        acc_id = int(request.POST.get('account_id'))
        company_name = request.POST.get('company_name')
        pin_number = request.POST.get('kra_pin')
        reg_number = request.POST.get('coreg_number')
        etr_number = request.POST.get('etr_number')
        physical_address = request.POST.get('phy_address')
        mobile_number = request.POST.get('mobile_number')
        postal_address = request.POST.get('postal_address')
        company = get_object_or_404(RegCompany, pk=acc_id)
        company.company_name = company_name
        company.pin_number = pin_number
        company.reg_number = reg_number
        company.etr_number = etr_number
        company.physical_address = physical_address
        company.mobile_number = mobile_number
        company.postal_address = postal_address
        company.save(
            update_fields=["company_name", "pin_number",
                           "reg_number", "etr_number",
                           "physical_address", "mobile_number",
                           "postal_address"])
    except Exception:
        return None
    else:
        return True


def make_payment(invoice_id, premium, mode):
    """Make payment."""
    try:
        # {u'message': u'00', u'rcode': u'0'}
        if mode in [1, 2, 3]:
            return False
        payment = kenswitch_payment(premium)
        rcode = payment['rcode']
        time_now = timezone.now()
        if int(rcode) == 0:
            # Update payment
            pays = get_object_or_404(
                CustomerInvoice, pk=invoice_id)
            pays.pay_status = True
            pays.paid_at = time_now
            pays.save(update_fields=["pay_status", "paid_at"])
    except Exception, e:
        raise e
    else:
        pass


def approve_invoice(invoice_id, status_id, account_id):
    """Make payment."""
    try:
        pays = get_object_or_404(CustomerInvoice, pk=invoice_id)
        pays.approve_status = status_id
        pays.approved_by_id = account_id
        pays.save(update_fields=["approve_status", "approved_by_id"])
    except Exception, e:
        raise e
    else:
        pass


def apply_discount(invoice_id, discount, premium):
    """Make payment."""
    try:
        dvalue = Decimal((100 - discount) / 100)
        pays = get_object_or_404(CustomerInvoice, pk=invoice_id)
        new_amount = premium * dvalue
        pays.payable_amount = new_amount
        pays.discount = discount
        pays.save(update_fields=["payable_amount", "discount"])
    except Exception, e:
        raise e
    else:
        pass


def kenswitch_payment(premium):
    """Method to make payments."""
    try:
        amount = str(int(premium) * 100)
        url_parts = 'KenswitchMobile/webresources/dits/fundstransfer'
        url = 'https://apps.kenswitch.com:8086/' + url_parts

        data = {"custid": "5B03-7321-93E9-4FED",
                "ttype": "t2a",
                "bankcode": "66",
                "acc": "01001030021701",
                "amt": amount,
                "pcode": "1234",
                "qualifier": "0"
                }
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        rjson = json.dumps(data)
        response = urllib2.urlopen(req, rjson)
        message = response.read()

        resp = json.loads(message)
    except Exception, e:
        print "Error making payment - %s" % (str(e))
        return {'message': '00', 'rcode': '999'}
    else:
        return resp


def auto_suggest(request):
    """Method to query existing customers."""
    try:
        results = []
        query_id = int(request.GET.get('id'))
        query = request.GET.get('q')
        # Filters for external ids
        if query_id == 4:
            agents = RegAgents.objects.filter(
                Q(ira_number__icontains=query) |
                Q(agent_name__icontains=query))
            for agent in agents:
                name = agent.agent_name
                agent_id = agent.id
                ira_no = agent.ira_number
                val = {'id': agent_id, 'label': name,
                       'value': name, 'ira_number': ira_no}
                results.append(val)
        else:
            acc_type = int(request.GET.get('acc'))
            if acc_type == 2:
                queryset = RegCompany.objects.filter(is_void=False)
                field_names = ['pin_number', 'etr_number']
                q_filter = Q()
                for field in field_names:
                    q_filter |= Q(**{"%s__icontains" % field: query})
                companys = queryset.filter(q_filter)
                for company in companys:
                    acc_id = company.account_id
                    kra_pin = company.pin_number
                    name = company.company_name
                    val = {'id': acc_id, 'label': name,
                           'value': name, 'kra_pin': kra_pin}
                    results.append(val)
            else:
                queryset = RegPerson.objects.filter(is_void=False)
                field_names = ['pin_number', 'idpass_number']
                q_filter = Q()
                for field in field_names:
                    q_filter |= Q(**{"%s__icontains" % field: query})
                persons = queryset.filter(q_filter)
                for person in persons:
                    acc_id = person.account_id
                    kra_pin = person.pin_number
                    name = '%s %s %s' % (person.first_name, person.surname,
                                         person.middle_name)
                    val = {'id': acc_id, 'label': name,
                           'value': name, 'kra_pin': kra_pin}
                    results.append(val)
    except Exception, e:
        print 'error quering %s' % (str(e))
        return []
    else:
        return results


def get_flat_list(filters, default_txt=False):
    """Get all countries."""
    initial_list = {'': default_txt} if default_txt else {}
    all_list = collections.OrderedDict(initial_list)
    try:
        if filters == 'towns':
            for a_list in listings.towns:
                all_list[a_list] = a_list
        elif filters == 'makes':
            for a_list in listings.makes:
                unit_name = a_list['name']
                unit_id = a_list['id']
                all_list[unit_id] = unit_name
    except Exception, e:
        error = 'Error getting flat list - %s' % (str(e))
        print error
        return ()
    else:
        return all_list.items


def get_country_list(default_txt=False, org_types=[]):
    """Get all countries."""
    initial_list = {'': default_txt} if default_txt else {}
    all_list = collections.OrderedDict(initial_list)
    try:
        my_list = RegCountry.objects.all().order_by('id')
        for a_list in my_list:
            unit_name = a_list.country_name
            all_list[a_list.id] = unit_name
    except Exception, e:
        error = 'Error getting list - %s' % (str(e))
        print error
        return ()
    else:
        return all_list.items


def get_consolidators_list(default_txt=False, org_types=[]):
    """Get all countries."""
    initial_list = {'': default_txt} if default_txt else {}
    all_list = collections.OrderedDict(initial_list)
    try:
        my_list = RegConsolidators.objects.all().order_by('id')
        for a_list in my_list:
            unit_name = a_list.consolidator_name
            all_list[a_list.id] = unit_name
    except Exception, e:
        error = 'Error getting list - %s' % (str(e))
        print error
        return ()
    else:
        return all_list.items


def get_insurance_list(default_txt=False, org_types=[], active=False):
    """Get all countries."""
    initial_list = {'': default_txt} if default_txt else {}
    all_list = collections.OrderedDict(initial_list)
    try:
        aids = RegSites.objects.filter(
            is_active=True, company_type=1).values_list(
                'company_id', flat=True)
        my_list = RegInsurance.objects.filter(
            is_active=True).order_by('id')
        for a_list in my_list:
            unit_name = a_list.company_name
            unit_id = a_list.id
            if active:
                if unit_id in aids:
                    all_list[unit_id] = unit_name
            else:
                all_list[unit_id] = unit_name
    except Exception, e:
        error = 'Error getting list - %s' % (str(e))
        print error
        return ()
    else:
        return all_list.items


def get_bank_list(default_txt=False, org_types=[]):
    """Get all banks."""
    initial_list = {'': default_txt} if default_txt else {}
    all_list = collections.OrderedDict(initial_list)
    try:
        my_list = RegBank.objects.filter(
            is_active=True).order_by('id')
        for a_list in my_list:
            unit_name = a_list.bank_name
            all_list[a_list.id] = unit_name
    except Exception, e:
        error = 'Error getting bank list - %s' % (str(e))
        print error
        return ()
    else:
        return all_list.items


def get_section_list(default_txt=False, org_types=[]):
    """Get all countries."""
    initial_list = {'': default_txt} if default_txt else {}
    all_list = collections.OrderedDict(initial_list)
    try:
        my_list = HSSection.objects.all().order_by('id')
        for a_list in my_list:
            unit_name = a_list.section_name
            all_list[a_list.id] = unit_name
    except Exception, e:
        error = 'Error getting list - %s' % (str(e))
        print error
        return ()
    else:
        return all_list.items


def get_broker_list(default_txt=False, org_types=[]):
    """Get all countries."""
    initial_list = {'': default_txt} if default_txt else {}
    all_list = collections.OrderedDict(initial_list)
    try:
        my_list = RegBroker.objects.all().order_by('id')
        for a_list in my_list:
            unit_name = a_list.broker_name
            all_list[a_list.id] = unit_name
    except Exception, e:
        error = 'Error getting list - %s' % (str(e))
        print error
        return ()
    else:
        return all_list.items


def gen_invoice_number(ins_co='1'):
    """Invoice validations."""
    try:
        ins_company = str(ins_co).zfill(2)
        last_invoice = CustomerInvoice.objects.all().order_by('id').last()
        if not last_invoice:
            return 'I%s0000010' % (ins_company)
        invoice_no = last_invoice.invoice_no
        invoice_int = int(invoice_no[3:-1])
        new_invoice_int = invoice_int + 1
        new_inv_no = str(new_invoice_int).zfill(6)
        invoice_no = '%s%s' % (ins_company, new_inv_no)
        luhn_check = calculate_luhn(invoice_no)
        new_invoice_no = 'I%s%s' % (invoice_no, luhn_check)
        return new_invoice_no
    except Exception, e:
        raise e
    else:
        pass


def get_invoice(request, id, qtype=1):
    """Method to get invoice details."""
    try:
        broker_name = ""
        if qtype == 2:
            invoice = CustomerInvoice.objects.get(invoice_id=id)
        else:
            invoice = CustomerInvoice.objects.get(id=id)
        if invoice:
            res = {'insurance': invoice.insurance.company_name}
            res['country'] = invoice.orders.country.country_name
            res['port'] = invoice.orders.origin_port.port_name
            res['voyage_start'] = invoice.orders.voyage_start
            res['voyage_end'] = invoice.orders.voyage_end
            res['premium'] = invoice.total_premium
            res['amount'] = invoice.payable_amount
            res['insured'] = invoice.sum_assured
            res['stamp_duty'] = invoice.stamp_duty
            res['itl'] = invoice.itl_amount
            res['pcf'] = invoice.pcf_amount
            bank = invoice.orders.bank
            bank_name = bank.bank_name if bank else ''
            res['bank'] = bank_name
            res['insurances'] = get_insurance(invoice.insurance_id)
            res['insurance_id'] = invoice.insurance_id
            person_id = invoice.person.id
            dates = invoice.created_at
            res['cert_id'] = dates.strftime("%d/%m/%Y")
            res['cert_date'] = dates.strftime("%d-%b-%Y")
            # Pass the whole object
            res['invoice'] = invoice
            res['freight'] = invoice.orders.total_freight
            # Get person details
            print person_id
            person, company = get_persons(person_id)
            if person:
                client_name = person.full_name.upper()
                mobile_number = person.mobile_number
                pin_number = person.pin_number.upper()
                id_number = person.idpass_number.upper()
            elif company:
                client_name = company.company_name.upper()
                mobile_number = company.mobile_number
                pin_number = company.pin_number.upper()
                id_number = company.etr_number.upper()
            else:
                client_name, mobile_number = '', ''
                id_number, pin_number = '', ''

            res['name'] = client_name
            res['tel'] = mobile_number
            res['pin'] = pin_number
            res['id'] = id_number

            res['serial'] = invoice.invoice_no[1:]
            # Get the goods
            items = []
            orders_id = invoice.orders_id
            print 'DATA', orders_id, person_id
            goods = CustomerGoods.objects.filter(
                person_id=person_id, orders_id=orders_id)
            idt = 0
            edt = 0
            slt = 0
            rlt = 0
            for good in goods:
                etax = good.import_duty + good.excise_duty + good.sugardev_levy
                tax = etax + good.raildev_levy
                item = [good.goods.hs_code, good.goods.goods_details,
                        good.amount, good.price, good.cargo_rate,
                        good.freight_cost, tax]
                items.append(item)
                idt += good.import_duty
                edt += good.excise_duty
                slt += good.sugardev_levy
                rlt += good.raildev_levy
            res['taxes'] = {1: idt, 2: edt, 3: slt, 4: rlt}
            res['goods'] = items
            agent = invoice.orders.agent
            if agent:
                agent_name = agent.agent_name
            broker = invoice.orders.broker
            if broker:
                broker_name = broker.broker_name
            agbk = "AGENT : %s" % (agent_name) if agent else broker_name
            if not agbk:
                handler = ""
            else:
                chk_agent = "AGENT : " not in agbk
                handler = 'BROKER : %s' % (broker_name) if chk_agent else ""
            res['handler'] = handler
    except Exception, e:
        print "Could not get invoice - %s" % (str(e))
        return {}
    else:
        return res


def get_billing_info(request, inv_no):
    """Method to get invoice details."""
    try:
        broker_name = ""
        inv_no = inv_no[1:] if inv_no.startswith('MI') else inv_no
        invoice = CustomerInvoice.objects.get(invoice_no=inv_no)
        if invoice:
            res = {'insurance': invoice.insurance.company_name}
            res['country'] = invoice.orders.country.country_name
            res['port'] = invoice.orders.origin_port.port_name
            res['voyage_start'] = invoice.orders.voyage_start
            res['voyage_end'] = invoice.orders.voyage_end
            res['premium'] = invoice.total_premium
            bank = invoice.orders.bank
            bank_name = bank.bank_name if bank else ''
            res['bank'] = bank_name
            person_id = invoice.person.id
            # Get person details
            print person_id
            person = RegPerson.objects.get(account_id=person_id)
            res['name'] = person.full_name.upper()
            res['pin'] = person.pin_number.upper()
            res['id'] = person.idpass_number.upper()
            # Get the goods
            items = []
            orders_id = invoice.orders_id
            print 'DATA', orders_id, person_id
            goods = CustomerGoods.objects.filter(
                person_id=person_id, orders_id=orders_id)
            idt = 0
            edt = 0
            slt = 0
            rlt = 0
            for good in goods:
                item = [good.goods.hs_code, good.goods.goods_details,
                        good.amount, good.price, good.cargo_rate]
                items.append(item)
                idt += good.import_duty
                edt += good.excise_duty
                slt += good.sugardev_levy
                rlt += good.raildev_levy
            res['taxes'] = {1: idt, 2: edt, 3: slt, 4: rlt}
            res['goods'] = items
            agent = invoice.orders.agent
            if agent:
                agent_name = agent.agent_name
            broker = invoice.orders.broker
            if broker:
                broker_name = broker.broker_name
            agbk = "AGENT : %s" % (agent_name) if agent else broker_name
            if not agbk:
                handler = ""
            else:
                chk_agent = "AGENT : " not in agbk
                handler = 'BROKER : %s' % (broker_name) if chk_agent else ""
            res['handler'] = handler
            res['message'] = 'Invoice details not found'
            res['code'] = 0
        else:
            res = {"message": "Invoice details not found", "code": 3}
    except Exception, e:
        print "Could not get billing info - %s" % (str(e))
        return {"message": "Error occured", "code": 9}
    else:
        return res


def hs_lists(items):
    """Method to make hs lists."""
    try:
        vals = '<option value="">Please Select Goods</option>'
        tts = {}
        for item in items:
            if item.heading and not item.hs_code:
                ohead = item.heading.split('.')
                ohd = ohead[1]
                opart = '%s0' % (ohd) if len(ohd) == 1 else ohd
                gname = repr(item.goods_details)
                gname = gname.replace("u'", "").replace("'", "")
                nhead = '%s%s' % (ohead[0].zfill(2), opart)
                tts[nhead] = {'name': gname, 'items': []}
        for item in items:
            if item.hs_code:
                hstart = item.hs_code.split('.')[0]
                if hstart in tts:
                    gname = repr(item.goods_details)
                    gname = gname.replace("u'", "").replace("'", "")
                    gdt = {'id': item.id, 'hscode': item.hs_code,
                           'name': gname}
                    tts[hstart]['items'].append(gdt)
        for tt in tts:
            otitle = tts[tt]['name']
            otl = len(otitle)
            tshort = '%s ...' % (otitle[:100]) if otl > 100 else otitle
            vals += '<optgroup label="%s" title="%s">' % (tshort, otitle)
            gitems = tts[tt]['items']
            for itms in gitems:
                itm_id = itms['id']
                itmn = str(itms['name'])
                itm_name = '%s %s' % (itms['hscode'], itmn)
                itl = len(itm_name)
                itms = '%s ...' % (itm_name[:100]) if itl > 100 else itm_name
                vals += '<option value="%s" title="%s">%s</option>' % (
                    itm_id, itm_name, itms)
            vals += '</optgroup>'
    except Exception, e:
        print 'error generating goods lists - %s' % (str(e))
        return ''
    else:
        return vals


def invoice_data(request, id, discount=0):
    """Get invoice data for calculation of discount."""
    try:
        invoice = get_invoice(request, id, 2)
        ng, vals = [], {}
        fcost = Decimal(0)
        pcost = Decimal(0)
        tax_cost = Decimal(0)
        if invoice:
            goods = invoice['goods']
            for good in goods:
                insured = (good[2] * good[3]) + good[5]
                other_tax = good[6]
                vat = (insured + other_tax) * Decimal(0.16)
                all_tax = other_tax + vat
                prem = insured * good[4]
                fcost += good[5]
                tax_cost += all_tax
                pcost += prem
                ngg = good + [prem]
                ng.append(ngg)
        others = Decimal(0)
        inv_obj = invoice['invoice']
        trans_id = inv_obj.orders.transport_mode
        total_cost = inv_obj.orders.total_cost
        total_freight = inv_obj.orders.total_freight
        cost_freight = total_freight + total_cost
        idf = (cost_freight + tax_cost) * (Decimal(0.02))
        insured = cost_freight + tax_cost + idf
        charges = get_other_costs(insured, trans_id)
        tax_premium = tax_cost * Decimal(0.001)
        rates = {}
        if charges:
            print charges
            others = charges['totals']
            rates = charges['rates']
        premium = pcost + tax_premium + others
        if discount > 0:
            dval = Decimal((100 - discount) / 100)
            premium = premium * dval
        vals['premium'] = premium
        vals['tax_premium'] = tax_premium
        vals['rates'] = rates
        vals['others'] = others + tax_premium
        vals['charges'] = charges
        vals['basis'] = insured
        vals['insured'] = total_cost
        vals['goods'] = ng
        vals['fcost'] = fcost
        vals['pcost'] = pcost
        vals['tcost'] = tax_cost
        vals['cost_freight'] = cost_freight
        vals['invoice'] = invoice
    except Exception, e:
        print 'error getting invoice - %s' % (str(e))
        return None
    else:
        return vals


def get_other_costs(sum_insured, trans_id):
    """Method to calculate other details."""
    try:
        charges = {}
        xrates = collections.OrderedDict()
        '''
        Overage premium rate
        Vessel aged 16 to 20 years
        Vessel aged 21 to 25 years
        Vessel aged 26 to 30 years
        Stamp Duty
        Policy Holders Fund
        Training Levy
        '''
        xrates['tshipment'] = {'name': 'Transhipment',
                               'rate': Decimal(0.00250)}
        xrates['sextension'] = {'name': 'Concealed Losses/Storage Extension',
                                'rate': Decimal(0.00150)}
        xrates['overage'] = {'name': 'Overage premium rate',
                             'rate': Decimal(0.00375)}
        xrates['sduty'] = {'name': 'Stamp Duty'}
        xrates['pcf'] = {'name': 'Policy Holders Fund',
                         'rate': Decimal(0.00250)}
        xrates['itl'] = {'name': 'Training Levy',
                         'rate': Decimal(0.00200)}
        tshipment = sum_insured * xrates['tshipment']['rate']
        sextension = sum_insured * xrates['sextension']['rate']
        overage = sum_insured * xrates['overage']['rate']
        print 'freight', trans_id
        stamp_duty = get_duty(trans_id, sum_insured)
        ptotals = tshipment + sextension + overage
        pcf = ptotals * xrates['pcf']['rate']
        itl = ptotals * xrates['itl']['rate']
        totals = ptotals + stamp_duty + pcf + itl
        charges['tshipment'] = tshipment
        charges['sextension'] = sextension
        charges['overage'] = overage
        charges['sduty'] = stamp_duty
        charges['pcf'] = pcf
        charges['itl'] = itl
        charges['totals'] = totals
        charges['rates'] = xrates
    except Exception, e:
        print 'error getting costs - %s' % (str(e))
        return None
    else:
        return charges


def create_notes(request, application_id, type_id=1):
    """Method to create notes."""
    try:
        account_id = request.user.id
        status = request.POST.get('approve')
        status_id = int(status) if status else 0
        message = request.POST.get('notes')
        discount = request.POST.get('discount')
        premium = request.POST.get('premium')
        drate = float(discount) if discount else 0
        print 'DISC', discount
        status = True if status_id == 1 else False
        #
        if type_id == 1 and status_id == 1:
            approve_invoice(application_id, status_id, account_id)
        if status_id > 0:
            new_note = ApprovalNotes(
                message=message.strip(), application_id=application_id,
                status=status, type_id=type_id, created_by_id=account_id)
            new_note.save()
        if drate > 0:
            premium_rate = Decimal(float(premium))
            apply_discount(application_id, drate, premium_rate)
            print 'Apply discount'
    except Exception, e:
        raise e
    else:
        pass


def luhn_checksum(check_number):
    """Generator http://en.wikipedia.org/wiki/Luhn_algorithm."""
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(check_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10


def is_luhn_valid(check_number):
    """Checker http://en.wikipedia.org/wiki/Luhn_algorithm."""
    return luhn_checksum(check_number) == 0


def calculate_luhn(partial_check_number):
    """Generator http://en.wikipedia.org/wiki/Luhn_algorithm."""
    check_digit = luhn_checksum(int(partial_check_number) * 10)
    return check_digit if check_digit == 0 else 10 - check_digit
