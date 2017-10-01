"""Individual details."""
from django.db import models
from django.contrib.sites.models import Site


class RegSites(models.Model):
    """Model for Persons details."""

    site_name = models.CharField(max_length=100)
    company_id = models.IntegerField()
    company_type = models.IntegerField()
    site = models.ForeignKey(Site)
    is_active = models.BooleanField(default=True)

    class Meta:
        """Override table details."""

        db_table = 'reg_sites'
        verbose_name = 'Registered Site'
        verbose_name_plural = 'Registered Sites'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.site_name)


class RegCountry(models.Model):
    """Model for Persons details."""

    country_code = models.CharField(max_length=2)
    country_name = models.CharField(max_length=100)

    class Meta:
        """Override table details."""

        db_table = 'list_country'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.country_name)


class RegPorts(models.Model):
    """Model for Ports details."""

    country = models.ForeignKey(RegCountry)
    port_name = models.CharField(max_length=100)

    class Meta:
        """Override table details."""

        db_table = 'list_port'
        verbose_name = 'Port'
        verbose_name_plural = 'Ports'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.port_name)


class RegVessel(models.Model):
    """Model for Vessels details."""

    vessel_name = models.CharField(max_length=200)
    vessel_year = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        """Override table details."""

        db_table = 'list_vessel'
        verbose_name = 'Vessel'
        verbose_name_plural = 'Vessels'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.vessel_name)


class RegInsurance(models.Model):
    """Model for Persons details."""

    company_name = models.CharField(max_length=100)
    company_initial = models.CharField(max_length=10, default='XXXX')
    is_active = models.BooleanField(default=True)

    class Meta:
        """Override table details."""

        db_table = 'list_company'
        verbose_name = 'Insurance Company'
        verbose_name_plural = 'Insurance Companies'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.company_name)


class RegBank(models.Model):
    """Model for Persons details."""

    bank_name = models.CharField(max_length=100)
    bank_code = models.CharField(max_length=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        """Override table details."""

        db_table = 'list_bank'
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.bank_name)


class RegBankBranch(models.Model):
    """Model for Persons details."""

    branch_name = models.CharField(max_length=100)
    branch_code = models.CharField(max_length=6)
    bank = models.ForeignKey(RegBank)
    is_active = models.BooleanField(default=True)

    class Meta:
        """Override table details."""

        db_table = 'list_bank_branch'
        verbose_name = 'Bank Branch'
        verbose_name_plural = 'Bank Branches'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.branch_name)


class RegAgents(models.Model):
    """Model for Persons details."""

    ira_number = models.CharField(max_length=20)
    agent_name = models.CharField(max_length=200)

    class Meta:
        """Override table details."""

        db_table = 'list_agent'
        verbose_name = 'Insurance Agent'
        verbose_name_plural = 'Insurance Agencies'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.agent_name)


class RegBroker(models.Model):
    """Model for Persons details."""

    broker_name = models.CharField(max_length=200)

    class Meta:
        """Override table details."""

        db_table = 'list_broker'
        verbose_name = 'Insurance Broker'
        verbose_name_plural = 'Insurance Brokers'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.broker_name)


class RegConsolidators(models.Model):
    """Model for Persons details."""

    consolidator_name = models.CharField(max_length=100)

    class Meta:
        """Override table details."""

        db_table = 'list_consolidators'
        verbose_name = 'Consolidator'
        verbose_name_plural = 'Consolidators'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.consolidator_name)
