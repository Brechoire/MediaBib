"""
Admin configuration pour l'app libraries.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Library


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour Library."""

    list_display = ["name", "email", "city", "is_active", "created_at"]
    list_filter = ["is_active", "city", "created_at"]
    search_fields = ["name", "email", "address"]
    ordering = ["-created_at"]
    
    fieldsets = (
        (None, {"fields": ("name", "email", "is_active")}),
        (_("Coordonnées"), {"fields": ("phone", "address", "postal_code", "city")}),
        (_("Dates"), {"fields": ("created_at", "updated_at")}),
    )
    
    readonly_fields = ["created_at", "updated_at"]
