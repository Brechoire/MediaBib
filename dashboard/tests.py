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

    def test_superadmin_required_mixin_allows_superadmin(self, client: Client) -> None:
        """Test que SuperAdminRequiredMixin permet au superadmin d'accéder."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )
        client.force_login(superadmin)

        # Accéder à la page de création de médiathèque
        # (protégée par SuperAdminRequiredMixin)
        response = client.get(reverse("libraries:create"))
        assert response.status_code == 200

    def test_superadmin_required_mixin_forbids_library_admin(
        self, client: Client
    ) -> None:
        """Test que SuperAdminRequiredMixin interdit l'accès aux library_admin."""
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

        # Essayer d'accéder à la page de création de médiathèque
        # (réservée aux superadmins)
        response = client.get(reverse("libraries:create"))
        # Doit retourner 403 Forbidden
        assert response.status_code == 403

    def test_superadmin_required_mixin_forbids_reader(self, client: Client) -> None:
        """Test que SuperAdminRequiredMixin interdit l'accès aux lecteurs."""
        reader = User.objects.create_user(
            email="reader@test.com",
            password="TestPass123!",
            first_name="John",
            last_name="Reader",
            role="reader",
        )
        client.force_login(reader)

        # Essayer d'accéder à la page de création de médiathèque
        response = client.get(reverse("libraries:create"))
        # Doit retourner 403 Forbidden
        assert response.status_code == 403

    def test_reader_placeholder_view(self, client: Client) -> None:
        """Test la vue placeholder pour les lecteurs."""
        reader = User.objects.create_user(
            email="reader@test.com",
            password="TestPass123!",
            first_name="John",
            last_name="Reader",
            role="reader",
        )
        client.force_login(reader)

        response = client.get(reverse("dashboard:reader"))
        assert response.status_code == 200
        assert "en cours de développement" in response.content.decode()

    def test_dashboard_access_mixin_authenticated_user(self, client: Client) -> None:
        """Test DashboardAccessMixin avec un utilisateur authentifié non-lecteur."""
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

        # Un library_admin devrait accéder au dashboard
        response = client.get(reverse("dashboard:index"))
        assert response.status_code == 200
        assert "Ma Médiathèque" in response.content.decode()

    def test_dashboard_context_data_superadmin(self, client: Client) -> None:
        """Test le contexte du dashboard pour le superadmin."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )
        client.force_login(superadmin)

        # Créer des données de test
        Library.objects.create(name="Lib Test", email="lib@test.com")
        User.objects.create_user(
            email="reader@test.com", password="TestPass123!", role="reader"
        )

        response = client.get(reverse("dashboard:index"))
        assert response.status_code == 200

        # Vérifier que le contexte contient les statistiques
        context = response.context
        assert context["page_title"] == "Tableau de bord"
        assert context["total_users"] >= 2
        assert context["total_libraries"] >= 1

    def test_dashboard_context_data_library_admin(self, client: Client) -> None:
        """Test le contexte du dashboard pour le library admin."""
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

        # Créer des lecteurs dans cette médiathèque
        User.objects.create_user(
            email="reader1@test.com",
            password="TestPass123!",
            role="reader",
            library=library,
        )
        User.objects.create_user(
            email="reader2@test.com",
            password="TestPass123!",
            role="reader",
            library=library,
        )

        response = client.get(reverse("dashboard:index"))
        assert response.status_code == 200

        context = response.context
        assert context["page_title"] == "Ma Médiathèque"
        assert context["total_readers"] == 2

    def test_get_template_names_superadmin(self, client: Client) -> None:
        """Test get_template_names pour superadmin."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )
        client.force_login(superadmin)

        response = client.get(reverse("dashboard:index"))
        assert response.status_code == 200
        # Le template utilisé est superadmin.html
        assert "dashboard/superadmin.html" in [t.name for t in response.templates]

    def test_get_template_names_library_admin(self, client: Client) -> None:
        """Test get_template_names pour library admin."""
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
        # Le template utilisé est library_admin.html
        assert "dashboard/library_admin.html" in [t.name for t in response.templates]

    def test_get_template_names_reader(self, client: Client) -> None:
        """Test get_template_names pour reader."""
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
        # Le template utilisé est reader_placeholder.html
        assert "dashboard/reader_placeholder.html" in [
            t.name for t in response.templates
        ]
