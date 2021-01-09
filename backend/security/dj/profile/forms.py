from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import (
    Form,
    ModelForm,
    CharField,
    PasswordInput,
)

from .._utils_.forms.helpers import password_validators_help_text_html
from ...models import ProfileModel


class InfoForm(ModelForm):
    error_messages = {
        'username_unique': 'User with this username already exists.',
        'email_unique': 'User with this email already exists.',
    }

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(InfoForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True
        self.fields['email'].required = True

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            self.Meta.model.objects.get(username=username)
        except self.Meta.model.DoesNotExist:
            return username
        else:
            if self.request.user.username == username:
                return username
            else:
                raise ValidationError(message=self.error_messages['username_unique'])

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            self.Meta.model.objects.get(email=email)
        except self.Meta.model.DoesNotExist:
            return email
        else:
            if self.request.user.email == email:
                return email
            else:
                raise ValidationError(message=self.error_messages['email_unique'])


class PasswordForm(ModelForm):
    error_messages = {
        'password_incorrect': 'Your current password was entered incorrectly. Please enter it again.',
        'password_mismatch': 'The two password fields didn’t match.',
    }
    current_password = CharField(
        label='current password',
        widget=PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'autofocus': True,
            },
            render_value=False,
        ),
        strip=False,
    )
    new_password1 = CharField(
        label='new password',
        widget=PasswordInput(
            attrs={
                'autocomplete': 'new-password',
            },
            render_value=False,
        ),
        strip=False,
        help_text=password_validators_help_text_html(),
    )
    new_password2 = CharField(
        label='new password confirmation',
        widget=PasswordInput(
            attrs={
                'autocomplete': 'new-password',
            },
            render_value=False,
        ),
        strip=False,
        help_text='Enter the same password as before, for verification.',
    )

    class Meta:
        model = get_user_model()
        fields = ['current_password', 'new_password1', 'new_password2', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(PasswordForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.instance.check_password(raw_password=current_password):
            raise ValidationError(message=self.error_messages['password_incorrect'])
        return current_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError(message=self.error_messages['password_mismatch'])
        return new_password2

    def _post_clean(self):
        super(PasswordForm, self)._post_clean()
        password = self.cleaned_data.get('new_password1')
        if password:
            try:
                validate_password(password=password, user=self.instance)
            except ValidationError as error:
                self.add_error(field='new_password1', error=error)

    def save(self, commit=True):
        self.instance.set_password(raw_password=self.cleaned_data.get('new_password1'))
        return super(PasswordForm, self).save(commit=commit)


class AvatarForm(ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['avatar', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(AvatarForm, self).__init__(*args, **kwargs)


class LogoutForm(Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(LogoutForm, self).__init__(*args, **kwargs)
