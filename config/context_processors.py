"""
Context processor pour la configuration du site.
"""

from django.core.cache import cache

from .models import SiteConfig


def site_config(request):
    """Ajoute la configuration du site au contexte de toutes les requêtes (avec cache)."""
    cache_key = "site_config"
    config = cache.get(cache_key)

    if config is None:
        try:
            config = SiteConfig.get_solo()
            cache.set(cache_key, config, 3600)  # Cache 1 heure
        except Exception:
            config = None

    return {
        "site_config": config,
    }
