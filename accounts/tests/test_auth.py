"""
Tests de l'authentification et de l'inscription.
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


@pytest.mark.django_db
class TestSuperAdminRegistration:
    """Tests de l'inscription du premier superadmin."""

    def test_setup_page_renders_when_no_users(self, client) -> None:
        """Test que la page d'inscription s'affiche quand il n'y a pas d'utilisateurs."""
        response = client.get(reverse("accounts:setup"))
        
        assert response.status_code == 200

    def test_setup_redirects_to_home_when_users_exist(self, client) -> None:
        """Test que la page redirige vers l'accueil si des utilisateurs existent."""
        User.objects.create_user(
            email="existing@test.com",
            password="TestPass123!",
            role="reader"
        )
        
        response = client.get(reverse("accounts:setup"))
        
        assert response.status_code == 302
        assert response.url == reverse("home")

    def test_setup_creates_superadmin(self, client) -> None:
        """Test que l'inscription crée un superadmin."""
        data = {
            "email": "superadmin@test.com",
            "first_name": "Super",
            "last_name": "Admin",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!"
        }
        
        response = client.post(reverse("accounts:setup"), data)
        
        assert response.status_code == 302
        assert User.objects.filter(email="superadmin@test.com").exists()
        
        user = User.objects.get(email="superadmin@test.com")
        assert user.role == "superadmin"
        assert user.is_superuser is True

    def test_setup_validates_email(self, client) -> None:
        """Test que l'email est validé."""
        data = {
            "email": "invalid-email",
            "first_name": "Test",
            "last_name": "User",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!"
        }
        
        response = client.post(reverse("accounts:setup"), data)
        
        assert response.status_code == 200
        assert not User.objects.filter(email="invalid-email").exists()
        assert "email" in response.context["form"].errors

    def test_setup_passwords_must_match(self, client) -> None:
        """Test que les mots de passe doivent correspondre."""
        data = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "ComplexPass123!",
            "password2": "DifferentPass123!"
        }
        
        response = client.post(reverse("accounts:setup"), data)
        
        assert response.status_code == 200
        assert not User.objects.filter(email="test@test.com").exists()
        assert "password2" in response.context["form"].errors


@pytest.mark.django_db
class TestLoginLogout:
    """Tests de connexion et déconnexion."""

    def test_login_page_renders(self, client) -> None:
        """Test que la page de connexion s'affiche."""
        response = client.get(reverse("accounts:login"))
        
        assert response.status_code == 200

    def test_login_with_valid_credentials(self, client) -> None:
        """Test la connexion avec des identifiants valides."""
        User.objects.create_user(
            email="user@test.com",
            password="TestPass123!",
            role="reader"
        )
        
        data = {
            "username": "user@test.com",
            "password": "TestPass123!"
        }
        response = client.post(reverse("accounts:login"), data)
        
        assert response.status_code == 302

    def test_login_with_invalid_credentials(self, client) -> None:
        """Test la connexion avec des identifiants invalides."""
        User.objects.create_user(
            email="user@test.com",
            password="TestPass123!",
            role="reader"
        )
        
        data = {
            "username": "user@test.com",
            "password": "WrongPassword123!"
        }
        response = client.post(reverse("accounts:login"), data)
        
        assert response.status_code == 200
        assert "__all__" in response.context["form"].errors or "form" in response.context

    def test_logout_redirects_to_home(self, client) -> None:
        """Test que la déconnexion redirige vers l'accueil."""
        user = User.objects.create_user(
            email="user@test.com",
            password="TestPass123!",
            role="reader"
        )
        client.force_login(user)
        
        response = client.post(reverse("accounts:logout"))
        
        assert response.status_code == 302
        assert response.url == reverse("home")


@pytest.mark.django_db
class TestPasswordChange:
    """Tests du changement de mot de passe."""

    def test_password_change_requires_login(self, client) -> None:
        """Test que le changement de mot de passe nécessite une connexion."""
        response = client.get(reverse("accounts:password_change"))
        
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_password_change_validates_old_password(self, client) -> None:
        """Test que l'ancien mot de passe doit être valide."""
        user = User.objects.create_user(
            email="user@test.com",
            password="OldPass123!",
            role="reader"
        )
        client.force_login(user)
        
        data = {
            "old_password": "WrongOldPass123!",
            "new_password1": "NewPass123!",
            "new_password2": "NewPass123!"
        }
        response = client.post(reverse("accounts:password_change"), data)
        
        assert response.status_code == 200
        assert "old_password" in response.context["form"].errors

    def test_password_change_success(self, client) -> None:
        """Test le changement réussi de mot de passe."""
        user = User.objects.create_user(
            email="user@test.com",
            password="OldPass123!",
            role="reader"
        )
        client.force_login(user)
        
        data = {
            "old_password": "OldPass123!",
            "new_password1": "NewPass123!",
            "new_password2": "NewPass123!"
        }
        response = client.post(reverse("accounts:password_change"), data)
        
        assert response.status_code == 302
        
        # Vérifier que le mot de passe a été changé
        user.refresh_from_db()
        assert user.check_password("NewPass123!")
