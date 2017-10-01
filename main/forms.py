"""To handle cargo details."""
from django import forms
from forms.functions import get_section_list


section_list = get_section_list("Please Select Section")


transact_list = (("", "Please Select Mode"), ("1", "Sea"),
                 ("2", "Air"))

package_list = (("", "Please Select Package"), ("1", "Containerized"),
                ("2", "Non-Containerized"))


class QuoteForm(forms.Form):
    """Cargo details form."""

    shipping_mode = forms.ChoiceField(
        choices=transact_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'shipping_mode',
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
                   'data-parsley-required': 'true',
                   'id': 'goods_category'}))

    goods_type = forms.ChoiceField(
        choices=(),
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'default-select2 form-control',
                   'id': 'goods_type'}))

    package_type = forms.ChoiceField(
        choices=package_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'id': 'package_type'}))

    sum_assured = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Sum Assured',
                   'data-parsley-required': 'true',
                   'data-parsley-group': 'registration',
                   'id': 'sum_assured'}))

    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control',
               'placeholder': 'Email.',
               'data-parsley-group': 'registration',
               'id': 'email'}))

    mobile_number = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'data-parsley-group': 'registration',
                   'placeholder': 'Mobile No.',
                   'id': 'mobile_number'}))

    currency_id = forms.CharField(widget=forms.HiddenInput(
        attrs={'id': 'currency_id'}))

    currency_value = forms.CharField(widget=forms.HiddenInput(
        attrs={'id': 'currency_value'}))
