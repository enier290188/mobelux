from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    include,
    path,
)

from .views import IndexView

urlpatterns = [
    path(route='', view=IndexView.as_view(), name='index'),
    path(
        route='',
        view=include(
            [
                path(route='security/', view=include('backend.security.dj.urls')),
                path(route='dashboard/', view=include('backend.dashboard.dj.urls')),
            ]
        )
    ),
    path(
        route='api/',
        view=include(
            [
                path(route='security/', view=include('backend.security.drf.urls')),
                path(route='dashboard/', view=include('backend.dashboard.drf.urls')),
            ]
        )
    ),
    path('admin/', admin.site.urls),
]

if settings.LOCAL is True:
    urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
