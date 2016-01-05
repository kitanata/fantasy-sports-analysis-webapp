from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class BillingInfoForm(forms.Form):
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    number = forms.CharField(label='Card Number', required=False)
    verification_value = forms.CharField(label='CVV', required=False)
    month = forms.CharField(label='Expiration Month', required=False)
    year = forms.CharField(label='Expiration Year', required=False)
    address1 = forms.CharField(label='Address', required=False)
    address2 = forms.CharField(label='Address Line 2', required=False)
    city = forms.CharField(label='City', required=False)
    state = forms.CharField(label='State', required=False)
    country = forms.CharField(label='Country', required=False)
    postal_code = forms.CharField(label='Zip Code', required=False)
    token = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(BillingInfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'billing-information'
        self.helper.form_method = 'post'
        self.helper.form_action = 'billing_information'
        self.helper.add_input(Submit('save', 'Save Billing Info'))
