from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration de l'app accounts."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "Gestion des utilisateurs"
