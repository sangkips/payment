from django.urls import path

from . import views

urlpatterns = [
    path(
        'user/register',
        views.AuthenticationView.as_view({'post': 'register'}),
        name='register'
    ),
]