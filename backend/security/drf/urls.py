from django.urls import path

from .views import SecurityView

app_name = 'security.drf'
urlpatterns = [
    path(route='', view=SecurityView.as_view(), name='index'),
]
