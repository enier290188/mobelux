from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK
)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from ..models import (
    AlbumModel,
    ImageModel,
)
from .serializers import (
    AlbumSerializer,
    ImageSerializer,
)


class DashboardView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            'message': 'GET: Dashboard.'
        }
        return Response(data=data, status=HTTP_200_OK)


class AlbumViewSet(ModelViewSet):
    serializer_class = AlbumSerializer

    def get_object(self):
        return get_object_or_404(AlbumModel, pk=self.request.query_params.get('pk'))

    def get_queryset(self):
        username = self.request.query_params.get('username')
        if username:
            try:
                user = get_user_model().objects.get(username=username)
                if user:
                    return AlbumModel.objects.filter(user__id=user.id).order_by('name')
            except get_user_model().DoesNotExist:
                return AlbumModel.objects.none()
        return AlbumModel.objects.all().order_by('name')


class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer

    def get_object(self):
        return get_object_or_404(ImageModel, pk=self.request.query_params.get('pk'))

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name:
            try:
                albums = AlbumModel.objects.filter(name=name)
                if albums:
                    return ImageModel.objects.filter(album__id=albums[0].id).order_by('title')
            except AlbumModel.DoesNotExist:
                return ImageModel.objects.none()
        return ImageModel.objects.all().order_by('title')
