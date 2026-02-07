"""
Tests du modèle CustomUser.
"""

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()


@pytest.mark.django_db
class TestCustomUserModel:
    """Tests du modèle CustomUser."""

    def test_create_superadmin_user(self) -> None:
        """Test la création d'un utilisateur superadmin."""
        user = User.objects.create_superuser(
            email="superadmin@test.com",
            password="TestPass123!",
            first_name="Super",
            last_name="Admin",
            role="superadmin",
        )

        assert user.email == "superadmin@test.com"
        assert user.role == "superadmin"
        assert user.is_superuser is True
        assert user.is_staff is True
        assert user.check_password("TestPass123!") is True

    def test_create_library_admin_user(self) -> None:
        """Test la création d'un utilisateur admin de médiathèque."""
        user = User.objects.create_user(
            email="library@test.com",
            password="TestPass123!",
            first_name="Library",
            last_name="Admin",
            role="library_admin",
        )

        assert user.email == "library@test.com"
        assert user.role == "library_admin"
        assert user.is_superuser is False
        assert user.is_staff is False

    def test_create_reader_user(self) -> None:
        """Test la création d'un utilisateur lecteur."""
        user = User.objects.create_user(
            email="reader@test.com",
            password="TestPass123!",
            first_name="John",
            last_name="Reader",
            role="reader",
        )

        assert user.email == "reader@test.com"
        assert user.role == "reader"
        assert user.is_superuser is False
        assert user.is_staff is False

    def test_user_str_method(self) -> None:
        """Test la méthode __str__ du modèle."""
        user = User.objects.create_user(
            email="test@test.com",
            password="TestPass123!",
            first_name="John",
            last_name="Doe",
            role="reader",
        )

        assert str(user) == "test@test.com"

    def test_user_email_normalized(self) -> None:
        """Test que l'email est normalisé en minuscules."""
        user = User.objects.create_user(
            email="TEST@EXAMPLE.COM", password="TestPass123!", role="reader"
        )

        assert user.email == "test@example.com"

    def test_user_email_required(self) -> None:
        """Test que l'email est obligatoire."""
        with pytest.raises(ValueError, match="L'adresse email est obligatoire"):
            User.objects.create_user(email="", password="TestPass123!", role="reader")

    def test_user_role_choices(self) -> None:
        """Test que le rôle utilise les bons choix."""
        valid_roles = ["superadmin", "library_admin", "reader"]

        for role in valid_roles:
            user = User.objects.create_user(
                email=f"{role}@test.com", password="TestPass123!", role=role
            )
            assert user.role == role

    def test_user_is_superadmin_property(self) -> None:
        """Test la propriété is_superadmin."""
        superadmin = User.objects.create_user(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )
        admin = User.objects.create_user(
            email="admin@test.com", password="TestPass123!", role="library_admin"
        )
        reader = User.objects.create_user(
            email="reader@test.com", password="TestPass123!", role="reader"
        )

        assert superadmin.is_superadmin is True
        assert admin.is_superadmin is False
        assert reader.is_superadmin is False

    def test_user_is_library_admin_property(self) -> None:
        """Test la propriété is_library_admin."""
        superadmin = User.objects.create_user(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )
        admin = User.objects.create_user(
            email="admin@test.com", password="TestPass123!", role="library_admin"
        )
        reader = User.objects.create_user(
            email="reader@test.com", password="TestPass123!", role="reader"
        )

        assert superadmin.is_library_admin is False
        assert admin.is_library_admin is True
        assert reader.is_library_admin is False

    def test_user_is_reader_property(self) -> None:
        """Test la propriété is_reader."""
        superadmin = User.objects.create_user(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )
        admin = User.objects.create_user(
            email="admin@test.com", password="TestPass123!", role="library_admin"
        )
        reader = User.objects.create_user(
            email="reader@test.com", password="TestPass123!", role="reader"
        )

        assert superadmin.is_reader is False
        assert admin.is_reader is False
        assert reader.is_reader is True

    def test_create_user_without_email_raises_error(self) -> None:
        """Test que la création sans email lève une erreur."""
        with pytest.raises(ValueError, match="L'adresse email est obligatoire"):
            User.objects.create_user(email="", password="TestPass123!", role="reader")

    def test_create_superuser_without_is_staff(self) -> None:
        """Test qu'un superuser doit avoir is_staff=True."""
        with pytest.raises(
            ValueError, match="Le superutilisateur doit avoir is_staff=True"
        ):
            User.objects.create_superuser(
                email="superadmin@test.com", password="TestPass123!", is_staff=False
            )

    def test_create_superuser_without_is_superuser(self) -> None:
        """Test qu'un superuser doit avoir is_superuser=True."""
        with pytest.raises(
            ValueError, match="Le superutilisateur doit avoir is_superuser=True"
        ):
            User.objects.create_superuser(
                email="superadmin@test.com", password="TestPass123!", is_superuser=False
            )
