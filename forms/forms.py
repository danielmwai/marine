"""To handle cargo details."""
from django import forms
from .functions import (
    get_country_list, get_consolidators_list, get_insurance_list,
    get_section_list, get_broker_list, get_flat_list, get_bank_list)


country_list = get_country_list("Please Select Country")
consolidator_list = get_consolidators_list("Please Select Consolidator")
insurance_list = get_insurance_list("Please Select Insurance", active=True)
section_list = get_section_list("Please Select Section")

broker_list = get_broker_list("Please Select Broker")

town_list = get_flat_list('towns', "Please Select Town")
car_make_list = get_flat_list('makes', "Please Select Make")
bank_list = get_bank_list("Please Select Bank")

transact_list = (("", "Please Select type"), ("1", "Insurance Company"),
                 ("2", "Bancassurance / Bank"))


bonds_list = (("", "Please Select Class"), ("1", "CB 1"),
              ("2", "CB 1A"), ("3", "CB 2"))

currency_list = (("1", "KES"), ("2", "USD"),
                 ("3", "GBP"), ("4", "EUR"))


class CargoForm(forms.Form):
    """Cargo details form."""

    country_id = forms.ChoiceField(
        choices=country_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'country_id',
                   'data-parsley-group': 'primary1',
                   'data-parsley-required': 'true'}))

    warehouse = forms.ChoiceField(
        choices=town_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'warehouse',
                   'data-parsley-group': 'primary1'}))

    car_make = forms.ChoiceField(
        choices=car_make_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'car_make'}))

    ex_country_id = forms.ChoiceField(
        choices=country_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'ex_country_id',
                   'data-parsley-group': 'primary1',
                   'data-parsley-required': 'true'}))

    conso_id = forms.ChoiceField(
        choices=consolidator_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'conso_id',
                   'data-parsley-group': 'primary1'}))

    insurance_co = forms.ChoiceField(
        choices=insurance_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'insurance_co',
                   'data-parsley-group': 'primary2',
                   'data-parsley-required': 'true'}))

    bank_id = forms.ChoiceField(
        choices=bank_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-group': 'primary2',
                   'id': 'bank_id'}))

    pay_bank = forms.ChoiceField(
        choices=bank_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'pay_bank'}))

    transact_mode = forms.ChoiceField(
        choices=transact_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'transact_mode',
                   'data-parsley-group': 'primary2',
                   'data-parsley-required': 'true'}))

    goods_section = forms.ChoiceField(
        choices=section_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'goods_section'}))

    goods_category = forms.ChoiceField(
        choices=(),
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'goods_category'}))

    goods_type = forms.ChoiceField(
        choices=(),
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'default-select2 form-control',
                   'id': 'goods_type'}))

    broker_id = forms.ChoiceField(
        choices=broker_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-group': 'primary2',
                   'id': 'broker_id'}))

    sum_assured = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Sum Assured',
                   'data-parsley-group': 'registration',
                   'id': 'sum_assured'}))

    vessel_name = forms.ChoiceField(
        choices=(),
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-group': 'primary1',
                   'id': 'vessel_name'}))

    currency = forms.ChoiceField(
        choices=currency_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-group': 'primary2',
                   'data-parsley-required': 'true',
                   'id': 'currency'}))


class BondForm(forms.Form):
    """Bonds details form."""

    bond_class = forms.ChoiceField(
        choices=bonds_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'bond_class',
                   'data-parsley-group': 'primary1',
                   'data-parsley-required': 'true'}))

    bond_amount = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'data-parsley-group': 'primary1',
                   'data-parsley-required': 'true',
                   'id': 'bond_amount'}))
