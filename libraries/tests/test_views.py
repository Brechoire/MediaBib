"""
Tests des vues de gestion des médiathèques.
"""


import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from libraries.models import Library

User = get_user_model()


@pytest.mark.django_db
class TestLibraryCreation:
    """Tests de la création de médiathèques par le superadmin."""

    def test_create_library_requires_superadmin(self, client: Client) -> None:
        """Test que la création de médiathèque nécessite un superadmin."""
        # Créer un utilisateur normal
        user = User.objects.create_user(
            email="user@test.com", password="TestPass123!", role="reader"
        )
        client.force_login(user)

        response = client.get(reverse("libraries:create"))

        # Devrait être interdit (403) ou redirigé
        assert response.status_code in [302, 403]

    def test_create_library_page_renders_for_superadmin(self, client: Client) -> None:
        """Test que la page de création s'affiche pour le superadmin."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )
        client.force_login(superadmin)

        response = client.get(reverse("libraries:create"))

        assert response.status_code == 200

    def test_create_library_success(self, client: Client) -> None:
        """Test la création réussie d'une médiathèque."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )
        client.force_login(superadmin)

        data = {
            "name": "Nouvelle Médiathèque",
            "email": "nouvelle@test.com",
            "phone": "0123456789",
            "address": "123 Rue Nouvelle",
            "postal_code": "75000",
            "city": "Paris",
            "password1": "LibPass123!",
            "password2": "LibPass123!",
        }

        response = client.post(reverse("libraries:create"), data)

        assert response.status_code == 302
        assert Library.objects.filter(name="Nouvelle Médiathèque").exists()

    def test_create_library_creates_admin_user(self, client: Client) -> None:
        """Test que la création de médiathèque crée aussi un admin."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )
        client.force_login(superadmin)

        data = {
            "name": "Médiathèque avec Admin",
            "email": "admin_lib@test.com",
            "phone": "0123456789",
            "address": "123 Rue Test",
            "postal_code": "75000",
            "city": "Paris",
            "password1": "AdminPass123!",
            "password2": "AdminPass123!",
        }

        response = client.post(reverse("libraries:create"), data)

        assert response.status_code == 302

        # Vérifier que la médiathèque existe
        library = Library.objects.get(email="admin_lib@test.com")

        # Vérifier que l'utilisateur admin a été créé
        admin_user = User.objects.filter(
            email="admin_lib@test.com", role="library_admin"
        ).first()

        assert admin_user is not None
        assert admin_user.library == library
