"""
Vues de l'app accounts.
"""

from typing import Any

from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
)
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from .forms import CustomAuthenticationForm, CustomPasswordChangeForm, SuperAdminSetupForm


User = get_user_model()


class SuperAdminSetupView(CreateView):
    """Vue d'inscription du premier superadmin."""

    model = User
    form_class = SuperAdminSetupForm
    template_name = "accounts/setup.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs) -> Any:
        """Redirige vers l'accueil si des utilisateurs existent déjà."""
        if User.objects.exists():
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form) -> HttpResponseRedirect:
        """Connecte l'utilisateur après l'inscription."""
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    """Vue de connexion personnalisée."""

    form_class = CustomAuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """Vue de déconnexion personnalisée."""

    next_page = "home"


class CustomPasswordChangeView(PasswordChangeView):
    """Vue de changement de mot de passe personnalisée."""

    form_class = CustomPasswordChangeForm
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("home")
