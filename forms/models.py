"""Individual details."""
import uuid
from django.db import models
from django.utils import timezone
from auth.models import AppUser
from main.models import (
    RegInsurance, RegPorts, RegCountry, RegAgents, RegBroker,
    RegConsolidators, RegBank, RegVessel)


class RegPerson(models.Model):
    """Model for Persons details."""

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, default=None)
    surname = models.CharField(max_length=100)
    pin_number = models.CharField(max_length=20, null=True)
    staff_number = models.CharField(max_length=20, null=True)
    idpass_number = models.CharField(max_length=15)
    mobile_number = models.CharField(max_length=20)
    postal_address = models.TextField()
    is_void = models.BooleanField(default=False)
    account = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    tax_status = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def _get_full_name(self):
        return '%s %s' % (self.first_name, self.surname)

    def make_void(self):
        """Inline call method."""
        self.is_void = True
        super(RegPerson, self).save()

    full_name = property(_get_full_name)

    class Meta:
        """Override table details."""

        db_table = 'reg_person'
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s %s' % (self.first_name, self.surname)


class RegCompany(models.Model):
    """Model for Persons details."""

    company_name = models.CharField(max_length=100)
    pin_number = models.CharField(max_length=20)
    reg_number = models.CharField(max_length=15)
    etr_number = models.CharField(max_length=15)
    mobile_number = models.CharField(max_length=100)
    postal_address = models.TextField()
    physical_address = models.TextField()
    email_address = models.TextField(null=True)
    account = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    is_void = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def _get_full_name(self):
        return '%s' % (self.company_name)

    def make_void(self):
        """Inline call method."""
        self.is_void = True
        super(RegCompany, self).save()

    full_name = property(_get_full_name)

    class Meta:
        """Override table details."""

        db_table = 'reg_company'
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.company_name)


class UserCompany(models.Model):
    """Model for all hs codes categories KRA."""

    account = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    company_id = models.IntegerField()
    company_type = models.IntegerField()
    validated = models.BooleanField(default=False)
    validated_by = models.ForeignKey(
        AppUser, related_name='validator', null=True)
    validated_at = models.DateTimeField(null=True)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'reg_user_company'
        verbose_name = 'User Company'
        verbose_name_plural = 'User Companies'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.id)


class HSSection(models.Model):
    """Model for all hs codes sections from KRA."""

    section_name = models.TextField()
    sea_rate = models.DecimalField(decimal_places=5, max_digits=10)
    air_rate = models.DecimalField(decimal_places=5, max_digits=10)
    road_rate = models.DecimalField(decimal_places=5, max_digits=10)
    war_strike = models.DecimalField(decimal_places=5, max_digits=10)
    trans_ship = models.DecimalField(decimal_places=5, max_digits=10)
    storage_ext = models.DecimalField(decimal_places=5, max_digits=10)
    over_age = models.DecimalField(decimal_places=5, max_digits=10)
    short_landing = models.DecimalField(decimal_places=5, max_digits=10)

    class Meta:
        """Override table details."""

        db_table = 'reg_hs_section'
        verbose_name = 'HS Section'
        verbose_name_plural = 'HS Sections'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.section_name)


class HSCategory(models.Model):
    """Model for all hs codes categories KRA."""

    section = models.ForeignKey(HSSection)
    category_name = models.TextField()

    class Meta:
        """Override table details."""

        db_table = 'reg_hs_category'
        verbose_name = 'HS Category'
        verbose_name_plural = 'HS Categories'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.category_name)


class HSSchedule(models.Model):
    """Model for all hs codes sections from KRA."""

    category = models.ForeignKey(HSCategory)
    sea_rate_ca = models.DecimalField(decimal_places=5, max_digits=10)
    sea_rate_cb = models.DecimalField(decimal_places=5, max_digits=10)
    sea_rate_cc = models.DecimalField(decimal_places=5, max_digits=10)
    sea_rate_nca = models.DecimalField(decimal_places=5, max_digits=10)
    sea_rate_ncb = models.DecimalField(decimal_places=5, max_digits=10)
    sea_rate_ncc = models.DecimalField(decimal_places=5, max_digits=10)
    air_rate = models.DecimalField(decimal_places=5, max_digits=10)
    road_rate = models.DecimalField(decimal_places=5, max_digits=10)
    rail_rate = models.DecimalField(decimal_places=5, max_digits=10)
    war_strike = models.DecimalField(decimal_places=5, max_digits=10)
    trans_ship = models.DecimalField(decimal_places=5, max_digits=10)
    storage_ext = models.DecimalField(decimal_places=5, max_digits=10)
    over_age = models.DecimalField(decimal_places=5, max_digits=10)
    short_landing = models.DecimalField(decimal_places=5, max_digits=10)
    extras_detail = models.TextField(null=True)
    insurance = models.ForeignKey(RegInsurance)

    class Meta:
        """Override table details."""

        db_table = 'reg_hs_schedule'
        verbose_name = 'Insurance Schedule'
        verbose_name_plural = 'Insurance Schedules'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.category)


class ISettings(models.Model):
    """Model for all insurance settings."""

    insurance = models.ForeignKey(RegInsurance)
    setting_name = models.CharField(max_length=5)
    setting_value = models.BigIntegerField()
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'reg_isettings'
        verbose_name = 'Insurance Set Up'
        verbose_name_plural = 'Insurance Set Ups'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.insurance)


class HSCodes(models.Model):
    """Model for all hs codes from KRA."""

    category = models.ForeignKey(HSCategory)
    heading = models.CharField(max_length=10, null=True)
    hs_code = models.CharField(max_length=20, null=True)
    goods_details = models.TextField()
    units = models.CharField(max_length=10, null=True)
    excise_duty = models.DecimalField(
        decimal_places=5, default=0, max_digits=30, null=True)
    import_duty = models.DecimalField(
        decimal_places=5, default=0, max_digits=30, null=True)
    raildev_levy = models.DecimalField(
        decimal_places=5, default=0, max_digits=30, null=True)
    sugardev_levy = models.DecimalField(
        decimal_places=5, default=0, max_digits=30, null=True)
    is_void = models.BooleanField(default=False)

    def make_void(self):
        """Inline call method."""
        self.is_void = True
        super(HSCodes, self).save()

    class Meta:
        """Override table details."""

        db_table = 'reg_hs_codes'
        verbose_name = 'HS Code'
        verbose_name_plural = 'HS Codes'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.hs_code)


class RegCargo(models.Model):
    """Model for Cargo details."""

    insurance_id = models.IntegerField()
    package_type = models.IntegerField()
    goods = models.ForeignKey(HSCodes)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=5, max_digits=30)
    freight_cost = models.DecimalField(decimal_places=5, max_digits=30)
    ship_type = models.IntegerField()
    cover_type = models.IntegerField()
    account = models.ForeignKey(AppUser, related_name='creator')
    category = models.ForeignKey(HSCategory)
    person = models.ForeignKey(AppUser)
    created_at = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    def make_void(self):
        """Inline call method."""
        self.is_void = True
        super(RegCargo, self).save()

    class Meta:
        """Override table details."""

        db_table = 'tmp_reg_cargo'
        verbose_name = 'Forms'
        verbose_name_plural = 'Forms'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.account_id)


class CustomerOrders(models.Model):
    """Model for all Customer orders."""

    transaction_type = models.IntegerField()
    person = models.ForeignKey(AppUser)
    origin_port = models.ForeignKey(RegPorts)
    country = models.ForeignKey(RegCountry)
    dest_port = models.ForeignKey(RegPorts, related_name="dest_port")
    inland_warehouse = models.CharField(max_length=100)
    voyage_start = models.DateField()
    voyage_end = models.DateField()
    transport_mode = models.IntegerField()
    logistics_type = models.IntegerField()
    consolidator = models.ForeignKey(RegConsolidators, null=True)
    insurance = models.ForeignKey(RegInsurance)
    handler = models.IntegerField()
    agent = models.ForeignKey(RegAgents, null=True)
    broker = models.ForeignKey(RegBroker, null=True)
    bank = models.ForeignKey(RegBank, null=True)
    vessel = models.ForeignKey(RegVessel, null=True)
    war_strike = models.IntegerField()
    storage_ext = models.IntegerField()
    trans_ship = models.IntegerField()
    over_age = models.IntegerField()
    short_land = models.IntegerField()
    pay_method = models.IntegerField()
    is_paid = models.BooleanField()
    total_freight = models.DecimalField(decimal_places=5, max_digits=30)
    total_tax = models.DecimalField(decimal_places=5, max_digits=30)
    total_cost = models.DecimalField(decimal_places=5, max_digits=30)
    sum_assured = models.DecimalField(decimal_places=5, max_digits=30)
    total_premium = models.DecimalField(decimal_places=5, max_digits=30)
    created_by = models.ForeignKey(AppUser, related_name="order_creator")
    created_at = models.DateTimeField()

    class Meta:
        """Override table details."""

        db_table = 'reg_orders'
        verbose_name = 'Customer Order'
        verbose_name_plural = 'Customer Orders'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.person)


class CustomerGoods(models.Model):
    """Model for all Customer Goods."""

    package_type = models.IntegerField()
    amount = models.IntegerField()
    price = models.DecimalField(decimal_places=5, max_digits=30)
    freight_cost = models.DecimalField(
        decimal_places=5, max_digits=30, default=0)
    cargo_rate = models.DecimalField(decimal_places=5, max_digits=30)
    import_duty = models.DecimalField(decimal_places=5, max_digits=30)
    excise_duty = models.DecimalField(decimal_places=5, max_digits=30)
    sugardev_levy = models.DecimalField(decimal_places=5, max_digits=30)
    raildev_levy = models.DecimalField(decimal_places=5, max_digits=30)
    goods = models.ForeignKey(HSCodes)
    orders = models.ForeignKey(CustomerOrders)
    person = models.ForeignKey(AppUser)
    created_by = models.ForeignKey(AppUser, related_name="created_by")
    created_at = models.DateTimeField()

    class Meta:
        """Override table details."""

        db_table = 'reg_order_goods'
        verbose_name = 'Forms'
        verbose_name_plural = 'Forms'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.id)


class CustomerInvoice(models.Model):
    """Model for all Invoices."""

    invoice_id = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)
    invoice_no = models.CharField(max_length=12, null=True)
    policy_no = models.CharField(max_length=50, null=True)
    payable_amount = models.DecimalField(decimal_places=5, max_digits=30)
    sum_assured = models.DecimalField(decimal_places=5, max_digits=30)
    total_premium = models.DecimalField(decimal_places=5, max_digits=30)
    stamp_duty = models.DecimalField(decimal_places=5, max_digits=30)
    pcf_amount = models.DecimalField(decimal_places=5, max_digits=30)
    itl_amount = models.DecimalField(decimal_places=5, max_digits=30)
    paid_amount = models.DecimalField(decimal_places=5, max_digits=30)
    discount = models.DecimalField(decimal_places=2, max_digits=5)
    war_strike = models.DecimalField(decimal_places=5, max_digits=30)
    trans_ship = models.DecimalField(decimal_places=5, max_digits=30)
    storage_ext = models.DecimalField(decimal_places=5, max_digits=30)
    over_age = models.DecimalField(decimal_places=5, max_digits=30)
    short_landing = models.DecimalField(decimal_places=5, max_digits=30)
    pay_status = models.BooleanField(default=False)
    insurance = models.ForeignKey(RegInsurance)
    person = models.ForeignKey(AppUser)
    orders = models.ForeignKey(CustomerOrders)
    approve_status = models.IntegerField(default=0)
    created_by = models.ForeignKey(AppUser, related_name="invoice_creator")
    approved_by = models.ForeignKey(
        AppUser, related_name="invoice_approver", null=True)
    created_at = models.DateTimeField()
    paid_at = models.DateTimeField(null=True)

    class Meta:
        """Override table details."""

        db_table = 'reg_invoice'
        verbose_name = 'Customer Invoice'
        verbose_name_plural = 'Customer Invoices'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.invoice_no)


class CustomerPayments(models.Model):
    """Model for all payments made."""

    invoice_no = models.CharField(max_length=12, null=True)
    paid_amount = models.DecimalField(decimal_places=5, max_digits=30)
    payment_details = models.TextField()
    payment_type = models.IntegerField(default=1)
    created_at = models.DateTimeField()

    class Meta:
        """Override table details."""

        db_table = 'reg_payments'
        verbose_name = 'Forms'
        verbose_name_plural = 'Forms'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.invoice_no)


class MpesaPayments(models.Model):
    """Model for all mpesa payments."""

    trans_amount = models.DecimalField(decimal_places=5, max_digits=30)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    trans_time = models.CharField(max_length=15)
    trans_type = models.CharField(max_length=15)
    trans_id = models.CharField(max_length=10)
    response_id = models.IntegerField()
    msisdn = models.CharField(max_length=12)
    bill_ref_no = models.CharField(max_length=15)
    created_at = models.DateTimeField(timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'reg_mpesa_payment'
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.trans_id)


class BondsType(models.Model):
    """Model for Bonds."""

    class_name = models.CharField(max_length=30)
    description = models.TextField()
    requirements = models.CharField(max_length=200)
    validity_days = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        """Override table details."""

        db_table = 'list_bond_types'
        verbose_name = 'Bonds Class'
        verbose_name_plural = 'Bonds Classes'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.class_name)


class BondsApplication(models.Model):
    """Model for Bonds."""

    bond = models.ForeignKey(BondsType)
    client = models.ForeignKey(AppUser)
    insurance = models.ForeignKey(RegInsurance)
    amount = models.DecimalField(decimal_places=5, max_digits=30)
    created_by = models.ForeignKey(
        AppUser, related_name='bond_creator')
    is_active = models.BooleanField(default=True)
    is_validated = models.BooleanField(default=True)
    validated_by = models.ForeignKey(
        AppUser, related_name='bond_validator', null=True)
    is_approved = models.BooleanField(default=True)
    approved_by = models.ForeignKey(
        AppUser, related_name='bond_approver', null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'reg_bond_application'
        verbose_name = 'Bonds Application'
        verbose_name_plural = 'Bonds Applications'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.bond)


class CurrencyExchange(models.Model):
    """Model for Currency Exchange rate."""

    currency_name = models.CharField(max_length=4)
    currency_full_name = models.CharField(max_length=50)
    exchange_rate = models.DecimalField(decimal_places=4, max_digits=20)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'reg_currency'
        verbose_name = 'Currency Exchange'
        verbose_name_plural = 'Currency Exchanges'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.currency_name)


class Notification(models.Model):
    """Model for Notifications."""

    account = models.ForeignKey(AppUser)
    is_read = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'reg_notification'
        verbose_name = 'System Notification'
        verbose_name_plural = 'System Notifications'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.account)


class NotificationDetail(models.Model):
    """Model for Notifications. E.g Registration, Application."""

    notification = models.ForeignKey(Notification)
    event_type_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'reg_notification_detail'
        verbose_name = 'System Notification Detail'
        verbose_name_plural = 'System Notification Details'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.notification)


class NotificationChange(models.Model):
    """Model for Notifications. E.g added, requested."""

    notification_change = models.ForeignKey(NotificationDetail)
    action_type_id = models.IntegerField()
    actor = models.ForeignKey(AppUser)

    class Meta:
        """Override table details."""

        db_table = 'reg_notification_change'
        verbose_name = 'System Notification Change'
        verbose_name_plural = 'System Notification Changes'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.notification)


class ApprovalNotes(models.Model):
    """Model for Bonds and Certificates approvals."""

    message = models.TextField(null=True)
    status = models.BooleanField(default=False)
    application_id = models.IntegerField()
    type_id = models.IntegerField()
    created_by = models.ForeignKey(AppUser)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'reg_approval_notes'
        verbose_name = 'Applications Approval'
        verbose_name_plural = 'Applications Approvals'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.id)
