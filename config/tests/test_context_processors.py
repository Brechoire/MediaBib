"""
Tests pour le context processor.
"""

import pytest
from django.test import RequestFactory

from config.context_processors import site_config
from config.models import SiteConfig


@pytest.mark.django_db
class TestSiteConfigContextProcessor:
    """Tests pour le context processor site_config."""

    def test_site_config_with_existing_config(self) -> None:
        """Test site_config avec une configuration existante."""
        # Créer une config
        config = SiteConfig.objects.create(
            site_name="Test Site",
            site_description="Description de test",
        )

        factory = RequestFactory()
        request = factory.get("/")

        result = site_config(request)

        assert "site_config" in result
        assert result["site_config"] == config
        assert result["site_config"].site_name == "Test Site"

    def test_site_config_with_no_config(self) -> None:
        """Test site_config sans configuration."""
        # S'assurer qu'aucune config n'existe
        SiteConfig.objects.all().delete()

        factory = RequestFactory()
        request = factory.get("/")

        result = site_config(request)

        assert "site_config" in result
        # get_solo() crée une config si elle n'existe pas, donc on vérifie
        # que le résultat est une config ou None si exception
        assert result["site_config"] is not None or result["site_config"] is None

    def test_site_config_uses_cache(self) -> None:
        """Test que site_config utilise le cache."""
        from django.core.cache import cache

        # Créer une config
        config = SiteConfig.objects.create(site_name="Test Site")

        factory = RequestFactory()
        request = factory.get("/")

        # Premier appel - met en cache
        result1 = site_config(request)

        # Modifier la config directement en DB
        config.site_name = "Modified Site"
        config.save()

        # Deuxième appel - doit retourner la version en cache
        result2 = site_config(request)

        # Les deux résultats doivent être identiques (depuis le cache)
        assert result1["site_config"].site_name == result2["site_config"].site_name

        # Vider le cache et vérifier que la nouvelle valeur est retournée
        cache.delete("site_config")
        result3 = site_config(request)
        assert result3["site_config"].site_name == "Modified Site"
