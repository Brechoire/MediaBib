"""
Tests pour le formulaire LibraryCreateForm.
"""

import pytest
from django.contrib.auth import get_user_model

from libraries.forms import LibraryCreateForm
from libraries.models import Library

User = get_user_model()


@pytest.mark.django_db
class TestLibraryCreateForm:
    """Tests pour LibraryCreateForm."""

    def test_clean_password2_matching_passwords(self) -> None:
        """Test clean_password2 avec des mots de passe correspondants."""
        form_data = {
            "name": "Test Library",
            "email": "test@library.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
        }
        form = LibraryCreateForm(data=form_data)

        # Le formulaire doit être valide
        assert form.is_valid()
        assert form.clean_password2() == "TestPass123!"

    def test_clean_password2_non_matching_passwords(self) -> None:
        """Test clean_password2 avec des mots de passe ne correspondant pas."""
        form_data = {
            "name": "Test Library",
            "email": "test@library.com",
            "password1": "TestPass123!",
            "password2": "DifferentPass123!",
        }
        form = LibraryCreateForm(data=form_data)

        # Le formulaire ne doit pas être valide
        assert not form.is_valid()
        assert "password2" in form.errors

    def test_clean_password2_missing_password2(self) -> None:
        """Test clean_password2 quand password2 est manquant."""
        form_data = {
            "name": "Test Library",
            "email": "test@library.com",
            "password1": "TestPass123!",
            # password2 est manquant
        }
        form = LibraryCreateForm(data=form_data)

        # Le formulaire ne doit pas être valide
        assert not form.is_valid()
        # clean_password2 retourne une chaîne vide si password2 est None

    def test_save_creates_library_and_user(self) -> None:
        """Test que save crée la médiathèque et l'utilisateur admin."""
        form_data = {
            "name": "Test Library",
            "email": "test@library.com",
            "phone": "0123456789",
            "address": "123 Test Street",
            "postal_code": "75000",
            "city": "Paris",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
        }
        form = LibraryCreateForm(data=form_data)

        assert form.is_valid()
        library = form.save()

        # Vérifier que la médiathèque a été créée
        assert Library.objects.filter(email="test@library.com").exists()
        assert library.name == "Test Library"

        # Vérifier que l'utilisateur admin a été créé
        assert User.objects.filter(email="test@library.com").exists()
        admin_user = User.objects.get(email="test@library.com")
        assert admin_user.role == "library_admin"
        assert admin_user.library == library

    def test_save_without_commit(self) -> None:
        """Test save avec commit=False."""
        form_data = {
            "name": "Test Library",
            "email": "test@library.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
        }
        form = LibraryCreateForm(data=form_data)

        assert form.is_valid()
        library = form.save(commit=False)

        # La médiathèque existe mais n'est pas encore sauvegardée en DB
        assert library.name == "Test Library"

        # L'utilisateur admin ne doit pas être créé
        assert not User.objects.filter(email="test@library.com").exists()
