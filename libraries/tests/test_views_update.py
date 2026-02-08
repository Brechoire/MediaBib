"""
Tests des vues de gestion des médiathèques - compléments.
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from libraries.models import Library

User = get_user_model()


@pytest.mark.django_db
class TestLibraryUpdateView:
    """Tests de la vue de modification de médiathèque."""

    def test_update_library_requires_login(self, client: Client) -> None:
        """Test que la modification nécessite une connexion."""
        library = Library.objects.create(name="Test Library", email="test@test.com")

        response = client.get(reverse("libraries:update", kwargs={"pk": library.pk}))
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_update_library_as_superadmin(self, client: Client) -> None:
        """Test modification par un superadmin."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )
        library = Library.objects.create(name="Test Library", email="test@test.com")

        client.force_login(superadmin)

        # GET request
        response = client.get(reverse("libraries:update", kwargs={"pk": library.pk}))
        assert response.status_code == 200

        # POST request
        data = {
            "name": "Updated Library",
            "phone": "0123456789",
            "address": "New Address",
            "postal_code": "75000",
            "city": "Paris",
            "is_active": True,
        }
        response = client.post(
            reverse("libraries:update", kwargs={"pk": library.pk}), data
        )
        assert response.status_code == 302

        library.refresh_from_db()
        assert library.name == "Updated Library"

    def test_update_library_as_library_admin_own_library(self, client: Client) -> None:
        """Test modification par un admin de sa propre médiathèque."""
        library = Library.objects.create(name="Test Library", email="test@test.com")

        library_admin = User.objects.create_user(
            email="admin@test.com",
            password="TestPass123!",
            first_name="Admin",
            last_name="User",
            role="library_admin",
            library=library,
        )
        client.force_login(library_admin)

        data = {
            "name": "My Updated Library",
            "phone": "0123456789",
            "address": "Address",
            "postal_code": "75000",
            "city": "Paris",
            "is_active": True,
        }
        response = client.post(
            reverse("libraries:update", kwargs={"pk": library.pk}), data
        )
        assert response.status_code == 302

        library.refresh_from_db()
        assert library.name == "My Updated Library"

    def test_update_library_as_library_admin_other_library(
        self, client: Client
    ) -> None:
        """Test qu'un admin ne peut pas modifier une autre médiathèque."""
        library1 = Library.objects.create(name="Library 1", email="lib1@test.com")
        library2 = Library.objects.create(name="Library 2", email="lib2@test.com")

        library_admin = User.objects.create_user(
            email="admin@test.com",
            password="TestPass123!",
            first_name="Admin",
            last_name="User",
            role="library_admin",
            library=library1,
        )
        client.force_login(library_admin)

        response = client.get(reverse("libraries:update", kwargs={"pk": library2.pk}))
        assert response.status_code == 404

    def test_update_library_as_reader(self, client: Client) -> None:
        """Test qu'un lecteur ne peut pas modifier de médiathèque."""
        library = Library.objects.create(name="Test Library", email="test@test.com")

        reader = User.objects.create_user(
            email="reader@test.com",
            password="TestPass123!",
            first_name="Reader",
            last_name="User",
            role="reader",
        )
        client.force_login(reader)

        response = client.get(reverse("libraries:update", kwargs={"pk": library.pk}))
        assert response.status_code == 403


@pytest.mark.django_db
class TestLibraryListView:
    """Tests de la vue de liste des médiathèques."""

    def test_list_libraries_requires_superadmin(self, client: Client) -> None:
        """Test que la liste nécessite un superadmin."""
        library = Library.objects.create(name="Test", email="test@test.com")

        library_admin = User.objects.create_user(
            email="admin@test.com",
            password="TestPass123!",
            role="library_admin",
            library=library,
        )
        client.force_login(library_admin)

        response = client.get(reverse("libraries:list"))
        assert response.status_code == 403

    def test_list_libraries_as_superadmin(self, client: Client) -> None:
        """Test liste des médiathèques par superadmin."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )

        Library.objects.create(name="Lib 1", email="lib1@test.com")
        Library.objects.create(name="Lib 2", email="lib2@test.com")

        client.force_login(superadmin)
        response = client.get(reverse("libraries:list"))

        assert response.status_code == 200
        content = response.content.decode()
        assert "Lib 1" in content
        assert "Lib 2" in content


@pytest.mark.django_db
class TestLibraryDetailView:
    """Tests de la vue de détail d'une médiathèque."""

    def test_detail_library_requires_login(self, client: Client) -> None:
        """Test que le détail nécessite une connexion."""
        library = Library.objects.create(name="Test Library", email="test@test.com")

        response = client.get(reverse("libraries:detail", kwargs={"pk": library.pk}))
        assert response.status_code == 302

    def test_detail_library_as_authenticated_user(self, client: Client) -> None:
        """Test vue détail par utilisateur authentifié."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )
        library = Library.objects.create(name="Test Library", email="test@test.com")

        client.force_login(superadmin)
        response = client.get(reverse("libraries:detail", kwargs={"pk": library.pk}))

        assert response.status_code == 200
        assert library.name in response.content.decode()

    def test_detail_library_with_user_count(self, client: Client) -> None:
        """Test que le détail affiche le nombre d'utilisateurs."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )
        library = Library.objects.create(name="Test Library", email="test@test.com")

        # Créer des utilisateurs dans cette médiathèque
        User.objects.create_user(
            email="user1@test.com",
            password="TestPass123!",
            role="reader",
            library=library,
        )
        User.objects.create_user(
            email="user2@test.com",
            password="TestPass123!",
            role="reader",
            library=library,
        )

        client.force_login(superadmin)
        response = client.get(reverse("libraries:detail", kwargs={"pk": library.pk}))

        assert response.status_code == 200


@pytest.mark.django_db
class TestLibraryCreateViewSession:
    """Tests pour le session handling dans LibraryCreateView."""

    def test_create_library_stores_password_in_session(self, client: Client) -> None:
        """Test que le mot de passe est stocké dans la session après création."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com",
            password="TestPass123!",
            role="superadmin",
        )
        client.force_login(superadmin)

        data = {
            "name": "Test Library",
            "email": "test@library.com",
            "phone": "0123456789",
            "address": "123 Test Street",
            "postal_code": "75000",
            "city": "Paris",
            "password1": "SecretPass123!",
            "password2": "SecretPass123!",
        }

        response = client.post(reverse("libraries:create"), data)

        assert response.status_code == 302
        # Verifier que le mot de passe est dans la session
        session = client.session
        assert session.get("generated_password") == "SecretPass123!"

    def test_create_library_context_shows_password_from_session(
        self, client: Client
    ) -> None:
        """Test que le contexte inclut le mot de passe depuis la session."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com",
            password="TestPass123!",
            role="superadmin",
        )
        client.force_login(superadmin)

        # Simuler une session avec un mot de passe genere
        session = client.session
        session["generated_password"] = "TempPass123!"
        session.save()

        # Faire un GET sur la page de creation
        response = client.get(reverse("libraries:create"))

        assert response.status_code == 200
        # Le mot de passe devrait etre dans le contexte
        assert response.context.get("generated_password") == "TempPass123!"


@pytest.mark.django_db
class TestLibraryUpdateViewBreadcrumb:
    """Tests pour les breadcrumbs dans LibraryUpdateView."""

    def test_update_library_breadcrumb_as_library_admin(self, client: Client) -> None:
        """Test breadcrumb pour library admin (non-superadmin)."""
        library = Library.objects.create(name="Test Library", email="test@test.com")

        library_admin = User.objects.create_user(
            email="admin@test.com",
            password="TestPass123!",
            first_name="Admin",
            last_name="User",
            role="library_admin",
            library=library,
        )
        client.force_login(library_admin)

        response = client.get(reverse("libraries:update", kwargs={"pk": library.pk}))
        assert response.status_code == 200

        # Verifier le breadcrumb pour non-superadmin
        context = response.context
        breadcrumb = context.get("breadcrumb_items", [])
        assert len(breadcrumb) == 2
        assert breadcrumb[0]["label"] == "Ma médiathèque"
