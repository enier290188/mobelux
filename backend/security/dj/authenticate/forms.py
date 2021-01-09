from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import (
    Form,
    ModelForm,
    CharField,
    PasswordInput,
    TextInput,
)

from .._utils_.forms.helpers import password_validators_help_text_html


class RegisterForm(ModelForm):
    error_messages = {
        'username_unique': 'User with this username already exists.',
        'email_unique': 'User with this email already exists.',
        'password_mismatch': 'The two password fields didn’t match.',
    }
    password1 = CharField(
        label='password',
        widget=PasswordInput(
            attrs={
                'autocomplete': 'new-password',
            },
            render_value=False,
        ),
        strip=False,
        help_text=password_validators_help_text_html(),
    )
    password2 = CharField(
        label='password confirmation',
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
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True
        self.fields['email'].required = True

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            self.Meta.model.objects.get(username=username)
        except self.Meta.model.DoesNotExist:
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
            raise ValidationError(message=self.error_messages['email_unique'])

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError(message=self.error_messages['password_mismatch'])
        return password2

    def _post_clean(self):
        super(RegisterForm, self)._post_clean()
        password = self.cleaned_data.get('password1')
        if password:
            try:
                validate_password(password=password, user=self.instance)
            except ValidationError as error:
                self.add_error(field='password1', error=error)

    def save(self, commit=True):
        self.instance.set_password(raw_password=self.cleaned_data.get('password1'))
        return super(RegisterForm, self).save(commit=commit)


class LoginForm(Form):
    username = CharField(
        label='username',
        widget=TextInput(
            attrs={
                'autocomplete': 'username',
                'autofocus': True,
                'render_value': False,
            },
        ),
    )
    password = CharField(
        label='password',
        widget=PasswordInput(
            attrs={
                'autocomplete': 'current-password',
            },
            render_value=False,
        ),
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(LoginForm, self).__init__(*args, **kwargs)
