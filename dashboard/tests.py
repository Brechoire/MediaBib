"""
Tests du dashboard.
"""


import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from libraries.models import Library

User = get_user_model()


@pytest.mark.django_db
class TestDashboardViews:
    """Tests des vues du dashboard."""

    def test_dashboard_requires_login(self, client: Client) -> None:
        """Test que le dashboard nécessite une connexion."""
        response = client.get(reverse("dashboard:index"))

        # Devrait rediriger vers la page de login
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_superadmin_dashboard(self, client: Client) -> None:
        """Test le dashboard du superadmin."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com",
            password="TestPass123!",
            first_name="Super",
            last_name="Admin",
            role="superadmin",
        )
        client.force_login(superadmin)

        response = client.get(reverse("dashboard:index"))

        assert response.status_code == 200
        assert "Tableau de bord" in response.content.decode()
        assert "Médiathèques récentes" in response.content.decode()

    def test_library_admin_dashboard(self, client: Client) -> None:
        """Test le dashboard de l'admin de médiathèque."""
        library = Library.objects.create(
            name="Médiathèque Test", email="library@test.com"
        )

        library_admin = User.objects.create_user(
            email="libraryadmin@test.com",
            password="TestPass123!",
            first_name="Library",
            last_name="Admin",
            role="library_admin",
            library=library,
        )
        client.force_login(library_admin)

        response = client.get(reverse("dashboard:index"))

        assert response.status_code == 200
        assert "Ma Médiathèque" in response.content.decode()
        assert library.name in response.content.decode()

    def test_reader_no_dashboard(self, client: Client) -> None:
        """Test que les lecteurs n'ont pas accès au dashboard."""
        reader = User.objects.create_user(
            email="reader@test.com",
            password="TestPass123!",
            first_name="John",
            last_name="Reader",
            role="reader",
        )
        client.force_login(reader)

        response = client.get(reverse("dashboard:index"))

        assert response.status_code == 200
        assert "en cours de développement" in response.content.decode()

    def test_superadmin_sees_statistics(self, client: Client) -> None:
        """Test que le superadmin voit les statistiques."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )

        # Créer quelques données
        Library.objects.create(name="Lib 1", email="lib1@test.com")
        Library.objects.create(name="Lib 2", email="lib2@test.com")
        User.objects.create_user(
            email="reader@test.com", password="TestPass123!", role="reader"
        )

        client.force_login(superadmin)
        response = client.get(reverse("dashboard:index"))

        assert response.status_code == 200
        content = response.content.decode()
        assert "Utilisateurs" in content
        assert "Médiathèques" in content
