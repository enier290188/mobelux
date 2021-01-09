from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin as AuthLoginRequiredMixin
from django.contrib.messages import (
    add_message,
    SUCCESS,
)
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from .forms import (
    AlbumCreateForm,
    AlbumUpdateForm,
    ImageCreateForm,
    ImageUpdateForm,
)
from ..models import (
    AlbumModel,
    ImageModel,
)


class DashboardView(AuthLoginRequiredMixin, TemplateView):
    template_name = 'mobelux/dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = get_user_model().objects.all()
        context['albums'] = AlbumModel.objects.all()
        context['images'] = ImageModel.objects.all()
        return context


class AlbumListView(AuthLoginRequiredMixin, ListView):
    model = AlbumModel
    template_name = 'mobelux/dashboard/album-list.html'

    def get_queryset(self):
        self.queryset = self.model.objects.all().filter(user__id=self.request.user.id)
        return super(AlbumListView, self).get_queryset()


class AlbumCreateView(AuthLoginRequiredMixin, CreateView):
    model = AlbumModel
    form_class = AlbumCreateForm
    template_name = 'mobelux/dashboard/album-create.html'

    def get_form_kwargs(self):
        kwargs = super(AlbumCreateView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def get_success_url(self):
        add_message(request=self.request, level=SUCCESS, message='Album "{name}" has been created.'.format(name=self.object.name))
        self.success_url = reverse_lazy(viewname='dashboard.dj:album-list')
        return super(AlbumCreateView, self).get_success_url()


class AlbumDetailView(AuthLoginRequiredMixin, DetailView):
    model = AlbumModel
    template_name = 'mobelux/dashboard/album-detail.html'

    def get_queryset(self):
        self.queryset = self.model.objects.all().filter(user__id=self.request.user.id)
        return super(AlbumDetailView, self).get_queryset()


class AlbumUpdateView(AuthLoginRequiredMixin, UpdateView):
    model = AlbumModel
    form_class = AlbumUpdateForm
    template_name = 'mobelux/dashboard/album-update.html'

    def get_queryset(self):
        self.queryset = self.model.objects.all().filter(user__id=self.request.user.id)
        return super(AlbumUpdateView, self).get_queryset()

    def get_form_kwargs(self):
        kwargs = super(AlbumUpdateView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def get_success_url(self):
        add_message(request=self.request, level=SUCCESS, message='Album "{name}" has been updated.'.format(name=self.object.name))
        self.success_url = reverse_lazy(viewname='dashboard.dj:album-update', kwargs={'pk': self.kwargs.get('pk')})
        return super(AlbumUpdateView, self).get_success_url()


class AlbumDeleteView(AuthLoginRequiredMixin, DeleteView):
    model = AlbumModel
    template_name = 'mobelux/dashboard/album-delete.html'

    def get_queryset(self):
        self.queryset = self.model.objects.all().filter(user__id=self.request.user.id)
        return super(AlbumDeleteView, self).get_queryset()

    def get_success_url(self):
        add_message(request=self.request, level=SUCCESS, message='Album "{name}" has been deleted.'.format(name=self.object.name))
        self.success_url = reverse_lazy(viewname='dashboard.dj:album-list')
        return super(AlbumDeleteView, self).get_success_url()


class ImageListView(AuthLoginRequiredMixin, ListView):
    model = ImageModel
    template_name = 'mobelux/dashboard/image-list.html'

    def get_queryset(self):
        self.queryset = self.model.objects.all().filter(user__id=self.request.user.id)
        return super(ImageListView, self).get_queryset()


class ImageCreateView(AuthLoginRequiredMixin, CreateView):
    model = ImageModel
    form_class = ImageCreateForm
    template_name = 'mobelux/dashboard/image-create.html'

    def get_form_kwargs(self):
        kwargs = super(ImageCreateView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def get_success_url(self):
        add_message(request=self.request, level=SUCCESS, message='Image "{title}" has been created.'.format(title=self.object.title))
        self.success_url = reverse_lazy(viewname='dashboard.dj:image-update', kwargs={'pk': self.object.pk})
        return super(ImageCreateView, self).get_success_url()


class ImageDetailView(AuthLoginRequiredMixin, DetailView):
    model = ImageModel
    template_name = 'mobelux/dashboard/image-detail.html'

    def get_queryset(self):
        self.queryset = self.model.objects.all().filter(user__id=self.request.user.id)
        return super(ImageDetailView, self).get_queryset()


class ImageUpdateView(AuthLoginRequiredMixin, UpdateView):
    model = ImageModel
    form_class = ImageUpdateForm
    template_name = 'mobelux/dashboard/image-update.html'

    def get_queryset(self):
        self.queryset = self.model.objects.all().filter(user__id=self.request.user.id)
        return super(ImageUpdateView, self).get_queryset()

    def get_form_kwargs(self):
        kwargs = super(ImageUpdateView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def get_success_url(self):
        add_message(request=self.request, level=SUCCESS, message='Image "{title}" has been updated.'.format(title=self.object.title))
        self.success_url = reverse_lazy(viewname='dashboard.dj:image-update', kwargs={'pk': self.kwargs.get('pk')})
        return super(ImageUpdateView, self).get_success_url()


class ImageDeleteView(AuthLoginRequiredMixin, DeleteView):
    model = ImageModel
    template_name = 'mobelux/dashboard/image-delete.html'

    def get_queryset(self):
        self.queryset = self.model.objects.all().filter(user__id=self.request.user.id)
        return super(ImageDeleteView, self).get_queryset()

    def get_success_url(self):
        add_message(request=self.request, level=SUCCESS, message='Image "{title}" has been deleted.'.format(title=self.object.title))
        self.success_url = reverse_lazy(viewname='dashboard.dj:image-list')
        return super(ImageDeleteView, self).get_success_url()
