"""
Admin configuration pour l'app config.
"""

from typing import Any

from django.contrib import admin
from django.http import HttpRequest

from .models import SiteConfig


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour SiteConfig."""

    fieldsets = (
        ("Informations générales", {"fields": ("site_name", "site_description")}),
        ("Contact", {"fields": ("contact_email", "contact_phone", "address")}),
        ("Apparence", {"fields": ("logo", "favicon", "primary_color")}),
        ("Maintenance", {"fields": ("maintenance_mode",), "classes": ("collapse",)}),
    )

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Empêche la création de multiples instances."""
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        """Empêche la suppression de l'instance unique."""
        return False
