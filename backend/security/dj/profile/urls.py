from django.urls import path

from .views import (
    ProfileView,
    InfoView,
    PasswordView,
    AvatarView,
    LogoutView,
)

app_name = 'profile'
urlpatterns = [
    path(route='', view=ProfileView.as_view(), name='index'),
    path(route='info/', view=InfoView.as_view(), name='info'),
    path(route='password/', view=PasswordView.as_view(), name='password'),
    path(route='avatar/', view=AvatarView.as_view(), name='avatar'),
    path(route='logout/', view=LogoutView.as_view(), name='logout'),
]
