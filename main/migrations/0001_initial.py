# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegAgents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ira_number', models.CharField(max_length=20)),
                ('agent_name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'list_agent',
                'verbose_name': 'Insurance Agent',
                'verbose_name_plural': 'Insurance Agencies',
            },
        ),
        migrations.CreateModel(
            name='RegBank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bank_name', models.CharField(max_length=100)),
                ('bank_code', models.CharField(max_length=2)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'list_bank',
                'verbose_name': 'Bank',
                'verbose_name_plural': 'Banks',
            },
        ),
        migrations.CreateModel(
            name='RegBankBranch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('branch_name', models.CharField(max_length=100)),
                ('branch_code', models.CharField(max_length=6)),
                ('is_active', models.BooleanField(default=True)),
                ('bank', models.ForeignKey(to='main.RegBank')),
            ],
            options={
                'db_table': 'list_bank_branch',
                'verbose_name': 'Bank Branch',
                'verbose_name_plural': 'Bank Branches',
            },
        ),
        migrations.CreateModel(
            name='RegBroker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('broker_name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'list_broker',
                'verbose_name': 'Insurance Broker',
                'verbose_name_plural': 'Insurance Brokers',
            },
        ),
        migrations.CreateModel(
            name='RegConsolidators',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('consolidator_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'list_consolidators',
                'verbose_name': 'Consolidator',
                'verbose_name_plural': 'Consolidators',
            },
        ),
        migrations.CreateModel(
            name='RegCountry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country_code', models.CharField(max_length=2)),
                ('country_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'list_country',
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='RegInsurance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_name', models.CharField(max_length=100)),
                ('company_initial', models.CharField(default=b'XXXX', max_length=10)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'list_company',
                'verbose_name': 'Insurance Company',
                'verbose_name_plural': 'Insurance Companies',
            },
        ),
        migrations.CreateModel(
            name='RegPorts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('port_name', models.CharField(max_length=100)),
                ('country', models.ForeignKey(to='main.RegCountry')),
            ],
            options={
                'db_table': 'list_port',
                'verbose_name': 'Port',
                'verbose_name_plural': 'Ports',
            },
        ),
        migrations.CreateModel(
            name='RegSites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_name', models.CharField(max_length=100)),
                ('company_id', models.IntegerField()),
                ('company_type', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
            options={
                'db_table': 'reg_sites',
                'verbose_name': 'Registered Site',
                'verbose_name_plural': 'Registered Sites',
            },
        ),
        migrations.CreateModel(
            name='RegVessel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vessel_name', models.CharField(max_length=200)),
                ('vessel_year', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'list_vessel',
                'verbose_name': 'Vessel',
                'verbose_name_plural': 'Vessels',
            },
        ),
    ]
