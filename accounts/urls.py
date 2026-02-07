"""
URLs de l'app accounts.
"""

from django.urls import path

from .views import (
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordChangeView,
    SuperAdminSetupView,
)


app_name = "accounts"

urlpatterns = [
    path("setup/", SuperAdminSetupView.as_view(), name="setup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path(
        "password-change/", CustomPasswordChangeView.as_view(), name="password_change"
    ),
]
