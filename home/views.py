"""
Vues de l'app home.
"""

from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

User = get_user_model()


def home_view(request: HttpRequest) -> HttpResponse:
    """Vue d'accueil conditionnelle.

    Redirige vers la configuration initiale si aucun utilisateur n'existe.
    Sinon, affiche la page d'accueil avec des liens conditionnels.
    """
    # Si aucun utilisateur n'existe, rediriger vers la configuration
    if not User.objects.exists():
        return redirect("accounts:setup")

    return render(request, "home/index.html")
