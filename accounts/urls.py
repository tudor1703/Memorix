from django.urls import path
from . import views
from .views import register_view, activate_view, profile_view

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('activate/<uidb64>/<token>/', activate_view, name='activate'),
    path('profile/', profile_view, name='profile'),
]

