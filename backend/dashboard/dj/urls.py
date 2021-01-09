from django.urls import (
    include,
    path,
)

from .views import (
    DashboardView,
    AlbumListView,
    AlbumCreateView,
    AlbumDetailView,
    AlbumUpdateView,
    AlbumDeleteView,
    ImageListView,
    ImageCreateView,
    ImageDetailView,
    ImageUpdateView,
    ImageDeleteView,
)

app_name = 'dashboard.dj'
urlpatterns = [
    path(route='', view=DashboardView.as_view(), name='index'),
    path(route='album/', view=include([
        path(route='', view=AlbumListView.as_view(), name='album-list'),
        path(route='create/', view=AlbumCreateView.as_view(), name='album-create'),
        path(route='<int:pk>/', view=include([
            path(route='detail/', view=AlbumDetailView.as_view(), name='album-detail'),
            path(route='update/', view=AlbumUpdateView.as_view(), name='album-update'),
            path(route='delete/', view=AlbumDeleteView.as_view(), name='album-delete'),
        ])),
    ])),
    path(route='image/', view=include([
        path(route='', view=ImageListView.as_view(), name='image-list'),
        path(route='create/', view=ImageCreateView.as_view(), name='image-create'),
        path(route='<int:pk>/', view=include([
            path(route='detail/', view=ImageDetailView.as_view(), name='image-detail'),
            path(route='update/', view=ImageUpdateView.as_view(), name='image-update'),
            path(route='delete/', view=ImageDeleteView.as_view(), name='image-delete'),
        ])),
    ])),
]
