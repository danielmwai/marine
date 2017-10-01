"""Admin backend for editing some admin details."""
from django.contrib import admin

from .models import (
    RegPerson, MpesaPayments, CustomerOrders, CustomerInvoice,
    UserCompany, HSCategory, HSCodes, RegCompany, CurrencyExchange)


class RegPersonAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['first_name', 'surname', 'middle_name' 'mobile_number']
    list_display = ['idpass_number', 'first_name', 'surname', 'pin_number',
                    'mobile_number', 'is_void']
    # readonly_fields = ['id']
    list_filter = ['is_void']


admin.site.register(RegPerson, RegPersonAdmin)


class RegCompanyAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['company_name' 'mobile_number']
    list_display = ['company_name', 'pin_number',
                    'mobile_number', 'is_void']
    # readonly_fields = ['id']
    list_filter = ['is_void']


admin.site.register(RegCompany, RegCompanyAdmin)


class MpesaPaymentsAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['first_name', 'last_name' 'msisdn', 'trans_id']
    list_display = ['trans_id', 'msisdn', 'trans_amount', 'first_name',
                    'last_name', 'bill_ref_no', 'created_at']
    # readonly_fields = ['id']
    list_filter = ['created_at']


admin.site.register(MpesaPayments, MpesaPaymentsAdmin)


class OrdersAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['person']
    list_display = ['person', 'is_paid', 'total_premium', 'created_at']
    # readonly_fields = ['id']
    list_filter = ['created_at']


admin.site.register(CustomerOrders, OrdersAdmin)


class InvoicesAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['invoice_no']
    list_display = ['invoice_no', 'pay_status', 'total_premium', 'person',
                    'created_by', 'created_at']
    # readonly_fields = ['id']
    list_filter = ['created_at']


admin.site.register(CustomerInvoice, InvoicesAdmin)


class UserCompanyAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['account']
    list_display = ['account', 'company_id', 'validated']
    # readonly_fields = ['id']
    list_filter = ['validated']


admin.site.register(UserCompany, UserCompanyAdmin)


class HSCategoryAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['category_name']
    list_display = ['id', 'section_id', 'category_name']
    # readonly_fields = ['id']
    list_filter = ['section_id']


admin.site.register(HSCategory, HSCategoryAdmin)


class HSCodesAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['hs_code']
    list_display = ['id', 'heading', 'goods_details']
    # readonly_fields = ['id']
    list_filter = ['category']


admin.site.register(HSCodes, HSCodesAdmin)


class CurrencyAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['currency_full_name']
    list_display = ['id', 'currency_name', 'currency_full_name',
                    'exchange_rate']
    # readonly_fields = ['id']
    list_filter = ['updated_at']


admin.site.register(CurrencyExchange, CurrencyAdmin)
