"""
Tests pour les modèles accounts.
"""

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestCustomUserMethods:
    """Tests pour les méthodes de CustomUser."""

    def test_get_full_name_with_names(self) -> None:
        """Test get_full_name avec prénom et nom."""
        user = User.objects.create_user(
            email="test@test.com",
            password="TestPass123!",
            first_name="John",
            last_name="Doe",
            role="reader",
        )

        assert user.get_full_name() == "John Doe"

    def test_get_full_name_without_names(self) -> None:
        """Test get_full_name sans prénom ni nom."""
        user = User.objects.create_user(
            email="test@test.com",
            password="TestPass123!",
            first_name="",
            last_name="",
            role="reader",
        )

        # Doit retourner l'email si pas de nom
        assert user.get_full_name() == "test@test.com"

    def test_get_full_name_with_only_first_name(self) -> None:
        """Test get_full_name avec seulement le prénom."""
        user = User.objects.create_user(
            email="test@test.com",
            password="TestPass123!",
            first_name="John",
            last_name="",
            role="reader",
        )

        assert user.get_full_name() == "John"

    def test_get_short_name_with_first_name(self) -> None:
        """Test get_short_name avec prénom."""
        user = User.objects.create_user(
            email="test@test.com",
            password="TestPass123!",
            first_name="John",
            last_name="Doe",
            role="reader",
        )

        assert user.get_short_name() == "John"

    def test_get_short_name_without_first_name(self) -> None:
        """Test get_short_name sans prénom."""
        user = User.objects.create_user(
            email="test@test.com",
            password="TestPass123!",
            first_name="",
            last_name="Doe",
            role="reader",
        )

        # Doit retourner l'email si pas de prénom
        assert user.get_short_name() == "test@test.com"
