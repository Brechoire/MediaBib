"""
Tests pour les modèles de configuration.
"""

import pytest

from config.models import SiteConfig


@pytest.mark.django_db
class TestSiteConfigModel:
    """Tests pour le modèle SiteConfig."""

    def test_site_config_creation(self) -> None:
        """Test la création d'une configuration."""
        config = SiteConfig.objects.create(
            site_name="Test Site",
            site_description="Description de test",
            contact_email="test@example.com",
        )

        assert config.site_name == "Test Site"
        assert config.site_description == "Description de test"
        assert config.contact_email == "test@example.com"
        assert config.pk == 1

    def test_site_config_str_method(self) -> None:
        """Test la méthode __str__."""
        config = SiteConfig.objects.create(site_name="Test Site")
        assert str(config) == "Test Site"

    def test_site_config_get_solo_creates_if_not_exists(self) -> None:
        """Test que get_solo crée une config si elle n'existe pas."""
        assert SiteConfig.objects.count() == 0

        config = SiteConfig.get_solo()

        assert SiteConfig.objects.count() == 1
        assert config.pk == 1
        assert config.site_name == "MediaBibli"  # Valeur par défaut

    def test_site_config_get_solo_returns_existing(self) -> None:
        """Test que get_solo retourne la config existante."""
        existing = SiteConfig.objects.create(
            site_name="Custom Site",
            pk=1,
        )

        config = SiteConfig.get_solo()

        assert config == existing
        assert config.site_name == "Custom Site"

    def test_site_config_save_ensures_pk_1(self) -> None:
        """Test que save force pk=1."""
        config = SiteConfig(site_name="Test Site")
        config.save()

        assert config.pk == 1

        # Essayer de créer une deuxième config
        config2 = SiteConfig(site_name="Second Site")
        config2.save()

        # La deuxième config doit aussi avoir pk=1 (écrase la première)
        assert config2.pk == 1
        assert SiteConfig.objects.count() == 1

    def test_site_config_default_values(self) -> None:
        """Test les valeurs par défaut."""
        config = SiteConfig.get_solo()

        assert config.site_name == "MediaBibli"
        assert config.primary_color == "#2563eb"
        assert config.maintenance_mode is False

    def test_site_config_meta_options(self) -> None:
        """Test les options Meta."""
        assert SiteConfig._meta.verbose_name == "Configuration du site"
        assert SiteConfig._meta.verbose_name_plural == "Configuration du site"
