"""
Tests du modèle Library.
"""

import pytest

from libraries.models import Library


@pytest.mark.django_db
class TestLibraryModel:
    """Tests du modèle Library."""

    def test_library_creation(self) -> None:
        """Test la création d'une médiathèque."""
        library = Library.objects.create(
            name="Médiathèque de Test",
            email="mediatheque@test.com",
            phone="0123456789",
            address="123 Rue de Test",
            postal_code="75000",
            city="Paris",
        )

        assert library.name == "Médiathèque de Test"
        assert library.email == "mediatheque@test.com"
        assert library.is_active is True
        assert library.id is not None

    def test_library_str_method(self) -> None:
        """Test la méthode __str__ du modèle."""
        library = Library.objects.create(
            name="Médiathèque de Test", email="mediatheque@test.com"
        )

        assert str(library) == "Médiathèque de Test"

    def test_library_unique_email(self) -> None:
        """Test que l'email doit être unique."""
        Library.objects.create(name="Première Médiathèque", email="test@example.com")

        with pytest.raises(Exception):  # IntegrityError
            Library.objects.create(
                name="Deuxième Médiathèque", email="test@example.com"
            )

    def test_library_active_status(self) -> None:
        """Test le statut actif/inactif."""
        library = Library.objects.create(
            name="Médiathèque Active", email="active@test.com", is_active=True
        )

        assert library.is_active is True

        library.is_active = False
        library.save()

        assert library.is_active is False
