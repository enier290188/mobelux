from django.contrib.auth.password_validation import password_validators_help_texts
from django.utils.functional import lazy
from django.utils.html import format_html_join


def _password_validators_help_text_html(password_validators=None):
    return format_html_join(sep='', format_string='<p class="m-0 p-0">{}</p>', args_generator=((help_text,) for help_text in password_validators_help_texts(password_validators)))


password_validators_help_text_html = lazy(_password_validators_help_text_html, str)
