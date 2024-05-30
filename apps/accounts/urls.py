from django.urls import path

from . import views

urlpatterns = [
    path(
        'user/register',
        views.AuthenticationView.as_view({'post': 'register'}),
        name='register'
    ),
    path(
        'user/login',
        views.AuthenticationView.as_view({'post': 'login'}),
        name='login'
    ),
]