from django.apps import AppConfig


class LibrariesConfig(AppConfig):
    """Configuration de l'app libraries."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "libraries"
    verbose_name = "Gestion des médiathèques"
