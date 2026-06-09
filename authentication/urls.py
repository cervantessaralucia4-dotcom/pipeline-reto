from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/',          views.register_view, name='auth-register'),
    path('auth/me/',                views.me_view,       name='auth-me'),
    path('auth/users/',             views.users_list,    name='auth-users'),
    path('auth/users/<int:pk>/rol/', views.change_rol,   name='auth-change-rol'),
]