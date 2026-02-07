"""
Modèles de l'app config.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteConfig(models.Model):
    """Configuration globale du site MediaBibli."""

    site_name = models.CharField(
        verbose_name=_("Nom du site"),
        max_length=100,
        default="MediaBibli",
        help_text=_("Nom affiché dans le logo et le titre du site"),
    )
    site_description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        help_text=_("Description du site affichée dans les métadonnées"),
    )
    contact_email = models.EmailField(
        verbose_name=_("Email de contact"),
        blank=True,
        help_text=_("Adresse email de contact affichée publiquement"),
    )
    contact_phone = models.CharField(
        verbose_name=_("Téléphone de contact"), max_length=20, blank=True
    )
    address = models.TextField(verbose_name=_("Adresse"), blank=True)
    logo = models.ImageField(
        verbose_name=_("Logo"), upload_to="config/logos/", blank=True, null=True
    )
    favicon = models.ImageField(
        verbose_name=_("Favicon"), upload_to="config/favicons/", blank=True, null=True
    )
    primary_color = models.CharField(
        verbose_name=_("Couleur principale"),
        max_length=7,
        default="#2563eb",
        help_text=_("Code couleur hexadécimal (ex: #2563eb)"),
    )
    maintenance_mode = models.BooleanField(
        verbose_name=_("Mode maintenance"),
        default=False,
        help_text=_("Activez pour afficher une page de maintenance"),
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Dernière modification"), auto_now=True
    )

    class Meta:
        verbose_name = _("Configuration du site")
        verbose_name_plural = _("Configuration du site")

    def __str__(self) -> str:
        return self.site_name

    @classmethod
    def get_solo(cls) -> "SiteConfig":
        """Retourne l'instance unique de configuration (crée si inexistante)."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def save(self, *args, **kwargs) -> None:
        """S'assure qu'il n'y a qu'une seule instance."""
        self.pk = 1
        super().save(*args, **kwargs)
