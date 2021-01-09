from django.conf import settings
from django.contrib.auth import (
    authenticate,
    login,
    REDIRECT_FIELD_NAME,
)
from django.contrib.auth.views import SuccessURLAllowedHostsMixin as AuthSuccessURLAllowedHostsMixin
from django.contrib.messages import (
    add_message,
    SUCCESS,
    WARNING,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic.base import RedirectView
from django.views.generic.edit import (
    FormView,
    CreateView,
)

from .forms import (
    RegisterForm,
    LoginForm,
)


class AuthenticateView(RedirectView):
    pattern_name = 'security.dj:authenticate:login'
    permanent = False
    query_string = True


class RegisterView(CreateView):
    model = RegisterForm.Meta.model
    form_class = RegisterForm
    template_name = 'mobelux/security/authenticate/register/register.html'
    success_url = reverse_lazy(viewname=settings.REGISTER_REDIRECT_URL)

    def get_form_kwargs(self):
        kwargs = super(RegisterView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def get_success_url(self):
        add_message(request=self.request, level=SUCCESS, message='User {user} has been registered. Thank you.'.format(user=self.object))
        return super(RegisterView, self).get_success_url()


class LoginView(AuthSuccessURLAllowedHostsMixin, FormView):
    form_class = LoginForm
    template_name = 'mobelux/security/authenticate/login/login.html'
    success_url = reverse_lazy(viewname=settings.LOGIN_REDIRECT_URL)
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def form_valid(self, form):
        self.object = authenticate(request=self.request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
        if self.object is None:
            form.add_error(field=None, error='Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return self.form_invalid(form=form)
        elif not self.object.is_active:
            add_message(request=self.request, level=WARNING, message='Welcome, {user}. Sorry, but this account is inactive.'.format(user=self.object))
            return self.get(request=self.request)
        else:
            login(request=self.request, user=self.object)
            self.get_redirect_to_url()
            return redirect(to=self.get_success_url())

    def get_redirect_to_url(self):
        redirect_to_url = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to_url,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        if url_is_safe:
            self.success_url = redirect_to_url

    def get_success_url(self):
        add_message(request=self.request, level=SUCCESS, message='Welcome, {user}. Thanks for logging in.'.format(user=self.object))
        return super(LoginView, self).get_success_url()
