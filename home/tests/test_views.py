"""
Tests de la vue d'accueil conditionnelle.
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


@pytest.mark.django_db
class TestHomeView:
    """Tests de la vue d'accueil conditionnelle."""

    def test_home_redirects_to_setup_when_no_users(self, client) -> None:
        """Test que l'accueil redirige vers la configuration si aucun utilisateur."""
        response = client.get(reverse("home"))

        assert response.status_code == 302
        assert response.url == reverse("accounts:setup")

    def test_home_shows_welcome_when_users_exist(self, client) -> None:
        """Test que l'accueil affiche la page de bienvenue si des utilisateurs existent."""
        User.objects.create_user(
            email="user@test.com", password="TestPass123!", role="reader"
        )

        response = client.get(reverse("home"))

        assert response.status_code == 200
        assert "MediaBibli" in response.content.decode()

    def test_home_shows_login_link_when_not_authenticated(self, client) -> None:
        """Test que l'accueil affiche le lien de connexion si non authentifié."""
        User.objects.create_user(
            email="user@test.com", password="TestPass123!", role="reader"
        )

        response = client.get(reverse("home"))

        assert response.status_code == 200
        assert "Se connecter" in response.content.decode()
        assert reverse("accounts:login") in response.content.decode()

    def test_home_shows_register_link_when_no_users(self, client) -> None:
        """Test que l'accueil redirige vers l'inscription si aucun utilisateur."""
        response = client.get(reverse("home"))

        assert response.status_code == 302
        assert response.url == reverse("accounts:setup")

    def test_home_shows_dashboard_link_when_authenticated(self, client) -> None:
        """Test que l'accueil affiche un message de bienvenue quand authentifié."""
        user = User.objects.create_user(
            email="user@test.com", password="TestPass123!", role="reader"
        )
        client.force_login(user)

        response = client.get(reverse("home"))

        assert response.status_code == 200
        assert "Bonjour" in response.content.decode()
