from django.apps import AppConfig


class ConfigConfig(AppConfig):
    """Configuration de l'app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "config"
    verbose_name = "Configuration du site"
