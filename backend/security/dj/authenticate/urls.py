from django.urls import path

from .views import (
    AuthenticateView,
    RegisterView,
    LoginView,
)

app_name = 'authenticate'
urlpatterns = [
    path(route='', view=AuthenticateView.as_view(), name='index'),
    path(route='register/', view=RegisterView.as_view(), name='register'),
    path(route='login/', view=LoginView.as_view(), name='login'),
]
