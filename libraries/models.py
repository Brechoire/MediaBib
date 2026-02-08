"""
Modèles de l'app libraries.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Library(models.Model):
    """Représente une médiathèque dans le système."""

    name = models.CharField(
        verbose_name=_("Nom"), max_length=200, help_text=_("Nom de la médiathèque")
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        unique=True,
        help_text=_("Adresse email de contact de la médiathèque"),
    )
    phone = models.CharField(
        verbose_name=_("Téléphone"),
        max_length=20,
        blank=True,
        help_text=_("Numéro de téléphone de la médiathèque"),
    )
    address = models.TextField(
        verbose_name=_("Adresse"),
        blank=True,
        help_text=_("Adresse complète de la médiathèque"),
    )
    postal_code = models.CharField(
        verbose_name=_("Code postal"), max_length=10, blank=True
    )
    city = models.CharField(verbose_name=_("Ville"), max_length=100, blank=True)
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
        db_index=True,
        help_text=_("Désactivez cette case pour désactiver la médiathèque"),
    )
    created_at = models.DateTimeField(
        verbose_name=_("Date de création"), auto_now_add=True, db_index=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Date de modification"), auto_now=True
    )

    class Meta:
        verbose_name = _("Médiathèque")
        verbose_name_plural = _("Médiathèques")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_active", "-created_at"]),
            models.Index(fields=["city", "is_active"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        """Retourne la représentation textuelle de la médiathèque."""
        return str(self.name)
