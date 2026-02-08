"""
Tests pour le context processor - exception handling.
"""

from unittest.mock import patch

import pytest
from django.test import RequestFactory

from config.context_processors import site_config
from config.models import SiteConfig


@pytest.mark.django_db
class TestSiteConfigContextProcessorExceptions:
    """Tests pour le exception handling du context processor."""

    def test_site_config_exception_handling(self) -> None:
        """Test que site_config gère les exceptions gracieusement."""
        # Mock get_solo pour lever une exception
        with patch.object(SiteConfig, "get_solo", side_effect=Exception("DB Error")):
            factory = RequestFactory()
            request = factory.get("/")

            result = site_config(request)

            # En cas d'exception, config doit être None
            assert "site_config" in result
            assert result["site_config"] is None

    def test_site_config_with_cache_exception(self) -> None:
        """Test site_config quand le cache échoue."""
        # Créer une config
        SiteConfig.objects.create(site_name="Test Site")

        # Mock cache.get pour retourner None (cache miss)
        with patch("django.core.cache.cache.get", return_value=None):
            factory = RequestFactory()
            request = factory.get("/")

            result = site_config(request)

            assert "site_config" in result
            assert result["site_config"] is not None
