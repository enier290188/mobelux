from rest_framework import serializers

from ..models import (
    AlbumModel,
    ImageModel,
)


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumModel
        fields = ('id', 'name', 'is_public', 'user')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ('id', 'title', 'album', 'user')
