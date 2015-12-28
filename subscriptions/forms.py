from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class BillingInfoForm(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    number = forms.CharField(label='Card Number')
    verification_value = forms.CharField(label='CVV')
    month = forms.CharField(label='Expiration Month')
    year = forms.CharField(label='Expiration Year')
    address1 = forms.CharField(label='Address')
    address2 = forms.CharField(label='Address Line 2')
    city = forms.CharField(label='City')
    state = forms.CharField(label='State')
    country = forms.CharField(label='Country')

    def __init__(self, *args, **kwargs):
        super(BillingInfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'billing-information'
        self.helper.form_method = 'post'
        self.helper.form_action = 'billing-information'
        self.helper.add_input(Submit('save', 'Save Billing Info'))
