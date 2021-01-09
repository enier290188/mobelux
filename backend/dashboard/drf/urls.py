from django.urls import (
    path,
    re_path,
)

from .views import (
    DashboardView,
    AlbumViewSet,
    ImageViewSet,
)

app_name = 'dashboard.drf'
urlpatterns = [
    path(route='', view=DashboardView.as_view(), name='index'),

    re_path(route='^album/$', view=AlbumViewSet.as_view({
        'get': 'retrieve',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    re_path(route='^album/user/$', view=AlbumViewSet.as_view({
        'get': 'list',
    })),

    re_path(route='^image/$', view=ImageViewSet.as_view({
        'get': 'retrieve',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    re_path(route='^image/album/$', view=ImageViewSet.as_view({
        'get': 'list',
    })),
]
