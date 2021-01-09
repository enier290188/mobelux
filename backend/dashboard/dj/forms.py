from django.forms import (
    ModelForm,
)

from ..models import (
    AlbumModel,
    ImageModel,
)


class AlbumCreateForm(ModelForm):
    error_messages = {
    }

    class Meta:
        model = AlbumModel
        fields = ['name', 'is_public', 'user']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(AlbumCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    def save(self, commit=True):
        self.instance.user = self.request.user
        return super(AlbumCreateForm, self).save(commit=commit)


class AlbumUpdateForm(ModelForm):
    error_messages = {
    }

    class Meta:
        model = AlbumModel
        fields = ['name', 'is_public', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(AlbumUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True


class ImageCreateForm(ModelForm):
    error_messages = {
    }

    class Meta:
        model = ImageModel
        fields = ['title', 'album', 'user']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ImageCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['autofocus'] = True
        self.fields['album'].queryset = AlbumModel.objects.all().filter(user__id=self.request.user.id)

    def save(self, commit=True):
        self.instance.user = self.request.user
        return super(ImageCreateForm, self).save(commit=commit)


class ImageUpdateForm(ModelForm):
    error_messages = {
    }

    class Meta:
        model = ImageModel
        fields = ['title', 'image', 'album', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ImageUpdateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['autofocus'] = True
        self.fields['album'].queryset = AlbumModel.objects.all().filter(user__id=self.request.user.id)
