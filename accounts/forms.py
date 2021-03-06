from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField, AuthenticationForm, PasswordResetForm,
    SetPasswordForm
)
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML


class CrispySetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CrispySetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'password_reset_confirm'
        self.helper.form_method = 'post'
        # need to make sure I post to the same exact url.
        self.helper.form_action = ''
        self.helper.add_input(Submit('changepassword', 'Change Password'))


class CrispyResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(CrispyResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'password_reset'
        self.helper.form_method = 'post'
        self.helper.form_action = 'password_reset'
        self.helper.add_input(Submit('reset', 'Reset Password'))


class CrispyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autofocus': '',
            'placeholder': 'example@example.com'
        }),
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••'
        })
    )

    def __init__(self, *args, **kwargs):
        super(CrispyAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'login'
        self.helper.form_method = 'post'
        self.helper.form_action = 'login'

        self.helper.layout = Layout(
            'username',
            'password',
            HTML("""
                <p><a href='{% url 'password_reset' %}'>
                Forgot your password?</a></p>
            """),
            Submit('login', 'Login')
        )


class EmailUserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required fields, plus a
    repeated password.
    """
    error_messages = {
        'duplicate_email': _('A user with that email already exists.'),
        'password_mismatch': _('The two password fields didn\'t match.'),
    }

    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••'
        }),
    )

    password2 = forms.CharField(
        label=_('Confirm password'),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••'
        }),
        help_text=_('Enter the same password as above, for verification.')
    )

    class Meta:
        model = get_user_model()
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@example.com'
            })
        }

    def clean_email(self):
        # Since EmailUser.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data['email']
        try:
            get_user_model()._default_manager.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(EmailUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(EmailUserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'sign-up'
        self.helper.form_method = 'post'
        self.helper.form_action = 'signup'
        self.helper.add_input(Submit('save', 'Sign Up'))


class EmailUserChangeForm(forms.ModelForm):

    """
    A form for updating users. Includes all the fields on the user, but
    replaces the password field with admin's password hash display field.
    """

    password = ReadOnlyPasswordHashField(label=_('Password'),
                                         help_text=_('Raw passwords are not'
                                                     ' stored, so there is no'
                                                     ' way to see this user\'s'
                                                     ' password.'))

    class Meta:
        model = get_user_model()
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(EmailUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial['password']


class EmailUserAccountInfoForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(EmailUserAccountInfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'account-info'
        self.helper.form_method = 'post'
        self.helper.form_action = 'account_info'
        self.helper.add_input(Submit('save', 'Save Changes'))


class DeleteAccountForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DeleteAccountForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'delete-account'
        self.helper.form_method = 'post'
        self.helper.form_action = 'delete_account'
        self.helper.add_input(
            Submit('save', 'I understand, delete my account.')
        )
