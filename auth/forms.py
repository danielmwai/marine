"""MINS forms."""
from django import forms
from django.utils.translation import ugettext_lazy as _
from simplemathcaptcha.fields import MathCaptchaField
from captcha.fields import CaptchaField
from forms.functions import (
    get_insurance_list, get_broker_list, get_bank_list)

person_type_list = (('', 'Select Client Type'), (1, 'Individual'),
                    (2, 'Company'))

tax_status_list = (('', 'Select Client Status'), (1, 'Resident'),
                   (2, 'Non-resident'), (2, 'Returning Resident'))

user_level_list = (('', 'Select Level'), ('User', 'User'),
                   ('Manager', 'Manager'), ('Admin', 'Admin'))

broker_list = get_broker_list("Please Select Broker")
insurance_list = get_insurance_list("Please Select Company")
bank_list = get_bank_list("Please Select Bank")


class LoginForm(forms.Form):
    """Login form for the application."""

    email = forms.CharField(widget=forms.EmailInput(
        attrs={'placeholder': _('Email address'),
               'class': 'form-control input-lg',
               'data-parsley-required': "true",
               'data-parsley-error-message': "Please enter email address.",
               'autofocus': 'true'}),
        error_messages={'required': 'Please enter your email address.',
                        'invalid': 'Please enter a valid email address.'})
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Password'),
               'class': 'form-control input-lg',
               'data-parsley-required': "true",
               'data-parsley-error-message': "Please enter your password.",
               'autofocus': 'true'}),
        error_messages={'required': 'Please enter your password.',
                        'invalid': 'Please enter a valid password.'},)

    def clean_email(self):
        """Method to clean username."""
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError("Please enter your email address.")
        return email

    def clean_password(self):
        """Method to clean password."""
        password = self.cleaned_data['password']
        if not password:
            raise forms.ValidationError("Please enter your password.")
        return password


class VerifyForm(forms.Form):
    """Verification form."""

    cert_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'data-parsley-required': 'true',
               'id': 'cert_number'}))
    captcha = MathCaptchaField()


class RegisterForm(forms.Form):
    """Registration form."""

    captcha = CaptchaField()

    kra_pin = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'data-parsley-required': 'true',
               'data-parsley-minlength': '11',
               'data-parsley-group': 'registration',
               'data-parsley-errors-container': '#regerrors',
               'data-parsley-maxlength': '11',
               'id': 'kra_pin'}))

    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control',
               'data-parsley-required': 'true',
               'data-parsley-group': 'registration',
               'id': 'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'data-parsley-required': 'true',
               'data-parsley-minlength': '6',
               'id': 'password1'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'data-parsley-required': 'true',
               'data-parsley-minlength': '6',
               'data-parsley-equalto': '#password1',
               'id': 'password2'}))

    broker_id = forms.ChoiceField(
        choices=broker_list,
        required=False,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'broker_id'}))

    insurance_id = forms.ChoiceField(
        choices=insurance_list,
        required=False,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'insurance_id'}))

    bank_id = forms.ChoiceField(
        choices=bank_list,
        required=False,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'bank_id'}))

    surname = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Surname',
                   'data-parsley-group': 'registration',
                   'id': 'surname'}))

    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'First Name',
                   'data-parsley-group': 'registration',
                   'id': 'first_name'}))

    middle_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Middle Name',
                   'data-parsley-group': 'registration',
                   'id': 'middle_name'}))

    company_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Company Name',
                   'data-parsley-group': 'registration',
                   'id': 'company_name'}))

    id_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'National ID / Passport',
                   'data-parsley-group': 'registration',
                   'id': 'id_number'}))

    staff_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Staff No.',
                   'data-parsley-group': 'registration',
                   'id': 'staff_number'}))

    mobile_number = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'data-parsley-group': 'registration',
                   'placeholder': 'Mobile No.',
                   'id': 'mobile_number'}))

    phy_address = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'rows': '3', 'id': 'phy_address',
                   'data-parsley-group': 'registration',
                   'class': 'form-control'}))

    postal_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': '3', 'id': 'postal_address',
                   'data-parsley-required': "true",
                   'data-parsley-group': 'registration',
                   'class': 'form-control'}))

    coreg_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Company Reg. No.',
                   'data-parsley-group': 'registration',
                   'id': 'coreg_number'}))

    etr_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'ETR Number',
                   'data-parsley-group': 'registration',
                   'id': 'etr_number'}))

    client_type = forms.ChoiceField(
        choices=person_type_list,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'client_type'}))

    tax_status = forms.ChoiceField(
        choices=tax_status_list,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-group': 'registration',
                   'id': 'tax_status'}))

    user_level = forms.ChoiceField(
        choices=user_level_list,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-group': 'registration',
                   'data-parsley-required': "true",
                   'id': 'user_level'}))

    def clean(self):
        """Clean up method."""
        self.cleaned_data = super(RegisterForm, self).clean()

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(
                    "Passwords don't match. Please enter both fields again.")

        if 'kra_pin' in self.cleaned_data:
            if len(self.cleaned_data['kra_pin']) != 11:
                raise forms.ValidationError("Invalid KRA PIN.")

        return self.cleaned_data
