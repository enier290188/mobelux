from django.urls import (
    include,
    path,
)

from .views import SecurityView

app_name = 'security.dj'
urlpatterns = [
    path(route='', view=SecurityView.as_view(), name='index'),
    path(route='authenticate/', view=include('backend.security.dj.authenticate.urls')),
    path(route='profile/', view=include('backend.security.dj.profile.urls')),
]
