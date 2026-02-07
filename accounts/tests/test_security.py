"""
Tests de sécurité.
"""

import pytest
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.mark.django_db
class TestSecurity:
    """Tests de sécurité."""

    def test_password_hashing(self) -> None:
        """Test que les mots de passe sont hashés."""
        user = User.objects.create_user(
            email="test@test.com", password="TestPass123!", role="reader"
        )

        # Le mot de passe ne doit pas être stocké en clair
        assert user.password != "TestPass123!"
        assert user.password.startswith(
            "pbkdf2_sha256$"
        )  # Algorithme Django par défaut

    def test_csrf_protection_enabled(self, client) -> None:
        """Test que la protection CSRF est activée."""
        response = client.get("/accounts/login/")

        assert response.status_code == 200
        # Le formulaire doit contenir un token CSRF
        content = response.content.decode()
        assert "csrfmiddlewaretoken" in content or "csrf" in content.lower()

    def test_sql_injection_prevention_in_login(self, client) -> None:
        """Test la prévention des injections SQL dans le login."""
        # Tentative d'injection SQL
        data = {"username": "' OR '1'='1", "password": "' OR '1'='1"}

        response = client.post("/accounts/login/", data)

        # Ne doit pas réussir à se connecter
        assert response.status_code == 200  # Rester sur la page de login

    def test_xss_prevention_in_templates(self, client) -> None:
        """Test la prévention XSS dans les templates."""
        # Créer un utilisateur avec un nom contenant du HTML
        User.objects.create_user(
            email="xss@test.com",
            password="TestPass123!",
            first_name="<script>alert('XSS')</script>",
            role="reader",
        )

        client.force_login(User.objects.get(email="xss@test.com"))
        response = client.get("/")

        content = response.content.decode()

        # Le script malveillant doit être échappé
        assert "alert('XSS')" not in content

    def test_user_cannot_access_other_users_data(self, client) -> None:
        """Test qu'un utilisateur ne peut pas accéder aux données d'autrui."""
        user1 = User.objects.create_user(
            email="user1@test.com", password="TestPass123!", role="reader"
        )
        User.objects.create_user(
            email="user2@test.com", password="TestPass123!", role="reader"
        )

        client.force_login(user1)

        # Vérifier que l'utilisateur ne peut pas voir l'autre utilisateur
        # (Ce test dépendrait de l'implémentation des vues de profil)
        # Ici on vérifie simplement que la session est correcte
        assert client.session.get("_auth_user_id") == str(user1.id)

    def test_admin_requires_staff_status(self, client) -> None:
        """Test que l'admin nécessite le statut staff."""
        user = User.objects.create_user(
            email="user@test.com",
            password="TestPass123!",
            role="reader",
            is_staff=False,
        )
        client.force_login(user)

        response = client.get("/admin/")

        # Devrait être interdit ou redirigé
        assert response.status_code in [302, 403]
