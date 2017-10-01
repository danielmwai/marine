"""Admin backend for editing some admin details."""
from django.contrib import admin

from .models import (
    RegCountry, RegPorts, RegInsurance, RegBank, RegAgents,
    RegBroker, RegConsolidators, RegSites)


class RegCountryAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['country_name']
    list_display = ['id', 'country_code', 'country_name']
    # readonly_fields = ['id']


admin.site.register(RegCountry, RegCountryAdmin)


class RegPortsAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['port_name']
    list_display = ['id', 'country', 'port_name']
    # readonly_fields = ['id']


admin.site.register(RegPorts, RegPortsAdmin)


class RegInsuranceAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['company_name']
    list_display = ['id', 'company_name', 'is_active']
    # readonly_fields = ['id']


admin.site.register(RegInsurance, RegInsuranceAdmin)


class RegBankAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['bank_name']
    list_display = ['id', 'bank_code', 'bank_name', 'is_active']
    # readonly_fields = ['id']


admin.site.register(RegBank, RegBankAdmin)


class RegAgentsAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['agent_name']
    list_display = ['id', 'ira_number', 'agent_name']
    # readonly_fields = ['id']


admin.site.register(RegAgents, RegAgentsAdmin)


class RegBrokerAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['broker_name']
    list_display = ['id', 'broker_name']
    # readonly_fields = ['id']


admin.site.register(RegBroker, RegBrokerAdmin)


class RegConsolidatorAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['consolidator_name']
    list_display = ['id', 'consolidator_name']
    # readonly_fields = ['id']


admin.site.register(RegConsolidators, RegConsolidatorAdmin)


class RegSitesAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['site_name']
    list_display = ['id', 'site_name', 'company_id']
    # readonly_fields = ['id']


admin.site.register(RegSites, RegSitesAdmin)
