# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='isettings',
            name='insurance',
            field=models.ForeignKey(to='main.RegInsurance'),
        ),
        migrations.AddField(
            model_name='hsschedule',
            name='category',
            field=models.ForeignKey(to='forms.HSCategory'),
        ),
        migrations.AddField(
            model_name='hsschedule',
            name='insurance',
            field=models.ForeignKey(to='main.RegInsurance'),
        ),
        migrations.AddField(
            model_name='hscodes',
            name='category',
            field=models.ForeignKey(to='forms.HSCategory'),
        ),
        migrations.AddField(
            model_name='hscategory',
            name='section',
            field=models.ForeignKey(to='forms.HSSection'),
        ),
        migrations.AddField(
            model_name='customerorders',
            name='agent',
            field=models.ForeignKey(to='main.RegAgents', null=True),
        ),
        migrations.AddField(
            model_name='customerorders',
            name='bank',
            field=models.ForeignKey(to='main.RegBank', null=True),
        ),
        migrations.AddField(
            model_name='customerorders',
            name='broker',
            field=models.ForeignKey(to='main.RegBroker', null=True),
        ),
        migrations.AddField(
            model_name='customerorders',
            name='consolidator',
            field=models.ForeignKey(to='main.RegConsolidators', null=True),
        ),
        migrations.AddField(
            model_name='customerorders',
            name='country',
            field=models.ForeignKey(to='main.RegCountry'),
        ),
        migrations.AddField(
            model_name='customerorders',
            name='created_by',
            field=models.ForeignKey(related_name='order_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customerorders',
            name='dest_port',
            field=models.ForeignKey(related_name='dest_port', to='main.RegPorts'),
        ),
        migrations.AddField(
            model_name='customerorders',
            name='insurance',
            field=models.ForeignKey(to='main.RegInsurance'),
        ),
        migrations.AddField(
            model_name='customerorders',
            name='origin_port',
            field=models.ForeignKey(to='main.RegPorts'),
        ),
        migrations.AddField(
            model_name='customerorders',
            name='person',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customerorders',
            name='vessel',
            field=models.ForeignKey(to='main.RegVessel', null=True),
        ),
        migrations.AddField(
            model_name='customerinvoice',
            name='approved_by',
            field=models.ForeignKey(related_name='invoice_approver', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='customerinvoice',
            name='created_by',
            field=models.ForeignKey(related_name='invoice_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customerinvoice',
            name='insurance',
            field=models.ForeignKey(to='main.RegInsurance'),
        ),
        migrations.AddField(
            model_name='customerinvoice',
            name='orders',
            field=models.ForeignKey(to='forms.CustomerOrders'),
        ),
        migrations.AddField(
            model_name='customerinvoice',
            name='person',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customergoods',
            name='created_by',
            field=models.ForeignKey(related_name='created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customergoods',
            name='goods',
            field=models.ForeignKey(to='forms.HSCodes'),
        ),
        migrations.AddField(
            model_name='customergoods',
            name='orders',
            field=models.ForeignKey(to='forms.CustomerOrders'),
        ),
        migrations.AddField(
            model_name='customergoods',
            name='person',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bondsapplication',
            name='approved_by',
            field=models.ForeignKey(related_name='bond_approver', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='bondsapplication',
            name='bond',
            field=models.ForeignKey(to='forms.BondsType'),
        ),
        migrations.AddField(
            model_name='bondsapplication',
            name='client',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bondsapplication',
            name='created_by',
            field=models.ForeignKey(related_name='bond_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bondsapplication',
            name='insurance',
            field=models.ForeignKey(to='main.RegInsurance'),
        ),
        migrations.AddField(
            model_name='bondsapplication',
            name='validated_by',
            field=models.ForeignKey(related_name='bond_validator', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='approvalnotes',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
