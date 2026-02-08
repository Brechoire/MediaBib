"""
Tests pour l'admin configuration.
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from config.models import SiteConfig

User = get_user_model()


@pytest.mark.django_db
class TestSiteConfigAdmin:
    """Tests pour l'admin SiteConfig."""

    def test_site_config_admin_has_add_permission_no_config(
        self, client: Client
    ) -> None:
        """Test has_add_permission retourne True quand aucune config n'existe."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )
        client.force_login(superadmin)

        # Aucune config n'existe, donc has_add_permission doit retourner True
        response = client.get(reverse("admin:config_siteconfig_add"))
        assert response.status_code == 200

    def test_site_config_admin_has_add_permission_with_config(
        self, client: Client
    ) -> None:
        """Test has_add_permission retourne False quand une config existe."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )
        client.force_login(superadmin)

        # Créer une config
        SiteConfig.objects.create(site_name="Test Site")

        # Une config existe, donc has_add_permission doit retourner False
        response = client.get(reverse("admin:config_siteconfig_add"))
        assert response.status_code == 403

    def test_site_config_admin_has_delete_permission(self, client: Client) -> None:
        """Test has_delete_permission retourne toujours False."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )
        client.force_login(superadmin)

        # Créer une config
        config = SiteConfig.objects.create(site_name="Test Site")

        # has_delete_permission doit retourner False
        response = client.post(
            reverse("admin:config_siteconfig_delete", args=[config.pk])
        )
        assert response.status_code == 403

    def test_site_config_admin_fieldsets(self, client: Client) -> None:
        """Test que les fieldsets sont correctement configurés."""
        superadmin = User.objects.create_superuser(
            email="superadmin@test.com", password="TestPass123!", role="superadmin"
        )
        client.force_login(superadmin)

        # Créer une config
        SiteConfig.objects.create(site_name="Test Site")

        response = client.get(reverse("admin:config_siteconfig_change", args=[1]))
        assert response.status_code == 200
        content = response.content.decode()

        # Vérifier les fieldsets
        assert "Informations générales" in content
        assert "Contact" in content
        assert "Apparence" in content
        assert "Maintenance" in content
