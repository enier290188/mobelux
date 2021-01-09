from django.conf import settings
from django.contrib.auth import (
    logout,
    update_session_auth_hash,
    REDIRECT_FIELD_NAME,
)
from django.contrib.auth.mixins import LoginRequiredMixin as AuthLoginRequiredMixin
from django.contrib.auth.views import SuccessURLAllowedHostsMixin as AuthSuccessURLAllowedHostsMixin
from django.contrib.messages import (
    add_message,
    SUCCESS,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic.base import RedirectView
from django.views.generic.edit import (
    FormView,
    UpdateView,
)

from .forms import (
    InfoForm,
    PasswordForm,
    AvatarForm,
    LogoutForm,
)


class ProfileView(AuthLoginRequiredMixin, RedirectView):
    pattern_name = 'security.dj:profile:info'
    permanent = False
    query_string = True


class InfoView(AuthLoginRequiredMixin, UpdateView):
    model = InfoForm.Meta.model
    form_class = InfoForm
    template_name = 'mobelux/security/profile/info/info.html'
    success_url = reverse_lazy(viewname='security.dj:profile:info')
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        self.kwargs[self.pk_url_kwarg] = self.request.user.pk
        return super(InfoView, self).get_object(queryset=queryset)

    def get_form_kwargs(self):
        kwargs = super(InfoView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def get_success_url(self):
        add_message(request=self.request, level=SUCCESS, message='User {user} has been updated.'.format(user=self.object))
        return super(InfoView, self).get_success_url()


class PasswordView(AuthLoginRequiredMixin, UpdateView):
    model = PasswordForm.Meta.model
    form_class = PasswordForm
    template_name = 'mobelux/security/profile/password/password.html'
    success_url = reverse_lazy(viewname='security.dj:profile:password')
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        self.kwargs[self.pk_url_kwarg] = self.request.user.pk
        return super(PasswordView, self).get_object(queryset=queryset)

    def get_form_kwargs(self):
        kwargs = super(PasswordView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        update_session_auth_hash(request=self.request, user=self.object)
        return redirect(to=self.get_success_url())

    def get_success_url(self):
        add_message(request=self.request, level=SUCCESS, message='User {user} has been updated.'.format(user=self.object))
        return super(PasswordView, self).get_success_url()


class AvatarView(AuthLoginRequiredMixin, UpdateView):
    model = AvatarForm.Meta.model
    form_class = AvatarForm
    template_name = 'mobelux/security/profile/avatar/avatar.html'
    success_url = reverse_lazy(viewname='security.dj:profile:avatar')
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        self.kwargs[self.pk_url_kwarg] = self.model.objects.get(id=self.request.user.profile.id).pk
        return super(AvatarView, self).get_object(queryset=queryset)

    def get_form_kwargs(self):
        kwargs = super(AvatarView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def get_success_url(self):
        add_message(request=self.request, level=SUCCESS, message='User {user} has been updated.'.format(user=self.object))
        return super(AvatarView, self).get_success_url()


class LogoutView(AuthLoginRequiredMixin, AuthSuccessURLAllowedHostsMixin, FormView):
    form_class = LogoutForm
    template_name = 'mobelux/security/profile/logout/logout.html'
    success_url = reverse_lazy(viewname=settings.LOGOUT_REDIRECT_URL)
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_form_kwargs(self):
        kwargs = super(LogoutView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def form_valid(self, form):
        self.object = self.request.user
        logout(request=self.request)
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
        add_message(request=self.request, level=SUCCESS, message='You have been logged out. We hope you come back soon, {user}.'.format(user=self.object))
        return super(LogoutView, self).get_success_url()
