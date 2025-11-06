from django.urls import path
from . import views
from .views import login_view, register_view, activate_view, profile_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("activate/<uidb64>/<token>/", activate_view, name="activate"),
    path("profile/", profile_view, name="profile"),
    path("logout/", LogoutView.as_view(next_page='login'), name="logout"),
]