# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.auth_view, name='auth'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]